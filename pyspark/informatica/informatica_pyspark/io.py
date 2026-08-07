from __future__ import annotations

import glob
import os
import shutil
import tempfile
from pathlib import Path
from typing import Protocol

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import (
    DateType,
    DoubleType,
    LongType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)

from .config import REPO_ROOT, RunConfig


def _schema(*fields: tuple[str, object]) -> StructType:
    return StructType([StructField(name, data_type, True) for name, data_type in fields])


SOURCE_SCHEMAS = {
    "demo_source1": _schema(
        ("LEAD_CO_MNE", StringType()),
        ("BRANCH_CO_MNE", StringType()),
        ("MIS_DATE", StringType()),
        ("ID", StringType()),
        ("DESCRIPTION", StringType()),
        ("SHORT_NAME", StringType()),
    ),
    "demo_source2": _schema(
        ("Title", StringType()),
        ("First_Name", StringType()),
        ("Middle_Name", StringType()),
        ("Last_Name", StringType()),
        ("Member_ID", LongType()),
        ("Member_Suffix", StringType()),
        ("Birth_Date", DateType()),
        ("Gender_Code", StringType()),
        ("Member_Record_Number", LongType()),
        ("Social_Security_Number", LongType()),
        ("Member_Type_Code", LongType()),
        ("Original_Effective_Date", DateType()),
        ("Relationship_to_Subscriber_Code", LongType()),
        ("Relationship_to_Subscriber_Code_Label", StringType()),
    ),
    "demo_source3": _schema(
        ("TX_ID", LongType()),
        ("ACCT_ID", LongType()),
        ("FIRST_NM", StringType()),
        ("LAST_NM", StringType()),
        ("TX_DTTM", TimestampType()),
        ("TX_AMT", DoubleType()),
        ("TX_TYPE_CD", StringType()),
        ("BAL_AMT", DoubleType()),
        ("TX_DESC", StringType()),
        ("CRDT_SCORE", LongType()),
        ("CUST_ID", LongType()),
    ),
    "demo_source4": _schema(
        ("ACCT_ID", LongType()),
        ("ACCT_TYP", StringType()),
        ("ACCT_DESC", StringType()),
        ("CRDT_LN", StringType()),
        ("CR8_DT", DateType()),
        ("CLSR_DT", DateType()),
        ("ACCT_STAT_CD", StringType()),
    ),
    "demo_source5": _schema(
        ("PRODUCT_ID", StringType()),
        ("PRODUCT_NM", StringType()),
        ("PRODUCT_NO", StringType()),
        ("COLOR", StringType()),
        ("STD_COST", StringType()),
        ("LIST_PRICE", StringType()),
        ("SELL_ST_DT", StringType()),
        ("SELL_ED_DT", StringType()),
    ),
    "lkp_demo_source1": _schema(
        ("ACCT_ID", LongType()),
        ("CUST_ID", LongType()),
        ("FIRST_NM", StringType()),
        ("LAST_NM", StringType()),
        ("CUST_ADDR", StringType()),
        ("CUST_PHN", StringType()),
        ("CUST_EML_ADDR", StringType()),
        ("AGE", LongType()),
        ("DOB", DateType()),
        ("CUST_TYP", StringType()),
    ),
    "lkp_demo_source2": _schema(
        ("CUST_ID", LongType()),
        ("CRDT_SCORE", LongType()),
        ("MAX_CRDT_SCORE", LongType()),
        ("MIN_CRDT_SCORE", LongType()),
        ("MAX_CRDT_LMT", LongType()),
        ("CURR_CRDT_BAL_AMT", DoubleType()),
        ("AVG_INC_AMT", DoubleType()),
    ),
    "lkp_demo_source3": _schema(
        ("ACCT_ID", LongType()),
        ("TX_TYPE_CD", StringType()),
        ("TX_TYPE_DESC", StringType()),
    ),
}

TARGET_SCHEMAS = {
    "demo_target1": _schema(
        ("Key", LongType()),
        ("LEAD_CO_MNE", StringType()),
        ("BRANCH_CO_MNE", StringType()),
        ("MIS_DATE", StringType()),
        ("ID", StringType()),
        ("DESCRIPTION", StringType()),
        ("SHORT_NAME", StringType()),
        ("CREATED_BY", StringType()),
        ("CREATED_TIME", TimestampType()),
        ("UPDATED_BY", StringType()),
        ("UPDATED_TIME", TimestampType()),
        ("ACTIVE_FLAG", StringType()),
        ("START_DATE", TimestampType()),
        ("END_DATE", TimestampType()),
    ),
}


