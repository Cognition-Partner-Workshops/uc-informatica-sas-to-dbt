#!/usr/bin/env python3
"""Load and dual-run m_demo_mapping2 in its pre-provisioned SFNFR schemas.

Run from the repository root with SFNFR_ACCOUNT/USER/ROLE/PRIVATE_KEY bound.
No infrastructure is created. CSV types and timestamp formats are explicit.
The baseline is replayed from SRC, not independently reread seed inputs.
"""

import argparse
import csv
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime
from decimal import Decimal
from pathlib import Path

import duckdb
import informatica_baseline as baseline
import snowflake.connector
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    load_pem_private_key,
)

ROOT = Path(__file__).resolve().parents[1]
DATABASE = "SFNFR_20261104"
SRC = "INFA_ACCTDIM_SRC_SFNFR_20261104"
LEGACY = "INFA_ACCTDIM_LEGACY_SFNFR_20261104"
SF = "INFA_ACCTDIM_SF_SFNFR_20261104"
WAREHOUSE = "WH_INFA_ACCTDIM"
SOURCE_COLUMNS = [
    (c, "VARCHAR")
    for c in (
        "LEAD_CO_MNE",
        "BRANCH_CO_MNE",
        "MIS_DATE",
        "ID",
        "DESCRIPTION",
        "SHORT_NAME",
    )
]
TARGET_COLUMNS = (
    [("KEY", "NUMBER(38,0)")]
    + SOURCE_COLUMNS
    + [
        ("CREATED_BY", "VARCHAR"),
        ("CREATED_TIME", "TIMESTAMP_NTZ(6)"),
        ("UPDATED_BY", "VARCHAR"),
        ("UPDATED_TIME", "TIMESTAMP_NTZ(6)"),
        ("ACTIVE_FLAG", "VARCHAR"),
        ("START_DATE", "TIMESTAMP_NTZ(6)"),
        ("END_DATE", "TIMESTAMP_NTZ(6)"),
    ]
)
OUTPUTS = ("DEMO_TARGET1_INS", "DEMO_TARGET1_UPD")
INPUTS = ("DEMO_SOURCE1", "DEMO_TARGET1")
REPORT = ROOT / "docs/parity/m_demo_mapping2_snowflake_parity.md"


def connect():
    key = load_pem_private_key(os.environ["SFNFR_PRIVATE_KEY"].encode(), password=None)
    return snowflake.connector.connect(
        account=os.environ["SFNFR_ACCOUNT"],
        user=os.environ["SFNFR_USER"],
        role=os.environ["SFNFR_ROLE"],
        private_key=key.private_bytes(
            Encoding.DER, PrivateFormat.PKCS8, NoEncryption()
        ),
        authenticator="SNOWFLAKE_JWT",
        database=DATABASE,
        warehouse=WAREHOUSE,
        session_parameters={"QUERY_TAG": "RUN:SFNFR_20261104;m_demo_mapping2"},
    )


def fqn(schema, table):
    return f"{DATABASE}.{schema}.{table}"


def csv_rows(path, columns):
    with path.open(newline="") as stream:
        reader = csv.DictReader(stream)
        if [c.upper() for c in (reader.fieldnames or [])] != [c for c, _ in columns]:
            raise ValueError(f"Unexpected column order: {path}")
        rows = []
        for row in reader:
            values = []
            for (_, kind), raw in zip(columns, row.values()):
                value: str | Decimal | None
                if raw == "":
                    value = None
                elif kind.startswith("TIMESTAMP"):
                    value = datetime.fromisoformat(raw).strftime("%Y-%m-%d %H:%M:%S.%f")
                elif kind.startswith("NUMBER"):
                    value = Decimal(raw)
                else:
                    value = raw
                values.append(value)
            rows.append(values)
    return rows


def load_table(cur, schema, table, columns, rows):
    definition = ", ".join(f'"{c}" {t}' for c, t in columns)
    cur.execute(f"CREATE OR REPLACE TABLE {fqn(schema, table)} ({definition})")
    binds = ", ".join(
        "TO_TIMESTAMP_NTZ(%s, 'YYYY-MM-DD HH24:MI:SS.FF6')"
        if t.startswith("TIMESTAMP")
        else "%s"
        for _, t in columns
    )
    if rows:
        cur.executemany(f"INSERT INTO {fqn(schema, table)} VALUES ({binds})", rows)
    print(f"loaded {fqn(schema, table)}: {len(rows)} rows")


