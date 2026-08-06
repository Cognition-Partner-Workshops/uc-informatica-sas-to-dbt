# Snowflake verification evidence

This document is self-contained evidence for the Snowflake migration run in
`DBT_INFORMATICA_RUN20260806` and the type-matched baseline in
`BASELINE_INFORMATICA_RUN20260806`. The raw command transcripts are also
committed under `docs/evidence/raw/` and are unedited copies of the final
script output.

## Environment and decisions

The comparator ran with `/home/ubuntu/venv-dbt/bin/python` (Python 3.12.8,
pandas 2.3.3). **DECISION:** pandas `<3` is an environment requirement of the
unmodified comparator because pandas 3 mis-normalizes an all-NULL DATE column;
it is not a modeling constraint and no comparator code was changed.

**DECISION:** `load_baseline_snowflake.py` derives baseline types from the
matching migrated table's `INFORMATION_SCHEMA.COLUMNS`, preserving migrated
ordinal order. The loader also asserts the CSV header sequence matches that
sequence case-insensitively. Rejected alternative: inferring types or loading
by position after silently accepting a different header order.

**DECISION:** Empty fields use the exact executed Snowflake file format
`NULL_IF=('')` and `EMPTY_FIELD_AS_NULL=TRUE`. Rejected alternative: loading
empty strings and normalizing them later.

**DECISION:** The Snowflake comparator report is
`docs/parity/informatica_parity_snowflake.md`; the existing DuckDB report was
not overwritten. Rejected alternative: reusing
`docs/parity/informatica_parity.md`.

**DECISION:** No rounded second MINUS was run. All exact MINUS queries returned
zero rows, so no stored value was rounded and no comparison query needed the
floating-point fallback.

**DECISION:** Query history uses `INFORMATION_SCHEMA.QUERY_HISTORY` for
immediate session-local evidence. Rejected alternative:
`ACCOUNT_USAGE.QUERY_HISTORY`, which may be delayed or permission-limited.

The verifier was invoked with the explicit flag matching the pasted SQL:

```text
python dbt/informatica/scripts/verify_snowflake.py --migrated-schema DBT_INFORMATICA_RUN20260806 --baseline-schema BASELINE_INFORMATICA_RUN20260806 --history-hours 6
```

## Model execution breakdown

Snowflake executed 31 warehouse models unmodified: 7 table models and 24
view models. Fixed models: 0. Snowflake SQL rejection errors: 0.
`int_m3__abort_fixture` is intentionally ephemeral and creates no warehouse
object in a normal build. The initial unactivated-venv adapter import failure
was an operator invocation error, not a Snowflake rejection.

## Baseline loader output

The final loader invocation was:

```text
python dbt/informatica/scripts/load_baseline_snowflake.py BASELINE_INFORMATICA_RUN20260806 --migrated-schema DBT_INFORMATICA_RUN20260806
```

The complete final output is committed in
`docs/evidence/raw/snowflake_baseline_load.txt`. These are real lines from
that transcript:

```text
COPY INTO "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET1_INS" FROM @%"DEMO_TARGET1_INS" FILE_FORMAT=(TYPE=CSV SKIP_HEADER=1 FIELD_OPTIONALLY_ENCLOSED_BY='"' NULL_IF=('') EMPTY_FIELD_AS_NULL=TRUE) PURGE=TRUE ON_ERROR='ABORT_STATEMENT'
NULL_VERIFICATION target=demo_target1_INS column=UPDATED_BY source_row=2
LOADED target=demo_target1_INS source=/home/ubuntu/repos/uc-informatica-sas-to-dbt/baseline/informatica/demo_target1_INS.csv
COPY INTO "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET1_UPD" FROM @%"DEMO_TARGET1_UPD" FILE_FORMAT=(TYPE=CSV SKIP_HEADER=1 FIELD_OPTIONALLY_ENCLOSED_BY='"' NULL_IF=('') EMPTY_FIELD_AS_NULL=TRUE) PURGE=TRUE ON_ERROR='ABORT_STATEMENT'
NULL_VERIFICATION target=demo_target1_UPD column=CREATED_BY source_row=2
LOADED target=demo_target1_UPD source=/home/ubuntu/repos/uc-informatica-sas-to-dbt/baseline/informatica/demo_target1_UPD.csv
COPY INTO "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET2" FROM @%"DEMO_TARGET2" FILE_FORMAT=(TYPE=CSV SKIP_HEADER=1 FIELD_OPTIONALLY_ENCLOSED_BY='"' NULL_IF=('') EMPTY_FIELD_AS_NULL=TRUE) PURGE=TRUE ON_ERROR='ABORT_STATEMENT'
NULL_VERIFICATION target=demo_target2 column=Soc_Number source_row=2
LOADED target=demo_target2 source=/home/ubuntu/repos/uc-informatica-sas-to-dbt/baseline/informatica/demo_target2.csv
COPY INTO "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET21" FROM @%"DEMO_TARGET21" FILE_FORMAT=(TYPE=CSV SKIP_HEADER=1 FIELD_OPTIONALLY_ENCLOSED_BY='"' NULL_IF=('') EMPTY_FIELD_AS_NULL=TRUE) PURGE=TRUE ON_ERROR='ABORT_STATEMENT'
NULL_VERIFICATION target=demo_target21 column=Member_Suffix source_row=2
LOADED target=demo_target21 source=/home/ubuntu/repos/uc-informatica-sas-to-dbt/baseline/informatica/demo_target21.csv
COPY INTO "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET3" FROM @%"DEMO_TARGET3" FILE_FORMAT=(TYPE=CSV SKIP_HEADER=1 FIELD_OPTIONALLY_ENCLOSED_BY='"' NULL_IF=('') EMPTY_FIELD_AS_NULL=TRUE) PURGE=TRUE ON_ERROR='ABORT_STATEMENT'
NULL_VERIFICATION target=demo_target3 column=SELL_ST_DT source_row=2
LOADED target=demo_target3 source=/home/ubuntu/repos/uc-informatica-sas-to-dbt/baseline/informatica/demo_target3.csv
COPY INTO "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET5" FROM @%"DEMO_TARGET5" FILE_FORMAT=(TYPE=CSV SKIP_HEADER=1 FIELD_OPTIONALLY_ENCLOSED_BY='"' NULL_IF=('') EMPTY_FIELD_AS_NULL=TRUE) PURGE=TRUE ON_ERROR='ABORT_STATEMENT'
LOADED target=demo_target5 source=/home/ubuntu/repos/uc-informatica-sas-to-dbt/baseline/informatica/demo_target5.csv
COPY INTO "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET6" FROM @%"DEMO_TARGET6" FILE_FORMAT=(TYPE=CSV SKIP_HEADER=1 FIELD_OPTIONALLY_ENCLOSED_BY='"' NULL_IF=('') EMPTY_FIELD_AS_NULL=TRUE) PURGE=TRUE ON_ERROR='ABORT_STATEMENT'
NULL_VERIFICATION target=demo_target6 column=CLSR_DT source_row=3
LOADED target=demo_target6 source=/home/ubuntu/repos/uc-informatica-sas-to-dbt/baseline/informatica/demo_target6.csv
```

## Created objects: full query and output

The verifier emitted:

```sql
SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA IN ('BASELINE_INFORMATICA_RUN20260806', 'DBT_INFORMATICA_RUN20260806')
ORDER BY TABLE_SCHEMA, TABLE_NAME
```

Full real output for both schemas:

