# Golden-dataset kit: `claims_processing` (PROVISIONAL)

Every file under `scenarios/*/expected_provisional/` is **hand-derived from the SAS source** (`legacy/sas/programs/claims_processing.sas`, `%parmv`, `%nobs`, `%sendmail`, `$CLMSTAT.`). No SAS runtime was available. They are **provisional** until a SAS host runs each scenario and replaces them with real output. `tools/sas_baseline.py` was used only as a second opinion (see "Baseline cross-check").

- `COVERAGE.md` – decision inventory (CLA-D01..CLA-D31), seed hits per side, covering scenarios.
- `scenarios.json` – manifest: `id`, `description`, `decision_ids`, `params` (macro parameters of `%claims_processing`), `targets`, optional `note`.
- `scenarios/<id>/inputs/<libref>/<DATASET>.csv` – inputs, same conventions as `legacy/sas/data/csv` (dates `DATE9.`, empty cell = missing).
- `scenarios/<id>/expected_provisional/<TARGET>.csv` – STG_INS.CLAIMS_REGISTER, CLAIMS_REVIEW_QUEUE, FRAUD_ALERTS. Header-only file = table empty or not created. Dates are ISO (`YYYY-MM-DD`), as in `tools/sas_baseline.py` output; no wall-clock timestamp columns exist in these targets.

## Running on a SAS host

1. For each scenario, point the librefs at the scenario inputs and import each CSV as a SAS dataset (char columns as char, date columns with `DATE9.` informat, empty = missing; keep the blank `POLICY_ID`/`CLAIMANT_ID` cells as blank character values).
2. `inputs/raw_ins/FRAUD_INDICATORS.csv` stands in for `TERA_DW.FRAUD_INDICATORS` (same as the seed); assign it to the `TERA_DW` libref.
3. `inputs/stg_ins/*.csv` (S07, S08 only) are pre-existing `STG_INS` base tables. In all other scenarios `STG_INS` starts empty (no tables).
4. Run `%claims_processing(proc_date=<params.proc_date>)` with `autoexec_local.sas` macro variables. S15 passes `proc_date=` (blank).
5. Export the three `STG_INS` tables and compare with `tools/parity_diff.py` (align on CLAIM_ID+FRAUD_SCORE; S04 has a duplicate CLAIM_ID by design).

## Scenarios -> decisions

| Scenario | Purpose | Main decisions |
|---|---|---|
| S01_core_rules | hash hit/miss (unknown, LAPSED, `Active` lowercase, blank key with no blank policy), date and amount boundaries (=, <, >), score boundaries 50/80, every adjudication rule and PEND-reason combination, max() clip to 0, catx blank flags | D05 D07 D08 D09-D11 D13 D15-D18 D21-D28 |
| S02_missing_values | missing EFFECTIVE/EXPIRATION/LOSS_DATE, SUM_INSURED, CLAIMED_AMOUNT, DEDUCTIBLE, FRAUD_SCORE | D09-D11 D16 D22-D27 |
| S03_blank_keys | blank POLICY_ID hits a blank-keyed policy; blank CLAIMANT_ID matches a blank-keyed fraud row | D08 D15 |
| S04_duplicate_keys | duplicate ACTIVE POLICY_ID (hash keeps first); fraud join fan-out | D06 D14 |
| S05_fractional_scores | `put(FRAUD_SCORE,4.)` rounds 80.5->81, 92.5->93 | D19 |
| S06_no_high_fraud | `%nobs(FRAUD_ALERTS)=0`: no append, no `%sendmail` | D20 |
| S07_prior_state | PROC APPEND onto existing base tables | D29 |
| S08_feed_missing_abort | feed for 31JAN2024 absent -> `%goto ABORT`; base tables unchanged | D03 |
| S09_empty_feed | zero-row feed | D04 D12 |
| S10_no_active_policies | no ACTIVE policy -> all invalid | D05 D07 D12 |
| S11-S14 | run dates 15JAN2024 (mid-month, decoy 31JAN2024 feed present), 29FEB2024 (leap day), 31MAR2024 (quarter-end), 31DEC2024 (year-end) | D02 |
| S15_blank_proc_date | blank proc_date -> `%parmv` error, feed unresolved, ABORT | D01 D03 |

31JAN2024 (month-end) is the default `&CURR_DT`; S01-S10 use it with default params.

## Provisional assumptions (verify on the SAS host)

- Hash object without `duplicate:` keeps the first record for a duplicate key (S04: GC0401 joins the HOME policy).
- Hash `find()` and PROC SQL `=` treat blank char keys as equal (S03); comparisons with missing numerics follow "missing is lowest" (S02).
- `put(x,4.)` rounds half away from zero (S05). `max(0, missing)` = 0 (S02).
- S15: with blank `proc_date`, `%parmv` sets its error flag but the program does not test it; `"&proc_date"d` then fails, so `exist()` is assumed to return 0 and the program ABORTs. The SAS log may show additional errors.
- `%sendmail` is called with `body=`, which the macro signature does not declare, and the macro uses `%seplist`, which is not in `legacy/sas/macros`. The SAS host needs a stub; it does not affect the datasets.
- `CLAIM_STATUS_DESC` (label of `$CLMSTAT.`) is a migration convenience column, same as `tools/sas_baseline.py`; SAS stores only `CLAIM_STATUS` with the format attached.
- D30 (all-blank PEND reason) and D31 (`$CLMSTAT.` OTHER) cannot be reached: a LOW claim within both thresholds is always approved by rule 3, and CLAIM_STATUS is always APPR/DENY/PEND.

## Baseline cross-check (`tools/sas_baseline.py`, S01-S10)

Matches `expected_provisional` exactly: S01, S06, S10. Differences, each re-checked against the SAS source and believed to be baseline defects: S02 (drops rows with missing EFFECTIVE_DATE or CLAIMED_AMOUNT), S03 (blank keys never match), S04 (duplicate policy fans out), S05 (alert reason rounds 80.5 to 80), S07 (writes tables instead of appending), S08 (fails: feed table missing), S09 (fails on a zero-row feed in DuckDB typing).
