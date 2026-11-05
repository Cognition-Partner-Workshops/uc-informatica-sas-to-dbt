select
    key as "KEY",
    lead_co_mne as "LEAD_CO_MNE",
    branch_co_mne as "BRANCH_CO_MNE",
    mis_date as "MIS_DATE",
    id as "ID",
    description as "DESCRIPTION",
    short_name as "SHORT_NAME",
    o_created_by as "CREATED_BY",
    o_created_time as "CREATED_TIME",
    cast(null as varchar) as "UPDATED_BY",
    cast(null as timestamp_ntz) as "UPDATED_TIME",
    cast(null as varchar) as "ACTIVE_FLAG",
    cast(null as timestamp_ntz) as "START_DATE",
    cast(null as timestamp_ntz) as "END_DATE"
from {{ ref('int_m_demo_mapping2__sequence') }}
