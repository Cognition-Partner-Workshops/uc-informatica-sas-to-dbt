select u.ID
from {{ ref('DEMO_TARGET1_UPD') }} u
join {{ ref('int_m_demo_mapping2__lkptrans') }} p on u.ID = p.ID
where u."KEY" != p.DIM_KEY
