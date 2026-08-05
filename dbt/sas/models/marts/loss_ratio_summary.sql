-- REPORTS.LOSS_RATIO_SUMMARY: PROC MEANS NWAY by line of business plus
-- aggregate ratios (missing when TOTAL_EARNED is not > 0, per the legacy
-- guard).
select
    policy_type,
    count(ytd_earned_premium) as n_policies,
    sum(ytd_earned_premium) as total_earned,
    sum(total_incurred) as total_incurred,
    sum(total_paid) as total_paid,
    sum(total_reserve) as total_reserves,
    sum(ibnr_estimate) as total_ibnr,
    case
        when sum(ytd_earned_premium) > 0
            then sum(total_incurred) / sum(ytd_earned_premium)
    end as agg_loss_ratio,
    case
        when sum(ytd_earned_premium) > 0
            then sum(total_incurred) / sum(ytd_earned_premium) + 0.30
    end as agg_combined_ratio
from {{ ref('policy_valuation') }}
group by policy_type
