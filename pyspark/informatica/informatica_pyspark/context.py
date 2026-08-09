from dataclasses import dataclass, field
from datetime import datetime, time
from typing import Callable

from pyspark.sql import Column, DataFrame, SparkSession, functions as F

from .config import RunConfig


class InformaticaAbort(RuntimeError):
    """An Informatica ABORT expression stopped the mapping."""


@dataclass(frozen=True)
class AbortCheck:
    predicate_df: DataFrame
    message: str


@dataclass
class MappingResult:
    targets: dict[str, DataFrame] = field(default_factory=dict)
    abort_checks: list[AbortCheck] = field(default_factory=list)
    sort_keys: dict[str, tuple[str, ...]] = field(default_factory=dict)


@dataclass
class MappingContext:
    spark: SparkSession
    config: RunConfig
    sources: dict[str, DataFrame]
    log: Callable[[str], None] = print

    @property
    def sysdate(self) -> Column:
        return F.lit(self.config.business_date)

    @property
    def systimestamp(self) -> Column:
        value = datetime.combine(self.config.business_date, time.min)
        return F.lit(value)
