{% set score_date = "cast('" ~ var('score_date') ~ "' as date)" %}

with bureau_max_date as (
    -- correlated subquery: max(SCORE_DATE) per CUSTOMER_ID with SCORE_DATE <= score date
    select CUSTOMER_ID, max(SCORE_DATE) as MAX_SCORE_DATE
    from {{ ref('stg_credit_risk_scoring__bureau_scores') }}
    where SCORE_DATE <= {{ score_date }}
    group by CUSTOMER_ID
),

bureau as (
    select b.*
    from {{ ref('stg_credit_risk_scoring__bureau_scores') }} b
    inner join bureau_max_date m
        on b.CUSTOMER_ID = m.CUSTOMER_ID
        and b.SCORE_DATE = m.MAX_SCORE_DATE
)

select
    a.ACCOUNT_ID,
    a.CUSTOMER_ID,
    a.ACCOUNT_TYPE,
    a.CURRENT_BALANCE,
    a.CREDIT_LIMIT,
    a.ACCT_AGE_MONTHS,
    a.DAYS_INACTIVE,
    a.UTILIZATION_PCT,
    a.CUSTOMER_SEGMENT,
    a.REGION_CODE,
    b.FICO_SCORE,
    b.VANTAGE_SCORE,
    b.BUREAU_INQS_6MO,
    b.BUREAU_TRADES_OPEN,
    b.BUREAU_DEROGS,
    b.BUREAU_UTIL_PCT,
    b.BUREAU_OLDEST_TRADE_MO,
    p.PMT_ONTIME_12MO,
    p.PMT_LATE_30_12MO,
    p.PMT_LATE_60_12MO,
    p.PMT_LATE_90_12MO,
    p.MAX_DAYS_PAST_DUE_EVER,
    p.MONTHS_SINCE_LAST_DPD,
    p.AVG_PMT_RATIO_12MO,
    c.COLLATERAL_VALUE,
    c.LAST_APPRAISAL_DATE,
    case
        when c.COLLATERAL_VALUE > 0 then a.CURRENT_BALANCE / c.COLLATERAL_VALUE
    end as LTV
from {{ ref('stg_credit_risk_scoring__cust_accounts_daily') }} a
left join bureau b
    on a.CUSTOMER_ID = b.CUSTOMER_ID
left join {{ ref('stg_credit_risk_scoring__payment_history') }} p
    on a.ACCOUNT_ID = p.ACCOUNT_ID
left join {{ ref('stg_credit_risk_scoring__collateral') }} c
    on a.ACCOUNT_ID = c.ACCOUNT_ID
where a.SNAPSHOT_DATE = {{ score_date }}
  and a.ACCOUNT_TYPE in ('MTG', 'AUTO', 'PERS', 'CC', 'LOC', 'HELC')
