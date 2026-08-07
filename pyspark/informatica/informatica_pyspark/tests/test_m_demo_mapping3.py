from pathlib import Path

import pytest
from pyspark.sql import functions as F

from informatica_pyspark.config import RunConfig, RunContext
from informatica_pyspark.infa import InformaticaAbort
from informatica_pyspark.io import CsvIO
from informatica_pyspark.mappings import m_demo_mapping3


SOURCE_HEADER = (
    "Title,First_Name,Middle_Name,Last_Name,Member_ID,Member_Suffix,"
    "Birth_Date,Gender_Code,Member_Record_Number,Social_Security_Number,"
    "Member_Type_Code,Original_Effective_Date,Relationship_to_Subscriber_Code,"
    "Relationship_to_Subscriber_Code_Label\n"
)


def _context(spark, input_dir):
    cfg = RunConfig(input_dir=Path(input_dir))
    return RunContext(cfg, spark, CsvIO(spark, cfg))


def _write_source(path, *rows):
    path.write_text(SOURCE_HEADER + "\n".join(rows) + "\n")


def test_mapping3_filters_and_routes_to_the_correct_instances(spark):
    outputs = m_demo_mapping3.run(_context(spark, "legacy/informatica/data"))

    assert outputs["demo_target2"].select("Member_Identifier").orderBy(
        "Member_Identifier"
    ).rdd.map(lambda row: row[0]).collect() == [30001.0, 30003.0, 30007.0]
    assert outputs["demo_target21"].select("Member_Identifier").orderBy(
        "Member_Identifier"
    ).rdd.map(lambda row: row[0]).collect() == [30002.0, 30004.0, 30006.0]
    assert outputs["demo_target2"].filter(F.col("Member_Identifier") == 30005).count() == 0


def test_mapping3_renames_and_orders_target_columns(spark):
    outputs = m_demo_mapping3.run(_context(spark, "legacy/informatica/data"))

    assert outputs["demo_target2"].columns == [
        "Title",
        "Gender",
        "First_Name",
        "Middle_Name",
        "Last_Name",
        "Member_Identifier",
        "Member_Suffix",
        "Date_of_Birth",
        "Member_Number",
        "Soc_Number",
        "Type_Code",
        "Relationship_to_Subscriber_Code",
        "Relationship_to_Subscriber_Code_Label",
        "Effective_Date",
    ]


def test_mapping3_aborts_only_for_null_label_on_filtered_in_row(spark, tmp_path):
    source = tmp_path / "source.csv"
    _write_source(
        source,
        "MS,Tara,S,Young,40001,,1982-11-01,F,600001,100000222,1,2021-07-01,1,",
    )
    cfg = RunConfig(input_overrides={"demo_source2": str(source)})
    with pytest.raises(InformaticaAbort, match=m_demo_mapping3.ABORT_MESSAGE):
        m_demo_mapping3.run(RunContext(cfg, spark, CsvIO(spark, cfg)))

    _write_source(
        source,
        "MR,Mina,Q,Lee,40002,Jr,1975-06-14,F,600002,,,"
        "2020-03-01,3,",
    )
    outputs = m_demo_mapping3.run(RunContext(cfg, spark, CsvIO(spark, cfg)))
    assert outputs["demo_target2"].count() == 0
    assert outputs["demo_target21"].count() == 0


def test_csv_input_override_is_used_for_named_source(spark, tmp_path):
    source = tmp_path / "override.csv"
    _write_source(
        source,
        "MR,Nico,T,Singh,40003,,1992-09-30,M,600003,,2,2023-02-14,19,SELF",
    )
    cfg = RunConfig(
        input_dir=tmp_path / "does-not-exist",
        input_overrides={"demo_source2": str(source)},
    )

    assert CsvIO(spark, cfg).read("demo_source2").count() == 1
