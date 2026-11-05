"""Offline regression checks for the account-dimension loader and canonical form."""

import csv
import hashlib
import json
import tempfile
import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from unittest.mock import MagicMock, patch

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, NoEncryption, PrivateFormat

import informatica_account_dim_snowflake as job


class TypedCsvTests(unittest.TestCase):
    def write_csv(self, directory, columns, values):
        path = Path(directory) / "input.csv"
        with path.open("w", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(c for c, _ in columns)
            writer.writerow(values)
        return path

    def test_text_is_not_inferred_as_boolean_date_or_number(self):
        with tempfile.TemporaryDirectory() as directory:
            values = ["Y", "FALSE", "2024-01-31", "00001", "N", "TRUE"]
            path = self.write_csv(directory, job.SOURCE_COLUMNS, values)
            self.assertEqual(job.csv_rows(path, job.SOURCE_COLUMNS), [values])

    def test_timestamp_microseconds_and_year_9999_are_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            columns = [("KEY", "NUMBER(38,0)"), ("TS", "TIMESTAMP_NTZ(6)")]
            path = self.write_csv(
                directory, columns, ["99", "9999-12-31 12:34:56.123456"]
            )
            self.assertEqual(
                job.csv_rows(path, columns),
                [[Decimal(99), "9999-12-31 12:34:56.123456"]],
            )

    def test_date_only_timestamp_and_empty_null(self):
        with tempfile.TemporaryDirectory() as directory:
            columns = [("TS", "TIMESTAMP_NTZ(6)"), ("FLAG", "VARCHAR")]
            path = self.write_csv(directory, columns, ["2024-01-31", ""])
            self.assertEqual(
                job.csv_rows(path, columns), [["2024-01-31 00:00:00.000000", None]]
            )

    def test_wrong_column_order_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_csv(
                directory, list(reversed(job.SOURCE_COLUMNS)), ["x"] * 6
            )
            with self.assertRaises(ValueError):
                job.csv_rows(path, job.SOURCE_COLUMNS)

    def test_empty_csv_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty.csv"
            path.touch()
            with self.assertRaises(ValueError):
                job.csv_rows(path, job.SOURCE_COLUMNS)


class CanonicalTests(unittest.TestCase):
    def row(self, value):
        return [Decimal(57), value] + [None] * 12

    def test_null_empty_and_literal_sentinel_differ(self):
        rows = {job.canonical_row(self.row(v)) for v in (None, "", r"\N")}
        self.assertEqual(len(rows), 3)

    def test_no_trim_and_delimiters_escaped(self):
        self.assertNotEqual(job.canonical_row(self.row(" x ")), job.canonical_row(self.row("x")))
        self.assertIn(r"a\|b\\c", job.canonical_row(self.row(r"a|b\c")))

    def test_key_and_timestamp(self):
        row = self.row("x")
        row[8] = datetime(2024, 1, 31, 0, 0, 0, 123456)
        canonical = job.canonical_row(row)
        self.assertTrue(canonical.startswith("57|"))
        self.assertIn("2024-01-31 00:00:00.123456", canonical)
        row[0] = Decimal("9" * 38)
        self.assertTrue(job.canonical_row(row).startswith("9" * 38 + "|"))
        row[0] = Decimal("1.5")
        with self.assertRaisesRegex(ValueError, "integer"):
            job.canonical_row(row)
        with self.assertRaisesRegex(ValueError, "width"):
            job.canonical_row([])

    def test_multiset_duplicate_multiplicity(self):
        self.assertEqual(job.multiset_diff(["x", "x"], ["x", "y"]), {
            "legacy_only": [("x", 2)], "target_only": [("y", 1)]})
        self.assertEqual(job.multiset_diff([], []), {"legacy_only": [], "target_only": []})
        self.assertEqual(job.multiset_diff(["x", "y"], ["y", "x"]), {
            "legacy_only": [], "target_only": []})


class ManifestTests(unittest.TestCase):
    def test_digest_determinism(self):
        self.assertEqual(job.digest({"b": 1, "a": {"y": 2, "x": 3}}),
                         job.digest({"a": {"x": 3, "y": 2}, "b": 1}))

    def test_roundtrip_and_mismatch_abort(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = job.freeze(directory)
            path = Path(directory) / "manifest.json"
            self.assertEqual(job.verify_manifest(path), manifest)
            changed = dict(manifest["inputs"], row_counts={"DEMO_SOURCE1": 999})
            with patch.object(job, "frozen_section", return_value=changed):
                with self.assertRaisesRegex(ValueError, "Frozen input mismatch"):
                    job.verify_manifest(path)
            manifest["input_digest"] = "invalid"
            path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, "Invalid manifest"):
                job.verify_manifest(path)

    def test_counts_include_physical_duplicates(self):
        counts = job.frozen_section()["row_counts"]
        for table in job.INPUTS:
            with job.input_path(table).open(newline="") as stream:
                self.assertEqual(counts[table], len(list(csv.DictReader(stream))))

    def test_repository_output_rejected(self):
        with self.assertRaisesRegex(ValueError, "outside"):
            job.outside_repo(job.ROOT / "evidence")


class GuardTests(unittest.TestCase):
    def cursor(self, monitor=None, size="X-Small", suspend=60, tag=None):
        cur = MagicMock()
        cur.execute.return_value = cur
        cur.description = [(n,) for n in ("name", "resource_monitor", "size", "auto_suspend")]
        cur.fetchall.return_value = [(job.WAREHOUSE, monitor, size, suspend)]
        cur.fetchone.return_value = (tag or job.EP.csid,)
        return cur

    def test_refuses_unattached_warehouse_before_tag_query(self):
        cur = self.cursor()
        with self.assertRaisesRegex(ValueError, "resource monitor"):
            job.compute_guard(cur)
        self.assertEqual(cur.execute.call_count, 1)

    def test_missing_warehouse(self):
        cur = self.cursor()
        cur.fetchall.return_value = []
        with self.assertRaises(ValueError):
            job.compute_guard(cur)

    def test_size_suspend_and_tag(self):
        for kwargs in ({"size": "Large"}, {"suspend": 0}, {"tag": "other"}):
            with self.assertRaises(ValueError):
                job.compute_guard(self.cursor(monitor=job.MONITOR, **kwargs))
        job.compute_guard(self.cursor(monitor=job.MONITOR))

    def test_setup_only_verifies_monitor_and_records_queries(self):
        cursor = self.cursor(monitor=job.MONITOR)
        cursor.sfqid = "query-id"
        tracked = job.Queries(cursor)
        job.setup(tracked)
        statements = [call.args[0] for call in cursor.execute.call_args_list]
        self.assertFalse(any("SET RESOURCE_MONITOR" in s for s in statements))
        self.assertTrue(any("SET TAG" in s for s in statements))
        self.assertEqual(sum(s.startswith("SHOW WAREHOUSES") for s in statements), 2)
        self.assertEqual(len(tracked.query_ids), len(statements))


class ExecutionTests(unittest.TestCase):
    def artifacts(self, directory, nodes):
        path = Path(directory) / "manifest.json"
        path.write_text(json.dumps({"nodes": nodes}))
        (Path(directory) / "frozen_compile.json").write_text(json.dumps({
            "input_digest": "frozen", "manifest_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}))

    def test_compiled_dependency_order_and_tests(self):
        base = {"database": job.DATABASE, "schema": job.TARGET}
        nodes = {
            "test": dict(base, schema=job.TARGET + "_dbt_test__audit", resource_type="test", compiled_code="SELECT 1 WHERE FALSE", depends_on={"nodes": ["model"]}),
            "model": dict(base, resource_type="model", compiled_code="SELECT 1", alias="M", config={"materialized": "table"}, depends_on={"nodes": []}),
        }
        with tempfile.TemporaryDirectory() as directory:
            self.artifacts(directory, nodes)
            cursor = MagicMock()
            cursor.execute.return_value.fetchall.return_value = []
            job.converted(cursor, directory, {"input_digest": "frozen"})
            self.assertIn("CREATE OR REPLACE TABLE", cursor.execute.call_args_list[0].args[0])
            self.assertEqual(cursor.execute.call_args_list[1].args[0], "SELECT 1 WHERE FALSE")
            cursor.execute.return_value.fetchall.return_value = [(1,)]
            with self.assertRaisesRegex(ValueError, "data test failed"):
                job.converted(cursor, directory, {"input_digest": "frozen"})
            with self.assertRaisesRegex(ValueError, "does not match"):
                job.converted(cursor, directory, {"input_digest": "changed"})

    def test_empty_compilation_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            self.artifacts(directory, {})
            with self.assertRaisesRegex(ValueError, "No compiled nodes"):
                job.converted(MagicMock(), directory, {"input_digest": "frozen"})

    def test_table_metadata_order_and_empty_checksum(self):
        metadata = [(c, "NUMBER", 38, 0, None, None) if t.startswith("NUMBER") else
                    (c, "TIMESTAMP_NTZ", None, None, None, None) if t.startswith("TIMESTAMP") else
                    (c, "TEXT", None, None, None, 16777216) for c, t in job.TARGET_COLUMNS]
        cursor = MagicMock()
        cursor.execute.return_value = cursor
        cursor.fetchall.side_effect = [metadata, []]
        cursor.fetchone.return_value = (0,)
        result, rows = job.table_evidence(cursor, job.LEGACY, job.OUTPUTS[0])
        self.assertEqual(rows, [])
        self.assertEqual(result["sha256"], hashlib.sha256(b"").hexdigest())
        cursor.fetchall.side_effect = [metadata[::-1]]
        with self.assertRaisesRegex(ValueError, "order mismatch"):
            job.table_evidence(cursor, job.LEGACY, job.OUTPUTS[0])

    def test_parity_requires_tested_run_and_preserves_differences(self):
        cursor = MagicMock()
        cursor.execute.return_value.fetchone.return_value = (1,)
        cursor.query_ids = ["qid"]
        manifest = {"input_digest": "frozen", "inputs": {"row_counts": dict.fromkeys(job.INPUTS, 1)}}
        history = [{"action": action, "success": True, "input_digest": "frozen"} for action in ("load", "run")]
        evidence = {"columns_and_types": [], "count": 1, "sha256": "same"}
        with tempfile.TemporaryDirectory() as directory, patch.object(job, "table_evidence", return_value=(evidence, ["row"])):
            self.assertTrue(job.parity(cursor, manifest, directory, history))
            self.assertFalse(job.parity(cursor, manifest, directory, []))
            report = json.loads((Path(directory) / "evidence.json").read_text())
            self.assertEqual(report["normalizations"], job.NORMALIZATIONS)
            self.assertEqual(report["query_ids"], ["qid"])


class ConnectionTests(unittest.TestCase):
    def test_endpoint_registered(self):
        self.assertEqual(job.sf.endpoint("cs_mig_inf_account_dimension"), job.EP)
        self.assertEqual(job.DATABASE, job.sf.database_name("mig_inf"))

    def test_connect_params(self):
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        pem = key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()).decode()
        env = {"SNOWFLAKE_EXT_ACCOUNT": "test", "SNOWFLAKE_EXT_USER": "EXT_TEST",
               "SNOWFLAKE_EXT_PRIVATE_KEY": pem, "DEVIN_SESSION_URL": "https://app.devin.ai/sessions/00000000000000000000000000000000",
               "SF_RUN_ID": job.sf.make_run_id("mig_inf", "dev")}
        with patch.dict(job.os.environ, env), patch.object(job, "published_commit", return_value="a" * 40), patch.object(job.snowflake.connector, "connect") as connector:
            job.connect()
        params = connector.call_args.kwargs
        self.assertNotIn("private_key_file", params)
        self.assertEqual(params["private_key"], key.private_bytes(Encoding.DER, PrivateFormat.PKCS8, NoEncryption()))
        self.assertEqual(params["user"], "EXT_TEST")
        self.assertEqual(params["application"], "Devin_Demo")
        self.assertEqual(params["role"], "DEVIN_EXT_ROLE")
        self.assertEqual(params["warehouse"], job.WAREHOUSE)
        tag = json.loads(params["session_parameters"]["QUERY_TAG"])
        self.assertEqual(list(tag), ["csid", "workload", "phase", "commit", "run_id", "session_url"])
        self.assertEqual(tag["session_url"], env["DEVIN_SESSION_URL"])

    def test_dirty_or_unpublished_head_refused(self):
        with patch.object(job.sf, "resolve_commit", return_value="a" * 40):
            for outputs in (["a" * 40, "modified"], ["a" * 40, "", ""]):
                with patch.object(job, "git", side_effect=outputs), self.assertRaises(ValueError):
                    job.published_commit()

    def test_clean_published_head(self):
        with patch.object(job.sf, "resolve_commit", return_value="a" * 40), patch.object(job, "git", side_effect=["a" * 40, "", "origin/feature"]):
            self.assertEqual(job.published_commit(), "a" * 40)


if __name__ == "__main__":
    unittest.main()
