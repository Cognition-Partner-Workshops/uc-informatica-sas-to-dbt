select *
from {{ ref('stg_informatica__lkp_demo_source2') }}
qualify row_number() over (partition by cust_id order by seed_row desc) = 1
