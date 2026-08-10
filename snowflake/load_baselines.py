import csv
import os
from pathlib import Path

import snowflake.connector


RUN_ID = "20260809T234500Z"
DATABASE = "DEVIN_MIGRATION_DEMO"
TARGET_SCHEMA = f"PYSPARK_INFORMATICA_{RUN_ID}"
BASELINE_SCHEMA = f"BASELINE_INFORMATICA_{RUN_ID}"
BASELINE_DIR = Path("baseline/informatica")
TARGETS = (
    "demo_target1_INS",
    "demo_target1_UPD",
    "demo_target2",
    "demo_target21",
    "demo_target3",
    "demo_target5",
    "demo_target6",
)


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
        cur.execute(f"use schema {DATABASE}.{BASELINE_SCHEMA}")
        for target in TARGETS:
            path = (BASELINE_DIR / f"{target}.csv").resolve()
            with path.open(newline="") as handle:
                header = next(csv.reader(handle))
            cur.execute(
                f"""
                select column_name
                from {DATABASE}.information_schema.columns
                where table_schema = %s and table_name = %s
                order by ordinal_position
                """,
                (TARGET_SCHEMA, target.upper()),
            )
            expected = [row[0] for row in cur.fetchall()]
            if header != expected:
                raise RuntimeError(
                    f"{target}: baseline header {header!r} does not match "
                    f"table columns {expected!r}"
                )

            cur.execute(
                f"create table {DATABASE}.{BASELINE_SCHEMA}.{target.upper()} "
                f"like {DATABASE}.{TARGET_SCHEMA}.{target.upper()}"
            )
            cur.execute(
                f"put 'file://{path}' "
                f"@%{target.upper()} "
                "auto_compress=false overwrite=true"
            )
            put_rows = cur.fetchall()
            copy_sql = (
                f"copy into {DATABASE}.{BASELINE_SCHEMA}.{target.upper()} "
                f"from @%{target.upper()} "
                """file_format=(type=csv skip_header=1
                field_optionally_enclosed_by='"'
                empty_field_as_null=true null_if=(''))"""
                " purge=false"
            )
            cur.execute(copy_sql)
            copy_rows = cur.fetchall()
            errors = [row for row in copy_rows if str(row[1]).upper() != "LOADED"]
            if errors:
                raise RuntimeError(f"{target}: COPY errors: {errors!r}")
            print(f"{target}: PUT={put_rows!r} COPY={copy_rows!r}")
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    main()
