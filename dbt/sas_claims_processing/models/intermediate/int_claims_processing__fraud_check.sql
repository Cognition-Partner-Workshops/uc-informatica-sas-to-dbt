select
    c.CLAIM_ID,
    c.POLICY_ID,
    c.CLAIMANT_ID,
    c.LOSS_DATE,
    c.REPORTED_DATE,
    c.CLAIMED_AMOUNT,
    c.CAUSE_CODE,
    c.DESCRIPTION,
    c.POLICY_TYPE,
    c.EFFECTIVE_DATE,
    c.EXPIRATION_DATE,
    c.SUM_INSURED,
    c.DEDUCTIBLE,
    fi.FRAUD_SCORE,
    fi.INDICATOR_FLAGS,
    case
        when fi.FRAUD_SCORE >= 80 then 'HIGH'
        when fi.FRAUD_SCORE >= 50 then 'MEDIUM'
        else 'LOW'
    end as FRAUD_RISK
from {{ ref('int_claims_processing__claims_validation') }} as c
left join {{ ref('stg_claims_processing__raw_ins_fraud_indicators') }} as fi
    on c.POLICY_ID = fi.POLICY_ID
    and c.CLAIMANT_ID = fi.CLAIMANT_ID
where c.VALIDATION_ERROR is null
