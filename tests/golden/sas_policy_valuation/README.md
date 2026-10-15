# Golden-dataset kit: `policy_valuation` (SAS) — PROVISIONAL

This kit holds the inputs a SAS host runs to produce **true golden outputs** for
`legacy/sas/programs/policy_valuation.sas`, covering every reachable branch of the program.
Every file under `expected_provisional/` was **derived by hand from SAS semantics**, without a SAS runtime.
These files are provisional until a SAS host replaces them with real output.

* `COVERAGE.md`: decision inventory (POL-D01 … POL-D46): SAS lines, condition, seed rows per side,
  exercised-by-seed Y/N, and the covering scenarios for each side.
* `scenarios.json`: manifest `[{"id","description","decision_ids","params","targets"}]` (plus `provisional`
  and `expected_outcome`). `params` are the macro parameters `val_date` (DATE9. text) and `lob`.
* `scenarios/<id>/inputs/raw_ins/{POLICIES,CLAIMS,PREMIUMS}.csv`: the only libref/tables the program reads.
  The program reads nothing from `oracle_dw`, `raw_bank`, `curated` or `stg_bank`.
  The CSV conventions match `legacy/sas/data/csv`: dates are DATE9. text, and an empty field is missing.
  A header-only file is a 0-observation data set.
* `scenarios/<id>/expected_provisional/{POLICY_VALUATION,LOSS_RATIO_SUMMARY}.csv`: hand-derived expected targets.

Seed coverage (`legacy/sas/data/csv`, 31JAN2024, lob=ALL): **46 decision points, 9 exercised, 37 not exercised.**
In particular, at a January valuation date every `YTD_EARNED_PREMIUM` is 0. So on the seed, every ratio, adequacy, IBNR
and AGG branch takes only its "else" side, and none of these branches can be proven by the current parity run.

## Scenario → decision map

| Scenario | val_date | lob | Decisions | Expected outcome |
|---|---|---|---|---|
| `S01_default_core` | `31JAN2024` | `ALL` | POL-D01, POL-D02, POL-D03, POL-D05, POL-D06, POL-D07, POL-D08, POL-D10, POL-D11, POL-D12, POL-D15, POL-D16, POL-D17, POL-D18, POL-D19, POL-D20, POL-D21, POL-D22, POL-D23, POL-D24, POL-D25, POL-D26, POL-D27, POL-D34, POL-D35, POL-D36, POL-D37, POL-D46 | POLICY_VALUATION, LOSS_RATIO_SUMMARY |
| `S02_default_missing` | `31JAN2024` | `ALL` | POL-D07, POL-D09, POL-D11, POL-D14, POL-D30, POL-D33, POL-D36, POL-D37, POL-D38, POL-D40, POL-D41, POL-D42 | POLICY_VALUATION, LOSS_RATIO_SUMMARY |
| `S03_default_format_class` | `31JAN2024` | `ALL` | POL-D36, POL-D39 | POLICY_VALUATION, LOSS_RATIO_SUMMARY |
| `S04_default_merge_keys` | `31JAN2024` | `ALL` | POL-D26, POL-D27, POL-D28, POL-D29 | POLICY_VALUATION, LOSS_RATIO_SUMMARY |
| `S05_default_empty_inforce` | `31JAN2024` | `ALL` | POL-D44 | POLICY_VALUATION, LOSS_RATIO_SUMMARY |
| `S06_default_empty_claims_premiums` | `31JAN2024` | `ALL` | POL-D45 | POLICY_VALUATION, LOSS_RATIO_SUMMARY |
| `S07_midmonth_15JUN2024` | `15JUN2024` | `ALL` | POL-D05, POL-D10, POL-D11, POL-D12, POL-D15, POL-D16, POL-D21, POL-D22, POL-D30, POL-D31, POL-D32, POL-D33, POL-D40, POL-D41, POL-D42, POL-D43 | POLICY_VALUATION, LOSS_RATIO_SUMMARY |
| `S08_leapday_29FEB2024` | `29FEB2024` | `ALL` | POL-D05, POL-D07, POL-D10, POL-D12, POL-D15, POL-D16, POL-D21, POL-D22, POL-D30, POL-D32 | POLICY_VALUATION, LOSS_RATIO_SUMMARY |
| `S09_quarterend_31MAR2024` | `31MAR2024` | `ALL` | POL-D05, POL-D10, POL-D15, POL-D30, POL-D32, POL-D33 | POLICY_VALUATION, LOSS_RATIO_SUMMARY |
| `S10_yearend_31DEC2024` | `31DEC2024` | `ALL` | POL-D05, POL-D10, POL-D11, POL-D15, POL-D21, POL-D30, POL-D32, POL-D33 | POLICY_VALUATION, LOSS_RATIO_SUMMARY |
| `S11_lob_auto` | `31JAN2024` | `AUTO` | POL-D02, POL-D03, POL-D04 | POLICY_VALUATION, LOSS_RATIO_SUMMARY |
| `S12_lob_lowercase` | `31JAN2024` | `home` | POL-D02, POL-D03, POL-D04 | POLICY_VALUATION, LOSS_RATIO_SUMMARY |
| `S13_lob_invalid_value` | `31JAN2024` | `VL` | POL-D02, POL-D04 | POLICY_VALUATION, LOSS_RATIO_SUMMARY |
| `S14_lob_multiword` | `31JAN2024` | `AUTO HOME` | POL-D02, POL-D04, POL-D44 | POLICY_VALUATION, LOSS_RATIO_SUMMARY |
| `S15_lob_blank` | `31JAN2024` | `(blank)` | POL-D02, POL-D04, POL-D38 | POLICY_VALUATION, LOSS_RATIO_SUMMARY |
| `S16_val_date_blank` | `(blank)` | `ALL` | POL-D01, POL-D46 | SAS ERROR, no target created |
| `S17_val_date_invalid` | `31FEB2024` | `ALL` | POL-D01, POL-D46 | SAS ERROR, no target created |