```text
OBJECT_VERIFICATION

SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA IN ('BASELINE_INFORMATICA_RUN20260806', 'DBT_INFORMATICA_RUN20260806')
ORDER BY TABLE_SCHEMA, TABLE_NAME

('BASELINE_INFORMATICA_RUN20260806', 'DEMO_TARGET1_INS', 'BASE TABLE')
('BASELINE_INFORMATICA_RUN20260806', 'DEMO_TARGET1_UPD', 'BASE TABLE')
('BASELINE_INFORMATICA_RUN20260806', 'DEMO_TARGET2', 'BASE TABLE')
('BASELINE_INFORMATICA_RUN20260806', 'DEMO_TARGET21', 'BASE TABLE')
('BASELINE_INFORMATICA_RUN20260806', 'DEMO_TARGET3', 'BASE TABLE')
('BASELINE_INFORMATICA_RUN20260806', 'DEMO_TARGET5', 'BASE TABLE')
('BASELINE_INFORMATICA_RUN20260806', 'DEMO_TARGET6', 'BASE TABLE')
('DBT_INFORMATICA_RUN20260806', 'DEMO_SOURCE1', 'BASE TABLE')
('DBT_INFORMATICA_RUN20260806', 'DEMO_SOURCE2', 'BASE TABLE')
('DBT_INFORMATICA_RUN20260806', 'DEMO_SOURCE3', 'BASE TABLE')
('DBT_INFORMATICA_RUN20260806', 'DEMO_SOURCE4', 'BASE TABLE')
('DBT_INFORMATICA_RUN20260806', 'DEMO_SOURCE5', 'BASE TABLE')
('DBT_INFORMATICA_RUN20260806', 'DEMO_TARGET1', 'BASE TABLE')
('DBT_INFORMATICA_RUN20260806', 'DEMO_TARGET1_INS', 'BASE TABLE')
('DBT_INFORMATICA_RUN20260806', 'DEMO_TARGET1_UPD', 'BASE TABLE')
('DBT_INFORMATICA_RUN20260806', 'DEMO_TARGET2', 'BASE TABLE')
('DBT_INFORMATICA_RUN20260806', 'DEMO_TARGET21', 'BASE TABLE')
('DBT_INFORMATICA_RUN20260806', 'DEMO_TARGET3', 'BASE TABLE')
('DBT_INFORMATICA_RUN20260806', 'DEMO_TARGET5', 'BASE TABLE')
('DBT_INFORMATICA_RUN20260806', 'DEMO_TARGET6', 'BASE TABLE')
('DBT_INFORMATICA_RUN20260806', 'INT_M1__AGG_TRANS', 'VIEW')
('DBT_INFORMATICA_RUN20260806', 'INT_M1__EXP_TRANS', 'VIEW')
('DBT_INFORMATICA_RUN20260806', 'INT_M1__EXP_TRANS1', 'VIEW')
('DBT_INFORMATICA_RUN20260806', 'INT_M1__EXP_TRANS2', 'VIEW')
('DBT_INFORMATICA_RUN20260806', 'INT_M1__RTR_TRANS_DEMO_TARGET5_GRP', 'VIEW')
('DBT_INFORMATICA_RUN20260806', 'INT_M1__RTR_TRANS_DEMO_TARGET6_GRP', 'VIEW')
('DBT_INFORMATICA_RUN20260806', 'INT_M1__SQ_DEMO_SOURCE4', 'VIEW')
('DBT_INFORMATICA_RUN20260806', 'INT_M2__EXPTRANS', 'VIEW')
('DBT_INFORMATICA_RUN20260806', 'INT_M2__RTR_INSERT', 'VIEW')
('DBT_INFORMATICA_RUN20260806', 'INT_M2__RTR_UPD', 'VIEW')
('DBT_INFORMATICA_RUN20260806', 'INT_M2__UPDTRANS', 'VIEW')
('DBT_INFORMATICA_RUN20260806', 'INT_M3__EXPTRANS', 'VIEW')
('DBT_INFORMATICA_RUN20260806', 'INT_M3__RTR_NEWGROUP1', 'VIEW')
('DBT_INFORMATICA_RUN20260806', 'INT_M3__RTR_NEWGROUP2', 'VIEW')
('DBT_INFORMATICA_RUN20260806', 'INT_M3__SQ_DEMO_SOURCE2', 'VIEW')
('DBT_INFORMATICA_RUN20260806', 'LKP_DEMO_SOURCE1', 'BASE TABLE')
('DBT_INFORMATICA_RUN20260806', 'LKP_DEMO_SOURCE2', 'BASE TABLE')
('DBT_INFORMATICA_RUN20260806', 'LKP_DEMO_SOURCE3', 'BASE TABLE')
('DBT_INFORMATICA_RUN20260806', 'STG_DEMO_SOURCE1', 'VIEW')
('DBT_INFORMATICA_RUN20260806', 'STG_DEMO_SOURCE2', 'VIEW')
('DBT_INFORMATICA_RUN20260806', 'STG_DEMO_SOURCE3', 'VIEW')
('DBT_INFORMATICA_RUN20260806', 'STG_DEMO_SOURCE4', 'VIEW')
('DBT_INFORMATICA_RUN20260806', 'STG_DEMO_SOURCE5', 'VIEW')
('DBT_INFORMATICA_RUN20260806', 'STG_DEMO_TARGET1', 'VIEW')
('DBT_INFORMATICA_RUN20260806', 'STG_LKP_DEMO_SOURCE1', 'VIEW')
('DBT_INFORMATICA_RUN20260806', 'STG_LKP_DEMO_SOURCE2', 'VIEW')
('DBT_INFORMATICA_RUN20260806', 'STG_LKP_DEMO_SOURCE3', 'VIEW')
```

## Samples, counts, and all exact MINUS queries

The following is the verifier's complete real output for all seven targets.
Every sample uses an explicit column list. Every count is side-by-side, and
all 14 exact MINUS queries are shown with their actual `(0 rows)` result.

