select
    CLAIM_ID::varchar as CLAIM_ID,
    POLICY_ID::varchar as POLICY_ID,
    CLAIMANT_ID::varchar as CLAIMANT_ID,
    LOSS_DATE::date as LOSS_DATE,
    REPORT_DATE::date as REPORT_DATE,
    CLAIM_STATUS::varchar as CLAIM_STATUS,
    INCURRED_AMOUNT::float as INCURRED_AMOUNT,
    PAID_AMOUNT::float as PAID_AMOUNT,
    RESERVED_AMOUNT::float as RESERVED_AMOUNT
from {{ source('raw_ins', 'RAW_INS_CLAIMS') }}
