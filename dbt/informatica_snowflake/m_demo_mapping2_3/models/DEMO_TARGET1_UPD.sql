select lookup_key as "Key",
       LEAD_CO_MNE, BRANCH_CO_MNE, MIS_DATE, ID, DESCRIPTION, SHORT_NAME,
       cast(null as varchar) as CREATED_BY,
       cast(null as timestamp) as CREATED_TIME,
       'IDWUSER' as UPDATED_BY,
       timestamp '2024-01-31 00:00:00' as UPDATED_TIME,
       cast(null as varchar) as ACTIVE_FLAG,
       cast(null as timestamp) as START_DATE,
       cast(null as timestamp) as END_DATE
from {{ ref('m2_lookup') }}
where lookup_key is not null
