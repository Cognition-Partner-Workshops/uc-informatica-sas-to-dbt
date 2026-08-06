#!/usr/bin/env python3
"""Load Informatica baseline CSVs into type-matched Snowflake tables."""

import argparse
import csv
import os
import re
from pathlib import Path

from cryptography.hazmat.primitives import serialization
import snowflake.connector


REPO_ROOT = Path(__file__).resolve().parents[3]
BASELINE_DIR = REPO_ROOT / "baseline" / "informatica"
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


def quote_identifier(identifier):
    if not IDENTIFIER.match(identifier):
        raise ValueError(f"unsafe Snowflake identifier: {identifier!r}")
    return f'"{identifier.upper()}"'


def quote_schema(schema):
    return quote_identifier(schema)


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


def target_column_types(cursor, migrated_schema, target):
    cursor.execute(
        """
        SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH,
               NUMERIC_PRECISION, NUMERIC_SCALE, DATETIME_PRECISION
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
        ORDER BY ORDINAL_POSITION
        """,
        (migrated_schema.upper(), target.upper()),
    )
    rows = cursor.fetchall()
    if not rows:
        raise RuntimeError(
            f"migrated target {migrated_schema}.{target} has no INFORMATION_SCHEMA columns"
        )
    types = {}
    ordered = []
    for name, data_type, char_len, precision, scale, datetime_precision in rows:
        upper_name = name.upper()
        if upper_name in types:
            raise RuntimeError(f"duplicate migrated column name: {target}.{name}")
        if data_type in {"NUMBER", "DECIMAL", "NUMERIC"}:
            sql_type = f"NUMBER({precision},{scale})"
        elif data_type in {"VARCHAR", "TEXT"}:
            sql_type = "VARCHAR"
        elif data_type.startswith("TIMESTAMP"):
            sql_type = f"{data_type}({datetime_precision})"
        elif data_type == "FIXED":
            sql_type = f"NUMBER({precision},{scale})"
        else:
            sql_type = data_type
        types[upper_name] = sql_type
        ordered.append((name, sql_type))
    return ordered, types


def csv_columns(path):
    with path.open(newline="") as handle:
        return next(csv.reader(handle))


def first_empty_cell(path):
    with path.open(newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        for row_number, row in enumerate(reader, start=2):
            for index, value in enumerate(row):
                if value == "":
                    return header[index], row_number
    return None


def execute_print(cursor, sql, parameters=None):
    print(sql)
    cursor.execute(sql, parameters or ())
    try:
        rows = cursor.fetchall()
    except snowflake.connector.errors.ProgrammingError:
        return []
    for row in rows:
        print(row)
    return rows


def load_target(cursor, baseline_schema, migrated_schema, target):
    csv_path = BASELINE_DIR / f"{target}.csv"
    if not csv_path.exists():
        raise RuntimeError(f"missing baseline CSV: {csv_path}")
    columns, types = target_column_types(cursor, migrated_schema, target)
    source_columns = csv_columns(csv_path)
    migrated_columns = [name for name, _ in columns]
    if [column.upper() for column in source_columns] != [
        column.upper() for column in migrated_columns
    ]:
        raise RuntimeError(
            f"{csv_path.name} column order does not match "
            f"{migrated_schema}.{target}: "
            f"csv={source_columns!r} migrated={migrated_columns!r}"
        )
    missing = [column for column in source_columns if column.upper() not in types]
    if missing:
        raise RuntimeError(
            f"{csv_path.name} columns missing from "
            f"{migrated_schema}.{target}: {missing}"
        )
    table = f"{quote_schema(baseline_schema)}.{quote_identifier(target)}"
    column_sql = ", ".join(
        f"{quote_identifier(name)} {sql_type}" for name, sql_type in columns
    )
    execute_print(cursor, f"CREATE SCHEMA IF NOT EXISTS {quote_schema(baseline_schema)}")
    execute_print(cursor, f"USE SCHEMA {quote_schema(baseline_schema)}")
    execute_print(cursor, f"CREATE OR REPLACE TABLE {table} ({column_sql})")
    file_uri = "file://" + str(csv_path)
    stage = f"@%{quote_identifier(target)}"
    execute_print(
        cursor,
        f"PUT '{file_uri}' {stage} AUTO_COMPRESS=TRUE OVERWRITE=TRUE",
    )
    file_format = (
        "TYPE=CSV SKIP_HEADER=1 FIELD_OPTIONALLY_ENCLOSED_BY='\"' "
        "NULL_IF=('') EMPTY_FIELD_AS_NULL=TRUE"
    )
    execute_print(
        cursor,
        f"COPY INTO {table} FROM {stage} "
        f"FILE_FORMAT=({file_format}) PURGE=TRUE ON_ERROR='ABORT_STATEMENT'",
    )
    execute_print(cursor, f"SELECT COUNT(*) FROM {table}")
    empty = first_empty_cell(csv_path)
    if empty:
        column, row_number = empty
        null_sql = (
            f"SELECT COUNT(*) FROM {table} "
            f"WHERE {quote_identifier(column)} IS NULL"
        )
        print(
            f"NULL_VERIFICATION target={target} column={column} "
            f"source_row={row_number}"
        )
        execute_print(cursor, null_sql)
    print(f"LOADED target={target} source={csv_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "baseline_schema",
        nargs="?",
        default="BASELINE_INFORMATICA_RUN20260806",
    )
    parser.add_argument(
        "--migrated-schema",
        default="DBT_INFORMATICA_RUN20260806",
    )
    args = parser.parse_args()
    con = connect()
    try:
        cursor = con.cursor()
        for target in TARGETS:
            load_target(
                cursor,
                args.baseline_schema,
                args.migrated_schema,
                target,
            )
    finally:
        con.close()


if __name__ == "__main__":
    main()
