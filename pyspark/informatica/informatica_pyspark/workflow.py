from __future__ import annotations

import logging

from .config import RunConfig
from .io import InformaticaIO, build_io
from .mappings import MAPPINGS
from .session import build_spark

LOGGER = logging.getLogger(__name__)
WORKFLOW_ORDER = ("m_demo_mapping2", "m_demo_mapping1", "m_demo_mapping3")


def run_mapping(name: str, cfg: RunConfig, io: InformaticaIO) -> None:
    mapping = MAPPINGS[name]
    spark = io.spark
    outputs = mapping.run(spark, cfg, io)
    for instance, frame in outputs.items():
        io.write_target(instance, frame)


def run_workflow(cfg: RunConfig, io: InformaticaIO | None = None) -> None:
    spark = io.spark if io is not None else build_spark(cfg)
    if io is None:
        io = build_io(spark, cfg)
    try:
        for name in WORKFLOW_ORDER:
            try:
                run_mapping(name, cfg, io)
            except Exception:
                LOGGER.exception("Failed_Email task for %s (NOT MIGRATED)", name)
                LOGGER.error("Control task: Stop parent (NOT MIGRATED)")
                raise
        LOGGER.info("SuccessEmail task (NOT MIGRATED)")
    finally:
        spark.stop()
