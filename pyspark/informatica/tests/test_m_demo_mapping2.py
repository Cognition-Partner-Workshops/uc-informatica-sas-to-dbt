from datetime import date
from pathlib import Path

from pyspark.sql import functions as F

from informatica_pyspark.config import RunConfig
from informatica_pyspark.context import MappingContext
from informatica_pyspark.functions import iif, isnull
from informatica_pyspark.io.local_csv import LocalCsvReader
from informatica_pyspark.mappings.m_demo_mapping2 import run


DATA = Path(__file__).resolve().parents[3] / "legacy/informatica/data"


def _sources(spark):
    reader = LocalCsvReader(spark, str(DATA))
    return {
        "demo_source1": reader.read("demo_source1"),
        "demo_target1": reader.read("demo_target1"),
    }


def _result(spark):
    config = RunConfig(business_date=date(2024, 1, 31))
    return run(
        MappingContext(
            spark=spark,
            config=config,
            sources=_sources(spark),
        )
    )


def test_md5_defect_flags_genuinely_unchanged_matched_row_as_update(spark):
    sources = _sources(spark)
    unchanged = sources["demo_target1"].where("ID = 'REC00001'").select(
        "LEAD_CO_MNE",
        "BRANCH_CO_MNE",
        "MIS_DATE",
        "ID",
        "DESCRIPTION",
        "SHORT_NAME",
        "SRC_ORDINAL",
    )
    result = run(
        MappingContext(
            spark=spark,
            config=RunConfig(business_date=date(2024, 1, 31)),
            sources={"demo_source1": unchanged, "demo_target1": sources["demo_target1"]},
        )
    )
    assert result.targets["demo_target1_INS"].count() == 0
    row = result.targets["demo_target1_UPD"].first()
    assert row.ID == "REC00001"
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
