# Unit Verification Packet — `credit_risk_scoring.sas`

Track: **SAS → dbt** (branch `devin/sas-track`) · Unit: `legacy/sas/programs/credit_risk_scoring.sas`

## 1. Unit overview

`credit_risk_scoring.sas` (macro `%credit_risk_scoring`, parameters `score_date=&CURR_DT`,
`model_id=CRM-2023-Q4-v2`) applies the validated logistic-regression scorecard
CRM-2023-Q4-v2 to the current banking portfolio and produces Basel III risk parameters —
PD (probability of default), LGD (loss given default), EAD (exposure at default) — plus a
1–7 risk-rating band and a rating-migration matrix. Scheduled weekly (Control-M
`BANK_WEEKLY_01`); the migration pins the run to business date **31JAN2024**.

Program flow (5 steps):

1. **Assemble scoring features** (`PROC SQL` → `WORK.SCORE_INPUT`): snapshot rows from
   `STG_BANK.CUST_ACCOUNTS_DAILY` for `SNAPSHOT_DATE = "&score_date"d` and account types
   `MTG, AUTO, PERS, CC, LOC, HELC`; left-joins `ORA_DW.BUREAU_SCORES` (latest
   `SCORE_DATE` per customer on/before the score date, via correlated subquery),
   `ORA_DW.PAYMENT_HISTORY` (by `ACCOUNT_ID`), and `ORA_DW.COLLATERAL` (by `ACCOUNT_ID`,
   deriving `LTV = CURRENT_BALANCE / COLLATERAL_VALUE` when collateral value > 0).
2. **Apply scorecard** (DATA step → `WORK.SCORED`): WOE bands for FICO, utilization,
   90-day delinquency count, account age, and LTV (secured types only);
   `LOG_ODDS = -3.2145 + 0.412·WOE_FICO + 0.198·WOE_UTIL + 0.289·WOE_DPD + 0.067·WOE_AGE + 0.134·WOE_LTV`;
   `PD = 1/(1+exp(-LOG_ODDS))`; LGD by product (secured: `max(0,min(1,(LTV-0.5)*0.8))`,
   else 0.40 default; CC: 0.75; other: 0.50); EAD with 50% credit-conversion factor on
   undrawn limits for revolving types (`CC, LOC, HELC`); `EXPECTED_LOSS = PD·LGD·EAD`;
   `NEW_RISK_RATING` banded 1–7 on PD; intermediate WOE/log-odds columns dropped.
3. **Risk migration matrix** (`PROC SQL` → `WORK.RISK_MIGRATION`): inner join of scored
   accounts back to the snapshot, keeping accounts whose rating changed or that had no
   prior rating, with `MIGRATION_DIRECTION` in `NEW / UPGRADE / DOWNGRADE / STABLE`.
4. **Load to curated** (`%lock` + `PROC APPEND FORCE`): appends `WORK.SCORED` →
   `CURATED.RISK_SCORES` and `WORK.RISK_MIGRATION` → `CURATED.RISK_MIGRATION`.
5. **Summary report** (`PROC MEANS NWAY`): `REPORTS.RISK_SUMMARY` aggregated by
   `ACCOUNT_TYPE × NEW_RISK_RATING` with `N_ACCOUNTS`, `AVG_PD`, `AVG_LGD`, `TOTAL_EAD`,
   `TOTAL_EL`.

**Sources:** `STG_BANK.CUST_ACCOUNTS_DAILY`, `ORA_DW.BUREAU_SCORES`,
`ORA_DW.PAYMENT_HISTORY`, `ORA_DW.COLLATERAL`
**Targets:** `CURATED.RISK_SCORES`, `CURATED.RISK_MIGRATION`, `REPORTS.RISK_SUMMARY`

dbt implementation: `int_scored` (steps 1–2) feeding marts `risk_scores`,
`risk_migration`, `risk_summary` (comparison keys: `ACCOUNT_ID` for scores/migration,
`ACCOUNT_TYPE, NEW_RISK_RATING` for the summary).

## 2. STM excerpt (from `docs/stm/sas_stm.md`, section `credit_risk_scoring`)

