from dataclasses import dataclass

from . import m_demo_mapping1, m_demo_mapping2, m_demo_mapping3


@dataclass(frozen=True)
class MappingSpec:
    run: object
    sources: tuple[str, ...]
    target_instances: tuple[str, ...]


MAPPINGS = {
    module.MAPPING_NAME: MappingSpec(module.run, module.SOURCES, module.TARGET_INSTANCES)
    for module in (m_demo_mapping1, m_demo_mapping2, m_demo_mapping3)
}
