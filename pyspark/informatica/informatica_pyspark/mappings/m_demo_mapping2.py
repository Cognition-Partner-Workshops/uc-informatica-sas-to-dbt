"""Mapping 2 contract: return exact target-instance schemas; never write or stop Spark."""

from pyspark.sql import functions as F

from ..config import RunContext
from ..infa import iif, isnull, lookup, md5_concat, not_isnull, sequence_nextval
from ..io import attach_line_ordinal
from ..schemas import TARGET_SCHEMAS

TARGETS = ["demo_target1_INS", "demo_target1_UPD"]


def run(ctx: RunContext) -> dict:
    source = attach_line_ordinal(ctx.io.read("demo_source1"))
    existing = ctx.io.read("demo_target1")
    chosen = lookup(
        existing,
        ["ID"],
        policy="Use Any Value",
        any_value_order=[("Key", True), ("__line_ordinal", True)],
    ).select(
        "ID",
        F.col("Key").alias("lookup_Key"),
        F.col("LEAD_CO_MNE").alias("LEAD_CO_MNE1"),
        F.col("BRANCH_CO_MNE").alias("BRANCH_CO_MNE1"),
        F.col("MIS_DATE").alias("MIS_DATE1"),
        F.col("DESCRIPTION").alias("DESCRIPTION1"),
        F.col("SHORT_NAME").alias("SHORT_NAME1"),
    )
    enriched = source.join(chosen, source.ID == chosen.ID, "left").drop(chosen.ID)
    enriched = (
        enriched.withColumn("Key", F.col("lookup_Key"))
        .withColumn("New_Flag", iif(isnull("Key"), F.lit("Insert")))
        .withColumn("MD5_src", F.lit("LEGACY_AES_VALUE"))
        .withColumn(
            "MD5_tgt",
            md5_concat(
                "LEAD_CO_MNE", "BRANCH_CO_MNE", "MIS_DATE", "DESCRIPTION", "SHORT_NAME"
            ),
        )
        .withColumn(
            "Changed_Flag",
            iif(
                not_isnull("Key") & (F.col("MD5_tgt") != F.col("MD5_src")),
                F.lit("Update"),
            ),
        )
        .withColumn("o_CREATED_BY", F.lit("IDWUSER"))
        .withColumn(
            "o_CREATED_TIME",
            F.lit(ctx.cfg.business_date).cast("timestamp"),
        )
        .withColumn("o_UPDATED_BY", F.lit("IDWUSER"))
        .withColumn(
            "o_UPDATED_TIME",
            F.lit(ctx.cfg.business_date).cast("timestamp"),
        )
    )

    inserts = sequence_nextval(
        enriched.where(F.col("New_Flag") == "Insert"),
        ["__line_ordinal"],
        current_value=57,
    )
    updates = enriched.where(F.col("Changed_Flag") == "Update")
    target_fields = TARGET_SCHEMAS["demo_target1"].fields

    def output(df, values):
        return df.select(
            *[
                values.get(field.name, F.lit(None).cast(field.dataType)).alias(field.name)
                for field in target_fields
            ]
        )

    ins = output(
        inserts,
        {
            "Key": F.col("NEXTVAL").cast("double"),
            "LEAD_CO_MNE": F.col("LEAD_CO_MNE"),
            "BRANCH_CO_MNE": F.col("BRANCH_CO_MNE"),
            "MIS_DATE": F.col("MIS_DATE"),
            "ID": F.col("ID"),
            "DESCRIPTION": F.col("DESCRIPTION"),
            "SHORT_NAME": F.col("SHORT_NAME"),
            "CREATED_BY": F.col("o_CREATED_BY"),
            "CREATED_TIME": F.col("o_CREATED_TIME"),
        },
    )
    upd = output(
        updates,
        {
            "Key": F.col("Key"),
            "LEAD_CO_MNE": F.col("LEAD_CO_MNE"),
            "BRANCH_CO_MNE": F.col("BRANCH_CO_MNE"),
            "MIS_DATE": F.col("MIS_DATE"),
            "ID": F.col("ID"),
            "DESCRIPTION": F.col("DESCRIPTION"),
            "SHORT_NAME": F.col("SHORT_NAME"),
            "UPDATED_BY": F.col("o_UPDATED_BY"),
            "UPDATED_TIME": F.col("o_UPDATED_TIME"),
        },
    )
    return {"demo_target1_INS": ins.drop("__line_ordinal"), "demo_target1_UPD": upd.drop("__line_ordinal")}
