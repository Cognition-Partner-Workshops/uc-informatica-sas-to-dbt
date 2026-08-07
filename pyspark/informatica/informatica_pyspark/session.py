from __future__ import annotations

import os

from pyspark.sql import SparkSession

from .config import RunConfig


DEFAULT_SPARK_JARS = (
    "/home/ubuntu/spark-jars/"
    "spark-snowflake_2.12-3.2.1-spark_3.5.jar,"
    "/home/ubuntu/spark-jars/snowflake-jdbc-4.0.2.jar"
)


def build_spark(cfg: RunConfig) -> SparkSession:
    builder = (
        SparkSession.builder.appName("informatica-pyspark")
        .master("local[*]")
        .config("spark.sql.session.timeZone", "UTC")
        .config("spark.sql.shuffle.partitions", "4")
        .config("spark.sql.adaptive.enabled", "false")
    )
    if cfg.io_mode == "snowflake":
        builder = builder.config(
            "spark.jars", os.environ.get("INFORMATICA_SPARK_JARS", DEFAULT_SPARK_JARS)
        )
    return builder.getOrCreate()
