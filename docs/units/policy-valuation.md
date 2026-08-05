# Unit Verification Packet: `policy_valuation.sas`

## 1. Unit Overview

`legacy/sas/programs/policy_valuation.sas` — **Monthly Policy Book Valuation**. It calculates in-force policy metrics, premium adequacy, loss ratios, and reserve estimates for the insurance book of business. Scheduled monthly (5th business day) via Control-M job `INS_MONTHLY_01`, wrapped in macro `%policy_valuation(val_date=&CURR_DT, lob=ALL)` with `lob` validated against `ALL AUTO HOME WL TL UL HLTH`.

Processing steps in the legacy program:

1. **In-force extraction** (`WORK.INFORCE`): from `RAW_INS.POLICIES` where `STATUS='ACTIVE'` and the valuation date falls within `[EFFECTIVE_DATE, EXPIRATION_DATE]`; derives `POLICY_AGE_MONTHS`, `MONTHS_TO_EXPIRY` (via `intck('month', ...)`), `RENEWAL_DUE_FLAG` (expiry within 3 months via `intnx`), and pro-rata `YTD_EARNED_PREMIUM`.
2. **Claims experience** (`WORK.CLAIMS_EXP`): 12-month window over `RAW_INS.CLAIMS` grouped by `POLICY_ID`; claim counts, incurred/paid/reserved sums, `OPEN_RESERVES` (status in `OPEN/INV/ADJ/PEND`), `DENIED_CLAIMS`.
3. **Premium collections** (`WORK.PREMIUM_COLL`): year-to-date window over `RAW_INS.PREMIUMS` grouped by `POLICY_ID`; collected/returned premium, last payment date, late-payment count.
4. **Valuation merge** (`STG_INS.POLICY_VALUATION`): `MERGE ... BY POLICY_ID` keeping in-force rows only (`if a`); derives `LOSS_RATIO`, `COMBINED_RATIO` (loss + 0.30 expense load), `PREMIUM_ADEQUATE`, `IBNR_ESTIMATE` (`max(0, earned*0.15 - paid)`), `TOTAL_RESERVE`, `VALUATION_DATE`; applies `$POLTYPE.`/`$RISKCAT.` display formats.
5. **LOB summary** (`REPORTS.LOSS_RATIO_SUMMARY`): `PROC MEANS NWAY CLASS POLICY_TYPE` sums, then a second DATA step adds `AGG_LOSS_RATIO` / `AGG_COMBINED_RATIO` when `TOTAL_EARNED > 0`.

**Sources:** `RAW_INS.POLICIES`, `RAW_INS.CLAIMS`, `RAW_INS.PREMIUMS`. (`TERA_DW.ACTUARIAL_TABLES` is named in the header comment but never read in the code.)

**Targets:** `STG_INS.POLICY_VALUATION`, `REPORTS.LOSS_RATIO_SUMMARY`. (`REPORTS.RESERVE_ADEQUACY` is listed in the header but never created anywhere in the program — it is not a real output.)

## 2. STM Excerpt (from `docs/stm/sas_stm.md`)

**Macro:** `%policy_valuation` — parameters: `val_date=&CURR_DT`, `lob=ALL`

**Inputs:** `RAW_INS.CLAIMS`, `RAW_INS.POLICIES`, `RAW_INS.PREMIUMS`, `STG_INS.POLICY_VALUATION`
**Persistent outputs:** `REPORTS.LOSS_RATIO_SUMMARY`, `STG_INS.POLICY_VALUATION`

