# m_demo_mapping1 → dbt (DuckDB)

dbt conversion of Informatica mapping `m_demo_mapping1` from
`legacy/informatica/wf_demo_mapping.XML` (group `infa_m1`). Builds DEMO_TARGET3,
DEMO_TARGET5 and DEMO_TARGET6 as tables in schema `main`.

No Snowflake credentials exist for this run, so reconciliation runs on DuckDB with
dbt-duckdb. Nothing here connects to Snowflake.

## Layout

| Path | Contents |
|---|---|
| `macros/load_infa_inputs.sql` | `dbt run-operation load_infa_inputs`: lands the seed CSVs from `legacy/informatica/data/` into schema `infa_src_infa_m1` with explicit column types; lookup tables get `SEED_ROW` (physical seed order) |
| `models/staging/` | `sq_demo_source4` (SQL override: inner join, pinned SYSTIMESTAMP, STRCMP dropped), `sq_demo_source5` — views in `infa_stg_infa_m1` |
| `models/intermediate/` | `lkp_trans1/2/3` (Use Last Value = highest `SEED_ROW` per key), `exp_trans1` (exp_TRANS + exp_TRANS1 + connected lookups) — views in `infa_stg_infa_m1` |
| `models/targets/` | `DEMO_TARGET5` (rtr_TRANS `ACCT_TYP != 'SB'`), `DEMO_TARGET6` (rtr_TRANS `ACCT_TYP = 'SB'` → agg_TRANS → SEQ_GEN), `DEMO_TARGET3` (exp_TRANS2) — tables in `main` |
| `docs/semantics_review.md` | Independent re-derivation of the lookup/router/aggregator semantics from the XML and review of these models |

Semantics follow the accepted baseline (`tools/informatica_baseline.py`, business date
2024-01-31): rows with NULL `ACCT_TYP` (ACCT_ID 1005) hit the unconnected DEFAULT1 router
group and are dropped; agg_TRANS pass-through ports take the highest `TX_ID` row per
account; `ACCT_KEY` starts at SEQ_GEN Current Value 281; `SELL_ST_DT` is NULL because
`TO_DATE(TO_CHAR(SYSDATE),'DD/MM/YYYY')` does not parse. Values keep the baseline's
types (e.g. `TX_AMT` keeps decimals although the Oracle target is `number(38,0)`).
Other accepted deviations from the Oracle target DDL: `ACCT_DESC` values exceed
`varchar2(10)` and DEMO_TARGET3 `number(15)` columns carry non-numeric text. A malformed
`SELL_ED_DT` fails the build (PowerCenter would reject only the row). Full XML re-derivation
and the baseline-vs-XML divergence list: `docs/semantics_review.md`; singular tests in
`tests/` pin the 1005 router drop and the lkp_TRANS1 last-value tie (1002 -> `DR`).

## Run

From the repo root (Python 3.11+):

```bash
python3 -m pip install -r requirements.txt "dbt-core~=1.9.0" "dbt-duckdb~=1.9.0"   # duckdb stays 1.4.1
cd dbt/informatica_snowflake/m_demo_mapping1
export DBT_PROFILES_DIR=$PWD
export INFA_DUCKDB_PATH=$PWD/target/infa.duckdb   # absolute, so the parity step finds it
dbt run-operation load_infa_inputs    # seed inputs -> infa_src_infa_m1
dbt build                             # models + tests -> main.DEMO_TARGET3/5/6
cd ../../..
python3 tools/parity_nfr.py --token INFA_M1 --duckdb "$INFA_DUCKDB_PATH" --schema main --report reports/infa_m1.md
```

`parity_nfr.py` exits 1 because the other mappings' targets (DEMO_TARGET1_INS/UPD,
DEMO_TARGET2/21) are absent from this database; DEMO_TARGET3/5/6 must be GREEN.
`INFA_DATA_DIR` overrides the seed directory (default `../../../legacy/informatica/data`,
relative to this project directory).
