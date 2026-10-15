select
    CUSTOMER_ID,
    FIRST_NAME,
    LAST_NAME,
    SSN_HASH,
    cast(DATE_OF_BIRTH as date) as DATE_OF_BIRTH,
    CUSTOMER_SEGMENT,
    cast(RISK_RATING as float) as RISK_RATING,
    REGION_CODE,
    PRIMARY_EMAIL,
    PHONE_NUMBER
from {{ source('source_sf', 'ORA_DW_CUST_DEMOGRAPHICS') }}