| Output Dataset | Column | Derivation | Source(s) |
|---|---|---|---|
| WORK.INFORCE | *(step)* | where p.STATUS = 'ACTIVE' and p.EFFECTIVE_DATE <= "&val_date"d and p.EXPIRATION_DATE >= "&val_date"d %if &lob ne ALL %then %do | RAW_INS.POLICIES p |
| WORK.INFORCE | POLICY_ID | `p.POLICY_ID` | RAW_INS.POLICIES p |
| WORK.INFORCE | CUSTOMER_ID | `p.CUSTOMER_ID` | RAW_INS.POLICIES p |
| WORK.INFORCE | POLICY_TYPE | `p.POLICY_TYPE` | RAW_INS.POLICIES p |
| WORK.INFORCE | EFFECTIVE_DATE | `p.EFFECTIVE_DATE` | RAW_INS.POLICIES p |
| WORK.INFORCE | EXPIRATION_DATE | `p.EXPIRATION_DATE` | RAW_INS.POLICIES p |
| WORK.INFORCE | ANNUAL_PREMIUM | `p.ANNUAL_PREMIUM` | RAW_INS.POLICIES p |
| WORK.INFORCE | SUM_INSURED | `p.SUM_INSURED` | RAW_INS.POLICIES p |
| WORK.INFORCE | DEDUCTIBLE | `p.DEDUCTIBLE` | RAW_INS.POLICIES p |
| WORK.INFORCE | RISK_CATEGORY | `p.RISK_CATEGORY` | RAW_INS.POLICIES p |
| WORK.INFORCE | UNDERWRITING_CLASS | `p.UNDERWRITING_CLASS` | RAW_INS.POLICIES p |
| WORK.INFORCE | AGENT_ID | `p.AGENT_ID` | RAW_INS.POLICIES p |
| WORK.INFORCE | BRANCH_CODE | `p.BRANCH_CODE` | RAW_INS.POLICIES p |
| WORK.INFORCE | POLICY_AGE_MONTHS | `intck('month', p.EFFECTIVE_DATE, "&val_date"d)` | RAW_INS.POLICIES p |
| WORK.INFORCE | MONTHS_TO_EXPIRY | `intck('month', "&val_date"d, p.EXPIRATION_DATE)` | RAW_INS.POLICIES p |
| WORK.INFORCE | RENEWAL_DUE_FLAG | `case when p.EXPIRATION_DATE <= intnx('month', "&val_date"d, 3) then 'Y' else 'N' end` | RAW_INS.POLICIES p |
| WORK.INFORCE | YTD_EARNED_PREMIUM | `p.ANNUAL_PREMIUM / 12 * min(12, intck('month', max(p.EFFECTIVE_DATE, intnx('year', "&val_date"d, 0, 'B')), min("&val_date"d, p.EXPIRATION_DATE)))` | RAW_INS.POLICIES p |
| WORK.CLAIMS_EXP | *(step)* | where c.LOSS_DATE >= intnx('month', "&val_date"d, -12) and c.LOSS_DATE <= "&val_date"d; group by c.POLICY_ID | RAW_INS.CLAIMS c |
| WORK.CLAIMS_EXP | POLICY_ID | `c.POLICY_ID` | RAW_INS.CLAIMS c |
| WORK.CLAIMS_EXP | NUM_CLAIMS | `count(distinct c.CLAIM_ID)` | RAW_INS.CLAIMS c |
| WORK.CLAIMS_EXP | TOTAL_INCURRED | `sum(c.INCURRED_AMOUNT)` | RAW_INS.CLAIMS c |
| WORK.CLAIMS_EXP | TOTAL_PAID | `sum(c.PAID_AMOUNT)` | RAW_INS.CLAIMS c |
| WORK.CLAIMS_EXP | TOTAL_RESERVED | `sum(c.RESERVED_AMOUNT)` | RAW_INS.CLAIMS c |
| WORK.CLAIMS_EXP | LAST_CLAIM_DATE | `max(c.LOSS_DATE)` | RAW_INS.CLAIMS c |
| WORK.CLAIMS_EXP | OPEN_RESERVES | `sum(case when c.CLAIM_STATUS in ('OPEN','INV','ADJ','PEND') then c.RESERVED_AMOUNT else 0 end)` | RAW_INS.CLAIMS c |
| WORK.CLAIMS_EXP | DENIED_CLAIMS | `sum(case when c.CLAIM_STATUS = 'DENY' then 1 else 0 end)` | RAW_INS.CLAIMS c |
| WORK.PREMIUM_COLL | *(step)* | where PAYMENT_DATE >= intnx('year', "&val_date"d, 0, 'B') and PAYMENT_DATE <= "&val_date"d; group by POLICY_ID | RAW_INS.PREMIUMS where |
| WORK.PREMIUM_COLL | POLICY_ID | `POLICY_ID` | RAW_INS.PREMIUMS where |
| WORK.PREMIUM_COLL | COLLECTED_PREMIUM | `sum(PREMIUM_AMOUNT)` | RAW_INS.PREMIUMS where |
| WORK.PREMIUM_COLL | RETURNED_PREMIUM | `sum(case when PAYMENT_STATUS = 'RETURNED' then PREMIUM_AMOUNT else 0 end)` | RAW_INS.PREMIUMS where |
| WORK.PREMIUM_COLL | LAST_PAYMENT_DATE | `max(PAYMENT_DATE)` | RAW_INS.PREMIUMS where |
| WORK.PREMIUM_COLL | LATE_PAYMENTS | `count(case when PAYMENT_STATUS = 'LATE' then 1 end)` | RAW_INS.PREMIUMS where |
| STG_INS.POLICY_VALUATION | *(step)* | MERGE by POLICY_ID | WORK.INFORCE, WORK.CLAIMS_EXP, WORK.PREMIUM_COLL |
| STG_INS.POLICY_VALUATION | LOSS_RATIO | if `YTD_EARNED_PREMIUM > 0` then `coalesce(TOTAL_INCURRED, 0) / YTD_EARNED_PREMIUM` | WORK.INFORCE, WORK.CLAIMS_EXP, WORK.PREMIUM_COLL |
| STG_INS.POLICY_VALUATION | LOSS_RATIO | if `NOT (YTD_EARNED_PREMIUM > 0)` then `.` | WORK.INFORCE, WORK.CLAIMS_EXP, WORK.PREMIUM_COLL |
| STG_INS.POLICY_VALUATION | COMBINED_RATIO | if `YTD_EARNED_PREMIUM > 0` then `LOSS_RATIO + 0.30` | WORK.INFORCE, WORK.CLAIMS_EXP, WORK.PREMIUM_COLL |
| STG_INS.POLICY_VALUATION | COMBINED_RATIO | if `NOT (YTD_EARNED_PREMIUM > 0)` then `.` | WORK.INFORCE, WORK.CLAIMS_EXP, WORK.PREMIUM_COLL |
| STG_INS.POLICY_VALUATION | PREMIUM_ADEQUATE | if `COMBINED_RATIO = .` then `'N'` | WORK.INFORCE, WORK.CLAIMS_EXP, WORK.PREMIUM_COLL |
| STG_INS.POLICY_VALUATION | PREMIUM_ADEQUATE | if `ELSE COMBINED_RATIO > 1.0` then `'N'` | WORK.INFORCE, WORK.CLAIMS_EXP, WORK.PREMIUM_COLL |
| STG_INS.POLICY_VALUATION | PREMIUM_ADEQUATE | if `NOT (ELSE COMBINED_RATIO > 1.0)` then `'Y'` | WORK.INFORCE, WORK.CLAIMS_EXP, WORK.PREMIUM_COLL |
| STG_INS.POLICY_VALUATION | IBNR_ESTIMATE | `max(0, YTD_EARNED_PREMIUM * 0.15 - coalesce(TOTAL_PAID, 0))` | WORK.INFORCE, WORK.CLAIMS_EXP, WORK.PREMIUM_COLL |
| STG_INS.POLICY_VALUATION | TOTAL_RESERVE | `coalesce(OPEN_RESERVES, 0) + IBNR_ESTIMATE` | WORK.INFORCE, WORK.CLAIMS_EXP, WORK.PREMIUM_COLL |
| STG_INS.POLICY_VALUATION | VALUATION_DATE | `"&val_date"d` | WORK.INFORCE, WORK.CLAIMS_EXP, WORK.PREMIUM_COLL |
| STG_INS.POLICY_VALUATION | POLICY_TYPE | display format `$POLTYPE.` | WORK.INFORCE, WORK.CLAIMS_EXP, WORK.PREMIUM_COLL |
| STG_INS.POLICY_VALUATION | RISK_CATEGORY | display format `$RISKCAT.` | WORK.INFORCE, WORK.CLAIMS_EXP, WORK.PREMIUM_COLL |
| STG_INS.POLICY_VALUATION | LOSS_RATIO | display format `percent8.2` | WORK.INFORCE, WORK.CLAIMS_EXP, WORK.PREMIUM_COLL |
| STG_INS.POLICY_VALUATION | COMBINED_RATIO | display format `percent8.2` | WORK.INFORCE, WORK.CLAIMS_EXP, WORK.PREMIUM_COLL |
| STG_INS.POLICY_VALUATION | IBNR_ESTIMATE | display format `dollar18.2` | WORK.INFORCE, WORK.CLAIMS_EXP, WORK.PREMIUM_COLL |
| STG_INS.POLICY_VALUATION | TOTAL_RESERVE | display format `dollar18.2` | WORK.INFORCE, WORK.CLAIMS_EXP, WORK.PREMIUM_COLL |
| STG_INS.POLICY_VALUATION | VALUATION_DATE | display format `date9.` | WORK.INFORCE, WORK.CLAIMS_EXP, WORK.PREMIUM_COLL |
| REPORTS.LOSS_RATIO_SUMMARY | *(aggregate)* | PROC MEANS NWAY CLASS POLICY_TYPE; N_POLICIES=n(first var), TOTAL_EARNED=sum(YTD_EARNED_PREMIUM), TOTAL_INCURRED=sum(TOTAL_INCURRED), TOTAL_PAID=sum(TOTAL_PAID), TOTAL_RESERVES=sum(TOTAL_RESERVE), TOTAL_IBNR=sum(IBNR_ESTIMATE) | STG_INS.POLICY_VALUATION |
| REPORTS.LOSS_RATIO_SUMMARY | AGG_LOSS_RATIO | if `TOTAL_EARNED > 0` then `TOTAL_INCURRED / TOTAL_EARNED` | REPORTS.LOSS_RATIO_SUMMARY |
| REPORTS.LOSS_RATIO_SUMMARY | AGG_COMBINED_RATIO | if `TOTAL_EARNED > 0` then `AGG_LOSS_RATIO + 0.30` | REPORTS.LOSS_RATIO_SUMMARY |
| REPORTS.LOSS_RATIO_SUMMARY | AGG_LOSS_RATIO | display format `percent8.2` | REPORTS.LOSS_RATIO_SUMMARY |
| REPORTS.LOSS_RATIO_SUMMARY | AGG_COMBINED_RATIO | display format `percent8.2` | REPORTS.LOSS_RATIO_SUMMARY |
| REPORTS.LOSS_RATIO_SUMMARY | TOTAL_EARNED | display format `dollar20.2` | REPORTS.LOSS_RATIO_SUMMARY |
| REPORTS.LOSS_RATIO_SUMMARY | TOTAL_INCURRED | display format `dollar20.2` | REPORTS.LOSS_RATIO_SUMMARY |
| REPORTS.LOSS_RATIO_SUMMARY | TOTAL_PAID | display format `dollar20.2` | REPORTS.LOSS_RATIO_SUMMARY |
| REPORTS.LOSS_RATIO_SUMMARY | TOTAL_RESERVES | display format `dollar20.2` | REPORTS.LOSS_RATIO_SUMMARY |
| REPORTS.LOSS_RATIO_SUMMARY | TOTAL_IBNR | display format `dollar20.2` | REPORTS.LOSS_RATIO_SUMMARY |

