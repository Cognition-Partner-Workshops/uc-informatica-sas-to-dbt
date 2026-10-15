# Golden-dataset kit: `credit_risk_scoring` (PROVISIONAL)

Branch-coverage scenarios for `legacy/sas/programs/credit_risk_scoring.sas`. A SAS host runs each scenario to replace
`expected_provisional/` with true golden output. Nothing here was produced by SAS: every expected file was hand-derived
from the SAS source (row-by-row transliteration of the DATA step / PROC SQL / PROC MEANS semantics, SAS missing-value
rules) and is **provisional** until a SAS run confirms it.

## Layout
- `COVERAGE.md` — decision table (CRE-D01..CRE-D35): SAS lines, condition, seed rows per side, exercised Y/N, covering scenarios.
- `scenarios.json` — manifest `[{id, description, decision_ids, params, targets}]`; `params` are the macro parameters
  of `%credit_risk_scoring(score_date=, model_id=)`.
- `scenarios/<id>/inputs/<libref>/<DATASET>.csv` — `stg_bank/CUST_ACCOUNTS_DAILY` (supplied directly, full 33-column
  legacy layout; columns not read by this program are blank), `oracle_dw/BUREAU_SCORES`, `oracle_dw/PAYMENT_HISTORY`,
  `oracle_dw/COLLATERAL`, and for S04 only `curated/RISK_SCORES` + `curated/RISK_MIGRATION` (pre-existing history).
  Same conventions as `legacy/sas/data/csv`: dates are DATE9. text, empty field = missing (numeric `.` / blank char).
- `scenarios/<id>/expected_provisional/{RISK_SCORES,RISK_MIGRATION,RISK_SUMMARY}.csv` — legacy column order;
  `SCORE_TIMESTAMP` (wall clock) excluded, as in `tools/sas_baseline.py`. Values are unformatted (no `percent8.4`,
  `dollar18.2`, `8.4`), full double precision; dates written ISO `YYYY-MM-DD` so `tools/parity_diff.py` can normalise them;
  empty = missing. Row order is not significant (PROC SQL without ORDER BY); files are sorted by SCORE_DATE, ACCOUNT_ID.
  RISK_SUMMARY order is the PROC MEANS class order (ACCOUNT_TYPE, NEW_RISK_RATING).

## Scenarios
| ID | params | decisions targeted (all ids in `scenarios.json`) |
|---|---|---|
| S01_default_branches | defaults | every WOE bin incl. missing FICO/UTIL/DPD/AGE/LTV (D13-D18), collateral 0/<0/missing and missing balance (D12), LGD clamp to 0 and 1 (D19-D20), missing BALANCE / CREDIT_LIMIT in `+`/`*` arithmetic (D22), rating 5 (D23), NEW/UPGRADE/DOWNGRADE/dropped (D25-D26), excluded date/missing date/excluded types (D01-D02), bureau miss and future-only bureau rows, bureau dated on score_date (D03-D04), payment miss (D08), PROC MEANS groups with some / all EAD missing (D30) |
| S02_join_cardinality_missing_keys | defaults | tied latest bureau date (D05), duplicate PAYMENT_HISTORY / COLLATERAL / CUST_ACCOUNTS_DAILY keys (D09, D11, D24), bureau rows with missing SCORE_DATE (D06), blank CUSTOMER_ID (D07) |
| S03_no_scored_rows | defaults | empty WORK.SCORED, `%nobs`=0, zero-row PROC MEANS (D31) |
| S04_append_to_existing_curated | defaults | PROC APPEND onto existing CURATED.RISK_SCORES / RISK_MIGRATION (D27-D28) |
| S05_mid_month_15JAN2024 | score_date=15JAN2024 | mid-month date (D32), future bureau row relative to score_date |
| S06_quarter_end_31MAR2024 | score_date=31MAR2024 | quarter-end (D32) |
| S07_year_end_31DEC2023 | score_date=31DEC2023 | year-end (D32) |
| S08_leap_day_model_override | score_date=29FEB2024, model_id=CRM-2024-Q1-V3 | leap day (D32), model override (D33), already-uppercase model_id (D35) |
| S09_blank_model_id | model_id blank | `%parmv` required-parameter ERROR, run continues, blank MODEL_ID (D34) |
| S10_blank_score_date | score_date blank | `%parmv` ERROR + invalid `""d` constant: no rows produced (D34); expected files are header-only |

## What the SAS host must know / assumptions
1. **MODEL_ID case.** `%parmv` defaults to `_CASE=U` and executes `%let &_parm = %qupcase(&&&_parm)`, which rewrites the
   caller's `model_id`. Expected MODEL_ID is therefore `CRM-2023-Q4-V2` (capital V) for the default. `tools/sas_baseline.py`
   and the dbt port emit `CRM-2023-Q4-v2`. Confirm on the host.
2. `%include "/opt/sas/custom/macros/parmv.sas"` / `nobs.sas` use host paths; point them at `legacy/sas/macros/`. `%lock` and
   (inside it) `%handle` are not `%include`d: they must come from the autocall path. `%handle` has no definition in this repo.
3. `%lock(CURATED.RISK_SCORES)` passes a positional argument to a keyword-only macro; expected behaviour assumed: "ERROR: More
   positional parameters found than defined", lock not taken, PROC APPEND still runs. If the host's autocall `%lock` differs,
   CRE-D29 must be re-inventoried.
4. `%parmv` references `&parmerr` and `&macro`, which `credit_risk_scoring` never declares: expect "Apparent symbolic reference"
   WARNINGs; they do not change outputs. A blank `model_id` (S09) logs ERROR but does not stop the macro.
5. S10: expected outcome is a failing job (SYSCC > 4, no target rows). If the host instead creates empty targets, the
   header-only files still apply.
6. Load each scenario fresh: empty CURATED/REPORTS libraries (except S04's curated inputs), STG_BANK.CUST_ACCOUNTS_DAILY taken
   from the scenario CSV (do not run `load_customer_accounts`). Import CSVs with numeric columns numeric, DATE9. columns as SAS
   dates, empty fields as missing; char key columns blank (not the string "NA").
7. PD is bounded by the coefficients to [0.01438, 0.12884]: ratings 1, 2, 6, 7 and MIGRATION_DIRECTION='STABLE' are dead code
   (marked unreachable in COVERAGE.md).
8. Compare with `tools/parity_diff.py` using keys RISK_SCORES=[ACCOUNT_ID, FICO_SCORE, PMT_LATE_90_12MO, COLLATERAL_VALUE],
   RISK_MIGRATION=[ACCOUNT_ID, PREV_RATING, PD], RISK_SUMMARY=[ACCOUNT_TYPE, NEW_RISK_RATING]. S02 contains intentional
   duplicate rows (fan-out); compare it as a multiset.

## Cross-check against `tools/sas_baseline.py` (default-param scenarios S01-S04)
Run from a throwaway script (inputs swapped in before the `scored` table is built), diffed with `tools/parity_diff.py`:
- S01: only MODEL_ID differs (assumption 1); all other values in all three targets match.
- S02: baseline keeps one arbitrary row on a tied latest bureau date (`row_number()`), drops bureau rows whose SCORE_DATE is
  missing (SQL NULL <= date is unknown), and never matches a blank CUSTOMER_ID (loaded as NULL). SAS fans out on ties, includes
  missing dates in the correlated max/equality, and matches blank to blank.
- S03: match.
- S04: baseline ignores existing CURATED history (outputs are rebuilt, not appended).
