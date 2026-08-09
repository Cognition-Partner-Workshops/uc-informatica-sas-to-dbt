# FROZEN CONTRACT — Informatica → PySpark migration (v2 run)

This contract is settled by the migration lead. Children implement against it and MUST NOT
change it unilaterally; if something in it is wrong or impossible, stop and report to the lead.

Repo: `Cognition-Partner-Workshops/uc-informatica-sas-to-dbt`
Base of all work: `main`. Integration branch: `integration/informatica-pyspark-v2`.
Ignore every pre-existing branch (dbt attempt and the earlier PySpark attempt). Do not read,
cherry-pick, or reference them. Fresh conversion from the XML only.

## 0. Hard rules (from the migration brief)

- Do NOT modify anything under `legacy/`, `tools/`, or `baseline/`. `baseline/` is gitignored and
  regenerated with the unmodified runner; never commit it.
- `tools/parity_diff.py` runs unmodified: same keys (`tools/keys/informatica_keys.json`),
  tolerances, exit codes. Wrapping it with a new `--actual` source directory is the only allowed
  extension.
- Reproduce legacy behavior including its bugs. Operator-visible strings (ABORT messages, email
  subject/text) are byte-for-byte interfaces, typos included.
- Label everything as either RECOVERED (determined by the XML) or DECISION (legacy undefined —
  state the rejected alternative).
- Never merge into `main`. Milestone PRs target `integration/informatica-pyspark-v2`.

## 1. Project layout (frozen)

```
pyspark/informatica/
  requirements.txt                 # pinned; pandas<3 (comparator gotcha), pyspark 3.5.x
  README.md                        # how to run local + Snowflake
  informatica_pyspark/
    __init__.py
    config.py                      # RunConfig
    session.py                     # build_spark(config)
    context.py                     # MappingContext, MappingResult, AbortCheck, InformaticaAbort
    functions.py                   # Informatica expression primitives (Column-level)
    lineage.py                     # CONNECTOR-graph parser used by lineage assertions + doc gen
    targets.py                     # target instance registry: instance -> physical target, column order
    io/
      __init__.py                  # get_reader(config), get_writer(config)
      base.py                      # SourceReader / TargetWriter ABCs
      local_csv.py
      snowflake.py
    mappings/
      __init__.py                  # MAPPINGS registry: name -> run callable
      m_demo_mapping1.py
      m_demo_mapping2.py
      m_demo_mapping3.py
    workflow/
      __init__.py
      runner.py                    # wf_demo_mapping task graph + link semantics
    cli.py                         # `python -m informatica_pyspark.cli ...`
  scripts/
    run_parity.py                  # subprocess wrapper around UNMODIFIED tools/parity_diff.py
    build_comparison_table.py      # assembles docs/pyspark/conversion_comparison.md from fragments
  tests/
    conftest.py                    # shared SparkSession fixture
    test_lineage.py                # executable lineage assertions (CI gate)
    test_functions.py
    test_workflow_semantics.py     # link/decision/failure fixtures
    test_abort.py                  # abort fixture: non-zero exit AND no partial writes
docs/pyspark/
  lineage.md                       # generated field-level lineage (from CONNECTOR graph)
  conversion_comparison.md         # assembled comparison table (first-class deliverable)
  comparison/m_demo_mapping1.md    # per-mapping fragments (one per mapping child)
  comparison/m_demo_mapping2.md
  comparison/m_demo_mapping3.md
  comparison/workflow.md           # workflow/session-level rows
  decisions.md                     # DECISION log (append-only, one section per milestone)
  defects.md                       # legacy defects with XML evidence (append-only)
docs/parity/                       # parity reports produced by the comparator
snowflake/                         # milestone 5 only: proof SQL, committed and re-runnable
```

Nothing outside `pyspark/`, `docs/`, `snowflake/`, `.github/workflows/` may be added or changed.

## 2. Runtime / environment (frozen)