def replay_from_src(cur):
    """Replay the unchanged baseline mapping with the warehouse's exact inputs."""
    with duckdb.connect() as con:
        for table, columns in (
            ("DEMO_SOURCE1", SOURCE_COLUMNS),
            ("DEMO_TARGET1", TARGET_COLUMNS),
        ):
            names = ", ".join(f'"{c}"' for c, _ in columns)
            extra = ', "__SEED_ROW"' if table == "DEMO_TARGET1" else ""
            rows = cur.execute(
                f"SELECT {names}{extra} FROM {fqn(SRC, table)}"
            ).fetchall()
            destination = "demo_target1_pre_raw" if extra else "demo_source1"
            fields = columns + ([("__SEED_ROW", "NUMBER(38,0)")] if extra else [])
            definition = ", ".join(
                f'"{c}" '
                + (
                    "TIMESTAMP"
                    if t.startswith("TIMESTAMP")
                    else "DOUBLE"
                    if t.startswith("NUMBER")
                    else "VARCHAR"
                )
                for c, t in fields
            )
            # The baseline references the mixed-case legacy Key identifier.
            definition = definition.replace('"KEY"', '"Key"')
            con.execute(f"CREATE TABLE {destination} ({definition})")
            if rows:
                con.executemany(
                    f"INSERT INTO {destination} VALUES ({','.join('?' for _ in fields)})",
                    rows,
                )
        con.execute("""CREATE TEMP VIEW demo_target1_pre AS
            SELECT * EXCLUDE (__SEED_ROW, rn) FROM (
                SELECT *, ROW_NUMBER() OVER (
                    PARTITION BY ID ORDER BY "Key" DESC, __SEED_ROW DESC
                ) rn FROM demo_target1_pre_raw
            ) WHERE rn = 1""")
        baseline.mapping2(con)


def load(cur):
    subprocess.run(
        [sys.executable, "tools/informatica_baseline.py"], cwd=ROOT, check=True
    )
    seeded = {
        t: (
            ROOT / "baseline/informatica" / f"{t.lower()[:-3]}{t[-3:]}.csv"
        ).read_bytes()
        for t in OUTPUTS
    }
    for table, columns in (
        ("DEMO_SOURCE1", SOURCE_COLUMNS),
        ("DEMO_TARGET1", TARGET_COLUMNS),
    ):
        rows = csv_rows(
            ROOT / "legacy/informatica/data" / f"{table.lower()}.csv", columns
        )
        if table == "DEMO_TARGET1":
            columns = columns + [("__SEED_ROW", "NUMBER(38,0)")]
            rows = [row + [i] for i, row in enumerate(rows, start=1)]
        load_table(cur, SRC, table, columns, rows)
    replay_from_src(cur)
    for table in OUTPUTS:
        path = ROOT / "baseline/informatica" / f"{table.lower()[:-3]}{table[-3:]}.csv"
        if path.read_bytes() != seeded[table]:
            raise ValueError(
                f"SRC replay differs from the frozen seed baseline: {table}"
            )
        load_table(cur, LEGACY, table, TARGET_COLUMNS, csv_rows(path, TARGET_COLUMNS))


def canonical_sql(schema, table):
    cells = []
    for column, kind in TARGET_COLUMNS:
        col = f'"{column}"'
        if kind.startswith("NUMBER"):
            value = f"TO_VARCHAR(ROUND(CAST({col} AS NUMBER(38,6)), 6))"
        elif kind.startswith("TIMESTAMP"):
            value = f"TO_CHAR({col}, 'YYYY-MM-DD HH24:MI:SS.FF6')"
        else:
            value = f"TRIM({col})"
        cells.append(f"COALESCE({value}, '\\\\N')")
    return f"SELECT ID, CONCAT_WS('|', {', '.join(cells)}) AS canonical FROM {fqn(schema, table)}"


def profile(cur, schema, table):
    expressions = []
    for col, kind in TARGET_COLUMNS:
        c = f'"{col}"'
        expressions.extend(
            [f"COUNT({c})", f"COUNT(DISTINCT {c})", f"MIN({c})", f"MAX({c})"]
        )
        expressions.append(
            f"SUM({c})"
            if kind.startswith("NUMBER")
            else f"SUM(LENGTH({c}))"
            if kind == "VARCHAR"
            else "NULL"
        )
    return cur.execute(
        f"SELECT {', '.join(expressions)} FROM {fqn(schema, table)}"
    ).fetchone()


