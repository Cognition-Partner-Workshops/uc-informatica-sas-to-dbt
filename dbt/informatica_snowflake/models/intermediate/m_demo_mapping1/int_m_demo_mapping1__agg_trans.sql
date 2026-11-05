select *, sum(tx_amt) over (partition by acct_id) as o_tx_amt
from {{ ref('int_m_demo_mapping1__rtr_trans') }}
where router_group = 'demo_target6_GRP'
qualify row_number() over (partition by acct_id order by tx_id desc) = 1
