select *
from {{ ref('stg_informatica__demo_target1') }}
qualify row_number() over (partition by id order by key desc nulls last, seed_row desc) = 1
