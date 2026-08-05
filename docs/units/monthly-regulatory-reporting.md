# Unit Verification Packet — `monthly_regulatory_reporting.sas`

## 1. Unit overview

`legacy/sas/programs/monthly_regulatory_reporting.sas` is the monthly Basel III / Call Report
program (Control-M job `BANK_MONTHLY_01`, monthly 3rd business day). The macro
`%monthly_regulatory_reporting(report_month=&PREV_YM)` derives the month-end date from the
`report_month` parameter (`YYYYMM`, pinned to `202401` / month-end 31JAN2024 in this migration)
and produces four persistent regulatory aggregations plus an Excel export:

1. **Step 1 — `REPORTS.MONTHLY_RWA`**: risk-weighted assets under the Basel III standardized
   approach. Month-end account snapshot rows (`STG_BANK.CUST_ACCOUNTS_DAILY`, filtered to
   `SNAPSHOT_DATE = month_end`) are left-joined to `ORA_DW.LOAN_DETAILS` and assigned a
   `RISK_WEIGHT` by account type (deposits 0.00; MTG 0.35/0.50 by LTV ≤/> 0.80; HELC 0.50;
   AUTO/PERS/CC 0.75; LOC and default 1.00), then aggregated by
   `REPORT_MONTH × ACCOUNT_TYPE × CUSTOMER_SEGMENT × RISK_WEIGHT` producing `N_ACCOUNTS`,
   `TOTAL_EXPOSURE`, and `RWA = sum(CURRENT_BALANCE * RISK_WEIGHT)`.
2. **Step 2 — `REPORTS.DELINQUENCY_AGING`**: same join, restricted to lending products
   (`MTG, AUTO, PERS, CC, LOC, HELC`), bucketing `DAYS_PAST_DUE` into
   `Current / 1-29 / 30-59 / 60-89 / 90-119 / 120-179 / 180+ / Unknown` and aggregating
   `N_ACCOUNTS`, `TOTAL_BALANCE`, `TOTAL_PAST_DUE` by `ACCOUNT_TYPE × REGION_CODE × bucket`.
3. **Step 3 — `REPORTS.LLP_COVERAGE`**: loan loss provision coverage per lending
   `ACCOUNT_TYPE`, using an **inner** join to `ORA_DW.LOAN_DETAILS` — `GROSS_LOANS`,
   `TOTAL_ALLOWANCE`, `COVERAGE_PCT`, `NPL_BALANCE` (balance where `DAYS_PAST_DUE >= 90`),
   `NPL_COVERAGE_PCT`.
4. **Step 4 — Excel export**: `%export_xlsx` writes the RWA, Delinquency, and LLP tables to
   `&REPORT_PATH/REG_REPORT_&report_month..xlsx` (side-effect only; not a parity target).
5. **Step 5 — `REPORTS.CAPITAL_ADEQUACY`**: single-row summary over `REPORTS.MONTHLY_RWA`:
   `TOTAL_RWA`, GL-placeholder capital amounts (CET1 50M, Tier 1 65M, Total 80M), the three
   capital ratios, and PASS/FAIL status vs the Basel III minimums (CET1 4.5%, Tier 1 6%,
   Total 8%).

**Sources:** `STG_BANK.CUST_ACCOUNTS_DAILY`, `ORA_DW.LOAN_DETAILS` (the header also names
`CURATED.DAILY_TRANSACTIONS` and `ORA_DW.COLLATERAL`, but no step reads them).
**Targets:** `REPORTS.MONTHLY_RWA`, `REPORTS.DELINQUENCY_AGING`, `REPORTS.LLP_COVERAGE`,
`REPORTS.CAPITAL_ADEQUACY` (+ the non-parity Excel file).

dbt implementation: `models/intermediate/int_rwa_weighted.sql` (per-account risk weighting off
`cust_accounts_daily` × `stg_loan_details`) feeding marts `monthly_rwa`, `delinquency_aging`,
`llp_coverage`, and `capital_adequacy`.

## 2. STM excerpt (from `docs/stm/sas_stm.md`)

**Macro:** `%monthly_regulatory_reporting` — parameters: `report_month=&PREV_YM`

**Inputs:** `ORA_DW.LOAN_DETAILS`, `STG_BANK.CUST_ACCOUNTS_DAILY`
**Persistent outputs:** `REPORTS.CAPITAL_ADEQUACY`, `REPORTS.DELINQUENCY_AGING`, `REPORTS.LLP_COVERAGE`, `REPORTS.MONTHLY_RWA`

