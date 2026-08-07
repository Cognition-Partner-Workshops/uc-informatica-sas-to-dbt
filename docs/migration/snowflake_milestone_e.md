# Snowflake end-to-end provisioning and parity record

Run id: `20260807T0658Z`

Created schemas:

- `SOURCE_INFORMATICA_20260807T0658Z`
- `PYSPARK_INFORMATICA_20260807T0658Z`
- `BASELINE_INFORMATICA_20260807T0658Z`

The pre-creation query returned only:

```text
BASELINE_INFORMATICA
DBT_INFORMATICA
INFORMATION_SCHEMA
```

The pre-existing `DBT_INFORMATICA` and `BASELINE_INFORMATICA` schemas were not
modified.

## Loader result

The generator created explicit typed DDL from `schemas.py` and loaded:

```text
demo_source1: 7 rows
demo_source2: 7 rows
demo_source3: 6 rows
demo_source4: 5 rows
demo_source5: 4 rows
lkp_demo_source1: 6 rows
lkp_demo_source2: 6 rows
lkp_demo_source3: 6 rows
demo_target1: 5 rows
```

All seven baseline CSV target instances were loaded into the baseline schema:

```text
demo_target1_INS: 4 rows
demo_target1_UPD: 3 rows
demo_target2: 3 rows
demo_target21: 3 rows
demo_target3: 4 rows
demo_target5: 2 rows
demo_target6: 2 rows
```

Normalized `V_<TARGET>` views were generated in both the baseline and migrated
schemas. The generated proof SQL is committed as durable evidence at
`docs/migration/snowflake_proof_20260807T0658Z.sql`.

## Ordinal materialization

The loader DDL includes a stored `__LINE_ORDINAL NUMBER(38,0) NOT NULL` on:

- `lkp_demo_source1`
- `lkp_demo_source2`
- `lkp_demo_source3`
- `demo_source1`
- `demo_target1`

Rows are inserted from `csv.DictReader` enumeration, so ordinal zero is the
first data line after the header and each subsequent value follows physical
file order. The generated loader output confirms the tables and row counts;
the target schemas remain standing for the follow-up Spark round-trip.

## Verification

The corrected table-function query worked. The selected variant was
`query_history`:

```sql
select query_id, query_text, start_time, end_time, rows_produced,
       warehouse_name, execution_status
from table(devin_migration_demo.information_schema.query_history(
  end_time_range_start => dateadd('hour', -3, current_timestamp()),
  result_limit => 200))
where warehouse_name = current_warehouse()
order by start_time desc
```

Representative real query-history output included:

```text
01c639a2-0107-4ec9-000f-dc5e0003a2b6 ... CREATE SCHEMA "SOURCE_INFORMATICA_20260807T0658Z" ... 0 DEVIN_DEMO_WH SUCCESS
01c639a2-0107-58ad-000f-dc5e0004208a ... CREATE SCHEMA "PYSPARK_INFORMATICA_20260807T0658Z" ... 0 DEVIN_DEMO_WH SUCCESS
01c639a2-0107-5426-000f-dc5e00040182 ... CREATE SCHEMA "BASELINE_INFORMATICA_20260807T0658Z" ... 0 DEVIN_DEMO_WH SUCCESS
01c639a2-0107-58c8-000f-dc5e00038536 ... INSERT INTO ... LKP_DEMO_SOURCE1 ... 6 DEVIN_DEMO_WH SUCCESS
01c639a2-0107-58c8-000f-dc5e000430c2 ... INSERT INTO ... LKP_DEMO_SOURCE3 ... 6 DEVIN_DEMO_WH SUCCESS
01c639a2-0107-58c8-000f-dc5e000430c6 ... INSERT INTO ... DEMO_TARGET1 ... 5 DEVIN_DEMO_WH SUCCESS
01c639a2-0107-544d-000f-dc5e00034766 ... CREATE OR REPLACE VIEW ... V_DEMO_TARGET5 ... 0 DEVIN_DEMO_WH SUCCESS
01c639af-0107-562f-000f-dc5e00038576 ... proof statement ... 7 DEVIN_DEMO_WH SUCCESS
01c639b0-0107-4ec9-000f-dc5e0003a2fe ... CREATE TABLE ... _MILESTONE_E_ROUND_TRIP ... 0 DEVIN_DEMO_WH SUCCESS
01c639b0-0107-58c8-000f-dc5e0004310e ... COPY INTO _MILESTONE_E_ROUND_TRIP_staging ... 2 DEVIN_DEMO_WH SUCCESS
01c639b0-0107-562f-000f-dc5e00038582 ... SELECT "ID", "LABEL" FROM _MILESTONE_E_ROUND_TRIP ... 2 DEVIN_DEMO_WH SUCCESS
01c639b0-0107-562f-000f-dc5e0003858a ... DROP TABLE "PYSPARK_INFORMATICA_20260807T0658Z"."_MILESTONE_E_ROUND_TRIP" ... 0 DEVIN_DEMO_WH SUCCESS
```

