"""Offline regression checks for the account-dimension loader and canonical form."""

import csv
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

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
    def test_canonical_sql_uses_legacy_order_and_exact_formats(self):
        sql = job.canonical_sql(job.LEGACY, "DEMO_TARGET1_INS")
        positions = [sql.index(f'"{column}"') for column, _ in job.TARGET_COLUMNS]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("NUMBER(38,6)", sql)
        self.assertIn("YYYY-MM-DD HH24:MI:SS.FF6", sql)
        self.assertEqual(sql.count("'\\\\N'"), 14)


if __name__ == "__main__":
    unittest.main()
