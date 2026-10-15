#!/usr/bin/env python3
"""Snowflake wrapper around tools/parity_diff.py.

Exports the requested targets from the run's BASELINE_<token> schema (legacy answer) and
DBT_<token> schema (dbt build) to CSV directories, then runs tools/parity_diff.py on them
unchanged (same normalization, same tolerances, same report format and exit code).

Usage:
  python3 tools/parity_snowflake.py --targets CUST_ACCOUNTS_DAILY,ACCT_EXCEPTIONS \
      --keys tools/keys/sas_keys.json \
      --report docs/parity/sas_load_customer_accounts_snowflake_parity.md

Connection comes from the environment only: SNOWFLAKE_ACCOUNT, SNOWFLAKE_HOST (optional but
needed when the account is a bare locator), SF_DEMO_USER, SF_DEMO_PASSWORD, SF_DEMO_ROLE,
SF_DEMO_WAREHOUSE, SF_DEMO_DATABASE, SF_RUN_TOKEN.
"""
import argparse
import glob
import os
import subprocess
import sys
import tempfile
from datetime import date, datetime
from decimal import Decimal

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from parity_diff import normalize  # noqa: E402


def connect():
    import snowflake.connector

    kw = dict(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SF_DEMO_USER"],
        password=os.environ["SF_DEMO_PASSWORD"],
        role=os.environ["SF_DEMO_ROLE"],
        warehouse=os.environ["SF_DEMO_WAREHOUSE"],
        database=os.environ["SF_DEMO_DATABASE"],
    )
    if os.environ.get("SNOWFLAKE_HOST"):
        kw["host"] = os.environ["SNOWFLAKE_HOST"]
    return snowflake.connector.connect(**kw)


def _cell(v):
    # The connector returns datetime.date / Decimal objects; render them the way the
    # baseline CSVs and parity_diff.normalize do (ISO dates, midnight time dropped).
    if isinstance(v, datetime):
        out = v.isoformat(sep=" ")
        return out[:10] if out.endswith("00:00:00") else out
    if isinstance(v, date):
        return v.isoformat()
    if isinstance(v, Decimal):
        return float(v)
    return v


def export(cur, database, schema, table, out_dir):
    exists = cur.execute(
        "select count(*) from information_schema.tables where table_schema = %s and table_name = %s",
        (schema, table),
    ).fetchone()[0]
    if not exists:
        return None
    cur.execute(f'select * from "{database}"."{schema}"."{table}"')
    cols = [d[0] for d in cur.description]
    rows = [[_cell(v) for v in r] for r in cur.fetchall()]
    df = normalize(pd.DataFrame(rows, columns=cols))
    df.to_csv(os.path.join(out_dir, f"{table}.csv"), index=False)
    return len(df)


def main():
    token = os.environ.get("SF_RUN_TOKEN", "")
    ap = argparse.ArgumentParser()
    ap.add_argument("--targets", required=True, help="comma-separated legacy target names")
    ap.add_argument("--keys", required=True)
    ap.add_argument("--report", required=True)
    ap.add_argument("--baseline-schema", default=f"BASELINE_{token}")
    ap.add_argument("--actual-schema", default=f"DBT_{token}")
    ap.add_argument("--workdir", default=None, help="keep the exported CSVs here")
    args = ap.parse_args()

    targets = [t.strip().upper() for t in args.targets.split(",") if t.strip()]
    work = args.workdir or tempfile.mkdtemp(prefix="parity_sf_")
    base_dir, act_dir = os.path.join(work, "baseline"), os.path.join(work, "actual")
    for d in (base_dir, act_dir):
        os.makedirs(d, exist_ok=True)
        # parity_diff compares every CSV it finds, so a reused workdir must start clean
        for old in glob.glob(os.path.join(d, "*.csv")):
            os.remove(old)

    database = os.environ["SF_DEMO_DATABASE"]
    con = connect()
    cur = con.cursor()
    for t in targets:
        n_base = export(cur, database, args.baseline_schema.upper(), t, base_dir)
        if n_base is None:
            sys.exit(f"baseline table {args.baseline_schema}.{t} not found")
        n_act = export(cur, database, args.actual_schema.upper(), t, act_dir)
        print(f"exported {t}: baseline={n_base} actual={'MISSING' if n_act is None else n_act}")
    con.close()

    rc = subprocess.call([
        sys.executable, os.path.join(HERE, "parity_diff.py"),
        "--baseline", base_dir, "--actual", act_dir,
        "--keys", args.keys, "--report", args.report,
    ])
    sys.exit(rc)


if __name__ == "__main__":
    main()
