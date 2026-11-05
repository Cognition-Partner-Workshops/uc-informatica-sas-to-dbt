select * exclude (key),
    56 + row_number() over (order by id) as key
from {{ ref('int_m_demo_mapping2__router') }}
where route = 'Insert'
