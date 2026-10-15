select
    ACCOUNT_ID,
    ACCOUNT_TYPE,
    CUSTOMER_SEGMENT,
    REGION_CODE,
    cast(CURRENT_BALANCE as float) as CURRENT_BALANCE,
    cast(SNAPSHOT_DATE as date) as SNAPSHOT_DATE
from {{ source('upstream_dbt', 'CUST_ACCOUNTS_DAILY') }}
