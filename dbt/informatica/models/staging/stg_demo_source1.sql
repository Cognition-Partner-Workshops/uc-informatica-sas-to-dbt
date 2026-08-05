select
    "LEAD_CO_MNE"   as lead_co_mne,
    "BRANCH_CO_MNE" as branch_co_mne,
    "MIS_DATE"      as mis_date,
    "ID"            as id,
    "DESCRIPTION"   as description,
    "SHORT_NAME"    as short_name
from {{ ref('demo_source1') }}
