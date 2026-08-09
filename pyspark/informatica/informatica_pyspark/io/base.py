from abc import ABC, abstractmethod

from pyspark.sql import DataFrame

ORDINAL_COL = "SRC_ORDINAL"


class SourceReader(ABC):
    @abstractmethod
    def read(self, logical_name: str) -> DataFrame:
        raise NotImplementedError


class TargetWriter(ABC):
    @abstractmethod
    def write(self, target_instance: str, df: DataFrame) -> None:
        raise NotImplementedError
