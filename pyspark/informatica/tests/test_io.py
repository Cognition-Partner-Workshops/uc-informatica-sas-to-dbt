import datetime as dt

from pyspark.sql.types import DateType, StringType, StructField, StructType, TimestampType

from informatica_pyspark.config import RunConfig
from informatica_pyspark.io import LocalCsvIO


def test_empty_csv_field_is_null(spark):
    cfg = RunConfig(business_date=dt.date(2024, 1, 31))
    frame = LocalCsvIO(spark, cfg).read_source("demo_source4")
    value = frame.where("ACCT_ID = 1005").select("ACCT_TYP").first().ACCT_TYP
    assert value is None


def test_target_date_and_timestamp_rendering(spark, tmp_path):
    cfg = RunConfig(business_date=dt.date(2024, 1, 31), out_dir=tmp_path)
    frame = spark.createDataFrame(
        [(dt.date(2024, 1, 31), dt.datetime(2024, 1, 15, 11, 0, 0))],
        StructType(
            [
                StructField("DATE_VALUE", DateType()),
                StructField("TIMESTAMP_VALUE", TimestampType()),
            ]
        ),
    )
    LocalCsvIO(spark, cfg).write_target("rendering", frame)
    assert (tmp_path / "rendering.csv").read_text() == (
        "DATE_VALUE,TIMESTAMP_VALUE\n2024-01-31,2024-01-15 11:00:00\n"
    )
