from __future__ import annotations

import glob
import base64
import os
import shutil
import tempfile
from pathlib import Path
from typing import Protocol

import snowflake.connector
from cryptography.hazmat.primitives import serialization
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import (
    DateType,
    DoubleType,
    IntegerType,
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

TARGET_INSTANCE_SCHEMAS: dict[str, StructType] = {
    "demo_target1_INS": _schema(
        ("Key", LongType()),
        ("LEAD_CO_MNE", StringType()),
        ("BRANCH_CO_MNE", StringType()),
        ("MIS_DATE", StringType()),
        ("ID", StringType()),
        ("DESCRIPTION", StringType()),
        ("SHORT_NAME", StringType()),
        ("CREATED_BY", StringType()),
        ("CREATED_TIME", DateType()),
        ("UPDATED_BY", StringType()),
        ("UPDATED_TIME", DateType()),
        ("ACTIVE_FLAG", StringType()),
        ("START_DATE", DateType()),
        ("END_DATE", DateType()),
    ),
    "demo_target1_UPD": _schema(
        ("Key", DoubleType()),
        ("LEAD_CO_MNE", StringType()),
        ("BRANCH_CO_MNE", StringType()),
        ("MIS_DATE", StringType()),
        ("ID", StringType()),
        ("DESCRIPTION", StringType()),
        ("SHORT_NAME", StringType()),
        ("CREATED_BY", StringType()),
        ("CREATED_TIME", DateType()),
        ("UPDATED_BY", StringType()),
        ("UPDATED_TIME", DateType()),
        ("ACTIVE_FLAG", StringType()),
        ("START_DATE", DateType()),
        ("END_DATE", DateType()),
    ),
    "demo_target2": _schema(
        ("Title", StringType()),
        ("Gender", StringType()),
        ("First_Name", StringType()),
        ("Middle_Name", StringType()),
        ("Last_Name", StringType()),
        ("Member_Identifier", DoubleType()),
        ("Member_Suffix", StringType()),
        ("Date_of_Birth", DateType()),
        ("Member_Number", DoubleType()),
        ("Soc_Number", DoubleType()),
        ("Type_Code", DoubleType()),
        ("Relationship_to_Subscriber_Code", DoubleType()),
        ("Relationship_to_Subscriber_Code_Label", StringType()),
        ("Effective_Date", DateType()),
    ),
    "demo_target21": _schema(
        ("Title", StringType()),
        ("Gender", StringType()),
        ("First_Name", StringType()),
        ("Middle_Name", StringType()),
        ("Last_Name", StringType()),
        ("Member_Identifier", DoubleType()),
        ("Member_Suffix", StringType()),
        ("Date_of_Birth", DateType()),
        ("Member_Number", DoubleType()),
        ("Soc_Number", DoubleType()),
        ("Type_Code", DoubleType()),
        ("Relationship_to_Subscriber_Code", DoubleType()),
        ("Relationship_to_Subscriber_Code_Label", StringType()),
        ("Effective_Date", DateType()),
    ),
    "demo_target3": _schema(
        ("PRODUCT_ID", StringType()),
        ("PRODUCT_NM", StringType()),
        ("PRODUCT_NO", StringType()),
        ("COLOR", StringType()),
        ("STD_COST", StringType()),
        ("LIST_PRICE", StringType()),
        ("SELL_ST_DT", DateType()),
        ("SELL_ED_DT", DateType()),
    ),
    "demo_target5": _schema(
        ("ACCT_ID", LongType()),
        ("FIRST_NM", StringType()),
        ("LAST_NM", StringType()),
        ("BAL_AMT", DoubleType()),
        ("CRDT_SCORE", LongType()),
    ),
    "demo_target6": _schema(
        ("ACCT_ID", LongType()),
        ("ACCT_TYP", StringType()),
        ("ACCT_DESC", StringType()),
        ("CR8_DT", DateType()),
        ("CRDT_LN", StringType()),
        ("CLSR_DT", DateType()),
        ("ACCT_STAT_CD", StringType()),
        ("TX_ID", LongType()),
        ("ACCT_KEY", IntegerType()),
        ("TX_DTTM", TimestampType()),
        ("TX_AMT", DoubleType()),
        ("TX_TYPE_CD", StringType()),
    ),
}


def _same_data_schema(actual: StructType, expected: StructType) -> bool:
    return [
        (field.name, field.dataType)
        for field in actual.fields
    ] == [
        (field.name, field.dataType)
        for field in expected.fields
    ]


def _validate_target_schema(instance: str, df: DataFrame) -> None:
    expected = TARGET_INSTANCE_SCHEMAS.get(instance)
    if expected is not None and not _same_data_schema(df.schema, expected):
        raise TypeError(
            f"{instance} schema mismatch: expected {expected.simpleString()}, "
            f"got {df.schema.simpleString()}"
        )


def _private_key_der() -> bytes:
    raw = os.environ.get("SNOWFLAKE_PRIVATE_KEY")
    if not raw:
        raise ValueError("Missing Snowflake setting(s): SNOWFLAKE_PRIVATE_KEY")
    raw = raw.replace("\\n", "\n")
    key = serialization.load_pem_private_key(raw.encode("utf-8"), password=None)
    return key.private_bytes(
        serialization.Encoding.DER,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )


def snowflake_connection(cfg: RunConfig):
    return snowflake.connector.connect(
        account=cfg.snowflake_account,
        user=cfg.snowflake_user,
        private_key=_private_key_der(),
        role=cfg.snowflake_role,
        warehouse=cfg.snowflake_warehouse,
        database=cfg.snowflake_database,
    )


def snowflake_type(data_type: object) -> str:
    if isinstance(data_type, LongType):
        return "NUMBER(38,0)"
    if isinstance(data_type, IntegerType):
        return "NUMBER(38,0)"
    if isinstance(data_type, DoubleType):
        return "FLOAT"
    if isinstance(data_type, StringType):
        return "VARCHAR"
    if isinstance(data_type, DateType):
        return "DATE"
    if isinstance(data_type, TimestampType):
        return "TIMESTAMP_NTZ"
    raise TypeError(f"Unsupported Spark type: {data_type}")


def create_target_table(connection, database: str, schema: str, instance: str) -> None:
    expected = TARGET_INSTANCE_SCHEMAS[instance]
    columns = ", ".join(
        f"{field.name.upper()} {snowflake_type(field.dataType)}"
        for field in expected.fields
    )
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {database}.{schema}")
        cursor.execute(
            f"CREATE OR REPLACE TABLE {database}.{schema}.{instance.upper()} "
            f"({columns})"
        )
    finally:
        cursor.close()


class InformaticaIO(Protocol):
    def read_source(self, name: str) -> DataFrame: ...

    def write_target(self, instance: str, df: DataFrame) -> None: ...


def build_io(spark: SparkSession, cfg: RunConfig) -> InformaticaIO:
    return LocalCsvIO(spark, cfg) if cfg.io_mode == "local" else SnowflakeIO(spark, cfg)


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
        _validate_target_schema(instance, df)
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
            "sfURL": f"{self.cfg.snowflake_account}.snowflakecomputing.com",
            "sfUser": self.cfg.snowflake_user,
            "sfWarehouse": self.cfg.snowflake_warehouse,
            "sfDatabase": self.cfg.snowflake_database,
            "sfSchema": self.cfg.snowflake_src_schema,
            "pem_private_key": base64.b64encode(_private_key_der()).decode("ascii"),
            "sfTimezone": "UTC",
        }
        if self.cfg.snowflake_role:
            options["sfRole"] = self.cfg.snowflake_role
        return options

    def read_source(self, name: str) -> DataFrame:
        if name not in SOURCE_SCHEMAS and name not in TARGET_SCHEMAS:
            raise KeyError(f"Unknown Informatica source: {name}")
        options = self._options()
        options["dbtable"] = f"{self.cfg.snowflake_src_schema}.{name}"
        schema = SOURCE_SCHEMAS.get(name, TARGET_SCHEMAS.get(name))
        frame = (
            self.spark.read.format("net.snowflake.spark.snowflake")
            .options(**options)
            .load()
        )
        columns = [
            F.col(field.name.upper()).cast(field.dataType).alias(field.name)
            for field in schema.fields
        ]
        columns.append(
            F.coalesce(F.col("__ROW_ORD"), F.lit(0))
            .cast(LongType())
            .alias("__ROW_ORD")
        )
        projected = frame.select(*columns)
        exact_schema = StructType(
            [*schema.fields, StructField("__ROW_ORD", LongType(), False)]
        )
        return self.spark.createDataFrame(projected.rdd, exact_schema)

    def write_target(self, instance: str, df: DataFrame) -> None:
        _validate_target_schema(instance, df)
        options = self._options()
        options["sfSchema"] = self.cfg.snowflake_run_schema
        options["dbtable"] = f"{self.cfg.snowflake_run_schema}.{instance.upper()}"
        connection = snowflake_connection(self.cfg)
        try:
            create_target_table(
                connection,
                self.cfg.snowflake_database,
                self.cfg.snowflake_run_schema,
                instance,
            )
        finally:
            connection.close()
        output_df = df.drop("__ROW_ORD") if "__ROW_ORD" in df.columns else df
        output_df = output_df.toDF(*(column.upper() for column in output_df.columns))
        output_df.write.format("net.snowflake.spark.snowflake").options(
            **options
        ).mode("append").save()
