#!/usr/bin/env python3
"""Synchronize the nine dbt source seeds from the recovered legacy files."""

from pathlib import Path
import shutil
import sys


REPO_ROOT = Path(__file__).resolve().parents[3]
LEGACY = REPO_ROOT / "legacy" / "informatica" / "data"
SEEDS = Path(__file__).resolve().parents[1] / "seeds"
FILES = (
    "demo_source1.csv",
    "demo_source2.csv",
    "demo_source3.csv",
    "demo_source4.csv",
    "demo_source5.csv",
    "lkp_demo_source1.csv",
    "lkp_demo_source2.csv",
    "lkp_demo_source3.csv",
    "demo_target1.csv",
)


def main() -> int:
    SEEDS.mkdir(parents=True, exist_ok=True)
    mismatches = []
    for filename in FILES:
        source = LEGACY / filename
        destination = SEEDS / filename
        if not source.is_file():
            print(f"missing legacy seed: {source}", file=sys.stderr)
            return 1
        shutil.copyfile(source, destination)
        if source.read_bytes() != destination.read_bytes():
            mismatches.append(filename)
    if mismatches:
        print("seed drift detected: " + ", ".join(mismatches), file=sys.stderr)
        return 1
    print(f"synchronized and verified {len(FILES)} seeds")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
