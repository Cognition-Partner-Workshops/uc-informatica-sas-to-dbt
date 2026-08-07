import shutil
import base64
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F
from pyspark.sql.types import DateType, TimestampType

from .schemas import LOOKUP_SCHEMAS, SOURCE_SCHEMAS, TARGET_SCHEMAS

LINE_ORDINAL_INPUTS = {
    "demo_source1",
    "demo_target1",
    "lkp_demo_source1",
    "lkp_demo_source2",
    "lkp_demo_source3",
}

def attach_line_ordinal(df: DataFrame, col: str = "__line_ordinal") -> DataFrame:
    """Attach the physical input order used by Informatica row policies."""
    return (
        df.coalesce(1)
        .withColumn("__physical_row", F.monotonically_increasing_id())
        .withColumn(
            col,
            F.row_number().over(Window.orderBy(F.col("__physical_row"))) - 1,
        )
        .drop("__physical_row")
    )


class CsvIO:
    def __init__(self, spark, cfg):
        self.spark, self.cfg = spark, cfg

    def read(self, name: str) -> DataFrame:
        schema = SOURCE_SCHEMAS.get(name) or LOOKUP_SCHEMAS.get(name) or TARGET_SCHEMAS[name]
        path = Path(self.cfg.input_overrides.get(name, Path(self.cfg.input_dir) / f"{name}.csv"))
        df = self.spark.read.option("header", True).schema(schema).csv(str(path))
        if name in LINE_ORDINAL_INPUTS:
            df = attach_line_ordinal(df)
        return df

    def write(self, instance: str, df: DataFrame):
        out = Path(self.cfg.output_dir)
        out.mkdir(parents=True, exist_ok=True)
        temp = out / f".{instance}.tmp"
        if temp.exists():
            shutil.rmtree(temp)
        formatted = df
        for field in df.schema.fields:
            if isinstance(field.dataType, DateType):
                formatted = formatted.withColumn(
                    field.name, F.date_format(F.col(field.name), "yyyy-MM-dd")
                )
            elif isinstance(field.dataType, TimestampType):
                formatted = formatted.withColumn(
                    field.name,
                    F.regexp_replace(
                        F.date_format(F.col(field.name), "yyyy-MM-dd HH:mm:ss"),
                        r" 00:00:00$",
                        "",
                    ),
                )
        formatted.coalesce(1).write.mode("overwrite").option("header", True).csv(str(temp))
        part = next(temp.glob("part-*.csv"))
        target = out / f"{instance}.csv"
        if target.exists():
            target.unlink()
        shutil.move(str(part), str(target))
        shutil.rmtree(temp)


class SnowflakeIO:
    """Spark Snowflake connector IO for one namespaced migration run."""

    def __init__(self, spark, cfg):
        self.spark, self.cfg = spark, cfg
        self.options = {
            "sfURL": cfg.account,
            "sfUser": cfg.user,
            "sfRole": cfg.role,
            "sfWarehouse": cfg.warehouse,
            "sfDatabase": cfg.database,
        }
        if cfg.private_key_path:
            key = serialization.load_pem_private_key(
                cfg.private_key_path.read_bytes(), password=None
            )
            der = key.private_bytes(
                serialization.Encoding.DER,
                serialization.PrivateFormat.PKCS8,
                serialization.NoEncryption(),
            )
            self.options["pem_private_key"] = base64.b64encode(der).decode("ascii")

    def _options(self, schema):
        sf_url = self.cfg.account
        if not sf_url.endswith(".snowflakecomputing.com"):
            sf_url = f"{sf_url}.snowflakecomputing.com"
        return {**self.options, "sfURL": sf_url, "sfSchema": schema}

    def read(self, name: str) -> DataFrame:
        df = (
            self.spark.read.format("snowflake")
            .options(**self._options(self.cfg.source_schema or self.cfg.schema))
            .option("dbtable", name)
            .load()
        )
        ordinal = next((c for c in df.columns if c.upper() == "__LINE_ORDINAL"), None)
        if ordinal:
            df = df.withColumnRenamed(ordinal, "__line_ordinal")
        return df

    def write(self, instance: str, df: DataFrame):
        (
            df.drop("__line_ordinal")
            if "__line_ordinal" in df.columns
            else df
        ).write.format("snowflake").options(
            **self._options(self.cfg.migrated_target_schema or self.cfg.schema)
        ).option(
            "dbtable", instance
        ).mode("overwrite").save()