- Single venv at `/home/ubuntu/venvs/pyspark-informatica`, created from
  `pyspark/informatica/requirements.txt`. Pins: `pyspark==3.5.*`, `pandas<3`, `duckdb`, `pytest`,
  `snowflake-connector-python`. The SAME venv runs the baseline runner, the pipeline, and
  `tools/parity_diff.py` (pandas<3 is required by the comparator).
- Java 17 is present on the box.

## 3. Config and session (frozen)

`RunConfig` (dataclass, built from CLI args + env, no hidden globals):

- `business_date: datetime.date = date(2024, 1, 31)` — the ONLY source of SYSDATE/SYSTIMESTAMP.
  Transformation code must never call `current_date()`/`current_timestamp()`.
- `io_mode: Literal["local", "snowflake"]`
- `source_dir` (default `legacy/informatica/data`), `target_dir` (default `out/pyspark/local`)
- `source_variant: Literal["normal", "abort"]` — `abort` swaps `demo_source2.csv` for
  `legacy/informatica/data/abort/demo_source2.csv`, mirroring `--trigger-abort`.
- Snowflake block: `account, user, role, warehouse, database, source_schema, target_schema,
  baseline_schema, private_key_path`.

`build_spark(config)` sets, at minimum: `spark.sql.shuffle.partitions=1`,
`spark.sql.session.timeZone=UTC`, AQE disabled, `spark.sql.legacy.timeParserPolicy=CORRECTED`.
Deterministic output requires an explicit `orderBy` before every write — never rely on natural order.

## 4. IO abstraction (frozen)

Transformation code is IO-free. It receives DataFrames and returns DataFrames. Only the runner
touches readers/writers. Local vs. Snowflake differ ONLY by which adapter the config selects —
no `if io_mode == ...` anywhere inside `mappings/` or `functions.py`.

```python
class SourceReader(ABC):
    def read(self, logical_name: str) -> DataFrame: ...   # e.g. "demo_source2", "lkp_demo_source1", "demo_target1"

class TargetWriter(ABC):
    def write(self, target_instance: str, df: DataFrame) -> None: ...   # e.g. "demo_target1_INS"
```

- Every reader attaches an ordinal column `SRC_ORDINAL` (long, 0-based, physical file order) to
  every source it returns. It is the ONLY sanctioned mechanism for `Use Last Value` /
  `Use Any Value` tie-breaks. Uppercase, referenced through `informatica_pyspark.io.base.ORDINAL_COL`,
  and dropped before writing. Casing must survive a Snowflake round-trip — never quote it lowercase.
- Local reader: CSV, `header=true`, all columns read as STRING then cast explicitly by the mapping.
  Ordinal from a single-partition read preserving file order.
- Snowflake reader/writer: `spark-snowflake` + matching `snowflake-jdbc`, jars pinned by version and
  cached under `~/.cache/informatica-pyspark/jars` (Maven Central 429s; use a mirror if needed).
  Key-pair auth: read the PEM from `SNOWFLAKE_PRIVATE_KEY`, convert to base64 PKCS8 DER in memory.
  Never write an unencrypted intermediate into the repo; the PEM file goes outside the repo, mode 600.

## 5. Mapping module contract (frozen)

```python
# informatica_pyspark/mappings/m_demo_mappingN.py
MAPPING_NAME = "m_demo_mappingN"
SOURCES = ("demo_sourceX", ...)          # logical names the runner must read
TARGET_INSTANCES = ("demo_targetY", ...) # exact XML INSTANCE names

def run(ctx: MappingContext) -> MappingResult: ...
```

- `MappingContext`: `.spark`, `.config`, `.sources: dict[str, DataFrame]`, `.sysdate` / `.systimestamp`
  (Column literals derived from `config.business_date`), `.log`.
- `MappingResult`: `targets: dict[str, DataFrame]` (keys = XML target instance names),
  `abort_checks: list[AbortCheck]`.
