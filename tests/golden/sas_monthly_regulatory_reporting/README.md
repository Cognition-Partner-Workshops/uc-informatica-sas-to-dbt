# Golden-dataset kit: monthly_regulatory_reporting (PROVISIONAL)

Branch-coverage scenarios for `legacy/sas/programs/monthly_regulatory_reporting.sas`. A SAS host runs each scenario
to replace the provisional expectations with true golden outputs; the same inputs then validate the dbt port.

**Everything under `expected_provisional/` is hand-derived from the SAS source, not produced by SAS.** No SAS
runtime was available. The expectations were derived with SAS semantics (missing numeric sorts lowest and is
`<=` any number; `sum()` ignores missing and is missing when all inputs are missing; `x*.` is missing; blank
character = missing; a PROC SQL summary without GROUP BY returns one row even on empty input).

## Layout

- `COVERAGE.md` - decision inventory (MON-D01..MON-D30), seed counts per side, covering scenarios.
- `scenarios.json` - manifest: `id`, `description`, `decision_ids` (the decisions whose seed-unhit sides the
  scenario hits), `params` (macro parameters), `targets`, plus `run_date` / `expected_outcome`.
- `scenarios/<id>/inputs/stg_bank/CUST_ACCOUNTS_DAILY.csv` - read as `STG_BANK.CUST_ACCOUNTS_DAILY` (supplied
  directly; `load_customer_accounts` is not run).
- `scenarios/<id>/inputs/oracle_dw/LOAN_DETAILS.csv` - read as `ORA_DW.LOAN_DETAILS`.
- `scenarios/<id>/expected_provisional/<TARGET>.csv` - `REPORTS.MONTHLY_RWA`, `DELINQUENCY_AGING`, `LLP_COVERAGE`,
  `CAPITAL_ADEQUACY`; same columns and order as `baseline/sas/` (the program writes no timestamp columns).

CSV conventions follow `legacy/sas/data/csv`: header row, dates as DATE9. text (`31JAN2024`), empty field = missing.
Column lists are the full legacy layouts; columns the program does not read are left empty. Account and
customer IDs are synthetic (`A9...`, `C9...`); no personal data is included.

## Scenarios

| id | report_month | decision_ids | what it exercises |
|----|--------------|--------------|-------------------|
| S01_default_rwa_arms | 202401 | MON-D03, MON-D06, MON-D11, MON-D13, MON-D14, MON-D16, MON-D17, MON-D19 | Default params (202401, run date 31JAN2024). One account per RISK_WEIGHT arm incl. MTG LTV <0.80 / =0.80 boundary / >0.80 / missing LTV / no LOAN row, IRA via ELSE, zero and negative weighted balances, rows dropped by SNAPSHOT_DATE (prior month-end, mid-month, missing) and a LOAN row with no account. |
| S02_default_delinquency_buckets | 202401 | MON-D13, MON-D14, MON-D15, MON-D16, MON-D17, MON-D19, MON-D22 | Default params. DAYS_PAST_DUE at every bucket edge (0,1,29,30,59,60,89,90,119,120,179,180) plus 250, missing DPD and missing PAST_DUE_AMOUNT on a LOAN row, negative DPD, a loan-type account with no LOAN row, and a deposit account excluded by the loan-type filter. |
| S03_default_llp_edges | 202401 | MON-D06, MON-D08, MON-D09, MON-D11, MON-D13, MON-D14, MON-D15, MON-D16, MON-D17, MON-D19, MON-D20, MON-D21, MON-D22, MON-D23 | Default params. LLP_COVERAGE edges: GROSS_LOANS <= 0 (credit balance), all balances missing (GROSS missing, NPL_BALANCE missing), GROSS > 0 with all ALLOWANCE_AMT missing (COVERAGE_PCT missing), normal NPL coverage, DPD missing (NPL case -> 0), and a loan-type account with no LOAN row (dropped by the INNER JOIN). Also an all-missing-balance MONTHLY_RWA group and all-missing TOTAL_PAST_DUE group. |
| S04_default_nonstandard_values | 202401 | MON-D04, MON-D07, MON-D10, MON-D13, MON-D14, MON-D16, MON-D18, MON-D19 | Default params. SAS-legal values that the dbt port's tests/types reject or treat differently: blank ACCOUNT_TYPE, lowercase 'mtg' (ELSE arm, not a loan type), blank CUSTOMER_SEGMENT, blank REGION_CODE, duplicate LOAN_DETAILS rows for one account (join fan-out in all three steps), non-integer DAYS_PAST_DUE in BETWEEN gaps (29.5, 89.5 -> 'Unknown'). |
| S05_default_capital_total_ratio_boundary | 202401 | MON-D28 | Default params. Single LOC account so sum(RWA) = 1,000,000,000.00: TOTAL_CAPITAL_RATIO exactly 8.0 (>= inclusive -> PASS), TIER1 6.5 PASS, CET1 5.0 PASS. |
| S06_default_capital_total_fail | 202401 | MON-D27 | Default params. Single LOC account so sum(RWA) = 1,050,000,000.00: TOTAL 7.62 FAIL, TIER1 6.19 PASS, CET1 4.76 PASS. |
| S07_default_capital_tier1_fail | 202401 | MON-D26, MON-D27 | Default params. Single LOC account so sum(RWA) = 1,100,000,000.00: TOTAL 7.27 FAIL, TIER1 5.91 FAIL, CET1 4.55 PASS. |
| S08_default_capital_cet1_fail | 202401 | MON-D25, MON-D26, MON-D27 | Default params. Single LOC account so sum(RWA) = 1,200,000,000.00: all three ratios below threshold -> FAIL. |
| S09_default_capital_zero_rwa | 202401 | MON-D24, MON-D25, MON-D26, MON-D27 | Default params. Deposit accounts only (incl. a negative balance): sum(RWA)=0 -> ratios missing, all statuses PASS via the sum(RWA)=0 arm; DELINQUENCY_AGING and LLP_COVERAGE are created with 0 rows. |
| S10_default_capital_negative_rwa | 202401 | MON-D11, MON-D20, MON-D24, MON-D25, MON-D26, MON-D27 | Default params. Only a credit-balance CC account: sum(RWA) < 0 -> ratios missing, CASE falls to ratio test with a negative ratio -> all FAIL. |
| S11_default_capital_missing_rwa | 202401 | MON-D08, MON-D09, MON-D20, MON-D24, MON-D25, MON-D26, MON-D27 | Default params. Only an MTG account with missing CURRENT_BALANCE: sum(RWA) missing -> ratios missing, missing >= threshold is false -> all FAIL. |
| S12_default_empty_month | 202401 | MON-D03, MON-D24, MON-D25, MON-D26, MON-D27, MON-D29 | Default params. No account has SNAPSHOT_DATE = 31JAN2024 (all at 31DEC2023): Steps 1-3 produce 0-row tables, CAPITAL_ADEQUACY still has one row with missing TOTAL_RWA and FAIL statuses. |
| S13_p202402_leap_month_end | 202402 | MON-D02, MON-D03 | report_month=202402 (leap year): month_end=29FEB2024; 28FEB2024 (not a month-end in 2024) and 31JAN2024 rows are dropped. |
| S14_p202302_nonleap_month_end | 202302 | MON-D02, MON-D03, MON-D06 | report_month=202302 (non-leap): month_end=28FEB2023; 27FEB2023 and 31JAN2023 rows are dropped. |
| S15_p202403_quarter_end | 202403 | MON-D02, MON-D03 | report_month=202403 (quarter-end): month_end=31MAR2024; 30MAR2024 and 29FEB2024 rows are dropped. |
| S16_p202312_year_end | 202312 | MON-D02, MON-D03 | report_month=202312 (year-end): month_end=31DEC2023; the seed run date 31JAN2024 and 30NOV2023 rows are dropped. |
| S17_p202404_30day_month_end | 202404 | MON-D02, MON-D03, MON-D15 | report_month=202404 (30-day month): month_end=30APR2024; mid-month 15APR2024 and 31MAR2024 rows are dropped. |
| S18_blank_report_month | (blank) | MON-D01 | report_month= (blank). %parmv logs 'ERROR: REPORT_MONTH is required' and sets parmerr, which the program never tests; inputn('01',yymmdd8.) is missing so month_start/month_end are '.', %substr(,1,4) errors, and the PROC SQL WHERE '.'d is invalid. Expected: no REPORTS table is created or replaced; ERRORs in the log; SYSCC > 0. |

