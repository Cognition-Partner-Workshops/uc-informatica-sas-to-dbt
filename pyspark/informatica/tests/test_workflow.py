import datetime as dt

import pytest

from informatica_pyspark.config import RunConfig
from informatica_pyspark import workflow


class _FakeSpark:
    def stop(self):
        pass


class _FakeIO:
    spark = _FakeSpark()


def _config():
    return RunConfig(business_date=dt.date(2024, 1, 31))


def test_workflow_uses_workflowlink_order(monkeypatch):
    executed = []

    def fake_run_mapping(name, cfg, io):
        executed.append(name)

    monkeypatch.setattr(workflow, "run_mapping", fake_run_mapping)
    workflow.run_workflow(_config(), _FakeIO())

    assert executed == [
        "m_demo_mapping2",
        "m_demo_mapping1",
        "m_demo_mapping3",
    ]


def test_workflow_is_fail_fast(monkeypatch):
    executed = []

    def fake_run_mapping(name, cfg, io):
        executed.append(name)
        if name == "m_demo_mapping1":
            raise RuntimeError("mapping failed")

    monkeypatch.setattr(workflow, "run_mapping", fake_run_mapping)

    with pytest.raises(RuntimeError, match="mapping failed"):
        workflow.run_workflow(_config(), _FakeIO())

    assert executed == ["m_demo_mapping2", "m_demo_mapping1"]