| Output Dataset | Column | Derivation | Source(s) |
|---|---|---|---|
| REPORTS.MONTHLY_RWA | *(step)* | left join ORA_DW.LOAN_DETAILS l on a.ACCOUNT_ID = l.ACCOUNT_ID; where a.SNAPSHOT_DATE = "&month_end"d; group by 1, 2, 3, 4 | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.LOAN_DETAILS l |
| REPORTS.MONTHLY_RWA | REPORT_MONTH | `"&report_month"` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.LOAN_DETAILS l |
| REPORTS.MONTHLY_RWA | ACCOUNT_TYPE | `ACCOUNT_TYPE` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.LOAN_DETAILS l |
| REPORTS.MONTHLY_RWA | CUSTOMER_SEGMENT | `CUSTOMER_SEGMENT` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.LOAN_DETAILS l |
| REPORTS.MONTHLY_RWA | RISK_WEIGHT | `case when ACCOUNT_TYPE in ('CHK','SAV','MMA') then 0.00 when ACCOUNT_TYPE = 'CD' then 0.00 when ACCOUNT_TYPE = 'MTG' and LTV <= 0.80 then 0.35 when ACCOUNT_TYPE = 'MTG' and LTV > 0.80 then 0.50 when ACCOUNT_TYPE = 'HELC' then 0.50 when ACCOUNT_TYPE in ('AUTO','PERS') then 0.75 when ACCOUNT_TYPE = 'CC' then 0.75 when ACCOUNT_TYPE = 'LOC' then 1.00 else 1.00 end` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.LOAN_DETAILS l |
| REPORTS.MONTHLY_RWA | N_ACCOUNTS | `count(*)` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.LOAN_DETAILS l |
| REPORTS.MONTHLY_RWA | TOTAL_EXPOSURE | `sum(CURRENT_BALANCE)` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.LOAN_DETAILS l |
| REPORTS.MONTHLY_RWA | RWA | `sum(CURRENT_BALANCE * calculated RISK_WEIGHT)` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.LOAN_DETAILS l |
| REPORTS.DELINQUENCY_AGING | *(step)* | left join ORA_DW.LOAN_DETAILS l on a.ACCOUNT_ID = l.ACCOUNT_ID; where a.SNAPSHOT_DATE = "&month_end"d and a.ACCOUNT_TYPE in ('MTG','AUTO','PERS','CC','LOC','HELC'); group by 1, 2, 3, 4 | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.LOAN_DETAILS l |
| REPORTS.DELINQUENCY_AGING | REPORT_MONTH | `"&report_month"` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.LOAN_DETAILS l |
| REPORTS.DELINQUENCY_AGING | ACCOUNT_TYPE | `ACCOUNT_TYPE` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.LOAN_DETAILS l |
| REPORTS.DELINQUENCY_AGING | REGION_CODE | `REGION_CODE` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.LOAN_DETAILS l |
| REPORTS.DELINQUENCY_AGING | DELINQ_BUCKET | `case when DAYS_PAST_DUE = 0 then 'Current' when DAYS_PAST_DUE between 1 and 29 then '1-29' when DAYS_PAST_DUE between 30 and 59 then '30-59' when DAYS_PAST_DUE between 60 and 89 then '60-89' when DAYS_PAST_DUE between 90 and 119 then '90-119' when DAYS_PAST_DUE between 120 and 179 then '120-179' when DAYS_PAST_DUE >= 180 then '180+' else 'Unknown' end` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.LOAN_DETAILS l |
| REPORTS.DELINQUENCY_AGING | N_ACCOUNTS | `count(*)` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.LOAN_DETAILS l |
| REPORTS.DELINQUENCY_AGING | TOTAL_BALANCE | `sum(CURRENT_BALANCE)` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.LOAN_DETAILS l |
| REPORTS.DELINQUENCY_AGING | TOTAL_PAST_DUE | `sum(PAST_DUE_AMOUNT)` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.LOAN_DETAILS l |
| REPORTS.LLP_COVERAGE | *(step)* | inner join ORA_DW.LOAN_DETAILS l on a.ACCOUNT_ID = l.ACCOUNT_ID; where a.SNAPSHOT_DATE = "&month_end"d and a.ACCOUNT_TYPE in ('MTG','AUTO','PERS','CC','LOC','HELC'); group by 1, 2 | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.LOAN_DETAILS l |
| REPORTS.LLP_COVERAGE | REPORT_MONTH | `"&report_month"` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.LOAN_DETAILS l |
| REPORTS.LLP_COVERAGE | ACCOUNT_TYPE | `a.ACCOUNT_TYPE` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.LOAN_DETAILS l |
| REPORTS.LLP_COVERAGE | N_LOANS | `count(*)` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.LOAN_DETAILS l |
| REPORTS.LLP_COVERAGE | GROSS_LOANS | `sum(a.CURRENT_BALANCE)` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.LOAN_DETAILS l |
| REPORTS.LLP_COVERAGE | TOTAL_ALLOWANCE | `sum(l.ALLOWANCE_AMT)` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.LOAN_DETAILS l |
| REPORTS.LLP_COVERAGE | COVERAGE_PCT | `case when sum(a.CURRENT_BALANCE) > 0 then sum(l.ALLOWANCE_AMT) / sum(a.CURRENT_BALANCE) * 100 else 0 end` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.LOAN_DETAILS l |
| REPORTS.LLP_COVERAGE | NPL_BALANCE | `sum(case when l.DAYS_PAST_DUE >= 90 then a.CURRENT_BALANCE else 0 end)` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.LOAN_DETAILS l |
| REPORTS.LLP_COVERAGE | NPL_COVERAGE_PCT | `case when calculated NPL_BALANCE > 0 then sum(l.ALLOWANCE_AMT) / calculated NPL_BALANCE * 100 else 0 end` | STG_BANK.CUST_ACCOUNTS_DAILY a; ORA_DW.LOAN_DETAILS l |
| REPORTS.CAPITAL_ADEQUACY | REPORT_MONTH | `"&report_month"` | REPORTS.MONTHLY_RWA |
| REPORTS.CAPITAL_ADEQUACY | TOTAL_RWA | `sum(RWA)` | REPORTS.MONTHLY_RWA |
| REPORTS.CAPITAL_ADEQUACY | CET1_CAPITAL | `50000000` | REPORTS.MONTHLY_RWA |
| REPORTS.CAPITAL_ADEQUACY | TIER1_CAPITAL | `65000000` | REPORTS.MONTHLY_RWA |
| REPORTS.CAPITAL_ADEQUACY | TOTAL_CAPITAL | `80000000` | REPORTS.MONTHLY_RWA |
| REPORTS.CAPITAL_ADEQUACY | CET1_RATIO | `case when sum(RWA) > 0 then 50000000 / sum(RWA) * 100 else . end` | REPORTS.MONTHLY_RWA |
| REPORTS.CAPITAL_ADEQUACY | TIER1_RATIO | `case when sum(RWA) > 0 then 65000000 / sum(RWA) * 100 else . end` | REPORTS.MONTHLY_RWA |
| REPORTS.CAPITAL_ADEQUACY | TOTAL_CAPITAL_RATIO | `case when sum(RWA) > 0 then 80000000 / sum(RWA) * 100 else . end` | REPORTS.MONTHLY_RWA |
| REPORTS.CAPITAL_ADEQUACY | CET1_STATUS | `case when sum(RWA) = 0 then 'PASS' when 50000000/sum(RWA)*100 >= 4.5 then 'PASS' else 'FAIL' end` | REPORTS.MONTHLY_RWA |
| REPORTS.CAPITAL_ADEQUACY | TIER1_STATUS | `case when sum(RWA) = 0 then 'PASS' when 65000000/sum(RWA)*100 >= 6.0 then 'PASS' else 'FAIL' end` | REPORTS.MONTHLY_RWA |
| REPORTS.CAPITAL_ADEQUACY | TOTAL_CAPITAL_STATUS | `case when sum(RWA) = 0 then 'PASS' when 80000000/sum(RWA)*100 >= 8.0 then 'PASS' else 'FAIL' end` | REPORTS.MONTHLY_RWA |

