select
    key as "KEY",
    lead_co_mne as "LEAD_CO_MNE",
    branch_co_mne as "BRANCH_CO_MNE",
    mis_date as "MIS_DATE",
    id as "ID",
    description as "DESCRIPTION",
    short_name as "SHORT_NAME",
    cast(null as varchar) as "CREATED_BY",
    cast(null as timestamp_ntz) as "CREATED_TIME",
    o_updated_by as "UPDATED_BY",
    o_updated_time as "UPDATED_TIME",
    cast(null as varchar) as "ACTIVE_FLAG",
    cast(null as timestamp_ntz) as "START_DATE",
    cast(null as timestamp_ntz) as "END_DATE"
from {{ ref('int_m_demo_mapping2__update_strategy') }}
