"""Mapping 2 contract: return exact target-instance schemas; never write or stop Spark."""

from ..config import RunContext

TARGETS = ["demo_target1_INS", "demo_target1_UPD"]


def run(ctx: RunContext) -> dict:
    raise NotImplementedError("m_demo_mapping2 is implemented in a later milestone")
