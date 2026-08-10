import subprocess
import sys
from pathlib import Path


def test_comparison_builder_audits_xml_expression_coverage():
    root = Path(__file__).resolve().parents[3]
    completed = subprocess.run(
        [sys.executable, "pyspark/informatica/scripts/build_comparison_table.py"],
        cwd=root,
        text=True,
        capture_output=True,
    )
    assert completed.returncode == 0, completed.stderr
    assert "Coverage audit: 89/89 TRANSFORMFIELD expressions" in completed.stdout
