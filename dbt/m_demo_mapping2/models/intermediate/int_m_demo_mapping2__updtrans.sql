select *, 'DD_UPDATE' as UPDATE_STRATEGY
from {{ ref('int_m_demo_mapping2__rtrtrans_update') }}
