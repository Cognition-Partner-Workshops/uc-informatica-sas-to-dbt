from pyspark.sql import SparkSession

from .config import RunConfig


def build_spark(config: RunConfig) -> SparkSession:
    return (
        SparkSession.builder.appName("informatica-pyspark")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.sql.session.timeZone", "UTC")
        .config("spark.sql.adaptive.enabled", "false")
        .config("spark.sql.legacy.timeParserPolicy", "CORRECTED")
        .getOrCreate()
    )
