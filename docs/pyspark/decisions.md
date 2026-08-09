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

## m_demo_mapping1

- **DECISION — aggregator pass-through tie-break.** The SQL override at line 580 orders
  by account but does not define intra-account order. The conversion selects the greatest
  `TX_ID` per `ACCT_ID` for the aggregator's pass-through ports. Physical `SRC_ORDINAL`
  order was rejected: it happens to choose the same seed row, so parity cannot distinguish
  the alternatives.
- **DECISION — lookup Use Last Value.** Lookup rows are ranked by maximum `SRC_ORDINAL`
  per key, preserving physical file order. First-value and arbitrary-value selection were
  rejected because the XML explicitly says Use Last Value (lines 498, 536, and 624).
- **DECISION — sequence allocation.** `ACCT_KEY` starts at 281 and uses a deterministic
  1-based `ACCT_ID` ordering over aggregated rows. Partition-natural order was rejected
  because Spark does not define it.
- **DECISION — CR8_DT rendering.** The regenerated baseline contains `2024-01-31`,
  not a timestamp string, so the pinned SYSTIMESTAMP is materialized as a DATE before
  writing. Keeping a timestamp would render `2024-01-31 00:00:00` and fail comparison.
- **RECOVERED — source typing.** String CSV inputs are cast according to XML port types:
  numeric account/transaction/customer identifiers to long, amounts to double, dates to
  date, transaction time to timestamp, and `CRDT_LN` remains string for LTRIM.

## m_demo_mapping2

- **DECISION — AES_DECRYPT representation.** The mapping calls `functions.aes_decrypt` with the
  XML arguments and receives the scaffold's `LEGACY_AES_VALUE` constant. A real AES-256 decrypt
  and NULL were rejected because the key/material are unavailable and neither can change the
  result unless it equals the target's 32-character MD5 digest exactly.
- **DECISION — Use Any Value tie-break.** Duplicate lookup IDs retain the greatest `SRC_ORDINAL`
  (the physical source order sanctioned by the contract). Choosing the highest Key happens to
  select the same row in this seed, while choosing the lowest ordinal selects Key 2 and fails
  parity.
- **DECISION — sequence assignment order.** Insert NEXTVAL values are `56 + row_number()` in
  `SRC_ORDINAL` order. An arbitrary window order or `monotonically_increasing_id` was rejected
  because it is not the physical Informatica pipeline order.
- **DECISION — ERROR defaults.** `ERROR('transformation error')` remains the milestone-0
  reject-default/NULL primitive. No expression in this mapping raises, so the defaults never
  fire.
- **DECISION — DD_UPDATE write semantics.** UPDTRANS forwards every Update-group row to the
  `demo_target1_UPD` instance; no CSV/warehouse upsert semantics are modeled.
- **DECISION — sort keys.** Both target instances use `sort_keys=("ID",)` to match the baseline
  ordering.