**Macro:** `%credit_risk_scoring` — parameters: `score_date=&CURR_DT`, `model_id=CRM-2023-Q4-v2`

**Inputs:** `CURATED.RISK_MIGRATION`, `CURATED.RISK_SCORES`, `ORA_DW.BUREAU_SCORES`, `ORA_DW.COLLATERAL`, `ORA_DW.PAYMENT_HISTORY`, `STG_BANK.CUST_ACCOUNTS_DAILY`
**Persistent outputs:** `CURATED.RISK_MIGRATION`, `CURATED.RISK_SCORES`, `REPORTS.RISK_SUMMARY`

| Output Dataset | Column | Derivation | Source(s) |
|---|---|---|---|
| WORK.SCORE_INPUT | *(step)* | left join ORA_DW.BUREAU_SCORES b on a.CUSTOMER_ID = b.CUSTOMER_ID and b.SCORE_DATE = (select max(SCORE_DATE) from ORA_DW.BUREAU_SCORES; left join ORA_DW.PAYMENT_HISTORY p on a.ACCOUNT_ID = p.ACCOUNT_ID; left join ORA_DW.COLLATERAL c on a.ACCOUNT_ID = c.ACCOUNT_ID; where CUSTOMER_ID = b.CUSTOMER_ID and SCORE_DATE <= "&score_date"d) | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.BUREAU_SCORES b; ORA_DW.PAYMENT_HISTORY p; ORA_DW.COLLATERAL c |
| WORK.SCORE_INPUT | ACCOUNT_ID | `a.ACCOUNT_ID` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.BUREAU_SCORES b; ORA_DW.PAYMENT_HISTORY p; ORA_DW.COLLATERAL c |
| WORK.SCORE_INPUT | CUSTOMER_ID | `a.CUSTOMER_ID` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.BUREAU_SCORES b; ORA_DW.PAYMENT_HISTORY p; ORA_DW.COLLATERAL c |
| WORK.SCORE_INPUT | ACCOUNT_TYPE | `a.ACCOUNT_TYPE` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.BUREAU_SCORES b; ORA_DW.PAYMENT_HISTORY p; ORA_DW.COLLATERAL c |
| WORK.SCORE_INPUT | CURRENT_BALANCE | `a.CURRENT_BALANCE` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.BUREAU_SCORES b; ORA_DW.PAYMENT_HISTORY p; ORA_DW.COLLATERAL c |
| WORK.SCORE_INPUT | CREDIT_LIMIT | `a.CREDIT_LIMIT` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.BUREAU_SCORES b; ORA_DW.PAYMENT_HISTORY p; ORA_DW.COLLATERAL c |
| WORK.SCORE_INPUT | ACCT_AGE_MONTHS | `a.ACCT_AGE_MONTHS` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.BUREAU_SCORES b; ORA_DW.PAYMENT_HISTORY p; ORA_DW.COLLATERAL c |
| WORK.SCORE_INPUT | DAYS_INACTIVE | `a.DAYS_INACTIVE` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.BUREAU_SCORES b; ORA_DW.PAYMENT_HISTORY p; ORA_DW.COLLATERAL c |
| WORK.SCORE_INPUT | UTILIZATION_PCT | `a.UTILIZATION_PCT` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.BUREAU_SCORES b; ORA_DW.PAYMENT_HISTORY p; ORA_DW.COLLATERAL c |
| WORK.SCORE_INPUT | CUSTOMER_SEGMENT | `a.CUSTOMER_SEGMENT` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.BUREAU_SCORES b; ORA_DW.PAYMENT_HISTORY p; ORA_DW.COLLATERAL c |
| WORK.SCORE_INPUT | REGION_CODE | `a.REGION_CODE` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.BUREAU_SCORES b; ORA_DW.PAYMENT_HISTORY p; ORA_DW.COLLATERAL c |
| WORK.SCORE_INPUT | FICO_SCORE | `b.FICO_SCORE` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.BUREAU_SCORES b; ORA_DW.PAYMENT_HISTORY p; ORA_DW.COLLATERAL c |
| WORK.SCORE_INPUT | VANTAGE_SCORE | `b.VANTAGE_SCORE` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.BUREAU_SCORES b; ORA_DW.PAYMENT_HISTORY p; ORA_DW.COLLATERAL c |
| WORK.SCORE_INPUT | BUREAU_INQS_6MO | `b.BUREAU_INQS_6MO` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.BUREAU_SCORES b; ORA_DW.PAYMENT_HISTORY p; ORA_DW.COLLATERAL c |
| WORK.SCORE_INPUT | BUREAU_TRADES_OPEN | `b.BUREAU_TRADES_OPEN` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.BUREAU_SCORES b; ORA_DW.PAYMENT_HISTORY p; ORA_DW.COLLATERAL c |
| WORK.SCORE_INPUT | BUREAU_DEROGS | `b.BUREAU_DEROGS` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.BUREAU_SCORES b; ORA_DW.PAYMENT_HISTORY p; ORA_DW.COLLATERAL c |
| WORK.SCORE_INPUT | BUREAU_UTIL_PCT | `b.BUREAU_UTIL_PCT` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.BUREAU_SCORES b; ORA_DW.PAYMENT_HISTORY p; ORA_DW.COLLATERAL c |
| WORK.SCORE_INPUT | BUREAU_OLDEST_TRADE_MO | `b.BUREAU_OLDEST_TRADE_MO` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.BUREAU_SCORES b; ORA_DW.PAYMENT_HISTORY p; ORA_DW.COLLATERAL c |
| WORK.SCORE_INPUT | PMT_ONTIME_12MO | `p.PMT_ONTIME_12MO` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.BUREAU_SCORES b; ORA_DW.PAYMENT_HISTORY p; ORA_DW.COLLATERAL c |
| WORK.SCORE_INPUT | PMT_LATE_30_12MO | `p.PMT_LATE_30_12MO` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.BUREAU_SCORES b; ORA_DW.PAYMENT_HISTORY p; ORA_DW.COLLATERAL c |
| WORK.SCORE_INPUT | PMT_LATE_60_12MO | `p.PMT_LATE_60_12MO` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.BUREAU_SCORES b; ORA_DW.PAYMENT_HISTORY p; ORA_DW.COLLATERAL c |
| WORK.SCORE_INPUT | PMT_LATE_90_12MO | `p.PMT_LATE_90_12MO` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.BUREAU_SCORES b; ORA_DW.PAYMENT_HISTORY p; ORA_DW.COLLATERAL c |
| WORK.SCORE_INPUT | MAX_DAYS_PAST_DUE_EVER | `p.MAX_DAYS_PAST_DUE_EVER` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.BUREAU_SCORES b; ORA_DW.PAYMENT_HISTORY p; ORA_DW.COLLATERAL c |
| WORK.SCORE_INPUT | MONTHS_SINCE_LAST_DPD | `p.MONTHS_SINCE_LAST_DPD` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.BUREAU_SCORES b; ORA_DW.PAYMENT_HISTORY p; ORA_DW.COLLATERAL c |
| WORK.SCORE_INPUT | AVG_PMT_RATIO_12MO | `p.AVG_PMT_RATIO_12MO` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.BUREAU_SCORES b; ORA_DW.PAYMENT_HISTORY p; ORA_DW.COLLATERAL c |
| WORK.SCORE_INPUT | COLLATERAL_VALUE | `c.COLLATERAL_VALUE` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.BUREAU_SCORES b; ORA_DW.PAYMENT_HISTORY p; ORA_DW.COLLATERAL c |
| WORK.SCORE_INPUT | LAST_APPRAISAL_DATE | `c.LAST_APPRAISAL_DATE` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.BUREAU_SCORES b; ORA_DW.PAYMENT_HISTORY p; ORA_DW.COLLATERAL c |
| WORK.SCORE_INPUT | LTV | `case when c.COLLATERAL_VALUE > 0 then a.CURRENT_BALANCE / c.COLLATERAL_VALUE else . end` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.BUREAU_SCORES b; ORA_DW.PAYMENT_HISTORY p; ORA_DW.COLLATERAL c |
| WORK.SCORED | *(step)* | DROP (all outputs): INTERCEPT WOE_FICO WOE_UTIL WOE_DPD WOE_AGE WOE_LTV LOG_ODDS | WORK.SCORE_INPUT |
| WORK.SCORED | INTERCEPT | `-3.2145` | WORK.SCORE_INPUT |
| WORK.SCORED | WOE_FICO | if `FICO_SCORE >= 760` then `-1.204` | WORK.SCORE_INPUT |
| WORK.SCORED | WOE_FICO | if `ELSE FICO_SCORE >= 720` then `-0.812` | WORK.SCORE_INPUT |
| WORK.SCORED | WOE_FICO | if `ELSE FICO_SCORE >= 680` then `-0.356` | WORK.SCORE_INPUT |
| WORK.SCORED | WOE_FICO | if `ELSE FICO_SCORE >= 640` then `0.198` | WORK.SCORE_INPUT |
| WORK.SCORED | WOE_FICO | if `ELSE FICO_SCORE >= 600` then `0.654` | WORK.SCORE_INPUT |
| WORK.SCORED | WOE_FICO | if `NOT (ELSE FICO_SCORE >= 600)` then `1.102` | WORK.SCORE_INPUT |
| WORK.SCORED | WOE_FICO | if `NOT (not missing(FICO_SCORE))` then `0.198` | WORK.SCORE_INPUT |
| WORK.SCORED | WOE_UTIL | if `UTILIZATION_PCT <= 10` then `-0.956` | WORK.SCORE_INPUT |
| WORK.SCORED | WOE_UTIL | if `ELSE UTILIZATION_PCT <= 30` then `-0.521` | WORK.SCORE_INPUT |
| WORK.SCORED | WOE_UTIL | if `ELSE UTILIZATION_PCT <= 50` then `-0.102` | WORK.SCORE_INPUT |
| WORK.SCORED | WOE_UTIL | if `ELSE UTILIZATION_PCT <= 70` then `0.334` | WORK.SCORE_INPUT |
| WORK.SCORED | WOE_UTIL | if `ELSE UTILIZATION_PCT <= 90` then `0.789` | WORK.SCORE_INPUT |
| WORK.SCORED | WOE_UTIL | if `NOT (ELSE UTILIZATION_PCT <= 90)` then `1.245` | WORK.SCORE_INPUT |
| WORK.SCORED | WOE_UTIL | if `NOT (not missing(UTILIZATION_PCT))` then `0` | WORK.SCORE_INPUT |
| WORK.SCORED | WOE_DPD | if `PMT_LATE_90_12MO = 0` then `-0.678` | WORK.SCORE_INPUT |
| WORK.SCORED | WOE_DPD | if `ELSE PMT_LATE_90_12MO = 1` then `0.445` | WORK.SCORE_INPUT |
| WORK.SCORED | WOE_DPD | if `NOT (ELSE PMT_LATE_90_12MO = 1)` then `1.567` | WORK.SCORE_INPUT |
| WORK.SCORED | WOE_DPD | if `NOT (not missing(PMT_LATE_90_12MO))` then `0` | WORK.SCORE_INPUT |
| WORK.SCORED | WOE_AGE | if `ACCT_AGE_MONTHS >= 120` then `-0.534` | WORK.SCORE_INPUT |
| WORK.SCORED | WOE_AGE | if `ELSE ACCT_AGE_MONTHS >= 60` then `-0.289` | WORK.SCORE_INPUT |
| WORK.SCORED | WOE_AGE | if `ELSE ACCT_AGE_MONTHS >= 24` then `0.045` | WORK.SCORE_INPUT |
| WORK.SCORED | WOE_AGE | if `NOT (ELSE ACCT_AGE_MONTHS >= 24)` then `0.456` | WORK.SCORE_INPUT |
| WORK.SCORED | WOE_AGE | if `NOT (not missing(ACCT_AGE_MONTHS))` then `0` | WORK.SCORE_INPUT |
| WORK.SCORED | WOE_LTV | if `LTV <= 0.60` then `-0.712` | WORK.SCORE_INPUT |
| WORK.SCORED | WOE_LTV | if `ELSE LTV <= 0.80` then `-0.234` | WORK.SCORE_INPUT |
| WORK.SCORED | WOE_LTV | if `ELSE LTV <= 1.00` then `0.356` | WORK.SCORE_INPUT |
| WORK.SCORED | WOE_LTV | if `NOT (ELSE LTV <= 1.00)` then `0.889` | WORK.SCORE_INPUT |
| WORK.SCORED | WOE_LTV | if `NOT (not missing(LTV))` then `0` | WORK.SCORE_INPUT |
| WORK.SCORED | WOE_LTV | if `NOT (ACCOUNT_TYPE in ('MTG','AUTO','HELC'))` then `0` | WORK.SCORE_INPUT |
| WORK.SCORED | LOG_ODDS | `INTERCEPT + 0.412 * WOE_FICO + 0.198 * WOE_UTIL + 0.289 * WOE_DPD + 0.067 * WOE_AGE + 0.134 * WOE_LTV` | WORK.SCORE_INPUT |
| WORK.SCORED | PD | `1 / (1 + exp(-LOG_ODDS))` | WORK.SCORE_INPUT |
| WORK.SCORED | LGD | if `not missing(LTV)` then `max(0, min(1, (LTV - 0.5) * 0.8))` | WORK.SCORE_INPUT |
| WORK.SCORED | LGD | if `NOT (not missing(LTV))` then `0.40` | WORK.SCORE_INPUT |
| WORK.SCORED | LGD | if `ELSE ACCOUNT_TYPE = 'CC'` then `0.75` | WORK.SCORE_INPUT |
| WORK.SCORED | LGD | if `NOT (ELSE ACCOUNT_TYPE = 'CC')` then `0.50` | WORK.SCORE_INPUT |
| WORK.SCORED | EAD | if `ACCOUNT_TYPE in ('CC','LOC','HELC')` then `CURRENT_BALANCE + 0.50 * (CREDIT_LIMIT - CURRENT_BALANCE)` | WORK.SCORE_INPUT |
| WORK.SCORED | EAD | if `NOT (ACCOUNT_TYPE in ('CC','LOC','HELC'))` then `CURRENT_BALANCE` | WORK.SCORE_INPUT |
| WORK.SCORED | EXPECTED_LOSS | `PD * LGD * EAD` | WORK.SCORE_INPUT |
| WORK.SCORED | NEW_RISK_RATING | if `PD < 0.005` then `1` | WORK.SCORE_INPUT |
| WORK.SCORED | NEW_RISK_RATING | if `ELSE PD < 0.01` then `2` | WORK.SCORE_INPUT |
| WORK.SCORED | NEW_RISK_RATING | if `ELSE PD < 0.03` then `3` | WORK.SCORE_INPUT |
| WORK.SCORED | NEW_RISK_RATING | if `ELSE PD < 0.07` then `4` | WORK.SCORE_INPUT |
| WORK.SCORED | NEW_RISK_RATING | if `ELSE PD < 0.15` then `5` | WORK.SCORE_INPUT |
| WORK.SCORED | NEW_RISK_RATING | if `ELSE PD < 0.30` then `6` | WORK.SCORE_INPUT |
| WORK.SCORED | NEW_RISK_RATING | if `NOT (ELSE PD < 0.30)` then `7` | WORK.SCORE_INPUT |
| WORK.SCORED | SCORE_DATE | `"&score_date"d` | WORK.SCORE_INPUT |
| WORK.SCORED | MODEL_ID | `"&model_id"` | WORK.SCORE_INPUT |
| WORK.SCORED | SCORE_TIMESTAMP | `datetime()` | WORK.SCORE_INPUT |
| WORK.SCORED | PD | display format `percent8.4` | WORK.SCORE_INPUT |
| WORK.SCORED | LGD | display format `percent8.4` | WORK.SCORE_INPUT |
| WORK.SCORED | EAD | display format `dollar18.2` | WORK.SCORE_INPUT |
| WORK.SCORED | EXPECTED_LOSS | display format `dollar18.2` | WORK.SCORE_INPUT |
| WORK.SCORED | SCORE_DATE | display format `date9.` | WORK.SCORE_INPUT |
| WORK.SCORED | SCORE_TIMESTAMP | display format `datetime20.` | WORK.SCORE_INPUT |
| WORK.RISK_MIGRATION | *(step)* | inner join STG_BANK.CUST_ACCOUNTS_DAILY a on s.ACCOUNT_ID = a.ACCOUNT_ID; where a.SNAPSHOT_DATE = "&score_date"d and (a.RISK_RATING ne s.NEW_RISK_RATING or a.RISK_RATING is null) | WORK.SCORED s; STG_BANK.CUST_ACCOUNTS_DAILY a |
| WORK.RISK_MIGRATION | SCORE_DATE | `"&score_date"d` | WORK.SCORED s; STG_BANK.CUST_ACCOUNTS_DAILY a |
| WORK.RISK_MIGRATION | ACCOUNT_ID | `a.ACCOUNT_ID` | WORK.SCORED s; STG_BANK.CUST_ACCOUNTS_DAILY a |
| WORK.RISK_MIGRATION | PREV_RATING | `a.RISK_RATING` | WORK.SCORED s; STG_BANK.CUST_ACCOUNTS_DAILY a |
| WORK.RISK_MIGRATION | CURR_RATING | `s.NEW_RISK_RATING` | WORK.SCORED s; STG_BANK.CUST_ACCOUNTS_DAILY a |
| WORK.RISK_MIGRATION | MIGRATION_DIRECTION | `case when a.RISK_RATING is null then 'NEW' when s.NEW_RISK_RATING < a.RISK_RATING then 'UPGRADE' when s.NEW_RISK_RATING > a.RISK_RATING then 'DOWNGRADE' else 'STABLE' end` | WORK.SCORED s; STG_BANK.CUST_ACCOUNTS_DAILY a |
| WORK.RISK_MIGRATION | PD | `s.PD` | WORK.SCORED s; STG_BANK.CUST_ACCOUNTS_DAILY a |
| WORK.RISK_MIGRATION | EXPECTED_LOSS | `s.EXPECTED_LOSS` | WORK.SCORED s; STG_BANK.CUST_ACCOUNTS_DAILY a |
| CURATED.RISK_SCORES | *(all columns of base)* | PROC APPEND FORCE (extra columns dropped) | WORK.SCORED |
| CURATED.RISK_MIGRATION | *(all columns of base)* | PROC APPEND FORCE (extra columns dropped) | WORK.RISK_MIGRATION |
| REPORTS.RISK_SUMMARY | *(aggregate)* | PROC MEANS NWAY CLASS ACCOUNT_TYPE × NEW_RISK_RATING; N_ACCOUNTS=n(first var), AVG_PD=mean(PD), AVG_LGD=mean(LGD), TOTAL_EAD=sum(EAD), TOTAL_EL=sum(EXPECTED_LOSS) | WORK.SCORED |

