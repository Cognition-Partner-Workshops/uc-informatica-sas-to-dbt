-- One masking policy per data type found in seeds/pii_classification.csv (TEXT, NUMBER, FLOAT, DATE, TIMESTAMP_NTZ).
-- Only a session whose current role is SF_20261015_DS_DBT sees clear values. Every other role, including
-- SF_20261015_DS_READER and roles above SF_20261015_DS_DBT in the hierarchy, sees the masked value:
-- '***MASKED***' for text, NULL for numbers, floats, dates and timestamps.
-- Run as SF_20261015_DS_DBT (CREATE MASKING POLICY on the run's schemas).
create masking policy if not exists DEVIN_MIGRATION_DEMO.DBT_SF_20261015_DS.PII_MASK_VARCHAR
  as (val varchar) returns varchar ->
  case when val is null then null when current_role() = 'SF_20261015_DS_DBT' then val else '***MASKED***' end
  comment = 'PII masking for VARCHAR columns tagged PII_CATEGORY, run SF_20261015_DS';

alter masking policy DEVIN_MIGRATION_DEMO.DBT_SF_20261015_DS.PII_MASK_VARCHAR
  set body -> case when val is null then null when current_role() = 'SF_20261015_DS_DBT' then val else '***MASKED***' end;

create masking policy if not exists DEVIN_MIGRATION_DEMO.DBT_SF_20261015_DS.PII_MASK_NUMBER
  as (val number) returns number ->
  case when current_role() = 'SF_20261015_DS_DBT' then val else null end
  comment = 'PII masking for NUMBER columns tagged PII_CATEGORY, run SF_20261015_DS';

create masking policy if not exists DEVIN_MIGRATION_DEMO.DBT_SF_20261015_DS.PII_MASK_FLOAT
  as (val float) returns float ->
  case when current_role() = 'SF_20261015_DS_DBT' then val else null end
  comment = 'PII masking for FLOAT columns tagged PII_CATEGORY, run SF_20261015_DS';

create masking policy if not exists DEVIN_MIGRATION_DEMO.DBT_SF_20261015_DS.PII_MASK_DATE
  as (val date) returns date ->
  case when current_role() = 'SF_20261015_DS_DBT' then val else null end
  comment = 'PII masking for DATE columns tagged PII_CATEGORY, run SF_20261015_DS';

create masking policy if not exists DEVIN_MIGRATION_DEMO.DBT_SF_20261015_DS.PII_MASK_TIMESTAMP_NTZ
  as (val timestamp_ntz) returns timestamp_ntz ->
  case when current_role() = 'SF_20261015_DS_DBT' then val else null end
  comment = 'PII masking for TIMESTAMP_NTZ columns tagged PII_CATEGORY, run SF_20261015_DS';

alter masking policy DEVIN_MIGRATION_DEMO.DBT_SF_20261015_DS.PII_MASK_VARCHAR
  set tag DEVIN_MIGRATION_DEMO.PUBLIC.RUN = 'SF_20261015_DS', DEVIN_MIGRATION_DEMO.PUBLIC.EXPIRES = '2026-10-18T02:32:20Z';
alter masking policy DEVIN_MIGRATION_DEMO.DBT_SF_20261015_DS.PII_MASK_NUMBER
  set tag DEVIN_MIGRATION_DEMO.PUBLIC.RUN = 'SF_20261015_DS', DEVIN_MIGRATION_DEMO.PUBLIC.EXPIRES = '2026-10-18T02:32:20Z';
alter masking policy DEVIN_MIGRATION_DEMO.DBT_SF_20261015_DS.PII_MASK_FLOAT
  set tag DEVIN_MIGRATION_DEMO.PUBLIC.RUN = 'SF_20261015_DS', DEVIN_MIGRATION_DEMO.PUBLIC.EXPIRES = '2026-10-18T02:32:20Z';
alter masking policy DEVIN_MIGRATION_DEMO.DBT_SF_20261015_DS.PII_MASK_DATE
  set tag DEVIN_MIGRATION_DEMO.PUBLIC.RUN = 'SF_20261015_DS', DEVIN_MIGRATION_DEMO.PUBLIC.EXPIRES = '2026-10-18T02:32:20Z';
alter masking policy DEVIN_MIGRATION_DEMO.DBT_SF_20261015_DS.PII_MASK_TIMESTAMP_NTZ
  set tag DEVIN_MIGRATION_DEMO.PUBLIC.RUN = 'SF_20261015_DS', DEVIN_MIGRATION_DEMO.PUBLIC.EXPIRES = '2026-10-18T02:32:20Z';
