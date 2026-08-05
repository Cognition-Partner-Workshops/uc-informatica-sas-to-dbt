select *
from {{ source('informatica_m1', 'lkp_demo_source1') }}
