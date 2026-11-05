select *
from {{ ref('stg_informatica__demo_source2') }}
where member_type_code is not null
