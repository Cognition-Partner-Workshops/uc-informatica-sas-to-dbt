# Golden-dataset kit: `load_customer_accounts` (PROVISIONAL)

Branch-coverage scenarios for `legacy/sas/programs/load_customer_accounts.sas`. A SAS host runs each scenario and
replaces `expected_provisional/` with real SAS output; until then every expected file is **provisional**.

**No SAS runtime was used.** Each expected row was derived from the SAS source (program, `%parmv`, `%nobs`,
`%sendmail`, `banking_formats.sas`, `autoexec_local.sas`), applying the SAS semantics row by row. The rows were
checked by hand and then compared with `tools/sas_baseline.py` (a Python/DuckDB re-implementation, used as a second
opinion and not as the oracle). Where they disagree, the SAS source decides (see "Cross-check" below).

## Files

| Path | Content |
|---|---|
| `COVERAGE.md` | Decision table LOA-D01..LOA-D30: SAS lines, condition, seed rows per side, exercised Y/N, covering scenarios |
| `scenarios.json` | Manifest: `id`, `description`, `decision_ids`, `params` (macro parameters), `targets` |
| `scenarios/<id>/inputs/oracle_dw/CUST_ACCOUNTS.csv`, `CUST_DEMOGRAPHICS.csv` | ORA_DW inputs. Same layout and conventions as `legacy/sas/data/csv` (dates DATE9., empty field = missing) |
| `scenarios/<id>/inputs/stg_bank/ACCT_EXCEPTIONS.csv` | Prior state of STG_BANK.ACCT_EXCEPTIONS (header-only = exists, empty). SAS-native layout: 27 data columns + SNAPSHOT_DATE + LOAD_TIMESTAMP (DATETIME, `30JAN2024:06:00:00`) |
| `scenarios/<id>/inputs/stg_bank/CUST_ACCOUNTS_DAILY.csv` | Prior state of STG_BANK.CUST_ACCOUNTS_DAILY (only in S03, S04, S15). Same SAS-native layout |
| `scenarios/<id>/expected_provisional/<TARGET>.csv` | Expected STG_BANK.CUST_ACCOUNTS_DAILY / ACCT_EXCEPTIONS after the run |

The program reads no RAW_BANK, RAW_INS or CURATED data. (DAILY_RATES is listed in the header comment but is never read.)

## Expected-output conventions

- Columns and order match `baseline/sas/CUST_ACCOUNTS_DAILY.csv` / `ACCT_EXCEPTIONS.csv`. The wall-clock `LOAD_TIMESTAMP`
  is left out, as `tools/sas_baseline.py` does.
- Output dates are ISO `yyyy-mm-dd`, as in `baseline/sas` (inputs use DATE9.). Numbers are unformatted. Empty = missing.
- `CUST_ACCOUNTS_DAILY` carries the `*_DESC` companions (ACCOUNT_TYPE_DESC, ACCOUNT_STATUS_DESC, RISK_RATING_DESC,
  CUSTOMER_SEGMENT_DESC, REGION_CODE_DESC). In SAS these are only the display formats `$ACCTTYPE.`, `$ACCTSTAT.`,
  `RISKRATE.`, `$CUSTSEG.`, `$REGION.`, including OTHER labels. The SAS host must export them as `put(<var>, <fmt>.)`.
  ACCT_EXCEPTIONS has no `*_DESC` columns, matching the baseline layout.
- ACCT_EXCEPTIONS has no EXCEPTION_CODE/EXCEPTION_DESC because the DATA step's global `drop` (line 156) applies to both
  output data sets. SNAPSHOT_DATE is missing on exception rows because the explicit OUTPUT runs before line 150 assigns it.
- Join fan-out produces duplicate ACCOUNT_IDs, and ACCT_EXCEPTIONS repeats a row once per rule hit. So compare with
  `tools/parity_diff.py` using **all columns** as the sort key. For example, build a keys JSON
  `{"CUST_ACCOUNTS_DAILY": [<all header columns>], "ACCT_EXCEPTIONS": [<all header columns>]}` from each expected header.