```text
SAMPLE target=demo_target1_INS
SELECT "KEY", "LEAD_CO_MNE", "BRANCH_CO_MNE", "MIS_DATE", "ID", "DESCRIPTION", "SHORT_NAME", "CREATED_BY", "CREATED_TIME", "UPDATED_BY", "UPDATED_TIME", "ACTIVE_FLAG", "START_DATE", "END_DATE" FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET1_INS" LIMIT 3
(57, 'BNK04', 'BR104', '2024-01-31', 'REC00004', 'General ledger account 4', 'GL0004', 'IDWUSER', datetime.datetime(2024, 1, 31, 0, 0), None, None, None, None, None)
(58, 'BNK05', 'BR105', '2024-01-31', 'REC00005', 'General ledger account 5', 'GL0005', 'IDWUSER', datetime.datetime(2024, 1, 31, 0, 0), None, None, None, None, None)
(59, 'BNK06', 'BR106', '2024-01-31', 'REC00006', 'General ledger account 6', 'GL0006', 'IDWUSER', datetime.datetime(2024, 1, 31, 0, 0), None, None, None, None, None)
ROW_COUNTS target=demo_target1_INS

SELECT 'BASELINE' AS SOURCE, COUNT(*) AS ROW_COUNT FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET1_INS"
UNION ALL
SELECT 'MIGRATED' AS SOURCE, COUNT(*) AS ROW_COUNT FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET1_INS"
ORDER BY SOURCE

('BASELINE', 4)
('MIGRATED', 4)
EXACT_MINUS baseline_to_migrated target=demo_target1_INS
SELECT "KEY", "LEAD_CO_MNE", "BRANCH_CO_MNE", "MIS_DATE", "ID", "DESCRIPTION", "SHORT_NAME", "CREATED_BY", "CREATED_TIME", "UPDATED_BY", "UPDATED_TIME", "ACTIVE_FLAG", "START_DATE", "END_DATE" FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET1_INS" MINUS SELECT "KEY", "LEAD_CO_MNE", "BRANCH_CO_MNE", "MIS_DATE", "ID", "DESCRIPTION", "SHORT_NAME", "CREATED_BY", "CREATED_TIME", "UPDATED_BY", "UPDATED_TIME", "ACTIVE_FLAG", "START_DATE", "END_DATE" FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET1_INS"
(0 rows)
EXACT_MINUS migrated_to_baseline target=demo_target1_INS
SELECT "KEY", "LEAD_CO_MNE", "BRANCH_CO_MNE", "MIS_DATE", "ID", "DESCRIPTION", "SHORT_NAME", "CREATED_BY", "CREATED_TIME", "UPDATED_BY", "UPDATED_TIME", "ACTIVE_FLAG", "START_DATE", "END_DATE" FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET1_INS" MINUS SELECT "KEY", "LEAD_CO_MNE", "BRANCH_CO_MNE", "MIS_DATE", "ID", "DESCRIPTION", "SHORT_NAME", "CREATED_BY", "CREATED_TIME", "UPDATED_BY", "UPDATED_TIME", "ACTIVE_FLAG", "START_DATE", "END_DATE" FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET1_INS"
(0 rows)
SAMPLE target=demo_target1_UPD
SELECT "KEY", "LEAD_CO_MNE", "BRANCH_CO_MNE", "MIS_DATE", "ID", "DESCRIPTION", "SHORT_NAME", "CREATED_BY", "CREATED_TIME", "UPDATED_BY", "UPDATED_TIME", "ACTIVE_FLAG", "START_DATE", "END_DATE" FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET1_UPD" LIMIT 3
(1.0, 'BNK01', 'BR101', '2024-01-31', 'REC00001', 'General ledger account 1', 'GL0001', None, None, 'IDWUSER', datetime.datetime(2024, 1, 31, 0, 0), None, None, None)
(99.0, 'BNK02', 'BR102', '2024-01-31', 'REC00002', 'General ledger account 2', 'GL0002', None, None, 'IDWUSER', datetime.datetime(2024, 1, 31, 0, 0), None, None, None)
(3.0, 'BNK03', 'BR103', '2024-01-31', 'REC00003', 'General ledger account 3', 'GL0003', None, None, 'IDWUSER', datetime.datetime(2024, 1, 31, 0, 0), None, None, None)
ROW_COUNTS target=demo_target1_UPD

SELECT 'BASELINE' AS SOURCE, COUNT(*) AS ROW_COUNT FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET1_UPD"
UNION ALL
SELECT 'MIGRATED' AS SOURCE, COUNT(*) AS ROW_COUNT FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET1_UPD"
ORDER BY SOURCE

('BASELINE', 3)
('MIGRATED', 3)
EXACT_MINUS baseline_to_migrated target=demo_target1_UPD
SELECT "KEY", "LEAD_CO_MNE", "BRANCH_CO_MNE", "MIS_DATE", "ID", "DESCRIPTION", "SHORT_NAME", "CREATED_BY", "CREATED_TIME", "UPDATED_BY", "UPDATED_TIME", "ACTIVE_FLAG", "START_DATE", "END_DATE" FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET1_UPD" MINUS SELECT "KEY", "LEAD_CO_MNE", "BRANCH_CO_MNE", "MIS_DATE", "ID", "DESCRIPTION", "SHORT_NAME", "CREATED_BY", "CREATED_TIME", "UPDATED_BY", "UPDATED_TIME", "ACTIVE_FLAG", "START_DATE", "END_DATE" FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET1_UPD"
(0 rows)
EXACT_MINUS migrated_to_baseline target=demo_target1_UPD
SELECT "KEY", "LEAD_CO_MNE", "BRANCH_CO_MNE", "MIS_DATE", "ID", "DESCRIPTION", "SHORT_NAME", "CREATED_BY", "CREATED_TIME", "UPDATED_BY", "UPDATED_TIME", "ACTIVE_FLAG", "START_DATE", "END_DATE" FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET1_UPD" MINUS SELECT "KEY", "LEAD_CO_MNE", "BRANCH_CO_MNE", "MIS_DATE", "ID", "DESCRIPTION", "SHORT_NAME", "CREATED_BY", "CREATED_TIME", "UPDATED_BY", "UPDATED_TIME", "ACTIVE_FLAG", "START_DATE", "END_DATE" FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET1_UPD"
(0 rows)
SAMPLE target=demo_target2
SELECT "TITLE", "GENDER", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "MEMBER_IDENTIFIER", "MEMBER_SUFFIX", "DATE_OF_BIRTH", "MEMBER_NUMBER", "SOC_NUMBER", "TYPE_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE_LABEL", "EFFECTIVE_DATE" FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET2" LIMIT 3
('MS', 'M', 'Eli', 'R', 'Baker', 30001.0, 'II', datetime.datetime(1990, 7, 12, 0, 0), 500000.0, None, 1.0, 2.0, 'CHILD', datetime.datetime(2022, 5, 1, 0, 0))
('MS', 'M', 'Omar', 'I', 'Novak', 30003.0, None, datetime.datetime(1998, 4, 3, 0, 0), 500002.0, None, 2.0, 18.0, 'CHILD', datetime.datetime(2016, 5, 1, 0, 0))
('MR', 'M', 'Nico', 'T', 'Singh', 30007.0, None, datetime.datetime(1992, 9, 30, 0, 0), 500006.0, None, 2.0, 19.0, 'SELF', datetime.datetime(2023, 2, 14, 0, 0))
ROW_COUNTS target=demo_target2

SELECT 'BASELINE' AS SOURCE, COUNT(*) AS ROW_COUNT FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET2"
UNION ALL
SELECT 'MIGRATED' AS SOURCE, COUNT(*) AS ROW_COUNT FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET2"
ORDER BY SOURCE

('BASELINE', 3)
('MIGRATED', 3)
EXACT_MINUS baseline_to_migrated target=demo_target2
SELECT "TITLE", "GENDER", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "MEMBER_IDENTIFIER", "MEMBER_SUFFIX", "DATE_OF_BIRTH", "MEMBER_NUMBER", "SOC_NUMBER", "TYPE_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE_LABEL", "EFFECTIVE_DATE" FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET2" MINUS SELECT "TITLE", "GENDER", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "MEMBER_IDENTIFIER", "MEMBER_SUFFIX", "DATE_OF_BIRTH", "MEMBER_NUMBER", "SOC_NUMBER", "TYPE_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE_LABEL", "EFFECTIVE_DATE" FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET2"
(0 rows)
EXACT_MINUS migrated_to_baseline target=demo_target2
SELECT "TITLE", "GENDER", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "MEMBER_IDENTIFIER", "MEMBER_SUFFIX", "DATE_OF_BIRTH", "MEMBER_NUMBER", "SOC_NUMBER", "TYPE_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE_LABEL", "EFFECTIVE_DATE" FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET2" MINUS SELECT "TITLE", "GENDER", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "MEMBER_IDENTIFIER", "MEMBER_SUFFIX", "DATE_OF_BIRTH", "MEMBER_NUMBER", "SOC_NUMBER", "TYPE_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE_LABEL", "EFFECTIVE_DATE" FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET2"
(0 rows)
SAMPLE target=demo_target21
SELECT "TITLE", "GENDER", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "MEMBER_IDENTIFIER", "MEMBER_SUFFIX", "DATE_OF_BIRTH", "MEMBER_NUMBER", "SOC_NUMBER", "TYPE_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE_LABEL", "EFFECTIVE_DATE" FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET21" LIMIT 3
('MR', 'F', 'Omar', 'K', 'Okafor', 30002.0, None, datetime.datetime(1990, 11, 16, 0, 0), 500001.0, 100000037.0, 2.0, 19.0, 'SELF', datetime.datetime(2016, 9, 1, 0, 0))
('MS', 'F', 'Ravi', 'O', 'Weiss', 30004.0, None, datetime.datetime(1948, 12, 22, 0, 0), 500003.0, 100000111.0, 2.0, 18.0, 'OTHER', datetime.datetime(2019, 2, 1, 0, 0))
('MS', 'F', 'Tara', 'S', 'Young', 30006.0, None, datetime.datetime(1982, 11, 1, 0, 0), 500005.0, 100000222.0, 1.0, 1.0, 'SPOUSE', datetime.datetime(2021, 7, 1, 0, 0))
ROW_COUNTS target=demo_target21

SELECT 'BASELINE' AS SOURCE, COUNT(*) AS ROW_COUNT FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET21"
UNION ALL
SELECT 'MIGRATED' AS SOURCE, COUNT(*) AS ROW_COUNT FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET21"
ORDER BY SOURCE

('BASELINE', 3)
('MIGRATED', 3)
EXACT_MINUS baseline_to_migrated target=demo_target21
SELECT "TITLE", "GENDER", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "MEMBER_IDENTIFIER", "MEMBER_SUFFIX", "DATE_OF_BIRTH", "MEMBER_NUMBER", "SOC_NUMBER", "TYPE_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE_LABEL", "EFFECTIVE_DATE" FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET21" MINUS SELECT "TITLE", "GENDER", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "MEMBER_IDENTIFIER", "MEMBER_SUFFIX", "DATE_OF_BIRTH", "MEMBER_NUMBER", "SOC_NUMBER", "TYPE_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE_LABEL", "EFFECTIVE_DATE" FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET21"
(0 rows)
EXACT_MINUS migrated_to_baseline target=demo_target21
SELECT "TITLE", "GENDER", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "MEMBER_IDENTIFIER", "MEMBER_SUFFIX", "DATE_OF_BIRTH", "MEMBER_NUMBER", "SOC_NUMBER", "TYPE_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE_LABEL", "EFFECTIVE_DATE" FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET21" MINUS SELECT "TITLE", "GENDER", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "MEMBER_IDENTIFIER", "MEMBER_SUFFIX", "DATE_OF_BIRTH", "MEMBER_NUMBER", "SOC_NUMBER", "TYPE_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE_LABEL", "EFFECTIVE_DATE" FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET21"
(0 rows)
SAMPLE target=demo_target3
SELECT "PRODUCT_ID", "PRODUCT_NM", "PRODUCT_NO", "COLOR", "STD_COST", "LIST_PRICE", "SELL_ST_DT", "SELL_ED_DT" FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET3" LIMIT 3
('PRD0001', 'Card Product 001', 'P001', 'Black', '186', '783', None, datetime.date(2024, 7, 17))
('PRD0002', 'Card Product 002', 'P002', 'Black', '908', '737', None, datetime.date(2025, 9, 28))
('PRD0003', 'Card Product 003', 'P003', 'Blue', '161', '351', None, datetime.date(2025, 8, 23))
ROW_COUNTS target=demo_target3

SELECT 'BASELINE' AS SOURCE, COUNT(*) AS ROW_COUNT FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET3"
UNION ALL
SELECT 'MIGRATED' AS SOURCE, COUNT(*) AS ROW_COUNT FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET3"
ORDER BY SOURCE

('BASELINE', 4)
('MIGRATED', 4)
EXACT_MINUS baseline_to_migrated target=demo_target3
SELECT "PRODUCT_ID", "PRODUCT_NM", "PRODUCT_NO", "COLOR", "STD_COST", "LIST_PRICE", "SELL_ST_DT", "SELL_ED_DT" FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET3" MINUS SELECT "PRODUCT_ID", "PRODUCT_NM", "PRODUCT_NO", "COLOR", "STD_COST", "LIST_PRICE", "SELL_ST_DT", "SELL_ED_DT" FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET3"
(0 rows)
EXACT_MINUS migrated_to_baseline target=demo_target3
SELECT "PRODUCT_ID", "PRODUCT_NM", "PRODUCT_NO", "COLOR", "STD_COST", "LIST_PRICE", "SELL_ST_DT", "SELL_ED_DT" FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET3" MINUS SELECT "PRODUCT_ID", "PRODUCT_NM", "PRODUCT_NO", "COLOR", "STD_COST", "LIST_PRICE", "SELL_ST_DT", "SELL_ED_DT" FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET3"
(0 rows)
SAMPLE target=demo_target5
SELECT "ACCT_ID", "FIRST_NM", "LAST_NM", "BAL_AMT", "CRDT_SCORE" FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET5" LIMIT 3
(1003, 'IVY', 'COSTA', 86284.15, 677)
(1004, 'AVA', 'PATEL', 72185.35, 626)
ROW_COUNTS target=demo_target5

SELECT 'BASELINE' AS SOURCE, COUNT(*) AS ROW_COUNT FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET5"
UNION ALL
SELECT 'MIGRATED' AS SOURCE, COUNT(*) AS ROW_COUNT FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET5"
ORDER BY SOURCE

('BASELINE', 2)
('MIGRATED', 2)
EXACT_MINUS baseline_to_migrated target=demo_target5
SELECT "ACCT_ID", "FIRST_NM", "LAST_NM", "BAL_AMT", "CRDT_SCORE" FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET5" MINUS SELECT "ACCT_ID", "FIRST_NM", "LAST_NM", "BAL_AMT", "CRDT_SCORE" FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET5"
(0 rows)
EXACT_MINUS migrated_to_baseline target=demo_target5
SELECT "ACCT_ID", "FIRST_NM", "LAST_NM", "BAL_AMT", "CRDT_SCORE" FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET5" MINUS SELECT "ACCT_ID", "FIRST_NM", "LAST_NM", "BAL_AMT", "CRDT_SCORE" FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET5"
(0 rows)
SAMPLE target=demo_target6
SELECT "ACCT_ID", "ACCT_TYP", "ACCT_DESC", "CR8_DT", "CRDT_LN", "CLSR_DT", "ACCT_STAT_CD", "TX_ID", "ACCT_KEY", "TX_DTTM", "TX_AMT", "TX_TYPE_CD" FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET6" LIMIT 3
(1001, 'SB', 'Account 1001 ledger', datetime.datetime(2024, 1, 31, 0, 0), '8000', datetime.date(2025, 6, 30), 'A', 5002, 281, datetime.datetime(2024, 1, 15, 11, 0), 2031.2399999999998, 'DR')
(1002, 'SB', 'Account 1002 ledger', datetime.datetime(2024, 1, 31, 0, 0), '48000', None, 'D', 5003, 282, datetime.datetime(2024, 1, 14, 5, 49), -1238.81, 'DR')
ROW_COUNTS target=demo_target6

SELECT 'BASELINE' AS SOURCE, COUNT(*) AS ROW_COUNT FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET6"
UNION ALL
SELECT 'MIGRATED' AS SOURCE, COUNT(*) AS ROW_COUNT FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET6"
ORDER BY SOURCE

('BASELINE', 2)
('MIGRATED', 2)
EXACT_MINUS baseline_to_migrated target=demo_target6
SELECT "ACCT_ID", "ACCT_TYP", "ACCT_DESC", "CR8_DT", "CRDT_LN", "CLSR_DT", "ACCT_STAT_CD", "TX_ID", "ACCT_KEY", "TX_DTTM", "TX_AMT", "TX_TYPE_CD" FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET6" MINUS SELECT "ACCT_ID", "ACCT_TYP", "ACCT_DESC", "CR8_DT", "CRDT_LN", "CLSR_DT", "ACCT_STAT_CD", "TX_ID", "ACCT_KEY", "TX_DTTM", "TX_AMT", "TX_TYPE_CD" FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET6"
(0 rows)
EXACT_MINUS migrated_to_baseline target=demo_target6
SELECT "ACCT_ID", "ACCT_TYP", "ACCT_DESC", "CR8_DT", "CRDT_LN", "CLSR_DT", "ACCT_STAT_CD", "TX_ID", "ACCT_KEY", "TX_DTTM", "TX_AMT", "TX_TYPE_CD" FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET6" MINUS SELECT "ACCT_ID", "ACCT_TYP", "ACCT_DESC", "CR8_DT", "CRDT_LN", "CLSR_DT", "ACCT_STAT_CD", "TX_ID", "ACCT_KEY", "TX_DTTM", "TX_AMT", "TX_TYPE_CD" FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET6"
(0 rows)
```

