from __future__ import annotations

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

from ..config import RunConfig
from ..functions import (
    inf_ltrim,
    inf_rtrim,
    inf_to_date_ddmmyyyy,
    lookup_use_last_value,
)
from ..io import InformaticaIO


TARGET_INSTANCES = ("demo_target6", "demo_target5", "demo_target3")


def _last_lookup(io: InformaticaIO, name: str, keys: list[str]) -> DataFrame:
    lookup = lookup_use_last_value(io.read_source(name), keys, "__ROW_ORD")
    return lookup.drop("__ROW_ORD")


def run(
    spark: SparkSession, cfg: RunConfig, io: InformaticaIO
) -> dict[str, DataFrame]:
    """Return the three m_demo_mapping1 target frames without writing them."""
    source3 = io.read_source("demo_source3").alias("source3")
    source4 = io.read_source("demo_source4").alias("source4")

    # The SQ override binds SYSTIMESTAMP positionally to CR8_DT.
    sq_accounts = (
        source4.join(
            source3,
            F.col("source4.ACCT_ID") == F.col("source3.ACCT_ID"),
            "inner",
        )
        .select(
            F.col("source4.ACCT_ID").alias("ACCT_ID"),
            F.col("source4.ACCT_TYP").alias("ACCT_TYP"),
            F.col("source4.ACCT_DESC").alias("ACCT_DESC"),
            F.col("source4.CRDT_LN").alias("CRDT_LN"),
            F.lit(cfg.business_date).cast("date").alias("CR8_DT"),
            F.col("source4.CLSR_DT").alias("CLSR_DT"),
            F.col("source4.ACCT_STAT_CD").alias("ACCT_STAT_CD"),
            F.col("source3.TX_ID").alias("TX_ID"),
            F.col("source3.LAST_NM").alias("LAST_NM"),
            F.col("source3.TX_DTTM").alias("TX_DTTM"),
            F.col("source3.TX_AMT").alias("TX_AMT"),
            F.col("source3.BAL_AMT").alias("BAL_AMT"),
            F.col("source3.CUST_ID").alias("CUST_ID"),
            F.col("source3.__ROW_ORD").alias("__ROW_ORD"),
        )
    )

    lkp_trans1 = _last_lookup(io, "lkp_demo_source3", ["ACCT_ID"]).select(
        F.col("ACCT_ID").alias("lkp1_ACCT_ID"),
        F.col("TX_TYPE_CD").alias("lkp_TX_TYPE_CD"),
    )
    exp_trans = (
        sq_accounts.join(
            lkp_trans1,
            sq_accounts.ACCT_ID == lkp_trans1.lkp1_ACCT_ID,
            "left",
        )
        .select(
            sq_accounts["*"],
            F.col("lkp_TX_TYPE_CD").alias("o_ACCT_ID"),
            inf_rtrim("ACCT_TYP").alias("o_acc_trim"),
            inf_ltrim("CRDT_LN").alias("o_crdt_trim"),
        )
    )

    lkp_trans2 = _last_lookup(io, "lkp_demo_source1", ["ACCT_ID"]).select(
        F.col("ACCT_ID").alias("lkp2_ACCT_ID"),
        F.col("FIRST_NM").alias("lkp_FIRST_NM"),
    )
    lkp_trans3 = _last_lookup(io, "lkp_demo_source2", ["CUST_ID"]).select(
        F.col("CUST_ID").alias("lkp3_CUST_ID"),
        F.col("CRDT_SCORE").alias("lkp_CRDT_SCORE"),
    )
    exp_trans1 = (
        exp_trans.join(
            lkp_trans2,
            exp_trans.ACCT_ID == lkp_trans2.lkp2_ACCT_ID,
            "left",
        )
        .join(
            lkp_trans3,
            exp_trans.CUST_ID == lkp_trans3.lkp3_CUST_ID,
            "left",
        )
        .select(
            exp_trans["*"],
            F.col("lkp_FIRST_NM").alias("FIRST_NM"),
            F.col("lkp_CRDT_SCORE").alias("CRDT_SCORE"),
            inf_rtrim("ACCT_DESC").alias("o_ACCT_DESC"),
        )
    )

    # Router conditions use the untrimmed ACCT_TYP pass-through.
    target6_group = exp_trans1.where(F.col("ACCT_TYP") == F.lit("SB"))
    target5_group = exp_trans1.where(F.col("ACCT_TYP") != F.lit("SB"))

    # The XML leaves pass-through selection within a group undefined.  Use
    # the highest TX_ID consistently for the recovered legacy decision.
    target6_agg = (
        target6_group.groupBy("ACCT_ID")
        .agg(
            F.max_by("o_ACCT_DESC", "TX_ID").alias("o_ACCT_DESC"),
            F.sum("TX_AMT").alias("o_TX_AMT"),
            F.max_by("o_crdt_trim", "TX_ID").alias("o_crdt_trim"),
            F.max_by("CLSR_DT", "TX_ID").alias("CLSR_DT"),
            F.max_by("TX_ID", "TX_ID").alias("TX_ID"),
            F.max_by("ACCT_STAT_CD", "TX_ID").alias("ACCT_STAT_CD"),
            F.max_by("TX_DTTM", "TX_ID").alias("TX_DTTM"),
            F.max_by("CR8_DT", "TX_ID").alias("CR8_DT"),
            F.max_by("o_ACCT_ID", "TX_ID").alias("o_ACCT_ID"),
            F.max_by("o_acc_trim", "TX_ID").alias("o_acc_trim"),
        )
        .withColumn(
            "ACCT_KEY",
            F.lit(280)
            + F.row_number().over(Window.orderBy(F.col("ACCT_ID"))),
        )
    )
    demo_target6 = target6_agg.select(
        "ACCT_ID",
        "o_acc_trim",
        "o_ACCT_DESC",
        "CR8_DT",
        "o_crdt_trim",
        "CLSR_DT",
        "ACCT_STAT_CD",
        "TX_ID",
        "ACCT_KEY",
        "TX_DTTM",
        "o_TX_AMT",
        "o_ACCT_ID",
    ).toDF(
        "ACCT_ID",
        "ACCT_TYP",
        "ACCT_DESC",
        "CR8_DT",
        "CRDT_LN",
        "CLSR_DT",
        "ACCT_STAT_CD",
        "TX_ID",
        "ACCT_KEY",
        "TX_DTTM",
        "TX_AMT",
        "TX_TYPE_CD",
    )

    demo_target5 = target5_group.select(
        "ACCT_ID",
        "FIRST_NM",
        "LAST_NM",
        "BAL_AMT",
        "CRDT_SCORE",
    )

    source5 = io.read_source("demo_source5")
    exp_trans2 = source5.select(
        "PRODUCT_ID",
        "PRODUCT_NM",
        "PRODUCT_NO",
        "COLOR",
        "STD_COST",
        "LIST_PRICE",
        # The legacy default TO_CHAR mask is incompatible with DD/MM/YYYY.
        inf_to_date_ddmmyyyy(
            F.date_format(
                F.lit(cfg.business_date).cast("timestamp"),
                "MM/dd/yyyy HH:mm:ss.SSSSSS",
            )
        ).alias("o_SELL_ST_DT"),
        inf_to_date_ddmmyyyy("SELL_ED_DT").alias("o_SELL_ED_DT"),
    )
    demo_target3 = exp_trans2.select(
        "PRODUCT_ID",
        "PRODUCT_NM",
        "PRODUCT_NO",
        "COLOR",
        "STD_COST",
        "LIST_PRICE",
        "o_SELL_ST_DT",
        "o_SELL_ED_DT",
    ).toDF(
        "PRODUCT_ID",
        "PRODUCT_NM",
        "PRODUCT_NO",
        "COLOR",
        "STD_COST",
        "LIST_PRICE",
        "SELL_ST_DT",
        "SELL_ED_DT",
    )

    return {
        "demo_target6": demo_target6,
        "demo_target5": demo_target5,
        "demo_target3": demo_target3,
    }
