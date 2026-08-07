import importlib.util
import xml.etree.ElementTree as ET

import pytest
from pyspark.sql.types import (
    DateType,
    DoubleType,
    IntegerType,
    LongType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)

from informatica_pyspark.config import REPO_ROOT
from informatica_pyspark.io import (
    TARGET_INSTANCE_SCHEMAS,
    _validate_target_schema,
    snowflake_type,
)


def _loader_module():
    path = REPO_ROOT / "pyspark" / "informatica" / "scripts" / "snowflake_load.py"
    spec = importlib.util.spec_from_file_location("snowflake_load", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_target_schema_validation_rejects_mismatch_and_skips_unknown(spark):
    wrong = spark.createDataFrame([(1,)], ["wrong"])
    with pytest.raises(TypeError, match="demo_target5 schema mismatch"):
        _validate_target_schema("demo_target5", wrong)
    _validate_target_schema("rendering", wrong)


@pytest.mark.parametrize(
    ("spark_type", "snowflake"),
    [
        (LongType(), "NUMBER(38,0)"),
        (IntegerType(), "NUMBER(38,0)"),
        (DoubleType(), "FLOAT"),
        (StringType(), "VARCHAR"),
        (DateType(), "DATE"),
        (TimestampType(), "TIMESTAMP_NTZ"),
    ],
)
def test_snowflake_type_mapping(spark_type, snowflake):
    assert snowflake_type(spark_type) == snowflake


def test_snowflake_type_rejects_unsupported_type():
    with pytest.raises(TypeError, match="Unsupported Spark type"):
        snowflake_type(StructType([StructField("x", StringType())]))


def test_loader_value_conversion_preserves_nulls_and_spaces():
    loader = _loader_module()
    assert loader._python_value("", StringType()) is None
    assert loader._python_value("  8000", StringType()) == "  8000"


def test_loader_source_override_falls_back_per_file(tmp_path):
    loader = _loader_module()
    override = tmp_path / "demo_source2.csv"
    override.write_text("override")

    assert loader._source_path(tmp_path, "demo_source2") == override
    assert loader._source_path(tmp_path, "demo_source2").read_text() == "override"
    for table in loader.SOURCE_TABLES:
        path = loader._source_path(tmp_path, table)
        assert path.exists()
        if table != "demo_source2":
            assert path == REPO_ROOT / "legacy" / "informatica" / "data" / f"{table}.csv"


def test_registry_names_and_order_match_xml():
    root = ET.parse(
        REPO_ROOT / "legacy" / "informatica" / "wf_demo_mapping.XML"
    ).getroot()
    xml_targets = {
        target.attrib["NAME"]: [
            field.attrib["NAME"] for field in target.findall("TARGETFIELD")
        ]
        for target in root.findall(".//TARGET")
    }
    target_instances = {
        instance.attrib["NAME"]: instance.attrib["TRANSFORMATION_NAME"]
        for instance in root.findall(".//INSTANCE")
        if instance.attrib.get("TYPE") == "TARGET"
    }
    for instance, schema in TARGET_INSTANCE_SCHEMAS.items():
        target_name = target_instances.get(instance, instance)
        assert [field.name for field in schema.fields] == xml_targets[target_name]
