# Informatica Snowflake parity notes

Scope: `m_demo_mapping2` only. Legacy files are inputs and are not modified.

## Models

| Model | Status | Snowflake error and portable fix |
|---|---|---|
| `stg_demo_source1` | changed | DuckDB-only `external_location: read_csv(...)` cannot supply a Snowflake relation. Added a Snowflake branch selecting from `ref('demo_source1')`; the DuckDB branch is unchanged. |
| `stg_demo_target1_pre` | changed | DuckDB-only `external_location: read_csv(...)` cannot supply a Snowflake relation. Added a Snowflake branch selecting from `ref('demo_target1_pre')`; the DuckDB branch is unchanged. |
| `int_demo_mapping2_lookup` | unmodified | No Snowflake SQL change required. |
| `demo_target1_ins` | unmodified | No Snowflake SQL change required. |
| `demo_target1_upd` | unmodified | No Snowflake SQL change required. |
| `demo_target1` | unmodified | No Snowflake SQL change required. |

## Setup errors and fixes

The preferred external seed path was rejected during dbt parsing because it
also discovered the abort fixture with a duplicate resource name:

```text
Compilation Error
  dbt found two seeds with the name "demo_source2".

  Since these resources have the same name, dbt will be unable to find the correct resource
  when looking for ref("demo_source2").

  To fix this, change the name of one of these resources:
  - seed.informatica_m_demo_mapping2.demo_source2 (../../legacy/informatica/data/abort/demo_source2.csv)
  - seed.informatica_m_demo_mapping2.demo_source2 (../../legacy/informatica/data/demo_source2.csv)
```

The two required CSVs were initially copied (without modification) to
`dbt/informatica/seeds/`, then replaced with committed relative symlinks to
the legacy files. The target symlink is named `demo_target1_pre.csv` to avoid
a database-name collision with the `demo_target1` model. `dbt seed
--target snowflake` successfully loaded both through the symlinks:

```text
Done. PASS=2 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=2
```

The original seed-name collision also caused this dependency error:

```text
Compilation Error
  Found a cycle: model.informatica_m_demo_mapping2.int_demo_mapping2_lookup --> model.informatica_m_demo_mapping2.demo_target1_ins --> model.informatica_m_demo_mapping2.demo_target1 --> model.informatica_m_demo_mapping2.stg_demo_target1_pre
```

That cycle was caused by the staging branch initially resolving the seed name
`demo_target1` to the model of the same name. It was fixed portably by using
`ref('demo_target1_pre')`.

## Snowflake scoped parity

Using the same `normalize()` and `compare()` code path as the DuckDB
comparator, with the baseline scoped to the two `m_demo_mapping2` targets:

| Target | Baseline rows | Snowflake rows | Result |
|---|---:|---:|---|
| `DEMO_TARGET1_INS` | 4 | 4 | MATCH |
| `DEMO_TARGET1_UPD` | 3 | 3 | MATCH |

Overall result: **PARITY VERIFIED** (exit code 0).

## Engine observations

All six dbt relations matched DuckDB row-for-row after normalizing Snowflake
timestamp display precision:

| Relation | Snowflake rows | DuckDB rows | Result |
|---|---:|---:|---|
| `stg_demo_source1` | 7 | 7 | match |
| `stg_demo_target1_pre` | 5 | 5 | match |
| `int_demo_mapping2_lookup` | 7 | 7 | match |
| `demo_target1_ins` | 4 | 4 | match |
| `demo_target1_upd` | 3 | 3 | match |
| `demo_target1` | 5 | 5 | match |

Snowflake folds the mixed-case CSV header `Key` to `KEY`; the existing
unquoted `Key` references work on both engines, so no additional identifier
change was needed. Snowflake reports the configured `DOUBLE` seed column as
`FLOAT`, while all VARCHARs report as `TEXT`; these type aliases produced
matching numeric and string values. `MIS_DATE` remained VARCHAR/TEXT, the
timestamp columns were `TIMESTAMP_NTZ`, and MD5 output matched. No
differences in null ordering, row-number ordering, date/timestamp parsing, or
merge behavior were observed for this dataset. In particular, the insert
`row_number()` ordering is by non-null unique IDs, and the lookup ranking is
by non-null numeric keys, so engine-specific null ordering cannot affect these
rows. The merge uses unique numeric keys and the same update-column list on
both engines, so its behavior also remained equivalent.

The baseline CSV writer renders midnight timestamps as `YYYY-MM-DD`, while
DuckDB query results render them as `YYYY-MM-DD 00:00:00`; this is display
formatting only and is normalized by the repository parity comparison helper.
