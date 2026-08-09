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
  `TX_ID` per `ACCT_ID` for the aggregator's pass-through ports, including `TX_DTTM`.
  Physical `SRC_ORDINAL`
  order was rejected: it happens to choose the same seed row, so parity cannot distinguish
  the alternatives.
- **DECISION — lookup Use Last Value.** Lookup rows are ranked by maximum `SRC_ORDINAL`
  per key, preserving physical file order. First-value and arbitrary-value selection were
  rejected because the XML explicitly says Use Last Value (lines 498, 536, and 624).
- **RECOVERED — sequence allocation.** `ACCT_KEY` starts at 281 and uses the
  `sq_demo_source4` sorted-port order: its first sorted port is `ACCT_ID` and
  `Number Of Sorted Ports = 1` at XML line 583. Partition-natural order was
  rejected because Spark does not define it. The comparison row is HIGH: reversing
  the order changes the baseline's 281/282 assignments.
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
  result unless it equals the target's 32-character MD5 digest exactly. This governs the
  low-confidence `MD5_src` row.
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

## m_demo_mapping3

- **RECOVERED — source casts.** XML lines 907–916 define Member_ID, Member_Record_Number,
  Social_Security_Number, Member_Type_Code, and Relationship_to_Subscriber_Code as double, and
  Birth_Date and Original_Effective_Date as date/time. The implementation casts the numeric ports
  to double and the date ports to Spark `DateType`.
- **DECISION — date representation.** `DateType` is used rather than `TimestampType` for
  `Birth_Date` and `Original_Effective_Date`, although
  the XML says date/time, because the CSV writer pins `timestampFormat=yyyy-MM-dd HH:mm:ss` while
  the baseline emits bare `1990-07-12`; TimestampType would produce a false string mismatch.
  The rejected alternative is TimestampType. This is safe only because the seed data has no
  time-of-day component.
- **RECOVERED — ABORT default and interface.** XML line 943 supplies the guarded output expression
  and `ERROR('transformation error')` default. The exact typo in
  `ABORT('Relationship_to_Subscriber_Code_Labe valuel is null')` is preserved; ERROR is unreachable
  because the ABORT guard wins.
- **DECISION — abort timing.** The runner evaluates the single post-SQL abort predicate before
  writing either mapping3 target. The rejected alternative is PowerCenter's possible mid-stream
  partial write behavior. The no-partial-write guarantee is scoped to mapping3's own targets;
  the legacy runner writes mapping1 and mapping2 outputs before mapping3 aborts.
- **RECOVERED — router groups and target bindings.** XML lines 948–950 define NEWGROUP1 as
  `ISNULL(Social_Security_Number)` and NEWGROUP2 as its negation. XML connector lines 1017–1044
  determine all 14 physical target bindings, including the guarded `o_` label port.
- **DECISION — target row ordering.** Both instances use `sort_keys = ("Member_Identifier",)`.
  The rejected alternative is the runner's sort-by-all-columns fallback. `SRC_ORDINAL` cannot be
  used because the runner drops helper columns before ordering.

## Milestone 4

- **RECOVERED — shared lookup duplicate resolution.** XML lookup policies at lines
  498, 536, and 624 are `Use Last Value`; line 285 is `Use Any Value`. Both
  resolve to the greatest physical `SRC_ORDINAL` in the shared `functions.last_value`
  primitive. The `Use Any Value` interpretation remains LOW confidence because the
  XML does not define which duplicate is selected; choosing the first ordinal was
  rejected because the seed lookup would select a different Key and fail parity.
- **RECOVERED — Source Qualifier ordering rule.** A Source Qualifier with
  `Number Of Sorted Ports > 0` orders downstream rows by its declared sorted ports;
  otherwise physical `SRC_ORDINAL` is retained. XML line 583 gives
  `sq_demo_source4` one sorted port (`ACCT_ID`), while line 154 gives
  `SQ_demo_source1` zero sorted ports. Existing sequence behavior is unchanged.
- **RECOVERED — source typing agreement.** The three mappings follow their Source
  Qualifier port datatypes. In particular, mapping2's SQ ports are strings except
  for the explicit lookup Key conversion, and mapping1's source5 ports pass through
  as strings. The emitted `demo_target3.PRODUCT_ID` therefore remains a string
  despite the physical target's XML `number` declaration; adding a cast would alter
  `PRD0001` and break the recovered behavior.
- **DECISION — Use Any Value remains LOW.** The shared primitive makes the
  `Use Any Value` case deterministic by physical ordinal. A PowerCenter runtime
  fixture with duplicate lookup rows and a discriminating result would be needed
  to upgrade this confidence.
- **DECISION — workflow process status.** `workflow_exit_code` is the single
  implementation of CONTRACT §8: any failed session returns process status 1,
  including when Control stops the parent. Mirroring the workflow's
  `FAIL_PARENT_IF_INSTANCE_FAILS="NO"` and returning 0 was rejected.
- **DECISION — workflow abort scope.** The session-level no-partial-write rule
  applies to the aborting mapping's targets. At workflow level, completed earlier
  sessions retain their outputs before the later mapping aborts; deleting those
  outputs would contradict the recovered runner behavior and the baseline abort
  fixture.
- **DECISION — helper-column names.** Mapping2 and mapping3 retain Informatica
  port names such as `New_Flag`, `MD5_src`, and
  `o_Relationship_to_Subscriber_Code_Label` to preserve lineage. These are real
  XML ports, not synthesized helpers, and are projected away before writes.
- **DECISION — mapping1 target5 sort keys.** `demo_target5` uses `("ACCT_ID",)` like
  the other targets. Its two output rows have distinct `ACCT_ID` values (1003 and
  1004), so dropping `BAL_AMT` is not load-bearing and preserves the output bytes.
- **RECOVERED — task traversal recording.** Workflow results now record the
  ordered task instances actually executed, including `Control` on the
  `Failed_Email2 → Control` stop-parent path. This makes the early return
  observable without changing its semantics.
