# Decisions

## Milestone 0

- **DECISION — AES_DECRYPT constant.** `legacy/informatica/wf_demo_mapping.XML` line 177 uses
  `AES_DECRYPT(...)`; the unmodified `tools/informatica_baseline.py` renders the comparison side
  as `CAST('LEGACY_AES_VALUE' AS VARCHAR)` at line 202.
  The primitive returns that literal. Rejected real AES-256 decryption because the key/material
  are not recoverable and would change Insert/Update classification.
- **DECISION — NULL concatenation.** `||` treats NULL operands as empty strings. The baseline's
  DuckDB operator is NULL-propagating, but the XML-derived concatenated inputs for the real seed
  rows contain no NULLs, so the two implementations cannot produce different target values.
  Rejected NULL propagation; `tests/test_functions.py` proves the XML-derived seed inputs are
  non-NULL.
- **RECOVERED — TO_DATE/IIF.** `legacy/informatica/wf_demo_mapping.XML` line 662 mask produces
  NULL in baseline `SELL_ST_DT`;
  two-argument false `IIF` produces NULL.
- **RECOVERED — business date.** SYSDATE and SYSTIMESTAMP derive only from 2024-01-31;
  SYSTIMESTAMP is midnight timestamp and SYSDATE is a date.
- **DECISION — ERROR.** `legacy/informatica/wf_demo_mapping.XML` line 943 area uses
  `ERROR('transformation error')`.
  It returns NULL/reject-default semantics rather than Spark `raise_error`; the alternative was
  rejected because it kills the whole run.
- **RECOVERED — ABORT message.** `legacy/informatica/wf_demo_mapping.XML` line 943 contains
  `ABORT('Relationship_to_Subscriber_Code_Labe
  valuel is null')`; the typo is preserved byte-for-byte.
- **RECOVERED — DECODE primitive.** DECODE is unused in this XML but is implemented and unit-tested.
- **DECISION — workflow exit status.** Any failed session makes `run-workflow` non-zero even with
  `FAIL_PARENT_IF_INSTANCE_FAILS="NO"`, as required by CONTRACT.md.
- **DECISION — shared physical targets.** The two target-instance pairs share one physical target
  definition, based on INSTANCE `TRANSFORMATION_NAME` at XML lines 345/346 and 1009/1010.
- **DECISION — Informatica date masks.** Informatica masks are translated to Spark/Java patterns
  before `TO_DATE` and `TO_CHAR`; in particular `DD` means day-of-month, `YYYY` calendar year,
  `MI` minute, and `HH24` 24-hour time. `TO_CHAR(date)` defaults to
  `MM/DD/YYYY HH24:MI:SS`, rather than a Spark cast.
- **DECISION — target write ordering and projection.** Mapping results may provide per-instance
  `sort_keys`; the runner orders by those keys and only falls back to all projected columns when
  absent. The runner projects physical target FIELDNUMBER order and removes `SRC_`/`WRK_` helpers
  before writing, so mapping children do not own IO-specific output shaping.
