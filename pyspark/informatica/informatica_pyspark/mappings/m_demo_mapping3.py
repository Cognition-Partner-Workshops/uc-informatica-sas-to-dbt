"""Mapping 3 contract: return exact target-instance schemas; abort before writing any target."""

from ..config import RunContext

TARGETS = ["demo_target2", "demo_target21"]


def run(ctx: RunContext) -> dict:
    raise NotImplementedError("m_demo_mapping3 is implemented in a later milestone")