Per-side detail is in `COVERAGE.md`. S01–S06 use the default params (`val_date=31JAN2024`, `lob=ALL`) and are the
scenarios cross-checked against `tools/sas_baseline.py`.

## Output conventions (what "same columns/order" means here)

* Column order follows the SAS PDV order of `STG_INS.POLICY_VALUATION`, and it matches `tools/sas_baseline.py`:
  INFORCE columns, then CLAIMS_EXP, then PREMIUM_COLL, then LOSS_RATIO … VALUATION_DATE.
* `POLICY_TYPE` and `RISK_CATEGORY` hold the **raw codes**. In SAS these codes carry `$POLTYPE.` / `$RISKCAT.` formats.
  Following the repo baseline/dbt convention, the formatted values are added as two trailing columns,
  `POLICY_TYPE_DESC = put(POLICY_TYPE,$POLTYPE.)` and `RISK_CATEGORY_DESC = put(RISK_CATEGORY,$RISKCAT.)`.
  These two columns do not exist in the SAS data set; the SAS-host export must add them.
  `PROC EXPORT` writes formatted values by default, so the export must also strip the formats from all variables (e.g. `format _all_;`)
  before writing raw values.
* Numbers are unformatted (no DOLLAR./PERCENT.), with ratios as fractions (0.75, not 75%).
  Dates in the expected outputs are ISO `YYYY-MM-DD`, as in `tools/sas_baseline.py` output. Empty means missing.
* This program writes no wall-clock timestamp columns, so no column was dropped.
  `REPORTS.RESERVE_ADEQUACY` appears in the program header, but the program never creates it, so it is not a target.
* For comparison, use `tools/parity_diff.py` with keys `POLICY_VALUATION: [POLICY_ID]`, `LOSS_RATIO_SUMMARY: [POLICY_TYPE]`.
  S04 deliberately has a missing and a duplicated `POLICY_ID`.

## Instructions for the SAS-host run

1. Use a fresh, empty `STG_INS` and `REPORTS` library per scenario. S16/S17 expect the targets to be **absent**.
2. Load each `inputs/raw_ins/*.csv` into `RAW_INS` with a DATA step using explicit informats
   (`DATE9.` for `*_DATE`, numeric for amounts, `$` with lengths at least those of the seed). Do not use PROC IMPORT, because
   it cannot type the header-only files in S06. Blank character fields must load as missing (blank).
3. The program hard-codes `%include "/opt/sas/custom/macros/parmv.sas"` and `.../nobs.sas`.
   The repo copies are `legacy/sas/macros/parmv.sas` and `nobs.sas`; make them available at that path.
   Compile `legacy/sas/formats/insurance_formats.sas` into the `INSURANCE` catalog on the `FMTSEARCH` path, as `autoexec_local.sas` does.
4. The last line of the program is `%policy_valuation(val_date=&CURR_DT)`, so `lob` cannot be passed through it.
   Set `%let CURR_DT=<params.val_date>;` and run a copy of the program with that invocation replaced by
   `%policy_valuation(val_date=<params.val_date>, lob=<params.lob>)`. Pass `lob=` empty for S15 and `lob=AUTO HOME` for S14.
5. S12–S15 deliberately pass `lob` values that `%parmv` rejects or rewrites. `%parmv` reports them with `%put ERROR:`
   and sets `PARMERR`, but the macro never tests `PARMERR`, so the steps still run. Because a `%put ERROR:` is not a step error,
   batch syntax-check mode (OBS=0) should not be triggered. If it is, record that, because it changes the expected result.
6. Save the log of each scenario. S16 (blank val_date) and S17 (`31FEB2024`) are expected to stop with an invalid
   date-constant ERROR, and no target data set should be created.