def canonical_diff(cur, table, rows_in):
    expected_columns = [c for c, _ in TARGET_COLUMNS]
    for schema in (LEGACY, SF):
        columns = cur.execute(
            f"SELECT COLUMN_NAME FROM {DATABASE}.INFORMATION_SCHEMA.COLUMNS "
            "WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s ORDER BY ORDINAL_POSITION",
            (schema, table),
        ).fetchall()
        if [row[0] for row in columns] != expected_columns:
            raise ValueError(f"Legacy column order mismatch: {fqn(schema, table)}")
    left, right = canonical_sql(LEGACY, table), canonical_sql(SF, table)
    result = {
        "table": table,
        "legacy_fqn": fqn(LEGACY, table),
        "new_fqn": fqn(SF, table),
        "key_columns": ["ID"],
        "rows_in": rows_in,
    }
    for label, query in (("legacy", left), ("new", right)):
        count, checksum = cur.execute(
            f"SELECT COUNT(*), HASH_AGG(canonical) FROM ({query})"
        ).fetchone()
        result[f"{label}_rows"] = count
        result[f"{label}_checksum"] = str(checksum)
    keyed = cur.execute(f"""WITH b AS ({left}), a AS ({right})
        SELECT COUNT(*) FROM b FULL OUTER JOIN a ON EQUAL_NULL(b.ID, a.ID)
        WHERE b.canonical IS NULL OR a.canonical IS NULL
           OR MD5(b.canonical) != MD5(a.canonical)""").fetchone()[0]
    bag = f"""WITH b AS ({left}), a AS ({right}),
        bm AS (SELECT canonical, ROW_NUMBER() OVER (
            PARTITION BY canonical ORDER BY canonical) occurrence FROM b),
        am AS (SELECT canonical, ROW_NUMBER() OVER (
            PARTITION BY canonical ORDER BY canonical) occurrence FROM a)"""
    removed = cur.execute(
        bag + " SELECT COUNT(*) FROM (SELECT * FROM bm EXCEPT SELECT * FROM am)"
    ).fetchone()[0]
    added = cur.execute(
        bag + " SELECT COUNT(*) FROM (SELECT * FROM am EXCEPT SELECT * FROM bm)"
    ).fetchone()[0]
    result.update(
        keyed_mismatches=keyed,
        legacy_only=removed,
        new_only=added,
        mismatches=max(keyed, removed, added),
        profile_matches=profile(cur, LEGACY, table) == profile(cur, SF, table),
    )
    return result


def export(cur, schema, table, path):
    names = ", ".join(f'"{c}"' for c, _ in TARGET_COLUMNS)
    rows = cur.execute(
        f"SELECT {names} FROM {fqn(schema, table)} ORDER BY ID"
    ).fetchall()
    with path.open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(c for c, _ in TARGET_COLUMNS)
        for row in rows:
            writer.writerow(
                value.isoformat(sep=" ") if isinstance(value, datetime) else value
                for value in row
            )


