from datetime import date
from pathlib import Path

import pytest

from informatica_pyspark.config import RunConfig
from informatica_pyspark.context import MappingContext
from informatica_pyspark.io.local_csv import LocalCsvReader
from informatica_pyspark.mappings.m_demo_mapping1 import run


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


def test_positional_override_and_discarded_strcmp(spark):
    result = mapping_result(spark)
    target = result.targets["demo_target6"].orderBy("ACCT_ID").collect()

    assert target[0]["CR8_DT"].isoformat() == "2024-01-31"
    assert target[0]["TX_TYPE_CD"] == "DR"
    assert "WRK_SQL_TX_TYPE_CD" not in result.targets["demo_target6"].columns
    # The SQL override's STRCMP(A, DR) is -1, but the unconnected SQ port is
    # not allowed to reach any target.
    assert result.targets["demo_target6"].where("TX_TYPE_CD = -1").count() == 0


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
