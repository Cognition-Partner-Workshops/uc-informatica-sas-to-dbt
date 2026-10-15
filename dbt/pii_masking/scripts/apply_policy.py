"""Apply sql/01-04 (or 99_rollback.sql with --rollback) as the run's dbt role, never ACCOUNTADMIN.

Needs SNOWFLAKE_ACCOUNT, SNOWFLAKE_HOST and SF_DEMO_USER/PASSWORD/ROLE/WAREHOUSE/DATABASE in the environment.
"""
import os
import sys
from pathlib import Path

import snowflake.connector

SQL = Path(__file__).resolve().parents[1] / "sql"
ROLE = "SF_20261015_DS_DBT"


def statements(path):
    body = "\n".join(l for l in path.read_text().splitlines() if not l.lstrip().startswith("--"))
    return [s.strip() for s in body.split(";") if s.strip()]


def main():
    files = [SQL / "99_rollback.sql"] if "--rollback" in sys.argv else sorted(SQL.glob("0[1-4]_*.sql"))
    con = snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"], host=os.environ["SNOWFLAKE_HOST"],
        user=os.environ["SF_DEMO_USER"], password=os.environ["SF_DEMO_PASSWORD"],
        role=os.environ["SF_DEMO_ROLE"], warehouse=os.environ["SF_DEMO_WAREHOUSE"],
        database=os.environ["SF_DEMO_DATABASE"], session_parameters={"QUERY_TAG": "SF_20261015_DS"})
    cur = con.cursor()
    role = cur.execute("select current_role()").fetchone()[0]
    if role != ROLE:
        raise SystemExit(f"refusing to run as {role}; expected {ROLE}")
    for f in files:
        stmts = statements(f)
        for s in stmts:
            cur.execute(s)
        print(f"{f.name}: {len(stmts)} statements OK as {role}")


if __name__ == "__main__":
    main()