## Comparator output and generated report

The final wrapper output and exit code were:

```text
# Parity Report

Baseline: `/home/ubuntu/repos/uc-informatica-sas-to-dbt/baseline/informatica`  |  Actual: `/home/ubuntu/evidence/snowflake_actual`

## DEMO_TARGET1_INS
- rows: baseline=4 actual=4
- columns compared: 14
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET1_UPD
- rows: baseline=3 actual=3
- columns compared: 14
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET2
- rows: baseline=3 actual=3
- columns compared: 14
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET21
- rows: baseline=3 actual=3
- columns compared: 14
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET3
- rows: baseline=4 actual=4
- columns compared: 8
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET5
- rows: baseline=2 actual=2
- columns compared: 5
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET6
- rows: baseline=2 actual=2
- columns compared: 12
- result: **MATCH** (all values within tolerance)

**Overall: PARITY VERIFIED**
SELECT * FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET1_INS"
EXPORTED demo_target1_INS rows=4 path=/home/ubuntu/evidence/snowflake_actual/demo_target1_INS.csv
SELECT * FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET1_UPD"
EXPORTED demo_target1_UPD rows=3 path=/home/ubuntu/evidence/snowflake_actual/demo_target1_UPD.csv
SELECT * FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET2"
EXPORTED demo_target2 rows=3 path=/home/ubuntu/evidence/snowflake_actual/demo_target2.csv
SELECT * FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET21"
EXPORTED demo_target21 rows=3 path=/home/ubuntu/evidence/snowflake_actual/demo_target21.csv
SELECT * FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET3"
EXPORTED demo_target3 rows=4 path=/home/ubuntu/evidence/snowflake_actual/demo_target3.csv
SELECT * FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET5"
EXPORTED demo_target5 rows=2 path=/home/ubuntu/evidence/snowflake_actual/demo_target5.csv
SELECT * FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET6"
EXPORTED demo_target6 rows=2 path=/home/ubuntu/evidence/snowflake_actual/demo_target6.csv
RUN_COMPARATOR /home/ubuntu/venv-dbt/bin/python /home/ubuntu/repos/uc-informatica-sas-to-dbt/tools/parity_diff.py --baseline /home/ubuntu/repos/uc-informatica-sas-to-dbt/baseline/informatica --actual /home/ubuntu/evidence/snowflake_actual --keys /home/ubuntu/repos/uc-informatica-sas-to-dbt/tools/keys/informatica_keys.json --report docs/parity/informatica_parity_snowflake.md
COMPARATOR_EXIT_CODE 0
```

