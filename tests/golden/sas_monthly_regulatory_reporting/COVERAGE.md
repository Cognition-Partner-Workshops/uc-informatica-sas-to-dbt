# Branch coverage: monthly_regulatory_reporting

Authority: `legacy/sas/programs/monthly_regulatory_reporting.sas` (line numbers below), the macros it `%include`s
(`parmv.sas`, `nobs.sas`, `export_xlsx.sas`) and `legacy/sas/config/autoexec_local.sas`.

Seed = `legacy/sas/data/csv` loaded into DuckDB, with `STG_BANK.CUST_ACCOUNTS_DAILY` taken from
`baseline/sas/CUST_ACCOUNTS_DAILY.csv` (466 rows, all `SNAPSHOT_DATE = 31JAN2024`; the seed tree has no `stg_bank`
directory) and `ORA_DW.LOAN_DETAILS` from `oracle_dw/LOAN_DETAILS.csv` (248 rows), default `report_month=202401`.
Counts are rows (or groups / runs, as labelled) taking each side. A decision is exercised (Y) only if every side has
a count > 0. "Covering scenarios" lists the scenarios that hit the sides the seed misses (all touching scenarios
when the decision is already exercised).

Summary: 30 decision points, 2 exercised by seed, 28 not exercised.
Every unexercised side is hit by at least one scenario except MON-D30 "valid DATA=/PATH= invocation", which is
unreachable without changing the SAS source (see notes).

