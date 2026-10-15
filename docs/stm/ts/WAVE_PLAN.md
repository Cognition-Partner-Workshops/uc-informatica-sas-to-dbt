# Wave plan, run SF_20261015_DS

This is the wave plan from the Act 0 legacy-estate inventory, which was delivered as a session attachment and never committed. It is recorded here so the status of each wave can be tracked. Waves 1 to 3 are copied unchanged; wave 4 is updated on 2026-10-15 now that the masking policy exists.

1. **Wave 1 (fastest honest result):** `load_customer_accounts` to dbt, checked by key against the baseline (CUST_ACCOUNTS_DAILY 466 rows, ACCT_EXCEPTIONS 32 rows). Alongside it, scai converts `m_demo_mapping3` with no hand edits and is checked against DEMO_TARGET2 and DEMO_TARGET21 (3 rows each). Both read sources that are already loaded and compare to baselines that already exist.
2. **Wave 2:** `monthly_regulatory_reporting` and `credit_risk_scoring`, which depend on Wave 1's account snapshot. Also `m_demo_mapping2` and `m_demo_mapping1` (scai output plus the hand fixes above).
3. **Wave 3:** `daily_transaction_processing` (largest volume, stateful logic). In parallel, the insurance track: `policy_valuation`, then `claims_processing`. Insurance does not depend on banking.
4. **Wave 4: ts-informatica-powercenter. No longer blocked on a masking policy; still blocked on source data and a baseline.** Before any model, it needs:
   - ~~a PII masking policy~~ **Done 2026-10-15.** The tag `DBT_SF_20261015_DS.PII_CATEGORY` and five per-type masking policies (`PII_MASK_VARCHAR`, `_NUMBER`, `_FLOAT`, `_DATE`, `_TIMESTAMP_NTZ`) are live. Only role `SF_20261015_DS_DBT` sees clear values. The tag is on all 127 personal-data columns found in `BASELINE_SF_20261015_DS` (45), `SOURCE_SF_20261015_DS` (37), `DBT_SF_20261015_DS` (23), and `SCAI_SF_20261015_DS` (22). See [`dbt/pii_masking/`](../../../dbt/pii_masking/) and its [classification](../../../dbt/pii_masking/CLASSIFICATION.md).
     A PowerCenter table landed later is masked by adding its columns to the classification and re-running `sql/04_apply_pii_tags.sql`. No new policy is needed: the tag picks the policy by data type. `dbt test` in `dbt/pii_masking` fails until every classified column carries the tag.
     Any `CREATE OR REPLACE` of a tagged table (`load_baseline.py`, or a migrated unit's `dbt build` into `DBT_`/`SCAI_`) drops its column tags and unmasks those columns. After each such build, run `dbt seed && dbt run-operation apply_pii_tags && dbt test` from `dbt/pii_masking`; the dbt test fails while any tag is missing. An `on-run-end` hook in each migrated unit could call the operation, but that is not done in this PR. This was observed once on 2026-10-15 at about 17:15 UTC.
   - source landing for Oracle, VSAM and PWX (open)
   - a baseline to compare against (open)

   The 3 SQL bodies missing from the repo also need to be found. Start with a scai assessment of all 11 exports, then pilot COMPTIME, Pay_Calendar and EHRP2BIIS_UPDATE. Do CPM and LES last. Fold the scripts into orchestration.
   The Act 0 count of 567 PowerCenter personal-data fields came from column names in the XML exports. None of those tables are in Snowflake yet, so none of them are in the 127 above.
