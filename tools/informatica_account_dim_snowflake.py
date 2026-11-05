#!/usr/bin/env python3
"""Frozen-input dual run; freeze and offline never connect to Snowflake."""

import argparse
import csv
import hashlib
import io
import json
import os
import subprocess
import sys
from collections import Counter
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any
from unittest.mock import patch
from xml.etree import ElementTree

import duckdb
import informatica_baseline as baseline
import sf_attribution as sf
import snowflake.connector
from dbt.cli.main import dbtRunner
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    load_pem_private_key,
)

ROOT = Path(__file__).resolve().parents[1]
DATABASE = sf.database_name("mig_inf")
SRC = f"INFA_ACCTDIM_SRC_{sf.RUN_TOKEN}"
LEGACY = f"INFA_ACCTDIM_LEGACY_{sf.RUN_TOKEN}"
TARGET = f"INFA_ACCTDIM_TARGET_{sf.RUN_TOKEN}"
WAREHOUSE = "WH_MIG_INF_ACCOUNT_DIMENSION"
SOURCE_COLUMNS = [
    (c, "VARCHAR")
    for c in (
        "LEAD_CO_MNE",
        "BRANCH_CO_MNE",
        "MIS_DATE",
        "ID",
        "DESCRIPTION",
        "SHORT_NAME",
    )
]
TARGET_COLUMNS = (
    [("KEY", "NUMBER(38,0)")]
    + SOURCE_COLUMNS
    + [
        ("CREATED_BY", "VARCHAR"),
        ("CREATED_TIME", "TIMESTAMP_NTZ(6)"),
        ("UPDATED_BY", "VARCHAR"),
        ("UPDATED_TIME", "TIMESTAMP_NTZ(6)"),
        ("ACTIVE_FLAG", "VARCHAR"),
        ("START_DATE", "TIMESTAMP_NTZ(6)"),
        ("END_DATE", "TIMESTAMP_NTZ(6)"),
    ]
)
OUTPUTS = ("DEMO_TARGET1_INS", "DEMO_TARGET1_UPD")
INPUTS = ("DEMO_SOURCE1", "DEMO_TARGET1")

PROJECT = ROOT / "dbt/m_demo_mapping2"
EP = sf.endpoint("cs_mig_inf_account_dimension")
MONITOR = sf.resource_monitor_name("mig_inf")
EMULATOR = "emulator: tools/informatica_baseline.py on DuckDB; PowerCenter engine unavailable"
NORMALIZATIONS = {
    "null": r"\N",
    "strings": "No trim; escape backslash by doubling, then pipe with backslash",
    "key": "NUMBER(38,0) integer text",
    "timestamps": "YYYY-MM-DD HH24:MI:SS.FF6",
    "metadata": "INFORMATION_SCHEMA types compared in XML order; DATETIME_PRECISION is not applicable in Snowflake",
    "row": "XML target column order; pipe-delimited",
    "checksum": "SHA-256 of UTF-8 sorted canonical rows joined by newline, no trailing newline; duplicates retained",
    "csv": "Empty fields become NULL; target physical order retained in __SEED_ROW",
}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def published_commit():
    commit = sf.resolve_commit()
    if commit != git("rev-parse", "HEAD") or git("status", "--porcelain"):
        raise ValueError("Resolved commit must be clean HEAD")
    if not git("branch", "-r", "--contains", commit):
        raise ValueError("HEAD must be contained in a remote branch")
    return commit


def attributed_options():
    params = sf.connection_params(
        EP, phase="dev", account=os.environ["SNOWFLAKE_EXT_ACCOUNT"],
        private_key_file="unused", commit=published_commit(),
        run_id=os.environ.get("SF_RUN_ID") or sf.make_run_id("mig_inf", "dev"),
        session_url=os.environ.get("DEVIN_SESSION_URL"), role="DEVIN_EXT_ROLE",
    )
    return params


def connection_options():
    params = attributed_options()
    params.pop("private_key_file")
    params["user"] = os.environ["SNOWFLAKE_EXT_USER"]
    key = load_pem_private_key(os.environ["SNOWFLAKE_EXT_PRIVATE_KEY"].encode(), password=None)
    params["private_key"] = key.private_bytes(Encoding.DER, PrivateFormat.PKCS8, NoEncryption())
    params.update(database=DATABASE, warehouse=WAREHOUSE)
    return params


