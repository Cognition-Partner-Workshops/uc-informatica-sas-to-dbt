-- m_demo_mapping2 Update router group -> UPDTRANS (DD_UPDATE) ->
-- demo_target1_UPD. Because md5_src is always NULL (see
-- int_m2_change_detect), changed_flag is never 'Update' and this instance
-- receives zero rows — preserved faithfully from the legacy mapping.
select
    lookup_key     as "Key",
    lead_co_mne    as "LEAD_CO_MNE",
    branch_co_mne  as "BRANCH_CO_MNE",
    mis_date       as "MIS_DATE",
    id             as "ID",
    description    as "DESCRIPTION",
    short_name     as "SHORT_NAME",
    cast(null as varchar)   as "CREATED_BY",
    cast(null as timestamp) as "CREATED_TIME",
    o_updated_by   as "UPDATED_BY",
    o_updated_time as "UPDATED_TIME",
    cast(null as varchar)   as "ACTIVE_FLAG",
    cast(null as timestamp) as "START_DATE",
    cast(null as timestamp) as "END_DATE"
from {{ ref('int_m2_change_detect') }}
where changed_flag = 'Update'
