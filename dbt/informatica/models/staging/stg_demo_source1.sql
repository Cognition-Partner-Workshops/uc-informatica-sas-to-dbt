select
    LEAD_CO_MNE,
    BRANCH_CO_MNE,
    MIS_DATE,
    ID,
    DESCRIPTION,
    SHORT_NAME
from {{ source('legacy_informatica_m2', 'demo_source1') }}