**Notes / ambiguities (from the STM):**
- SAS missing-value ordering: `LTV <= 0.80` is TRUE when LTV is missing, so MTG accounts without a LOAN_DETAILS match get risk weight 0.35.
- DAYS_PAST_DUE missing (no LOAN_DETAILS row) falls through every aging bucket to 'Unknown' (missing is not =0 and not >=1).
- The ORDER BY clauses affect display order only and are irrelevant to row-level parity.

## 3. Verification evidence (actual run, 2026-08-05)

Commands executed from the repo root (dbt from inside `dbt/sas`):

```bash
python3 tools/sas_lineage.py
python3 tools/sas_baseline.py
python3 tools/sas_load_raw.py
(cd dbt/sas && dbt build --profiles-dir . --no-partial-parse)
python3 tools/parity_diff.py --baseline baseline/sas --actual dbt/sas/dev.duckdb \
  --schema main --keys tools/keys/sas_keys.json --report /tmp/parity.md
```

Baseline runner output for this unit's targets:

```
baseline MONTHLY_RWA: 59 rows
baseline DELINQUENCY_AGING: 70 rows
baseline LLP_COVERAGE: 6 rows
baseline CAPITAL_ADEQUACY: 1 rows
```

dbt build result:

```
Finished running 8 seeds, 17 table models, 67 data tests, 25 view models in 0 hours 0 minutes and 2.67 seconds (2.67s).
Completed successfully
Done. PASS=117 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=117
```

