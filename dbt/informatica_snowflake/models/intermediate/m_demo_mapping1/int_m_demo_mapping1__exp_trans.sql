select q.*, rtrim(q.acct_typ) as o_acc_trim,
    ltrim(q.crdt_ln) as o_crdt_trim, l.tx_type_cd as o_acct_id
from {{ ref('int_m_demo_mapping1__sq_demo_source4') }} q
left join {{ ref('int_m_demo_mapping1__lkp_trans1') }} l on q.acct_id = l.acct_id
