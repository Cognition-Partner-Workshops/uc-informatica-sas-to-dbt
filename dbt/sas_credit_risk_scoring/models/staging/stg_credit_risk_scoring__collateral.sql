select
    ACCOUNT_ID,
    cast(COLLATERAL_VALUE as float) as COLLATERAL_VALUE,
    cast(LAST_APPRAISAL_DATE as date) as LAST_APPRAISAL_DATE
from {{ source('source_sf', 'ORA_DW_COLLATERAL') }}