The complete generated report content was:

```markdown
# Parity Report

Baseline: `/home/ubuntu/repos/uc-informatica-sas-to-dbt/baseline/informatica`  |  Actual: `/home/ubuntu/evidence/snowflake_actual`

## DEMO_TARGET1_INS
- rows: baseline=4 actual=4
- columns compared: 14
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET1_UPD
- rows: baseline=3 actual=3
- columns compared: 14
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET2
- rows: baseline=3 actual=3
- columns compared: 14
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET21
- rows: baseline=3 actual=3
- columns compared: 14
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET3
- rows: baseline=4 actual=4
- columns compared: 8
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET5
- rows: baseline=2 actual=2
- columns compared: 5
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET6
- rows: baseline=2 actual=2
- columns compared: 12
- result: **MATCH** (all values within tolerance)

**Overall: PARITY VERIFIED**
```

## Query history

The verifier emitted this exact query (the invocation used
`--history-hours 6`):

```sql
SELECT START_TIME, QUERY_ID, USER_NAME, ROLE_NAME, WAREHOUSE_NAME,
       EXECUTION_STATUS, QUERY_TEXT
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY(
    END_TIME_RANGE_START => DATEADD('hour', -6, CURRENT_TIMESTAMP()),
    RESULT_LIMIT => 10000
))
WHERE USER_NAME = CURRENT_USER()
  AND ROLE_NAME = CURRENT_ROLE()
  AND WAREHOUSE_NAME = CURRENT_WAREHOUSE()
ORDER BY START_TIME
```

The following are real query-history rows from the same output. They cover
`create or replace transient table devin_migration_demo.DBT_INFORMATICA_RUN20260806.demo_target*`
DDL and verification count/MINUS queries. Long DDL query text is truncated
only in this inline excerpt and is marked explicitly; the full rows remain
unedited in `docs/evidence/raw/snowflake_verifier.txt`.

