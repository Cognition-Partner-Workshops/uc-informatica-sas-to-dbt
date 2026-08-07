import shutil
from pathlib import Path

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from .schemas import LOOKUP_SCHEMAS, SOURCE_SCHEMAS, TARGET_SCHEMAS


class CsvIO:
    def __init__(self, spark, cfg):
        self.spark, self.cfg = spark, cfg

    def read(self, name: str) -> DataFrame:
        schema = SOURCE_SCHEMAS.get(name) or LOOKUP_SCHEMAS.get(name) or TARGET_SCHEMAS[name]
        path = Path(self.cfg.input_dir) / f"{name}.csv"
        df = self.spark.read.option("header", True).schema(schema).csv(str(path))
        if name in LOOKUP_SCHEMAS or name == "demo_target1":
            df = df.withColumn("__line_ordinal", F.monotonically_increasing_id())
        return df

    def write(self, instance: str, df: DataFrame):
        out = Path(self.cfg.output_dir)
        out.mkdir(parents=True, exist_ok=True)
        temp = out / f".{instance}.tmp"
        if temp.exists():
            shutil.rmtree(temp)
        formatted = df
        for field in df.schema.fields:
            if field.dataType.simpleString() in ("date", "timestamp"):
                formatted = formatted.withColumn(
                    field.name, F.date_format(F.col(field.name), "yyyy-MM-dd HH:mm:ss")
                )
        formatted.coalesce(1).write.mode("overwrite").option("header", True).csv(str(temp))
        part = next(temp.glob("part-*.csv"))
        target = out / f"{instance}.csv"
        if target.exists():
            target.unlink()
        shutil.move(str(part), str(target))
        shutil.rmtree(temp)


class SnowflakeIO:
    """Snowflake shape; connection options are intentionally wired for a later milestone."""

    def __init__(self, spark, cfg):
        self.spark, self.cfg = spark, cfg
        self.options = {
            "sfURL": cfg.account,
            "sfUser": cfg.user,
            "sfRole": cfg.role,
            "sfWarehouse": cfg.warehouse,
            "sfDatabase": cfg.database,
            "sfSchema": cfg.schema,
        }

    def read(self, name: str) -> DataFrame:
        return self.spark.read.format("snowflake").options(**self.options).option(
            "dbtable", name
        ).load()

    def write(self, instance: str, df: DataFrame):
        df.write.format("snowflake").options(**self.options).option(
            "dbtable", instance
        ).mode("overwrite").save()
