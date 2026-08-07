import datetime as dt

from informatica_pyspark.config import RunConfig
from informatica_pyspark.functions import lookup_use_last_value
from informatica_pyspark.io import LocalCsvIO
from informatica_pyspark.mappings.m_demo_mapping1 import run


def _io(spark, tmp_path):
    cfg = RunConfig(business_date=dt.date(2024, 1, 31), out_dir=tmp_path)
    return cfg, LocalCsvIO(spark, cfg)


def test_mapping1_last_value_lookup_collapses_duplicate_keys(spark, tmp_path):
    cfg, io = _io(spark, tmp_path)
    lookup = lookup_use_last_value(
        io.read_source("lkp_demo_source3"), ["ACCT_ID"], "__ROW_ORD"
    )

    rows = lookup.where("ACCT_ID = 1002").select("TX_TYPE_CD").collect()

    assert [row.TX_TYPE_CD for row in rows] == ["DR"]
    assert lookup.select("ACCT_ID").count() == lookup.select("ACCT_ID").distinct().count()


def test_mapping1_routes_lookup_return_to_target6_tx_type(spark, tmp_path):
    cfg, io = _io(spark, tmp_path)
    outputs = run(spark, cfg, io)

    row = (
        outputs["demo_target6"]
        .where("ACCT_ID = 1002")
        .select("TX_TYPE_CD")
        .collect()
    )

    assert [item.TX_TYPE_CD for item in row] == ["DR"]


def test_mapping1_drops_null_account_type_from_both_router_groups(spark, tmp_path):
    cfg, io = _io(spark, tmp_path)
    outputs = run(spark, cfg, io)

    assert outputs["demo_target6"].where("ACCT_ID = 1005").count() == 0
    assert outputs["demo_target5"].where("ACCT_ID = 1005").count() == 0
