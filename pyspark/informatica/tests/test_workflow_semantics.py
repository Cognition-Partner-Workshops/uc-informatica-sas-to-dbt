from informatica_pyspark.config import RunConfig
from informatica_pyspark.context import MappingResult
from informatica_pyspark.workflow.runner import EMAILS, run_workflow


class Reader:
    def read(self, name):
        return self.spark.range(1)


class Writer:
    def __init__(self):
        self.writes = []

    def write(self, name, frame):
        self.writes.append(name)


def outcomes(spark, statuses):
    def make(name):
        def run(_ctx):
            if statuses[name] == 0:
                raise RuntimeError(name)
            return MappingResult()
        return run
    return {name: make(name) for name in statuses}


def run(spark, statuses):
    reader = Reader()
    reader.spark = spark
    writer = Writer()
    result = run_workflow(RunConfig(), mapping_runner=outcomes(spark, statuses),
                          reader=reader, writer=writer, spark=spark, log=lambda _: None)
    return result


def test_all_success(spark):
    result = run(spark, {"m_demo_mapping1": 1, "m_demo_mapping2": 1, "m_demo_mapping3": 1})
    assert not result.failed
    assert result.emails == [("SuccessEmail", *EMAILS["SuccessEmail"])]


def test_mapping2_failure_still_runs_mapping1(spark):
    result = run(spark, {"m_demo_mapping1": 1, "m_demo_mapping2": 0, "m_demo_mapping3": 1})
    assert "s_m_demo_mapping1" in result.sessions
    assert result.emails[0] == ("Failed_Email1", *EMAILS["Failed_Email1"])


def test_mapping1_failure_stops_parent_before_mapping3(spark):
    result = run(spark, {"m_demo_mapping1": 0, "m_demo_mapping2": 1, "m_demo_mapping3": 1})
    assert "s_m_demo_mapping3" not in result.sessions
    assert result.emails == [("Failed_Email2", *EMAILS["Failed_Email2"])]
    assert result.failed


def test_mapping3_failure_emits_failed_email(spark):
    result = run(spark, {"m_demo_mapping1": 1, "m_demo_mapping2": 1, "m_demo_mapping3": 0})
    assert result.emails == [("Failed_Email3", *EMAILS["Failed_Email3"])]
