"""PySpark implementation of the m_demo_mapping2 mapping."""

from pyspark.sql import Window, functions as F

from ..context import MappingContext, MappingResult
from ..functions import aes_decrypt, concat, iif, isnull, md5, not_, substr
from ..io.base import ORDINAL_COL

MAPPING_NAME = "m_demo_mapping2"
SOURCES = ("demo_source1", "demo_target1")
TARGET_INSTANCES = ("demo_target1_INS", "demo_target1_UPD")


def run(ctx: MappingContext) -> MappingResult:
    source = ctx.sources["demo_source1"].alias("source")
    lookup_window = Window.partitionBy("ID").orderBy(F.col(ORDINAL_COL).desc())
    lookup = (
        ctx.sources["demo_target1"]
        .withColumn("Key", F.col("Key").cast("double"))
        .withColumn("_lookup_rank", F.row_number().over(lookup_window))
        .where(F.col("_lookup_rank") == 1)
        .drop("_lookup_rank")
        .alias("lookup")
    )
    joined = source.join(
        lookup,
        F.col("source.ID") == F.col("lookup.ID"),
        "left",
    )

    transformed = joined.select(
        F.col("source.LEAD_CO_MNE").alias("LEAD_CO_MNE"),
        F.col("source.BRANCH_CO_MNE").alias("BRANCH_CO_MNE"),
        F.col("source.MIS_DATE").alias("MIS_DATE"),
        F.col("source.ID").alias("ID"),
        F.col("source.DESCRIPTION").alias("DESCRIPTION"),
        F.col("source.SHORT_NAME").alias("SHORT_NAME"),
        F.col("lookup.Key").alias("Key"),
        F.col("lookup.LEAD_CO_MNE").alias("LEAD_CO_MNE1"),
        F.col("lookup.BRANCH_CO_MNE").alias("BRANCH_CO_MNE1"),
        F.col("lookup.MIS_DATE").alias("MIS_DATE1"),
        F.col("lookup.DESCRIPTION").alias("DESCRIPTION1"),
        F.col("lookup.SHORT_NAME").alias("SHORT_NAME1"),
        F.col(f"source.{ORDINAL_COL}"),
    ).withColumn(
        "New_Flag", iif(isnull(F.col("Key")), F.lit("Insert"))
    ).withColumn(
        "MD5_src",
        aes_decrypt(
            F.col("LEAD_CO_MNE1"),
            substr(F.col("SHORT_NAME"), 1, 3),
            F.lit(256),
        ),
    ).withColumn(
        "MD5_tgt",
        md5(
            concat(
                F.col("LEAD_CO_MNE"),
                F.col("BRANCH_CO_MNE"),
                F.col("MIS_DATE"),
                F.col("DESCRIPTION"),
                F.col("SHORT_NAME"),
            )
        ),
    ).withColumn(
        "Changed_Flag",
        iif(
            not_(isnull(F.col("Key"))) & (
                F.col("MD5_tgt") != F.col("MD5_src")
            ),
            F.lit("Update"),
        ),
    ).withColumn("o_CREATED_BY", F.lit("IDWUSER")
    ).withColumn("o_CREATED_TIME", ctx.sysdate
    ).withColumn("o_UPDATED_BY", F.lit("IDWUSER")
    ).withColumn("o_UPDATED_TIME", ctx.sysdate)

    insert_rows = transformed.where(F.col("New_Flag") == F.lit("Insert"))
    update_rows = transformed.where(F.col("Changed_Flag") == F.lit("Update"))
    sequence_window = Window.orderBy(F.col(ORDINAL_COL))
    insert_rows = insert_rows.withColumn(
        "_sequence_key",
        (F.lit(56) + F.row_number().over(sequence_window)).cast("long"),
    )

    ins = insert_rows.select(
        F.col("_sequence_key").alias("Key"),
        "LEAD_CO_MNE",
        "BRANCH_CO_MNE",
        "MIS_DATE",
        "ID",
        "DESCRIPTION",
        "SHORT_NAME",
        F.col("o_CREATED_BY").alias("CREATED_BY"),
        F.col("o_CREATED_TIME").alias("CREATED_TIME"),
    )
    upd = update_rows.select(
        F.col("Key").cast("double").alias("Key"),
        "LEAD_CO_MNE",
        "BRANCH_CO_MNE",
        "MIS_DATE",
        "ID",
        "DESCRIPTION",
        "SHORT_NAME",
        F.col("o_UPDATED_BY").alias("UPDATED_BY"),
        F.col("o_UPDATED_TIME").alias("UPDATED_TIME"),
    )
    return MappingResult(
        targets={"demo_target1_INS": ins, "demo_target1_UPD": upd},
        sort_keys={"demo_target1_INS": ("ID",), "demo_target1_UPD": ("ID",)},
    )
