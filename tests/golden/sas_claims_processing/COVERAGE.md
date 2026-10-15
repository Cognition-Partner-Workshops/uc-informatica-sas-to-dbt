# claims_processing — decision coverage (PROVISIONAL)

Source: `legacy/sas/programs/claims_processing.sas` (line numbers), macros `%parmv`, `%nobs`, `%sendmail` (included), format `$CLMSTAT.` (`legacy/sas/formats/insurance_formats.sas`). `%lock` and `%export_xlsx` are not included by this program.

Seed = `legacy/sas/data/csv`, run date 31JAN2024, default params. Counts are rows taking each side at that decision's grain: macro-level decisions count 1 per run; D05/D06 count POLICIES rows; D07-D11 count feed rows reaching the test; D13-D19 and D21-D28 count FRAUD_CHECK rows (one per valid claim x matching fraud row); D29 counts target tables. A decision is exercised (Y) only if every side is hit by the seed.

Decision points: 31; exercised by seed: 10; not exercised: 21. D30 and D31 have a side that is unreachable by construction (see README) and stay N.

| ID | SAS line(s) | Condition | Seed rows per side | Exercised | Covering scenarios |
|---|---|---|---|---|---|
| CLA-D01 | 20 | `%parmv(proc_date,_req=1)` required-parameter check | nonblank=1; blank=0 | N | S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13, S14, S15 |
| CLA-D02 | 18, 23 | `proc_date` value (default `&CURR_DT`=31JAN2024 = month-end) drives feed name and PROCESSING_DATE/ALERT_DATE | default_31JAN2024=1; mid_month=0; leap_day=0; quarter_end=0; year_end=0 | N | S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13, S14 |
| CLA-D03 | 33-35, 224-228 | `exist(RAW_INS.CLAIMS_FEED_<yyyymmdd>)=0` -> `%goto ABORT` | exists=1; abort=0 | N | S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13, S14, S15 |
| CLA-D04 | 40-41 | `set RAW_INS.&feed_ds` has 0 vs >0 observations | nonempty=1; empty=0 | N | S01, S02, S03, S04, S05, S06, S07, S09, S10, S11, S12, S13, S14 |
| CLA-D05 | 47 | hash `dataset:` `where=(STATUS='ACTIVE')` (case-sensitive) per POLICIES row | loaded=244; excluded=76 | Y | S01, S02, S03, S04, S05, S06, S07, S09, S10, S11, S12, S13, S14 |
| CLA-D06 | 47-49 | hash load with duplicate POLICY_ID (default: first kept, later ignored) per loaded row | unique=244; duplicate_ignored=0 | N | S01, S02, S03, S04, S05, S06, S07, S09, S11, S12, S13, S14 |
| CLA-D07 | 57-63 | `h_pol.find()` `rc ne 0` -> CLAIMS_INVALID (per feed row) | hit=228; miss_inactive=17; miss_unknown=15 | Y | S01, S02, S03, S04, S05, S06, S07, S10, S11, S12, S13, S14 |
| CLA-D08 | 57 | blank POLICY_ID key lookup (SAS blank char = blank) | blank_hit=0; blank_miss=0 | N | S01, S03 |
| CLA-D09 | 66 | `LOSS_DATE < EFFECTIVE_DATE` (missing sorts lowest) | lt_true=26; eq_false=1; gt_false=201; loss_missing_true=0; eff_missing=0 | N | S01, S02, S03, S04, S05, S06, S07, S11, S12, S13, S14 |
| CLA-D10 | 66 | `LOSS_DATE > EXPIRATION_DATE` (missing sorts lowest) | gt_true=0; eq_false=0; lt_false=202; exp_missing_true=0; loss_missing_false=0 | N | S01, S02, S03, S04, S05, S06, S07, S11, S12, S13, S14 |
| CLA-D11 | 75 | `CLAIMED_AMOUNT > SUM_INSURED` (missing sorts lowest) | gt_true=12; eq_false=0; lt_false=190; ca_missing_false=0; si_missing_true=0 | N | S01, S02, S03, S04, S05, S06, S07, S11, S12, S13, S14 |
| CLA-D12 | 87 | `%nobs(WORK.CLAIMS_VALID)` >0 vs =0 | positive=1; zero=0 | N | S01, S02, S03, S04, S05, S06, S07, S09, S10, S11, S12, S13, S14 |
| CLA-D13 | 105-107 | left join FRAUD_INDICATORS on POLICY_ID+CLAIMANT_ID: match vs no match (per valid claim) | match=76; nomatch=114 | Y | S01, S02, S03, S04, S05, S06, S07, S11, S12, S13, S14 |
| CLA-D14 | 105-107 | join cardinality per matched claim: one vs several fraud rows (fan-out) | single=76; multi=0 | N | S01, S02, S03, S04, S05, S06, S07, S11, S12, S13, S14 |
| CLA-D15 | 106-107 | blank CLAIMANT_ID in join (PROC SQL blank = blank) | blank_match=0; blank_nomatch=0 | N | S01, S03 |
| CLA-D16 | 99-103 | CASE FRAUD_SCORE >=80 HIGH / >=50 MEDIUM / else LOW (missing -> LOW) | gt80_high=18; eq80_high=1; 50to80_medium=23; eq50_medium=1; lt50_low=33; missing_low=114 | Y | S01, S02, S03, S04, S05, S06, S07, S11, S12, S13, S14 |
| CLA-D17 | 114 | `where FRAUD_RISK='HIGH'` into WORK.FRAUD_ALERTS | kept=19; dropped=171 | Y | S01, S02, S03, S04, S05, S06, S07, S11, S12, S13, S14 |
| CLA-D18 | 115-117 | `catx('; ', ..., INDICATOR_FLAGS)` drops blank flags | flags_present=19; flags_blank=0 | N | S01, S03, S04, S05, S07, S11, S12, S13, S14 |
| CLA-D19 | 116 | `put(FRAUD_SCORE,4.)` rounding of non-integer score | integer=19; fractional=0 | N | S01, S03, S04, S05, S07, S11, S12, S13, S14 |
| CLA-D20 | 122, 204-214 | `&nobs_fraud > 0` -> PROC APPEND FRAUD_ALERTS + `%sendmail`; else skipped | positive_append_sendmail=1; zero_skip=0 | N | S01, S02, S03, S04, S05, S06, S07, S09, S10, S11, S12, S13, S14 |
| CLA-D21 | 136-141 | `FRAUD_RISK='HIGH'` -> DENY, APPROVED_AMOUNT=0, MANUAL_REVIEW | true=19; false=171 | Y | S01, S02, S03, S04, S05, S06, S07, S11, S12, S13, S14 |
| CLA-D22 | 145-155 | rule 2: LOW and CLAIMED_AMOUNT<=5000 and POLICY_TYPE in (AUTO,HOME,RENT) -> APPR | taken=42; taken_eq5000=0; taken_ca_missing=0; fail_medium=24; fail_amount=105; fail_type=0 | N | S01, S02, S03, S04, S05, S06, S07, S11, S12, S13, S14 |
| CLA-D23 | 157-167 | rule 3: LOW and CLAIMED_AMOUNT<=SUM_INSURED*0.25 and <=50000 -> APPR | taken=47; taken_eq25pct=0; taken_eq50000=0; taken_ca_missing=0; fail_medium=24; fail_gt25pct=51; fail_gt50000=7 | N | S01, S02, S04, S05, S06, S12, S13, S14 |
| CLA-D24 | 151, 163 | `max(0, CLAIMED_AMOUNT-DEDUCTIBLE)` (missing arg ignored by max) | positive=76; clipped_zero=13; arg_missing_zero=0 | N | S01, S02, S03, S04, S05, S06, S07, S11, S12, S13, S14 |
| CLA-D25 | 171 | PEND reason `ifc(FRAUD_RISK='MEDIUM',...)` | present=24; absent=58 | Y | S01, S02, S05, S06 |
| CLA-D26 | 172 | PEND reason `ifc(CLAIMED_AMOUNT>50000,'Large claim','')` | present=25; absent=57 | Y | S01, S02, S05, S06 |
| CLA-D27 | 173 | PEND reason `ifc(CLAIMED_AMOUNT>SUM_INSURED*0.25,...)` | present=57; absent=25 | Y | S01, S02, S05, S06 |
| CLA-D28 | 136-175 | final ADJUDICATION_RESULT / output dataset | APPR=89; DENY=19; PEND=82 | Y | S01, S02, S03, S04, S05, S06, S07, S11, S12, S13, S14 |
| CLA-D29 | 194-207 | PROC APPEND to STG_INS base: base absent (created) vs existing (rows added) | base_absent=3; base_exists=0 | N | S01, S02, S03, S04, S05, S06, S07, S09, S10, S11, S12, S13, S14 |
| CLA-D30 | 170-173 | `catx('; ', '', '', '')` all PEND reasons blank -> missing ADJUDICATION_REASON | nonblank=82; all_blank (unreachable)=0 | N | S01, S02, S05, S06 |
| CLA-D31 | 189-191; insurance_formats.sas | `$CLMSTAT.` mapped label vs `OTHER='Unknown'` | mapped=190; other (unreachable)=0 | N | S01, S02, S03, S04, S05, S06, S07, S11, S12, S13, S14 |

Scenario key: S01 = `S01_core_rules`; S02 = `S02_missing_values`; S03 = `S03_blank_keys`; S04 = `S04_duplicate_keys`; S05 = `S05_fractional_scores`; S06 = `S06_no_high_fraud`; S07 = `S07_prior_state`; S08 = `S08_feed_missing_abort`; S09 = `S09_empty_feed`; S10 = `S10_no_active_policies`; S11 = `S11_mid_month`; S12 = `S12_leap_day`; S13 = `S13_quarter_end`; S14 = `S14_year_end`; S15 = `S15_blank_proc_date`
