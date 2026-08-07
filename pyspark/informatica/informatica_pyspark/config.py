from dataclasses import dataclass, field
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
    input_overrides: dict[str, str] = field(default_factory=dict)
    snowflake_connector_version: str = "3.2.1"
    snowflake_jdbc_version: str = "4.0.2"
    snowflake_jars_dir: Path | None = None

    @classmethod
    def from_yaml(cls, path: str | Path) -> "RunConfig":
        raw: dict[str, Any] = yaml.safe_load(Path(path).read_text()) or {}
        if isinstance(raw.get("business_date"), str):
            raw["business_date"] = date.fromisoformat(raw["business_date"])
        for key in (
            "input_dir",
            "output_dir",
            "private_key_path",
            "snowflake_jars_dir",
        ):
            if key in raw:
                raw[key] = Path(raw[key]).expanduser() if raw[key] else None
        return cls(**raw)


@dataclass
class RunContext:
    cfg: RunConfig
    spark: Any
    io: Any
