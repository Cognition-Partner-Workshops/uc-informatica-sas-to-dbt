select
    DIM_KEY as "KEY", LEAD_CO_MNE, BRANCH_CO_MNE, MIS_DATE, ID, DESCRIPTION, SHORT_NAME,
    cast(null as varchar) as CREATED_BY,
    cast(null as timestamp_ntz(6)) as CREATED_TIME,
    O_UPDATED_BY as UPDATED_BY,
    cast(O_UPDATED_TIME as timestamp_ntz(6)) as UPDATED_TIME,
    cast(null as varchar) as ACTIVE_FLAG,
    cast(null as timestamp_ntz(6)) as START_DATE,
    cast(null as timestamp_ntz(6)) as END_DATE
from {{ ref('int_m_demo_mapping2__updtrans') }}