class InformaticaIO(Protocol):
    def read_source(self, name: str) -> DataFrame: ...

    def write_target(self, instance: str, df: DataFrame) -> None: ...


class LocalCsvIO:
    def __init__(self, spark: SparkSession, cfg: RunConfig):
        self.spark = spark
        self.cfg = cfg
        self.base_dir = REPO_ROOT / "legacy" / "informatica" / "data"

    def read_source(self, name: str) -> DataFrame:
        if name not in SOURCE_SCHEMAS and name not in TARGET_SCHEMAS:
            raise KeyError(f"Unknown Informatica source: {name}")
        schema = (
            SOURCE_SCHEMAS[name] if name in SOURCE_SCHEMAS else TARGET_SCHEMAS[name]
        )
        override = self.cfg.data_dir / f"{name}.csv"
        fallback = self.base_dir / f"{name}.csv"
        path = override if override.exists() else fallback
        return (
            self.spark.read.option("header", True)
            .schema(schema)
            .csv(str(path))
            .coalesce(1)
            .withColumn("__ROW_ORD", F.monotonically_increasing_id())
        )

    def write_target(self, instance: str, df: DataFrame) -> None:
        self.cfg.out_dir.mkdir(parents=True, exist_ok=True)
        temp_dir = Path(tempfile.mkdtemp(prefix=f".{instance}.", dir=self.cfg.out_dir))
        try:
            output_df = df.drop("__ROW_ORD") if "__ROW_ORD" in df.columns else df
            (
                output_df.coalesce(1)
                .write.mode("overwrite")
                .option("header", True)
                .option("dateFormat", "yyyy-MM-dd")
                .option("timestampFormat", "yyyy-MM-dd HH:mm:ss")
                .csv(str(temp_dir))
            )
            part_files = glob.glob(str(temp_dir / "part-*.csv"))
            if len(part_files) != 1:
                raise RuntimeError(f"Expected one output part for {instance}")
            os.replace(part_files[0], self.cfg.out_dir / f"{instance}.csv")
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


class SnowflakeIO:
    def __init__(self, spark: SparkSession, cfg: RunConfig):
        self.spark = spark
        self.cfg = cfg

    def _options(self) -> dict[str, str]:
        required = {
            "account": self.cfg.snowflake_account,
            "user": self.cfg.snowflake_user,
            "warehouse": self.cfg.snowflake_warehouse,
            "database": self.cfg.snowflake_database,
            "src_schema": self.cfg.snowflake_src_schema,
            "run_schema": self.cfg.snowflake_run_schema,
            "SNOWFLAKE_PRIVATE_KEY": self.cfg.snowflake_private_key,
        }
        missing = [name for name, value in required.items() if not value]
        if missing:
            raise ValueError(
                "Missing Snowflake setting(s): " + ", ".join(missing)
            )
        options = {
            "sfAccount": self.cfg.snowflake_account,
            "sfUser": self.cfg.snowflake_user,
            "sfWarehouse": self.cfg.snowflake_warehouse,
            "sfDatabase": self.cfg.snowflake_database,
            "sfSchema": self.cfg.snowflake_src_schema,
            "pem_private_key": self.cfg.snowflake_private_key,
        }
        if self.cfg.snowflake_role:
            options["sfRole"] = self.cfg.snowflake_role
        return options

    def read_source(self, name: str) -> DataFrame:
        if name not in SOURCE_SCHEMAS and name not in TARGET_SCHEMAS:
            raise KeyError(f"Unknown Informatica source: {name}")
        options = self._options()
        options["dbtable"] = f"{self.cfg.snowflake_src_schema}.{name}"
        return (
            self.spark.read.format("net.snowflake.spark.snowflake")
            .options(**options)
            .load()
        )

    def write_target(self, instance: str, df: DataFrame) -> None:
        options = self._options()
        options["sfSchema"] = self.cfg.snowflake_run_schema
        options["dbtable"] = f"{self.cfg.snowflake_run_schema}.{instance}"
        output_df = df.drop("__ROW_ORD") if "__ROW_ORD" in df.columns else df
        output_df.write.format("net.snowflake.spark.snowflake").options(
            **options
        ).mode("overwrite").save()
