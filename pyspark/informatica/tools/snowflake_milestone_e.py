"""Provision one isolated Snowflake Informatica parity run.

This script uses explicit schemas from ``informatica_pyspark.schemas``. It
creates no objects until it has checked that all namespaced schemas are absent.
The private key is read from ``SNOWFLAKE_PRIVATE_KEY`` only to create a
0600 runtime file outside the repository.
"""

import argparse
import csv
import os
import re
import tempfile
from datetime import date, datetime
from pathlib import Path

import snowflake.connector
from pyspark.sql.types import (
    DateType,
    DoubleType,
    LongType,
    StringType,
    StructType,
    TimestampType,
)

from informatica_pyspark.schemas import LOOKUP_SCHEMAS, SOURCE_SCHEMAS, TARGET_SCHEMAS

ACCOUNT = "YD76133.us-east-2.aws"
USER = "devin_demo"
ROLE = "devin_migration_demo"
WAREHOUSE = "devin_demo_wh"
DATABASE = "devin_migration_demo"
TARGETS = [
    "demo_target1_INS",
    "demo_target1_UPD",
    "demo_target2",
    "demo_target21",
    "demo_target3",
    "demo_target5",
    "demo_target6",
]
ORDINAL_INPUTS = {
    "demo_source1",
    "lkp_demo_source1",
    "lkp_demo_source2",
    "lkp_demo_source3",
    "demo_target1",
}


def quote_ident(value):
    if not re.fullmatch(r"[A-Za-z0-9_]+", value):
        raise ValueError(f"unsafe identifier: {value}")
    return f'"{value.upper()}"'


def schema_name(prefix, run_id):
    return f"{prefix}_INFORMATICA_{run_id}"


def snowflake_type(field):
    typ = field.dataType
    if isinstance(typ, StringType):
        return "VARCHAR"
    if isinstance(typ, DoubleType):
        return "NUMBER(38,6)"
    if isinstance(typ, LongType):
        return "NUMBER(38,0)"
    if isinstance(typ, DateType):
        return "DATE"
    if isinstance(typ, TimestampType):
        return "TIMESTAMP_NTZ"
    raise TypeError(f"unsupported Spark type: {typ}")


def table_ddl(schema, table, struct, ordinal=False):
    fields = [f"{quote_ident(f.name)} {snowflake_type(f)}" for f in struct.fields]
    if ordinal:
        fields.append(f'{quote_ident("__LINE_ORDINAL")} NUMBER(38,0) NOT NULL')
    return f"CREATE TABLE {quote_ident(schema)}.{quote_ident(table)} ({', '.join(fields)})"


def csv_value(raw, field):
    if raw == "":
        return None
    typ = field.dataType
    if isinstance(typ, StringType):
        return raw
    if isinstance(typ, DoubleType):
        return float(raw)
    if isinstance(typ, LongType):
        return int(float(raw))
    if isinstance(typ, DateType):
        return date.fromisoformat(raw)
    if isinstance(typ, TimestampType):
        return datetime.fromisoformat(raw.replace("Z", "+00:00")).replace(tzinfo=None)
    raise TypeError(typ)


def connect(key_path):
    return snowflake.connector.connect(
        account=ACCOUNT,
        user=USER,
        role=ROLE,
        warehouse=WAREHOUSE,
        database=DATABASE,
        private_key_file=key_path,
    )


def runtime_key(run_id):
    pem = os.environ.get("SNOWFLAKE_PRIVATE_KEY")
    if not pem:
        raise RuntimeError("SNOWFLAKE_PRIVATE_KEY is not set")
    path = Path(tempfile.gettempdir()) / f"informatica-snowflake-{run_id}.pem"
    path.write_text(pem)
    path.chmod(0o600)
    return path


def ensure_absent_and_create(cur, schemas):
    cur.execute(
        f"SELECT schema_name FROM {DATABASE}.information_schema.schemata "
        "ORDER BY schema_name"
    )
    existing = [row[0] for row in cur.fetchall()]
    print("Existing schemas before creation:")
    for name in existing:
        print(name)
    collisions = sorted(set(schemas) & set(existing))
    if collisions:
        raise RuntimeError(f"intended schemas already exist: {collisions}")
    for schema in schemas:
        cur.execute(f"CREATE SCHEMA {quote_ident(schema)}")
        print(f"created schema {schema}")


def load_csv(cur, schema, table, path, struct, ordinal):
    columns = [f.name for f in struct.fields]
    if ordinal:
        columns.append("__LINE_ORDINAL")
    placeholders = ", ".join(["%s"] * len(columns))
    sql = (
        f"INSERT INTO {quote_ident(schema)}.{quote_ident(table)} "
        f"({', '.join(quote_ident(c) for c in columns)}) VALUES ({placeholders})"
    )
    with path.open(newline="") as fh:
        rows = []
        for ordinal_value, raw_row in enumerate(csv.DictReader(fh)):
            values = [csv_value(raw_row[f], field) for f, field in
                      zip(columns[: len(struct.fields)], struct.fields)]
            if ordinal:
                values.append(ordinal_value)
            rows.append(values)
        if rows:
            cur.executemany(sql, rows)
    print(f"loaded {schema}.{table}: {len(rows)} rows from {path}")


def create_typed_table(cur, schema, table, struct, ordinal=False):
    cur.execute(f"DROP TABLE IF EXISTS {quote_ident(schema)}.{quote_ident(table)}")
    ddl = table_ddl(schema, table, struct, ordinal)
    cur.execute(ddl)
    print(f"DDL {schema}.{table}: {ddl}")


