"""PySpark conversion of Informatica mapping m_demo_mapping1."""

from pyspark.sql import Window, functions as F

from .. import functions
from ..context import MappingContext, MappingResult
from ..io.base import ORDINAL_COL

MAPPING_NAME = "m_demo_mapping1"
SOURCES = ("demo_source3", "demo_source4", "demo_source5",
           "lkp_demo_source1", "lkp_demo_source2", "lkp_demo_source3")
TARGET_INSTANCES = ("demo_target3", "demo_target5", "demo_target6")


def run(ctx: MappingContext) -> MappingResult:
    source3 = ctx.sources["demo_source3"].select(
        F.col("TX_ID").cast("long").alias("TX_ID"),
        F.col("ACCT_ID").cast("long").alias("ACCT_ID"),
        F.col("LAST_NM"),
        F.col("TX_DTTM").cast("timestamp").alias("TX_DTTM"),
        F.col("TX_AMT").cast("double").alias("TX_AMT"),
        F.col("BAL_AMT").cast("double").alias("BAL_AMT"),
        F.col("CUST_ID").cast("long").alias("CUST_ID"),
        F.col("TX_TYPE_CD").alias("SRC_TX_TYPE_CD"),
    ).alias("source3")
    source4 = ctx.sources["demo_source4"].select(
        F.col("ACCT_ID").cast("long").alias("ACCT_ID"),
        F.col("ACCT_TYP"),
        F.col("ACCT_DESC"),
        F.col("CRDT_LN"),
        F.col("CLSR_DT").cast("date").alias("CLSR_DT"),
        F.col("ACCT_STAT_CD"),
    ).alias("source4")

    # RECOVERED: the SQL override binds SELECT expressions positionally to SQ ports.
    # CR8_DT therefore receives SYSTIMESTAMP, while the unconnected TX_TYPE_CD
    # receives a computed STRCMP result and is deliberately discarded.
    joined = source3.join(source4, F.col("source3.ACCT_ID") == F.col("source4.ACCT_ID"),
                          "inner").select(
        F.col("source4.ACCT_ID").alias("ACCT_ID"),
        F.col("source4.ACCT_TYP"),
        F.col("source4.ACCT_DESC"),
        F.col("source4.CRDT_LN"),
        ctx.systimestamp.cast("date").alias("CR8_DT"),
        F.col("source4.CLSR_DT"),
        F.col("source4.ACCT_STAT_CD"),
        F.col("source3.TX_ID"),
        F.col("source3.LAST_NM"),
        F.col("source3.TX_DTTM"),
        F.col("source3.TX_AMT"),
        F.col("source3.BAL_AMT"),
        F.col("source3.CUST_ID"),
        functions.strcmp(
            F.col("source4.ACCT_STAT_CD"), F.col("source3.SRC_TX_TYPE_CD")
        ).alias("WRK_SQL_TX_TYPE_CD"),
    )

    exp_trans = joined.select(
        "*",
        functions.rtrim(F.col("ACCT_TYP")).alias("WRK_O_ACC_TRIM"),
        functions.ltrim(F.col("CRDT_LN")).alias("WRK_O_CRDT_TRIM"),
    )

    lookup1 = functions.last_value(
        ctx.sources["lkp_demo_source1"],
        "ACCT_ID",
    ).select("ACCT_ID", "FIRST_NM").alias("lookup1")
    lookup2 = functions.last_value(
        ctx.sources["lkp_demo_source2"],
        "CUST_ID",
    ).select("CUST_ID", "CRDT_SCORE").alias("lookup2")
    lookup3 = functions.last_value(
        ctx.sources["lkp_demo_source3"],
        "ACCT_ID",
    ).select("ACCT_ID", "TX_TYPE_CD").alias("lookup3")

    enriched = (
        exp_trans.alias("exp")
        .join(lookup1, F.col("exp.ACCT_ID") == F.col("lookup1.ACCT_ID"), "left")
        .join(lookup2, F.col("exp.CUST_ID") == F.col("lookup2.CUST_ID"), "left")
        .join(lookup3, F.col("exp.ACCT_ID") == F.col("lookup3.ACCT_ID"), "left")
        .select(
            F.col("exp.*"),
            F.col("lookup1.FIRST_NM").alias("FIRST_NM"),
            F.col("lookup2.CRDT_SCORE").cast("long").alias("CRDT_SCORE"),
            F.col("lookup3.TX_TYPE_CD").alias("WRK_O_ACCT_ID"),
        )
        .withColumn("WRK_O_ACCT_DESC", functions.rtrim(F.col("ACCT_DESC")))
    )

    # RECOVERED: router conditions use the untrimmed ACCT_TYP pass-through.
    target5 = enriched.where(F.col("ACCT_TYP") != F.lit("SB")).select(
        "ACCT_ID", "FIRST_NM", "LAST_NM", "BAL_AMT", "CRDT_SCORE",
    )

    sb = enriched.where(F.col("ACCT_TYP") == F.lit("SB"))
    sb_window = Window.partitionBy("ACCT_ID").orderBy(F.col("TX_ID").desc())
    sb = (
        sb.withColumn("WRK_AGG_ROW", F.row_number().over(sb_window))
        .withColumn("WRK_SUM_TX_AMT", F.sum("TX_AMT").over(
            Window.partitionBy("ACCT_ID")
        ))
        .where(F.col("WRK_AGG_ROW") == 1)
    )
    # RECOVERED: sq_demo_source4 has one sorted port, ACCT_ID, so the
    # sequence consumes rows in the Source Qualifier sorted-port order.
    sequence_window = Window.orderBy(F.col("ACCT_ID"))
    target6 = sb.select(
        "ACCT_ID",
        F.col("WRK_O_ACC_TRIM").alias("ACCT_TYP"),
        F.col("WRK_O_ACCT_DESC").alias("ACCT_DESC"),
        "CR8_DT",
        F.col("WRK_O_CRDT_TRIM").alias("CRDT_LN"),
        "CLSR_DT",
        "ACCT_STAT_CD",
        "TX_ID",
        (F.lit(280) + F.row_number().over(sequence_window)).cast("long").alias("ACCT_KEY"),
        "TX_DTTM",
        F.col("WRK_SUM_TX_AMT").alias("TX_AMT"),
        F.col("WRK_O_ACCT_ID").alias("TX_TYPE_CD"),
    )

    source5 = ctx.sources["demo_source5"]
    target3 = source5.select(
        "PRODUCT_ID", "PRODUCT_NM", "PRODUCT_NO", "COLOR", "STD_COST", "LIST_PRICE",
        # RECOVERED: evaluate both shared primitives; this intentionally parses
        # the default TO_CHAR mask with the incompatible DD/MM/YYYY mask.
        functions.to_date(
            functions.to_char(ctx.sysdate), "DD/MM/YYYY"
        ).alias("SELL_ST_DT"),
        functions.to_date(F.col("SELL_ED_DT"), "DD/MM/YYYY").alias("SELL_ED_DT"),
    )

    return MappingResult(
        targets={
            "demo_target3": target3,
            "demo_target5": target5,
            "demo_target6": target6,
        },
        sort_keys={
            "demo_target3": ("PRODUCT_ID",),
            "demo_target5": ("ACCT_ID",),
            "demo_target6": ("ACCT_ID",),
        },
    )