def connect():
    return snowflake.connector.connect(**connection_options())


class Queries:
    def __init__(self, cursor):
        self.cursor = cursor
        self.query_ids: list[str] = []

    def execute(self, *args):
        try:
            self.cursor.execute(*args)
        finally:
            if self.cursor.sfqid:
                self.query_ids.append(self.cursor.sfqid)
        return self.cursor

    def executemany(self, sql, rows):
        for row in rows:
            self.execute(sql, row)


def compute_guard(cur, require_tag=True):
    cursor = cur.execute(f"SHOW WAREHOUSES LIKE '{WAREHOUSE}'")
    names = [d[0].lower() for d in cursor.description]
    rows = [dict(zip(names, row)) for row in cursor.fetchall()]
    wh = next((r for r in rows if r["name"] == WAREHOUSE), None)
    if not wh or str(wh.get("resource_monitor", "")).upper() != MONITOR.upper():
        raise ValueError("Warehouse missing or not attached to the required resource monitor; ask a control connection to attach it")
    if str(wh.get("size", "")).upper().replace("-", "") != "XSMALL" or int(wh["auto_suspend"]) != 60:
        raise ValueError("Warehouse must be X-Small with auto_suspend 60")
    if require_tag:
        tag = cur.execute(
            "SELECT SYSTEM$GET_TAG('DEVIN_GOVERNANCE.TAGS.DEVIN_CSID', %s, 'warehouse')",
            (WAREHOUSE,),
        ).fetchone()[0]
        if tag != EP.csid:
            raise ValueError("Warehouse DEVIN_CSID mismatch")


def setup(cur):
    compute_guard(cur, require_tag=False)
    comment = sf.external_comment(workload="mig_inf", csid=EP.csid, job="account_dimension").replace("'", "''")
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE} COMMENT = '{comment}'")
    for schema in (SRC, LEGACY, TARGET):
        cur.execute(f"CREATE SCHEMA IF NOT EXISTS {DATABASE}.{schema} COMMENT = '{comment}'")
    cur.execute(f"ALTER WAREHOUSE {WAREHOUSE} SET TAG DEVIN_GOVERNANCE.TAGS.DEVIN_CSID = '{EP.csid}'")
    compute_guard(cur)


def outside_repo(directory):
    path = Path(directory).expanduser().resolve()
    if path == ROOT or ROOT in path.parents:
        raise ValueError("Output must be outside the repository")
    path.mkdir(parents=True, exist_ok=True)
    return path


def input_path(table):
    return ROOT / "legacy/informatica/data" / f"{table.lower()}.csv"


def baseline_path(table):
    return ROOT / "baseline/informatica" / f"{table.lower()[:-3]}{table[-3:]}.csv"


def frozen_section():
    xml = ElementTree.parse(ROOT / "legacy/informatica/wf_demo_mapping.XML")
    target = xml.find(".//TARGET[@NAME='demo_target1']")
    if target is None or [f.attrib["NAME"].upper() for f in target.findall("TARGETFIELD")] != [c for c, _ in TARGET_COLUMNS]:
        raise ValueError("Configured columns differ from XML target order")
    files = [ROOT / "legacy/informatica/wf_demo_mapping.XML",
             *(input_path(t) for t in INPUTS), *(baseline_path(t) for t in OUTPUTS),
             ROOT / "tools/informatica_baseline.py",
             *(p for p in PROJECT.rglob("*") if p.is_file()
               and not {"target", "logs"}.intersection(p.relative_to(PROJECT).parts))]
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    counts = {}
    for table in INPUTS:
        rows = csv.reader(io.StringIO(input_path(table).read_bytes().decode("utf-8")))
        next(rows)
        counts[table] = sum(1 for _ in rows)
    return {"file_hashes": hashes, "row_counts": counts}


