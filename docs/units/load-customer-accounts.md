# Unit Verification Packet — `load_customer_accounts.sas`

## 1. Unit overview

`legacy/sas/programs/load_customer_accounts.sas` produces the **daily customer account
snapshot** (Control-M job `BANK_DAILY_01`, daily 06:00). The `%load_customer_accounts`
macro (parameters `run_date=&CURR_DT`, `region=ALL`) runs four steps:

1. **Extract (PROC SQL)** — inner join `ORA_DW.CUST_ACCOUNTS` to
   `ORA_DW.CUST_DEMOGRAPHICS` on `CUSTOMER_ID`, filtered to
   `ACCOUNT_STATUS not in ('W','C')` and `OPEN_DATE <= "&run_date"d`
   (optional `REGION_CODE` filter when `region ne ALL`), into `WORK.ACCT_RAW`.
2. **Business rules / derivations (DATA step)** — derives `ACCT_AGE_MONTHS`
   (`intck('month', OPEN_DATE, run_date)`), `DAYS_INACTIVE`, `UTILIZATION_PCT`
   (revolving types `CC/LOC/HELC` with `CREDIT_LIMIT > 0`), `DORMANCY_FLAG`
   (`DAYS_INACTIVE > 365` and status `A`), `HIGH_BALANCE_FLAG`
   (`CURRENT_BALANCE >= 250000`), plus `SNAPSHOT_DATE` and `LOAD_TIMESTAMP`.
   Three sequential data-quality rules each `output` an exception row:
   `NEG_BAL` (negative balance on deposit types `CHK/SAV/MMA/CD`),
   `HIGH_UTIL` (`UTILIZATION_PCT > 95`), `NO_RISK` (missing `RISK_RATING`).
   Every row is output to the snapshot; exception rows also go to
   `WORK.ACCT_EXCEPTIONS`. A DATA-step `drop EXCEPTION_CODE EXCEPTION_DESC;`
   applies to **both** outputs, and exception rows are output **before**
   `SNAPSHOT_DATE`/`LOAD_TIMESTAMP` are assigned (so those are null on them).
3. **Exception load** — `WORK.ACCT_EXCEPTIONS` is inserted into
   `STG_BANK.ACCT_EXCEPTIONS` (with an email alert when > 100 exceptions).
4. **Summary (PROC MEANS)** — `WORK.ACCT_SUMMARY` by
   `ACCOUNT_TYPE × REGION_CODE` (work-only, not persisted).

**Sources:** `ORA_DW.CUST_ACCOUNTS`, `ORA_DW.CUST_DEMOGRAPHICS`
(`RAW_BANK.DAILY_RATES` is declared in the header but never referenced in code).
**Persistent targets:** `STG_BANK.CUST_ACCOUNTS_DAILY`, `STG_BANK.ACCT_EXCEPTIONS`.

dbt implementation: `staging/stg_cust_accounts.sql`, `staging/stg_cust_demographics.sql`
→ `intermediate/int_acct_base.sql` → marts `cust_accounts_daily.sql` and
`acct_exceptions.sql` (PROC FORMAT display recodes materialized as `*_DESC`
columns via `fmt_*` seed lookups).

## 2. STM excerpt (from `docs/stm/sas_stm.md`)

## load_customer_accounts

**Purpose:** Extract customer account data from Oracle DW, apply business rules, compute derived metrics, and load into the staging layer for downstream reporting.

**Macro:** `%load_customer_accounts` — parameters: `run_date=&CURR_DT`, `region=ALL`

**Inputs:** `ORA_DW.CUST_ACCOUNTS`, `ORA_DW.CUST_DEMOGRAPHICS`, `STG_BANK.ACCT_EXCEPTIONS`, `STG_BANK.CUST_ACCOUNTS_DAILY`
**Persistent outputs:** `STG_BANK.ACCT_EXCEPTIONS`, `STG_BANK.CUST_ACCOUNTS_DAILY`

