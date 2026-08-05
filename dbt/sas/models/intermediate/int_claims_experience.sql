-- policy_valuation step 2: 12-month claims experience per policy
-- (window = intnx('month', val_date, -12) .. val_date).
select
    c.policy_id,
    count(distinct c.claim_id) as num_claims,
    sum(c.incurred_amount) as total_incurred,
    sum(c.paid_amount) as total_paid,
    sum(c.reserved_amount) as total_reserved,
    max(c.loss_date) as last_claim_date,
    sum(case when c.claim_status in ('OPEN', 'INV', 'ADJ', 'PEND')
             then c.reserved_amount else 0 end) as open_reserves,
    sum(case when c.claim_status = 'DENY' then 1 else 0 end) as denied_claims
from {{ ref('stg_claims') }} c
where c.loss_date >= cast('{{ var("claims_window_start") }}' as date)
  and c.loss_date <= cast('{{ var("run_date") }}' as date)
group by c.policy_id
