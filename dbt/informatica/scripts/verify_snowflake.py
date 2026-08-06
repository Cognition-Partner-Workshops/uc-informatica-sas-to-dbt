#!/usr/bin/env python3
"""Emit rerunnable Snowflake object, sample, count, MINUS, and history evidence."""

import argparse
import os
import re
from datetime import datetime, timezone

from cryptography.hazmat.primitives import serialization
import snowflake.connector


TARGETS = (
    "demo_target1_INS",
    "demo_target1_UPD",
    "demo_target2",
    "demo_target21",
    "demo_target3",
    "demo_target5",
    "demo_target6",
)
IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_$]*$")


def qi(identifier):
    if not IDENTIFIER.match(identifier):
        raise ValueError(f"unsafe Snowflake identifier: {identifier!r}")
    return f'"{identifier.upper()}"'


def qs(schema):
    return qi(schema)


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


def run(cursor, sql, parameters=None):
    print(sql)
    cursor.execute(sql, parameters or ())
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    if not rows:
        print("(0 rows)")
    return rows


def columns(cursor, schema, target):
    cursor.execute(
        """
        SELECT COLUMN_NAME, DATA_TYPE
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
        ORDER BY ORDINAL_POSITION
        """,
        (schema.upper(), target.upper()),
    )
    rows = cursor.fetchall()
    if not rows:
        raise RuntimeError(f"no columns found for {schema}.{target}")
    return rows


def select_list(column_rows, rounded_column=None):
    items = []
    for name, data_type in column_rows:
        expression = qi(name)
        if name.upper() == (rounded_column or "").upper():
            expression = f"ROUND({expression}, 6) AS {qi(name)}"
        items.append(expression)
    return ", ".join(items)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--migrated-schema", default="DBT_INFORMATICA_RUN20260806")
    parser.add_argument("--baseline-schema", default="BASELINE_INFORMATICA_RUN20260806")
    parser.add_argument("--history-hours", type=int, default=6)
    args = parser.parse_args()
    con = connect()
    try:
        cursor = con.cursor()
        print("OBJECT_VERIFICATION")
        run(
            cursor,
            f"""
SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA IN ('{args.baseline_schema.upper()}', '{args.migrated_schema.upper()}')
ORDER BY TABLE_SCHEMA, TABLE_NAME
""",
        )
        for target in TARGETS:
            migrated = f"{qs(args.migrated_schema)}.{qi(target)}"
            baseline = f"{qs(args.baseline_schema)}.{qi(target)}"
            column_rows = columns(cursor, args.migrated_schema, target)
            projection = select_list(column_rows)
            print(f"SAMPLE target={target}")
            run(cursor, f"SELECT {projection} FROM {migrated} LIMIT 3")
            print(f"ROW_COUNTS target={target}")
            run(
                cursor,
                f"""
SELECT 'BASELINE' AS SOURCE, COUNT(*) AS ROW_COUNT FROM {baseline}
UNION ALL
SELECT 'MIGRATED' AS SOURCE, COUNT(*) AS ROW_COUNT FROM {migrated}
ORDER BY SOURCE
""",
            )
            print(f"EXACT_MINUS baseline_to_migrated target={target}")
            baseline_to_migrated = run(
                cursor,
                f"SELECT {projection} FROM {baseline} MINUS "
                f"SELECT {projection} FROM {migrated}",
            )
            print(f"EXACT_MINUS migrated_to_baseline target={target}")
            migrated_to_baseline = run(
                cursor,
                f"SELECT {projection} FROM {migrated} MINUS "
                f"SELECT {projection} FROM {baseline}",
            )
            if target == "demo_target6" and (
                baseline_to_migrated or migrated_to_baseline
            ):
                rounded_projection = select_list(column_rows, rounded_column="TX_AMT")
                print("DECISION rounded_second_minus target=demo_target6 column=TX_AMT")
                print("DECISION alternative rejected: changing stored data or model SQL")
                print(f"ROUNDED_MINUS baseline_to_migrated target={target}")
                rounded_left = run(
                    cursor,
                    f"SELECT {rounded_projection} FROM {baseline} MINUS "
                    f"SELECT {rounded_projection} FROM {migrated}",
                )
                print(f"ROUNDED_MINUS migrated_to_baseline target={target}")
                rounded_right = run(
                    cursor,
                    f"SELECT {rounded_projection} FROM {migrated} MINUS "
                    f"SELECT {rounded_projection} FROM {baseline}",
                )
                if rounded_left or rounded_right:
                    raise RuntimeError(
                        "demo_target6 exact MINUS mismatch remains after TX_AMT "
                        "rounding; this is a data finding"
                    )
            elif baseline_to_migrated or migrated_to_baseline:
                raise RuntimeError(f"non-floating MINUS mismatch in {target}")
        history_sql = f"""
SELECT START_TIME, QUERY_ID, USER_NAME, ROLE_NAME, WAREHOUSE_NAME,
       EXECUTION_STATUS, QUERY_TEXT
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY(
    END_TIME_RANGE_START => DATEADD('hour', -{args.history_hours}, CURRENT_TIMESTAMP()),
    RESULT_LIMIT => 10000
))
WHERE USER_NAME = CURRENT_USER()
  AND ROLE_NAME = CURRENT_ROLE()
  AND WAREHOUSE_NAME = CURRENT_WAREHOUSE()
ORDER BY START_TIME
"""
        print("QUERY_HISTORY_SOURCE INFORMATION_SCHEMA.QUERY_HISTORY")
        print(
            "DECISION alternative rejected: ACCOUNT_USAGE.QUERY_HISTORY was not "
            "used because this session requires immediate, session-local history."
        )
        run(cursor, history_sql)
        print(f"EVIDENCE_CAPTURED_AT {datetime.now(timezone.utc).isoformat()}")
    finally:
        con.close()


if __name__ == "__main__":
    main()
