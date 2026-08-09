import os
import subprocess
import sys
from pathlib import Path

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


def test_real_data_abort_fixture(tmp_path, capsys):
    normal_dir = tmp_path / "normal"
    abort_dir = tmp_path / "abort"
    assert run_mapping(
        "m_demo_mapping3", RunConfig(target_dir=str(normal_dir))
    ) == 0
    assert (normal_dir / "demo_target2.csv").exists()
    assert (normal_dir / "demo_target21.csv").exists()

    assert run_mapping(
        "m_demo_mapping3",
        RunConfig(source_variant="abort", target_dir=str(abort_dir)),
    ) != 0
    assert capsys.readouterr().err == (
        "ABORT('Relationship_to_Subscriber_Code_Labe valuel is null')\n"
    )
    assert not (abort_dir / "demo_target2.csv").exists()
    assert not (abort_dir / "demo_target21.csv").exists()


def _run_cli(*arguments):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])
    return subprocess.run(
        [sys.executable, "-m", "informatica_pyspark.cli", *arguments],
        cwd=Path(__file__).resolve().parents[3],
        env=env,
        text=True,
        capture_output=True,
    )


def test_real_data_workflow_abort_writes_prior_sessions_only(tmp_path):
    target_dir = tmp_path / "workflow-abort"
    completed = _run_cli(
        "run-workflow",
        "--io", "local",
        "--source-variant", "abort",
        "--target-dir", str(target_dir),
    )
    assert completed.returncode != 0
    assert "ABORT('Relationship_to_Subscriber_Code_Labe valuel is null')" in (
        completed.stderr.splitlines()
    )
    assert "Failed_Email3: subject='Execution Status' text='Dataload  s_m_demo_mapping3t was failed to execute'" in completed.stdout
    # §5 forbids partial writes within the aborting session; at workflow
    # level, earlier sessions already completed and their targets remain.
    for target in (
        "demo_target1_INS", "demo_target1_UPD", "demo_target3",
        "demo_target5", "demo_target6",
    ):
        assert (target_dir / f"{target}.csv").exists()
    assert not (target_dir / "demo_target2.csv").exists()
    assert not (target_dir / "demo_target21.csv").exists()


def test_real_data_workflow_normal_writes_all_targets(tmp_path):
    target_dir = tmp_path / "workflow-normal"
    completed = _run_cli(
        "run-workflow",
        "--io", "local",
        "--target-dir", str(target_dir),
    )
    assert completed.returncode == 0
    for target in (
        "demo_target1_INS", "demo_target1_UPD", "demo_target2",
        "demo_target21", "demo_target3", "demo_target5", "demo_target6",
    ):
        assert (target_dir / f"{target}.csv").exists()
