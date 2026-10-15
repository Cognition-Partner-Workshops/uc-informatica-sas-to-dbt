select
    cast(ACCOUNT_ID as varchar) as ACCOUNT_ID,
    cast(ACCOUNT_TYPE as varchar) as ACCOUNT_TYPE,
    cast(CUSTOMER_ID as varchar) as CUSTOMER_ID,
    cast(CUSTOMER_SEGMENT as varchar) as CUSTOMER_SEGMENT,
    cast(REGION_CODE as varchar) as REGION_CODE,
    cast(BRANCH_ID as varchar) as BRANCH_ID,
    cast(CURRENT_BALANCE as float) as CURRENT_BALANCE,
    cast(RISK_RATING as float) as RISK_RATING
from {{ source('upstream_dbt', 'CUST_ACCOUNTS_DAILY') }}
