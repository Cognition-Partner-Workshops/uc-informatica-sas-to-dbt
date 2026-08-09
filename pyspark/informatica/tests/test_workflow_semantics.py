from pyspark.sql import functions as F

from informatica_pyspark.config import RunConfig
from informatica_pyspark.context import MappingResult
from informatica_pyspark.workflow.runner import EMAILS, WORKFLOW_LINKS, WORKFLOW_TASKS, run_workflow


class Reader:
    def read(self, name):
        return self.spark.range(1)


class Writer:
    def __init__(self):
        self.writes = []
        self.frames = {}

    def write(self, name, frame):
        self.writes.append(name)
        self.frames[name] = frame


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


def test_workflow_declarations_preserve_xml_conditions():
    assert WORKFLOW_TASKS == (
        "Start", "Failed_Email2", "SuccessEmail", "Failed_Email1", "Control",
        "Decision2", "Decision1", "Decision3", "Failed_Email3",
    )
    assert sorted(WORKFLOW_LINKS) == sorted((
        ("Decision2", "Failed_Email2", "$Decision2.Condition = 0"),
        ("Decision3", "SuccessEmail", "$Decision3.Condition = 1"),
        ("Decision1", "Failed_Email1", "$Decision1.Condition = 0"),
        ("Failed_Email2", "Control", ""),
        ("Decision1", "s_m_demo_mapping1", ""),
        ("Decision2", "s_m_demo_mapping3", "$Decision2.Condition = 1"),
        ("Start", "s_m_demo_mapping2", ""),
        ("s_m_demo_mapping2", "Decision1", ""),
        ("s_m_demo_mapping1", "Decision2", ""),
        ("s_m_demo_mapping3", "Decision3", ""),
        ("Decision3", "Failed_Email3", "$Decision3.Condition = 0"),
    ))


def test_target_projection_helpers_and_declared_sort_keys(spark):
    writer = Writer()

    def mapping(_ctx):
        frame = spark.createDataFrame([(2, "x", "helper")], ["ID", "DESCRIPTION", "WRK_TEMP"])
        return MappingResult(
            targets={"demo_target1_INS": frame},
            sort_keys={"demo_target1_INS": ("ID",)},
        )

    result = run_workflow(
        RunConfig(), mapping_runner={
            "m_demo_mapping1": mapping,
            "m_demo_mapping2": lambda _: MappingResult(),
            "m_demo_mapping3": lambda _: MappingResult(),
        }, reader=Reader(), writer=writer, spark=spark, log=lambda _: None)
    assert result.sessions["s_m_demo_mapping2"].status == 1
    assert writer.frames["demo_target1_INS"].columns == [
        "Key", "LEAD_CO_MNE", "BRANCH_CO_MNE", "MIS_DATE", "ID", "DESCRIPTION", "SHORT_NAME",
        "CREATED_BY", "CREATED_TIME", "UPDATED_BY", "UPDATED_TIME", "ACTIVE_FLAG", "START_DATE",
        "END_DATE",
    ]
    assert "WRK_TEMP" not in writer.frames["demo_target1_INS"].columns
