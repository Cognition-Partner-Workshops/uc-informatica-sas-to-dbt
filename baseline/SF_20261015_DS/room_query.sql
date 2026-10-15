-- Row counts of every legacy baseline target, as loaded for the run
select 'ACCT_EXCEPTIONS' as target, count(*) as row_count from DEVIN_MIGRATION_DEMO.BASELINE_SF_20261015_DS.ACCT_EXCEPTIONS
union all
select 'CAPITAL_ADEQUACY' as target, count(*) as row_count from DEVIN_MIGRATION_DEMO.BASELINE_SF_20261015_DS.CAPITAL_ADEQUACY
union all
select 'CLAIMS_REGISTER' as target, count(*) as row_count from DEVIN_MIGRATION_DEMO.BASELINE_SF_20261015_DS.CLAIMS_REGISTER
union all
select 'CLAIMS_REVIEW_QUEUE' as target, count(*) as row_count from DEVIN_MIGRATION_DEMO.BASELINE_SF_20261015_DS.CLAIMS_REVIEW_QUEUE
union all
select 'CUST_ACCOUNTS_DAILY' as target, count(*) as row_count from DEVIN_MIGRATION_DEMO.BASELINE_SF_20261015_DS.CUST_ACCOUNTS_DAILY
union all
select 'DAILY_TRANSACTIONS' as target, count(*) as row_count from DEVIN_MIGRATION_DEMO.BASELINE_SF_20261015_DS.DAILY_TRANSACTIONS
union all
select 'DELINQUENCY_AGING' as target, count(*) as row_count from DEVIN_MIGRATION_DEMO.BASELINE_SF_20261015_DS.DELINQUENCY_AGING
union all
select 'DEMO_TARGET1_INS' as target, count(*) as row_count from DEVIN_MIGRATION_DEMO.BASELINE_SF_20261015_DS.DEMO_TARGET1_INS
union all
select 'DEMO_TARGET1_UPD' as target, count(*) as row_count from DEVIN_MIGRATION_DEMO.BASELINE_SF_20261015_DS.DEMO_TARGET1_UPD
union all
select 'DEMO_TARGET2' as target, count(*) as row_count from DEVIN_MIGRATION_DEMO.BASELINE_SF_20261015_DS.DEMO_TARGET2
union all
select 'DEMO_TARGET21' as target, count(*) as row_count from DEVIN_MIGRATION_DEMO.BASELINE_SF_20261015_DS.DEMO_TARGET21
union all
select 'DEMO_TARGET3' as target, count(*) as row_count from DEVIN_MIGRATION_DEMO.BASELINE_SF_20261015_DS.DEMO_TARGET3
union all
select 'DEMO_TARGET5' as target, count(*) as row_count from DEVIN_MIGRATION_DEMO.BASELINE_SF_20261015_DS.DEMO_TARGET5
union all
select 'DEMO_TARGET6' as target, count(*) as row_count from DEVIN_MIGRATION_DEMO.BASELINE_SF_20261015_DS.DEMO_TARGET6
union all
select 'FRAUD_ALERTS' as target, count(*) as row_count from DEVIN_MIGRATION_DEMO.BASELINE_SF_20261015_DS.FRAUD_ALERTS
union all
select 'LLP_COVERAGE' as target, count(*) as row_count from DEVIN_MIGRATION_DEMO.BASELINE_SF_20261015_DS.LLP_COVERAGE
union all
select 'LOSS_RATIO_SUMMARY' as target, count(*) as row_count from DEVIN_MIGRATION_DEMO.BASELINE_SF_20261015_DS.LOSS_RATIO_SUMMARY
union all
select 'MONTHLY_RWA' as target, count(*) as row_count from DEVIN_MIGRATION_DEMO.BASELINE_SF_20261015_DS.MONTHLY_RWA
union all
select 'POLICY_VALUATION' as target, count(*) as row_count from DEVIN_MIGRATION_DEMO.BASELINE_SF_20261015_DS.POLICY_VALUATION
union all
select 'RISK_MIGRATION' as target, count(*) as row_count from DEVIN_MIGRATION_DEMO.BASELINE_SF_20261015_DS.RISK_MIGRATION
union all
select 'RISK_SCORES' as target, count(*) as row_count from DEVIN_MIGRATION_DEMO.BASELINE_SF_20261015_DS.RISK_SCORES
union all
select 'RISK_SUMMARY' as target, count(*) as row_count from DEVIN_MIGRATION_DEMO.BASELINE_SF_20261015_DS.RISK_SUMMARY
union all
select 'RUNNING_BALANCES' as target, count(*) as row_count from DEVIN_MIGRATION_DEMO.BASELINE_SF_20261015_DS.RUNNING_BALANCES
union all
select 'TXN_ANOMALIES' as target, count(*) as row_count from DEVIN_MIGRATION_DEMO.BASELINE_SF_20261015_DS.TXN_ANOMALIES
order by 1;
