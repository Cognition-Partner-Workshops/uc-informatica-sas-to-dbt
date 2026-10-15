select
    POLICY_ID,
    CLAIMANT_ID,
    FRAUD_SCORE,
    INDICATOR_FLAGS
from {{ source('legacy', 'RAW_INS_FRAUD_INDICATORS') }}