All scenarios with `report_month=202401` use the default macro parameter and the 31JAN2024 run date.

## Running on a SAS host

1. Load each `inputs/<libref>/<DATASET>.csv` into the matching libref (`STG_BANK`, `ORA_DW`) with numeric columns
   numeric (`CURRENT_BALANCE`, `LTV`, `DAYS_PAST_DUE`, `PAST_DUE_AMOUNT`, `ALLOWANCE_AMT`) and DATE9. columns as
   SAS dates. Empty cells must become SAS missing (`.` / blank), not 0. Clear `REPORTS` between scenarios.
2. Run the program; for non-default months call `%monthly_regulatory_reporting(report_month=<value>)` (the source
   only invokes the default, which resolves to `&PREV_YM` = 202401); for S18 call with `report_month=`.
3. Export the four REPORTS tables to CSV with unformatted values and compare with `tools/parity_diff.py`
   (keys in `tools/keys/sas_keys.json`). Row order is not significant; ties in `MONTHLY_RWA` (same type/segment,
   different RISK_WEIGHT) have no defined order in the SAS `order by`.

## Things the SAS-host run must know

- The `%include` paths are hard-coded to `/opt/sas/custom/macros/` (not `&REPO_ROOT`).
- `%export_xlsx` is called with `file=` / `sheet=`, which are not parameters of the macro (`DATA`, `PATH`, `REPLACE`,
  `LABEL`), and it delegates to `%export_dbms`, which is not in the repository. Expect macro ERRORs and no workbook
  (MON-D30). If the host is in batch with syntax-check-on-error, `CAPITAL_ADEQUACY` (created after the exports) may
  not be produced; record the log and SYSCC with the golden output.
- S18 (blank `report_month`) has no expected tables: `%parmv` logs an ERROR, `parmerr` is never tested, the derived
  dates are invalid and every PROC SQL step should fail. Capture the log as the golden artefact.
- Floating-point boundary: S05 relies on `80000000/1000000000*100 >= 8.0` (evaluates to exactly 8.0 in IEEE double).

## Cross-checks performed

- The hand-derivation evaluator reproduces the committed `baseline/sas/` outputs for the seed data (parity_diff: MATCH).
- `tools/sas_baseline.py` (unmodified, via a throwaway runner) on S01-S12: all four targets MATCH `expected_provisional`.
  S13-S18 cannot be cross-checked because the re-implementation hard-codes the 31JAN2024 run date.
- The dbt port was reviewed statically; suspected divergences are listed in the run summary (S04 values).
