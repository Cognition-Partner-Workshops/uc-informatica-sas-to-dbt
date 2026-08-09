import pytest
from pyspark.sql import functions as F

from informatica_pyspark.config import RunConfig
from informatica_pyspark.context import AbortCheck, InformaticaAbort, MappingResult
from informatica_pyspark.workflow.runner import run_mapping, run_workflow


class Reader:
    def __init__(self, spark):
        self.spark = spark

    def read(self, name):
        return self.spark.range(1)


class Writer:
    def __init__(self):
        self.writes = []

    def write(self, name, frame):
        self.writes.append(name)


def test_abort_check_prevents_writes(spark, capsys):
    writer = Writer()

    def aborting(_ctx):
        return MappingResult(
            targets={"target": spark.range(1)},
            abort_checks=[AbortCheck(spark.range(1).select(F.lit(1)),
                                     "Relationship_to_Subscriber_Code_Labe valuel is null")],
        )

    code = run_mapping(
        "m_demo_mapping1", RunConfig(), mapping_runner={"m_demo_mapping1": aborting},
        reader=Reader(spark), writer=writer, spark=spark,
    )
    assert code != 0
    assert writer.writes == []
    assert capsys.readouterr().err == (
        "ABORT('Relationship_to_Subscriber_Code_Labe valuel is null')\n"
    )
    result = run_workflow(
        RunConfig(), mapping_runner={
            "m_demo_mapping1": aborting,
            "m_demo_mapping2": lambda _: MappingResult(),
            "m_demo_mapping3": lambda _: MappingResult(),
        }, reader=Reader(spark), writer=Writer(), spark=spark, log=lambda _: None)
    error = result.sessions["s_m_demo_mapping1"].error
    assert isinstance(error, InformaticaAbort)
    assert str(error) == "Relationship_to_Subscriber_Code_Labe valuel is null"


def test_unexpected_session_failure_prints_traceback(spark, capsys):
    def broken(_ctx):
        raise RuntimeError("unexpected mapping bug")

    code = run_mapping(
        "m_demo_mapping1", RunConfig(), mapping_runner={"m_demo_mapping1": broken},
        reader=Reader(spark), writer=Writer(), spark=spark,
    )
    assert code != 0
    stderr = capsys.readouterr().err
    assert "Traceback (most recent call last):" in stderr
    assert "RuntimeError: unexpected mapping bug" in stderr


def test_abort_preserves_prior_mapping_outputs_but_not_aborting_targets(spark):
    writer = Writer()

    def completed(*instances):
        return lambda _ctx: MappingResult(
            targets={instance: spark.range(1) for instance in instances}
        )

    def aborting(_ctx):
        return MappingResult(
            targets={"demo_target2": spark.range(1), "demo_target21": spark.range(1)},
            abort_checks=[AbortCheck(spark.range(1).select(F.lit(1)), "abort")],
        )

    result = run_workflow(
        RunConfig(), mapping_runner={
            "m_demo_mapping1": completed("demo_target3", "demo_target5", "demo_target6"),
            "m_demo_mapping2": completed("demo_target1_INS", "demo_target1_UPD"),
            "m_demo_mapping3": aborting,
        }, reader=Reader(spark), writer=writer, spark=spark, log=lambda _: None,
    )
    assert result.failed
    assert writer.writes == [
        "demo_target1_INS", "demo_target1_UPD", "demo_target3", "demo_target5", "demo_target6",
    ]


@pytest.mark.skip(reason="Real mapping3 remains a Milestone 0 stub.")
def test_real_data_abort_fixture():
    pass
