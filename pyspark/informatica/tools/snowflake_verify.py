"""Verify an existing milestone-E Snowflake run."""

import argparse
from pathlib import Path

import snowflake.connector
from pyspark.sql import Row

from informatica_pyspark.config import RunConfig
from informatica_pyspark.io import SnowflakeIO
from informatica_pyspark.session import build_spark
from snowflake_milestone_e import (
    ACCOUNT,
    DATABASE,
    ROLE,
    TARGETS,
    USER,
    WAREHOUSE,
    connect,
    history_sql,
    proof_sql,
    runtime_key,
    schema_name,
)


def history_variants():
    yield "query_history", history_sql()
    yield (
        "query_history_by_user",
        "select query_id, query_text, start_time, end_time, rows_produced, "
        "warehouse_name, execution_status from table("
        "devin_migration_demo.information_schema.query_history_by_user("
        "user_name => current_user(), result_limit => 200)) "
        "order by start_time desc",
    )
    yield (
        "query_history_by_warehouse",
        "select query_id, query_text, start_time, end_time, rows_produced, "
        "warehouse_name, execution_status from table("
        "devin_migration_demo.information_schema.query_history_by_warehouse("
        "warehouse_name => current_warehouse(), result_limit => 200)) "
        "order by start_time desc",
    )


def run_spark_round_trip(key_path, source_schema, migrated_schema, jars_dir):
    cfg = RunConfig(
        io="snowflake",
        account=ACCOUNT,
        user=USER,
        role=ROLE,
        warehouse=WAREHOUSE,
        database=DATABASE,
        source_schema=source_schema,
        migrated_target_schema=migrated_schema,
        private_key_path=key_path,
        snowflake_jars_dir=jars_dir,
    )
    spark = build_spark(cfg)
    try:
        frame = spark.createDataFrame(
            [
                Row(ID=101, LABEL="snowflake-round-trip"),
                Row(ID=102, LABEL="second-row"),
            ]
        )
        io = SnowflakeIO(spark, cfg)
        io.write("_MILESTONE_E_ROUND_TRIP", frame)
        result_io = SnowflakeIO(
            spark,
            RunConfig(
                io="snowflake",
                account=ACCOUNT,
                user=USER,
                role=ROLE,
                warehouse=WAREHOUSE,
                database=DATABASE,
                source_schema=migrated_schema,
                migrated_target_schema=migrated_schema,
                private_key_path=key_path,
                snowflake_jars_dir=jars_dir,
            ),
        )
        result = result_io.read("_MILESTONE_E_ROUND_TRIP").orderBy("ID").collect()
        print("Spark Snowflake round-trip output:")
        for row in result:
            print(row)
        if [(row.ID, row.LABEL) for row in result] != [
            (101, "snowflake-round-trip"),
            (102, "second-row"),
        ]:
            raise AssertionError(f"unexpected round-trip rows: {result}")
        conn = connect(key_path)
        conn.autocommit(True)
        try:
            conn.cursor().execute(
                f'DROP TABLE "{migrated_schema}"."_MILESTONE_E_ROUND_TRIP"'
            )
        finally:
            conn.close()
        print("Spark Snowflake round-trip: PASS; throwaway table dropped")
    finally:
        spark.stop()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--repo", default=".")
    parser.add_argument("--jars-dir", type=Path)
    args = parser.parse_args()
    run_id = args.run_id
    baseline = schema_name("BASELINE", run_id)
    migrated = schema_name("PYSPARK", run_id)
    key_path = runtime_key(run_id)

    conn = connect(key_path)
    conn.autocommit(True)
    cur = conn.cursor()
    try:
        sql = proof_sql(baseline, migrated)
        cur.execute(sql)
        print("Proof output:")
        for row in cur.fetchall():
            print(row)

        for name, history in history_variants():
            try:
                cur.execute(history)
                rows = cur.fetchall()
                print(f"Query-history variant used: {name}")
                print("Query-history SQL:")
                print(history)
                print("Query-history output:")
                for row in rows:
                    print(row)
                break
            except snowflake.connector.errors.ProgrammingError as exc:
                print(f"Query-history variant {name} unavailable: {exc}")
        else:
            raise RuntimeError("no query-history table function variant succeeded")
    finally:
        cur.close()
        conn.close()

    run_spark_round_trip(key_path, f"SOURCE_INFORMATICA_{run_id}",
                         migrated, args.jars_dir)


if __name__ == "__main__":
    main()
