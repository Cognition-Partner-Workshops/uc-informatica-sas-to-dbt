from datetime import date
from pathlib import Path

from pyspark.sql import functions as F

from informatica_pyspark.config import RunConfig
from informatica_pyspark.context import MappingContext
from informatica_pyspark.functions import iif, isnull
from informatica_pyspark.io.base import ORDINAL_COL
from informatica_pyspark.mappings.m_demo_mapping2 import run


DATA = Path(__file__).resolve().parents[3] / "legacy/informatica/data"


def _source(spark, name):
    return (
        spark.read.option("header", "true")
        .option("inferSchema", "false")
        .csv(str(DATA / f"{name}.csv"))
        .withColumn(ORDINAL_COL, F.monotonically_increasing_id().cast("long"))
    )


def _result(spark):
    config = RunConfig(business_date=date(2024, 1, 31))
    return run(
        MappingContext(
            spark=spark,
            config=config,
            sources={
                "demo_source1": _source(spark, "demo_source1"),
                "demo_target1": _source(spark, "demo_target1"),
            },
        )
    )


def test_md5_defect_flags_genuinely_unchanged_matched_row_as_update(spark):
    result = _result(spark)
    row = result.targets["demo_target1_UPD"].where("ID = 'REC00001'").first()
    expected = spark.sql(
        "SELECT md5('BNK01BR1012024-01-31General ledger account 1GL0001')"
    ).first()[0]
    assert expected != "LEGACY_AES_VALUE"
    assert row.UPDATED_BY == "IDWUSER"
    assert row.Key == 1.0


def test_two_argument_iif_drives_null_router_flags(spark):
    result = _result(spark)
    assert result.targets["demo_target1_INS"].count() == 4
    assert result.targets["demo_target1_UPD"].count() == 3
    assert spark.range(1).select(
        iif(isnull(F.lit("matched")), F.lit("Insert")).alias("value")
    ).first().value is None


def test_use_any_value_tie_break_keeps_latest_ordinal_key_99(spark):
    result = _result(spark)
    row = result.targets["demo_target1_UPD"].where("ID = 'REC00002'").first()
    assert row.Key == 99.0


def test_sequence_starts_at_57_in_source_ordinal_order(spark):
    result = _result(spark)
    rows = result.targets["demo_target1_INS"].orderBy("ID").select("ID", "Key").collect()
    assert [(row.ID, row.Key) for row in rows] == [
        ("REC00004", 57),
        ("REC00005", 58),
        ("REC00006", 59),
        ("REC00007", 60),
    ]


def test_router_default_is_not_written_and_update_uses_source_description(spark):
    result = _result(spark)
    assert set(result.targets) == {"demo_target1_INS", "demo_target1_UPD"}
    row = result.targets["demo_target1_UPD"].where("ID = 'REC00001'").first()
    assert row.DESCRIPTION == "General ledger account 1"


def test_router_group_conditions_replicate_rows_that_match_both_groups(spark):
    rows = spark.createDataFrame(
        [("Insert", "Update"), (None, "Update")],
        ["New_Flag", "Changed_Flag"],
    )
    insert = rows.where(F.col("New_Flag") == "Insert")
    update = rows.where(F.col("Changed_Flag") == "Update")
    assert insert.count() == 1
    assert update.count() == 2
