# Decisions

## Milestone 0

- **DECISION — AES_DECRYPT constant.** XML line 177 uses `AES_DECRYPT(...)`; the unmodified
  baseline renders the comparison side as `CAST('LEGACY_AES_VALUE' AS VARCHAR)` at line 202.
  The primitive returns that literal. Rejected real AES-256 decryption because the key/material
  are not recoverable and would change Insert/Update classification.
- **DECISION — NULL concatenation.** `||` treats NULL operands as empty strings. The baseline's
  DuckDB operator is NULL-propagating, but no concatenated seed input is NULL and MD5 does not
  drive classification. Rejected NULL propagation; closing action is a NULL-focused mapping test.
- **RECOVERED — TO_DATE/IIF.** The XML line 662 mask produces NULL in baseline `SELL_ST_DT`;
  two-argument false `IIF` produces NULL.
- **RECOVERED — business date.** SYSDATE and SYSTIMESTAMP derive only from 2024-01-31;
  SYSTIMESTAMP is midnight timestamp and SYSDATE is a date.
- **DECISION — ERROR.** XML default value near line 943 uses `ERROR('transformation error')`.
  It returns NULL/reject-default semantics rather than Spark `raise_error`; the alternative was
  rejected because it kills the whole run.
- **RECOVERED — ABORT message.** XML line 943 contains `ABORT('Relationship_to_Subscriber_Code_Labe
  valuel is null')`; the typo is preserved byte-for-byte.
- **RECOVERED — DECODE primitive.** DECODE is unused in this XML but is implemented and unit-tested.
- **DECISION — workflow exit status.** Any failed session makes `run-workflow` non-zero even with
  `FAIL_PARENT_IF_INSTANCE_FAILS="NO"`, as required by CONTRACT.md.
- **DECISION — shared physical targets.** The two target-instance pairs share one physical target
  definition, based on INSTANCE `TRANSFORMATION_NAME` at XML lines 345/346 and 1009/1010.
