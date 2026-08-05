select *
from {{ ref('demo_target1_upd') }}
where CREATED_BY is not null
   or CREATED_TIME is not null
   or ACTIVE_FLAG is not null
   or START_DATE is not null
   or END_DATE is not null
