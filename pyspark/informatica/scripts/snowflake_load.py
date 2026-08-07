from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path

import pandas as pd

from informatica_pyspark.config import (
    DEFAULT_SNOWFLAKE_ACCOUNT,
    DEFAULT_SNOWFLAKE_DATABASE,
    DEFAULT_SNOWFLAKE_ROLE,
    DEFAULT_SNOWFLAKE_USER,
    DEFAULT_SNOWFLAKE_WAREHOUSE,
    REPO_ROOT,
)
from informatica_pyspark.io import (
    SOURCE_SCHEMAS,
    TARGET_INSTANCE_SCHEMAS,
    TARGET_SCHEMAS,
    snowflake_connection,
    snowflake_type,
)


SOURCE_TABLES = (
    "demo_source1",
    "demo_source2",
    "demo_source3",
    "demo_source4",
    "demo_source5",
    "lkp_demo_source1",
    "lkp_demo_source2",
    "lkp_demo_source3",
    "demo_target1",
)
DEFAULT_DATA_DIR = REPO_ROOT / "legacy" / "informatica" / "data"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-schema", required=True)
    parser.add_argument("--baseline-schema")
    parser.add_argument("--skip-baseline", action="store_true")
    parser.add_argument("--data-dir", default="legacy/informatica/data")
    parser.add_argument("--baseline-dir", default="baseline/informatica")
    parser.add_argument("--account", default=DEFAULT_SNOWFLAKE_ACCOUNT)
    parser.add_argument("--user", default=DEFAULT_SNOWFLAKE_USER)
    parser.add_argument("--role", default=DEFAULT_SNOWFLAKE_ROLE)
    parser.add_argument("--warehouse", default=DEFAULT_SNOWFLAKE_WAREHOUSE)
    parser.add_argument("--database", default=DEFAULT_SNOWFLAKE_DATABASE)
    return parser


def _connection(args):
    return snowflake_connection(
        account=args.account,
        user=args.user,
        role=args.role,
        warehouse=args.warehouse,
        database=args.database,
    )


def _python_value(value, data_type):
    if pd.isna(value) or value == "":
        return None
    if data_type.simpleString() == "date":
        return pd.Timestamp(value).date()
    if data_type.simpleString() == "timestamp":
        return pd.Timestamp(value).to_pydatetime()
    if data_type.simpleString() == "bigint":
        return int(value)
    if data_type.simpleString() == "double":
        return float(value)
    return str(value)


def _source_path(data_dir: Path, table: str) -> Path:
    override = data_dir / f"{table}.csv"
    return override if override.exists() else DEFAULT_DATA_DIR / f"{table}.csv"


def _load_table(
    connection, database, schema, table, path, definition, include_row_ord=True
):
    frame = pd.read_csv(
        path,
        dtype="string",
        keep_default_na=False,
        na_values=[""],
        skipinitialspace=False,
    )
    expected_columns = [field.name for field in definition.fields]
    if list(frame.columns) != expected_columns:
        raise ValueError(
            f"{path}: expected columns {expected_columns}, got {list(frame.columns)}"
        )
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {database}.{schema}")
        columns = ", ".join(
            f"{field.name.upper()} {snowflake_type(field.dataType)}"
            for field in definition.fields
        )
        if include_row_ord:
            columns += ", __ROW_ORD NUMBER(38,0)"
        cursor.execute(
            f"CREATE OR REPLACE TABLE {database}.{schema}.{table.upper()} "
            f"({columns})"
        )
        names = [field.name.upper() for field in definition.fields]
        if include_row_ord:
            names.append("__ROW_ORD")
        placeholders = ", ".join(["%s"] * len(names))
        rows = [
            tuple(
                [_python_value(row[field.name], field.dataType) for field in definition.fields]
                + ([index] if include_row_ord else [])
            )
            for index, (_, row) in enumerate(frame.iterrows())
        ]
        if rows:
            cursor.executemany(
                f"INSERT INTO {database}.{schema}.{table.upper()} "
                f"({', '.join(names)}) VALUES ({placeholders})",
                rows,
            )
        connection.commit()
        print(f"loaded {schema}.{table}: {len(rows)} rows")
    finally:
        cursor.close()


def main(argv=None):
    args = _parser().parse_args(argv)
    if not args.skip_baseline and not args.baseline_schema:
        _parser().error("--baseline-schema is required unless --skip-baseline is set")
    data_dir = Path(args.data_dir)
    baseline_dir = Path(args.baseline_dir)
    connection = _connection(args)
    try:
        for table in SOURCE_TABLES:
            definition = (
                SOURCE_SCHEMAS[table]
                if table in SOURCE_SCHEMAS
                else TARGET_SCHEMAS[table]
            )
            _load_table(
                connection,
                args.database,
                args.source_schema,
                table,
                _source_path(data_dir, table),
                definition,
            )
        if not args.skip_baseline:
            for table, definition in TARGET_INSTANCE_SCHEMAS.items():
                _load_table(
                    connection,
                    args.database,
                    args.baseline_schema,
                    table,
                    baseline_dir / f"{table}.csv",
                    definition,
                    include_row_ord=False,
                )
    finally:
        connection.close()


if __name__ == "__main__":
    main()
