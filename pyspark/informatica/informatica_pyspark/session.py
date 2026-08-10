from pathlib import Path

from pyspark.sql import SparkSession

from .config import RunConfig


def build_spark(config: RunConfig) -> SparkSession:
    builder = (
        SparkSession.builder.appName("informatica-pyspark")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.sql.session.timeZone", "UTC")
        .config("spark.sql.adaptive.enabled", "false")
        .config("spark.sql.legacy.timeParserPolicy", "CORRECTED")
    )
    if config.io_mode == "snowflake":
        jar_dir = Path.home() / ".cache" / "informatica-pyspark" / "jars"
        jars = (
            jar_dir / "spark-snowflake_2.12-3.2.1-spark_3.5.jar",
            jar_dir / "snowflake-jdbc-4.0.2.jar",
        )
        missing = [str(path) for path in jars if not path.is_file()]
        if missing:
            raise FileNotFoundError(f"Snowflake jars not found: {', '.join(missing)}")
        builder = builder.config("spark.jars", ",".join(str(path) for path in jars))
    return builder.getOrCreate()
