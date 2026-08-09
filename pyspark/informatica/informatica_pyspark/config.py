from dataclasses import dataclass, field
from datetime import date
from typing import Literal


@dataclass(frozen=True)
class RunConfig:
    business_date: date = date(2024, 1, 31)
    io_mode: Literal["local", "snowflake"] = "local"
    source_dir: str = "legacy/informatica/data"
    target_dir: str = "out/pyspark/local"
    source_variant: Literal["normal", "abort"] = "normal"
    account: str = ""
    user: str = ""
    role: str = ""
    warehouse: str = ""
    database: str = ""
    source_schema: str = ""
    target_schema: str = ""
    baseline_schema: str = ""
    private_key_path: str = ""
    extra: dict = field(default_factory=dict)
