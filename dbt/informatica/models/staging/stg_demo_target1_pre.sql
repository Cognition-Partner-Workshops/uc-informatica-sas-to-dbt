select
    cast(Key as double) as Key,
    LEAD_CO_MNE,
    BRANCH_CO_MNE,
    MIS_DATE,
    ID,
    DESCRIPTION,
    SHORT_NAME,
    CREATED_BY,
    CREATED_TIME,
    UPDATED_BY,
    UPDATED_TIME,
    ACTIVE_FLAG,
    START_DATE,
    END_DATE
from {{ source('legacy_informatica_m2', 'demo_target1_pre') }}
