select
    ACCOUNT_ID,
    CUSTOMER_ID,
    ACCOUNT_TYPE,
    ACCOUNT_STATUS,
    cast(OPEN_DATE as date) as OPEN_DATE,
    cast(CLOSE_DATE as date) as CLOSE_DATE,
    CURRENT_BALANCE,
    AVAILABLE_BALANCE,
    CREDIT_LIMIT,
    cast(INTEREST_RATE as float) as INTEREST_RATE,
    BRANCH_ID,
    OFFICER_ID,
    cast(LAST_ACTIVITY_DATE as date) as LAST_ACTIVITY_DATE
from {{ source('source_sf', 'ORA_DW_CUST_ACCOUNTS') }}