```text
(datetime.datetime(2026, 8, 5, 22, 1, 54, 876000, tzinfo=<DstTzInfo 'America/Los_Angeles' PDT-1 day, 17:00:00 DST>), '01c6338d-0107-544d-000f-dc5e0003403e', 'DEVIN_DEMO', 'DEVIN_MIGRATION_DEMO', 'DEVIN_DEMO_WH', 'SUCCESS', 'create or replace transient table devin_migration_demo.DBT_INFORMATICA_RUN20260806.demo_target3






    as (

/*
  RECOVERED: product fields pass through exp_TRANS2.
  RECOVERED: SELL_ST_DT is the NULL o_SELL_ST_DT legacy defect; SELL_ED_DT
  is the DD/MM/YYYY conversion result. RECOVERED: SELL_ST_DT is a DATE
  port whose expression yields NULL; the intermediate model emits
  cast(null as date). Parity comparison requires pandas<3 as an environment
  requirement, not a modeling decision.
*/
select
    PRODUCT_ID,
    PRODUCT_NM,
    PRODUCT_NO,
    COLOR,
    STD_COST,
    LIST_PRICE,
    o_SELL_ST_DT as SELL_ST_DT,
    o_SELL_ED_DT as SELL_ED_DT
from devin_migration_demo.DBT_INFORMATICA_RUN20260806.int_m1__exp_TRANS2
    )

/* {"app": "dbt", "dbt_version": "1.12.0", "profile_name": "informatica_migration", "target_name": "snowflake", "node_id": "model.informatica_migration.demo_target3"} */;')
(datetime.datetime(2026, 8, 5, 22, 1, 57, 926000, tzinfo=<DstTzInfo 'America/Los_Angeles' PDT-1 day, 17:00:00 DST>), '01c6338d-0107-544d-000f-dc5e0003404e', 'DEVIN_DEMO', 'DEVIN_MIGRATION_DEMO', 'DEVIN_DEMO_WH', 'SUCCESS', 'create or replace transient table devin_migration_demo.DBT_INFORMATICA_RUN20260806.demo_target5






    as (

/*
  RECOVERED: target receives one row per connected demo_target5 router row.
  FIRST_NM and CRDT_SCORE come from connected lkp_TRANS2 and lkp_TRANS3;
  LAST_NM and BAL_AMT pass through from demo_source3 via the SQ.
*/
select
    ACCT_ID,
    FIRST_NM,
    LAST_NM,
    BAL_AMT,
    CRDT_SCORE
from devin_migration_demo.DBT_INFORMATICA_RUN20260806.int_m1__rtr_TRANS_demo_target5_GRP
    )

/* {"app": "dbt", "dbt_version": "1.12.0", "profile_name": "informatica_migration", "target_name": "snowflake", "node_id": "model.informatica_migration.demo_target5"} */;')
(datetime.datetime(2026, 8, 5, 22, 1, 58, 173000, tzinfo=<DstTzInfo 'America/Los_Angeles' PDT-1 day, 17:00:00 DST>), '01c6338d-0107-5426-000f-dc5e000311ee', 'DEVIN_DEMO', 'DEVIN_MIGRATION_DEMO', 'DEVIN_DEMO_WH', 'SUCCESS', 'create or replace transient table devin_migration_demo.DBT_INFORMATICA_RUN20260806.demo_target1_ins






    as (

/*
  RECOVERED: demo_target1_INS receives the Insert router group and the
  SEQTRANS-generated Key, source fields, and created audit ports.
  RECOVERED: UPDATED_BY, UPDATED_TIME, ACTIVE_FLAG, START_DATE, and END_DATE
  have no connectors for this target instance and are typed NULLs.
*/
select
    Key,
    LEAD_CO_MNE,
    BRANCH_CO_MNE,
    MIS_DATE,
    ID,
    DESCRIPTION,
    SHORT_NAME,
    o_CREATED_BY as CREATED_BY,
    o_CREATED_TIME as CREATED_TIME,
    cast(null as VARCHAR) as UPDATED_BY,
    cast(null as TIMESTAMP) as UPDATED_TIME,
    cast(null as VARCHAR) as ACTIVE_FLAG,
    cast(null as TIMESTAMP) as START_DATE,
    cast(null as TIMESTAMP) as END_DATE
from devin_migration_demo.DBT_INFORMATICA_RUN20260806.int_m2__rtr_insert
    )

/* {"app": "dbt", "dbt_version": "1.12.0", "profile_name": "informatica_migration", "target_name": "snowflake", "node_id": "model.informatica_migration.demo_target1_ins"} */;')
(datetime.datetime(2026, 8, 5, 22, 1, 58, 550000, tzinfo=<DstTzInfo 'America/Los_Angeles' PDT-1 day, 17:00:00 DST>), '01c6338d-0107-544d-000f-dc5e00034052', 'DEVIN_DEMO', 'DEVIN_MIGRATION_DEMO', 'DEVIN_DEMO_WH', 'SUCCESS', 'create or replace transient table devin_migration_demo.DBT_INFORMATICA_RUN20260806.demo_target2






    as (

/*
  RECOVERED: CONNECTOR elements map NEWGROUP1 router ports to these target
  columns in this order: Title, Gender, First_Name, Middle_Name, Last_Name,
  Member_Identifier, Member_Suffix, Date_of_Birth, Member_Number, Soc_Number,
  Type_Code, Relationship_to_Subscriber_Code,
  Relationship_to_Subscriber_Code_Label, Effective_Date.
  RECOVERED: the export holds one target DEFINITION, TARGET NAME="demo_target2"
  DATABASETYPE="Oracle", and two INSTANCEs of it, NAME="demo_target2" and
  NAME="demo_target21", both TRANSFORMATION_NAME="demo_target2" and both
  TARGETLOADORDER ORDER="1". Each instance is fed by its own router group and
  has its own SESSIONEXTENSION Relational Writer with its own reject file
  (demo_target21.bad for this instance, demo_target211.bad for demo_target21),
  so the legacy writes one physical Oracle table, demo_target2, from two
  writers.
  DECISION: dbt has no equivalent of two models writing one relation, so each
  target instance is modelled as its own table. Rejected alternat ... [QUERY_TEXT TRUNCATED; full row is in raw transcript]
(datetime.datetime(2026, 8, 5, 22, 2, 1, 252000, tzinfo=<DstTzInfo 'America/Los_Angeles' PDT-1 day, 17:00:00 DST>), '01c6338e-0107-4ef4-000f-dc5e0002655a', 'DEVIN_DEMO', 'DEVIN_MIGRATION_DEMO', 'DEVIN_DEMO_WH', 'SUCCESS', 'create or replace transient table devin_migration_demo.DBT_INFORMATICA_RUN20260806.demo_target21






    as (

/*
  RECOVERED: CONNECTOR elements map NEWGROUP2 router ports to these target
  columns in this order: Title, Gender, First_Name, Middle_Name, Last_Name,
  Member_Identifier, Member_Suffix, Date_of_Birth, Member_Number, Soc_Number,
  Type_Code, Relationship_to_Subscriber_Code,
  Relationship_to_Subscriber_Code_Label, Effective_Date.
  RECOVERED: the export holds one target DEFINITION, TARGET NAME="demo_target2"
  DATABASETYPE="Oracle", and two INSTANCEs of it, NAME="demo_target21" and
  NAME="demo_target2", both TRANSFORMATION_NAME="demo_target2" and both
  TARGETLOADORDER ORDER="1". Each instance is fed by its own router group and
  has its own SESSIONEXTENSION Relational Writer with its own reject file
  (demo_target211.bad for this instance, demo_target21.bad for demo_target2),
  so the legacy writes one physical Oracle table, demo_target2, from two
  writers.
  DECISION: dbt has no equivalent of two models writing one relation, so each
  target instance is modelled as its own table. Rejected alternati ... [QUERY_TEXT TRUNCATED; full row is in raw transcript]
(datetime.datetime(2026, 8, 5, 22, 2, 1, 593000, tzinfo=<DstTzInfo 'America/Los_Angeles' PDT-1 day, 17:00:00 DST>), '01c6338e-0107-4ec9-000f-dc5e00021592', 'DEVIN_DEMO', 'DEVIN_MIGRATION_DEMO', 'DEVIN_DEMO_WH', 'SUCCESS', 'create or replace transient table devin_migration_demo.DBT_INFORMATICA_RUN20260806.demo_target6






    as (

/*
  RECOVERED: target columns connect to agg_TRANS ports as listed below.
  DECISION: SEQ_GEN current value 281 means emitted keys begin at 281;
  dense_rank ordered by ACCT_ID represents the recovered sorted input order.
*/
select
    ACCT_ID,
    o_acc_trim as ACCT_TYP,
    o_ACCT_DESC as ACCT_DESC,
    CR8_DT,
    o_crdt_trim as CRDT_LN,
    CLSR_DT,
    ACCT_STAT_CD,
    TX_ID,
    280 + dense_rank() over (order by ACCT_ID) as ACCT_KEY,
    TX_DTTM,
    o_TX_AMT as TX_AMT,
    o_ACCT_ID as TX_TYPE_CD
from devin_migration_demo.DBT_INFORMATICA_RUN20260806.int_m1__agg_TRANS
    )

/* {"app": "dbt", "dbt_version": "1.12.0", "profile_name": "informatica_migration", "target_name": "snowflake", "node_id": "model.informatica_migration.demo_target6"} */;')
(datetime.datetime(2026, 8, 5, 22, 2, 1, 854000, tzinfo=<DstTzInfo 'America/Los_Angeles' PDT-1 day, 17:00:00 DST>), '01c6338e-0107-4ef4-000f-dc5e00026562', 'DEVIN_DEMO', 'DEVIN_MIGRATION_DEMO', 'DEVIN_DEMO_WH', 'SUCCESS', 'create or replace transient table devin_migration_demo.DBT_INFORMATICA_RUN20260806.demo_target1_upd






    as (

/*
  RECOVERED: demo_target1_UPD receives the UPDTRANS Key from LKPTRANS, not
  SEQTRANS, together with source fields and updated audit ports.
  RECOVERED: CREATED_BY, CREATED_TIME, ACTIVE_FLAG, START_DATE, and END_DATE
  have no connectors for this target instance and are typed NULLs.
*/
select
    Key,
    LEAD_CO_MNE,
    BRANCH_CO_MNE,
    MIS_DATE,
    ID,
    DESCRIPTION,
    SHORT_NAME,
    cast(null as VARCHAR) as CREATED_BY,
    cast(null as TIMESTAMP) as CREATED_TIME,
    o_UPDATED_BY as UPDATED_BY,
    o_UPDATED_TIME as UPDATED_TIME,
    cast(null as VARCHAR) as ACTIVE_FLAG,
    cast(null as TIMESTAMP) as START_DATE,
    cast(null as TIMESTAMP) as END_DATE
from devin_migration_demo.DBT_INFORMATICA_RUN20260806.int_m2__updtrans
    )

/* {"app": "dbt", "dbt_version": "1.12.0", "profile_name": "informatica_migration", "target_name": "snowflake", "node_id": "model.informatica_migration.demo_target1_upd"} */;')
(datetime.datetime(2026, 8, 5, 22, 7, 15, 628000, tzinfo=<DstTzInfo 'America/Los_Angeles' PDT-1 day, 17:00:00 DST>), '01c63393-0107-5426-000f-dc5e000312da', 'DEVIN_DEMO', 'DEVIN_MIGRATION_DEMO', 'DEVIN_DEMO_WH', 'SUCCESS', 'SELECT \'BASELINE\' AS SOURCE, COUNT(*) AS ROW_COUNT FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET1_INS"
UNION ALL
SELECT \'MIGRATED\' AS SOURCE, COUNT(*) AS ROW_COUNT FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET1_INS"
ORDER BY SOURCE')
(datetime.datetime(2026, 8, 5, 22, 7, 15, 821000, tzinfo=<DstTzInfo 'America/Los_Angeles' PDT-1 day, 17:00:00 DST>), '01c63393-0107-544d-000f-dc5e0003412e', 'DEVIN_DEMO', 'DEVIN_MIGRATION_DEMO', 'DEVIN_DEMO_WH', 'SUCCESS', 'SELECT "KEY", "LEAD_CO_MNE", "BRANCH_CO_MNE", "MIS_DATE", "ID", "DESCRIPTION", "SHORT_NAME", "CREATED_BY", "CREATED_TIME", "UPDATED_BY", "UPDATED_TIME", "ACTIVE_FLAG", "START_DATE", "END_DATE" FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET1_INS" MINUS SELECT "KEY", "LEAD_CO_MNE", "BRANCH_CO_MNE", "MIS_DATE", "ID", "DESCRIPTION", "SHORT_NAME", "CREATED_BY", "CREATED_TIME", "UPDATED_BY", "UPDATED_TIME", "ACTIVE_FLAG", "START_DATE", "END_DATE" FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET1_INS"')
(datetime.datetime(2026, 8, 5, 22, 7, 16, 130000, tzinfo=<DstTzInfo 'America/Los_Angeles' PDT-1 day, 17:00:00 DST>), '01c63393-0107-5426-000f-dc5e000312de', 'DEVIN_DEMO', 'DEVIN_MIGRATION_DEMO', 'DEVIN_DEMO_WH', 'SUCCESS', 'SELECT "KEY", "LEAD_CO_MNE", "BRANCH_CO_MNE", "MIS_DATE", "ID", "DESCRIPTION", "SHORT_NAME", "CREATED_BY", "CREATED_TIME", "UPDATED_BY", "UPDATED_TIME", "ACTIVE_FLAG", "START_DATE", "END_DATE" FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET1_INS" MINUS SELECT "KEY", "LEAD_CO_MNE", "BRANCH_CO_MNE", "MIS_DATE", "ID", "DESCRIPTION", "SHORT_NAME", "CREATED_BY", "CREATED_TIME", "UPDATED_BY", "UPDATED_TIME", "ACTIVE_FLAG", "START_DATE", "END_DATE" FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET1_INS"')
(datetime.datetime(2026, 8, 5, 22, 7, 17, 616000, tzinfo=<DstTzInfo 'America/Los_Angeles' PDT-1 day, 17:00:00 DST>), '01c63393-0107-5354-000f-dc5e0002f2fe', 'DEVIN_DEMO', 'DEVIN_MIGRATION_DEMO', 'DEVIN_DEMO_WH', 'SUCCESS', 'SELECT \'BASELINE\' AS SOURCE, COUNT(*) AS ROW_COUNT FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET1_UPD"
UNION ALL
SELECT \'MIGRATED\' AS SOURCE, COUNT(*) AS ROW_COUNT FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET1_UPD"
ORDER BY SOURCE')
(datetime.datetime(2026, 8, 5, 22, 7, 17, 812000, tzinfo=<DstTzInfo 'America/Los_Angeles' PDT-1 day, 17:00:00 DST>), '01c63393-0107-5427-000f-dc5e00033102', 'DEVIN_DEMO', 'DEVIN_MIGRATION_DEMO', 'DEVIN_DEMO_WH', 'SUCCESS', 'SELECT "KEY", "LEAD_CO_MNE", "BRANCH_CO_MNE", "MIS_DATE", "ID", "DESCRIPTION", "SHORT_NAME", "CREATED_BY", "CREATED_TIME", "UPDATED_BY", "UPDATED_TIME", "ACTIVE_FLAG", "START_DATE", "END_DATE" FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET1_UPD" MINUS SELECT "KEY", "LEAD_CO_MNE", "BRANCH_CO_MNE", "MIS_DATE", "ID", "DESCRIPTION", "SHORT_NAME", "CREATED_BY", "CREATED_TIME", "UPDATED_BY", "UPDATED_TIME", "ACTIVE_FLAG", "START_DATE", "END_DATE" FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET1_UPD"')
(datetime.datetime(2026, 8, 5, 22, 7, 18, 141000, tzinfo=<DstTzInfo 'America/Los_Angeles' PDT-1 day, 17:00:00 DST>), '01c63393-0107-5427-000f-dc5e00033106', 'DEVIN_DEMO', 'DEVIN_MIGRATION_DEMO', 'DEVIN_DEMO_WH', 'SUCCESS', 'SELECT "KEY", "LEAD_CO_MNE", "BRANCH_CO_MNE", "MIS_DATE", "ID", "DESCRIPTION", "SHORT_NAME", "CREATED_BY", "CREATED_TIME", "UPDATED_BY", "UPDATED_TIME", "ACTIVE_FLAG", "START_DATE", "END_DATE" FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET1_UPD" MINUS SELECT "KEY", "LEAD_CO_MNE", "BRANCH_CO_MNE", "MIS_DATE", "ID", "DESCRIPTION", "SHORT_NAME", "CREATED_BY", "CREATED_TIME", "UPDATED_BY", "UPDATED_TIME", "ACTIVE_FLAG", "START_DATE", "END_DATE" FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET1_UPD"')
(datetime.datetime(2026, 8, 5, 22, 7, 19, 390000, tzinfo=<DstTzInfo 'America/Los_Angeles' PDT-1 day, 17:00:00 DST>), '01c63393-0107-5427-000f-dc5e0003310a', 'DEVIN_DEMO', 'DEVIN_MIGRATION_DEMO', 'DEVIN_DEMO_WH', 'SUCCESS', 'SELECT \'BASELINE\' AS SOURCE, COUNT(*) AS ROW_COUNT FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET2"
UNION ALL
SELECT \'MIGRATED\' AS SOURCE, COUNT(*) AS ROW_COUNT FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET2"
ORDER BY SOURCE')
(datetime.datetime(2026, 8, 5, 22, 7, 19, 596000, tzinfo=<DstTzInfo 'America/Los_Angeles' PDT-1 day, 17:00:00 DST>), '01c63393-0107-5427-000f-dc5e0003310e', 'DEVIN_DEMO', 'DEVIN_MIGRATION_DEMO', 'DEVIN_DEMO_WH', 'SUCCESS', 'SELECT "TITLE", "GENDER", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "MEMBER_IDENTIFIER", "MEMBER_SUFFIX", "DATE_OF_BIRTH", "MEMBER_NUMBER", "SOC_NUMBER", "TYPE_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE_LABEL", "EFFECTIVE_DATE" FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET2" MINUS SELECT "TITLE", "GENDER", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "MEMBER_IDENTIFIER", "MEMBER_SUFFIX", "DATE_OF_BIRTH", "MEMBER_NUMBER", "SOC_NUMBER", "TYPE_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE_LABEL", "EFFECTIVE_DATE" FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET2"')
(datetime.datetime(2026, 8, 5, 22, 7, 19, 865000, tzinfo=<DstTzInfo 'America/Los_Angeles' PDT-1 day, 17:00:00 DST>), '01c63393-0107-544d-000f-dc5e00034136', 'DEVIN_DEMO', 'DEVIN_MIGRATION_DEMO', 'DEVIN_DEMO_WH', 'SUCCESS', 'SELECT "TITLE", "GENDER", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "MEMBER_IDENTIFIER", "MEMBER_SUFFIX", "DATE_OF_BIRTH", "MEMBER_NUMBER", "SOC_NUMBER", "TYPE_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE_LABEL", "EFFECTIVE_DATE" FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET2" MINUS SELECT "TITLE", "GENDER", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "MEMBER_IDENTIFIER", "MEMBER_SUFFIX", "DATE_OF_BIRTH", "MEMBER_NUMBER", "SOC_NUMBER", "TYPE_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE_LABEL", "EFFECTIVE_DATE" FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET2"')
(datetime.datetime(2026, 8, 5, 22, 7, 21, 156000, tzinfo=<DstTzInfo 'America/Los_Angeles' PDT-1 day, 17:00:00 DST>), '01c63393-0107-544d-000f-dc5e0003413a', 'DEVIN_DEMO', 'DEVIN_MIGRATION_DEMO', 'DEVIN_DEMO_WH', 'SUCCESS', 'SELECT \'BASELINE\' AS SOURCE, COUNT(*) AS ROW_COUNT FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET21"
UNION ALL
SELECT \'MIGRATED\' AS SOURCE, COUNT(*) AS ROW_COUNT FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET21"
ORDER BY SOURCE')
(datetime.datetime(2026, 8, 5, 22, 7, 21, 338000, tzinfo=<DstTzInfo 'America/Los_Angeles' PDT-1 day, 17:00:00 DST>), '01c63393-0107-4ef4-000f-dc5e0002664e', 'DEVIN_DEMO', 'DEVIN_MIGRATION_DEMO', 'DEVIN_DEMO_WH', 'SUCCESS', 'SELECT "TITLE", "GENDER", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "MEMBER_IDENTIFIER", "MEMBER_SUFFIX", "DATE_OF_BIRTH", "MEMBER_NUMBER", "SOC_NUMBER", "TYPE_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE_LABEL", "EFFECTIVE_DATE" FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET21" MINUS SELECT "TITLE", "GENDER", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "MEMBER_IDENTIFIER", "MEMBER_SUFFIX", "DATE_OF_BIRTH", "MEMBER_NUMBER", "SOC_NUMBER", "TYPE_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE_LABEL", "EFFECTIVE_DATE" FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET21"')
(datetime.datetime(2026, 8, 5, 22, 7, 21, 537000, tzinfo=<DstTzInfo 'America/Los_Angeles' PDT-1 day, 17:00:00 DST>), '01c63393-0107-4ec9-000f-dc5e0002168a', 'DEVIN_DEMO', 'DEVIN_MIGRATION_DEMO', 'DEVIN_DEMO_WH', 'SUCCESS', 'SELECT "TITLE", "GENDER", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "MEMBER_IDENTIFIER", "MEMBER_SUFFIX", "DATE_OF_BIRTH", "MEMBER_NUMBER", "SOC_NUMBER", "TYPE_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE_LABEL", "EFFECTIVE_DATE" FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET21" MINUS SELECT "TITLE", "GENDER", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "MEMBER_IDENTIFIER", "MEMBER_SUFFIX", "DATE_OF_BIRTH", "MEMBER_NUMBER", "SOC_NUMBER", "TYPE_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE", "RELATIONSHIP_TO_SUBSCRIBER_CODE_LABEL", "EFFECTIVE_DATE" FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET21"')
(datetime.datetime(2026, 8, 5, 22, 7, 22, 832000, tzinfo=<DstTzInfo 'America/Los_Angeles' PDT-1 day, 17:00:00 DST>), '01c63393-0107-5426-000f-dc5e000312e6', 'DEVIN_DEMO', 'DEVIN_MIGRATION_DEMO', 'DEVIN_DEMO_WH', 'SUCCESS', 'SELECT \'BASELINE\' AS SOURCE, COUNT(*) AS ROW_COUNT FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET3"
UNION ALL
SELECT \'MIGRATED\' AS SOURCE, COUNT(*) AS ROW_COUNT FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET3"
ORDER BY SOURCE')
(datetime.datetime(2026, 8, 5, 22, 7, 23, 100000, tzinfo=<DstTzInfo 'America/Los_Angeles' PDT-1 day, 17:00:00 DST>), '01c63393-0107-544d-000f-dc5e0003413e', 'DEVIN_DEMO', 'DEVIN_MIGRATION_DEMO', 'DEVIN_DEMO_WH', 'SUCCESS', 'SELECT "PRODUCT_ID", "PRODUCT_NM", "PRODUCT_NO", "COLOR", "STD_COST", "LIST_PRICE", "SELL_ST_DT", "SELL_ED_DT" FROM "BASELINE_INFORMATICA_RUN20260806"."DEMO_TARGET3" MINUS SELECT "PRODUCT_ID", "PRODUCT_NM", "PRODUCT_NO", "COLOR", "STD_COST", "LIST_PRICE", "SELL_ST_DT", "SELL_ED_DT" FROM "DBT_INFORMATICA_RUN20260806"."DEMO_TARGET3"')
```

