#!/usr/bin/env python3
"""Snowflake path for tools/parity_diff.py.

parity_diff.py reads a CSV directory (baseline) and a CSV directory or DuckDB
file (actual). This wrapper exports the named tables from two Snowflake
schemas into CSV directories and runs parity_diff.py on them unchanged, so the
comparison and its tolerances stay the ones in parity_diff.py.

  python3 tools/parity_diff_snowflake.py \
      --baseline-schema BASELINE_SF_20261015_DS --actual-schema SCAI_SF_20261015_DS \
      --tables DEMO_TARGET3 DEMO_TARGET5 DEMO_TARGET6 \
      --keys tools/keys/informatica_keys.json \
      --report docs/parity/m_demo_mapping1_snowflake_parity.md

Connection comes from the environment: SNOWFLAKE_ACCOUNT, SNOWFLAKE_HOST,
SF_DEMO_USER, SF_DEMO_PASSWORD, SF_DEMO_ROLE, SF_DEMO_WAREHOUSE, SF_DEMO_DATABASE.
"""
import argparse
import os
import subprocess
import sys
import shutil
import tempfile
from datetime import date, datetime

import pandas as pd
import snowflake.connector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import parity_diff  # noqa: E402


def _ts(v):
    try:
        return datetime.fromisoformat(v)
    except (TypeError, ValueError):
        return v


def export(cur, schema: str, tables: list, out_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True)
    for t in tables:
        cur.execute(
            "select column_name, data_type from information_schema.columns "
            "where table_schema = %s and table_name = %s order by ordinal_position",
            (schema, t.upper()),
        )
        cols = cur.fetchall()
        # Timestamps are read as text: some loaded values lie past year 9999, which Python
        # datetimes cannot hold; those stay as Snowflake renders them.
        select = ", ".join(
            f"to_varchar(\"{c}\", 'YYYY-MM-DD HH24:MI:SS') as \"{c}\"" if d.startswith("TIMESTAMP") else f'"{c}"'
            for c, d in cols
        )
        cur.execute(f'select {select} from "{schema}"."{t.upper()}"')
        df = pd.DataFrame(cur.fetchall(), columns=[c for c, _ in cols])
        for c, d in cols:
            if d.startswith("TIMESTAMP"):
                df[c] = df[c].map(_ts)
        # DATE arrives as datetime.date; hand parity_diff timestamps as DuckDB does, then
        # apply its normalisation (dates/timestamps -> ISO text).
        df = df.map(lambda v: pd.Timestamp(v) if type(v) is date else v)
        parity_diff.normalize(df).to_csv(os.path.join(out_dir, f"{t}.csv"), index=False)


def copy_csv(src_dir: str, tables: list, out_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True)
    for t in tables:
        shutil.copy(os.path.join(src_dir, f"{t}.csv"), os.path.join(out_dir, f"{t}.csv"))


def main():
    ap = argparse.ArgumentParser()
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--baseline-schema", help="Snowflake schema holding the baseline tables")
    src.add_argument("--baseline-csv", help="baseline CSV directory, e.g. baseline/informatica")
    ap.add_argument("--actual-schema", required=True)
    ap.add_argument("--tables", nargs="+", required=True)
    ap.add_argument("--keys", required=True)
    ap.add_argument("--report", required=True)
    args = ap.parse_args()

    e = os.environ
    con = snowflake.connector.connect(
        account=e["SNOWFLAKE_ACCOUNT"], host=e["SNOWFLAKE_HOST"],
        user=e["SF_DEMO_USER"], password=e["SF_DEMO_PASSWORD"], role=e["SF_DEMO_ROLE"],
        warehouse=e["SF_DEMO_WAREHOUSE"], database=e["SF_DEMO_DATABASE"],
    )
    with tempfile.TemporaryDirectory() as tmp:
        base = (os.path.join("snowflake", args.baseline_schema) if args.baseline_schema
                else os.path.normpath(args.baseline_csv))
        act = os.path.join("snowflake", args.actual_schema)
        cur = con.cursor()
        if args.baseline_schema:
            export(cur, args.baseline_schema, args.tables, os.path.join(tmp, base))
        else:
            copy_csv(args.baseline_csv, args.tables, os.path.join(tmp, base))
        export(cur, args.actual_schema, args.tables, os.path.join(tmp, act))
        con.close()
        rc = subprocess.call(
            [sys.executable, os.path.join(HERE, "parity_diff.py"),
             "--baseline", base, "--actual", act,
             "--keys", os.path.abspath(args.keys), "--report", os.path.abspath(args.report)],
            cwd=tmp,
        )
    sys.exit(rc)


if __name__ == "__main__":
    main()