**Notes / ambiguities:**
- Bureau join picks the latest SCORE_DATE per customer on or before the score date via a correlated subquery.
- WOE defaults for missing inputs: FICO→0.198, UTIL→0, DPD→0, AGE→0, LTV→0 (and LTV WOE applies only to MTG/AUTO/HELC).
- SCORE_TIMESTAMP = datetime() is non-deterministic and excluded from the baseline and migrated model.
- REPORTS.RISK_SUMMARY is PROC MEANS NWAY by ACCOUNT_TYPE × NEW_RISK_RATING; N_ACCOUNTS is the n of the first analysis variable (PD, never missing here).

## 3. Verification evidence

Run performed 2026-08-05 on branch `devin/sas-track` (business date pinned to 31JAN2024).

Commands executed (repo root unless noted):

```
python3 tools/sas_lineage.py        # regenerated docs/stm/sas_stm.{json,md} (no diff)
python3 tools/sas_baseline.py       # materialized baseline/sas/*
python3 tools/sas_load_raw.py       # loaded raw seeds into dbt/sas/dev.duckdb
(cd dbt/sas && dbt build --profiles-dir . --no-partial-parse)
python3 tools/parity_diff.py --baseline baseline/sas --actual dbt/sas/dev.duckdb \
  --schema main --keys tools/keys/sas_keys.json --report /tmp/parity.md
```