## Assumptions to confirm on the SAS host (provisional points)

* **PROC MEANS class levels (POL-D39, S03).** `CLASS POLICY_TYPE` groups by the *formatted* value
  (default ORDER=FORMATTED / GROUPINTERNAL not set). So the unlisted codes `ZZA` and `ZZB` both format to `Unknown`
  and form one level. The output variable is expected to hold the first-encountered raw value (`ZZA`, which is also the lowest).
* **Missing values.** `EFFECTIVE_DATE <= val_date` is true for a missing date (missing sorts lowest), and `max()`/`min()` ignore missing.
  `sum()` (both PROC SQL and PROC MEANS) ignores missing and returns missing only when all values are missing.
  `coalesce` is applied only where the program writes it.
* **MERGE with missing keys (POL-D28, S04).** A missing `POLICY_ID` in WORK.INFORCE matches the missing-key group in
  CLAIMS_EXP/PREMIUM_COLL. A duplicated INFORCE key is a many-to-one merge: both rows receive the same claim/premium values.
* **Boundaries.** `intnx('month',d,n)` aligns to the beginning of the month, `intnx('year',d,0,'B')` gives 1 January,
  and `intck('month',…)` counts month boundaries. `COMBINED_RATIO = 0.7 + 0.30` evaluates to exactly 1.0 in IEEE double,
  so the result is `PREMIUM_ADEQUATE='Y'` (S07 P0000702, S08 P0000801).
* `STATUS = 'ACTIVE'` is case-sensitive: `active` is excluded (S01 P0000111).
* `%nobs` is used only in `%put` notes, so it introduces no data branch.

## Baseline cross-check (`tools/sas_baseline.py`, default-param scenarios S01–S06)

The cross-check pointed `tools/sas_load_raw.py` at each scenario's inputs, then ran `build()` from a throwaway script
(not committed) and diffed the result against `expected_provisional/` with `tools/parity_diff.py`.
S01, S05 and S06 match. The hand derivations were re-checked against the SAS source for every disagreement, and every
remaining mismatch is a suspected baseline divergence:

* POL-D07 (S02): the baseline drops in-force policies whose `EFFECTIVE_DATE` is missing (SQL NULL `<=` is unknown).
  SAS keeps them because missing sorts lowest. The dropped row also shifts `N_POLICIES` for AUTO.
* POL-D38 (S02): the baseline `LOSS_RATIO_SUMMARY` keeps a NULL `POLICY_TYPE` group.
  `PROC MEANS CLASS` excludes missing class values.
* POL-D39 (S03): the baseline groups by the raw `POLICY_TYPE` (two rows ZZA, ZZB).
  `PROC MEANS` groups by the formatted value (one `Unknown` level).
* POL-D28 (S04): the baseline LEFT JOIN cannot match NULL `POLICY_ID`. The SAS MERGE BY matches missing keys, so the
  claim/premium columns and the summary sums differ.

## dbt static check (`dbt/sas_policy_valuation/` on `devin/1792036489-sas-policy-valuation`, read only)

The models reproduce S01, S02, S05–S11 as far as can be judged by reading them. In particular they handle the missing `EFFECTIVE_DATE` inclusion,
the `coalesce(greatest(...),0)` IBNR, the `date_trunc`-based intnx windows, and the exclusion of a missing `POLICY_TYPE` from the summary.
Suspected divergences:

* POL-D02 (S12, S13, S14, S15), `models/intermediate/int_policy_valuation__inforce.sql`: dbt raises a compile error for `home`,
  `VL`, `AUTO HOME` and a blank lob. SAS upcases `home`, and for the other three it logs a `%parmv` ERROR and still produces output.
* POL-D28 (S04), `models/intermediate/int_policy_valuation__valuation.sql`: the LEFT JOIN on `POLICY_ID` does not match a NULL key,
  whereas the SAS MERGE does.
* POL-D28/POL-D29 (S04), `models/staging/_staging.yml` (`not_null` + `unique` on POLICY_ID): under `dbt build` these staging test failures
  skip the marts, so the run produces no output. SAS accepts the missing and duplicate keys.
* POL-D39 (S03), `models/intermediate/int_policy_valuation__loss_ratio_means.sql`: `group by POLICY_TYPE` uses the raw code,
  not the `$POLTYPE.` formatted level, so the output has two rows instead of one `Unknown` row.
* Test-only (S02, S03, S15), `models/marts/_marts.yml`: the POLICY_TYPE/RISK_CATEGORY `not_null`/`accepted_values`/`relationships` tests
  fail on missing or unlisted codes, which SAS accepts and labels `Unknown`/`Unrated`. The data still matches, but `dbt build` reports failures.
* dbt `val_date` is an ISO var (`2024-01-31`), while the scenario params are DATE9., so the harness must convert them.
  S16/S17 fail in both SAS and dbt, so no divergence is recorded for them.
