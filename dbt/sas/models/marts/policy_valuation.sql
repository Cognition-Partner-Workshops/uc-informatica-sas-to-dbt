-- STG_INS.POLICY_VALUATION: in-force valuation metrics with loss/combined
-- ratios, premium adequacy, IBNR, and total reserve. The $POLTYPE/$RISKCAT
-- display formats are materialized as *_DESC columns via seed lookups.
with merged as (
    select
        i.*,
        c.num_claims,
        c.total_incurred,
        c.total_paid,
        c.total_reserved,
        c.last_claim_date,
        c.open_reserves,
        c.denied_claims,
        m.collected_premium,
        m.returned_premium,
        m.last_payment_date,
        m.late_payments
    from {{ ref('int_policy_inforce') }} i
    left join {{ ref('int_claims_experience') }} c
        on i.policy_id = c.policy_id
    left join {{ ref('int_premium_collections') }} m
        on i.policy_id = m.policy_id
)

select
    g.*,
    case
        when g.ytd_earned_premium > 0
            then coalesce(g.total_incurred, 0) / g.ytd_earned_premium
    end as loss_ratio,
    case
        when g.ytd_earned_premium > 0
            then coalesce(g.total_incurred, 0) / g.ytd_earned_premium + 0.30
    end as combined_ratio,
    case
        when g.ytd_earned_premium > 0
             and coalesce(g.total_incurred, 0) / g.ytd_earned_premium + 0.30 <= 1.0
            then 'Y' else 'N'
    end as premium_adequate,
    greatest(0, g.ytd_earned_premium * 0.15 - coalesce(g.total_paid, 0))
        as ibnr_estimate,
    coalesce(g.open_reserves, 0)
        + greatest(0, g.ytd_earned_premium * 0.15 - coalesce(g.total_paid, 0))
        as total_reserve,
    cast('{{ var("run_date") }}' as date) as valuation_date,
    coalesce(fp.label, 'Unknown') as policy_type_desc,
    coalesce(fr.label, 'Unrated') as risk_category_desc
from merged g
left join {{ ref('fmt_policy_type') }} fp on g.policy_type = fp.code
left join {{ ref('fmt_risk_category') }} fr on g.risk_category = fr.code
