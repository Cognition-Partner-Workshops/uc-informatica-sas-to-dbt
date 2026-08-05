with update_keys as (
    select Key
    from {{ ref('demo_target1_upd') }}
),
preexisting as (
    select
        Key,
        CREATED_BY,
        CREATED_TIME,
        ACTIVE_FLAG,
        START_DATE,
        END_DATE
    from {{ ref('stg_demo_target1_pre') }}
)
select target.Key
from {{ ref('demo_target1') }} as target
inner join update_keys
    on update_keys.Key = target.Key
inner join preexisting
    on preexisting.Key = target.Key
where target.CREATED_BY is distinct from preexisting.CREATED_BY
   or target.CREATED_TIME is distinct from preexisting.CREATED_TIME
   or target.ACTIVE_FLAG is distinct from preexisting.ACTIVE_FLAG
   or target.START_DATE is distinct from preexisting.START_DATE
   or target.END_DATE is distinct from preexisting.END_DATE
