select
    a.ACCOUNT_TYPE,
    a.CURRENT_BALANCE,
    l.ALLOWANCE_AMT,
    l.DAYS_PAST_DUE
from {{ ref('stg_monthly_regulatory_reporting__cust_accounts_daily') }} as a
inner join {{ ref('stg_monthly_regulatory_reporting__loan_details') }} as l
    on a.ACCOUNT_ID = l.ACCOUNT_ID
where a.SNAPSHOT_DATE = last_day(to_date('{{ var("report_month") }}' || '01', 'YYYYMMDD'))
    and a.ACCOUNT_TYPE in ('MTG', 'AUTO', 'PERS', 'CC', 'LOC', 'HELC')
