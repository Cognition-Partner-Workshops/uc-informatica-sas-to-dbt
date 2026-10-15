with adjudication_rules as (
    select
        *,
        case
            when FRAUD_RISK = 'HIGH' then 'DENY'
            when FRAUD_RISK = 'LOW'
                and (CLAIMED_AMOUNT is null or CLAIMED_AMOUNT <= 5000)
                and POLICY_TYPE in ('AUTO', 'HOME', 'RENT') then 'APPR'
            when FRAUD_RISK = 'LOW'
                and (CLAIMED_AMOUNT is null or CLAIMED_AMOUNT <= SUM_INSURED * 0.25)
                and (CLAIMED_AMOUNT is null or CLAIMED_AMOUNT <= 50000) then 'APPR'
            else 'PEND'
        end as ADJUDICATION_RESULT
    from {{ ref('int_claims_processing__fraud_check') }}
)

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
    ADJUDICATION_RESULT,
    case
        when ADJUDICATION_RESULT = 'DENY' then 'High fraud risk - SIU referral'
        when ADJUDICATION_RESULT = 'APPR'
            and FRAUD_RISK = 'LOW'
            and (CLAIMED_AMOUNT is null or CLAIMED_AMOUNT <= 5000)
            and POLICY_TYPE in ('AUTO', 'HOME', 'RENT')
            then 'Auto-approved: low risk, small claim'
        when ADJUDICATION_RESULT = 'APPR' then
            'Auto-approved: within 25% of sum insured'
        else nullif(
            array_to_string(
                array_construct_compact(
                    iff(FRAUD_RISK = 'MEDIUM', 'Medium fraud risk', null),
                    iff(CLAIMED_AMOUNT is not null and CLAIMED_AMOUNT > 50000, 'Large claim', null),
                    iff(
                        (CLAIMED_AMOUNT is not null and SUM_INSURED * 0.25 is null)
                            or CLAIMED_AMOUNT > SUM_INSURED * 0.25,
                        'Exceeds 25% threshold',
                        null
                    )
                ),
                '; '
            ),
            ''
        )
    end as ADJUDICATION_REASON,
    case
        when ADJUDICATION_RESULT = 'DENY' then 0::float
        when ADJUDICATION_RESULT = 'APPR' then
            greatest(0, coalesce(CLAIMED_AMOUNT - DEDUCTIBLE, 0))::float
        else null::float
    end as APPROVED_AMOUNT,
    ADJUDICATION_RESULT in ('DENY', 'PEND') as IS_MANUAL_REVIEW
from adjudication_rules
