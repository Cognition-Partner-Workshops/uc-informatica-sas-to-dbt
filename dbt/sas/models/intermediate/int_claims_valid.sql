-- claims_processing step 1: hash-object lookup against ACTIVE policies plus
-- sequential validation (policy found, loss date in period, claimed amount
-- within sum insured). Invalid rows are excluded (WORK.CLAIMS_INVALID is
-- never persisted by the legacy program).
select
    f.claim_id,
    f.policy_id,
    f.claimant_id,
    f.loss_date,
    f.reported_date,
    f.claimed_amount,
    f.cause_code,
    f.description,
    p.policy_type,
    p.effective_date,
    p.expiration_date,
    p.sum_insured,
    p.deductible
from {{ ref('stg_claims_feed') }} f
inner join {{ ref('stg_policies') }} p
    on f.policy_id = p.policy_id
   and p.status = 'ACTIVE'
where f.loss_date >= p.effective_date
  and f.loss_date <= p.expiration_date
  and f.claimed_amount <= p.sum_insured
