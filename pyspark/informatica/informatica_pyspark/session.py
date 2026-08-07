from pyspark.sql import SparkSession

from .config import RunConfig


def build_spark(cfg: RunConfig) -> SparkSession:
    builder = (
        SparkSession.builder.appName("informatica-pyspark")
        .master("local[*]")
        .config("spark.sql.ansi.enabled", "false")
        .config("spark.sql.legacy.timeParserPolicy", "CORRECTED")
        .config("spark.sql.session.timeZone", "UTC")
    )
    if cfg.io == "snowflake":
        packages = ",".join(
            [
                f"net.snowflake:spark-snowflake_2.12:{cfg.snowflake_connector_version}",
                f"net.snowflake:snowflake-jdbc:{cfg.snowflake_jdbc_version}",
            ]
        )
        builder = builder.config("spark.jars.packages", packages)
    return builder.getOrCreate()
