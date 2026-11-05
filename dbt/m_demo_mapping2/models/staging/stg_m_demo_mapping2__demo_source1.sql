select
    cast(LEAD_CO_MNE as varchar) as LEAD_CO_MNE,
    cast(BRANCH_CO_MNE as varchar) as BRANCH_CO_MNE,
    cast(MIS_DATE as varchar) as MIS_DATE,
    cast(ID as varchar) as ID,
    cast(DESCRIPTION as varchar) as DESCRIPTION,
    cast(SHORT_NAME as varchar) as SHORT_NAME
from {{ source('infa_acctdim_src', 'DEMO_SOURCE1') }}
