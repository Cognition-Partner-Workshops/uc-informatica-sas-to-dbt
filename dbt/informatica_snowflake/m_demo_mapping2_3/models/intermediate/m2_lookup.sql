with pre_state as (
    select *, row_number() over (
        partition by ID order by cast("Key" as double) desc, SEED_ROW desc
    ) as lookup_rank
    from {{ source('infa_m23', 'demo_target1') }}
)
select s.* exclude (SEED_ROW), s.SEED_ROW,
       cast(p."Key" as double) as lookup_key
from {{ source('infa_m23', 'demo_source1') }} s
left join pre_state p on s.ID = p.ID and p.lookup_rank = 1
