from __future__ import annotations

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from ..config import RunConfig
from ..functions import assert_no_abort
from ..io import InformaticaIO


TARGET_INSTANCES = ("demo_target2", "demo_target21")
TARGET_COLUMNS = (
    "Title",
    "Gender",
    "First_Name",
    "Middle_Name",
    "Last_Name",
    "Member_Identifier",
    "Member_Suffix",
    "Date_of_Birth",
    "Member_Number",
    "Soc_Number",
    "Type_Code",
    "Relationship_to_Subscriber_Code",
    "Relationship_to_Subscriber_Code_Label",
    "Effective_Date",
)
NUMERIC_TARGET_COLUMNS = (
    "Member_Identifier",
    "Member_Number",
    "Soc_Number",
    "Type_Code",
    "Relationship_to_Subscriber_Code",
)


def _target_projection(frame: DataFrame) -> DataFrame:
    renamed = (
        frame.withColumnRenamed("Member_ID", "Member_Identifier")
        .withColumnRenamed("Birth_Date", "Date_of_Birth")
        .withColumnRenamed("Gender_Code", "Gender")
        .withColumnRenamed("Member_Record_Number", "Member_Number")
        .withColumnRenamed("Social_Security_Number", "Soc_Number")
        .withColumnRenamed("Member_Type_Code", "Type_Code")
        .withColumnRenamed("Original_Effective_Date", "Effective_Date")
    )
    for column in NUMERIC_TARGET_COLUMNS:
        renamed = renamed.withColumn(column, F.col(column).cast("double"))
    return renamed.select(*TARGET_COLUMNS)


def run(
    spark: SparkSession, cfg: RunConfig, io: InformaticaIO
) -> dict[str, DataFrame]:
    source = io.read_source("demo_source2")
    filtered = source.where(F.col("Member_Type_Code").isNotNull())
    assert_no_abort(
        filtered,
        F.col("Relationship_to_Subscriber_Code_Label").isNull(),
        "Relationship_to_Subscriber_Code_Labe valuel is null",
    )

    projected = _target_projection(filtered)
    return {
        "demo_target2": projected.where(F.col("Soc_Number").isNull()),
        "demo_target21": projected.where(F.col("Soc_Number").isNotNull()),
    }