This unit's target sections copied from the parity report (`/tmp/parity.md`):

```
## CAPITAL_ADEQUACY
- rows: baseline=1 actual=1
- columns compared: 11
- result: **MATCH** (all values within tolerance)

## DELINQUENCY_AGING
- rows: baseline=70 actual=70
- columns compared: 7
- result: **MATCH** (all values within tolerance)

## LLP_COVERAGE
- rows: baseline=6 actual=6
- columns compared: 8
- result: **MATCH** (all values within tolerance)

## MONTHLY_RWA
- rows: baseline=59 actual=59
- columns compared: 7
- result: **MATCH** (all values within tolerance)

**Overall: PARITY VERIFIED**
```

**parity_diff exit code: 0**

| Target | Baseline rows | Actual rows | Result |
|---|---|---|---|
| MONTHLY_RWA | 59 | 59 | MATCH |
| DELINQUENCY_AGING | 70 | 70 | MATCH |
| LLP_COVERAGE | 6 | 6 | MATCH |
| CAPITAL_ADEQUACY | 1 | 1 | MATCH |

## 4. Snowflake notes

Items in this unit's SQL that a Snowflake deployment should review:

- **NULL LTV vs SAS missing ordering** — the legacy `LTV <= 0.80` predicate is TRUE for SAS
  missing values. The dbt model `int_rwa_weighted.sql` encodes this explicitly as
  `(l.ltv <= 0.80 or l.ltv is null)`; in Snowflake `NULL <= 0.80` is NULL (falsy), so this
  explicit `is null` branch must be preserved — do not "simplify" it back to the legacy predicate.
- **`Unknown` delinquency bucket** — accounts with no `LOAN_DETAILS` row have NULL
  `days_past_due` and must fall to the `else 'Unknown'` branch. Snowflake CASE handles NULL the
  same way as DuckDB here, but any refactor to `IFF`/lookup tables must keep the NULL→Unknown
  behavior.
- **Integer division** — ratio expressions like `50000000 / sum(rwa) * 100` and
  `sum(allowance_amt) / sum(current_balance) * 100`: `sum(rwa)` is DECIMAL/DOUBLE so division is
  non-integer in both engines, but if capital amounts are ever sourced as INTEGER GL values,
  Snowflake's `/` returns exact decimals with limited scale — consider casting operands to
  `NUMBER(38,10)` or `FLOAT` to match the 1e-6 parity tolerance.
- **CAPITAL_ADEQUACY NULL ratios** — the legacy `else .` (SAS missing) is expressed as a CASE
  with no ELSE (implicit NULL). Snowflake behaves identically; keep the statuses' separate
  `sum(RWA) = 0 → 'PASS'` guard, which prevents division by zero from ever being evaluated.
- **`var()`-driven literals** — `report_month` and `run_date` are dbt vars
  (`dbt_project.yml`); a Snowflake deployment should pass these per-run
  (`--vars '{report_month: ..., run_date: ...}'`) rather than relying on the pinned defaults.
- **Fixed-precision money columns** — the legacy formats (`dollar20.2`, `8.2`) are display-only;
  amounts should land in Snowflake as `NUMBER(20,2)`-style columns, with percent columns kept at
  higher scale to preserve parity of ratio values.
- **Excel export (Step 4)** — `%export_xlsx` has no dbt equivalent; in Snowflake this becomes a
  downstream extract (e.g. `COPY INTO @stage` or a BI export) and is out of scope for parity.
- **Grouping-set syntax** — models use positional `GROUP BY 1, 2, 3, 4`, valid in Snowflake;
  no DuckDB-only syntax is present in the unit's models.