def digest(section):
    return hashlib.sha256(json.dumps(section, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def freeze(directory):
    section = frozen_section()
    manifest = {"source_commit": git("rev-parse", "HEAD"), "business_date": "2024-01-31",
                "inputs": section, "input_digest": digest(section)}
    path = outside_repo(directory) / "manifest.json"
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Frozen manifest: {path}")
    return manifest


def verify_manifest(path):
    manifest = json.loads(Path(path).read_text())
    if manifest["business_date"] != "2024-01-31" or manifest["input_digest"] != digest(manifest["inputs"]):
        raise ValueError("Invalid manifest")
    if frozen_section() != manifest["inputs"]:
        raise ValueError("Frozen input mismatch")
    return manifest


def fqn(schema, table):
    return f"{DATABASE}.{schema}.{table}"


def csv_rows(path, columns, data=None):
    with io.StringIO((data if data is not None else path.read_bytes()).decode("utf-8"), newline="") as stream:
        reader = csv.DictReader(stream)
        if [c.upper() for c in (reader.fieldnames or [])] != [c for c, _ in columns]:
            raise ValueError(f"Unexpected column order: {path}")
        rows = []
        for row in reader:
            values = []
            for (_, kind), raw in zip(columns, row.values()):
                value: str | Decimal | None
                if raw == "":
                    value = None
                elif kind.startswith("TIMESTAMP"):
                    value = datetime.fromisoformat(raw).strftime("%Y-%m-%d %H:%M:%S.%f")
                elif kind.startswith("NUMBER"):
                    value = Decimal(raw)
                else:
                    value = raw
                values.append(value)
            rows.append(values)
    return rows


def load_table(cur, schema, table, columns, rows):
    definition = ", ".join(f'"{c}" {t}' for c, t in columns)
    cur.execute(f"CREATE OR REPLACE TABLE {fqn(schema, table)} ({definition})")
    binds = ", ".join(
        "TO_TIMESTAMP_NTZ(%s, 'YYYY-MM-DD HH24:MI:SS.FF6')"
        if t.startswith("TIMESTAMP")
        else "%s"
        for _, t in columns
    )
    if rows:
        cur.executemany(f"INSERT INTO {fqn(schema, table)} VALUES ({binds})", rows)
    print(f"loaded {fqn(schema, table)}: {len(rows)} rows")


def replay_from_src(cur):
    """Replay the unchanged baseline mapping with the warehouse's exact inputs."""
    with duckdb.connect() as con:
        for table, columns in (
            ("DEMO_SOURCE1", SOURCE_COLUMNS),
            ("DEMO_TARGET1", TARGET_COLUMNS),
        ):
            names = ", ".join(f'"{c}"' for c, _ in columns)
            extra = ', "__SEED_ROW"' if table == "DEMO_TARGET1" else ""
            rows = cur.execute(
                f"SELECT {names}{extra} FROM {fqn(SRC, table)}"
            ).fetchall()
            destination = "demo_target1_pre_raw" if extra else "demo_source1"
            fields = columns + ([("__SEED_ROW", "NUMBER(38,0)")] if extra else [])
            definition = ", ".join(
                f'"{c}" '
                + (
                    "TIMESTAMP"
                    if t.startswith("TIMESTAMP")
                    else "DOUBLE"
                    if t.startswith("NUMBER")
                    else "VARCHAR"
                )
                for c, t in fields
            )
            # The baseline references the mixed-case legacy Key identifier.
            definition = definition.replace('"KEY"', '"Key"')
            con.execute(f"CREATE TABLE {destination} ({definition})")
            if rows:
                con.executemany(
                    f"INSERT INTO {destination} VALUES ({','.join('?' for _ in fields)})",
                    rows,
                )
        con.execute("""CREATE TEMP VIEW demo_target1_pre AS
            SELECT * EXCLUDE (__SEED_ROW, rn) FROM (
                SELECT *, ROW_NUMBER() OVER (
                    PARTITION BY ID ORDER BY "Key" DESC, __SEED_ROW DESC
                ) rn FROM demo_target1_pre_raw
            ) WHERE rn = 1""")
        baseline.mapping2(con)



def load(cur, manifest):
    subprocess.run([sys.executable, "tools/informatica_baseline.py"], cwd=ROOT, check=True)
    subprocess.run(["git", "diff", "--exit-code", "--", "baseline/informatica"], cwd=ROOT, check=True)
    seeded = {t: baseline_path(t).read_bytes() for t in OUTPUTS}
    for table, columns in (("DEMO_SOURCE1", SOURCE_COLUMNS), ("DEMO_TARGET1", TARGET_COLUMNS)):
        data = input_path(table).read_bytes()
        if hashlib.sha256(data).hexdigest() != manifest["inputs"]["file_hashes"][str(input_path(table).relative_to(ROOT))]:
            raise ValueError(f"Frozen input mismatch: {table}")
        rows = csv_rows(input_path(table), columns, data)
        if table == "DEMO_TARGET1":
            columns = columns + [("__SEED_ROW", "NUMBER(38,0)")]
            rows = [row + [i] for i, row in enumerate(rows, 1)]
        load_table(cur, SRC, table, columns, rows)
        count = cur.execute(f"SELECT COUNT(*) FROM {fqn(SRC, table)}").fetchone()[0]
        if count != manifest["inputs"]["row_counts"][table]:
            raise ValueError(f"SRC count mismatch: {table}")
    replay_from_src(cur)
    for table in OUTPUTS:
        if baseline_path(table).read_bytes() != seeded[table]:
            raise ValueError(f"SRC replay differs from independent baseline: {table}")
        load_table(cur, LEGACY, table, TARGET_COLUMNS, csv_rows(baseline_path(table), TARGET_COLUMNS))
    print(EMULATOR)


def canonical_row(row):
    if len(row) != len(TARGET_COLUMNS):
        raise ValueError("Wrong canonical row width")
    cells = []
    for value, (_, kind) in zip(row, TARGET_COLUMNS):
        if value is None:
            cells.append(r"\N")
            continue
        if kind.startswith("NUMBER"):
            number = Decimal(value)
            if number != number.to_integral_value():
                raise ValueError("KEY must be an integer")
            value = format(number, ".0f")
        elif kind.startswith("TIMESTAMP"):
            value = value.strftime("%Y-%m-%d %H:%M:%S.%f")
        cells.append(str(value).replace("\\", "\\\\").replace("|", r"\|"))
    return "|".join(cells)


def multiset_diff(left, right):
    def occurrences(rows):
        return {(v, i) for v, count in Counter(rows).items() for i in range(1, count + 1)}
    a, b = occurrences(left), occurrences(right)
    return {"legacy_only": sorted(a - b), "target_only": sorted(b - a)}


def table_evidence(cur, schema, table):
    metadata = cur.execute(
        f"SELECT COLUMN_NAME, DATA_TYPE, NUMERIC_PRECISION, NUMERIC_SCALE, DATETIME_PRECISION, CHARACTER_MAXIMUM_LENGTH "
        f"FROM {DATABASE}.INFORMATION_SCHEMA.COLUMNS "
        "WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s ORDER BY ORDINAL_POSITION",
        (schema, table),
    ).fetchall()
    if [r[0] for r in metadata] != [c for c, _ in TARGET_COLUMNS]:
        raise ValueError(f"XML target order mismatch: {fqn(schema, table)}")
    for row, (_, kind) in zip(metadata, TARGET_COLUMNS):
        if kind.startswith("NUMBER"):
            valid = row[1] in ("NUMBER", "FIXED") and tuple(row[2:4]) == (38, 0)
        elif kind.startswith("TIMESTAMP"):
            valid = row[1] == "TIMESTAMP_NTZ"
        else:
            valid = row[1] in ("TEXT", "VARCHAR")
        if not valid:
            raise ValueError(f"Unexpected target type: {row}")
    count = cur.execute(f"SELECT COUNT(*) FROM {fqn(schema, table)}").fetchone()[0]
    names = ", ".join(f'"{c}"' for c, _ in TARGET_COLUMNS)
    rows = [canonical_row(r) for r in cur.execute(f"SELECT {names} FROM {fqn(schema, table)}").fetchall()]
    if count != len(rows):
        raise ValueError("Table changed during parity")
    return {"fqn": fqn(schema, table), "columns_and_types": metadata, "count": count,
            "sha256": hashlib.sha256("\n".join(sorted(rows)).encode()).hexdigest()}, rows


def parity(cur, manifest, directory, history):
    counts = {t: cur.execute(f"SELECT COUNT(*) FROM {fqn(SRC, t)}").fetchone()[0] for t in INPUTS}
    results = []
    for table in OUTPUTS:
        left, a = table_evidence(cur, LEGACY, table)
        right, b = table_evidence(cur, TARGET, table)
        differences = multiset_diff(a, b)
        match = (left["columns_and_types"] == right["columns_and_types"]
                 and left["count"] == right["count"] and left["sha256"] == right["sha256"]
                 and not any(differences.values()))
        results.append({"table": table, "legacy": left, "target": right,
                        "rows_in": counts, "differences": differences, "match": match})
    runs = [h for h in history if h["action"] in ("load", "run")]
    tested = bool(runs and runs[-1]["action"] == "run" and runs[-1]["success"]
                  and runs[-1]["input_digest"] == manifest["input_digest"])
    loaded = any(h["action"] == "load" and h["success"] and h["input_digest"] == manifest["input_digest"] for h in runs)
    passed = loaded and tested and counts == manifest["inputs"]["row_counts"] and all(r["match"] for r in results)
    payload = {"manifest": manifest, "legacy_engine": EMULATOR, "normalizations": NORMALIZATIONS,
               "application": "Devin_Demo (unregistered)", "query_ids": cur.query_ids,
               "outputs": results, "converted_tests_passed": tested, "history": history, "match": passed}
    directory = outside_repo(directory)
    encoded = json.dumps(payload, indent=2, default=str)
    (directory / "evidence.json").write_text(encoded + "\n")
    (directory / "evidence.md").write_text(
        "# Frozen account dimension parity\n\n" + EMULATOR + "\n\n"
        + ("PASS" if passed else "FAIL") + "\n\n"
        + "```json\n" + encoded + "\n```\n")
    print("PASS" if passed else "FAIL")
    return passed


def offline(directory):
    directory = outside_repo(directory)
    database = directory / "account_dimension.duckdb"
    with duckdb.connect(str(database)) as con:
        con.execute("CREATE SCHEMA IF NOT EXISTS src")
        for table, columns in (("DEMO_SOURCE1", SOURCE_COLUMNS), ("DEMO_TARGET1", TARGET_COLUMNS)):
            fields = columns + ([("__SEED_ROW", "NUMBER(38,0)")] if table == "DEMO_TARGET1" else [])
            rows = csv_rows(input_path(table), columns)
            if table == "DEMO_TARGET1":
                rows = [row + [i] for i, row in enumerate(rows, 1)]
            definition = ", ".join(f'"{c}" {t.replace("NUMBER", "DECIMAL").replace("TIMESTAMP_NTZ(6)", "TIMESTAMP")}' for c, t in fields)
            con.execute(f"CREATE OR REPLACE TABLE src.{table} ({definition})")
            if rows:
                con.executemany(f"INSERT INTO src.{table} VALUES ({','.join('?' for _ in fields)})", rows)
    env = dict(os.environ, DBT_DUCKDB_PATH=str(database), DBT_QUERY_TAG="offline-duckdb")
    subprocess.run([str(Path(sys.executable).parent / "dbt"), "build", "--project-dir", str(PROJECT),
                    "--profiles-dir", str(PROJECT), "--target", "duckdb"], env=env, cwd=ROOT, check=True)


def compile_models(manifest, directory):
    directory = outside_repo(directory)
    env = {"DBT_QUERY_TAG": attributed_options()["session_parameters"]["QUERY_TAG"],
           "DBT_SF_DATABASE": DATABASE, "DBT_SF_TARGET_SCHEMA": TARGET, "DBT_SF_SOURCE_SCHEMA": SRC}
    # Fail closed if any adapter path attempts to open a Snowflake connection.
    with patch.dict(os.environ, env), patch(
        "snowflake.connector.connect", side_effect=RuntimeError(
            "dbt compile needs a Snowflake connection; no connection was made. Ask the operator to compile."
        )
    ):
        result = dbtRunner().invoke([
            "compile", "--project-dir", str(PROJECT), "--profiles-dir", str(PROJECT),
            "--target", "snowflake", "--target-path", str(directory),
            "--no-introspect", "--no-populate-cache", "--exclude", "resource_type:unit_test",
        ])
    if not result.success:
        raise RuntimeError("Connection-blocked dbt compile failed; see dbt output")
    artifact = directory / "manifest.json"
    (directory / "frozen_compile.json").write_text(json.dumps({
        "input_digest": manifest["input_digest"],
        "manifest_sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(),
    }))


def converted(cur, artifacts, frozen):
    receipt = json.loads((Path(artifacts) / "frozen_compile.json").read_text())
    if receipt != {"input_digest": frozen["input_digest"], "manifest_sha256": hashlib.sha256(
        (Path(artifacts) / "manifest.json").read_bytes()).hexdigest()}:
        raise ValueError("Compiled artifact does not match frozen inputs")
    manifest = json.loads((Path(artifacts) / "manifest.json").read_text())
    nodes = {k: n for k, n in manifest["nodes"].items() if n["resource_type"] in ("model", "test")}
    executed = 0
    while nodes:
        ready = [(k, n) for k, n in nodes.items() if not (set(n["depends_on"]["nodes"]) & nodes.keys())]
        if not ready:
            raise ValueError("Cyclic dbt dependencies")
        for key, node in ready:
            sql = node.get("compiled_code")
            if not sql or node.get("database") != DATABASE or node.get("schema", "").upper() != TARGET:
                raise ValueError(f"Missing compiled SQL or incorrect target: {key}")
            if node["resource_type"] == "model":
                materialization = node["config"]["materialized"].upper()
                if materialization not in ("VIEW", "TABLE"):
                    raise ValueError(f"Unsupported materialization: {materialization}")
                cur.execute(f'CREATE OR REPLACE {materialization} {fqn(TARGET, node["alias"])} AS {sql}')
            elif cur.execute(sql).fetchall():
                raise ValueError(f"dbt data test failed: {key}")
            executed += 1
            del nodes[key]
    if not executed:
        raise ValueError("No compiled nodes")
    print(f"Executed {executed} compiled models/data tests")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("setup", "freeze", "load", "compile", "run", "parity", "offline"))
    parser.add_argument("--manifest")
    parser.add_argument("--out")
    parser.add_argument("--artifacts", default=str(PROJECT / "target"))
    args = parser.parse_args()
    os.chdir(ROOT)
    if args.action in ("freeze", "offline"):
        if not args.out:
            parser.error("--out is required")
        (freeze if args.action == "freeze" else offline)(args.out)
        return
    if args.action in ("load", "compile", "run", "parity") and not args.manifest:
        parser.error("--manifest is required")
    if args.action == "parity" and not args.out:
        parser.error("--out is required")
    manifest: Any = verify_manifest(args.manifest) if args.manifest else None
    if args.action == "compile":
        if not args.out:
            parser.error("--out is required")
        compile_models(manifest, args.out)
        return
    if args.action == "setup" and not args.out:
        parser.error("setup requires --out to record query IDs outside the repository")
    history_dir = Path(args.manifest).resolve().parent if args.manifest else args.out
    history_path = outside_repo(history_dir) / "query_history.json"
    history = json.loads(history_path.read_text()) if history_path and history_path.exists() else []
    with connect() as con, con.cursor() as cursor:
        cur = Queries(cursor)
        success = False
        try:
            if args.action == "setup":
                setup(cur)
            else:
                compute_guard(cur)
                if args.action == "load":
                    load(cur, manifest)
                elif args.action == "run":
                    converted(cur, args.artifacts, manifest)
                elif not parity(cur, manifest, args.out, history):
                    raise SystemExit(1)
            success = True
        finally:
            history.append({"action": args.action, "input_digest": manifest["input_digest"] if manifest else None,
                            "success": success, "query_ids": cur.query_ids})
            history_path.write_text(json.dumps(history, indent=2) + "\n")
            print(json.dumps({"query_ids": cur.query_ids}))


if __name__ == "__main__":
    main()