**Notes / ambiguities (from the STM):**
- YTD_EARNED_PREMIUM uses `intck('month', max(EFFECTIVE_DATE, 01JAN2024), min(31JAN2024, EXPIRATION_DATE))` — month-boundary counting makes this 0 for every policy at the January valuation date, so YTD_EARNED_PREMIUM = 0, LOSS_RATIO and COMBINED_RATIO are missing, PREMIUM_ADEQUATE = 'N' for all rows and IBNR_ESTIMATE = 0. This is the faithful legacy semantics for run date 31JAN2024.
- REPORTS.RESERVE_ADEQUACY is listed in the program header but never created anywhere in the code; it is not a real output.
- The MERGE is 1:1 by POLICY_ID (all inputs are aggregated or unique per policy); `if a` keeps in-force policies only.
- AGG_LOSS_RATIO / AGG_COMBINED_RATIO stay missing because TOTAL_EARNED sums to 0 (the `if TOTAL_EARNED > 0` guard fails).
- $POLTYPE./$RISKCAT. are display formats; migrated as explicit *_DESC columns via seed lookups.

## 3. Verification Evidence

Run on branch `devin/sas-track` (business date pinned to 31JAN2024). Commands executed from the repo root:

```
python3 tools/sas_lineage.py      # regenerated docs/stm/sas_stm.{json,md}
python3 tools/sas_baseline.py     # baseline/sas/* (POLICY_VALUATION: 166 rows, LOSS_RATIO_SUMMARY: 8 rows)
python3 tools/sas_load_raw.py     # raw seed data -> dbt/sas/dev.duckdb
(cd dbt/sas && dbt build --profiles-dir . --no-partial-parse)
python3 tools/parity_diff.py --baseline baseline/sas --actual dbt/sas/dev.duckdb \
  --schema main --keys tools/keys/sas_keys.json --report /tmp/parity.md
```

