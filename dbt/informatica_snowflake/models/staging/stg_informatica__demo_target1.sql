select
    cast("SEED_ROW" as number(38,0)) as seed_row,
    cast("KEY" as float) as key,
    cast("LEAD_CO_MNE" as varchar) as lead_co_mne,
    cast("BRANCH_CO_MNE" as varchar) as branch_co_mne,
    cast("MIS_DATE" as varchar) as mis_date,
    cast("ID" as varchar) as id,
    cast("DESCRIPTION" as varchar) as description,
    cast("SHORT_NAME" as varchar) as short_name,
    cast("CREATED_BY" as varchar) as created_by,
    cast("CREATED_TIME" as timestamp_ntz) as created_time,
    cast("UPDATED_BY" as varchar) as updated_by,
    cast("UPDATED_TIME" as timestamp_ntz) as updated_time,
    cast("ACTIVE_FLAG" as varchar) as active_flag,
    cast("START_DATE" as timestamp_ntz) as start_date,
    cast("END_DATE" as timestamp_ntz) as end_date
from {{ source('infa_source', 'DEMO_TARGET1') }}
