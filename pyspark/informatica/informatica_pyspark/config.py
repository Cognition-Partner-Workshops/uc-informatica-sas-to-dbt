from __future__ import annotations

import datetime as dt
import os
from dataclasses import dataclass, field
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DATA_DIR = REPO_ROOT / "legacy" / "informatica" / "data"


@dataclass(frozen=True)
class RunConfig:
    business_date: dt.date
    io_mode: str = "local"
    data_dir: Path = DEFAULT_DATA_DIR
    out_dir: Path = Path("out")
    account: str | None = None
    user: str | None = None
    role: str | None = None
    warehouse: str | None = None
    database: str | None = None
    src_schema: str | None = None
    run_schema: str | None = None
    snowflake_private_key: str | None = field(
        default=None, init=False, repr=False, compare=False
    )

    def __post_init__(self) -> None:
        if self.io_mode not in {"local", "snowflake"}:
            raise ValueError("io_mode must be 'local' or 'snowflake'")
        object.__setattr__(
            self, "snowflake_private_key", os.environ.get("SNOWFLAKE_PRIVATE_KEY")
        )
        data_dir = Path(self.data_dir)
        if not data_dir.is_absolute():
            data_dir = REPO_ROOT / data_dir
        object.__setattr__(self, "data_dir", data_dir)
        object.__setattr__(self, "out_dir", Path(self.out_dir))

    @property
    def business_timestamp(self) -> dt.datetime:
        return dt.datetime.combine(self.business_date, dt.time.min)

    @property
    def snowflake_account(self) -> str | None:
        return self.account

    @property
    def snowflake_user(self) -> str | None:
        return self.user

    @property
    def snowflake_role(self) -> str | None:
        return self.role

    @property
    def snowflake_warehouse(self) -> str | None:
        return self.warehouse

    @property
    def snowflake_database(self) -> str | None:
        return self.database

    @property
    def snowflake_src_schema(self) -> str | None:
        return self.src_schema

    @property
    def snowflake_run_schema(self) -> str | None:
        return self.run_schema
