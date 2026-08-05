-- claims_processing step 3: sequential auto-adjudication rules (first match
-- wins): high fraud -> DENY, low-risk small claim -> APPR, low-risk within
-- 25% of sum insured -> APPR, everything else -> PEND.
select
    *,
    case
        when fraud_risk = 'HIGH' then 'DENY'
        when fraud_risk = 'LOW' and claimed_amount <= 5000
             and policy_type in ('AUTO', 'HOME', 'RENT') then 'APPR'
        when fraud_risk = 'LOW' and claimed_amount <= sum_insured * 0.25
             and claimed_amount <= 50000 then 'APPR'
        else 'PEND'
    end as adjudication_result,
    case
        when fraud_risk = 'HIGH' then 'High fraud risk - SIU referral'
        when fraud_risk = 'LOW' and claimed_amount <= 5000
             and policy_type in ('AUTO', 'HOME', 'RENT')
            then 'Auto-approved: low risk, small claim'
        when fraud_risk = 'LOW' and claimed_amount <= sum_insured * 0.25
             and claimed_amount <= 50000
            then 'Auto-approved: within 25% of sum insured'
        else concat_ws('; ',
            case when fraud_risk = 'MEDIUM' then 'Medium fraud risk' end,
            case when claimed_amount > 50000 then 'Large claim' end,
            case when claimed_amount > sum_insured * 0.25
                 then 'Exceeds 25% threshold' end)
    end as adjudication_reason,
    case
        when fraud_risk = 'HIGH' then 0
        when fraud_risk = 'LOW' and claimed_amount <= 5000
             and policy_type in ('AUTO', 'HOME', 'RENT')
            then greatest(0, claimed_amount - deductible)
        when fraud_risk = 'LOW' and claimed_amount <= sum_insured * 0.25
             and claimed_amount <= 50000
            then greatest(0, claimed_amount - deductible)
    end as approved_amount
from {{ ref('int_fraud_check') }}
