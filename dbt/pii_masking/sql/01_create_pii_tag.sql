-- PII tag for run SF_20261015_DS. Run as SF_20261015_DS_DBT (CREATE TAG on the run's schemas); never ACCOUNTADMIN.
-- Snowflake cannot set a tag on a tag ("Object tagging not supported for object type TAG"), so RUN and EXPIRES
-- for this object live in its comment. Teardown drops it with schema DBT_SF_20261015_DS.
create tag if not exists DEVIN_MIGRATION_DEMO.DBT_SF_20261015_DS.PII_CATEGORY
  allowed_values 'NAME', 'EMAIL', 'PHONE', 'STREET_ADDRESS', 'DATE_OF_BIRTH', 'AGE', 'GENDER',
                 'NATIONAL_ID', 'CUSTOMER_ID', 'STAFF_ID', 'ORG_UNIT'
  comment = 'Personal-data category, drives tag-based masking. RUN=SF_20261015_DS, EXPIRES=2026-10-18T02:32:20Z';
