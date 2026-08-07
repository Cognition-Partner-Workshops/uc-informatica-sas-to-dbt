"""PySpark conversion of the Informatica demo mapping 1."""

from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F

from ..config import RunContext
from ..infa import infa_to_date, lookup, ltrim, rtrim, sequence_nextval

TARGETS = ["demo_target3", "demo_target5", "demo_target6"]


def run(ctx: RunContext) -> dict[str, DataFrame]:
    source3 = ctx.io.read("demo_source3")
    source4 = ctx.io.read("demo_source4")
    source5 = ctx.io.read("demo_source5")
    lkp_source1 = ctx.io.read("lkp_demo_source1")
    lkp_source2 = ctx.io.read("lkp_demo_source2")
    lkp_source3 = ctx.io.read("lkp_demo_source3")

    source3 = source3.alias("source3")
    source4 = source4.alias("source4")
    sq = source4.join(
        source3, F.col("source4.ACCT_ID") == F.col("source3.ACCT_ID"), "inner"
    ).select(
        F.col("source4.ACCT_ID").alias("ACCT_ID"),
        F.col("source4.ACCT_TYP").alias("ACCT_TYP"),
        F.col("source4.ACCT_DESC").alias("ACCT_DESC"),
        F.col("source4.CRDT_LN").alias("CRDT_LN"),
        # DEF-1: positional SYSTIMESTAMP lands in CR8_DT, not source4.CR8_DT.
        F.lit(ctx.cfg.business_date).cast("date").alias("CR8_DT"),
        F.col("source4.CLSR_DT").alias("CLSR_DT"),
        F.col("source4.ACCT_STAT_CD").alias("ACCT_STAT_CD"),
        F.col("source3.TX_ID").alias("TX_ID"),
        F.col("source3.LAST_NM").alias("LAST_NM"),
        F.col("source3.TX_DTTM").alias("TX_DTTM"),
        F.col("source3.TX_AMT").alias("TX_AMT"),
        F.col("source3.BAL_AMT").alias("BAL_AMT"),
        F.col("source3.CUST_ID").alias("CUST_ID"),
        # DEF-1b: positional STRCMP lands in an unconnected port; do not compute it.
    )

    first_name = lookup(lkp_source1, ["ACCT_ID"], policy="Use Last Value").select(
        "ACCT_ID", F.col("FIRST_NM").alias("lkp_FIRST_NM")
    )
    credit_score = lookup(
        lkp_source2, ["CUST_ID"], policy="Use Last Value"
    ).select("CUST_ID", F.col("CRDT_SCORE").alias("lkp_CRDT_SCORE"))
    transaction_type = lookup(
        lkp_source3, ["ACCT_ID"], policy="Use Last Value"
    ).select("ACCT_ID", F.col("TX_TYPE_CD").alias("lkp_TX_TYPE_CD"))

    joined = (
        sq.join(first_name, "ACCT_ID", "left")
        .join(credit_score, "CUST_ID", "left")
        .join(transaction_type, "ACCT_ID", "left")
        .withColumn("o_acc_trim", rtrim("ACCT_TYP"))
        .withColumn("o_crdt_trim", ltrim("CRDT_LN"))
        .withColumn("o_ACCT_DESC", rtrim("ACCT_DESC"))
    )

    # DEF-4: the unconnected router default drops NULL ACCT_TYP rows.
    target5_rows = joined.where(F.col("ACCT_TYP") != F.lit("SB"))
    target6_rows = joined.where(F.col("ACCT_TYP") == F.lit("SB"))

    target5 = target5_rows.select(
        "ACCT_ID",
        F.col("lkp_FIRST_NM").alias("FIRST_NM"),
        "LAST_NM",
        "BAL_AMT",
        F.col("lkp_CRDT_SCORE").alias("CRDT_SCORE"),
    )

    # DECISION-1: aggregator pass-through columns use the highest TX_ID row.
    account_window = Window.partitionBy("ACCT_ID")
    latest_window = account_window.orderBy(F.col("TX_ID").desc())
    aggregated = (
        target6_rows.withColumn("o_TX_AMT", F.sum("TX_AMT").over(account_window))
        .withColumn("__latest", F.row_number().over(latest_window))
        .where(F.col("__latest") == 1)
        .drop("__latest")
    )
    # DECISION-2: sequence values are consumed in ascending ACCT_ID order.
    aggregated = sequence_nextval(aggregated, ["ACCT_ID"], 281)
    target6 = aggregated.select(
        "ACCT_ID",
        F.col("o_acc_trim").alias("ACCT_TYP"),
        F.col("o_ACCT_DESC").alias("ACCT_DESC"),
        "CR8_DT",
        F.col("o_crdt_trim").alias("CRDT_LN"),
        "CLSR_DT",
        "ACCT_STAT_CD",
        "TX_ID",
        F.col("NEXTVAL").alias("ACCT_KEY"),
        "TX_DTTM",
        F.col("o_TX_AMT").alias("TX_AMT"),
        F.col("lkp_TX_TYPE_CD").alias("TX_TYPE_CD"),
    )

    # DEF-3: the session-default formatted date cannot match DD/MM/YYYY.
    session_date_text = F.date_format(
        F.lit(ctx.cfg.business_date), "MM/dd/yyyy HH:mm:ss.SSSSSS"
    )
    target3 = source5.select(
        "PRODUCT_ID",
        "PRODUCT_NM",
        "PRODUCT_NO",
        "COLOR",
        "STD_COST",
        "LIST_PRICE",
        infa_to_date(session_date_text, "DD/MM/YYYY").alias("SELL_ST_DT"),
        infa_to_date("SELL_ED_DT", "DD/MM/YYYY").alias("SELL_ED_DT"),
    )

    return {
        "demo_target3": target3,
        "demo_target5": target5,
        "demo_target6": target6,
    }
