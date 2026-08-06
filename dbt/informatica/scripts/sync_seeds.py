#!/usr/bin/env python3
"""Synchronize the nine dbt source seeds from the recovered legacy files."""

import csv
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
ORDINAL_FILES = {
    "lkp_demo_source1.csv",
    "lkp_demo_source2.csv",
    "lkp_demo_source3.csv",
    "demo_target1.csv",
}


def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.reader(handle))


def synchronize_ordinal_seed(source: Path, destination: Path) -> bool:
    source_rows = read_csv(source)
    expected_header = source_rows[0] + ["SEED_ROW"]
    expected_rows = [
        row + [str(seed_row)]
        for seed_row, row in enumerate(source_rows[1:], start=1)
    ]
    drifted = True
    if destination.exists():
        actual_rows = read_csv(destination)
        stripped_rows = [row[:-1] for row in actual_rows[1:]]
        ordinals = [row[-1] for row in actual_rows[1:]]
        drifted = (
            actual_rows[:1] != [expected_header]
            or stripped_rows != source_rows[1:]
            or ordinals != [str(i) for i in range(1, len(source_rows))]
        )
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(expected_header)
        writer.writerows(expected_rows)
    return drifted


def main() -> int:
    SEEDS.mkdir(parents=True, exist_ok=True)
    mismatches = []
    for filename in FILES:
        source = LEGACY / filename
        destination = SEEDS / filename
        if not source.is_file():
            print(f"missing legacy seed: {source}", file=sys.stderr)
            return 1
        if filename in ORDINAL_FILES:
            drifted = synchronize_ordinal_seed(source, destination)
        else:
            drifted = destination.exists() and source.read_bytes() != destination.read_bytes()
            shutil.copyfile(source, destination)
        if drifted:
            mismatches.append(filename)
    if mismatches:
        print("seed drift detected: " + ", ".join(mismatches), file=sys.stderr)
        return 1
    print(f"synchronized and verified {len(FILES)} seeds")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
