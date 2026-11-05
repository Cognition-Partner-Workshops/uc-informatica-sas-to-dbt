select *, 280 + dense_rank() over (order by acct_id) as acct_key
from {{ ref('int_m_demo_mapping1__agg_trans') }}
