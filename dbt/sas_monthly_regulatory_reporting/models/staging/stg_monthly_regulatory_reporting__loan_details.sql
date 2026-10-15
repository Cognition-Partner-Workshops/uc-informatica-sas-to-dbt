select
    ACCOUNT_ID,
    cast(LTV as float) as LTV,
    cast(DAYS_PAST_DUE as number) as DAYS_PAST_DUE,
    cast(PAST_DUE_AMOUNT as float) as PAST_DUE_AMOUNT,
    cast(ALLOWANCE_AMT as float) as ALLOWANCE_AMT
from {{ source('source_sf', 'ORA_DW_LOAN_DETAILS') }}