- `AbortCheck(predicate_df, message)`: `message` is the ABORT string byte-for-byte from the XML.
  The runner evaluates ALL abort checks BEFORE writing ANY target. If any check yields ≥1 row it
  raises `InformaticaAbort(message)`; the process prints the message and exits non-zero, and no
  target is written (no partial writes). This is a DECISION (PowerCenter aborts mid-stream); record it.
- Aggregators, routers, lookups, sequence generators are expressed with `functions.py` primitives so
  the identical code path runs local and against Snowflake.

## 6. Naming (frozen)

- Output file / table name = the XML target INSTANCE name, verbatim: `demo_target1_INS`,
  `demo_target1_UPD`, `demo_target2`, `demo_target21`, `demo_target3`, `demo_target5`, `demo_target6`.
  Local: `<target_dir>/<instance>.csv` (header, one file per target, not a Spark part-dir).
- Output columns = the physical TARGET's `TARGETFIELD` names, exact case, in `FIELDNUMBER` order.
  `demo_target1_INS`/`demo_target1_UPD` share physical `demo_target1`; `demo_target2`/`demo_target21`
  share physical `demo_target2` (INSTANCE `TRANSFORMATION_NAME` proves it). Represent this in
  `targets.py` as one physical definition with two writer instances — record the decision.
- A column corresponding to a real Informatica port keeps that port's name. Columns synthesized
  with no XML port behind them must be uppercase and prefixed `SRC_`/`WRK_`. The runner's
  prefix-drop is a safety net, not the mechanism that guarantees the target schema; projection
  to the physical TARGET field order is what guarantees the output schema.

## 7. Business date

Pinned to 2024-01-31. `SYSDATE` and `SYSTIMESTAMP` both resolve from `config.business_date`.
The exact literal each one produces must be reconciled against `baseline/informatica/*.csv`
(regenerate with `python tools/informatica_baseline.py`), and the reconciliation stated in the
comparison table row.

## 8. Workflow semantics (RECOVERED from the XML — implement literally)

Tasks: `Start`, sessions `s_m_demo_mapping1/2/3`, decisions `Decision1/2/3`, emails
`Failed_Email1/2/3`, `SuccessEmail`, and `Control` (Control Option = `Stop parent`).
`SUSPEND_ON_ERROR="NO"`; every task instance has `FAIL_PARENT_IF_INSTANCE_FAILS="NO"`,
`FAIL_PARENT_IF_INSTANCE_DID_NOT_RUN="NO"`, `TREAT_INPUTLINK_AS_AND="YES"`.

Decision expressions: `Decision1 = $s_m_demo_mapping2.Status = 1`,
`Decision2 = $s_m_demo_mapping1.Status = 1`, `Decision3 = $s_m_demo_mapping3.Status = 1`.

Links (empty CONDITION means unconditional — implement exactly that, it is a legacy defect, not a typo):

| From | To | Condition |
|---|---|---|
| Start | s_m_demo_mapping2 | (empty) |
| s_m_demo_mapping2 | Decision1 | (empty) |
| Decision1 | Failed_Email1 | `$Decision1.Condition = 0` |
| Decision1 | s_m_demo_mapping1 | **(empty) — mapping1 runs even when mapping2 FAILED** |
| s_m_demo_mapping1 | Decision2 | (empty) |
| Decision2 | Failed_Email2 | `$Decision2.Condition = 0` |
| Decision2 | s_m_demo_mapping3 | `$Decision2.Condition = 1` |
| Failed_Email2 | Control | (empty) — Control Option `Stop parent` |
| s_m_demo_mapping3 | Decision3 | (empty) |
| Decision3 | SuccessEmail | `$Decision3.Condition = 1` |
| Decision3 | Failed_Email3 | `$Decision3.Condition = 0` |

Email payloads, byte-for-byte (all to `data-eng-alerts@example.com`):

