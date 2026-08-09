"""Milestone 0 stub for m_demo_mapping3."""

from ..context import MappingContext, MappingResult

MAPPING_NAME = "m_demo_mapping3"
SOURCES = ("demo_source2",)
TARGET_INSTANCES = ("demo_target2", "demo_target21")


def run(ctx: MappingContext) -> MappingResult:
    raise NotImplementedError