## Build tails

Snowflake dbt build tail (full output:
`docs/evidence/raw/snowflake_dbt_build.txt`):

```text
[0m05:02:03  127 of 138 PASS not_null_demo_target6_ACCT_ID .................................. [[32mPASS[0m in 0.20s]
[0m05:02:03  133 of 138 START test not_null_demo_target6_TX_AMT ............................. [RUN]
[0m05:02:04  130 of 138 PASS not_null_demo_target6_ACCT_TYP ................................. [[32mPASS[0m in 0.12s]
[0m05:02:04  134 of 138 START test not_null_demo_target6_TX_DTTM ............................ [RUN]
[0m05:02:04  131 of 138 PASS not_null_demo_target6_CR8_DT ................................... [[32mPASS[0m in 0.12s]
[0m05:02:04  135 of 138 START test not_null_demo_target6_TX_ID .............................. [RUN]
[0m05:02:04  132 of 138 PASS not_null_demo_target6_CRDT_LN .................................. [[32mPASS[0m in 0.13s]
[0m05:02:04  136 of 138 START test not_null_demo_target6_TX_TYPE_CD ......................... [RUN]
[0m05:02:04  133 of 138 PASS not_null_demo_target6_TX_AMT ................................... [[32mPASS[0m in 0.14s]
[0m05:02:04  137 of 138 START test unique_demo_target6_ACCT_ID .............................. [RUN]
[0m05:02:04  134 of 138 PASS not_null_demo_target6_TX_DTTM .................................. [[32mPASS[0m in 0.12s]
[0m05:02:04  138 of 138 START test unique_demo_target6_ACCT_KEY ............................. [RUN]
[0m05:02:04  137 of 138 PASS unique_demo_target6_ACCT_ID .................................... [[32mPASS[0m in 0.14s]
[0m05:02:04  135 of 138 PASS not_null_demo_target6_TX_ID .................................... [[32mPASS[0m in 0.20s]
[0m05:02:04  136 of 138 PASS not_null_demo_target6_TX_TYPE_CD ............................... [[32mPASS[0m in 0.19s]
[0m05:02:04  138 of 138 PASS unique_demo_target6_ACCT_KEY ................................... [[32mPASS[0m in 0.13s]
[0m05:02:04
[0m05:02:04  Finished running 9 seeds, 7 table models, 98 data tests, 24 view models in 0 hours 0 minutes and 18.88 seconds (18.88s).
[0m05:02:05
[0m05:02:05  [32mCompleted successfully[0m
[0m05:02:05
[0m05:02:05  Done. PASS=138 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=138
```