The stored ordinal checks returned:

```text
lkp_demo_source1: stored=[0, 1, 2, 3, 4, 5] csv_expected=[0, 1, 2, 3, 4, 5] MATCH=True
lkp_demo_source2: stored=[0, 1, 2, 3, 4, 5] csv_expected=[0, 1, 2, 3, 4, 5] MATCH=True
lkp_demo_source3: stored=[0, 1, 2, 3, 4, 5] csv_expected=[0, 1, 2, 3, 4, 5] MATCH=True
demo_source1: stored=[0, 1, 2, 3, 4, 5, 6] csv_expected=[0, 1, 2, 3, 4, 5, 6] MATCH=True
demo_target1: stored=[0, 1, 2, 3, 4] csv_expected=[0, 1, 2, 3, 4] MATCH=True
```

The Spark connector round-trip passed:

```text
Row(ID=Decimal('101'), LABEL='snowflake-round-trip')
Row(ID=Decimal('102'), LABEL='second-row')
Spark Snowflake round-trip: PASS; throwaway table dropped
```

The generated proof statement was first executed against the empty migrated
tables as the expected negative control. After the mapping modules landed, the
same run schemas were reused for the end-to-end workflow. The final proof
statement was executed unchanged and passed all seven targets:

```text
('DEMO_TARGET1_INS', 4, 4, 8128491501339877599, 8128491501339877599, 0, 0, 'PASS')
('DEMO_TARGET1_UPD', 3, 3, -5257889502721467851, -5257889502721467851, 0, 0, 'PASS')
('DEMO_TARGET2', 3, 3, 3123907108787439864, 3123907108787439864, 0, 0, 'PASS')
('DEMO_TARGET21', 3, 3, -5462086455473858760, -5462086455473858760, 0, 0, 'PASS')
('DEMO_TARGET3', 4, 4, 2979066879702683896, 2979066879702683896, 0, 0, 'PASS')
('DEMO_TARGET5', 2, 2, -4578390602032457200, -4578390602032457200, 0, 0, 'PASS')
('DEMO_TARGET6', 2, 2, -987830873279475629, -987830873279475629, 0, 0, 'PASS')
```

The Snowflake workflow exited `0`. The local workflow exited `0`, and the
unmodified parity comparator reported all seven targets as `MATCH`.

Final-run query-history evidence included the end-to-end proof and regenerated
normalisation:

```text
01c639bd-0107-4ec9-000f-dc5e0003a4ce ... proof statement ... 7 DEVIN_DEMO_WH SUCCESS
01c639bc-0107-4ec9-000f-dc5e0003a49a ... CREATE OR REPLACE VIEW ... PYSPARK...V_DEMO_TARGET5 ... 0 DEVIN_DEMO_WH SUCCESS
01c639bc-0107-544d-000f-dc5e00034936 ... CREATE OR REPLACE VIEW ... BASELINE...V_DEMO_TARGET5 ... 0 DEVIN_DEMO_WH SUCCESS
01c639bc-0107-5426-000f-dc5e0004031e ... CREATE OR REPLACE VIEW ... PYSPARK...V_DEMO_TARGET6 ... 0 DEVIN_DEMO_WH SUCCESS
01c639bc-0107-58c8-000f-dc5e0004327a ... DROP TABLE ... _MILESTONE_E_ROUND_TRIP ... 0 DEVIN_DEMO_WH SUCCESS
```

The final Snowflake target column checks showed `DATE` for migrated
`DEMO_TARGET3.SELL_ST_DT` and `SELL_ED_DT`, and `NUMBER` for migrated
`DEMO_TARGET5.ACCT_ID`, `BAL_AMT`, and `CRDT_SCORE`. The generated view for
`DEMO_TARGET5` uses `TO_VARCHAR(TO_DECIMAL(...,38,6))` for the numeric columns,
which resolved the initial end-to-end formatting divergence.

## Maven fallback

The initial Maven coordinates were tested, but Maven Central returned HTTP 429
rate-limit responses and Spark reported unresolved dependencies. The
connector and JDBC jars were therefore provisioned outside the repository:

```text
$HOME/.cache/informatica-snowflake-jars/spark-snowflake_2.12-3.2.1-spark_3.5.jar
$HOME/.cache/informatica-snowflake-jars/snowflake-jdbc-4.0.2.jar
```

`session.py` uses `spark.jars` when `snowflake_jars_dir` is supplied; otherwise
it retains the pinned `spark.jars.packages` fallback.
