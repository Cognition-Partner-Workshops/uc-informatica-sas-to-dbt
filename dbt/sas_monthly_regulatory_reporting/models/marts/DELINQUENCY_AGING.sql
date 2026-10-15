select
    '{{ var("report_month") }}'::varchar(6) as REPORT_MONTH,
    ACCOUNT_TYPE,
    REGION_CODE,
    DELINQ_BUCKET,
    count(*) as N_ACCOUNTS,
    cast(sum(CURRENT_BALANCE) as float) as TOTAL_BALANCE,
    cast(sum(PAST_DUE_AMOUNT) as float) as TOTAL_PAST_DUE
from {{ ref('int_monthly_regulatory_reporting__delinquency_bucketed') }}
group by ACCOUNT_TYPE, REGION_CODE, DELINQ_BUCKET
