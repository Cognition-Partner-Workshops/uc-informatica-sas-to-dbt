select
    a.CLAIM_ID,
    a.POLICY_ID,
    a.CLAIMANT_ID,
    a.LOSS_DATE,
    a.REPORTED_DATE,
    a.CLAIMED_AMOUNT,
    a.CAUSE_CODE,
    a.DESCRIPTION,
    a.POLICY_TYPE,
    a.EFFECTIVE_DATE,
    a.EXPIRATION_DATE,
    a.SUM_INSURED,
    a.DEDUCTIBLE,
    a.FRAUD_SCORE,
    a.INDICATOR_FLAGS,
    a.FRAUD_RISK,
    a.ADJUDICATION_RESULT,
    a.ADJUDICATION_REASON,
    a.APPROVED_AMOUNT,
    '{{ var("proc_date") }}'::date as PROCESSING_DATE,
    a.ADJUDICATION_RESULT as CLAIM_STATUS,
    coalesce(s.LABEL, 'Unknown') as CLAIM_STATUS_DESC
from {{ ref('int_claims_processing__adjudication') }} as a
left join {{ ref('claims_processing__fmt_clmstat') }} as s
    on a.ADJUDICATION_RESULT = s.CODE
