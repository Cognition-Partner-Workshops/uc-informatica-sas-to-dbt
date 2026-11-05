select
    cast("LEAD_CO_MNE" as varchar) as lead_co_mne,
    cast("BRANCH_CO_MNE" as varchar) as branch_co_mne,
    cast("MIS_DATE" as varchar) as mis_date,
    cast("ID" as varchar) as id,
    cast("DESCRIPTION" as varchar) as description,
    cast("SHORT_NAME" as varchar) as short_name
from {{ source('infa_source', 'DEMO_SOURCE1') }}