def normalized_projection(struct):
    expressions = []
    for field in struct.fields:
        col = quote_ident(field.name)
        typ = field.dataType
        if isinstance(typ, (DoubleType, LongType)):
            expr = f"TO_VARCHAR(TO_DECIMAL({col},38,6))"
        elif isinstance(typ, DateType):
            expr = f"TO_VARCHAR({col}::DATE,'YYYY-MM-DD')"
        elif isinstance(typ, TimestampType):
            expr = f"TO_VARCHAR({col}::TIMESTAMP_NTZ,'YYYY-MM-DD HH24:MI:SS')"
        else:
            expr = f"TRIM({col})"
        expressions.append(f"{expr} AS {quote_ident(field.name)}")
    return ", ".join(expressions)


def create_views(cur, baseline_schema, migrated_schema):
    for target in TARGETS:
        struct = TARGET_SCHEMAS[
            "demo_target1" if target in {"demo_target1_INS", "demo_target1_UPD"} else target
        ]
        projection = normalized_projection(struct)
        for schema in (baseline_schema, migrated_schema):
            cur.execute(
                f"CREATE OR REPLACE VIEW {quote_ident(schema)}.{quote_ident('V_' + target)} "
                f"AS SELECT {projection} FROM {quote_ident(schema)}.{quote_ident(target)}"
            )
        print(f"created normalized views V_{target} in both schemas")


def proof_sql(baseline_schema, migrated_schema):
    checks = []
    for target in TARGETS:
        b = f"{quote_ident(baseline_schema)}.{quote_ident('V_' + target)}"
        m = f"{quote_ident(migrated_schema)}.{quote_ident('V_' + target)}"
        checks.append(
            f"""select '{target.upper()}' as target,
       (select count(*) from {b}) as baseline_rows,
       (select count(*) from {m}) as migrated_rows,
       (select hash_agg(*) from {b}) as baseline_hash,
       (select hash_agg(*) from {m}) as migrated_hash,
       (select count(*) from (select * from {b} minus select * from {m})) as baseline_minus_migrated,
       (select count(*) from (select * from {m} minus select * from {b})) as migrated_minus_baseline"""
        )
    return (
        "with chk as (\n" + "\nunion all\n".join(checks) + "\n)\n"
        "select target, baseline_rows, migrated_rows, baseline_hash, migrated_hash,\n"
        "       baseline_minus_migrated, migrated_minus_baseline,\n"
        "       case when baseline_rows = migrated_rows and baseline_hash = migrated_hash\n"
        "                 and baseline_minus_migrated = 0 and migrated_minus_baseline = 0\n"
        "            then 'PASS' else 'FAIL' end as verdict\n"
        "from chk order by target;"
    )


def history_sql():
    return (
        "select query_id, query_text, start_time, end_time, rows_produced, "
        "warehouse_name, execution_status "
        "from table(devin_migration_demo.information_schema.query_history("
        "end_time_range_start => dateadd('hour', -3, current_timestamp()), "
        "result_limit => 200)) "
        "where warehouse_name = current_warehouse() "
        "order by start_time desc"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", default=datetime.utcnow().strftime("%Y%m%dT%H%MZ"))
    parser.add_argument("--repo", default=".")
    args = parser.parse_args()
    run_id = args.run_id
    source = schema_name("SOURCE", run_id)
    migrated = schema_name("PYSPARK", run_id)
    baseline = schema_name("BASELINE", run_id)
    key_path = runtime_key(run_id)
    conn = connect(key_path)
    conn.autocommit(True)
    cur = conn.cursor()
    try:
        ensure_absent_and_create(cur, [source, migrated, baseline])
        data_dir = Path(args.repo) / "legacy/informatica/data"
        for name, struct in {**SOURCE_SCHEMAS, **LOOKUP_SCHEMAS}.items():
            create_typed_table(cur, source, name, struct, name in ORDINAL_INPUTS)
            load_csv(cur, source, name, data_dir / f"{name}.csv", struct, name in ORDINAL_INPUTS)
        create_typed_table(cur, source, "demo_target1", TARGET_SCHEMAS["demo_target1"], True)
        load_csv(cur, source, "demo_target1", data_dir / "demo_target1.csv",
                 TARGET_SCHEMAS["demo_target1"], True)
        for target in TARGETS:
            struct = TARGET_SCHEMAS[
                "demo_target1" if target in {"demo_target1_INS", "demo_target1_UPD"} else target
            ]
            create_typed_table(cur, migrated, target, struct)
        baseline_dir = Path(args.repo) / "baseline/informatica"
        for target in TARGETS:
            struct = TARGET_SCHEMAS[
                "demo_target1" if target in {"demo_target1_INS", "demo_target1_UPD"} else target
            ]
            create_typed_table(cur, baseline, target, struct)
            load_csv(cur, baseline, target, baseline_dir / f"{target}.csv", struct, False)
        create_views(cur, baseline, migrated)
        proof = proof_sql(baseline, migrated)
        proof_path = Path(args.repo) / "build/pyspark/informatica" / f"proof_{run_id}.sql"
        proof_path.parent.mkdir(parents=True, exist_ok=True)
        proof_path.write_text(proof + "\n")
        print(f"proof SQL: {proof_path}")
        print(proof)
        print("query history SQL:")
        print(history_sql())
        cur.execute(history_sql())
        print("query history output:")
        for row in cur.fetchall():
            print(row)
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
