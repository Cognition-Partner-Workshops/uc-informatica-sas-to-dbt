select
    '{{ var("report_month") }}'::varchar(6) as REPORT_MONTH,
    ACCOUNT_TYPE,
    CUSTOMER_SEGMENT,
    RISK_WEIGHT,
    count(*) as N_ACCOUNTS,
    cast(sum(CURRENT_BALANCE) as float) as TOTAL_EXPOSURE,
    cast(sum(CURRENT_BALANCE * RISK_WEIGHT) as float) as RWA
from {{ ref('int_monthly_regulatory_reporting__rwa_weighted') }}
group by ACCOUNT_TYPE, CUSTOMER_SEGMENT, RISK_WEIGHT