| Output Dataset | Column | Derivation | Source(s) |
|---|---|---|---|
| WORK.ACCT_RAW | *(step)* | inner join ORA_DW.CUST_DEMOGRAPHICS d on a.CUSTOMER_ID = d.CUSTOMER_ID; where a.ACCOUNT_STATUS not in ('W', 'C') and a.OPEN_DATE <= "&run_date"d %if &region ne ALL %then %do | ORA_DW.CUST_ACCOUNTS a; ORA_DW.CUST_DEMOGRAPHICS d |
| WORK.ACCT_RAW | ACCOUNT_ID | `a.ACCOUNT_ID` | ORA_DW.CUST_ACCOUNTS a; ORA_DW.CUST_DEMOGRAPHICS d |
| WORK.ACCT_RAW | CUSTOMER_ID | `a.CUSTOMER_ID` | ORA_DW.CUST_ACCOUNTS a; ORA_DW.CUST_DEMOGRAPHICS d |
| WORK.ACCT_RAW | ACCOUNT_TYPE | `a.ACCOUNT_TYPE` | ORA_DW.CUST_ACCOUNTS a; ORA_DW.CUST_DEMOGRAPHICS d |
| WORK.ACCT_RAW | ACCOUNT_STATUS | `a.ACCOUNT_STATUS` | ORA_DW.CUST_ACCOUNTS a; ORA_DW.CUST_DEMOGRAPHICS d |
| WORK.ACCT_RAW | OPEN_DATE | `a.OPEN_DATE` | ORA_DW.CUST_ACCOUNTS a; ORA_DW.CUST_DEMOGRAPHICS d |
| WORK.ACCT_RAW | CLOSE_DATE | `a.CLOSE_DATE` | ORA_DW.CUST_ACCOUNTS a; ORA_DW.CUST_DEMOGRAPHICS d |
| WORK.ACCT_RAW | CURRENT_BALANCE | `a.CURRENT_BALANCE` | ORA_DW.CUST_ACCOUNTS a; ORA_DW.CUST_DEMOGRAPHICS d |
| WORK.ACCT_RAW | AVAILABLE_BALANCE | `a.AVAILABLE_BALANCE` | ORA_DW.CUST_ACCOUNTS a; ORA_DW.CUST_DEMOGRAPHICS d |
| WORK.ACCT_RAW | CREDIT_LIMIT | `a.CREDIT_LIMIT` | ORA_DW.CUST_ACCOUNTS a; ORA_DW.CUST_DEMOGRAPHICS d |
| WORK.ACCT_RAW | INTEREST_RATE | `a.INTEREST_RATE` | ORA_DW.CUST_ACCOUNTS a; ORA_DW.CUST_DEMOGRAPHICS d |
| WORK.ACCT_RAW | BRANCH_ID | `a.BRANCH_ID` | ORA_DW.CUST_ACCOUNTS a; ORA_DW.CUST_DEMOGRAPHICS d |
| WORK.ACCT_RAW | OFFICER_ID | `a.OFFICER_ID` | ORA_DW.CUST_ACCOUNTS a; ORA_DW.CUST_DEMOGRAPHICS d |
| WORK.ACCT_RAW | LAST_ACTIVITY_DATE | `a.LAST_ACTIVITY_DATE` | ORA_DW.CUST_ACCOUNTS a; ORA_DW.CUST_DEMOGRAPHICS d |
| WORK.ACCT_RAW | FIRST_NAME | `d.FIRST_NAME` | ORA_DW.CUST_ACCOUNTS a; ORA_DW.CUST_DEMOGRAPHICS d |
| WORK.ACCT_RAW | LAST_NAME | `d.LAST_NAME` | ORA_DW.CUST_ACCOUNTS a; ORA_DW.CUST_DEMOGRAPHICS d |
| WORK.ACCT_RAW | SSN_HASH | `d.SSN_HASH` | ORA_DW.CUST_ACCOUNTS a; ORA_DW.CUST_DEMOGRAPHICS d |
| WORK.ACCT_RAW | DATE_OF_BIRTH | `d.DATE_OF_BIRTH` | ORA_DW.CUST_ACCOUNTS a; ORA_DW.CUST_DEMOGRAPHICS d |
| WORK.ACCT_RAW | CUSTOMER_SEGMENT | `d.CUSTOMER_SEGMENT` | ORA_DW.CUST_ACCOUNTS a; ORA_DW.CUST_DEMOGRAPHICS d |
| WORK.ACCT_RAW | RISK_RATING | `d.RISK_RATING` | ORA_DW.CUST_ACCOUNTS a; ORA_DW.CUST_DEMOGRAPHICS d |
| WORK.ACCT_RAW | REGION_CODE | `d.REGION_CODE` | ORA_DW.CUST_ACCOUNTS a; ORA_DW.CUST_DEMOGRAPHICS d |
| WORK.ACCT_RAW | PRIMARY_EMAIL | `d.PRIMARY_EMAIL` | ORA_DW.CUST_ACCOUNTS a; ORA_DW.CUST_DEMOGRAPHICS d |
| WORK.ACCT_RAW | PHONE_NUMBER | `d.PHONE_NUMBER` | ORA_DW.CUST_ACCOUNTS a; ORA_DW.CUST_DEMOGRAPHICS d |
| STG_BANK.CUST_ACCOUNTS_DAILY / WORK.ACCT_EXCEPTIONS | *(step)* | DROP (all outputs): EXCEPTION_CODE EXCEPTION_DESC | WORK.ACCT_RAW |
| STG_BANK.CUST_ACCOUNTS_DAILY / WORK.ACCT_EXCEPTIONS | ACCT_AGE_MONTHS | `intck('month', OPEN_DATE, "&run_date"d)` | WORK.ACCT_RAW |
| STG_BANK.CUST_ACCOUNTS_DAILY / WORK.ACCT_EXCEPTIONS | DAYS_INACTIVE | `"&run_date"d - LAST_ACTIVITY_DATE` | WORK.ACCT_RAW |
| STG_BANK.CUST_ACCOUNTS_DAILY / WORK.ACCT_EXCEPTIONS | UTILIZATION_PCT | if `ACCOUNT_TYPE in ('CC', 'LOC', 'HELC') and CREDIT_LIMIT > 0` then `(CURRENT_BALANCE / CREDIT_LIMIT) * 100` | WORK.ACCT_RAW |
| STG_BANK.CUST_ACCOUNTS_DAILY / WORK.ACCT_EXCEPTIONS | UTILIZATION_PCT | if `NOT (ACCOUNT_TYPE in ('CC', 'LOC', 'HELC') and CREDIT_LIMIT > 0)` then `.` | WORK.ACCT_RAW |
| STG_BANK.CUST_ACCOUNTS_DAILY / WORK.ACCT_EXCEPTIONS | DORMANCY_FLAG | if `DAYS_INACTIVE > 365 and ACCOUNT_STATUS = 'A'` then `'Y'` | WORK.ACCT_RAW |
| STG_BANK.CUST_ACCOUNTS_DAILY / WORK.ACCT_EXCEPTIONS | DORMANCY_FLAG | if `NOT (DAYS_INACTIVE > 365 and ACCOUNT_STATUS = 'A')` then `'N'` | WORK.ACCT_RAW |
| STG_BANK.CUST_ACCOUNTS_DAILY / WORK.ACCT_EXCEPTIONS | HIGH_BALANCE_FLAG | if `CURRENT_BALANCE >= 250000` then `'Y'` | WORK.ACCT_RAW |
| STG_BANK.CUST_ACCOUNTS_DAILY / WORK.ACCT_EXCEPTIONS | HIGH_BALANCE_FLAG | if `NOT (CURRENT_BALANCE >= 250000)` then `'N'` | WORK.ACCT_RAW |
| STG_BANK.CUST_ACCOUNTS_DAILY / WORK.ACCT_EXCEPTIONS | EXCEPTION_CODE | if `ACCOUNT_TYPE in ('CHK', 'SAV', 'MMA', 'CD') and CURRENT_BALANCE < 0` then `'NEG_BAL'` | WORK.ACCT_RAW |
| STG_BANK.CUST_ACCOUNTS_DAILY / WORK.ACCT_EXCEPTIONS | EXCEPTION_DESC | if `ACCOUNT_TYPE in ('CHK', 'SAV', 'MMA', 'CD') and CURRENT_BALANCE < 0` then `catx(' ', 'Negative balance', put(CURRENT_BALANCE, dollar18.2), 'on deposit account', ACCOUNT_ID)` | WORK.ACCT_RAW |
| STG_BANK.CUST_ACCOUNTS_DAILY / WORK.ACCT_EXCEPTIONS | EXCEPTION_CODE | if `UTILIZATION_PCT > 95` then `'HIGH_UTIL'` | WORK.ACCT_RAW |
| STG_BANK.CUST_ACCOUNTS_DAILY / WORK.ACCT_EXCEPTIONS | EXCEPTION_DESC | if `UTILIZATION_PCT > 95` then `catx(' ', 'Utilization at', put(UTILIZATION_PCT, 5.1), '%', 'for account', ACCOUNT_ID)` | WORK.ACCT_RAW |
| STG_BANK.CUST_ACCOUNTS_DAILY / WORK.ACCT_EXCEPTIONS | EXCEPTION_CODE | if `RISK_RATING = .` then `'NO_RISK'` | WORK.ACCT_RAW |
| STG_BANK.CUST_ACCOUNTS_DAILY / WORK.ACCT_EXCEPTIONS | EXCEPTION_DESC | if `RISK_RATING = .` then `catx(' ', 'Missing risk rating for customer', CUSTOMER_ID)` | WORK.ACCT_RAW |
| STG_BANK.CUST_ACCOUNTS_DAILY / WORK.ACCT_EXCEPTIONS | SNAPSHOT_DATE | `"&run_date"d` | WORK.ACCT_RAW |
| STG_BANK.CUST_ACCOUNTS_DAILY / WORK.ACCT_EXCEPTIONS | LOAD_TIMESTAMP | `datetime()` | WORK.ACCT_RAW |
| WORK.ACCT_EXCEPTIONS | *(row output)* | when `ACCOUNT_TYPE in ('CHK', 'SAV', 'MMA', 'CD') and CURRENT_BALANCE < 0` | WORK.ACCT_RAW |
| WORK.ACCT_EXCEPTIONS | *(row output)* | when `UTILIZATION_PCT > 95` | WORK.ACCT_RAW |
| WORK.ACCT_EXCEPTIONS | *(row output)* | when `RISK_RATING = .` | WORK.ACCT_RAW |
| STG_BANK.CUST_ACCOUNTS_DAILY | *(row output)* | always | WORK.ACCT_RAW |
| STG_BANK.CUST_ACCOUNTS_DAILY / WORK.ACCT_EXCEPTIONS | ACCOUNT_TYPE | display format `$ACCTTYPE.` | WORK.ACCT_RAW |
| STG_BANK.CUST_ACCOUNTS_DAILY / WORK.ACCT_EXCEPTIONS | ACCOUNT_STATUS | display format `$ACCTSTAT.` | WORK.ACCT_RAW |
| STG_BANK.CUST_ACCOUNTS_DAILY / WORK.ACCT_EXCEPTIONS | RISK_RATING | display format `RISKRATE.` | WORK.ACCT_RAW |
| STG_BANK.CUST_ACCOUNTS_DAILY / WORK.ACCT_EXCEPTIONS | CUSTOMER_SEGMENT | display format `$CUSTSEG.` | WORK.ACCT_RAW |
| STG_BANK.CUST_ACCOUNTS_DAILY / WORK.ACCT_EXCEPTIONS | REGION_CODE | display format `$REGION.` | WORK.ACCT_RAW |
| STG_BANK.CUST_ACCOUNTS_DAILY / WORK.ACCT_EXCEPTIONS | CURRENT_BALANCE | display format `dollar18.2` | WORK.ACCT_RAW |
| STG_BANK.CUST_ACCOUNTS_DAILY / WORK.ACCT_EXCEPTIONS | AVAILABLE_BALANCE | display format `dollar18.2` | WORK.ACCT_RAW |
| STG_BANK.CUST_ACCOUNTS_DAILY / WORK.ACCT_EXCEPTIONS | CREDIT_LIMIT | display format `dollar18.2` | WORK.ACCT_RAW |
| STG_BANK.CUST_ACCOUNTS_DAILY / WORK.ACCT_EXCEPTIONS | OPEN_DATE | display format `date9.` | WORK.ACCT_RAW |
| STG_BANK.CUST_ACCOUNTS_DAILY / WORK.ACCT_EXCEPTIONS | CLOSE_DATE | display format `date9.` | WORK.ACCT_RAW |
| STG_BANK.CUST_ACCOUNTS_DAILY / WORK.ACCT_EXCEPTIONS | LAST_ACTIVITY_DATE | display format `date9.` | WORK.ACCT_RAW |
| STG_BANK.CUST_ACCOUNTS_DAILY / WORK.ACCT_EXCEPTIONS | LOAD_TIMESTAMP | display format `datetime20.` | WORK.ACCT_RAW |
| OUT=WORK.ACCT_SUMMARY(DROP=_TYPE_ | *(row output)* | always |  |
| STG_BANK.ACCT_EXCEPTIONS | * | `pass-through (all columns)` | WORK.ACCT_EXCEPTIONS |
| WORK.ACCT_SUMMARY | *(aggregate)* | PROC MEANS NWAY CLASS ACCOUNT_TYPE × REGION_CODE; N_ACCOUNTS=n(first var), TOTAL_BALANCE=sum(CURRENT_BALANCE), AVG_BALANCE=mean(CURRENT_BALANCE), AVG_UTILIZATION=mean(UTILIZATION_PCT), AVG_AGE_MONTHS=mean(ACCT_AGE_MONTHS) | STG_BANK.CUST_ACCOUNTS_DAILY |

**Notes / ambiguities:**
- The `drop EXCEPTION_CODE EXCEPTION_DESC;` statement is a DATA-step statement (not a dataset option), so it applies to *both* output datasets — WORK.ACCT_EXCEPTIONS therefore does NOT contain the exception code/description columns; exception rows are copies of the account row at the time each rule fires.
- Exception rows are output *before* SNAPSHOT_DATE / LOAD_TIMESTAMP are assigned, so those columns are missing (null) on exception rows.
- LOAD_TIMESTAMP = datetime() is wall-clock and non-deterministic; it is excluded from the baseline and the migrated model.
- RAW_BANK.DAILY_RATES is declared as an input in the program header but never referenced in the code.
- An account row can fire multiple exception rules (e.g. HIGH_UTIL and NO_RISK), producing multiple identical rows in ACCT_EXCEPTIONS (identical because the code/description columns are dropped).


## 3. Verification evidence

Commands run from the repo root (dbt from `dbt/sas/`), 2026-08-05:

```
python3 tools/sas_lineage.py       # regenerated docs/stm/sas_stm.{json,md} — no diff vs committed
python3 tools/sas_baseline.py      # baseline CUST_ACCOUNTS_DAILY: 466 rows; baseline ACCT_EXCEPTIONS: 32 rows
python3 tools/sas_load_raw.py      # raw seed data loaded into dbt/sas/dev.duckdb
cd dbt/sas && dbt build --profiles-dir . --no-partial-parse
cd ../.. && python3 tools/parity_diff.py --baseline baseline/sas --actual dbt/sas/dev.duckdb \
  --schema main --keys tools/keys/sas_keys.json --report /tmp/parity.md
```

dbt build result:

```
Finished running 8 seeds, 17 table models, 67 data tests, 25 view models in 0 hours 0 minutes and 4.17 seconds (4.17s).
Completed successfully
Done. PASS=117 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=117
```

This unit's target sections from the parity report:

```
## ACCT_EXCEPTIONS
- rows: baseline=32 actual=32
- columns compared: 28
- result: **MATCH** (all values within tolerance)

## CUST_ACCOUNTS_DAILY
- rows: baseline=466 actual=466
- columns compared: 33
- result: **MATCH** (all values within tolerance)
```

Overall report footer: `**Overall: PARITY VERIFIED**` — **parity_diff exit code: 0**.

## 4. Snowflake notes

Items in this unit's SQL a Snowflake deployment should review:

- **`datediff('month', ...)` vs SAS `intck('month', ...)`** — `int_acct_base.sql` uses
  `DATEDIFF(month, open_date, run_date)`. Snowflake's `DATEDIFF(month, ...)` counts
  month-boundary crossings, which matches SAS `INTCK`'s default (DISCRETE) semantics,
  so this ports directly — but verify no future change to CONTINUOUS-style semantics
  is expected. `DATEDIFF(day, ...)` for `DAYS_INACTIVE` is identical in Snowflake.
- **Division in `UTILIZATION_PCT`** — `(current_balance / credit_limit) * 100`.
  Snowflake division of NUMBER types yields scaled NUMBER (default scale rules),
  DuckDB yields DOUBLE. If balances/limits land as NUMBER(38, 2), consider an explicit
  cast to FLOAT/NUMBER with sufficient scale to preserve the 1e-6 parity tolerance.
- **`run_date` var cast** — `cast('{{ var("run_date") }}' as date)` relies on an
  ISO-8601 literal (`2024-01-31`); Snowflake honors this regardless of `DATE_INPUT_FORMAT`,
  but keep the var ISO-formatted.
- **Null comparison semantics** — the exception rules rely on SQL null semantics
  (`utilization_pct > 95` is false for null; `risk_rating is null` for the SAS
  missing-value test `RISK_RATING = .`). Identical in Snowflake; no change needed.
- **`b.*` column expansion + seed lookups** — `cust_accounts_daily.sql` selects `b.*`
  plus five `fmt_*` seed-lookup `*_DESC` columns. In Snowflake, dbt seeds default to
  uppercase unquoted identifiers — consistent with these models, but confirm the
  project-wide `quoting` config when pointing at Snowflake.
- **Non-deterministic `LOAD_TIMESTAMP`** — the legacy `datetime()` column is
  intentionally excluded from the migrated model and parity; if required in Snowflake,
  add `CURRENT_TIMESTAMP()` at load and continue excluding it from reconciliation.
- **Exception-row semantics** — `acct_exceptions.sql` reproduces the legacy quirks
  (no exception code/description columns; null `snapshot_date`; one row per fired rule,
  so an account can appear multiple times). Downstream Snowflake consumers should not
  assume uniqueness on `account_id` in `ACCT_EXCEPTIONS`.
