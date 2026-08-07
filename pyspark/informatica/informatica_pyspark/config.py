from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class RunConfig:
    io: str = "csv"
    business_date: date = date(2024, 1, 31)
    input_dir: Path = Path("legacy/informatica/data")
    output_dir: Path = Path("build/pyspark/informatica")
    account: str = ""
    user: str = ""
    role: str = ""
    warehouse: str = ""
    database: str = ""
    schema: str = ""
    source_schema: str = ""
    migrated_target_schema: str = ""
    baseline_schema: str = ""
    run_schema_suffix: str = ""
    schema_suffix_env: str = "SNOWFLAKE_SCHEMA_SUFFIX"
    private_key_path: Path | None = None
    snowflake_connector_version: str = "2.16.0-spark_3.5"
    snowflake_jdbc_version: str = "3.18.0"

    @classmethod
    def from_yaml(cls, path: str | Path) -> "RunConfig":
        raw: dict[str, Any] = yaml.safe_load(Path(path).read_text()) or {}
        if isinstance(raw.get("business_date"), str):
            raw["business_date"] = date.fromisoformat(raw["business_date"])
        for key in ("input_dir", "output_dir", "private_key_path"):
            if key in raw:
                raw[key] = Path(raw[key]) if raw[key] else None
        return cls(**raw)


@dataclass
class RunContext:
    cfg: RunConfig
    spark: Any
    io: Any
