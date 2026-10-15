with claims_with_active_policy as (
    select
        f.CLAIM_ID,
        f.POLICY_ID,
        f.CLAIMANT_ID,
        f.LOSS_DATE,
        f.REPORTED_DATE,
        f.CLAIMED_AMOUNT,
        f.CAUSE_CODE,
        f.DESCRIPTION,
        p.POLICY_ID as MATCHED_POLICY_ID,
        p.POLICY_TYPE,
        p.EFFECTIVE_DATE,
        p.EXPIRATION_DATE,
        p.SUM_INSURED,
        p.DEDUCTIBLE
    from {{ ref('stg_claims_processing__raw_ins_claims_feed') }} as f
    left join {{ ref('stg_claims_processing__raw_ins_policies') }} as p
        on f.POLICY_ID = p.POLICY_ID
        and p.STATUS = 'ACTIVE'
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
    case
        when MATCHED_POLICY_ID is null then
            'Policy not found or inactive:' ||
            coalesce(' ' || nullif(trim(POLICY_ID), ''), '')
        when (
            (LOSS_DATE is null and EFFECTIVE_DATE is not null) or LOSS_DATE < EFFECTIVE_DATE
            or (LOSS_DATE is not null and EXPIRATION_DATE is null) or LOSS_DATE > EXPIRATION_DATE
        ) then
            'Loss date ' || coalesce(upper(to_char(LOSS_DATE, 'DDMONYYYY')), '.') ||
            ' outside policy period ' ||
            coalesce(upper(to_char(EFFECTIVE_DATE, 'DDMONYYYY')), '.') || ' - ' ||
            coalesce(upper(to_char(EXPIRATION_DATE, 'DDMONYYYY')), '.')
        when (CLAIMED_AMOUNT is not null and SUM_INSURED is null)
            or CLAIMED_AMOUNT > SUM_INSURED then
            'Claimed amount ' || coalesce(trim(to_varchar(CLAIMED_AMOUNT, '$999,999,999,990.00')), '.') ||
            ' exceeds sum insured ' || coalesce(trim(to_varchar(SUM_INSURED, '$999,999,999,990.00')), '.')
        else null
    end as VALIDATION_ERROR
from claims_with_active_policy
