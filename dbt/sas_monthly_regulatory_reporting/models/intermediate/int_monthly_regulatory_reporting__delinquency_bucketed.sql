select
    a.ACCOUNT_TYPE,
    a.REGION_CODE,
    a.CURRENT_BALANCE,
    l.PAST_DUE_AMOUNT,
    case
        when l.DAYS_PAST_DUE = 0 then 'Current'
        when l.DAYS_PAST_DUE between 1 and 29 then '1-29'
        when l.DAYS_PAST_DUE between 30 and 59 then '30-59'
        when l.DAYS_PAST_DUE between 60 and 89 then '60-89'
        when l.DAYS_PAST_DUE between 90 and 119 then '90-119'
        when l.DAYS_PAST_DUE between 120 and 179 then '120-179'
        when l.DAYS_PAST_DUE >= 180 then '180+'
        else 'Unknown'
    end as DELINQ_BUCKET
from {{ ref('stg_monthly_regulatory_reporting__cust_accounts_daily') }} as a
left join {{ ref('stg_monthly_regulatory_reporting__loan_details') }} as l
    on a.ACCOUNT_ID = l.ACCOUNT_ID
where a.SNAPSHOT_DATE = last_day(to_date('{{ var("report_month") }}' || '01', 'YYYYMMDD'))
    and a.ACCOUNT_TYPE in ('MTG', 'AUTO', 'PERS', 'CC', 'LOC', 'HELC')
