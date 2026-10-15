select
    CLAIM_ID,
    POLICY_ID,
    CLAIMANT_ID,
    LOSS_DATE,
    REPORTED_DATE,
    CLAIMED_AMOUNT,
    CAUSE_CODE,
    DESCRIPTION,
    POLICY_TYPE,
    EFFECTIVE_DATE,
    EXPIRATION_DATE,
    SUM_INSURED,
    DEDUCTIBLE,
    FRAUD_SCORE,
    INDICATOR_FLAGS,
    FRAUD_RISK,
    array_to_string(
        array_construct_compact(
            'Fraud score: ' || to_varchar(round(FRAUD_SCORE)),
            nullif(trim(INDICATOR_FLAGS), '')
        ),
        '; '
    ) as ALERT_REASON,
    '{{ var("proc_date") }}'::date as ALERT_DATE
from {{ ref('int_claims_processing__fraud_check') }}
where FRAUD_RISK = 'HIGH'