- Inputs keep at least one non-missing value in every date column, so CSV type inference matches the seed.
  Balances are written with decimals so they load as numeric (double).

## Scenarios

| ID | Params | Decisions targeted (sides) | Key rows |
|---|---|---|---|
| S01_default_extract_join | default | D06 a-d, D07 b, D08 a-e, D09 a-d, D11 a/c, D21-D25 b/c, D29 b | A0102 W / A0103 C excluded; A0104 blank and A0105 `w` status kept; A0106 OPEN_DATE=run date kept; A0107 next day excluded; A0108 missing OPEN_DATE kept (missing sorts low); A0109 x2 (C102 has two demographics rows); A0110 no demographics; C103 no account; A0111 blank CUSTOMER_ID joins blank demographics (PROC SQL matches missing keys); BOND / XYZ / ZZ / 2.5 / 0 hit format OTHER; C105 blank segment/region/risk |
| S02_default_derivations_exceptions | default | D11 b, D12 a-c, D13 a-d, D14 a/b, D15 a-e, D16 a-d, D17 a-e, D18 a-d, D19, D20 a-c, D30 c | 1900/2000 -> exactly 95 (no HIGH_UTIL); missing balance on SAV -> NEG_BAL (missing < 0); 250000.00 -> Y; LAST_ACTIVITY 30JAN2023 -> 366 days Y, 31JAN2023 -> 365 N; A0219/A0220 two exception rows each |
| S03_default_no_exceptions_prior_kept | default | D26 b, D28 b | 0 exceptions -> no INSERT: the prior ACCT_EXCEPTIONS row survives. The prior CUST_ACCOUNTS_DAILY row (A0399) is replaced |
| S04_default_empty_extract_exit | default | D10 b | every account filtered -> %goto EXIT: both prior STG_BANK tables unchanged (SNAPSHOT_DATE 2024-01-30) |
| S05_default_prior_exceptions_append | default | D28 b | prior A0590 + new A0501 NEG_BAL |
| S06_default_sendmail_over_100 | default | D27 b, D06 d | 53 snapshot rows, 101 exception rows (100 for C601 + 1 for C602) -> `%sendmail` branch |
| S07_region_NE | region=NE | D04 b, D05 a/b/c | SE and blank-region rows dropped before the DATA step |
| S08_region_lowercase_sw | region=sw | D02 b | `%parmv _case=U` upcases to SW |
| S09_region_invalid_HQ | region=HQ | D02 c, D25 a | `%parmv` logs ERROR, but `&parmerr` is never tested: the HQ filter still applies |
| S10_region_blank | region= | D02 d, D05 d | `d.REGION_CODE = ""` keeps only blank REGION_CODE |
| S11_run_date_mid_month | run_date=15MAR2024 | D03 b | intck('month', 16FEB2024, 15MAR2024)=1; 366/365 days across 29FEB2024; negative DAYS_INACTIVE |
| S12_run_date_quarter_end | run_date=30JUN2024 | D03 c | ages 3/0/2; 366/365 boundary |
| S13_run_date_year_end | run_date=31DEC2024 | D03 d | 366/365 boundary in leap year 2024; 250000 boundary; HIGH_UTIL 98 |
| S14_run_date_leap_day | run_date=29FEB2024 | D03 e | 28FEB2023 -> 366 Y, 01MAR2023 -> 365 N; 29FEB2020 -> 48 months |
| S15_run_date_blank | run_date= | D01 b | error path: targets expected unchanged (low confidence, see below) |

"default" means `run_date=31JAN2024, region=ALL`. Full side-by-side coverage is in `COVERAGE.md`.

## What is provisional / least certain

