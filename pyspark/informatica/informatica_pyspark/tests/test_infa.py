from datetime import date, datetime

import pytest
from pyspark.sql import functions as F
from pyspark.sql.types import DateType, StringType, StructField, StructType, TimestampType

from informatica_pyspark.infa import (
    InformaticaAbort,
    abort_if,
    iif,
    infa_to_date,
    lookup,
    sequence_nextval,
)
from informatica_pyspark.config import RunConfig
from informatica_pyspark.io import CsvIO


def test_infa_helpers(spark):
    df = spark.createDataFrame([("31/01/2024", "bad")], ["good", "bad"])
    assert df.select(infa_to_date("good", "DD/MM/YYYY")).first()[0] == date(2024, 1, 31)
    assert df.select(infa_to_date("bad", "DD/MM/YYYY")).first()[0] is None
    assert df.select(iif(F.lit(True), F.lit("yes"))).first()[0] == "yes"


def test_lookup_policies(spark):
    df = spark.createDataFrame([(1, 2, 1), (1, 9, 2)], ["id", "Key", "__line_ordinal"])
    assert lookup(df, ["id"], "Use Last Value").first()["Key"] == 9
    assert lookup(
        df, ["id"], "Use Any Value", any_value_order=[("Key", True)]
    ).first()["Key"] == 9


def test_sequence_and_abort(spark):
    df = spark.createDataFrame([(2,), (1,)], ["id"])
    assert [r.NEXTVAL for r in sequence_nextval(df, ["id"], 57).orderBy("id").collect()] == [57, 58]
    with pytest.raises(InformaticaAbort):
        abort_if(df, F.col("id") == 1, "bad")


def test_csv_write_matches_baseline_formatting(spark, tmp_path):
    cfg = RunConfig(output_dir=tmp_path)
    io = CsvIO(spark, cfg)
    df = spark.createDataFrame(
        [
            (datetime(2024, 1, 31, 0, 0), datetime(2024, 1, 31, 12, 34, 56),
             date(2024, 1, 31), None, None),
        ],
        StructType([
            StructField("midnight", TimestampType()),
            StructField("timestamp", TimestampType()),
            StructField("date_value", DateType()),
            StructField("date_null", DateType()),
            StructField("string_null", StringType()),
        ]),
    )
    io.write("fixture", df)
    assert (tmp_path / "fixture.csv").read_bytes() == (
        b"midnight,timestamp,date_value,date_null,string_null\n"
        b"2024-01-31,2024-01-31 12:34:56,2024-01-31,,\n"
    )


def test_csv_lookup_ordinal_is_last_physical_line(spark, tmp_path):
    lookup_path = tmp_path / "lkp_demo_source1.csv"
    lookup_path.write_text(
        "ACCT_ID,CUST_ID,FIRST_NM,LAST_NM,CUST_ADDR,CUST_PHN,CUST_EML_ADDR,AGE,DOB,CUST_TYP\n"
        "1001,70031,FIRST,,,,,,,\n"
        "1001,70031,LAST,,,,,,,\n"
    )
    io = CsvIO(spark, RunConfig(input_dir=tmp_path))
    result = lookup(io.read("lkp_demo_source1"), ["ACCT_ID"]).first()
    assert result["FIRST_NM"] == "LAST"
    assert result["__line_ordinal"] == 1
