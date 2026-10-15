select
    ACCOUNT_TYPE,
    REGION_CODE,
    count(CURRENT_BALANCE) as N_ACCOUNTS,
    sum(CURRENT_BALANCE) as TOTAL_BALANCE,
    avg(CURRENT_BALANCE) as AVG_BALANCE,
    avg(UTILIZATION_PCT) as AVG_UTILIZATION,
    avg(ACCT_AGE_MONTHS) as AVG_AGE_MONTHS
from {{ ref('int_load_customer_accounts__acct_derived') }}
group by ACCOUNT_TYPE, REGION_CODE
