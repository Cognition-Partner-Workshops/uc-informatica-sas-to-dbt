# Unit Verification Packet — `daily_transaction_processing.sas`

Track: SAS → dbt (DuckDB, Snowflake-compatible SQL)
Legacy artifact: `legacy/sas/programs/daily_transaction_processing.sas`
Run date pinned to **31JAN2024** (`txn_date=&CURR_DT`).

## 1. Unit overview

Daily transaction ETL pipeline (Control-M job `BANK_DAILY_02`, daily 07:30, depends on
`load_customer_accounts.sas` / `BANK_DAILY_01`). The macro `%daily_transaction_processing(txn_date=)`:

1. **Validate feed** — reads `RAW_BANK.TXN_FEED_YYYYMMDD` (for 31JAN2024: `TXN_FEED_20240131`) and
   splits rows into `WORK.TXN_VALIDATED` / `WORK.TXN_REJECTED` with sequential rules (first failing
   rule wins, `RETURN` after each): missing `TRANSACTION_ID` / `ACCOUNT_ID` / `TRANSACTION_AMOUNT`,
   `abs(TRANSACTION_AMOUNT) > 10,000,000`, `TRANSACTION_TYPE` not in
   `('DEP','WDR','TRF','PMT','FEE','INT','ADJ','REV','CHG','REF')`, future-dated transactions.
2. **Enrich** — PROC SQL left join to `STG_BANK.CUST_ACCOUNTS_DAILY` on `ACCOUNT_ID`, pulling
   account/customer attributes, `CURRENT_BALANCE as PRE_TXN_BALANCE`, and a per-row
   `POST_TXN_BALANCE` (credit types add, debit types subtract `abs(amount)`), ordered by
   `ACCOUNT_ID, TRANSACTION_DATE, TRANSACTION_ID`.
3. **Running balance** — DATA step with `BY ACCOUNT_ID TRANSACTION_DATE TRANSACTION_ID` and
   `RETAIN RUNNING_BALANCE`, seeded from `PRE_TXN_BALANCE` on `first.ACCOUNT_ID`, then cumulatively
   adjusted per transaction type (DEP/INT/REF/REV add; WDR/PMT/FEE/CHG subtract `abs`; TRF/ADJ add).
