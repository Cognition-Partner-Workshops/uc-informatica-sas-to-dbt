"""Milestone 0 stub for m_demo_mapping1."""

from ..context import MappingContext, MappingResult

MAPPING_NAME = "m_demo_mapping1"
SOURCES = ("demo_source3", "demo_source4", "demo_source5",
           "lkp_demo_source1", "lkp_demo_source2", "lkp_demo_source3")
TARGET_INSTANCES = ("demo_target3", "demo_target5", "demo_target6")


def run(ctx: MappingContext) -> MappingResult:
    raise NotImplementedError
