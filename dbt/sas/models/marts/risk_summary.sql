-- REPORTS.RISK_SUMMARY: PROC MEANS NWAY by account type x new risk rating.
select
    account_type,
    new_risk_rating,
    count(pd) as n_accounts,
    avg(pd) as avg_pd,
    avg(lgd) as avg_lgd,
    sum(ead) as total_ead,
    sum(expected_loss) as total_el
from {{ ref('int_scored') }}
group by account_type, new_risk_rating