DuckDB dbt build tail (full output:
`docs/evidence/raw/duckdb_build.txt`):

```text
[0m05:14:21  130 of 138 PASS not_null_demo_target1_upd_DESCRIPTION .......................... [[32mPASS[0m in 0.07s]
[0m05:14:21  132 of 138 START test not_null_demo_target1_upd_Key ............................ [RUN]
[0m05:14:21  133 of 138 START test not_null_demo_target1_upd_LEAD_CO_MNE .................... [RUN]
[0m05:14:21  134 of 138 START test not_null_demo_target1_upd_MIS_DATE ....................... [RUN]
[0m05:14:21  131 of 138 PASS not_null_demo_target1_upd_ID ................................... [[32mPASS[0m in 0.06s]
[0m05:14:21  135 of 138 START test not_null_demo_target1_upd_SHORT_NAME ..................... [RUN]
[0m05:14:21  134 of 138 PASS not_null_demo_target1_upd_MIS_DATE ............................. [[32mPASS[0m in 0.06s]
[0m05:14:21  136 of 138 START test not_null_demo_target1_upd_UPDATED_BY ..................... [RUN]
[0m05:14:21  132 of 138 PASS not_null_demo_target1_upd_Key .................................. [[32mPASS[0m in 0.07s]
[0m05:14:21  137 of 138 START test not_null_demo_target1_upd_UPDATED_TIME ................... [RUN]
[0m05:14:21  133 of 138 PASS not_null_demo_target1_upd_LEAD_CO_MNE .......................... [[32mPASS[0m in 0.08s]
[0m05:14:21  138 of 138 START test unique_demo_target1_upd_ID ............................... [RUN]
[0m05:14:21  135 of 138 PASS not_null_demo_target1_upd_SHORT_NAME ........................... [[32mPASS[0m in 0.07s]
[0m05:14:21  136 of 138 PASS not_null_demo_target1_upd_UPDATED_BY ........................... [[32mPASS[0m in 0.06s]
[0m05:14:21  137 of 138 PASS not_null_demo_target1_upd_UPDATED_TIME ......................... [[32mPASS[0m in 0.05s]
[0m05:14:21  138 of 138 PASS unique_demo_target1_upd_ID ..................................... [[32mPASS[0m in 0.03s]
[0m05:14:21
[0m05:14:21  Finished running 9 seeds, 7 table models, 98 data tests, 24 view models in 0 hours 0 minutes and 3.51 seconds (3.51s).
[0m05:14:21
[0m05:14:21  [32mCompleted successfully[0m
[0m05:14:21
[0m05:14:21  Done. PASS=138 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=138
```

The final DuckDB parity transcript is committed at
`docs/evidence/raw/duckdb_parity.txt` and ends with `Overall: PARITY VERIFIED`.
The Snowflake workflow transcript is committed at
`docs/evidence/raw/snowflake_run_workflow.txt`.