| ID | SAS line(s) | Condition | Seed rows per side | Exercised | Covering scenarios |
|----|-------------|-----------|--------------------|-----------|--------------------|
| MON-D01 | 24 (parmv.sas) | %parmv(report_month,_req=1): value supplied vs blank (blank logs ERROR, sets parmerr; caller never tests parmerr so steps still run with an invalid date) | non-blank: 1; blank: 0 (runs) | N | S18 |
| MON-D02 | 26-28 | report_month month-end variant fed to inputn/intnx(month,..,0,E) | 31-day non-quarter month-end (incl. default 202401): 1; 30-day month-end: 0; Feb leap-year month-end (29th): 0; Feb non-leap month-end (28th): 0; quarter-end (non-Dec): 0; year-end (Dec 31): 0 (runs) | N | S13, S14, S15, S16, S17 |
| MON-D03 | 63, 94, 137 | WHERE a.SNAPSHOT_DATE = "&month_end"d | = month_end (kept): 466; other month-end date (dropped): 0; non-month-end / mid-month date (dropped): 0; missing SNAPSHOT_DATE (dropped): 0 (account rows) | N | S01, S12, S13, S14, S15, S16, S17 |
| MON-D04 | 61-62 | Step 1 LEFT JOIN LOAN_DETAILS on ACCOUNT_ID (all account types) | no LOAN_DETAILS match: 230; exactly one match: 236; multiple matches (fan-out): 0 (accounts at month_end) | N | S04 |
| MON-D05 | 46-56 | RISK_WEIGHT CASE arm taken | CHK/SAV/MMA: 188; CD: 24; MTG<=0.80: 40; MTG>0.80: 20; HELC: 14; AUTO/PERS: 55; CC: 91; LOC: 16; ELSE: 18 (joined rows) | Y | S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S13, S14, S15, S16, S17 |
| MON-D06 | 49-50 | MTG LTV test (SAS missing < 0.80, so missing LTV takes the 0.35 arm) | LTV < 0.80: 40; LTV = 0.80: 0; LTV > 0.80: 20; LTV missing on matched LOAN row: 0; no LOAN row (LTV missing via join): 0 (MTG joined rows) | N | S01, S03, S14 |
| MON-D07 | 55 | RISK_WEIGHT ELSE source (case-sensitive compare, blank = missing char) | IRA: 18; blank ACCOUNT_TYPE: 0; other unlisted code (e.g. lowercase 'mtg'): 0 (ELSE rows) | N | S04 |
| MON-D08 | 58-59 | CURRENT_BALANCE missing: CURRENT_BALANCE*RISK_WEIGHT is missing; sum() ignores it but count(*) still counts the row | non-missing: 466; missing: 0 (joined rows) | N | S03, S11 |
| MON-D09 | 58-59 | MONTHLY_RWA group where every CURRENT_BALANCE is missing -> TOTAL_EXPOSURE and RWA missing | >=1 non-missing balance: 59; all balances missing: 0 (output groups) | N | S03, S11 |
| MON-D10 | 45, 64 | CUSTOMER_SEGMENT blank forms its own group (sorts first) | present: 466; blank: 0 (joined rows) | N | S04 |
| MON-D11 | 59 | sign of CURRENT_BALANCE*RISK_WEIGHT for weighted (RISK_WEIGHT>0) rows | > 0: 254; = 0: 0; < 0: 0 (weighted rows) | N | S01, S03, S10 |
| MON-D12 | 95, 138 | ACCOUNT_TYPE in ('MTG','AUTO','PERS','CC','LOC','HELC') | loan type (kept): 236; not a loan type / blank (dropped): 230 (accounts at month_end) | Y | S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S13, S14, S15, S16, S17 |
| MON-D13 | 92-93 | Step 2 LEFT JOIN LOAN_DETAILS (loan-type accounts) | no LOAN_DETAILS match: 0; exactly one match: 236; multiple matches (fan-out): 0 (loan-type accounts) | N | S01, S02, S03, S04 |
| MON-D14 | 78-87 | DELINQ_BUCKET CASE arm taken | Current: 186; 1-29: 25; 30-59: 13; 60-89: 8; 90-119: 1; 120-179: 1; 180+: 2; Unknown: 0 (joined rows) | N | S01, S02, S03, S04 |
| MON-D15 | 80-85 | DELINQ_BUCKET inclusive BETWEEN / >= boundaries (DAYS_PAST_DUE exactly at an edge) | 1: 0; 29: 1; 30: 1; 59: 0; 60: 0; 89: 0; 90: 0; 119: 0; 120: 0; 179: 0; 180: 0 (joined rows) | N | S02, S03, S17 |
| MON-D16 | 86 | 'Unknown' bucket source | no LOAN row (DPD missing via join): 0; DAYS_PAST_DUE missing on LOAN row: 0; negative DAYS_PAST_DUE: 0; non-integer DPD in a BETWEEN gap (e.g. 29.5): 0 (Unknown rows) | N | S01, S02, S03, S04 |
| MON-D17 | 90 | DELINQUENCY_AGING group where every PAST_DUE_AMOUNT is missing -> TOTAL_PAST_DUE missing | >=1 non-missing: 70; all missing: 0 (output groups) | N | S01, S02, S03 |
| MON-D18 | 77, 96 | REGION_CODE blank forms its own group (sorts first) | present: 236; blank: 0 (joined rows) | N | S04 |
| MON-D19 | 135-136 | Step 3 INNER JOIN LOAN_DETAILS (loan-type accounts) | no match (account dropped from LLP): 0; exactly one match: 236; multiple matches (fan-out): 0 (loan-type accounts) | N | S01, S02, S03, S04 |
| MON-D20 | 122-126 | COVERAGE_PCT: sum(CURRENT_BALANCE) > 0 (missing is not > 0) | > 0: 6; <= 0: 0; missing (all balances missing): 0 (output groups) | N | S03, S10, S11 |
| MON-D21 | 124 | COVERAGE_PCT numerator sum(ALLOWANCE_AMT) when GROSS_LOANS > 0 | non-missing: 6; all missing -> COVERAGE_PCT missing: 0 (output groups) | N | S03 |
| MON-D22 | 127 | NPL CASE l.DAYS_PAST_DUE >= 90 (missing is not >= 90 -> 0) | >= 90: 4; < 90: 232; missing: 0 (inner-joined rows) | N | S02, S03 |
| MON-D23 | 129-133 | NPL_COVERAGE_PCT: calculated NPL_BALANCE > 0 | > 0: 2; <= 0: 4; missing (every NPL row has missing balance): 0 (output groups) | N | S03 |
| MON-D24 | 173, 178-180 | ratio CASE sum(RWA) > 0 else . (summary query always returns one row) | > 0: 1; = 0: 0; < 0: 0; missing (no rows or all RWA missing): 0 (runs) | N | S09, S10, S11, S12 |
| MON-D25 | 182 | CET1_STATUS (threshold 4.5) | PASS via sum(RWA)=0: 0; PASS ratio >= 4.5: 1; FAIL ratio < 4.5: 0; FAIL via sum(RWA) missing or negative: 0 (runs) | N | S08, S09, S10, S11, S12 |
| MON-D26 | 184 | TIER1_STATUS (threshold 6.0) | PASS via sum(RWA)=0: 0; PASS ratio >= 6.0: 1; FAIL ratio < 6.0: 0; FAIL via sum(RWA) missing or negative: 0 (runs) | N | S07, S08, S09, S10, S11, S12 |
| MON-D27 | 186 | TOTAL_CAPITAL_STATUS (threshold 8.0) | PASS via sum(RWA)=0: 0; PASS ratio >= 8.0: 1; FAIL ratio < 8.0: 0; FAIL via sum(RWA) missing or negative: 0 (runs) | N | S06, S07, S08, S09, S10, S11, S12 |
| MON-D28 | 186 | >= is inclusive: TOTAL_CAPITAL_RATIO exactly 8.0 (sum(RWA)=1,000,000,000) | ratio exactly 8.0: 0; ratio not exactly 8.0: 1 (runs) | N | S05 |
| MON-D29 | 40-141, 170-190 | empty input for the month (no account at month_end): Steps 1-3 create 0-row tables, Step 5 still emits 1 row with missing TOTAL_RWA | rows at month_end: 1; no rows at month_end: 0 (runs) | N | S12 |
| MON-D30 | 146-164 (export_xlsx.sas) | %export_xlsx invoked with FILE=/SHEET= which are not parameters of the macro (DATA,PATH,REPLACE,LABEL); %export_dbms is not in the repo | invocation as coded (macro ERROR, no workbook): 1; valid DATA=/PATH= invocation: 0 (runs) | N | - |

## Not decision points for this program (inspected, no reachable branch)

- `%nobs` (`nobs.sas`) is `%include`d but never called, so its missing-dataset / 0-observation branches are dead code here.
  Empty input is handled by PROC SQL itself (MON-D29).
- `%lock` and `%sendmail` are not included or called; there is no `%abort`, `SYSCC` test or `parmerr` test in the program.
- No user format from `legacy/sas/formats/banking_formats.sas` is applied (no `put()`/`format` statement on a code column);
  only the display formats `dollar20.2` / `8.2` are attached, which do not change stored values, so there is no
  format OTHER / unmatched-label branch.
- `CURATED.DAILY_TRANSACTIONS` and `ORA_DW.COLLATERAL` are listed in the program header but never read.
- Run date: the program has no run-date input other than `report_month` (default `&PREV_YM`, fixed to `202401` in
  `autoexec_local.sas`); `CURR_DT` is not referenced. Run-date variants are therefore expressed as `report_month`
  values (MON-D02) plus SNAPSHOT_DATE values that are month-end / mid-month / missing (MON-D03).
