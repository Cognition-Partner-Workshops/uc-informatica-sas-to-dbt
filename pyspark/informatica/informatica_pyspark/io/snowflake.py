from pyspark.sql import DataFrame, SparkSession, Window, functions as F

from .base import SourceReader, TargetWriter


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
        return frame.withColumn(
            "SRC_ORDINAL",
            F.row_number().over(Window.orderBy(F.monotonically_increasing_id())) - 1,
        )


class SnowflakeWriter(TargetWriter):
    def __init__(self, options: dict[str, str]):
        self.options = options

    def write(self, target_instance: str, df: DataFrame) -> None:
        output = df.drop("SRC_ORDINAL") if "SRC_ORDINAL" in df.columns else df
        (
            output.write.format("snowflake")
            .options(**self.options)
            .option("dbtable", target_instance)
            .mode("append")
            .save()
        )
