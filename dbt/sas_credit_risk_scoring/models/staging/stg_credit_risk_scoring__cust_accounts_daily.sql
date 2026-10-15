select
    ACCOUNT_ID,
    CUSTOMER_ID,
    ACCOUNT_TYPE,
    cast(CURRENT_BALANCE as float) as CURRENT_BALANCE,
    cast(CREDIT_LIMIT as float) as CREDIT_LIMIT,
    ACCT_AGE_MONTHS,
    DAYS_INACTIVE,
    cast(UTILIZATION_PCT as float) as UTILIZATION_PCT,
    CUSTOMER_SEGMENT,
    REGION_CODE,
    cast(RISK_RATING as float) as RISK_RATING,
    cast(SNAPSHOT_DATE as date) as SNAPSHOT_DATE
from {{ source('upstream_dbt', 'CUST_ACCOUNTS_DAILY') }}
