select *,
    case when new_flag = 'Insert' then 'Insert'
         when changed_flag = 'Update' then 'Update' end as route
from {{ ref('int_m_demo_mapping2__expression') }}
