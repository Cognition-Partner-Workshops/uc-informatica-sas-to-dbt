from datetime import datetime

from informatica_pyspark.io.local_csv import LocalCsvWriter


def test_local_writer_uses_baseline_timestamp_format(spark, tmp_path):
    LocalCsvWriter(str(tmp_path)).write(
        "demo_target6",
        spark.createDataFrame([(datetime(2024, 1, 15, 11, 0, 0),)], ["TX_DTTM"]),
    )
    output = (tmp_path / "demo_target6.csv").read_text()
    assert "2024-01-15 11:00:00" in output
    assert "T11:00:00" not in output


def test_local_writer_prepare_removes_stale_targets(spark, tmp_path):
    writer = LocalCsvWriter(str(tmp_path))
    writer.write("stale_target", spark.createDataFrame([(1,)], ["value"]))
    assert (tmp_path / "stale_target.csv").exists()
    writer.prepare()
    assert not (tmp_path / "stale_target.csv").exists()
