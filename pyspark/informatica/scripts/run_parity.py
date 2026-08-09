"""Invoke the repository's unmodified parity comparator."""

import argparse
import subprocess
import sys
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--actual", default="out/pyspark/local")
    parser.add_argument("--report", default="docs/parity/informatica_pyspark_parity.md")
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[3]
    command = [
        sys.executable, str(root / "tools/parity_diff.py"),
        "--baseline", "baseline/informatica",
        "--actual", args.actual,
        "--keys", "tools/keys/informatica_keys.json",
        "--report", args.report,
    ]
    return subprocess.run(command, cwd=root).returncode


if __name__ == "__main__":
    raise SystemExit(main())
