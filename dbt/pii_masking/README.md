# PII masking checks

This dbt project loads the PII classification seeds and tests that classified columns carry the expected `PII_CATEGORY` tag and a tag-based masking policy. Run `scripts/build_classification.py`, then `scripts/apply_policy.py`, then `dbt seed` and `dbt test`. Before tearing down the demo objects, run `sql/99_rollback.sql`.

Set `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_HOST`, `SF_DEMO_USER`, `SF_DEMO_PASSWORD`, `SF_DEMO_ROLE`, `SF_DEMO_WAREHOUSE`, and `SF_DEMO_DATABASE` in the environment. Use the demo run role and warehouse.

Any `CREATE OR REPLACE` of a tagged table (`load_baseline.py`, or a migrated unit's `dbt build` into `DBT_`/`SCAI_`) drops its column tags and unmasks those columns. After each such build, run `dbt seed && dbt run-operation apply_pii_tags && dbt test` from this directory. The dbt test fails while any tag is missing. An `on-run-end` hook in each migrated unit could call the operation, but that is not done in this PR. This was observed once on 2026-10-15 at about 17:15 UTC.
