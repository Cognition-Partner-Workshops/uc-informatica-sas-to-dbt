#!/usr/bin/env python3
"""Export Snowflake marts and invoke the unmodified parity comparator."""

import argparse
import csv
import os
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

from cryptography.hazmat.primitives import serialization
import snowflake.connector


REPO_ROOT = Path(__file__).resolve().parents[3]
TARGETS = (
    "demo_target1_INS",
    "demo_target1_UPD",
    "demo_target2",
    "demo_target21",
    "demo_target3",
    "demo_target5",
    "demo_target6",
)


def csv_value(value):
    if value is None:
        return ""
    if isinstance(value, datetime):
        if value.time().isoformat() == "00:00:00":
            return value.date().isoformat()
        return value.isoformat(sep=" ")
    if isinstance(value, date):
        return value.isoformat()
    return value


def connect():
    key_path = os.environ.get("SNOWFLAKE_PRIVATE_KEY_PATH")
    if not key_path:
        raise RuntimeError("SNOWFLAKE_PRIVATE_KEY_PATH is required")
    with open(key_path, "rb") as handle:
        key = serialization.load_pem_private_key(handle.read(), password=None)
    private_key = key.private_bytes(
        serialization.Encoding.DER,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )
    return snowflake.connector.connect(
        account=os.environ.get("SNOWFLAKE_ACCOUNT", "YD76133.us-east-2.aws"),
        user=os.environ.get("SNOWFLAKE_USER", "devin_demo"),
        role=os.environ.get("SNOWFLAKE_ROLE", "devin_migration_demo"),
        warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE", "devin_demo_wh"),
        database=os.environ.get("SNOWFLAKE_DATABASE", "devin_migration_demo"),
        private_key=private_key,
    )


def export_targets(schema, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    con = connect()
    try:
        cursor = con.cursor()
        for target in TARGETS:
            sql = f'SELECT * FROM "{schema.upper()}"."{target.upper()}"'
            print(sql)
            cursor.execute(sql)
            rows = cursor.fetchall()
            headers = [description[0] for description in cursor.description]
            path = output_dir / f"{target}.csv"
            with path.open("w", newline="") as handle:
                writer = csv.writer(handle, lineterminator="\n")
                writer.writerow(headers)
                writer.writerows(
                    [[csv_value(value) for value in row] for row in rows]
                )
            print(f"EXPORTED {target} rows={len(rows)} path={path}")
    finally:
        con.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--migrated-schema",
        default="DBT_INFORMATICA_RUN20260806",
    )
    parser.add_argument(
        "--output-dir",
        default=str(REPO_ROOT / "evidence" / "snowflake_actual"),
    )
    parser.add_argument(
        "--report",
        default=str(REPO_ROOT / "docs" / "parity" / "informatica_parity_snowflake.md"),
    )
    args = parser.parse_args()
    output_dir = Path(args.output_dir)
    report = Path(args.report)
    export_targets(args.migrated_schema, output_dir)
    command = [
        sys.executable,
        str(REPO_ROOT / "tools" / "parity_diff.py"),
        "--baseline",
        str(REPO_ROOT / "baseline" / "informatica"),
        "--actual",
        str(output_dir),
        "--keys",
        str(REPO_ROOT / "tools" / "keys" / "informatica_keys.json"),
        "--report",
        str(report),
    ]
    print("RUN_COMPARATOR " + " ".join(command))
    completed = subprocess.run(command, cwd=REPO_ROOT)
    print(f"COMPARATOR_EXIT_CODE {completed.returncode}")
    raise SystemExit(completed.returncode)


if __name__ == "__main__":
    main()