### dbt build result

```
Finished running 8 seeds, 17 table models, 67 data tests, 25 view models in 0 hours 0 minutes and 2.57 seconds (2.57s).

Completed successfully

Done. PASS=117 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=117
```

### Parity report — this unit's targets (copied from /tmp/parity.md)

```
## LOSS_RATIO_SUMMARY
- rows: baseline=8 actual=8
- columns compared: 9
- result: **MATCH** (all values within tolerance)

## POLICY_VALUATION
- rows: baseline=166 actual=166
- columns compared: 35
- result: **MATCH** (all values within tolerance)
```

Overall report footer: `**Overall: PARITY VERIFIED**`

**Parity exit code: 0**

| Target | Baseline rows | dbt rows | Result |
|---|---|---|---|
| POLICY_VALUATION | 166 | 166 | MATCH (35 columns within 1e-6 tolerance) |
| LOSS_RATIO_SUMMARY | 8 | 8 | MATCH (9 columns within 1e-6 tolerance) |

dbt models for this unit: `int_policy_inforce`, `int_claims_experience`, `int_premium_collections`, `policy_valuation`, `loss_ratio_summary` (plus staging models `stg_policies`, `stg_claims`, `stg_premiums` and format seeds `fmt_policy_type`, `fmt_risk_category`).

