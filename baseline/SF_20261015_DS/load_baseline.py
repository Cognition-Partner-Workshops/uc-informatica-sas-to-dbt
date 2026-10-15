#!/usr/bin/env python3
"""Build the tagged Snowflake baseline for one demo run.

Creates, under DEVIN_MIGRATION_DEMO, the five run schemas, the run warehouse and
its 5 credit resource monitor, the two roles and two users, loads the legacy
source tables and the legacy baseline tables from the deterministic tools in
tools/, tags every object with RUN and EXPIRES, and prints per-step timings and
the credits the load cost.

Connection: SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER and SNOWFLAKE_PASSWORD (a PAT works)
with a role that can create warehouses, roles, users and resource monitors.
Generated passwords are written only to --creds-out (mode 600); nothing else
prints them.

Usage, from the repo root after the two baseline tools have run:
    python3 baseline/<token>/load_baseline.py --token SF_20261015_DS
"""
import argparse
import datetime as dt
import glob
import json
import os
import re
import secrets
import sys
import tempfile
import time

import duckdb
import snowflake.connector

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "tools"))
import informatica_baseline  # noqa: E402
import sas_load_raw  # noqa: E402

DB = "DEVIN_MIGRATION_DEMO"
SAS_PREFIX = {"ora_dw": "ORA_DW", "raw_bank": "RAW_BANK", "raw_ins": "RAW_INS", "curated_src": "CURATED"}

DUCK_TO_SF = {
    "VARCHAR": "VARCHAR", "BIGINT": "NUMBER(38,0)", "INTEGER": "NUMBER(38,0)", "HUGEINT": "NUMBER(38,0)",
    "DOUBLE": "FLOAT", "FLOAT": "FLOAT", "DATE": "DATE", "TIMESTAMP": "TIMESTAMP_NTZ",
    "TIMESTAMP_NS": "TIMESTAMP_NTZ", "BOOLEAN": "BOOLEAN", "TIME": "TIME",
}


def sf_type(duck_type: str) -> str:
    t = duck_type.upper()
    if t.startswith("DECIMAL"):
        return "NUMBER" + t[len("DECIMAL"):]
    return DUCK_TO_SF.get(t, "VARCHAR")