- **S15 (blank run_date).** `""d` is an invalid date constant. The expected outcome is: PROC SQL fails, `%nobs` returns
  blank for the absent WORK.ACCT_RAW (so the `=0` abort test is false), the DATA step fails at compile time and does not
  replace STG_BANK.CUST_ACCOUNTS_DAILY, and there is no INSERT. Batch syntax-check mode (OBS=0) and the exact
  `%nobs`/`%parmv` error cascade can only be confirmed on SAS.
- **S10 (blank region).** This assumes PROC SQL treats `""` as equal to a blank (missing) REGION_CODE.
- **S01 A0111.** This assumes the SAS loader stores the empty CUSTOMER_ID as a blank character value on both tables,
  so PROC SQL joins them.
- **S02 A0207.** This assumes IEEE double arithmetic gives `(1900/2000)*100 = 95` exactly (true for Python and x86
  SAS).

## Running on a SAS host (requirements and gotchas)

1. Build `BANKING.FORMATS` from `legacy/sas/formats/banking_formats.sas` and keep `fmtsearch=(BANKING ...)`, as in
   `autoexec_local.sas`.
2. The program `%include`s `/opt/sas/custom/macros/{parmv,nobs,lock}.sas` (and `sendmail.sas`) by absolute path.
   Stage `legacy/sas/macros` there.
3. `autoexec_local.sas` refers to `load_seed_data.sas`, which is not in the repo, so a CSV loader must be written.
   Read date columns with the DATE9. informat (LOAD_TIMESTAMP with DATETIME20.), numeric columns as numeric and the
   rest as character. An empty field must become missing (blank for character columns).
4. Use a fresh STG_BANK library per scenario. **Pre-create STG_BANK.ACCT_EXCEPTIONS** from `inputs/stg_bank/ACCT_EXCEPTIONS.csv`
   with the same 29 columns in the same order: `insert into ... select *` is positional and fails if the table is
   absent. Load `inputs/stg_bank/CUST_ACCOUNTS_DAILY.csv` when it is present.
5. Line 216 always calls `%load_customer_accounts(run_date=&CURR_DT)`. For non-default params, suppress that line
   (for example, `%include` a copy without it) and call the macro once with the scenario's `params`. Do not let both
   calls run: the INSERT would append the exceptions twice.
6. Expected log noise: `%parmv(run_date, ..., _msg=...)` always sets error 5 and writes `ERROR: ... Run date is required`
   even when run_date is valid, because `_msg=` forces the error branch. `&macro`/`&parmerr` are unresolved in the caller.
   The run continues, because the program never tests `&parmerr`.
7. `%sendmail` (S06) is called with `body=`, which is not a parameter of the macro. Expect `ERROR: The keyword parameter BODY
   was not defined with the macro`, and no mail. `%seplist`, which `sendmail.sas` needs, is not in the repo either.
   Keep EMAIL_ONCALL pointed at a sink.
8. `%lock` is included but never called. WORK.ACCT_SUMMARY (PROC MEANS) is deleted at `%EXIT`, so LOA-D29/D30 have no
   persisted output to compare.
9. Export the targets without LOAD_TIMESTAMP, with dates as ISO `yyyy-mm-dd`, numbers unformatted, and the `*_DESC`
   columns as above. Then diff with `tools/parity_diff.py` against `expected_provisional/` using all-column keys.

## Cross-check against tools/sas_baseline.py (S01-S06, default params)

S02 and S06 match exactly. S01 matches except for two rows that the baseline drops:

- A0104 has a missing ACCOUNT_STATUS. The baseline's `not in ('W','C')` is NULL-unsafe and drops the row. SAS keeps
  it, because a blank is not W or C.
- A0111 has a missing CUSTOMER_ID. The baseline uses an ANSI join, but SAS PROC SQL matches missing keys.

S03, S04 and S05 differ because the baseline does not model prior STG_BANK state (no `%goto EXIT` retention, no
INSERT-append, no skipped INSERT). The baseline also hard-codes `region=ALL` and 31JAN2024, so S07-S15 cannot be
cross-checked. The seed has no missing statuses or keys, so these gaps do not affect the existing seed parity.
