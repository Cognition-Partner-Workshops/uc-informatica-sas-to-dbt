select *
from {{ ref('stg_informatica__lkp_demo_source3') }}
qualify row_number() over (partition by acct_id order by seed_row desc) = 1
