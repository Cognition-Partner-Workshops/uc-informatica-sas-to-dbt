select
    PAYMENT_ID::varchar as PAYMENT_ID,
    POLICY_ID::varchar as POLICY_ID,
    PAYMENT_DATE::date as PAYMENT_DATE,
    PREMIUM_AMOUNT::float as PREMIUM_AMOUNT,
    PAYMENT_STATUS::varchar as PAYMENT_STATUS
from {{ source('raw_ins', 'RAW_INS_PREMIUMS') }}
