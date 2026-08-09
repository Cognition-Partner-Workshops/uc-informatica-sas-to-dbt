"""Milestone 0 stub for m_demo_mapping2."""

from ..context import MappingContext, MappingResult

MAPPING_NAME = "m_demo_mapping2"
SOURCES = ("demo_source1", "demo_target1")
TARGET_INSTANCES = ("demo_target1_INS", "demo_target1_UPD")


def run(ctx: MappingContext) -> MappingResult:
    raise NotImplementedError
