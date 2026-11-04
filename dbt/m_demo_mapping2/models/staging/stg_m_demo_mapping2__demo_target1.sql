select
    cast("KEY" as number(38,0)) as DIM_KEY,
    cast(LEAD_CO_MNE as varchar) as LEAD_CO_MNE,
    cast(BRANCH_CO_MNE as varchar) as BRANCH_CO_MNE,
    cast(MIS_DATE as varchar) as MIS_DATE,
    cast(ID as varchar) as ID,
    cast(DESCRIPTION as varchar) as DESCRIPTION,
    cast(SHORT_NAME as varchar) as SHORT_NAME,
    cast(CREATED_BY as varchar) as CREATED_BY,
    cast(CREATED_TIME as timestamp_ntz(6)) as CREATED_TIME,
    cast(UPDATED_BY as varchar) as UPDATED_BY,
    cast(UPDATED_TIME as timestamp_ntz(6)) as UPDATED_TIME,
    cast(ACTIVE_FLAG as varchar) as ACTIVE_FLAG,
    cast(START_DATE as timestamp_ntz(6)) as START_DATE,
    cast(END_DATE as timestamp_ntz(6)) as END_DATE,
    cast(__SEED_ROW as number(38,0)) as SEED_ROW
from {{ source('infa_acctdim_src', 'DEMO_TARGET1') }}
