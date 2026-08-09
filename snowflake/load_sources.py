import csv
import os
from pathlib import Path

import snowflake.connector


RUN_ID = "20260809T234500Z"
DATABASE = "DEVIN_MIGRATION_DEMO"
SOURCE_SCHEMA = f"SOURCE_INFORMATICA_{RUN_ID}"
TARGET_SCHEMA = f"PYSPARK_INFORMATICA_{RUN_ID}"
BASELINE_SCHEMA = f"BASELINE_INFORMATICA_{RUN_ID}"
SCHEMAS = (SOURCE_SCHEMA, TARGET_SCHEMA, BASELINE_SCHEMA)
SOURCE_DIR = Path("legacy/informatica/data")
SOURCE_NAMES = (
    "demo_source1",
    "demo_source2",
    "demo_source3",
    "demo_source4",
    "demo_source5",
    "demo_target1",
    "lkp_demo_source1",
    "lkp_demo_source2",
    "lkp_demo_source3",
)


def quote_identifier(value: str) -> str:
    return '"' + value.replace('"', '""') + '"'


def connect():
    return snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        role=os.environ["SNOWFLAKE_ROLE"],
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        database=DATABASE,
        private_key_file=os.environ["SNOWFLAKE_PRIVATE_KEY_PATH"],
    )


def main() -> None:
    conn = connect()
    try:
        cur = conn.cursor()
        placeholders = ", ".join(["%s"] * len(SCHEMAS))
        cur.execute(
            f"""
            select schema_name
            from {DATABASE}.information_schema.schemata
            where schema_name in ({placeholders})
            """,
            SCHEMAS,
        )
        existing = {row[0] for row in cur.fetchall()}
        if existing:
            raise RuntimeError(f"Settled schemas already exist: {sorted(existing)}")

        for schema in SCHEMAS:
            cur.execute(f"create schema {DATABASE}.{schema}")

        for logical_name in SOURCE_NAMES:
            path = SOURCE_DIR / f"{logical_name}.csv"
            with path.open(newline="") as handle:
                rows = list(csv.reader(handle))
            columns = rows[0]
            values = [
                tuple(value if value != "" else None for value in row) + (ordinal,)
                for ordinal, row in enumerate(rows[1:])
            ]
            column_sql = ", ".join(
                f"{quote_identifier(column)} varchar" for column in columns
            )
            column_sql += ', "SRC_ORDINAL" number(38,0) not null'
            table = logical_name.upper()
            cur.execute(
                f"create table {DATABASE}.{SOURCE_SCHEMA}.{table} ({column_sql})"
            )
            placeholders = ", ".join(["%s"] * len(columns + ["SRC_ORDINAL"]))
            identifiers = ", ".join(quote_identifier(column) for column in columns)
            identifiers += ', "SRC_ORDINAL"'
            cur.executemany(
                f"insert into {DATABASE}.{SOURCE_SCHEMA}.{table} ({identifiers}) "
                f"values ({placeholders})",
                values,
            )
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    main()
