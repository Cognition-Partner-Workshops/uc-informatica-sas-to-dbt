select q.*, rtrim(q.acct_desc) as o_acct_desc,
    l1.first_nm, l2.crdt_score
from {{ ref('int_m_demo_mapping1__exp_trans') }} q
left join {{ ref('int_m_demo_mapping1__lkp_trans2') }} l1 on q.acct_id = l1.acct_id
left join {{ ref('int_m_demo_mapping1__lkp_trans3') }} l2 on q.cust_id = l2.cust_id
