# Baseline SF_20261015_DS

The frozen legacy answer for one demo run of the Informatica plus SAS to dbt on Snowflake migration. Everything the migration children build is compared, row for row, against the tables this branch loads into `DEVIN_MIGRATION_DEMO.BASELINE_SF_20261015_DS`. Every Snowflake object of the run carries the tags `RUN = 'SF_20261015_DS'` and `EXPIRES = '2026-10-18T02:32:20Z'`, and `teardown.sh` drops them all.

## Snowflake objects of the run

| Kind | Name | Purpose |
|---|---|---|
| Schema | `DEVIN_MIGRATION_DEMO.SOURCE_SF_20261015_DS` | Legacy inputs: Informatica `DEMO_SOURCE1..5`, `DEMO_TARGET1` pre-state, `LKP_DEMO_SOURCE1..3`; SAS `ORA_DW_*`, `RAW_BANK_*`, `RAW_INS_*`, `CURATED_DAILY_TRANSACTIONS` (23 tables) |
| Schema | `DEVIN_MIGRATION_DEMO.BASELINE_SF_20261015_DS` | Every target the two baseline tools emit (24 tables) |
| Schema | `DEVIN_MIGRATION_DEMO.DBT_SF_20261015_DS` | Empty; the dbt children build here |
| Schema | `DEVIN_MIGRATION_DEMO.SCAI_SF_20261015_DS` | Empty; the SnowConvert AI replatform deploys here |
| Schema | `DEVIN_MIGRATION_DEMO.ORACLE_SF_20261015_DS` | Empty; converted Oracle objects go here if their tables can be stubbed |
| Warehouse | `SF_20261015_DS_WH` | X-Small, auto-suspend 60 s, auto-resume, created suspended. The only warehouse the run may use |
| Resource monitor | `SF_20261015_DS_MON` | 5 credit quota, notify at 80 percent, suspend at 100 percent, attached to the run warehouse only |
| Role | `SF_20261015_DS_DBT` | Usage on database and warehouse, select on SOURCE_ and BASELINE_, all privileges plus future grants on DBT_, SCAI_, ORACLE_, imported privileges on SNOWFLAKE for ACCOUNT_USAGE |
| Role | `SF_20261015_DS_READER` | Usage and select on the five schemas, monitor on the warehouse and the resource monitor |
| User | `SF_20261015_DS_DEMO` | `LEGACY_SERVICE`, default role `SF_20261015_DS_DBT`, default warehouse `SF_20261015_DS_WH`. The sessions and `scai` sign in as this user |
| User | `SF_20261015_DS_READER_USER` | `LEGACY_SERVICE`, default role `SF_20261015_DS_READER`. For Snowsight in the room |
| Tags | `DEVIN_MIGRATION_DEMO.PUBLIC.RUN`, `.EXPIRES` | Created once, shared by every run |

The demo user's credentials live in the Partner Demo - ViewOnly org as the secrets `SF_DEMO_USER`, `SF_DEMO_PASSWORD`, `SF_DEMO_ROLE`, `SF_DEMO_WAREHOUSE`, `SF_DEMO_DATABASE` and `SF_RUN_TOKEN`, added through `POST /v3/organizations/{org}/secrets`. The loader writes them to a mode 600 file under `/dev/shm` on the machine that ran it and nowhere else.

## Rebuild from a clean clone

You need Python 3.12 with `duckdb`, `pandas` and `snowflake-connector-python`, and `SNOWFLAKE_PAT` (or `SNOWFLAKE_PASSWORD`) for an ACCOUNTADMIN user of account `yd76133.us-east-2.aws` in the environment. Pick a fresh token for a fresh run; `SF_20261015_DS` is the one this branch documents.

```bash
git clone git@github.com:Cognition-Partner-Workshops/uc-informatica-sas-to-dbt.git
cd uc-informatica-sas-to-dbt
git checkout baseline/SF_20261015_DS
pip install duckdb pandas snowflake-connector-python

python3 tools/informatica_baseline.py        # writes baseline/informatica/*.csv
python3 tools/sas_baseline.py                # writes baseline/sas/*.csv
python3 baseline/SF_20261015_DS/load_baseline.py --token SF_20261015_DS
```

What each command printed on 2026-10-15 (full log in `load_report.json`):

