from pyspark.sql import SparkSession

from .config import RunConfig


def build_spark(cfg: RunConfig) -> SparkSession:
    return (
        SparkSession.builder.appName("informatica-pyspark")
        .master("local[*]")
        .config("spark.sql.ansi.enabled", "false")
        .getOrCreate()
    )
