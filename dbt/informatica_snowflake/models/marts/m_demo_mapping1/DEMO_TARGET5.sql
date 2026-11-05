select acct_id, first_nm, last_nm, bal_amt, crdt_score
from {{ ref('int_m_demo_mapping1__rtr_trans') }}
where router_group = 'demo_target5_GRP'