| Step | Output | Time |
|---|---|---|
| `tools/informatica_baseline.py` | 7 CSVs: DEMO_TARGET1_INS 4, DEMO_TARGET1_UPD 3, DEMO_TARGET2 3, DEMO_TARGET21 3, DEMO_TARGET3 4, DEMO_TARGET5 2, DEMO_TARGET6 2 rows | 0.5 s |
| `tools/sas_baseline.py` | 17 CSVs, among them CUST_ACCOUNTS_DAILY 466, DAILY_TRANSACTIONS 18,903, RISK_SCORES 236, MONTHLY_RWA 59, CLAIMS_REGISTER 190, POLICY_VALUATION 166 rows | 0.9 s |
| loader: tags | `CREATE TAG IF NOT EXISTS` RUN and EXPIRES | 0.8 s |
| loader: warehouse and resource monitor | warehouse created suspended, monitor created and attached | 1.5 s |
| loader: schemas | five schemas | 1.0 s |
| loader: roles and grants | two roles, 91 grants | 31.0 s |
| loader: users | two users with generated passwords | 3.9 s |
| loader: load SOURCE | 23 tables, 22,969 rows (DuckDB to Parquet, PUT, COPY INTO) | 50.6 s |
| loader: load BASELINE | 24 tables, 21,141 rows | 58.7 s |
| loader: tags on objects | 10 `ALTER ... SET TAG` | 2.8 s |
| loader: proof query | row count per baseline table, saved as `room_query.sql` | 2.5 s |
| loader: credits | monitor at 0.00 of 5 the second it finished; the hourly metering row later read 0.078 credits | 0.8 s |
| **loader total** | | **153.6 s** |

The loader is idempotent: schemas, warehouse, roles and users are `IF NOT EXISTS`, tables are `CREATE OR REPLACE`, and the user passwords are regenerated on every run (so rerun it only when you also mean to rotate the ViewOnly secrets).

## Prove it in the room

`room_query.sql` is the query to paste into a Snowsight worksheet as `SF_20261015_DS_READER_USER`:

```sql
select 'CUST_ACCOUNTS_DAILY' as target, count(*) as row_count from DEVIN_MIGRATION_DEMO.BASELINE_SF_20261015_DS.CUST_ACCOUNTS_DAILY
union all
select 'DAILY_TRANSACTIONS', count(*) from DEVIN_MIGRATION_DEMO.BASELINE_SF_20261015_DS.DAILY_TRANSACTIONS
union all ...
```

It returns 24 rows and matches the CSV row counts in `baseline/informatica/` and `baseline/sas/` exactly. The same user can open Admin, Warehouses, `SF_20261015_DS_WH` and Admin, Resource Monitors, `SF_20261015_DS_MON` to see the quota and the credits used.

## Credits and cost of the baseline

The baseline load ran 323 queries on `SF_20261015_DS_WH` in about two minutes of warehouse time. The first metering row from `INFORMATION_SCHEMA.WAREHOUSE_METERING_HISTORY` is 0.078 credits (0.000 cloud services). The resource monitor shows 0.08 of 5.00.

## Teardown

```bash
python3 baseline/SF_20261015_DS/teardown.py --token SF_20261015_DS         # list what would go
bash baseline/SF_20261015_DS/teardown.sh --yes                             # drop it
```

The script lists the run's objects by name and by tag (ACCOUNT_USAGE.TAG_REFERENCES lags by up to two hours), drops warehouse, users, schemas, roles and monitor in that order, then prints `select count(*) from snowflake.account_usage.tag_references where tag_name in ('RUN','EXPIRES') and tag_value like 'SF_%'` and the warehouse's last metering row. The six `SF_DEMO_*` and `SF_RUN_TOKEN` secrets in ViewOnly are removed by hand afterwards (Settings, Secrets, or `DELETE /v3/organizations/{org}/secrets/{id}`).

## Branch contents

- `baseline/SF_20261015_DS/` : this README, `load_baseline.py`, `teardown.py`, `teardown.sh`, `room_query.sql`, `load_report.json`.
- `baseline/informatica/*.csv` and `baseline/sas/*.csv` : the frozen legacy answer, regenerated by the two tools and loaded as-is.
- `tools/sas_baseline.py`, `tools/sas_load_raw.py`, `tools/sas_lineage.py`, `tools/keys/sas_keys.json`, `docs/stm/sas_stm.*` : copied from branch `devin/sas-track`, where the SAS tooling lived until now. `main` carried the Informatica tools only.
- `legacy/sas/data/csv/raw_ins/*.csv` and `legacy/sas/data/generate_ins_seed_data.py` : the synthesized insurance inputs the SAS tooling depends on, also from `devin/sas-track`. They come out of `generate_ins_seed_data.py` with a fixed seed.

Nothing under `legacy/sas/programs/`, `legacy/informatica/` or `tools/parity_diff.py` changed.
