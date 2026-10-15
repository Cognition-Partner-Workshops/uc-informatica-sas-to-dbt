select
    cast('{{ var("score_date") }}' as date) as SCORE_DATE,
    a.ACCOUNT_ID,
    a.RISK_RATING as PREV_RATING,
    s.NEW_RISK_RATING as CURR_RATING,
    case
        when a.RISK_RATING is null then 'NEW'
        when s.NEW_RISK_RATING < a.RISK_RATING then 'UPGRADE'
        when s.NEW_RISK_RATING > a.RISK_RATING then 'DOWNGRADE'
        else 'STABLE'
    end as MIGRATION_DIRECTION,
    s.PD,
    s.EXPECTED_LOSS
from {{ ref('int_credit_risk_scoring__scored') }} s
inner join {{ ref('stg_credit_risk_scoring__cust_accounts_daily') }} a
    on s.ACCOUNT_ID = a.ACCOUNT_ID
where a.SNAPSHOT_DATE = cast('{{ var("score_date") }}' as date)
  and (a.RISK_RATING <> s.NEW_RISK_RATING or a.RISK_RATING is null)
