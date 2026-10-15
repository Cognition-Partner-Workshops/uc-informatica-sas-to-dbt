# PII masking checks

This dbt project loads the PII classification seeds and tests that classified columns carry the expected `PII_CATEGORY` tag and a tag-based masking policy. Run `scripts/build_classification.py`, then `scripts/apply_policy.py`, then `dbt seed` and `dbt test`. Before tearing down the demo objects, run `sql/99_rollback.sql`.

Set `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_HOST`, `SF_DEMO_USER`, `SF_DEMO_PASSWORD`, `SF_DEMO_ROLE`, `SF_DEMO_WAREHOUSE`, and `SF_DEMO_DATABASE` in the environment. Use the demo run role and warehouse.

A dbt rebuild of a tagged table using `CREATE OR REPLACE` drops its column tags. The classification test will fail until `sql/04_apply_pii_tags.sql` is re-applied.
