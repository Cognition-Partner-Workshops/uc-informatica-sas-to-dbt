from pyspark.sql import DataFrame, SparkSession

from .base import ORDINAL_COL, SourceReader, TargetWriter


class SnowflakeReader(SourceReader):
    def __init__(self, spark: SparkSession, options: dict[str, str]):
        self.spark = spark
        self.options = options

    def read(self, logical_name: str) -> DataFrame:
        frame = (
            self.spark.read.format("snowflake")
            .options(**self.options)
            .option("dbtable", logical_name)
            .load()
        )
        if ORDINAL_COL not in frame.columns:
            raise ValueError(
                f"Snowflake source {logical_name!r} must contain persisted {ORDINAL_COL}"
            )
        return frame


class SnowflakeWriter(TargetWriter):
    def __init__(self, options: dict[str, str]):
        self.options = options

    def write(self, target_instance: str, df: DataFrame) -> None:
        output = df.drop("SRC_ORDINAL") if "SRC_ORDINAL" in df.columns else df
        (
            output.write.format("snowflake")
            .options(**self.options)
            .option("dbtable", target_instance)
            .mode("overwrite")
            .save()
        )
