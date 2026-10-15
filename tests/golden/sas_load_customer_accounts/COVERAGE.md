# load_customer_accounts — decision coverage

Source of truth: `legacy/sas/programs/load_customer_accounts.sas` (line numbers below), the `%parmv`/`%nobs`/`%sendmail` macros it includes and `legacy/sas/formats/banking_formats.sas`.

Seed = `legacy/sas/data/csv` with run date 31JAN2024 and default macro parameters (one run). Seed counts are rows taking each side: input account rows for join/WHERE decisions, extracted rows (466) for DATA-step decisions; for macro-parameter and %nobs decisions the count is runs (the seed is one run). A decision is exercised only if every side has a count > 0.

Scenario IDs refer to `scenarios.json` / `scenarios/<id>/` (prefix only, e.g. S02 = `S02_default_derivations_exceptions`).

| ID | SAS line(s) | Condition | Side | Seed rows | Exercised by seed | Covering scenarios |
|---|---|---|---|---|---|---|
| LOA-D01 | 19 | %parmv(run_date, _req=1, _msg=...) -- run_date supplied? | a: run_date supplied (note: _msg= makes %parmv always log ERROR) | 1 run | N | S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13, S14 |
|  |  |  | b: run_date blank | 0 |  | S15 |
| LOA-D02 | 20 | %parmv(region, _val=ALL NE SE MW SW W NW, _case=U) | a: valid value as given | 1 run | N | S01, S02, S03, S04, S05, S06, S07, S11, S12, S13, S14, S15 |
|  |  |  | b: valid after upcase (lowercase input) | 0 |  | S08 |
|  |  |  | c: not in list (ERROR logged, run continues) | 0 |  | S09 |
|  |  |  | d: blank (allowed, _req=0) | 0 |  | S10 |
| LOA-D03 | 17, 63, 100, 103, 150 | run_date value class | a: 31JAN2024 default (month-end) | 1 run | N | S01, S02, S03, S04, S05, S06, S07, S08, S09, S10 |
|  |  |  | b: mid-month | 0 |  | S11 |
|  |  |  | c: quarter-end | 0 |  | S12 |
|  |  |  | d: year-end | 0 |  | S13 |
|  |  |  | e: leap day 29FEB | 0 |  | S14 |
| LOA-D04 | 64 | %if &region ne ALL (region filter added?) | a: ALL: no filter | 1 run | N | S01, S02, S03, S04, S05, S06, S11, S12, S13, S14 |
|  |  |  | b: not ALL: filter added | 0 |  | S07, S08, S09, S10 |
| LOA-D05 | 65 | d.REGION_CODE = "&region" (when filter active) | a: equal (kept) | 0 | N | S07, S08, S09 |
|  |  |  | b: different non-missing (excluded) | 0 |  | S07, S08, S09, S10 |
|  |  |  | c: missing REGION_CODE, non-blank param (excluded) | 0 |  | S07 |
|  |  |  | d: missing REGION_CODE, blank param (kept) | 0 |  | S10 |
| LOA-D06 | 59-61 | inner join CUST_ACCOUNTS a / CUST_DEMOGRAPHICS d on CUSTOMER_ID | a: account matches 1 demographics row | 487 | N | S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13, S14 |
|  |  |  | b: account with no demographics row (dropped) | 0 |  | S01, S04 |
|  |  |  | c: demographics row with no account (dropped) | 0 |  | S01 |
|  |  |  | d: account matches >1 demographics rows (fan-out) | 0 |  | S01, S06 |
| LOA-D07 | 61 | PROC SQL join on missing key (SAS: missing = missing) | a: non-missing CUSTOMER_ID matched | 487 | N | S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13, S14 |
|  |  |  | b: missing CUSTOMER_ID matched to missing CUSTOMER_ID | 0 |  | S01 |
| LOA-D08 | 62 | a.ACCOUNT_STATUS not in ('W','C') | a: W (excluded) | 7 | N | S01, S04 |
|  |  |  | b: C (excluded) | 14 |  | S01, S03, S04, S05, S07, S08, S09, S10 |
|  |  |  | c: other code (kept) | 466 |  | S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13, S14 |
|  |  |  | d: missing (kept) | 0 |  | S01 |
|  |  |  | e: lowercase w/c (kept, case-sensitive) | 0 |  | S01 |
| LOA-D09 | 63 | a.OPEN_DATE <= "&run_date"d | a: before run date (kept) | 487 | N | S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13, S14 |
|  |  |  | b: equal (kept) | 0 |  | S01, S11, S12, S13, S14 |
|  |  |  | c: after (excluded) | 0 |  | S01, S04, S11, S12, S13, S14 |
|  |  |  | d: missing (kept: missing sorts lowest) | 0 |  | S01 |
| LOA-D10 | 71-77 | %if &nobs_raw = 0 %then %goto EXIT | a: rows extracted | 1 run | N | S01, S02, S03, S05, S06, S07, S08, S09, S10, S11, S12, S13, S14 |
|  |  |  | b: 0 rows: EXIT, no target written | 0 |  | S04 |
| LOA-D11 | 100 | intck('month', OPEN_DATE, run_date) | a: same month -> 0 | 0 | N | S01, S02, S11, S12, S13, S14 |
|  |  |  | b: earlier month -> boundary count | 466 |  | S01, S02, S03, S05, S06, S07, S08, S09, S10, S11, S12, S13, S14 |
|  |  |  | c: OPEN_DATE missing -> missing | 0 |  | S01 |
| LOA-D12 | 103 | run_date - LAST_ACTIVITY_DATE | a: >= 0 | 466 | N | S01, S02, S03, S05, S06, S07, S08, S09, S10, S11, S12, S13, S14 |
|  |  |  | b: activity after run date -> negative | 0 |  | S02, S11 |
|  |  |  | c: LAST_ACTIVITY_DATE missing -> missing | 0 |  | S02 |
| LOA-D13 | 106-109 | ACCOUNT_TYPE in ('CC','LOC','HELC') and CREDIT_LIMIT > 0 | a: true -> computed | 121 | N | S02, S07, S11, S13 |
|  |  |  | b: revolving, limit <= 0 -> . | 0 |  | S02 |
|  |  |  | c: revolving, limit missing -> . | 0 |  | S02 |
|  |  |  | d: non-revolving -> . | 345 |  | S01, S02, S03, S05, S06, S07, S08, S09, S10, S11, S12, S13, S14 |
| LOA-D14 | 107 | (CURRENT_BALANCE / CREDIT_LIMIT) * 100 missing propagation | a: balance present | 121 | N | S02, S07, S11, S13 |
|  |  |  | b: balance missing -> missing | 0 |  | S02 |
| LOA-D15 | 112-115 | DAYS_INACTIVE > 365 and ACCOUNT_STATUS = 'A' | a: >365 and A -> Y | 19 | N | S02, S11, S12, S13, S14 |
|  |  |  | b: >365, status not A -> N | 1 |  | S02 |
|  |  |  | c: =365 -> N | 0 |  | S02, S11, S12, S13, S14 |
|  |  |  | d: DAYS_INACTIVE missing -> N | 0 |  | S02 |
|  |  |  | e: <365 -> N | 446 |  | S01, S02, S03, S05, S06, S07, S08, S09, S10, S11, S12, S13, S14 |
| LOA-D16 | 118-121 | CURRENT_BALANCE >= 250000 | a: >250000 -> Y | 51 | N | S02 |
|  |  |  | b: =250000 -> Y | 0 |  | S02, S13 |
|  |  |  | c: <250000 -> N | 415 |  | S01, S02, S03, S05, S06, S07, S08, S09, S10, S11, S12, S13, S14 |
|  |  |  | d: missing -> N | 0 |  | S02 |
| LOA-D17 | 124-130 | ACCOUNT_TYPE in ('CHK','SAV','MMA','CD') and CURRENT_BALANCE < 0 -> NEG_BAL | a: deposit, < 0 -> exception | 7 | N | S02, S05, S06, S10, S12, S14 |
|  |  |  | b: deposit, missing -> exception (missing < 0) | 0 |  | S02 |
|  |  |  | c: deposit, = 0 -> none | 0 |  | S02 |
|  |  |  | d: deposit, > 0 -> none | 205 |  | S01, S02, S03, S05, S07, S08, S09, S11, S12, S13, S14 |
|  |  |  | e: non-deposit, < 0 or missing -> none | 0 |  | S01, S02 |
| LOA-D18 | 133-139 | UTILIZATION_PCT > 95 -> HIGH_UTIL | a: > 95 -> exception | 9 | N | S02, S07, S11, S13 |
|  |  |  | b: = 95 -> none | 0 |  | S02 |
|  |  |  | c: < 95 -> none | 112 |  | S02 |
|  |  |  | d: missing -> none | 345 |  | S01, S02, S03, S05, S06, S07, S08, S09, S10, S11, S12, S13, S14 |
| LOA-D19 | 142-147 | RISK_RATING = . -> NO_RISK | a: missing -> exception | 16 | Y | S01, S02, S06 |
|  |  |  | b: present -> none | 450 |  | S01, S02, S03, S05, S06, S07, S08, S09, S10, S11, S12, S13, S14 |
| LOA-D20 | 129, 138, 146 | explicit OUTPUT count per observation to WORK.ACCT_EXCEPTIONS | a: 0 | 435 | Y | S01, S02, S03, S05, S07, S08, S09, S11, S12, S13, S14 |
|  |  |  | b: 1 | 30 |  | S01, S02, S05, S06, S07, S10, S11, S12, S13, S14 |
|  |  |  | c: 2 | 1 |  | S02, S06 |
| LOA-D21 | 87; formats 15-28 | $ACCTTYPE. on ACCOUNT_TYPE | a: listed code | 466 | N | S01, S02, S03, S05, S06, S07, S08, S09, S10, S11, S12, S13, S14 |
|  |  |  | b: OTHER='Unknown' (unlisted) | 0 |  | S01 |
|  |  |  | c: blank -> OTHER | 0 |  | S01 |
| LOA-D22 | 88; formats 31-41 | $ACCTSTAT. on ACCOUNT_STATUS | a: listed code | 466 | N | S01, S02, S03, S05, S06, S07, S08, S09, S10, S11, S12, S13, S14 |
|  |  |  | b: OTHER='Unknown' (unlisted) | 0 |  | S01 |
|  |  |  | c: blank -> OTHER | 0 |  | S01 |
| LOA-D23 | 89; formats 44-53 | RISKRATE. on RISK_RATING | a: 1-7 | 450 | N | S01, S02, S03, S05, S06, S07, S08, S09, S10, S11, S12, S13, S14 |
|  |  |  | b: OTHER='Not Rated' (non-missing, unlisted) | 0 |  | S01 |
|  |  |  | c: missing -> OTHER | 16 |  | S01, S02, S06 |
| LOA-D24 | 90; formats 106-114 | $CUSTSEG. on CUSTOMER_SEGMENT | a: listed code | 466 | N | S01, S02, S03, S05, S06, S07, S08, S09, S10, S11, S12, S13, S14 |
|  |  |  | b: OTHER='Unclassified' (unlisted) | 0 |  | S01 |
|  |  |  | c: blank -> OTHER | 0 |  | S01 |
| LOA-D25 | 91; formats 94-103 | $REGION. on REGION_CODE | a: listed code (incl. HQ) | 466 | N | S01, S02, S03, S05, S06, S07, S08, S09, S11, S12, S13, S14 |
|  |  |  | b: OTHER='Unknown' (unlisted) | 0 |  | S01 |
|  |  |  | c: blank -> OTHER | 0 |  | S01, S10 |
| LOA-D26 | 164-170 | %if &nobs_except > 0 -> INSERT INTO STG_BANK.ACCT_EXCEPTIONS | a: > 0 -> insert | 1 run | N | S01, S02, S05, S06, S07, S10, S11, S12, S13, S14 |
|  |  |  | b: = 0 -> no insert (prior rows untouched) | 0 |  | S03, S08, S09 |
| LOA-D27 | 173-180 | %if &nobs_except > 100 -> %sendmail | a: <= 100 | 1 run | N | S01, S02, S03, S05, S07, S08, S09, S10, S11, S12, S13, S14 |
|  |  |  | b: > 100 -> sendmail branch | 0 |  | S06 |
| LOA-D28 | 168-169 | INSERT appends to prior STG_BANK.ACCT_EXCEPTIONS | a: prior table empty | 1 run | N | S01, S02, S06, S07, S08, S09, S10, S11, S12, S13, S14 |
|  |  |  | b: prior table has rows (accumulate) | 0 |  | S03, S05 |
| LOA-D29 | 188-189 | PROC MEANS CLASS ACCOUNT_TYPE REGION_CODE (no MISSING option) | a: both class values present | 466 | N | S01, S02, S03, S05, S06, S07, S08, S09, S11, S12, S13, S14 |
|  |  |  | b: a class value missing -> row excluded from WORK.ACCT_SUMMARY | 0 |  | S01, S10 |
| LOA-D30 | 190-196 | PROC MEANS n=/sum/mean ignore missing | a: all analysis vars present | 121 | N | S02, S07, S11, S13 |
|  |  |  | b: UTILIZATION_PCT missing (ignored by mean) | 345 |  | S01, S02, S03, S05, S06, S07, S08, S09, S10, S11, S12, S13, S14 |
|  |  |  | c: CURRENT_BALANCE missing (excluded from n=, sum, mean) | 0 |  | S02 |

**Totals:** 30 decision points; 2 exercised by the seed, 28 not exercised. Every side of every decision is hit by at least one scenario.

## Notes on the inventory

- `%lock` (lock.sas, line 15) is `%include`d but never invoked: no lock path exists, so it is not a decision point.
- No hash objects, BY-group FIRST./LAST., RETAIN, `||`/catx-into-target or sum()-vs-+ constructs reach a persisted column in this program. EXCEPTION_CODE / EXCEPTION_DESC (catx, put dollar18.2 / 5.1) are dropped from BOTH outputs by the global DROP statement (line 156), so their formatting is unobservable and is not inventoried as a decision.
- LOA-D21..D25 (format OTHER labels) are display-only in SAS; they are observable here through the `*_DESC` companion columns that tools/sas_baseline.py and the dbt port materialize on CUST_ACCOUNTS_DAILY (see README).
- LOA-D29/D30 only affect WORK.ACCT_SUMMARY, which is deleted at %EXIT; they have no persisted expected output.
- LOA-D03 run-date classes change only date arithmetic and the OPEN_DATE filter; the program has no calendar-specific branch.
