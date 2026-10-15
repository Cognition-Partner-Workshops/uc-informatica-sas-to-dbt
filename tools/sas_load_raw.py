#!/usr/bin/env python3
"""Load the SAS seed CSVs into a DuckDB database as typed source tables.

Shared by tools/sas_baseline.py (in-memory) and the dbt project (persisted
raw schemas in dbt/sas/dev.duckdb, referenced as dbt sources) so both sides
of the parity comparison read identically-typed inputs.

SAS DATE9. strings (e.g. 31JAN2024) are parsed to DATE columns; everything
else keeps pandas/DuckDB type inference. Deterministic and idempotent.

Usage:
    python3 tools/sas_load_raw.py --db dbt/sas/dev.duckdb
"""

import argparse
import os
import re

import duckdb
import pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_ROOT = os.path.join(REPO, "legacy", "sas", "data", "csv")

DATE9 = re.compile(r"^\d{2}[A-Z]{3}\d{4}$")

# schema -> directory under legacy/sas/data/csv
SCHEMAS = {
    "ora_dw": "oracle_dw",
    "raw_bank": "raw_bank",
    "raw_ins": "raw_ins",
    "curated_src": "curated",
}


def read_seed_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    for col in df.columns:
        s = df[col].dropna()
        if len(s) and s.map(lambda v: isinstance(v, str) and bool(DATE9.match(v))).all():
            df[col] = pd.to_datetime(df[col], format="%d%b%Y").dt.date
    return df


def load_all(con: duckdb.DuckDBPyConnection) -> None:
    for schema, subdir in SCHEMAS.items():
        con.execute(f"create schema if not exists {schema}")
        directory = os.path.join(CSV_ROOT, subdir)
        for fname in sorted(os.listdir(directory)):
            if not fname.lower().endswith(".csv"):
                continue
            table = os.path.splitext(fname)[0].lower()
            df = read_seed_csv(os.path.join(directory, fname))
            con.register("_seed_df", df)
            con.execute(f"create or replace table {schema}.{table} as select * from _seed_df")
            con.unregister("_seed_df")
            print(f"  loaded {schema}.{table}: {len(df)} rows")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default=os.path.join(REPO, "dbt", "sas", "dev.duckdb"))
    args = parser.parse_args()
    os.makedirs(os.path.dirname(args.db), exist_ok=True)
    con = duckdb.connect(args.db)
    load_all(con)
    con.close()
    print(f"Raw seed data loaded into {args.db}")


if __name__ == "__main__":
    main()
