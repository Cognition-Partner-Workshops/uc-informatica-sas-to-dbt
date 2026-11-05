select
    NEXTVAL as "KEY", LEAD_CO_MNE, BRANCH_CO_MNE, MIS_DATE, ID, DESCRIPTION, SHORT_NAME,
    O_CREATED_BY as CREATED_BY,
    cast(O_CREATED_TIME as timestamp_ntz(6)) as CREATED_TIME,
    cast(null as varchar) as UPDATED_BY,
    cast(null as timestamp_ntz(6)) as UPDATED_TIME,
    cast(null as varchar) as ACTIVE_FLAG,
    cast(null as timestamp_ntz(6)) as START_DATE,
    cast(null as timestamp_ntz(6)) as END_DATE
from {{ ref('int_m_demo_mapping2__seqtrans') }}