4. **Anomaly detection** — 90-day per-account stats (`mean`/`std` of `abs(TRANSACTION_AMOUNT)`)
   from `CURATED.DAILY_TRANSACTIONS` *history only* (before today's append), then classifies each
   enriched transaction: `HIGH_AMOUNT` (z-score > 3), `OVERDRAFT` (`RUNNING_BALANCE < 0`, which in
   SAS missing-ordering also captures null balances), `LARGE_WITHDRAWAL` (WDR with
   `abs(amount) > PRE_TXN_BALANCE * 0.9`), `ORPHAN_ACCOUNT` (missing `CUSTOMER_ID`); keeps only
   anomalous rows (`HAVING ANOMALY_TYPE ne ''`).
5. **Load curated layer** — `PROC APPEND FORCE` of the day's transactions onto
   `CURATED.DAILY_TRANSACTIONS` (FORCE drops the enrichment columns, keeping the 10 base feed
   columns) and of anomalies onto `CURATED.TXN_ANOMALIES`.
6. **Persist balances** — rewrites `CURATED.RUNNING_BALANCES` with
   `ACCOUNT_ID, TRANSACTION_DATE, TRANSACTION_ID, RUNNING_BALANCE` for the day's feed.

**Sources:** `RAW_BANK.TXN_FEED_20240131`, `STG_BANK.CUST_ACCOUNTS_DAILY`,
`CURATED.DAILY_TRANSACTIONS` (history, for z-score stats), `BANKING.FORMATS`.
**Targets:** `CURATED.DAILY_TRANSACTIONS`, `CURATED.TXN_ANOMALIES`, `CURATED.RUNNING_BALANCES`.

dbt implementation (existing on `devin/sas-track`): `stg_txn_feed`, `stg_daily_transactions_hist`
→ `int_txn_validated`, `int_txn_stats`, `int_txn_with_balance` → marts `daily_transactions`,
`running_balances`, `txn_anomalies`. The RETAIN/BY-group running balance is a window
`sum(bal_delta) over (partition by account_id order by transaction_date, transaction_id rows
between unbounded preceding and current row)` seeded from the snapshot balance.

## 2. STM excerpt (from `docs/stm/sas_stm.md`, section `daily_transaction_processing`)

**Macro:** `%daily_transaction_processing` — parameters: `txn_date=&CURR_DT`

**Inputs:** `CURATED.DAILY_TRANSACTIONS`, `CURATED.RUNNING_BALANCES`, `CURATED.TXN_ANOMALIES`, `RAW_BANK.&txn_ds`, `STG_BANK.CUST_ACCOUNTS_DAILY` (feed pattern: `TXN_FEED_YYYYMMDD`)
**Persistent outputs:** `CURATED.DAILY_TRANSACTIONS`, `CURATED.RUNNING_BALANCES`, `CURATED.TXN_ANOMALIES`

| Output Dataset | Column | Derivation | Source(s) |
|---|---|---|---|
| WORK.TXN_VALIDATED / WORK.TXN_REJECTED | *(step)* | DROP (all outputs): REJECT_REASON | RAW_BANK.&TXN_DS |
| WORK.TXN_VALIDATED / WORK.TXN_REJECTED | REJECT_REASON | if `missing(TRANSACTION_ID)` then `'Missing TRANSACTION_ID'` | RAW_BANK.&TXN_DS |
| WORK.TXN_VALIDATED / WORK.TXN_REJECTED | REJECT_REASON | if `missing(ACCOUNT_ID)` then `'Missing ACCOUNT_ID'` | RAW_BANK.&TXN_DS |
| WORK.TXN_VALIDATED / WORK.TXN_REJECTED | REJECT_REASON | if `missing(TRANSACTION_AMOUNT)` then `'Missing TRANSACTION_AMOUNT'` | RAW_BANK.&TXN_DS |
| WORK.TXN_VALIDATED / WORK.TXN_REJECTED | REJECT_REASON | if `abs(TRANSACTION_AMOUNT) > 10000000` then `catx(' ', 'Amount exceeds threshold:', put(TRANSACTION_AMOUNT, dollar18.2))` | RAW_BANK.&TXN_DS |
| WORK.TXN_VALIDATED / WORK.TXN_REJECTED | REJECT_REASON | if `TRANSACTION_TYPE not in ('DEP','WDR','TRF','PMT','FEE','INT','ADJ','REV','CHG','REF')` then `catx(' ', 'Invalid transaction type:', TRANSACTION_TYPE)` | RAW_BANK.&TXN_DS |
| WORK.TXN_VALIDATED / WORK.TXN_REJECTED | REJECT_REASON | if `TRANSACTION_DATE > "&txn_date"d` then `catx(' ', 'Future dated:', put(TRANSACTION_DATE, date9.))` | RAW_BANK.&TXN_DS |
| WORK.TXN_REJECTED | *(row output)* | when `missing(TRANSACTION_ID)` | RAW_BANK.&TXN_DS |
| WORK.TXN_REJECTED | *(row output)* | when `missing(ACCOUNT_ID)` | RAW_BANK.&TXN_DS |
| WORK.TXN_REJECTED | *(row output)* | when `missing(TRANSACTION_AMOUNT)` | RAW_BANK.&TXN_DS |
| WORK.TXN_REJECTED | *(row output)* | when `abs(TRANSACTION_AMOUNT) > 10000000` | RAW_BANK.&TXN_DS |
| WORK.TXN_REJECTED | *(row output)* | when `TRANSACTION_TYPE not in ('DEP','WDR','TRF','PMT','FEE','INT','ADJ','REV','CHG','REF')` | RAW_BANK.&TXN_DS |
| WORK.TXN_REJECTED | *(row output)* | when `TRANSACTION_DATE > "&txn_date"d` | RAW_BANK.&TXN_DS |
| WORK.TXN_VALIDATED | *(row output)* | always | RAW_BANK.&TXN_DS |
| WORK.TXN_ENRICHED | *(step)* | left join STG_BANK.CUST_ACCOUNTS_DAILY a on t.ACCOUNT_ID = a.ACCOUNT_ID | WORK.TXN_VALIDATED t; STG_BANK.CUST_ACCOUNTS_DAILY a |
| WORK.TXN_ENRICHED | T.* | `pass-through (all columns)` | WORK.TXN_VALIDATED t; STG_BANK.CUST_ACCOUNTS_DAILY a |
| WORK.TXN_ENRICHED | ACCOUNT_TYPE | `a.ACCOUNT_TYPE` | WORK.TXN_VALIDATED t; STG_BANK.CUST_ACCOUNTS_DAILY a |
| WORK.TXN_ENRICHED | CUSTOMER_ID | `a.CUSTOMER_ID` | WORK.TXN_VALIDATED t; STG_BANK.CUST_ACCOUNTS_DAILY a |
| WORK.TXN_ENRICHED | CUSTOMER_SEGMENT | `a.CUSTOMER_SEGMENT` | WORK.TXN_VALIDATED t; STG_BANK.CUST_ACCOUNTS_DAILY a |
| WORK.TXN_ENRICHED | REGION_CODE | `a.REGION_CODE` | WORK.TXN_VALIDATED t; STG_BANK.CUST_ACCOUNTS_DAILY a |
| WORK.TXN_ENRICHED | BRANCH_ID | `a.BRANCH_ID` | WORK.TXN_VALIDATED t; STG_BANK.CUST_ACCOUNTS_DAILY a |
| WORK.TXN_ENRICHED | PRE_TXN_BALANCE | `a.CURRENT_BALANCE` | WORK.TXN_VALIDATED t; STG_BANK.CUST_ACCOUNTS_DAILY a |
| WORK.TXN_ENRICHED | POST_TXN_BALANCE | `case when t.TRANSACTION_TYPE in ('DEP','INT','REF','REV') then a.CURRENT_BALANCE + t.TRANSACTION_AMOUNT when t.TRANSACTION_TYPE in ('WDR','PMT','FEE','CHG') then a.CURRENT_BALANCE - abs(t.TRANSACTION_AMOUNT) when t.TRANSACTION_TYPE in ('TRF','ADJ') then a.CURRENT_BALANCE + t.TRANSACTION_AMOUNT else a.CURRENT_BALANCE end` | WORK.TXN_VALIDATED t; STG_BANK.CUST_ACCOUNTS_DAILY a |
| WORK.TXN_ENRICHED | RISK_RATING | `a.RISK_RATING` | WORK.TXN_VALIDATED t; STG_BANK.CUST_ACCOUNTS_DAILY a |
| WORK.TXN_WITH_BALANCE | *(step)* | BY ACCOUNT_ID TRANSACTION_DATE TRANSACTION_ID; RETAIN RUNNING_BALANCE | WORK.TXN_ENRICHED |
| WORK.TXN_WITH_BALANCE | RUNNING_BALANCE | if `first.ACCOUNT_ID` then `PRE_TXN_BALANCE` | WORK.TXN_ENRICHED |
| WORK.TXN_WITH_BALANCE | RUNNING_BALANCE | if `TRANSACTION_TYPE in ('DEP','INT','REF','REV')` then `RUNNING_BALANCE + TRANSACTION_AMOUNT` | WORK.TXN_ENRICHED |
| WORK.TXN_WITH_BALANCE | RUNNING_BALANCE | if `ELSE TRANSACTION_TYPE in ('WDR','PMT','FEE','CHG')` then `RUNNING_BALANCE - abs(TRANSACTION_AMOUNT)` | WORK.TXN_ENRICHED |
| WORK.TXN_WITH_BALANCE | RUNNING_BALANCE | if `ELSE TRANSACTION_TYPE in ('TRF','ADJ')` then `RUNNING_BALANCE + TRANSACTION_AMOUNT` | WORK.TXN_ENRICHED |
| WORK.TXN_WITH_BALANCE | RUNNING_BALANCE | display format `dollar18.2` | WORK.TXN_ENRICHED |
| WORK.TXN_STATS | *(step)* | where TRANSACTION_DATE >= intnx('day', "&txn_date"d, -90); group by ACCOUNT_ID | CURATED.DAILY_TRANSACTIONS where |
| WORK.TXN_STATS | ACCOUNT_ID | `ACCOUNT_ID` | CURATED.DAILY_TRANSACTIONS where |
| WORK.TXN_STATS | AVG_TXN_AMT | `mean(abs(TRANSACTION_AMOUNT))` | CURATED.DAILY_TRANSACTIONS where |
| WORK.TXN_STATS | STD_TXN_AMT | `std(abs(TRANSACTION_AMOUNT))` | CURATED.DAILY_TRANSACTIONS where |
| WORK.TXN_STATS | TXN_COUNT | `count(*)` | CURATED.DAILY_TRANSACTIONS where |
| WORK.TXN_ANOMALIES | *(step)* | left join WORK.TXN_STATS s on e.ACCOUNT_ID = s.ACCOUNT_ID; having ANOMALY_TYPE ne '' | WORK.TXN_WITH_BALANCE e; WORK.TXN_STATS s |
| WORK.TXN_ANOMALIES | E.* | `pass-through (all columns)` | WORK.TXN_WITH_BALANCE e; WORK.TXN_STATS s |
| WORK.TXN_ANOMALIES | AVG_TXN_AMT | `s.AVG_TXN_AMT` | WORK.TXN_WITH_BALANCE e; WORK.TXN_STATS s |
| WORK.TXN_ANOMALIES | STD_TXN_AMT | `s.STD_TXN_AMT` | WORK.TXN_WITH_BALANCE e; WORK.TXN_STATS s |
| WORK.TXN_ANOMALIES | Z_SCORE | `case when s.STD_TXN_AMT > 0 then (abs(e.TRANSACTION_AMOUNT) - s.AVG_TXN_AMT) / s.STD_TXN_AMT else . end` | WORK.TXN_WITH_BALANCE e; WORK.TXN_STATS s |
| WORK.TXN_ANOMALIES | ANOMALY_TYPE | `case when calculated Z_SCORE > 3 then 'HIGH_AMOUNT' when e.RUNNING_BALANCE < 0 then 'OVERDRAFT' when e.TRANSACTION_TYPE = 'WDR' and abs(e.TRANSACTION_AMOUNT) > e.PRE_TXN_BALANCE * 0.9 then 'LARGE_WITHDRAWAL' when missing(e.CUSTOMER_ID) then 'ORPHAN_ACCOUNT' else '' end` | WORK.TXN_WITH_BALANCE e; WORK.TXN_STATS s |
| CURATED.DAILY_TRANSACTIONS | *(all columns of base)* | PROC APPEND FORCE (extra columns dropped) | WORK.TXN_WITH_BALANCE |
| CURATED.TXN_ANOMALIES | *(all columns of base)* | PROC APPEND FORCE (extra columns dropped) | WORK.TXN_ANOMALIES |

**Notes / ambiguities:**
- PROC SQL uses SAS missing-value ordering: a missing RUNNING_BALANCE satisfies `RUNNING_BALANCE < 0`, so transactions on accounts absent from the snapshot (null balances) are classified OVERDRAFT — the ORPHAN_ACCOUNT branch is unreachable for them. The migrated SQL reproduces this with explicit IS NULL handling.
- Z-score statistics are computed from CURATED.DAILY_TRANSACTIONS *before* the day's feed is appended, i.e. from history only. STD() in PROC SQL is the sample standard deviation.
- PROC APPEND FORCE drops the enrichment columns not present in the existing CURATED.DAILY_TRANSACTIONS structure, so the final curated table keeps only the 10 original feed columns.
- Validation rules are sequential with RETURN: a row is rejected by the first failing rule only.

## 3. Verification evidence

Commands run (from repo root; dbt from inside `dbt/sas`):

```
python3 tools/sas_lineage.py
python3 tools/sas_baseline.py
python3 tools/sas_load_raw.py
(cd dbt/sas && dbt build --profiles-dir . --no-partial-parse)
python3 tools/parity_diff.py --baseline baseline/sas --actual dbt/sas/dev.duckdb \
  --schema main --keys tools/keys/sas_keys.json --report /tmp/parity.md
```

Baseline runner output for this unit's inputs/targets:

```
  loaded raw_bank.txn_feed_20240131: 622 rows
  loaded curated_src.daily_transactions: 18293 rows
  baseline TXN_ANOMALIES: 46 rows
  baseline DAILY_TRANSACTIONS: 18903 rows
  baseline RUNNING_BALANCES: 610 rows
```

(622 feed rows → 610 validated + 12 rejected; 18293 history + 610 = 18903 curated transactions.)

`dbt build` completed green — `Done. PASS=117 WARN=0 ERROR=0 SKIP=0 NO-OP=0 TOTAL=117`.
Models and schema tests for this unit:

```
OK created sql view model main.stg_daily_transactions_hist
OK created sql view model main.stg_txn_feed
OK created sql view model main.int_txn_stats
OK created sql view model main.int_txn_validated
OK created sql view model main.int_txn_with_balance
OK created sql table model main.daily_transactions
OK created sql table model main.running_balances
OK created sql table model main.txn_anomalies
PASS accepted_values_daily_transactions_transaction_type__DEP__WDR__TRF__PMT__FEE__INT__ADJ__REV__CHG__REF
PASS not_null_daily_transactions_account_id
PASS not_null_daily_transactions_transaction_id
PASS unique_daily_transactions_transaction_id
PASS not_null_running_balances_account_id
PASS not_null_running_balances_transaction_id
PASS unique_running_balances_transaction_id
PASS accepted_values_txn_anomalies_anomaly_type__HIGH_AMOUNT__OVERDRAFT__LARGE_WITHDRAWAL__ORPHAN_ACCOUNT
PASS not_null_txn_anomalies_anomaly_type
PASS not_null_txn_anomalies_transaction_id
PASS unique_txn_anomalies_transaction_id
```

Parity report sections for this unit's targets (from `/tmp/parity.md`):

```
## DAILY_TRANSACTIONS
- rows: baseline=18903 actual=18903
- columns compared: 10
- result: **MATCH** (all values within tolerance)

## RUNNING_BALANCES
- rows: baseline=610 actual=610
- columns compared: 4
- result: **MATCH** (all values within tolerance)

## TXN_ANOMALIES
- rows: baseline=46 actual=46
- columns compared: 23
- result: **MATCH** (all values within tolerance)

**Overall: PARITY VERIFIED**
```

**Parity exit code: 0**

| Target | Baseline rows | Actual (dbt) rows | Result |
|---|---|---|---|
| CURATED.DAILY_TRANSACTIONS (`daily_transactions`) | 18,903 | 18,903 | MATCH |
| CURATED.RUNNING_BALANCES (`running_balances`) | 610 | 610 | MATCH |
| CURATED.TXN_ANOMALIES (`txn_anomalies`) | 46 | 46 | MATCH |

## 4. Snowflake notes

Items in this unit's SQL a Snowflake deployment should review:

- **Sample vs. population standard deviation** — `int_txn_stats` uses `stddev_samp` to match SAS
  PROC SQL `std()`. Snowflake's bare `STDDEV` is also sample stddev, but keep the explicit
  `STDDEV_SAMP` to avoid ambiguity.
- **Date interval arithmetic** — `int_txn_stats` filters with
  `cast('...' as date) - interval '90 days'`. Snowflake supports `INTERVAL '90 days'`, but
  `DATEADD(day, -90, ...)` is the more idiomatic/robust form if this is ever parameterized.
- **NULL ordering semantics** — the SAS missing-value quirk (null `RUNNING_BALANCE` →
  `OVERDRAFT`; null `PRE_TXN_BALANCE` makes the LARGE_WITHDRAWAL comparison true) is encoded with
  explicit `IS NULL` predicates in `txn_anomalies.sql`, so it ports to Snowflake unchanged — do not
  "simplify" these predicates, as Snowflake three-valued logic would otherwise drop those rows.
- **Window function determinism** — the running balance uses
  `sum(...) over (partition by account_id order by transaction_date, transaction_id rows between
  unbounded preceding and current row)`. `TRANSACTION_ID` is unique within an account, so the
  ordering is total and results are deterministic on Snowflake; the explicit `ROWS` frame avoids
  the default `RANGE` frame's peer-row ties.
- **Division by zero** — the z-score guard `when s.std_txn_amt > 0` prevents divide-by-zero and
  yields NULL otherwise (SAS `.`), which behaves identically on Snowflake.
- **`union all` append semantics** — `daily_transactions` models PROC APPEND FORCE as a
  `union all` of history + day's feed, keeping only the 10 base columns. In an incremental
  Snowflake deployment this would become an `insert`/dbt incremental model keyed on
  `transaction_id`; the current full-rebuild form is correct but rescans history each run.
- **Display formats only** — `dollar18.2` / `date9.` formats in the legacy program are
  display-layer only and intentionally not migrated; values are stored as raw numerics/dates.
