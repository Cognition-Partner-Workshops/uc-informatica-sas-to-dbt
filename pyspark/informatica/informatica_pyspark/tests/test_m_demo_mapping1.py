from datetime import date, datetime

from pyspark.sql import functions as F
from pyspark.sql.types import (
    DateType,
    LongType,
    StringType,
    StructField,
    StructType,
)

from informatica_pyspark.config import RunConfig, RunContext
from informatica_pyspark.mappings.m_demo_mapping1 import run


class StubIO:
    def __init__(self, frames):
        self.frames = frames

    def read(self, name):
        return self.frames[name]


def _context(spark, frames):
    return RunContext(RunConfig(business_date=date(2024, 1, 31)), spark, StubIO(frames))


def test_mapping1_reproduces_router_aggregation_sequence_and_lookups(spark):
    source3 = spark.createDataFrame(
        [
            (10, 1, "unused", "LAST1", datetime(2024, 1, 1), 5.0, 20),
            (11, 1, "unused", "LAST2", datetime(2024, 1, 2), 7.0, 20),
            (12, 2, "unused", "LAST3", datetime(2024, 1, 3), 3.0, 30),
            (13, 3, "unused", "LAST4", datetime(2024, 1, 4), 9.0, 30),
        ],
        ["TX_ID", "ACCT_ID", "FIRST_NM", "LAST_NM", "TX_DTTM", "TX_AMT", "CUST_ID"],
    ).withColumn("BAL_AMT", F.lit(100.0)).withColumn("TX_TYPE_CD", F.lit("DR"))
    source4 = spark.createDataFrame(
        [
            (1, "SB", " desc1 ", " 8000", date(2020, 1, 1), None, "A"),
            (2, "SB", " desc2 ", " 9000", date(2020, 1, 2), None, "A"),
            (3, "CA", " desc3 ", "1000", date(2020, 1, 3), None, "A"),
            (4, None, " desc4 ", "1000", date(2020, 1, 4), None, "A"),
        ],
        StructType(
            [
                StructField("ACCT_ID", LongType()),
                StructField("ACCT_TYP", StringType()),
                StructField("ACCT_DESC", StringType()),
                StructField("CRDT_LN", StringType()),
                StructField("CR8_DT", DateType()),
                StructField("CLSR_DT", DateType()),
                StructField("ACCT_STAT_CD", StringType()),
            ]
        ),
    )
    source5 = spark.createDataFrame(
        [("p", "product", "n", "red", "1", "2", "01/01/2020", "02/02/2024")],
        [
            "PRODUCT_ID",
            "PRODUCT_NM",
            "PRODUCT_NO",
            "COLOR",
            "STD_COST",
            "LIST_PRICE",
            "SELL_ST_DT",
            "SELL_ED_DT",
        ],
    )
    frames = {
        "demo_source3": source3,
        "demo_source4": source4,
        "demo_source5": source5,
        "lkp_demo_source1": spark.createDataFrame(
            [(1, "FIRST1"), (3, "FIRST3")], ["ACCT_ID", "FIRST_NM"]
        ).withColumn("__line_ordinal", F.monotonically_increasing_id()),
        "lkp_demo_source2": spark.createDataFrame(
            [(20, 200), (30, 300)], ["CUST_ID", "CRDT_SCORE"]
        ).withColumn("__line_ordinal", F.monotonically_increasing_id()),
        "lkp_demo_source3": spark.createDataFrame(
            [(1, "TYPE1"), (2, "TYPE2"), (3, "TYPE3")], ["ACCT_ID", "TX_TYPE_CD"]
        ).withColumn("__line_ordinal", F.monotonically_increasing_id()),
    }

    outputs = run(_context(spark, frames))
    target5 = outputs["demo_target5"].orderBy("ACCT_ID").collect()
    target6 = outputs["demo_target6"].orderBy("ACCT_ID").collect()

    assert [row.ACCT_ID for row in target5] == [3]
    assert target5[0].FIRST_NM == "FIRST3"
    assert target5[0].CRDT_SCORE == 300
    assert [row.ACCT_KEY for row in target6] == [281, 282]
    assert target6[0].TX_ID == 11
    assert target6[0].TX_AMT == 12.0
    assert [row.TX_TYPE_CD for row in target6] == ["TYPE1", "TYPE2"]
    assert all(row.CR8_DT == date(2024, 1, 31) for row in target6)


def test_mapping1_defect3_sell_start_date_is_null(spark):
    source5 = spark.createDataFrame(
        [("p", "product", "n", "red", "1", "2", "31/01/2024", "02/02/2024")],
        [
            "PRODUCT_ID",
            "PRODUCT_NM",
            "PRODUCT_NO",
            "COLOR",
            "STD_COST",
            "LIST_PRICE",
            "SELL_ST_DT",
            "SELL_ED_DT",
        ],
    )
    empty = spark.createDataFrame([], "id long")
    frames = {
            "demo_source3": spark.createDataFrame(
                [], "TX_ID long, ACCT_ID long, FIRST_NM string, LAST_NM string, "
                "TX_DTTM timestamp, TX_AMT double, TX_TYPE_CD string, "
                "BAL_AMT double, CUST_ID long"
            ),
        "demo_source4": spark.createDataFrame(
            [], "ACCT_ID long, ACCT_TYP string, ACCT_DESC string, CRDT_LN string, "
            "CR8_DT date, CLSR_DT date, ACCT_STAT_CD string"
        ),
        "demo_source5": source5,
        "lkp_demo_source1": empty.select(
            F.col("id").alias("ACCT_ID"), F.lit(None).cast("string").alias("FIRST_NM")
        ).withColumn("__line_ordinal", F.lit(0)),
        "lkp_demo_source2": empty.select(
            F.col("id").alias("CUST_ID"), F.lit(None).cast("long").alias("CRDT_SCORE")
        ).withColumn("__line_ordinal", F.lit(0)),
        "lkp_demo_source3": empty.select(
            F.col("id").alias("ACCT_ID"), F.lit(None).cast("string").alias("TX_TYPE_CD")
        ).withColumn("__line_ordinal", F.lit(0)),
    }

    row = run(_context(spark, frames))["demo_target3"].first()
    assert row.SELL_ST_DT is None
    assert row.SELL_ED_DT == date(2024, 2, 2)
