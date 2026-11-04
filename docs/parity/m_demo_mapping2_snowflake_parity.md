# m_demo_mapping2 — Snowflake dual-run parity

Frozen business date: **2024-01-31**. Warehouse: `WH_INFA_ACCTDIM`.

## Input identity

The loader runs the unchanged baseline on the seeds, loads typed SRC tables,
replays `informatica_baseline.mapping2` from those exact Snowflake SRC rows,
and asserts byte-identical output before loading LEGACY. dbt reads the same SRC.

- `SFNFR_20261104.INFA_ACCTDIM_SRC_SFNFR_20261104.DEMO_SOURCE1`: 7 rows
- `SFNFR_20261104.INFA_ACCTDIM_SRC_SFNFR_20261104.DEMO_TARGET1`: 5 rows

`rows in` is the total physical input cardinality, including the duplicate lookup row.

LEGACY: `SFNFR_20261104.INFA_ACCTDIM_LEGACY_SFNFR_20261104`. New: `SFNFR_20261104.INFA_ACCTDIM_SF_SFNFR_20261104`.

## Canonical Snowflake comparison

| output | rows in | legacy rows | new rows | mismatches | legacy checksum | new checksum |
|---|---:|---:|---:|---:|---:|---:|
| DEMO_TARGET1_INS | 12 | 4 | 4 | 0 | -8099959845793173784 | -8099959845793173784 |
| DEMO_TARGET1_UPD | 12 | 3 | 3 | 0 | -4703698863453485522 | -4703698863453485522 |

Business key: `ID` for both outputs. Columns follow the XML target order.

Each canonical row uses NULL → `\N`, numbers → `TO_VARCHAR(ROUND(CAST(x AS NUMBER(38,6)),6))`,
timestamps → `YYYY-MM-DD HH24:MI:SS.FF6`, strings → `TRIM(x)`, joined by `|`.
Table checksum is Snowflake `HASH_AGG(canonical)`; row hash is `MD5(canonical)`.
A keyed full outer join compares row hashes. Both multiset EXCEPT directions
compare `(canonical, occurrence)` to retain duplicate multiplicity.

| output | keyed diff | legacy-only multiset | new-only multiset | L2 profiles equal |
|---|---:|---:|---:|---|
| DEMO_TARGET1_INS | 0 | 0 | 0 | True |
| DEMO_TARGET1_UPD | 0 | 0 | 0 | True |

L2 compares non-null counts, distinct counts, min/max for every column,
numeric sums and string total lengths. L4: no differing rows when all counts are zero.
Stored column names and order are checked against the legacy target definition.

## dbt build

`PASS=32 TOTAL=32` (from local `target/run_results.json`).
The build includes key/domain/relationship tests and unit fixtures for the legacy
always-update anomaly and duplicate lookup selection.

## Legacy anomalies (not mismatches)

- XML EXPTRANS compares AES_DECRYPT output to MD5. As documented by the supplied
  baseline, every lookup-matched row updates; this is not repaired into normal SCD2 logic.
- LKPTRANS Use Any Value is frozen to highest Key, then last physical seed row.
- SEQTRANS Current Value 57 yields insert keys starting at 57 in ID order.
- Unconnected ports remain NULL: ACTIVE_FLAG/START_DATE/END_DATE in both branches,
  UPDATED_* on inserts and CREATED_* on updates. No dimension merge is performed.
- MIS_DATE remains VARCHAR; source state END_DATE 9999-12-31 is TIMESTAMP_NTZ(6).

Explained mismatches: none.

## Unchanged parity_diff.py result

# Parity Report

Baseline: `LEGACY export`  |  Actual: `SF export`

## DEMO_TARGET1_INS
- rows: baseline=4 actual=4
- columns compared: 14
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET1_UPD
- rows: baseline=3 actual=3
- columns compared: 14
- result: **MATCH** (all values within tolerance)

**Overall: PARITY VERIFIED**

## Exact canonical SQL (legacy; change only schema to compare new)

```sql
SELECT ID, CONCAT_WS('|', COALESCE(TO_VARCHAR(ROUND(CAST("KEY" AS NUMBER(38,6)), 6)), '\\N'), COALESCE(TRIM("LEAD_CO_MNE"), '\\N'), COALESCE(TRIM("BRANCH_CO_MNE"), '\\N'), COALESCE(TRIM("MIS_DATE"), '\\N'), COALESCE(TRIM("ID"), '\\N'), COALESCE(TRIM("DESCRIPTION"), '\\N'), COALESCE(TRIM("SHORT_NAME"), '\\N'), COALESCE(TRIM("CREATED_BY"), '\\N'), COALESCE(TO_CHAR("CREATED_TIME", 'YYYY-MM-DD HH24:MI:SS.FF6'), '\\N'), COALESCE(TRIM("UPDATED_BY"), '\\N'), COALESCE(TO_CHAR("UPDATED_TIME", 'YYYY-MM-DD HH24:MI:SS.FF6'), '\\N'), COALESCE(TRIM("ACTIVE_FLAG"), '\\N'), COALESCE(TO_CHAR("START_DATE", 'YYYY-MM-DD HH24:MI:SS.FF6'), '\\N'), COALESCE(TO_CHAR("END_DATE", 'YYYY-MM-DD HH24:MI:SS.FF6'), '\\N')) AS canonical FROM SFNFR_20261104.INFA_ACCTDIM_LEGACY_SFNFR_20261104.DEMO_TARGET1_INS;
```

## Rerun

Bind SFNFR_ACCOUNT, SFNFR_USER, SFNFR_ROLE and SFNFR_PRIVATE_KEY securely,
then run from the repository root (no secrets are written to disk):

```sh
~/sfenv/bin/python tools/informatica_account_dim_snowflake.py load
~/dbtenv/bin/dbt build --project-dir dbt/m_demo_mapping2 --profiles-dir dbt/m_demo_mapping2 --target snowflake
~/sfenv/bin/python tools/informatica_account_dim_snowflake.py parity
```
