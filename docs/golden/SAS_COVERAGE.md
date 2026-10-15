# SAS golden-dataset coverage (PROVISIONAL)

Branch coverage of the six SAS programs in `legacy/sas/programs`, from the per-program kits under `tests/golden/sas_<program>/`.
Decision points, seed counts and scenarios come from each kit's `COVERAGE.md` and `scenarios.json`. The seed is `legacy/sas/data/csv` at 31JAN2024 with default macro parameters.
A decision is exercised by the seed only if every reachable side is hit.

**Every expected output is provisional.** The `expected_provisional/` files were derived by hand from the SAS source (no SAS runtime was available), and `tools/sas_baseline.py` is a Python/DuckDB re-implementation used only as a second opinion. The outputs become golden once a licensed SAS host runs `tools/sas_golden/run_golden.sas` and the `golden/` diffs are reviewed (runbook: `tools/sas_golden/README.md`).

## Coverage by program

| Program | Decision points | Exercised by seed | Unexercised by seed | Scenarios |
|---|---:|---:|---:|---:|
| claims_processing | 31 | 10 | 21 | 15 |
| credit_risk_scoring | 35 | 6 | 29 | 10 |
| daily_transaction_processing | 37 | 9 | 28 | 19 |
| load_customer_accounts | 30 | 2 | 28 | 15 |
| monthly_regulatory_reporting | 30 | 2 | 28 | 18 |
| policy_valuation | 46 | 9 | 37 | 17 |
| **Total** | **209** | **38** | **171** | **94** |

## Suspected dbt divergences (39)

Places where the dbt ports (on the per-unit branches, not on this base branch) are expected to differ from SAS. Each line is copied verbatim from the kit report; the bracketed IDs are its decision IDs. Severity is not ranked.

