import datetime as dt

from pyspark.sql import functions as F

from informatica_pyspark.config import RunConfig
from informatica_pyspark.functions import inf_iif
from informatica_pyspark.io import LocalCsvIO
from informatica_pyspark.mappings.m_demo_mapping2 import run


def _mapping2(spark):
    cfg = RunConfig(business_date=dt.date(2024, 1, 31))
    return run(spark, cfg, LocalCsvIO(spark, cfg))


def test_use_any_value_tie_break_selects_highest_key(spark):
    outputs = _mapping2(spark)
    row = outputs["demo_target1_UPD"].where("ID = 'REC00002'").first()
    assert row.Key == 99.0


def test_two_argument_iif_has_null_else_branch(spark):
    row = spark.range(1).select(
        inf_iif(F.lit(False), F.lit("true")).alias("value")
    ).first()
    assert row.value is None


def test_update_description_comes_from_source(spark):
    outputs = _mapping2(spark)
    row = outputs["demo_target1_UPD"].where("ID = 'REC00001'").first()
    assert row.DESCRIPTION == "General ledger account 1"