## 4. Snowflake Notes

Items a Snowflake deployment should review in this unit's SQL:

- **`datediff('month', ...)` month-boundary semantics.** The models rely on DuckDB's `datediff('month', a, b)` matching SAS `intck('month', a, b)` (calendar-month boundaries crossed). Snowflake's `DATEDIFF(month, ...)` also counts month boundaries, so behavior matches — but this is the load-bearing assumption behind `POLICY_AGE_MONTHS`, `MONTHS_TO_EXPIRY`, and especially `YTD_EARNED_PREMIUM` (which is 0 at the January run date). Regression-test these columns first on Snowflake.
- **Pinned date literals via dbt vars.** SAS `intnx` results are precomputed as project vars (`run_date`, `year_start` = `intnx('year', run_date, 0, 'B')`, `renewal_horizon_end` = `intnx('month', run_date, 3)` with BEGINNING alignment). A production deployment should derive these from the actual run date (e.g. `DATE_TRUNC('year', ...)`, `DATEADD`/`DATE_TRUNC` for the 3-month renewal horizon) instead of hard-coded vars.
- **`greatest(...)`/`least(...)` NULL handling.** `IBNR_ESTIMATE` uses `greatest(0, ...)` and `YTD_EARNED_PREMIUM` uses `least(12, ...)`/`greatest`/`least` on dates. Snowflake's `GREATEST`/`LEAST` return NULL if any argument is NULL (unlike some engines); inputs here are guaranteed non-NULL by the in-force filter, but verify if source nullability changes (or use `GREATEST_IGNORE_NULLS`).
- **Division semantics.** `LOSS_RATIO`/`AGG_LOSS_RATIO` divide by earned premium guarded by `> 0` CASE predicates, so no divide-by-zero occurs; NULL (SAS missing `.`) is produced by the CASE with no ELSE. This ports cleanly, but keep the guard if refactoring.
- **`count(case when ... then 1 end)` for `LATE_PAYMENTS`** counts non-NULL expressions — identical in Snowflake; do not rewrite as `SUM` without preserving NULL-when-no-match behavior against COUNT's 0-when-no-match.
- **Display formats.** SAS `percent8.2`/`dollar18.2`/`date9.` formats are presentation-only and intentionally not ported; `$POLTYPE.`/`$RISKCAT.` recodes are materialized as `POLICY_TYPE_DESC`/`RISK_CATEGORY_DESC` via seed lookups (`fmt_policy_type`, `fmt_risk_category`) with `coalesce` defaults ('Unknown'/'Unrated') matching the formats' OTHER buckets.
- **1:1 merge assumption.** The SAS `MERGE ... BY POLICY_ID; if a;` is ported as LEFT JOINs from `int_policy_inforce`. This is only equivalent because claims/premium inputs are pre-aggregated to one row per `POLICY_ID`; a uniqueness test on those intermediates is the guard to keep in Snowflake.
- **`VALUATION_DATE` cast.** `cast('<run_date>' as date)` uses an ISO-8601 literal — Snowflake-compatible regardless of session `DATE_INPUT_FORMAT`, but keep literals ISO.
