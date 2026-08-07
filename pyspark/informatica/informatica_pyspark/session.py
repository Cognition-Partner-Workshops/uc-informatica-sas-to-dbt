from pyspark.sql import SparkSession

from .config import RunConfig


def build_spark(cfg: RunConfig) -> SparkSession:
    # Later Snowflake milestone: add the connector package/jar here, for example
    # .config("spark.jars.packages", "net.snowflake:spark-snowflake_2.12:<version>").
    return (
        SparkSession.builder.appName("informatica-pyspark")
        .master("local[*]")
        .config("spark.sql.ansi.enabled", "false")
        .config("spark.sql.legacy.timeParserPolicy", "CORRECTED")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )
