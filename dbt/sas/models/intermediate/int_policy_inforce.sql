-- policy_valuation step 1: in-force policies at the valuation date with
-- age/expiry metrics, renewal flag, and YTD earned premium (month-boundary
-- counting per SAS intck; 0 at the January valuation date).
with run as (
    select cast('{{ var("run_date") }}' as date) as run_date
)

select
    p.policy_id,
    p.customer_id,
    p.policy_type,
    p.effective_date,
    p.expiration_date,
    p.annual_premium,
    p.sum_insured,
    p.deductible,
    p.risk_category,
    p.underwriting_class,
    p.agent_id,
    p.branch_code,
    datediff('month', p.effective_date, r.run_date) as policy_age_months,
    datediff('month', r.run_date, p.expiration_date) as months_to_expiry,
    -- intnx('month', run_date, 3) with default BEGINNING alignment
    case
        when p.expiration_date <= cast('{{ var("renewal_horizon_end") }}' as date)
            then 'Y' else 'N'
    end as renewal_due_flag,
    p.annual_premium / 12 * least(12,
        datediff('month',
            greatest(p.effective_date, cast('{{ var("year_start") }}' as date)),
            least(r.run_date, p.expiration_date))) as ytd_earned_premium
from {{ ref('stg_policies') }} p
cross join run r
where p.status = 'ACTIVE'
  and p.effective_date <= r.run_date
  and p.expiration_date >= r.run_date
