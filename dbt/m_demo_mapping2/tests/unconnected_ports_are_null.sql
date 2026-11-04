select ID from {{ ref('DEMO_TARGET1_INS') }}
where UPDATED_BY is not null or UPDATED_TIME is not null
   or ACTIVE_FLAG is not null or START_DATE is not null or END_DATE is not null
union all
select ID from {{ ref('DEMO_TARGET1_UPD') }}
where CREATED_BY is not null or CREATED_TIME is not null
   or ACTIVE_FLAG is not null or START_DATE is not null or END_DATE is not null
