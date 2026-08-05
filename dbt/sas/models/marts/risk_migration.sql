-- CURATED.RISK_MIGRATION: accounts whose model rating differs from the
-- snapshot rating (or that have no prior rating).
select
    cast('{{ var("run_date") }}' as date) as score_date,
    a.account_id,
    a.risk_rating as prev_rating,
    s.new_risk_rating as curr_rating,
    case
        when a.risk_rating is null then 'NEW'
        when s.new_risk_rating < a.risk_rating then 'UPGRADE'
        when s.new_risk_rating > a.risk_rating then 'DOWNGRADE'
        else 'STABLE'
    end as migration_direction,
    s.pd,
    s.expected_loss
from {{ ref('int_scored') }} s
inner join {{ ref('cust_accounts_daily') }} a
    on s.account_id = a.account_id
where a.snapshot_date = cast('{{ var("run_date") }}' as date)
  and (a.risk_rating <> s.new_risk_rating or a.risk_rating is null)
