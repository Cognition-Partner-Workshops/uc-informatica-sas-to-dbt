"""Run proof/proof_query.sql as the reader user and as the demo role; write proof/proof_<who>.md.

Reader: SF_READER_USER / SF_READER_PASSWORD with its default role. Demo: SF_DEMO_* with role SF_DEMO_ROLE.
Both need SNOWFLAKE_ACCOUNT, SNOWFLAKE_HOST, SF_DEMO_WAREHOUSE and SF_DEMO_DATABASE.
"""
import os
from pathlib import Path

import snowflake.connector

ROOT = Path(__file__).resolve().parents[1]


def statements():
    body = "\n".join(l for l in (ROOT / "proof" / "proof_query.sql").read_text().splitlines()
                     if not l.lstrip().startswith("--"))
    return [s.strip() for s in body.split(";") if s.strip()]


def run(who):
    reader = who == "reader"
    con = snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"], host=os.environ["SNOWFLAKE_HOST"],
        user=os.environ["SF_READER_USER" if reader else "SF_DEMO_USER"],
        password=os.environ["SF_READER_PASSWORD" if reader else "SF_DEMO_PASSWORD"],
        role=None if reader else os.environ["SF_DEMO_ROLE"],
        warehouse=os.environ["SF_DEMO_WAREHOUSE"], database=os.environ["SF_DEMO_DATABASE"],
        session_parameters={"QUERY_TAG": "SF_20261015_DS"})
    cur = con.cursor()
    role = cur.execute("select current_role()").fetchone()[0]
    out = [f"# Proof query as {'reader user' if reader else 'demo user'}, role `{role}`", ""]
    for i, s in enumerate(statements(), 1):
        cur.execute(s)
        cols = [d[0] for d in cur.description]
        out += [f"## Query {i}", "", "| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
        out += ["| " + " | ".join("NULL" if v is None else str(v) for v in row) + " |" for row in cur.fetchall()]
        out.append("")
    (ROOT / "proof" / f"proof_{who}.md").write_text("\n".join(out))
    print(f"{who}: role {role}, {len(statements())} queries")


if __name__ == "__main__":
    run("reader")
    run("demo")
