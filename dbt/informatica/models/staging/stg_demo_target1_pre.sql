-- Pre-image of demo_target1: the SCD lookup table used by m_demo_mapping2
select
    "Key"           as key,
    "LEAD_CO_MNE"   as lead_co_mne,
    "BRANCH_CO_MNE" as branch_co_mne,
    "MIS_DATE"      as mis_date,
    "ID"            as id,
    "DESCRIPTION"   as description,
    "SHORT_NAME"    as short_name
from {{ ref('demo_target1') }}
