select *
from {{ ref('int_m_demo_mapping2__router') }}
where route = 'Update'
