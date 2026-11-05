"""Load isolated Informatica inputs; empty CSV fields alone are SQL NULL."""
import os
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[3]
SCHEMA = "infa_src_infa_m23"


def load(path=None, data=None):
    path = Path(path or os.environ.get("INFA_DUCKDB_PATH", "target/infa.duckdb"))
    data = Path(data or ROOT / "legacy/informatica/data")
    path.parent.mkdir(parents=True, exist_ok=True)
    with duckdb.connect(str(path)) as con:
        con.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}")
        for name in ("demo_source1", "demo_source2", "demo_target1"):
            con.execute(
                f'CREATE OR REPLACE TABLE {SCHEMA}."{name}" AS '
                "SELECT row_number() OVER () AS SEED_ROW, * "
                "FROM read_csv(?, header=true, all_varchar=true, nullstr='')",
                [str(data / f"{name}.csv")],
            )
            print(f"Loaded {SCHEMA}.{name}")


if __name__ == "__main__":
    load()
