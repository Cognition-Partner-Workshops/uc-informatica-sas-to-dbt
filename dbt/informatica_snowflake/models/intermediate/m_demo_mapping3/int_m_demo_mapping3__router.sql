select *,
    case when social_security_number is null then 'NEWGROUP1' else 'NEWGROUP2' end as route
from {{ ref('int_m_demo_mapping3__expression') }}
