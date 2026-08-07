import datetime as dt

from pyspark.sql import functions as F
from pyspark.sql.types import StringType, StructField, StructType

from informatica_pyspark.functions import (
    inf_concat,
    inf_iif,
    inf_ltrim,
    inf_rtrim,
    inf_to_date_ddmmyyyy,
    lookup_use_any_value,
    lookup_use_last_value,
)


def test_null_semantics(spark):
    row = spark.createDataFrame(
        [(None, "  x  ", None)],
        StructType(
            [
                StructField("null_value", StringType()),
                StructField("text", StringType()),
                StructField("condition", StringType()),
            ]
        ),
    )
    result = row.select(
        inf_iif(F.lit(False), F.lit("yes")).alias("iif"),
        inf_concat(F.col("null_value"), F.lit("x")).alias("concat"),
        inf_rtrim(F.col("text")).alias("rtrim"),
        inf_ltrim(F.col("text")).alias("ltrim"),
    ).first()
    assert result.iif is None
    assert result.concat == "x"
    assert result.rtrim == "  x"
    assert result.ltrim == "x  "


def test_lookup_collapse_policies(spark):
    lookup = spark.createDataFrame(
        [(1, 2, "low"), (1, 99, "high"), (2, 3, "other")],
        ["id", "Key", "value"],
    ).withColumn("__ROW_ORD", F.monotonically_increasing_id())
    last = lookup_use_last_value(lookup, ["id"], "__ROW_ORD")
    any_value = lookup_use_any_value(lookup, ["id"], "__ROW_ORD")
    assert last.where("id = 1").select("value").first().value == "high"
    assert any_value.where("id = 1").select("value").first().value == "high"


def test_to_date_unparseable_is_null(spark):
    frame = spark.createDataFrame([("31/02/2024",), ("31/01/2024",)], ["value"])
    values = [
        row.value
        for row in frame.select(inf_to_date_ddmmyyyy("value").alias("value")).collect()
    ]
    assert values == [None, dt.date(2024, 1, 31)]