Baseline runner output for this unit's targets:

```
  baseline RISK_SCORES: 236 rows
  baseline RISK_MIGRATION: 195 rows
  baseline RISK_SUMMARY: 12 rows
```

dbt build result:

```
Finished running 8 seeds, 17 table models, 67 data tests, 25 view models in 0 hours 0 minutes and 2.97 seconds (2.97s).
Completed successfully
Done. PASS=117 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=117
```

Parity report sections for this unit (from `/tmp/parity.md`):

```
## RISK_MIGRATION
- rows: baseline=195 actual=195
- columns compared: 7
- result: **MATCH** (all values within tolerance)

## RISK_SCORES
- rows: baseline=236 actual=236
- columns compared: 34
- result: **MATCH** (all values within tolerance)

## RISK_SUMMARY
- rows: baseline=12 actual=12
- columns compared: 7
- result: **MATCH** (all values within tolerance)
```

Overall report verdict: `**Overall: PARITY VERIFIED**` — **parity exit code: 0**.

Comparison keys (`tools/keys/sas_keys.json`): `RISK_SCORES`/`RISK_MIGRATION` →
`ACCOUNT_ID`; `RISK_SUMMARY` → `ACCOUNT_TYPE, NEW_RISK_RATING`.

## 4. Snowflake notes

