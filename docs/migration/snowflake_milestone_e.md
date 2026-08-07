# Snowflake milestone E provisioning record

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
schemas. The generated proof SQL is written to the ignored
`build/pyspark/informatica/proof_<RUNID>.sql`.

## Ordinal materialization

The loader DDL includes a stored `__LINE_ORDINAL NUMBER(38,0) NOT NULL` on:

- `lkp_demo_source1`
- `lkp_demo_source2`
- `lkp_demo_source3`
- `demo_target1`

Rows are inserted from `csv.DictReader` enumeration, so ordinal zero is the
first data line after the header and each subsequent value follows physical
file order. The generated loader output confirms the tables and row counts;
the target schemas remain standing for the follow-up Spark round-trip.

## Query-history blocker

The requested query was attempted exactly as an `information_schema.query_history`
object query:

```sql
select query_id, query_text, start_time, rows_produced
from devin_migration_demo.information_schema.query_history
where user_name = current_user()
  and warehouse_name = current_warehouse()
  and start_time >= dateadd('hour', -2, current_timestamp())
order by start_time desc
```

Snowflake returned:

```text
002003 (42S02): SQL compilation error:
Object 'DEVIN_MIGRATION_DEMO.INFORMATION_SCHEMA.QUERY_HISTORY' does not exist or not authorized.
```

Per the migration handoff instruction, no alternate query source or query shape
was substituted after this schema/authorization surprise. Consequently, the
Spark connector round-trip, proof execution, and query-history evidence remain
pending the lead's decision on the authorized Snowflake query-history interface.
