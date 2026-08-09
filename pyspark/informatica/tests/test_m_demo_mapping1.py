from datetime import date
from pathlib import Path

import pytest

from informatica_pyspark.config import RunConfig
from informatica_pyspark.context import MappingContext
from informatica_pyspark import functions
from informatica_pyspark.io.local_csv import LocalCsvReader
from informatica_pyspark.mappings.m_demo_mapping1 import run
from pyspark.sql import functions as F


DATA = Path(__file__).resolve().parents[3] / "legacy" / "informatica" / "data"


def mapping_result(spark):
    config = RunConfig(business_date=date(2024, 1, 31))
    reader = LocalCsvReader(spark, str(DATA))
    names = (
        "demo_source3", "demo_source4", "demo_source5",
        "lkp_demo_source1", "lkp_demo_source2", "lkp_demo_source3",
    )
    sources = {name: reader.read(name) for name in names}
    return run(MappingContext(spark=spark, config=config, sources=sources))


def mapping_result_with_sources(spark):
    config = RunConfig(business_date=date(2024, 1, 31))
    reader = LocalCsvReader(spark, str(DATA))
    names = (
        "demo_source3", "demo_source4", "demo_source5",
        "lkp_demo_source1", "lkp_demo_source2", "lkp_demo_source3",
    )
    sources = {name: reader.read(name) for name in names}
    return config, sources


def test_positional_override_and_discarded_strcmp(spark):
    config, sources = mapping_result_with_sources(spark)
    result = run(MappingContext(spark=spark, config=config, sources=sources))
    target = result.targets["demo_target6"].orderBy("ACCT_ID").collect()

    override_values = (
        sources["demo_source3"].alias("source3")
        .join(
            sources["demo_source4"].alias("source4"),
            F.col("source3.ACCT_ID") == F.col("source4.ACCT_ID"),
            "inner",
        )
        .select(
            functions.strcmp(
                F.col("source4.ACCT_STAT_CD"), F.col("source3.TX_TYPE_CD")
            ).alias("OVERRIDE_STRCMP")
        )
        .collect()
    )
    assert all(row.OVERRIDE_STRCMP is not None for row in override_values)
    assert all(isinstance(row.OVERRIDE_STRCMP, int) for row in override_values)
    assert {row.OVERRIDE_STRCMP for row in override_values} == {-1, 1}
    assert target[0]["CR8_DT"].isoformat() == "2024-01-31"
    assert target[0]["TX_TYPE_CD"] == "DR"
    assert "WRK_SQL_TX_TYPE_CD" not in result.targets["demo_target6"].columns


def test_unconnected_lookup_returns_last_tx_type_code(spark):
    result = mapping_result(spark)
    rows = result.targets["demo_target6"].select("ACCT_ID", "TX_TYPE_CD").collect()
    assert {(row.ACCT_ID, row.TX_TYPE_CD) for row in rows} == {(1001, "DR"), (1002, "DR")}


def test_all_lookup_use_last_value(spark):
    result = mapping_result(spark)
    target5 = result.targets["demo_target5"].orderBy("ACCT_ID").collect()
    assert [(row.ACCT_ID, row.FIRST_NM, row.CRDT_SCORE) for row in target5] == [
        (1003, "IVY", 677),
        (1004, "AVA", 626),
    ]
    target6 = result.targets["demo_target6"].orderBy("ACCT_ID").collect()
    assert target6[1].TX_TYPE_CD == "DR"


def test_lookup_duplicates_are_last_value_for_first_name_and_score(spark):
    config, sources = mapping_result_with_sources(spark)
    sources["demo_source4"] = sources["demo_source4"].withColumn(
        "ACCT_TYP",
        F.when(F.col("ACCT_ID") == "1002", F.lit("CA")).otherwise(F.col("ACCT_TYP")),
    )
    result = run(MappingContext(spark=spark, config=config, sources=sources))
    row = result.targets["demo_target5"].where("ACCT_ID = 1002").first()
    assert row.FIRST_NM == "ZOE"
    assert row.CRDT_SCORE == 450


def test_router_null_account_type_is_dropped_and_aggregator_is_deterministic(spark):
    result = mapping_result(spark)
    target5 = result.targets["demo_target5"]
    target6 = result.targets["demo_target6"]
    assert target5.select("ACCT_ID").rdd.flatMap(lambda row: row).collect() == [1003, 1004]
    row = target6.where("ACCT_ID = 1001").first()
    assert row.TX_ID == 5002
    assert row.TX_AMT == pytest.approx(2031.24)
    assert row.CRDT_LN == "8000"


def test_sequence_and_legacy_sell_start_date_defect(spark):
    result = mapping_result(spark)
    target6 = result.targets["demo_target6"].orderBy("ACCT_ID").collect()
    assert [row.ACCT_KEY for row in target6] == [281, 282]
    target3 = result.targets["demo_target3"]
    assert target3.where("SELL_ST_DT IS NOT NULL").count() == 0
    assert target3.count() == 4
