import datetime as dt

import pytest

from informatica_pyspark.config import RunConfig
from informatica_pyspark.functions import InformaticaAbort
from informatica_pyspark.io import LocalCsvIO
from informatica_pyspark.mappings import m_demo_mapping3


def _outputs(spark, tmp_path, data_dir="legacy/informatica/data"):
    cfg = RunConfig(
        business_date=dt.date(2024, 1, 31),
        data_dir=data_dir,
        out_dir=tmp_path,
    )
    io = LocalCsvIO(spark, cfg)
    return m_demo_mapping3.run(spark, cfg, io)


def test_abort_fails_before_writing_targets(spark, tmp_path):
    with pytest.raises(InformaticaAbort, match="Relationship_to_Subscriber"):
        _outputs(spark, tmp_path, "legacy/informatica/data/abort")

    assert list(tmp_path.glob("*.csv")) == []


def test_router_groups_follow_connector_targets(spark, tmp_path):
    outputs = _outputs(spark, tmp_path)
    target2_ids = {
        row.Member_Identifier
        for row in outputs["demo_target2"].select("Member_Identifier").collect()
    }
    target21_ids = {
        row.Member_Identifier
        for row in outputs["demo_target21"].select("Member_Identifier").collect()
    }

    assert target2_ids == {30001.0, 30003.0, 30007.0}
    assert target21_ids == {30002.0, 30004.0, 30006.0}
    assert all(row.Soc_Number is None for row in outputs["demo_target2"].collect())
    assert all(row.Soc_Number is not None for row in outputs["demo_target21"].collect())


def test_source_filter_excludes_member_with_null_type_code(spark, tmp_path):
    outputs = _outputs(spark, tmp_path)
    all_ids = {
        row.Member_Identifier
        for frame in outputs.values()
        for row in frame.select("Member_Identifier").collect()
    }

    assert len(all_ids) == 6
    assert 30005.0 not in all_ids
