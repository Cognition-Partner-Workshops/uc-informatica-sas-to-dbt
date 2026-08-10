import os
from pathlib import Path

import snowflake.connector


RUN_ID = "20260809T234500Z"
DATABASE = "DEVIN_MIGRATION_DEMO"
SOURCE_SCHEMA = f"SOURCE_INFORMATICA_{RUN_ID}"
TARGET_SCHEMA = f"PYSPARK_INFORMATICA_{RUN_ID}"
BASELINE_SCHEMA = f"BASELINE_INFORMATICA_{RUN_ID}"
SQL_DIR = Path(__file__).parent / "sql"
PROOF_PATH = Path(__file__).parent / "PROOF.md"


def connect():
    return snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        role=os.environ["SNOWFLAKE_ROLE"],
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        database=DATABASE,
        private_key_file=os.environ["SNOWFLAKE_PRIVATE_KEY_PATH"],
    )


def render(value):
    return (
        "NULL"
        if value is None
        else "\n".join(line.rstrip() for line in str(value).splitlines())
    )


def run_sql(cur, sql: str) -> str:
    outputs = []
    statements = [statement.strip() for statement in sql.split(";") if statement.strip()]
    for index, statement in enumerate(statements, start=1):
        outputs.append(f"-- statement {index}")
        outputs.append(statement)
        cur.execute(statement)
        if cur.description is None:
            outputs.append(f"-- {cur.rowcount} rows")
            outputs.append(f"STATUS: {cur.rowcount}")
            continue
        columns = [description[0] for description in cur.description]
        rows = cur.fetchall()
        outputs.append(f"-- {len(rows)} rows")
        outputs.append(" | ".join(columns))
        outputs.extend(" | ".join(render(value) for value in row) for row in rows)
    return "\n".join(outputs)


def show_tables(cur, schema: str) -> str:
    cur.execute(f"show tables in schema {DATABASE}.{schema}")
    columns = [description[0] for description in cur.description]
    rows = cur.fetchall()
    selected = ("name", "rows", "created_on")
    lines = [" | ".join(selected)]
    for row in rows:
        values = dict(zip(columns, row))
        lines.append(" | ".join(render(values[column]) for column in selected))
    return "\n".join(lines)


def sample(cur, table: str) -> str:
    cur.execute(f"select * from {DATABASE}.{TARGET_SCHEMA}.{table} limit 5")
    lines = [" | ".join(description[0] for description in cur.description)]
    lines.extend(" | ".join(render(value) for value in row) for row in cur.fetchall())
    return "\n".join(lines)


def query_history_output(cur) -> str:
    sql_path = SQL_DIR / "05_query_history.sql"
    cur.execute(sql_path.read_text())
    columns = [description[0] for description in cur.description]
    rows = cur.fetchall()
    values = [dict(zip(columns, row)) for row in rows]
    excluded = ("ALTER SESSION", "SELECT * FROM TABLE(RESULT_SCAN(", "GET @", "PUT ")
    substantive = [
        row for row in values
        if not any(str(row["QUERY_TEXT"]).upper().startswith(prefix) for prefix in excluded)
    ]
    counts = {
        schema: sum(row["SCHEMA_NAME"] == schema for row in values)
        for schema in (SOURCE_SCHEMA, TARGET_SCHEMA, BASELINE_SCHEMA)
    }
    lines = ["QUERY_COUNT_BY_SCHEMA", "SCHEMA | QUERY_COUNT"]
    lines.extend(f"{schema} | {counts[schema]}" for schema in counts)
    lines.append("SUBSTANTIVE_QUERY_HISTORY")
    lines.append(" | ".join(columns))
    lines.extend(
        " | ".join(render(row[column]) for column in columns)
        for row in substantive
    )
    return "\n".join(lines)


def main() -> None:
    conn = connect()
    sections = []
    try:
        cur = conn.cursor()
        cur.execute(
            f"show schemas like '%{RUN_ID}%' in database {DATABASE}"
        )
        sections.append(
            "## SHOW SCHEMAS\n\n"
            + "\n".join(
                " | ".join(render(value) for value in row) for row in cur.fetchall()
            )
        )
        for schema in (SOURCE_SCHEMA, TARGET_SCHEMA, BASELINE_SCHEMA):
            sections.append(
                f"## SHOW TABLES {schema}\n\n{show_tables(cur, schema)}"
            )
        for table in ("DEMO_TARGET1_INS", "DEMO_TARGET2", "DEMO_TARGET6"):
            sections.append(
                f"## SAMPLE {table}\n\n{sample(cur, table)}"
            )
        for number in range(1, 7):
            sql_path = next(SQL_DIR.glob(f"{number:02d}_*.sql"))
            output = (
                query_history_output(cur)
                if number == 5
                else run_sql(cur, sql_path.read_text())
            )
            sections.append(
                f"## {sql_path.name}\n\n```text\n{output}\n```"
            )
    finally:
        conn.close()

    PROOF_PATH.write_text("# Snowflake Warehouse Parity Proof\n\n" + "\n\n".join(sections) + "\n")
    print(PROOF_PATH)


if __name__ == "__main__":
    main()
