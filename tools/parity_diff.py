#!/usr/bin/env python3
"""Row-level parity diff between a legacy baseline and a dbt build output.

Usage:
  python3 tools/parity_diff.py --baseline baseline/sas --actual dbt/sas/dev.duckdb \
      --schema main --keys keys.json --report docs/parity/sas_parity.md

  python3 tools/parity_diff.py --baseline baseline/informatica --actual baseline_actual_dir \
      --keys keys.json --report docs/parity/informatica_parity.md

Baseline: a directory of CSV files, one per legacy target (<TARGET>.csv).
Actual:   either a DuckDB database file (tables looked up by target name, case-insensitive,
          optionally in --schema), a Snowflake database selected with
          ``--actual snowflake --schema <schema>``, or a directory of CSVs with
          matching names. Snowflake connection settings use the SNOWFLAKE_*
          environment variables documented in tools/README.md.
Keys:     JSON mapping target name -> list of key columns used to align rows.

Exit code 0 only if every target matches: identical row counts, identical values in every
shared column (numeric tolerance 1e-6, dates normalized to ISO-8601, strings whitespace-trimmed).
"""
import argparse
import json
import math
import os
import sys
from datetime import date, datetime

import pandas as pd

NUMERIC_TOL = 1e-6


def normalize(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip().upper() for c in df.columns]
    for col in df.columns:
        s = df[col]
        if pd.api.types.is_datetime64_any_dtype(s):
            df[col] = s.dt.strftime("%Y-%m-%d %H:%M:%S").str.replace(" 00:00:00", "", regex=False)
        elif s.dtype == object:
            df[col] = s.map(_norm_cell)
    return df


def _norm_cell(v):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return None
    if isinstance(v, (datetime, date)):
        out = v.isoformat(sep=" ")
        return out[:10] if out.endswith("00:00:00") else out
    if isinstance(v, str):
        return v.strip()
    return v


def load_baseline(path: str) -> dict:
    out = {}
    for f in sorted(os.listdir(path)):
        if f.lower().endswith(".csv"):
            out[os.path.splitext(f)[0].upper()] = normalize(pd.read_csv(os.path.join(path, f)))
    return out


def load_actual(path: str, schema: str) -> dict:
    if path.lower() == "snowflake":
        import snowflake.connector
        from cryptography.hazmat.primitives import serialization

        required = [
            "SNOWFLAKE_ACCOUNT",
            "SNOWFLAKE_USER",
            "SNOWFLAKE_ROLE",
            "SNOWFLAKE_WAREHOUSE",
            "SNOWFLAKE_DATABASE",
            "SNOWFLAKE_PRIVATE_KEY_PATH",
        ]
        missing = [name for name in required if not os.environ.get(name)]
        if missing:
            raise RuntimeError(
                "missing Snowflake environment variables: " + ", ".join(missing)
            )
        if not schema:
            raise RuntimeError("--schema is required when --actual snowflake")

        with open(os.environ["SNOWFLAKE_PRIVATE_KEY_PATH"], "rb") as key_file:
            key = serialization.load_pem_private_key(key_file.read(), password=None)
        private_key = key.private_bytes(
            serialization.Encoding.DER,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
        con = snowflake.connector.connect(
            account=os.environ["SNOWFLAKE_ACCOUNT"],
            user=os.environ["SNOWFLAKE_USER"],
            role=os.environ["SNOWFLAKE_ROLE"],
            warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
            database=os.environ["SNOWFLAKE_DATABASE"],
            schema=schema,
            private_key=private_key,
        )
        out = {}
        cursor = con.cursor()
        cursor.execute(
            """
            select table_name
            from information_schema.tables
            where table_schema = %s
              and table_type = 'BASE TABLE'
            order by table_name
            """,
            (schema.upper(),),
        )
        tables = [row[0] for row in cursor.fetchall()]
        for table in tables:
            cursor.execute(f'select * from "{table}"')
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            out[table.upper()] = normalize(pd.DataFrame(rows, columns=columns))
        cursor.close()
        con.close()
        return out
    if os.path.isdir(path):
        return load_baseline(path)
    import duckdb

    con = duckdb.connect(path, read_only=True)
    out = {}
    rows = con.execute(
        "select table_schema, table_name from information_schema.tables"
    ).fetchall()
    for sch, tbl in rows:
        if schema and sch.lower() != schema.lower():
            continue
        out[tbl.upper()] = normalize(con.execute(f'select * from "{sch}"."{tbl}"').fetch_df())
    con.close()
    return out


def compare(name, base: pd.DataFrame, act: pd.DataFrame, keys: list) -> list:
    problems = []
    keys = [k.upper() for k in keys]
    shared = [c for c in base.columns if c in act.columns]
    missing = [c for c in base.columns if c not in act.columns]
    if missing:
        problems.append(f"columns missing from actual: {missing}")
    if len(base) != len(act):
        problems.append(f"row count mismatch: baseline={len(base)} actual={len(act)}")
    try:
        b = base[shared].sort_values(keys).reset_index(drop=True)
        a = act[shared].sort_values(keys).reset_index(drop=True)
    except KeyError as e:
        problems.append(f"key column missing: {e}")
        return problems
    n = min(len(b), len(a))
    for col in shared:
        bs, as_ = b[col].iloc[:n], a[col].iloc[:n]
        bnum = pd.to_numeric(bs, errors="coerce")
        anum = pd.to_numeric(as_, errors="coerce")
        if bnum.notna().equals(anum.notna()) and bnum.notna().any():
            bad = (bnum - anum).abs() > NUMERIC_TOL
            bad |= bnum.isna() != anum.isna()
        else:
            bad = bs.fillna("\0").astype(str).str.strip() != as_.fillna("\0").astype(str).str.strip()
        if bad.any():
            i = int(bad.idxmax())
            problems.append(
                f"column {col}: {int(bad.sum())}/{n} rows differ "
                f"(first at {dict(b.loc[i, keys])}: baseline={bs.iloc[i]!r} actual={as_.iloc[i]!r})"
            )
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--actual", required=True)
    ap.add_argument("--schema", default="")
    ap.add_argument("--keys", required=True, help="JSON file: target -> [key columns]")
    ap.add_argument("--report", required=True)
    args = ap.parse_args()

    with open(args.keys) as fh:
        keys = {k.upper(): v for k, v in json.load(fh).items()}
    base = load_baseline(args.baseline)
    act = load_actual(args.actual, args.schema)

    lines = ["# Parity Report", "", f"Baseline: `{args.baseline}`  |  Actual: `{args.actual}`", ""]
    ok = True
    for name, bdf in base.items():
        lines.append(f"## {name}")
        if name not in act:
            ok = False
            lines += ["", "**MISSING in actual output**", ""]
            continue
        problems = compare(name, bdf, act[name], keys.get(name, list(bdf.columns[:1])))
        lines.append(f"- rows: baseline={len(bdf)} actual={len(act[name])}")
        lines.append(f"- columns compared: {len([c for c in bdf.columns if c in act[name].columns])}")
        if problems:
            ok = False
            lines.append("- **MISMATCH**:")
            lines += [f"  - {p}" for p in problems]
        else:
            lines.append("- result: **MATCH** (all values within tolerance)")
        lines.append("")
    lines.append(f"**Overall: {'PARITY VERIFIED' if ok else 'PARITY FAILED'}**")

    os.makedirs(os.path.dirname(args.report), exist_ok=True)
    with open(args.report, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