- **claims_processing** [CLA-D02]: CLA-D02, models/staging/_sources.yml + stg_claims_processing__raw_ins_claims_feed.sql: feed source fixed to CLAIMS_FEED_20240131, so S11-S14 (15JAN/29FEB/31MAR/31DEC2024) read the wrong or a missing feed and stamp the wrong PROCESSING_DATE/ALERT_DATE; S11's decoy 31JAN2024 row would be processed
- **claims_processing** [CLA-D03/CLA-D01]: CLA-D03/CLA-D01, models/staging/stg_claims_processing__raw_ins_claims_feed.sql: no exist()/parmv abort guard; S08 (feed missing) errors instead of a no-op, and S15 (blank proc_date) still produces output
- **claims_processing** [CLA-D29]: CLA-D29, models/marts/CLAIMS_REGISTER.sql, CLAIMS_REVIEW_QUEUE.sql, FRAUD_ALERTS.sql: rebuilt as tables, not PROC APPEND; S07 prior STG_INS rows get dropped and S08 existing rows aren't kept
- **claims_processing** [CLA-D06]: CLA-D06, models/intermediate/int_claims_processing__claims_validation.sql: left join to ACTIVE policies with no first-row dedup (hash keeps the first duplicate key); S04 GC0401 fans out to HOME+AUTO rows and _marts.yml uniqueness tests would fail
- **claims_processing** [CLA-D08]: CLA-D08, models/intermediate/int_claims_processing__claims_validation.sql: a blank POLICY_ID loaded as NULL never joins; S03 GC0301 is lost (SAS hash matches blank to blank). This depends on how blank CSV cells are loaded
- **claims_processing** [CLA-D15]: CLA-D15, models/intermediate/int_claims_processing__fraud_check.sql: NULL CLAIMANT_ID never equals NULL; S03 GC0302 comes out LOW/APPR instead of HIGH/DENY with a FRAUD_ALERTS row. Same load-dependency caveat
- **credit_risk_scoring** [CRE-D35]: CRE-D35, models/intermediate/int_credit_risk_scoring__scored.sql, MODEL_ID = '{{ var("model_id") }}' keeps 'CRM-2023-Q4-v2'; SAS %parmv(_CASE=U) upcases model_id so SAS writes 'CRM-2023-Q4-V2' (all scenarios except S08/S10)
- **credit_risk_scoring** [CRE-D06]: CRE-D06, models/intermediate/int_credit_risk_scoring__score_input.sql, bureau_max_date filters SCORE_DATE <= date and joins on equality, so NULL SCORE_DATE rows never qualify; SAS treats missing <= date as true and missing = missing as a match (S02 A9020005 gets FICO 600 in SAS, NULL bureau in dbt)
- **credit_risk_scoring** [CRE-D07]: CRE-D07, models/intermediate/int_credit_risk_scoring__score_input.sql, left join a.CUSTOMER_ID = b.CUSTOMER_ID never matches when the key loads as NULL; SAS matches blank to blank (S02 A9020007); depends on whether Snowflake load keeps '' or NULL
- **credit_risk_scoring** [CRE-D27]: CRE-D27, models/marts/RISK_SCORES.sql, materialized as table (full rebuild) instead of PROC APPEND onto CURATED.RISK_SCORES, so prior history is dropped (S04)
- **credit_risk_scoring** [CRE-D28]: CRE-D28, models/marts/RISK_MIGRATION.sql, materialized as table instead of PROC APPEND onto CURATED.RISK_MIGRATION, so prior history is dropped (S04)
- **credit_risk_scoring** [CRE-D34]: CRE-D34, dbt_project.yml / models (no %parmv equivalent), blank model_id or score_date is not validated: blank score_date makes cast('' as date) fail rather than SAS ERROR path; blank model_id behaviour matches only by accident (S09/S10, low impact)
- **daily_transaction_processing** [DAI-D13]: DAI-D13 int_daily_transaction_processing__txn_validated.sql: TRANSACTION_TYPE IN (...) compares without blank padding, so 'DEP ' is rejected; SAS keeps it (S15)
- **daily_transaction_processing** [DAI-D15]: DAI-D15 int_daily_transaction_processing__txn_enriched.sql / int_daily_transaction_processing__txn_with_balance.sql: ACCOUNT_ID 'A9000131 ' neither joins to nor partitions with 'A9000131' (no rtrim); SAS treats them as the same value, so PRE/RUNNING_BALANCE and anomalies differ (S15)
- **daily_transaction_processing** [DAI-D34]: DAI-D34 models/marts/TXN_ANOMALIES.sql: the table holds current-run anomalies only; SAS PROC APPEND keeps the rows already in CURATED.TXN_ANOMALIES (S06)
- **daily_transaction_processing** [DAI-D33]: DAI-D33 models/marts/TXN_ANOMALIES.sql: with 0 new anomalies SAS skips the append and leaves the existing table unchanged; dbt rebuilds it empty (S07)
- **daily_transaction_processing** [DAI-D02]: DAI-D02 models/staging/_sources.yml + stg_daily_transaction_processing__txn_feed.sql: feed source is hardcoded to RAW_BANK_TXN_FEED_20240131; SAS reads TXN_FEED_<txn_date>, so non-default run dates read the wrong feed or fail (S16-S19)
- **daily_transaction_processing** [DAI-D03]: DAI-D03 stg_daily_transaction_processing__txn_feed.sql: a missing feed is a dbt run error; SAS logs ERROR, takes %goto ABORT and leaves all targets unchanged (S12)
- **daily_transaction_processing** [DAI-D01]: DAI-D01 int_daily_transaction_processing__txn_validated.sql / __txn_stats.sql: to_date('') errors on a blank txn_date; SAS (low confidence) aborts and leaves targets unchanged (S13)
- **daily_transaction_processing** [DAI-D35]: DAI-D35 stg_daily_transaction_processing__curated_daily_transactions.sql: absent history is a dbt error; SAS (low confidence) creates DAILY_TRANSACTIONS with 19 columns from TXN_WITH_BALANCE and writes nothing else (S11)
- **daily_transaction_processing** [DAI-D36]: DAI-D36 models/marts/DAILY_TRANSACTIONS.sql: dbt has no lock path, so a held lock does not stop the rebuild; SAS (low confidence) leaves DAILY_TRANSACTIONS unchanged when another session holds the lock (S14)
- **daily_transaction_processing** [DAI-D14/DAI-D37]: DAI-D14 / DAI-D37 models/marts/_marts.yml: data matches, but the unique tests on RUNNING_BALANCES/DAILY_TRANSACTIONS.TRANSACTION_ID fail on legitimate SAS outputs: snapshot fan-out (S03) and a TRANSACTION_ID already in history (S06)
- **load_customer_accounts** [LOA-D02/D04/D05]: LOA-D02/D04/D05 (S07-S10) models/intermediate/int_load_customer_accounts__acct_raw.sql: no region var/filter, so all regions are emitted instead of only d.REGION_CODE="&region" (incl. upcase of lowercase, invalid HQ still filtering, blank region keeping only missing REGION_CODE)
- **load_customer_accounts** [LOA-D07]: LOA-D07 (S01 A0111) int_load_customer_accounts__acct_raw.sql: ANSI inner join on CUSTOMER_ID drops rows with missing key; SAS PROC SQL matches missing to missing
- **load_customer_accounts** [LOA-D10]: LOA-D10 (S04) marts/CUST_ACCOUNTS_DAILY.sql + marts/ACCT_EXCEPTIONS.sql: no nobs_raw=0 %goto EXIT guard; tables rebuilt empty instead of leaving prior STG_BANK contents
- **load_customer_accounts** [LOA-D26b]: LOA-D26b (S03) marts/ACCT_EXCEPTIONS.sql: full-refresh table empties the target when there are 0 exceptions; SAS skips the INSERT and prior rows survive
- **load_customer_accounts** [LOA-D28b]: LOA-D28b (S05) marts/ACCT_EXCEPTIONS.sql: replaces instead of appending to prior STG_BANK.ACCT_EXCEPTIONS rows (SAS INSERT accumulates across runs)
- **load_customer_accounts** [LOA-D01b]: LOA-D01b (S15) dbt_project.yml var run_date: blank value makes ''::date fail the build; SAS logs errors and leaves targets unchanged (likely equivalent end state, low severity)
- **load_customer_accounts** [LOA-D27b]: LOA-D27b (S06) no %sendmail equivalent (side effect only; data matches)
- **load_customer_accounts** [LOA-D29]: LOA-D29 int_load_customer_accounts__acct_summary.sql: GROUP BY keeps NULL ACCOUNT_TYPE/REGION_CODE groups that PROC MEANS CLASS excludes (ephemeral, unreferenced; no target impact)
- **monthly_regulatory_reporting** [MON-D14/MON-D15/MON-D16]: MON-D14/MON-D15/MON-D16 | dbt/sas_monthly_regulatory_reporting/models/staging/stg_monthly_regulatory_reporting__loan_details.sql | cast(DAYS_PAST_DUE as number) has scale 0, so it rounds non-integer DPD: in S04, 29.5 becomes 30 (bucket '30-59') and 89.5 becomes 90 ('90-119'). SAS puts both in 'Unknown' because they fall in BETWEEN gaps.
- **monthly_regulatory_reporting** [MON-D22/MON-D23]: MON-D22/MON-D23 | same staging model, feeding models/marts/LLP_COVERAGE.sql | the rounded 89.5 -> 90 meets DPD >= 90, so S04 LLP_COVERAGE row CC gets NPL_BALANCE=2500 and NPL_COVERAGE_PCT=1.0. SAS gives 0 and 0.
- **monthly_regulatory_reporting** [MON-D04/MON-D13/MON-D19]: MON-D04/MON-D13/MON-D19 | models/staging/_staging.yml | the unique test on stg loan_details ACCOUNT_ID fails for S04's two LOAN_DETAILS rows on one account. SAS allows this and fans the join out (the SQL would fan out the same way), but under dbt build the test failure skips every downstream model.
- **monthly_regulatory_reporting** [MON-D07/MON-D10/MON-D18]: MON-D07/MON-D10/MON-D18 | models/marts/_marts.yml | not_null/accepted_values/relationships tests on ACCOUNT_TYPE, CUSTOMER_SEGMENT and REGION_CODE fail for S04's blank ACCOUNT_TYPE, lowercase 'mtg', blank CUSTOMER_SEGMENT and blank REGION_CODE. SAS writes these rows (ELSE arm with weight 1.00, blank groups sort first), but dbt build errors and skips CAPITAL_ADEQUACY, which is a child of MONTHLY_RWA.
- **policy_valuation** [POL-D02]: POL-D02 models/intermediate/int_policy_valuation__inforce.sql: lob 'home' (SAS %parmv upcases it), 'VL', 'AUTO HOME' and blank all raise a dbt compile error; SAS only logs a %parmv ERROR and still runs (S12-S15)
- **policy_valuation** [POL-D28]: POL-D28 models/intermediate/int_policy_valuation__valuation.sql: the LEFT JOIN on POLICY_ID never matches a NULL key; the SAS MERGE BY matches missing keys to missing keys, so claim/premium columns come out NULL (S04)
- **policy_valuation** [POL-D28/POL-D29]: POL-D28/POL-D29 models/staging/_staging.yml: the not_null+unique tests on stg policies POLICY_ID fail on missing/duplicate keys, so dbt build skips the marts; SAS outputs these rows (S04)
- **policy_valuation** [POL-D39]: POL-D39 models/intermediate/int_policy_valuation__loss_ratio_means.sql: groups by the raw POLICY_TYPE, but PROC MEANS CLASS groups by the $POLTYPE. formatted value, so unlisted codes ZZA/ZZB should collapse into one 'Unknown' row (S03)
- **policy_valuation** [POL-D36/D37/D38]: Test-only POL-D36/D37/D38 models/marts/_marts.yml: POLICY_TYPE/RISK_CATEGORY not_null/accepted_values/relationships tests fail on missing or unlisted codes that SAS labels Unknown/Unrated; the data matches but dbt build reports failures (S02, S03, S15)