Items in this unit's dbt SQL (`int_scored`, `risk_scores`, `risk_migration`,
`risk_summary`) a Snowflake deployment should review:

- **Latest-bureau-pull dedup** uses `row_number() over (partition by customer_id order by
  score_date desc) ... where rn = 1` inside a subquery. Valid Snowflake SQL; optionally
  rewrite with `QUALIFY row_number() ... = 1` for idiomatic Snowflake.
- **Division for LTV** (`current_balance / collateral_value`): Snowflake division of
  integer-typed columns yields exact NUMBER results with limited scale; ensure inputs are
  FLOAT/NUMBER with adequate scale so PD/LGD bands at boundaries (e.g. LTV = 0.80)
  resolve identically. Guarded against divide-by-zero by the `collateral_value > 0` case.
- **`exp()` in the logistic PD** is IEEE-754 double math on DuckDB; Snowflake's `EXP` is
  also double-precision, but boundary rows where PD sits within 1e-6 of a rating cutoff
  (0.005/0.01/0.03/0.07/0.15/0.30) could band differently — parity tolerance is 1e-6,
  rating is an integer, so re-run parity on Snowflake to confirm.
- **Run-date variable**: models take the score date via `var("run_date")` and
  `cast('...' as date)`, replacing the SAS `"&score_date"d` literal. Set the dbt var (or
  a Snowflake session variable) for the desired business date in deployment.
- **Excluded column**: legacy `SCORE_TIMESTAMP = datetime()` is intentionally omitted
  (non-deterministic). If required downstream, add `current_timestamp()` in Snowflake and
  exclude it from parity comparisons.
- **Append semantics**: legacy `PROC APPEND` accumulates history in
  `CURATED.RISK_SCORES`/`RISK_MIGRATION`; the dbt models are full-refresh tables for the
  pinned run date. For production Snowflake, consider `materialized='incremental'` with
  `unique_key=['score_date','account_id']` to preserve weekly history.
- **Locking**: `%lock` macro semantics are unnecessary on Snowflake (MVCC handles
  concurrent writers); no equivalent needed.
- **SAS display formats** (`percent8.4`, `dollar18.2`, `date9.`) are presentation-only
  and intentionally not carried into the models; apply formatting in the BI layer.
- **Case sensitivity**: DuckDB columns are lowercase; Snowflake defaults to uppercase
  unquoted identifiers. The models use unquoted identifiers throughout, so they resolve
  cleanly, but any downstream tooling that quotes identifiers should expect uppercase.
