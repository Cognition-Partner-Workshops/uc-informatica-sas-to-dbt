select
    POLICY_ID::varchar as POLICY_ID,
    CUSTOMER_ID::varchar as CUSTOMER_ID,
    POLICY_TYPE::varchar as POLICY_TYPE,
    STATUS::varchar as STATUS,
    EFFECTIVE_DATE::date as EFFECTIVE_DATE,
    EXPIRATION_DATE::date as EXPIRATION_DATE,
    ANNUAL_PREMIUM::float as ANNUAL_PREMIUM,
    SUM_INSURED::float as SUM_INSURED,
    DEDUCTIBLE::float as DEDUCTIBLE,
    RISK_CATEGORY::varchar as RISK_CATEGORY,
    UNDERWRITING_CLASS::varchar as UNDERWRITING_CLASS,
    AGENT_ID::varchar as AGENT_ID,
    BRANCH_CODE::varchar as BRANCH_CODE
from {{ source('raw_ins', 'RAW_INS_POLICIES') }}