def parity(cur):
    counts = {
        t: cur.execute(f"SELECT COUNT(*) FROM {fqn(SRC, t)}").fetchone()[0]
        for t in INPUTS
    }
    results = [canonical_diff(cur, table, sum(counts.values())) for table in OUTPUTS]
    run_results = json.loads(
        (ROOT / "dbt/m_demo_mapping2/target/run_results.json").read_text()
    )["results"]
    dbt_ok = all(r["status"] in ("success", "pass") for r in run_results)
    dbt_summary = f"PASS={sum(r['status'] in ('success', 'pass') for r in run_results)} TOTAL={len(run_results)}"
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="infa_acctdim_parity_") as work:
        base, actual = Path(work) / "legacy", Path(work) / "new"
        base.mkdir()
        actual.mkdir()
        for table in OUTPUTS:
            export(cur, LEGACY, table, base / f"{table}.csv")
            export(cur, SF, table, actual / f"{table}.csv")
        tool_report = Path(work) / "parity_diff.md"
        process = subprocess.run(
            [
                sys.executable,
                "tools/parity_diff.py",
                "--baseline",
                str(base),
                "--actual",
                str(actual),
                "--keys",
                "tools/keys/informatica_keys.json",
                "--report",
                str(tool_report),
            ],
            cwd=ROOT,
            check=False,
        )
        comparison = (
            tool_report.read_text()
            .replace(str(base), "LEGACY export")
            .replace(str(actual), "SF export")
        )
    payload = {
        "job": "informatica_account_dim",
        "outputs": results,
        "input_tables": [fqn(SRC, t) for t in INPUTS],
        "input_counts": counts,
        "parity_diff_exit_code": process.returncode,
        "dbt_summary": dbt_summary,
        "explained_mismatches": "None",
    }
    REPORT.with_suffix(".json").write_text(json.dumps(payload, indent=2) + "\n")
    lines = [
        "# m_demo_mapping2 — Snowflake dual-run parity",
        "",
        "Frozen business date: **2024-01-31**. Warehouse: `WH_INFA_ACCTDIM`.",
        "",
        "## Input identity",
        "",
        "The loader runs the unchanged baseline on the seeds, loads typed SRC tables,",
        "replays `informatica_baseline.mapping2` from those exact Snowflake SRC rows,",
        "and asserts byte-identical output before loading LEGACY. dbt reads the same SRC.",
        "",
        *[f"- `{fqn(SRC, t)}`: {n} rows" for t, n in counts.items()],
        "",
        "`rows in` is the total physical input cardinality, including the duplicate lookup row.",
        "",
        f"LEGACY: `{DATABASE}.{LEGACY}`. New: `{DATABASE}.{SF}`.",
        "",
        "## Canonical Snowflake comparison",
        "",
        "| output | rows in | legacy rows | new rows | mismatches | legacy checksum | new checksum |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for r in results:
        lines.append(
            "| "
            + " | ".join(
                str(r[k])
                for k in (
                    "table",
                    "rows_in",
                    "legacy_rows",
                    "new_rows",
                    "mismatches",
                    "legacy_checksum",
                    "new_checksum",
                )
            )
            + " |"
        )
    lines += [
        "",
        "Business key: `ID` for both outputs. Columns follow the XML target order.",
        "",
        "Each canonical row uses NULL → `\\N`, numbers → `TO_VARCHAR(ROUND(CAST(x AS NUMBER(38,6)),6))`,",
        "timestamps → `YYYY-MM-DD HH24:MI:SS.FF6`, strings → `TRIM(x)`, joined by `|`.",
        "Table checksum is Snowflake `HASH_AGG(canonical)`; row hash is `MD5(canonical)`.",
        "A keyed full outer join compares row hashes. Both multiset EXCEPT directions",
        "compare `(canonical, occurrence)` to retain duplicate multiplicity.",
        "",
        "| output | keyed diff | legacy-only multiset | new-only multiset | L2 profiles equal |",
        "|---|---:|---:|---:|---|",
    ]
    for r in results:
        lines.append(
            f"| {r['table']} | {r['keyed_mismatches']} | {r['legacy_only']} | "
            f"{r['new_only']} | {r['profile_matches']} |"
        )
    lines += [
        "",
        "L2 compares non-null counts, distinct counts, min/max for every column,",
        "numeric sums and string total lengths. L4: no differing rows when all counts are zero.",
        "Stored column names and order are checked against the legacy target definition.",
        "",
        "## dbt build",
        "",
        f"`{dbt_summary}` (from local `target/run_results.json`).",
        "The build includes key/domain/relationship tests and unit fixtures for the legacy",
        "always-update anomaly and duplicate lookup selection.",
        "",
        "## Legacy anomalies (not mismatches)",
        "",
        "- XML EXPTRANS compares AES_DECRYPT output to MD5. As documented by the supplied",
        "  baseline, every lookup-matched row updates; this is not repaired into normal SCD2 logic.",
        "- LKPTRANS Use Any Value is frozen to highest Key, then last physical seed row.",
        "- SEQTRANS Current Value 57 yields insert keys starting at 57 in ID order.",
        "- Unconnected ports remain NULL: ACTIVE_FLAG/START_DATE/END_DATE in both branches,",
        "  UPDATED_* on inserts and CREATED_* on updates. No dimension merge is performed.",
        "- MIS_DATE remains VARCHAR; source state END_DATE 9999-12-31 is TIMESTAMP_NTZ(6).",
        "",
        "Explained mismatches: none.",
        "",
        "## Unchanged parity_diff.py result",
        "",
        comparison,
        "## Exact canonical SQL (legacy; change only schema to compare new)",
        "",
        "```sql",
        canonical_sql(LEGACY, OUTPUTS[0]) + ";",
        "```",
        "",
        "## Rerun",
        "",
        "Bind SFNFR_ACCOUNT, SFNFR_USER, SFNFR_ROLE and SFNFR_PRIVATE_KEY securely,",
        "then run from the repository root (no secrets are written to disk):",
        "",
        "```sh",
        "~/sfenv/bin/python tools/informatica_account_dim_snowflake.py load",
        "~/dbtenv/bin/dbt build --project-dir dbt/m_demo_mapping2 --profiles-dir dbt/m_demo_mapping2 --target snowflake",
        "~/sfenv/bin/python tools/informatica_account_dim_snowflake.py parity",
        "```",
        "",
    ]
    REPORT.write_text("\n".join(lines))
    print(json.dumps(payload, indent=2))
    if (
        not dbt_ok
        or process.returncode
        or any(
            r["mismatches"]
            or not r["profile_matches"]
            or r["legacy_rows"] != r["new_rows"]
            or r["legacy_checksum"] != r["new_checksum"]
            for r in results
        )
    ):
        raise SystemExit(1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("load", "parity"))
    args = parser.parse_args()
    os.chdir(ROOT)
    with connect() as con, con.cursor() as cur:
        if args.action == "load":
            load(cur)
        else:
            parity(cur)


if __name__ == "__main__":
    main()
