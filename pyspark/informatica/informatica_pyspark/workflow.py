import logging

from .config import RunContext
from .mappings import REGISTRY

LOG = logging.getLogger(__name__)


def run_workflow(ctx: RunContext) -> int:
    statuses = {}
    for name in ("m_demo_mapping2", "m_demo_mapping1", "m_demo_mapping3"):
        try:
            outputs = REGISTRY[name].run(ctx)
            for instance, df in outputs.items():
                ctx.io.write(instance, df)
            statuses[name] = 1
        except Exception as exc:
            LOG.error("%s failed: %s", name, exc)
            statuses[name] = 0
            if name == "m_demo_mapping2":
                LOG.error("Decision1 empty condition is unconditional; continuing to mapping1")
            if name == "m_demo_mapping1":
                LOG.error("Control Stop parent after Failed_Email2")
                return 1
    return 0 if all(statuses.values()) else 1