- `Failed_Email2`: subject `Run status`, text `Sessio 's_m_demo_mapping1' failed`
- `SuccessEmail`: subject `Run Status`, text `Session s_m_demo_mapping3 executed successfully`
- `Failed_Email1`: subject `Execution Status`, text `Dataload s_m_demo_mapping2 was failed to execute`
- `Failed_Email3`: subject `Execution Status`, text `Dataload  s_m_demo_mapping3t was failed to execute`
  (two spaces after `Dataload`, trailing `t` on the session name — preserve exactly)

Emails are not sent; the runner emits them to stdout and to a run log as a stable record, and the
workflow tests assert the exact strings.

Exit code (DECISION by the lead): `run-workflow` exits non-zero if ANY session task failed, even
though `FAIL_PARENT_IF_INSTANCE_FAILS="NO"` would leave the PowerCenter workflow non-failed.
Rejected alternative: exit 0 to mirror the attribute — rejected because the migration brief requires
the ABORT path to fail the run and `tools/informatica_baseline.py --trigger-abort` exits non-zero.
`run-mapping` exits non-zero when that mapping aborts or errors. Record this in `docs/pyspark/decisions.md`.

## 9. CLI (frozen)

```
python -m informatica_pyspark.cli run-mapping <m_demo_mappingN> [--io local|snowflake] [--source-variant normal|abort] [--target-dir DIR]
python -m informatica_pyspark.cli run-workflow                  [--io local|snowflake] [--source-variant normal|abort] [--target-dir DIR]
python -m informatica_pyspark.cli lineage --out docs/pyspark/lineage.md
```

## 10. Comparison table format (frozen)

Per-mapping fragment `docs/pyspark/comparison/<mapping>.md` — a single markdown table, exactly
these columns in this order:

`| Mapping | Transformation | Port / Object | XML line | Original Informatica code (verbatim) | Converted PySpark code (file:lines + snippet) | Confidence | Reason & closing action |`

- One row per: every `TRANSFORMFIELD` with a non-empty `EXPRESSION` (89 total across the three
  mappings: mapping1 = 54, mapping2 = 20, mapping3 = 15), plus Source Qualifier SQL overrides,
  lookup conditions and policies, router group conditions, aggregator group-by/aggregate ports,
  sequence generator state, and update strategy expressions. Workflow-level rows (decision
  expressions, link conditions, email texts, control option) go in `comparison/workflow.md`.
- Original code column: verbatim from the XML (decoded entities), in backticks, with its line number.
- Confidence rubric (identical wording in every fragment; the assembled doc states it once):
  - **HIGH** — semantics unambiguous in the XML AND at least one baseline row would fail parity if
    the conversion were wrong.
  - **MEDIUM** — unambiguous but weakly exercised: the output is constant/degenerate in the seed
    data, so parity cannot catch a wrong conversion.
  - **LOW** — the conversion rests on a judgement call the XML does not determine; name the
    alternative that was rejected.
  - **NOT MIGRATED** — deliberate (e.g. dead port with no outgoing connector); name every one.
- Every non-HIGH row states specifically what a wrong conversion would look like and why the
  controls would not catch it; every MEDIUM/LOW names a closing action (what data or ruling would
  upgrade it). A fragment with zero MEDIUMs will be rejected on review.
- `scripts/build_comparison_table.py` concatenates the fragments into
  `docs/pyspark/conversion_comparison.md` and computes: total rows, migrated, not-migrated-by-design,
  confidence split, a prioritized "review these first" list, and LOW rows grouped by underlying decision.

## 11. Verification gates every milestone must pass

1. `pytest pyspark/informatica/tests` green.
2. `python tools/informatica_baseline.py` (unmodified) regenerates `baseline/informatica/`.
3. `python pyspark/informatica/scripts/run_parity.py` → unmodified `tools/parity_diff.py` exits 0
   for the targets the milestone owns.
4. Abort fixture: `run-workflow --source-variant abort` exits non-zero and writes no target file.
5. CI workflow `.github/workflows/pyspark-informatica.yml` runs 1–4 on every PR.
