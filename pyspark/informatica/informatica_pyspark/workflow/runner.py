"""wf_demo_mapping workflow semantics, including its recovered defects."""

from dataclasses import dataclass, field
from typing import Callable

from pyspark.sql import functions as F

from ..config import RunConfig
from ..context import InformaticaAbort, MappingContext, MappingResult
from ..io import get_reader, get_writer
from ..mappings import MAPPINGS, MappingSpec
from ..session import build_spark
from ..targets import columns_for

EMAILS = {
    "Failed_Email2": ("Run status", "Sessio 's_m_demo_mapping1' failed"),
    "SuccessEmail": ("Run Status", "Session s_m_demo_mapping3 executed successfully"),
    "Failed_Email1": ("Execution Status", "Dataload s_m_demo_mapping2 was failed to execute"),
    "Failed_Email3": ("Execution Status", "Dataload  s_m_demo_mapping3t was failed to execute"),
}


@dataclass
class SessionOutcome:
    status: int
    result: MappingResult | None = None
    error: Exception | None = None


@dataclass
class WorkflowResult:
    sessions: dict[str, SessionOutcome] = field(default_factory=dict)
    emails: list[tuple[str, str, str]] = field(default_factory=list)
    failed: bool = False


def _emit_email(name: str, emails: list, log: Callable[[str], None]):
    subject, text = EMAILS[name]
    emails.append((name, subject, text))
    log(f"{name}: subject={subject!r} text={text!r}")


def _run_session(name: str, mapping_name: str, config: RunConfig, spark, reader, writer,
                 mapping_runner) -> SessionOutcome:
    try:
        spec = mapping_runner[mapping_name]
        if isinstance(spec, MappingSpec):
            run, source_names = spec.run, spec.sources
        else:
            run, source_names = spec, MAPPINGS[mapping_name].sources
        sources = {logical: reader.read(logical) for logical in source_names}
        result = run(MappingContext(spark=spark, config=config, sources=sources))
        for check in result.abort_checks:
            if check.predicate_df.limit(1).count():
                raise InformaticaAbort(check.message)
        for instance, frame in result.targets.items():
            expected = columns_for(instance)
            helper_columns = [column for column in frame.columns
                              if column.startswith(("SRC_", "WRK_"))]
            frame = frame.drop(*helper_columns)
            missing = [column for column in expected if column not in frame.columns]
            for column in missing:
                frame = frame.withColumn(column, F.lit(None))
            frame = frame.select(*expected)
            keys = result.sort_keys.get(instance)
            if keys:
                frame = frame.orderBy(*keys)
            else:
                # Fallback is deterministic but mappings should supply legacy sort keys.
                frame = frame.orderBy(*frame.columns)
            writer.write(instance, frame)
        return SessionOutcome(1, result=result)
    except Exception as exc:
        return SessionOutcome(0, error=exc)


def run_mapping(mapping_name: str, config: RunConfig, mapping_runner=None,
                reader=None, writer=None, spark=None) -> int:
    spark = spark or build_spark(config)
    reader = reader or get_reader(config)
    if getattr(reader, "spark", None) is None:
        reader.spark = spark
    writer = writer or get_writer(config)
    outcome = _run_session("s_" + mapping_name, mapping_name, config, spark, reader, writer,
                           mapping_runner or MAPPINGS)
    if outcome.error:
        print(str(outcome.error))
        return 1
    return 0


def run_workflow(config: RunConfig, mapping_runner=None, reader=None, writer=None,
                 spark=None, log=print) -> WorkflowResult:
    mapping_runner = mapping_runner or MAPPINGS
    result = WorkflowResult()
    spark = spark or build_spark(config)
    reader = reader or get_reader(config)
    if getattr(reader, "spark", None) is None:
        reader.spark = spark
    writer = writer or get_writer(config)

    # Start -> mapping2 -> Decision1.
    result.sessions["s_m_demo_mapping2"] = _run_session(
        "s_m_demo_mapping2", "m_demo_mapping2", config, spark, reader, writer, mapping_runner)
    mapping2_ok = result.sessions["s_m_demo_mapping2"].status == 1
    if not mapping2_ok:
        _emit_email("Failed_Email1", result.emails, log)

    # Empty Decision1 -> mapping1 link is intentional: mapping1 always runs.
    result.sessions["s_m_demo_mapping1"] = _run_session(
        "s_m_demo_mapping1", "m_demo_mapping1", config, spark, reader, writer, mapping_runner)
    mapping1_ok = result.sessions["s_m_demo_mapping1"].status == 1
    if not mapping1_ok:
        _emit_email("Failed_Email2", result.emails, log)
        # Control Option = Stop parent.
        result.failed = True
        return result

    if mapping1_ok:
        result.sessions["s_m_demo_mapping3"] = _run_session(
            "s_m_demo_mapping3", "m_demo_mapping3", config, spark, reader, writer, mapping_runner)
        mapping3_ok = result.sessions["s_m_demo_mapping3"].status == 1
        if mapping3_ok:
            _emit_email("SuccessEmail", result.emails, log)
        else:
            _emit_email("Failed_Email3", result.emails, log)

    result.failed = any(outcome.status == 0 for outcome in result.sessions.values())
    return result
