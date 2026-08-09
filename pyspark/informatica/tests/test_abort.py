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


def test_abort_check_prevents_writes(spark):
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
    result = run_workflow(
        RunConfig(), mapping_runner={
            "m_demo_mapping1": aborting,
            "m_demo_mapping2": lambda _: MappingResult(),
            "m_demo_mapping3": lambda _: MappingResult(),
        }, reader=Reader(spark), writer=Writer(), spark=spark, log=lambda _: None)
    error = result.sessions["s_m_demo_mapping1"].error
    assert isinstance(error, InformaticaAbort)
    assert str(error) == "Relationship_to_Subscriber_Code_Labe valuel is null"


@pytest.mark.skip(reason="Real mapping3 remains a Milestone 0 stub.")
def test_real_data_abort_fixture():
    pass
