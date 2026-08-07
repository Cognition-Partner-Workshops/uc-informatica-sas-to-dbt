from pyspark.sql import Window
from pyspark.sql import functions as F
from pyspark.sql.types import DateType, DoubleType, LongType

from ..functions import (
    inf_aes_decrypt_unrecoverable,
    inf_concat,
    inf_iif,
    inf_isnull,
    inf_md5,
    lookup_use_any_value,
)


TARGET_INSTANCES = ("demo_target1_INS", "demo_target1_UPD")


def run(spark, cfg, io):
    source = io.read_source("demo_source1").alias("source")
    lookup = lookup_use_any_value(
        io.read_source("demo_target1"), ["ID"], "__ROW_ORD"
    )
    lookup = lookup.select(
        F.col("ID").alias("__lookup_ID"),
        F.col("Key").alias("__lookup_Key"),
        F.col("LEAD_CO_MNE").alias("__lookup_LEAD_CO_MNE"),
        F.col("BRANCH_CO_MNE").alias("__lookup_BRANCH_CO_MNE"),
        F.col("MIS_DATE").alias("__lookup_MIS_DATE"),
        F.col("DESCRIPTION").alias("__lookup_DESCRIPTION"),
        F.col("SHORT_NAME").alias("__lookup_SHORT_NAME"),
    ).alias("lookup")

    joined = source.join(
        lookup,
        F.col("source.ID") == F.col("lookup.__lookup_ID"),
        "left",
    )

    exptrans = joined.select(
        F.col("source.LEAD_CO_MNE").alias("LEAD_CO_MNE"),
        F.col("source.BRANCH_CO_MNE").alias("BRANCH_CO_MNE"),
        F.col("source.MIS_DATE").alias("MIS_DATE"),
        F.col("source.ID").alias("ID"),
        F.col("source.DESCRIPTION").alias("DESCRIPTION"),
        F.col("source.SHORT_NAME").alias("SHORT_NAME"),
        F.col("lookup.__lookup_Key").cast(DoubleType()).alias("Key"),
        F.col("lookup.__lookup_LEAD_CO_MNE").alias("LEAD_CO_MNE1"),
        F.col("lookup.__lookup_BRANCH_CO_MNE").alias("BRANCH_CO_MNE1"),
        F.col("lookup.__lookup_MIS_DATE").alias("MIS_DATE1"),
        F.col("lookup.__lookup_DESCRIPTION").alias("DESCRIPTION1"),
        F.col("lookup.__lookup_SHORT_NAME").alias("SHORT_NAME1"),
        inf_aes_decrypt_unrecoverable(
            F.col("lookup.__lookup_LEAD_CO_MNE"),
            F.substring(F.col("source.SHORT_NAME"), 1, 3),
            256,
        ).alias("MD5_src"),
        inf_md5(
            inf_concat(
                F.col("source.LEAD_CO_MNE"),
                F.col("source.BRANCH_CO_MNE"),
                F.col("source.MIS_DATE"),
                F.col("source.DESCRIPTION"),
                F.col("source.SHORT_NAME"),
            )
        ).alias("MD5_tgt"),
        inf_isnull(F.col("lookup.__lookup_Key")).alias("__lookup_key_is_null"),
        F.lit("IDWUSER").alias("o_CREATED_BY"),
        F.lit(cfg.business_date).cast(DateType()).alias("o_CREATED_TIME"),
        F.lit("IDWUSER").alias("o_UPDATED_BY"),
        F.lit(cfg.business_date).cast(DateType()).alias("o_UPDATED_TIME"),
        F.col("source.__ROW_ORD").alias("__ROW_ORD"),
    ).withColumn(
        "New_Flag",
        inf_iif(F.col("__lookup_key_is_null"), F.lit("Insert")),
    ).withColumn(
        "Changed_Flag",
        inf_iif(
            (~inf_isnull(F.col("Key"))) & (F.col("MD5_tgt") != F.col("MD5_src")),
            F.lit("Update"),
        ),
    ).drop("__lookup_key_is_null")

    insert_rows = exptrans.where(F.col("New_Flag") == "Insert")
    insert_group = insert_rows.select(
        F.col("LEAD_CO_MNE").alias("LEAD_CO_MNE2"),
        F.col("BRANCH_CO_MNE").alias("BRANCH_CO_MNE2"),
        F.col("MIS_DATE").alias("MIS_DATE2"),
        F.col("ID").alias("ID1"),
        F.col("DESCRIPTION").alias("DESCRIPTION2"),
        F.col("SHORT_NAME").alias("SHORT_NAME2"),
        F.col("LEAD_CO_MNE1").alias("LEAD_CO_MNE11"),
        F.col("BRANCH_CO_MNE1").alias("BRANCH_CO_MNE11"),
        F.col("MIS_DATE1").alias("MIS_DATE11"),
        F.col("DESCRIPTION1").alias("DESCRIPTION11"),
        F.col("SHORT_NAME1").alias("SHORT_NAME11"),
        F.col("New_Flag").alias("New_Flag1"),
        F.col("Changed_Flag").alias("Changed_Flag1"),
        F.col("o_CREATED_BY").alias("o_CREATED_BY1"),
        F.col("o_CREATED_TIME").alias("o_CREATED_TIME1"),
        F.col("o_UPDATED_BY").alias("o_UPDATED_BY1"),
        F.col("o_UPDATED_TIME").alias("o_UPDATED_TIME1"),
        F.col("Key").alias("Key1"),
        F.col("__ROW_ORD"),
    )
    insert_window = Window.orderBy(F.col("__ROW_ORD"))
    insert = insert_group.select(
        (F.lit(56).cast(LongType()) + F.row_number().over(insert_window)).cast(
            LongType()
        ).alias("Key"),
        F.col("LEAD_CO_MNE2").alias("LEAD_CO_MNE"),
        F.col("BRANCH_CO_MNE2").alias("BRANCH_CO_MNE"),
        F.col("MIS_DATE2").alias("MIS_DATE"),
        F.col("ID1").alias("ID"),
        F.col("DESCRIPTION2").alias("DESCRIPTION"),
        F.col("SHORT_NAME2").alias("SHORT_NAME"),
        F.col("o_CREATED_BY1").alias("CREATED_BY"),
        F.col("o_CREATED_TIME1").alias("CREATED_TIME"),
        F.lit(None).cast("string").alias("UPDATED_BY"),
        F.lit(None).cast(DateType()).alias("UPDATED_TIME"),
        F.lit(None).cast("string").alias("ACTIVE_FLAG"),
        F.lit(None).cast(DateType()).alias("START_DATE"),
        F.lit(None).cast(DateType()).alias("END_DATE"),
    )

    update_group = exptrans.where(F.col("Changed_Flag") == "Update").select(
        F.col("LEAD_CO_MNE").alias("LEAD_CO_MNE4"),
        F.col("BRANCH_CO_MNE").alias("BRANCH_CO_MNE4"),
        F.col("MIS_DATE").alias("MIS_DATE4"),
        F.col("ID").alias("ID3"),
        F.col("DESCRIPTION").alias("DESCRIPTION4"),
        F.col("SHORT_NAME").alias("SHORT_NAME4"),
        F.col("LEAD_CO_MNE1").alias("LEAD_CO_MNE13"),
        F.col("BRANCH_CO_MNE1").alias("BRANCH_CO_MNE13"),
        F.col("MIS_DATE1").alias("MIS_DATE13"),
        F.col("DESCRIPTION1").alias("DESCRIPTION13"),
        F.col("SHORT_NAME1").alias("SHORT_NAME13"),
        F.col("New_Flag").alias("New_Flag3"),
        F.col("Changed_Flag").alias("Changed_Flag3"),
        F.col("o_CREATED_BY").alias("o_CREATED_BY3"),
        F.col("o_CREATED_TIME").alias("o_CREATED_TIME3"),
        F.col("o_UPDATED_BY").alias("o_UPDATED_BY3"),
        F.col("o_UPDATED_TIME").alias("o_UPDATED_TIME3"),
        F.col("Key").alias("Key3"),
    )
    updtrans = update_group.select(
        F.col("LEAD_CO_MNE4").alias("LEAD_CO_MNE3"),
        F.col("BRANCH_CO_MNE4").alias("BRANCH_CO_MNE3"),
        F.col("MIS_DATE4").alias("MIS_DATE3"),
        F.col("ID3").alias("ID2"),
        F.col("DESCRIPTION4").alias("DESCRIPTION3"),
        F.col("SHORT_NAME4").alias("SHORT_NAME3"),
        F.col("New_Flag3").alias("New_Flag2"),
        F.col("Changed_Flag3").alias("Changed_Flag2"),
        F.col("o_CREATED_BY3").alias("o_CREATED_BY2"),
        F.col("o_CREATED_TIME3").alias("o_CREATED_TIME2"),
        F.col("o_UPDATED_BY3").alias("o_UPDATED_BY2"),
        F.col("o_UPDATED_TIME3").alias("o_UPDATED_TIME2"),
        F.col("Key3").alias("Key2"),
    )
    update = updtrans.select(
        F.col("Key2").cast(DoubleType()).alias("Key"),
        F.col("LEAD_CO_MNE3").alias("LEAD_CO_MNE"),
        F.col("BRANCH_CO_MNE3").alias("BRANCH_CO_MNE"),
        F.col("MIS_DATE3").alias("MIS_DATE"),
        F.col("ID2").alias("ID"),
        F.col("DESCRIPTION3").alias("DESCRIPTION"),
        F.col("SHORT_NAME3").alias("SHORT_NAME"),
        F.lit(None).cast("string").alias("CREATED_BY"),
        F.lit(None).cast(DateType()).alias("CREATED_TIME"),
        F.col("o_UPDATED_BY2").alias("UPDATED_BY"),
        F.col("o_UPDATED_TIME2").alias("UPDATED_TIME"),
        F.lit(None).cast("string").alias("ACTIVE_FLAG"),
        F.lit(None).cast(DateType()).alias("START_DATE"),
        F.lit(None).cast(DateType()).alias("END_DATE"),
    )

    return {"demo_target1_INS": insert, "demo_target1_UPD": update}
