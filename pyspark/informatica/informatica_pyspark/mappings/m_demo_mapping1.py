"""Mapping 1 contract: return exact target-instance schemas; never write or stop Spark."""

from ..config import RunContext

TARGETS = ["demo_target3", "demo_target5", "demo_target6"]


def run(ctx: RunContext) -> dict:
    raise NotImplementedError("m_demo_mapping1 is implemented in a later milestone")