class Runner:
    def __init__(self, args):
        self.args = args
        self.token = args.token
        self.expires = args.expires
        self.timings = []
        self.creds = {}
        self.cs = snowflake.connector.connect(
            account=os.environ.get("SNOWFLAKE_ACCOUNT", "yd76133.us-east-2.aws"),
            user=os.environ.get("SNOWFLAKE_USER", "SMITCHESCOGNITION"),
            password=os.environ.get("SNOWFLAKE_PASSWORD") or os.environ["SNOWFLAKE_PAT"],
            role=os.environ.get("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
            session_parameters={"QUERY_TAG": f"RUN={args.token};PHASE=baseline_load"},
        ).cursor()
        self.duck = duckdb.connect(":memory:")
        self.tmp = tempfile.mkdtemp(prefix="sf_baseline_")

    # names
    @property
    def wh(self):
        return f"{self.token}_WH"

    @property
    def mon(self):
        return f"{self.token}_MON"

    def schema(self, kind):
        return f"{DB}.{kind}_{self.token}"

    def sql(self, q, quiet=False):
        if not quiet:
            print("   ", " ".join(q.split())[:140])
        self.cs.execute(q)
        return self.cs.fetchall()

    def step(self, name, fn):
        t0 = time.time()
        print(f"\n== {name}")
        out = fn()
        secs = time.time() - t0
        self.timings.append((name, secs))
        print(f"   done in {secs:.1f}s")
        return out

    # steps
    def tags(self):
        self.sql(f"CREATE TAG IF NOT EXISTS {DB}.PUBLIC.RUN COMMENT = 'demo run token'")
        self.sql(f"CREATE TAG IF NOT EXISTS {DB}.PUBLIC.EXPIRES COMMENT = 'ISO timestamp after which teardown may drop the object'")

    def warehouse(self):
        self.sql(f"""CREATE WAREHOUSE IF NOT EXISTS {self.wh} WITH WAREHOUSE_SIZE = XSMALL
            AUTO_SUSPEND = 60 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE
            COMMENT = 'demo run {self.token}; dropped by baseline/{self.token}/teardown.sh'""")
        if not self.sql(f"SHOW RESOURCE MONITORS LIKE '{self.mon}'"):
            self.sql(f"""CREATE RESOURCE MONITOR {self.mon} WITH CREDIT_QUOTA = 5
                FREQUENCY = NEVER START_TIMESTAMP = IMMEDIATELY
                TRIGGERS ON 80 PERCENT DO NOTIFY ON 100 PERCENT DO SUSPEND ON 105 PERCENT DO SUSPEND_IMMEDIATE""")
        self.sql(f"ALTER WAREHOUSE {self.wh} SET RESOURCE_MONITOR = {self.mon}")
        self.sql(f"USE WAREHOUSE {self.wh}")

    def schemas(self):
        for kind in ("SOURCE", "BASELINE", "DBT", "SCAI", "ORACLE"):
            self.sql(f"CREATE SCHEMA IF NOT EXISTS {self.schema(kind)} COMMENT = 'demo run {self.token}'")

    def roles(self):
        dbt, rdr = f"{self.token}_DBT", f"{self.token}_READER"
        for r in (dbt, rdr):
            self.sql(f"CREATE ROLE IF NOT EXISTS {r}")
            self.sql(f"GRANT ROLE {r} TO ROLE SYSADMIN")
            self.sql(f"GRANT USAGE ON DATABASE {DB} TO ROLE {r}")
            self.sql(f"GRANT USAGE, MONITOR ON WAREHOUSE {self.wh} TO ROLE {r}")
            self.sql(f"GRANT MONITOR ON RESOURCE MONITOR {self.mon} TO ROLE {r}")
        for kind in ("SOURCE", "BASELINE"):
            s = self.schema(kind)
            for r in (dbt, rdr):
                self.sql(f"GRANT USAGE ON SCHEMA {s} TO ROLE {r}")
                self.sql(f"GRANT SELECT ON ALL TABLES IN SCHEMA {s} TO ROLE {r}")
                self.sql(f"GRANT SELECT ON FUTURE TABLES IN SCHEMA {s} TO ROLE {r}")
                self.sql(f"GRANT SELECT ON ALL VIEWS IN SCHEMA {s} TO ROLE {r}")
                self.sql(f"GRANT SELECT ON FUTURE VIEWS IN SCHEMA {s} TO ROLE {r}")
        for kind in ("DBT", "SCAI", "ORACLE"):
            s = self.schema(kind)
            self.sql(f"GRANT ALL PRIVILEGES ON SCHEMA {s} TO ROLE {dbt}")
            for obj in ("TABLES", "VIEWS", "STAGES", "SEQUENCES", "FUNCTIONS", "PROCEDURES", "FILE FORMATS"):
                self.sql(f"GRANT ALL PRIVILEGES ON FUTURE {obj} IN SCHEMA {s} TO ROLE {dbt}")
                self.sql(f"GRANT ALL PRIVILEGES ON ALL {obj} IN SCHEMA {s} TO ROLE {dbt}")
            self.sql(f"GRANT USAGE ON SCHEMA {s} TO ROLE {rdr}")
            for obj in ("TABLES", "VIEWS"):
                self.sql(f"GRANT SELECT ON ALL {obj} IN SCHEMA {s} TO ROLE {rdr}")
                self.sql(f"GRANT SELECT ON FUTURE {obj} IN SCHEMA {s} TO ROLE {rdr}")
        self.sql(f"GRANT IMPORTED PRIVILEGES ON DATABASE SNOWFLAKE TO ROLE {dbt}")

    def users(self):
        plan = {
            f"{self.token}_DEMO": (f"{self.token}_DBT", "DBT"),
            f"{self.token}_READER_USER": (f"{self.token}_READER", "BASELINE"),
        }
        for user, (role, ns) in plan.items():
            pw = "Sf" + secrets.token_urlsafe(24) + "1!"
            self.sql(f"CREATE USER IF NOT EXISTS {user} TYPE = LEGACY_SERVICE")
            self.cs.execute(f"""ALTER USER {user} SET PASSWORD = '{pw}' MUST_CHANGE_PASSWORD = FALSE
                DEFAULT_ROLE = {role} DEFAULT_WAREHOUSE = {self.wh}
                DEFAULT_NAMESPACE = {self.schema(ns)}
                COMMENT = 'demo run {self.token}; dropped by baseline/{self.token}/teardown.sh'""")
            print(f"    ALTER USER {user} SET PASSWORD = '***' ...")
            self.sql(f"GRANT ROLE {role} TO USER {user}")
            self.creds[user] = {"role": role, "password": pw}

    # loading
    def _parquet(self, select_sql, name):
        path = os.path.join(self.tmp, f"{name}.parquet").replace("\\", "/")
        self.duck.execute(f"COPY ({select_sql}) TO '{path}' (FORMAT PARQUET)")
        return path

    def _load_table(self, schema_fq, table, select_sql):
        cols = self.duck.execute(f"DESCRIBE SELECT * FROM ({select_sql})").fetchall()
        ddl = ", ".join(f'"{c[0].upper()}" {sf_type(c[1])}' for c in cols)
        self.sql(f'CREATE OR REPLACE TABLE {schema_fq}."{table}" ({ddl})', quiet=True)
        path = self._parquet(select_sql, table)
        stage = f"{schema_fq}.%\"{table}\""
        self.cs.execute(f"PUT 'file://{path}' @{stage} AUTO_COMPRESS = FALSE OVERWRITE = TRUE")
        self.cs.execute(f"""COPY INTO {schema_fq}."{table}" FROM @{stage}
            FILE_FORMAT = (TYPE = PARQUET USE_LOGICAL_TYPE = TRUE) MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE PURGE = TRUE""")
        n = self.cs.execute(f'SELECT COUNT(*) FROM {schema_fq}."{table}"').fetchone()[0]
        print(f"    {schema_fq}.{table}: {n} rows")
        return n

    def load_source(self):
        s = self.schema("SOURCE")
        informatica_baseline.load(self.duck)
        inf = {
            "DEMO_SOURCE1": "SELECT * FROM demo_source1",
            "DEMO_SOURCE2": "SELECT * FROM demo_source2",
            "DEMO_SOURCE3": "SELECT * FROM demo_source3",
            "DEMO_SOURCE4": "SELECT * FROM demo_source4",
            "DEMO_SOURCE5": "SELECT * FROM demo_source5",
            "DEMO_TARGET1": "SELECT __seed_row AS SEED_ROW, * EXCLUDE (__seed_row) FROM demo_target1_pre_raw",
            "LKP_DEMO_SOURCE1": "SELECT __seed_row AS SEED_ROW, * EXCLUDE (__seed_row) FROM lkp_demo_source1_raw",
            "LKP_DEMO_SOURCE2": "SELECT __seed_row AS SEED_ROW, * EXCLUDE (__seed_row) FROM lkp_demo_source2_raw",
            "LKP_DEMO_SOURCE3": "SELECT __seed_row AS SEED_ROW, * EXCLUDE (__seed_row) FROM lkp_demo_source3_raw",
        }
        counts = {t: self._load_table(s, t, q) for t, q in inf.items() if self.want(t)}
        sas_load_raw.load_all(self.duck)
        for schema, prefix in SAS_PREFIX.items():
            for (tbl,) in self.duck.execute(
                    f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema}' ORDER BY 1").fetchall():
                name = f"{prefix}_{tbl.upper()}"
                if self.want(name):
                    counts[name] = self._load_table(s, name, f"SELECT * FROM {schema}.{tbl}")
        return counts

    def load_baseline(self):
        s = self.schema("BASELINE")
        counts = {}
        for track in ("informatica", "sas"):
            for csv in sorted(glob.glob(os.path.join(REPO, "baseline", track, "*.csv"))):
                name = os.path.splitext(os.path.basename(csv))[0].upper()
                if self.want(name):
                    counts[name] = self._load_table(s, name, self._csv_query(csv))
        return counts

    def _csv_query(self, csv):
        path = csv.replace(chr(92), "/")
        q = f"SELECT * FROM read_csv_auto('{path}', header = true, sample_size = -1)"
        flagged = [c[0] for c in self.duck.execute(f"DESCRIBE {q}").fetchall() if c[1].upper() == "BOOLEAN"]
        if flagged:
            # one-letter codes such as GENDER = 'F' are text in the legacy output, not booleans
            types = ", ".join(f"'{c}': 'VARCHAR'" for c in flagged)
            q = f"SELECT * FROM read_csv_auto('{path}', header = true, sample_size = -1, types = {{{types}}})"
        return q

    def want(self, table):
        return not self.args.tables or table in self.args.tables

    def tag_objects(self):
        tags = f"{DB}.PUBLIC.RUN = '{self.token}', {DB}.PUBLIC.EXPIRES = '{self.expires}'"
        for kind in ("SOURCE", "BASELINE", "DBT", "SCAI", "ORACLE"):
            self.sql(f"ALTER SCHEMA {self.schema(kind)} SET TAG {tags}")
        self.sql(f"ALTER WAREHOUSE {self.wh} SET TAG {tags}")
        for r in (f"{self.token}_DBT", f"{self.token}_READER"):
            self.sql(f"ALTER ROLE {r} SET TAG {tags}")
        for u in self.creds:
            self.sql(f"ALTER USER {u} SET TAG {tags}")
        self.sql(f"ALTER RESOURCE MONITOR {self.mon} SET NOTIFY_USERS = ({os.environ.get('SNOWFLAKE_USER', 'SMITCHESCOGNITION')})")

    def proof(self):
        s = self.schema("BASELINE")
        tables = [r[1] for r in self.sql(f"SHOW TABLES IN SCHEMA {s}", quiet=True)]
        union = "\nunion all\n".join(f"select '{t}' as target, count(*) as row_count from {s}.{t}" for t in tables)
        rows = self.sql(union, quiet=True)
        print("\n    Room query (BASELINE row counts):")
        for t, n in rows:
            print(f"    {t:28s} {n}")
        with open(os.path.join(REPO, "baseline", self.token, "room_query.sql"), "w") as fh:
            fh.write("-- Row counts of every legacy baseline target, as loaded for the run\n" + union + "\norder by 1;\n")
        return rows

    def credits(self):
        mon = self.sql(f"SHOW RESOURCE MONITORS LIKE '{self.mon}'", quiet=True)
        used = mon[0][2] if mon else None
        meter = self.sql(f"""select start_time, end_time, credits_used, credits_used_compute, credits_used_cloud_services
            from table({DB}.information_schema.warehouse_metering_history(dateadd('hour', -24, current_timestamp()), current_timestamp(), '{self.wh}'))
            order by start_time""", quiet=True)
        print(f"    resource monitor {self.mon}: used_credits = {used} of 5")
        for m in meter:
            print(f"    metering {m[0]} .. {m[1]}: {m[2]} credits ({m[3]} compute, {m[4]} cloud services)")
        return {"monitor_used_credits": str(used), "metering_rows": [[str(x) for x in m] for m in meter]}

    def write_creds(self):
        path = self.args.creds_out
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as fh:
            fh.write(f"export SF_RUN_TOKEN={self.token}\n")
            fh.write(f"export SF_DEMO_DATABASE={DB}\nexport SF_DEMO_WAREHOUSE={self.wh}\n")
            for user, c in self.creds.items():
                key = "SF_DEMO" if user.endswith("_DEMO") else "SF_READER"
                fh.write(f"export {key}_USER={user}\nexport {key}_PASSWORD='{c['password']}'\nexport {key}_ROLE={c['role']}\n")
        print(f"    credentials written to {path} (mode 600)")

    def run(self):
        if self.args.reload:
            return self.reload()
        self.step("tags", self.tags)
        self.step("warehouse and resource monitor", self.warehouse)
        self.step("schemas", self.schemas)
        self.step("roles and grants", self.roles)
        self.step("users", self.users)
        src = self.step("load SOURCE", self.load_source)
        base = self.step("load BASELINE", self.load_baseline)
        self.step("tags on objects", self.tag_objects)
        proof = self.step("proof query", self.proof)
        cred = self.step("credits", self.credits)
        self.write_creds()
        report = {
            "token": self.token, "expires": self.expires, "run_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "timings_seconds": {n: round(s, 1) for n, s in self.timings},
            "source_rows": src, "baseline_rows": base, "proof": [[t, n] for t, n in proof], "credits": cred,
        }
        with open(os.path.join(REPO, "baseline", self.token, "load_report.json"), "w") as fh:
            json.dump(report, fh, indent=2)
        print("\n== timings")
        for n, s in self.timings:
            print(f"    {n:32s} {s:7.1f}s")
        print(f"    {'total':32s} {sum(s for _, s in self.timings):7.1f}s")


    def reload(self):
        """Reload named tables in place (same DDL path, same tags); no roles, users or passwords touched."""
        src = self.step("load SOURCE", self.load_source)
        base = self.step("load BASELINE", self.load_baseline)
        self.step("tags on objects", self.tag_objects)
        proof = self.step("proof query", self.proof)
        cred = self.step("credits", self.credits)
        report = {
            "token": self.token, "reload_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "tables": sorted(self.args.tables or []),
            "timings_seconds": {n: round(s, 1) for n, s in self.timings},
            "source_rows": src, "baseline_rows": base, "proof": [[t, n] for t, n in proof], "credits": cred,
        }
        with open(os.path.join(REPO, "baseline", self.token, "reload_report.json"), "w") as fh:
            json.dump(report, fh, indent=2)
        print("\n== timings")
        for n, s in self.timings:
            print(f"    {n:32s} {s:7.1f}s")
        print(f"    {'total':32s} {sum(s for _, s in self.timings):7.1f}s")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--token", required=True, help="run token, e.g. SF_20261015_DS")
    ap.add_argument("--expires", default=(dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=72)).strftime("%Y-%m-%dT%H:%M:%SZ"))
    ap.add_argument("--creds-out", default=None, help="where the generated passwords go (default /dev/shm/sf_<token>.env)")
    ap.add_argument("--tables", default="", help="comma list: load only these SOURCE_/BASELINE_ tables")
    ap.add_argument("--reload", action="store_true", help="reload --tables in place; skip tags, warehouse, schemas, roles and users")
    args = ap.parse_args()
    args.tables = {t.strip().upper() for t in args.tables.split(",") if t.strip()}
    if not re.fullmatch(r"SF_[A-Z0-9]+_[A-Z]{2}", args.token):
        ap.error(f"token {args.token!r} must look like SF_20261015_DS (it is spliced into object names)")
    args.creds_out = args.creds_out or f"/dev/shm/sf_{args.token}.env"
    Runner(args).run()


if __name__ == "__main__":
    main()
