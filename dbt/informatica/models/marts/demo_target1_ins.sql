-- m_demo_mapping2 Insert router group -> demo_target1_INS. The surrogate Key
-- comes from SEQTRANS (current value 57, increment 1), assigned in source
-- (ID) order. Ports not connected on this instance load NULL.
select
    56 + row_number() over (order by id) as "Key",
    lead_co_mne    as "LEAD_CO_MNE",
    branch_co_mne  as "BRANCH_CO_MNE",
    mis_date       as "MIS_DATE",
    id             as "ID",
    description    as "DESCRIPTION",
    short_name     as "SHORT_NAME",
    o_created_by   as "CREATED_BY",
    o_created_time as "CREATED_TIME",
    cast(null as varchar)   as "UPDATED_BY",
    cast(null as timestamp) as "UPDATED_TIME",
    cast(null as varchar)   as "ACTIVE_FLAG",
    cast(null as timestamp) as "START_DATE",
    cast(null as timestamp) as "END_DATE"
from {{ ref('int_m2_change_detect') }}
where new_flag = 'Insert'