## Suspected baseline divergences (28)

Places where `tools/sas_baseline.py` is believed to differ from SAS semantics. Each was found by running the baseline on scenario inputs through a throwaway runner (not committed). Lines are verbatim.

- **claims_processing** [CLA-D09]: CLA-D09, tools/sas_baseline.py claims_valid: drops claims whose policy EFFECTIVE_DATE is missing (SQL NULL comparison); SAS keeps them because missing sorts lowest (S02 GC0201, GC0202)
- **claims_processing** [CLA-D11/CLA-D22/CLA-D23]: CLA-D11/CLA-D22/CLA-D23, claims_valid + adjudication: drops claims with missing CLAIMED_AMOUNT; SAS keeps them as valid and approves them via `. <= x` being true (S02 GC0206, GC0208, GC0209)
- **claims_processing** [CLA-D08]: CLA-D08, claims_valid: blank POLICY_ID never matches a blank-keyed ACTIVE policy (S03 GC0301 missing)
- **claims_processing** [CLA-D15]: CLA-D15, fraud_check: blank CLAIMANT_ID never matches a blank-keyed fraud row (S03 GC0302 LOW/APPR instead of HIGH/DENY; FRAUD_ALERTS row missing)
- **claims_processing** [CLA-D06]: CLA-D06, claims_valid: duplicate ACTIVE POLICY_ID fans out to 2 rows; SAS hash keeps the first (S04 GC0401)
- **claims_processing** [CLA-D19]: CLA-D19, FRAUD_ALERTS: cast(FRAUD_SCORE as integer) gives 80 for 80.5 and 92 for 92.5; SAS put(,4.) rounds to 81 and 93 (S05)
- **claims_processing** [CLA-D29]: CLA-D29, write_outputs: replaces STG_INS tables instead of appending (S07 prior rows lost)
- **claims_processing** [CLA-D03]: CLA-D03, build: no exist() guard; fails with 'claims_feed_20240131 does not exist' instead of a no-op ABORT (S08)
- **claims_processing** [CLA-D04]: CLA-D04, sas_load_raw/build: zero-row feed CSV loads with INTEGER columns and claims_valid fails with a DATE binder error (S09); this is a loader typing limitation
- **credit_risk_scoring** [CRE-D35]: CRE-D35, tools/sas_baseline.py MODEL_ID = 'CRM-2023-Q4-v2' but SAS %parmv(_CASE=U) upcases to 'CRM-2023-Q4-V2' (S01-S04; only S01 difference)
- **credit_risk_scoring** [CRE-D05]: CRE-D05, latest_bureau uses row_number() and keeps one arbitrary row on a tied latest SCORE_DATE; SAS correlated-subquery join keeps all tied rows (S02 A9020001: 2 rows in SAS, 1 in baseline)
- **credit_risk_scoring** [CRE-D06]: CRE-D06, SCORE_DATE <= RUN_DATE excludes NULL dates; SAS keeps missing dates and matches missing = missing (S02 A9020005)
- **credit_risk_scoring** [CRE-D07]: CRE-D07, blank CUSTOMER_ID loads as NULL and never joins; SAS matches blank to blank (S02 A9020007)
- **credit_risk_scoring** [CRE-D27/CRE-D28]: CRE-D27/CRE-D28, baseline rebuilds RISK_SCORES/RISK_MIGRATION from WORK data and ignores existing CURATED history that PROC APPEND keeps (S04)
- **credit_risk_scoring** [CRE-D32/CRE-D33]: CRE-D32/CRE-D33, RUN_DATE and MODEL_ID are hard-coded, so S05-S10 (non-default params) cannot be cross-checked
- **daily_transaction_processing** [DAI-D05]: DAI-D05 tools/sas_baseline.py txn_validated: 'TRANSACTION_ID is not null' keeps a blank-only TRANSACTION_ID; SAS missing() rejects it (S01: one extra row in all three targets; the blank row is also first in its BY group, which shifts running balances)
- **daily_transaction_processing** [DAI-D22]: DAI-D22 tools/sas_baseline.py txn_with_balance: window ORDER BY TRANSACTION_DATE uses DuckDB's default NULLS LAST; SAS sorts a missing date first, so running balances differ (S01, S02)
- **daily_transaction_processing** [DAI-D13]: DAI-D13 tools/sas_baseline.py txn_validated: no trailing-blank padding in the type check, so 'DEP ' is rejected; SAS keeps it (S15)
- **daily_transaction_processing** [DAI-D15]: DAI-D15 tools/sas_baseline.py txn_with_balance: 'A9000131 ' does not join and forms its own partition (missing balance -> OVERDRAFT); SAS treats it as the same account (S15)
- **daily_transaction_processing** [DAI-D34/DAI-D33]: DAI-D34 / DAI-D33 tools/sas_baseline.py TXN_ANOMALIES: the existing CURATED.TXN_ANOMALIES is not modelled (no append onto existing rows, and the table is emitted empty instead of unchanged when there are 0 new anomalies) (S06, S07)
- **load_customer_accounts** [LOA-D08d]: LOA-D08d (S01 A0104) tools/sas_baseline.py acct_base: a.ACCOUNT_STATUS not in ('W','C') is NULL-unsafe and drops missing-status rows; SAS keeps them
- **load_customer_accounts** [LOA-D07b]: LOA-D07b (S01 A0111) tools/sas_baseline.py acct_base: ANSI join drops missing CUSTOMER_ID; SAS PROC SQL joins missing to missing
- **load_customer_accounts** [LOA-D10b]: LOA-D10b (S04) tools/sas_baseline.py: no %goto EXIT path; writes empty targets instead of leaving prior STG_BANK state
- **load_customer_accounts** [LOA-D26b/LOA-D28b]: LOA-D26b/LOA-D28b (S03, S05) tools/sas_baseline.py: ignores prior STG_BANK.ACCT_EXCEPTIONS (no skipped-INSERT retention, no INSERT append)
- **monthly_regulatory_reporting** (no decision): none (tools/sas_baseline.py run unmodified via a throwaway runner on S01-S12 matches expected_provisional for all 4 targets in parity_diff; it cannot run S13-S18 because RUN_DATE is hard-coded to 31JAN2024)
- **policy_valuation** [POL-D07]: POL-D07 tools/sas_baseline.py drops in-force policies with missing EFFECTIVE_DATE (NULL <= date); SAS keeps them because missing sorts lowest (S02)
- **policy_valuation** [POL-D38]: POL-D38 baseline LOSS_RATIO_SUMMARY keeps a NULL POLICY_TYPE group; PROC MEANS CLASS excludes missing class values (S02)
- **policy_valuation** [POL-D39]: POL-D39 baseline groups the summary by raw POLICY_TYPE (ZZA, ZZB as two rows); PROC MEANS groups by formatted value (one 'Unknown' level) (S03)
- **policy_valuation** [POL-D28]: POL-D28 baseline LEFT JOIN cannot match NULL POLICY_ID; SAS MERGE BY matches missing keys, so claim/premium columns and summary sums differ (S04)

