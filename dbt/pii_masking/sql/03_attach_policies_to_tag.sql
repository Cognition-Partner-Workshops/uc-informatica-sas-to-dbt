-- Tag-based masking: a column tagged PII_CATEGORY gets the policy that matches its data type.
-- Run once as SF_20261015_DS_DBT (APPLY MASKING POLICY on the account). Re-running fails with "already attached";
-- run 99_rollback.sql first to start over.
alter tag DEVIN_MIGRATION_DEMO.DBT_SF_20261015_DS.PII_CATEGORY set
  masking policy DEVIN_MIGRATION_DEMO.DBT_SF_20261015_DS.PII_MASK_VARCHAR,
  masking policy DEVIN_MIGRATION_DEMO.DBT_SF_20261015_DS.PII_MASK_NUMBER,
  masking policy DEVIN_MIGRATION_DEMO.DBT_SF_20261015_DS.PII_MASK_FLOAT,
  masking policy DEVIN_MIGRATION_DEMO.DBT_SF_20261015_DS.PII_MASK_DATE,
  masking policy DEVIN_MIGRATION_DEMO.DBT_SF_20261015_DS.PII_MASK_TIMESTAMP_NTZ;
