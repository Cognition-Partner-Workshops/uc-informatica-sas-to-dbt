select 56 + row_number() over (order by ID, SEED_ROW) as "Key",
       LEAD_CO_MNE, BRANCH_CO_MNE, MIS_DATE, ID, DESCRIPTION, SHORT_NAME,
       'IDWUSER' as CREATED_BY,
       timestamp '2024-01-31 00:00:00' as CREATED_TIME,
       cast(null as varchar) as UPDATED_BY,
       cast(null as timestamp) as UPDATED_TIME,
       cast(null as varchar) as ACTIVE_FLAG,
       cast(null as timestamp) as START_DATE,
       cast(null as timestamp) as END_DATE
from {{ ref('m2_lookup') }}
where lookup_key is null
