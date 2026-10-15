select
    a.ACCOUNT_TYPE,
    a.CUSTOMER_SEGMENT,
    a.CURRENT_BALANCE,
    cast(
        case
            when a.ACCOUNT_TYPE in ('CHK', 'SAV', 'MMA') then 0.00
            when a.ACCOUNT_TYPE = 'CD' then 0.00
            when a.ACCOUNT_TYPE = 'MTG' and (l.LTV <= 0.80 or l.LTV is null) then 0.35
            when a.ACCOUNT_TYPE = 'MTG' and l.LTV > 0.80 then 0.50
            when a.ACCOUNT_TYPE = 'HELC' then 0.50
            when a.ACCOUNT_TYPE in ('AUTO', 'PERS') then 0.75
            when a.ACCOUNT_TYPE = 'CC' then 0.75
            when a.ACCOUNT_TYPE = 'LOC' then 1.00
            else 1.00
        end as float
    ) as RISK_WEIGHT
from {{ ref('stg_monthly_regulatory_reporting__cust_accounts_daily') }} as a
left join {{ ref('stg_monthly_regulatory_reporting__loan_details') }} as l
    on a.ACCOUNT_ID = l.ACCOUNT_ID
where a.SNAPSHOT_DATE = last_day(to_date('{{ var("report_month") }}' || '01', 'YYYYMMDD'))
