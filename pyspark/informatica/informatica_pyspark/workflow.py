import logging

from .config import RunContext
from .mappings import REGISTRY

LOG = logging.getLogger(__name__)


def run_workflow(ctx: RunContext) -> int:
    statuses = {}
    LOG.info("Start")
    LOG.info("Evaluating s_m_demo_mapping2")
    for name in ("m_demo_mapping2", "m_demo_mapping1", "m_demo_mapping3"):
        try:
            outputs = REGISTRY[name].run(ctx)
            for instance, df in outputs.items():
                ctx.io.write(instance, df)
            statuses[name] = 1
            if name == "m_demo_mapping2":
                LOG.info("Decision1: $s_m_demo_mapping2.Status = 1 -> status=1")
                LOG.info("Decision1 empty condition -> s_m_demo_mapping1 (unconditional DEF-5)")
            elif name == "m_demo_mapping1":
                LOG.info("Decision2: $s_m_demo_mapping1.Status = 1 -> status=1")
                LOG.info("Decision2 Condition = 1 -> s_m_demo_mapping3")
            else:
                LOG.info("Decision3: $s_m_demo_mapping3.Status = 1 -> status=1")
                LOG.info("SuccessEmail")
        except Exception as exc:
            LOG.error("%s failed: %s", name, exc)
            statuses[name] = 0
            if name == "m_demo_mapping2":
                LOG.info("Decision1: $s_m_demo_mapping2.Status = 1 -> status=0")
                LOG.info("Failed_Email1")
                LOG.info("Decision1 empty condition -> s_m_demo_mapping1 (unconditional DEF-5)")
            if name == "m_demo_mapping1":
                LOG.info("Decision2: $s_m_demo_mapping1.Status = 1 -> status=0")
                LOG.info("Failed_Email2")
                LOG.info("Control: Stop parent")
                LOG.error("Control Stop parent after Failed_Email2")
                return 1
            if name == "m_demo_mapping3":
                LOG.info("Decision3: $s_m_demo_mapping3.Status = 1 -> status=0")
                LOG.info("Failed_Email3")
    return 0 if all(statuses.values()) else 1
