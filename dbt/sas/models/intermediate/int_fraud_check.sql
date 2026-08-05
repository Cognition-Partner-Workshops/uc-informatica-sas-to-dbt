-- claims_processing step 2: fraud screening with $-format style recode of
-- the fraud score into HIGH / MEDIUM / LOW bands.
select
    c.*,
    f.fraud_score,
    f.indicator_flags,
    case
        when f.fraud_score >= 80 then 'HIGH'
        when f.fraud_score >= 50 then 'MEDIUM'
        else 'LOW'
    end as fraud_risk
from {{ ref('int_claims_valid') }} c
left join {{ ref('stg_fraud_indicators') }} f
    on c.policy_id = f.policy_id
   and c.claimant_id = f.claimant_id
