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
    output_dir: Path = Path("baseline/pyspark")
    account: str = ""
    user: str = ""
    role: str = ""
    warehouse: str = ""
    database: str = ""
    schema: str = ""
    schema_suffix_env: str = "SNOWFLAKE_SCHEMA_SUFFIX"

    @classmethod
    def from_yaml(cls, path: str | Path) -> "RunConfig":
        raw: dict[str, Any] = yaml.safe_load(Path(path).read_text()) or {}
        if isinstance(raw.get("business_date"), str):
            raw["business_date"] = date.fromisoformat(raw["business_date"])
        for key in ("input_dir", "output_dir"):
            if key in raw:
                raw[key] = Path(raw[key])
        return cls(**raw)


@dataclass
class RunContext:
    cfg: RunConfig
    spark: Any
    io: Any
