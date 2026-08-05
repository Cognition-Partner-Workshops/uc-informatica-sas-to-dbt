select *
from {{ ref('demo_target1_ins') }}
where UPDATED_BY is not null
   or UPDATED_TIME is not null
   or ACTIVE_FLAG is not null
   or START_DATE is not null
   or END_DATE is not null
