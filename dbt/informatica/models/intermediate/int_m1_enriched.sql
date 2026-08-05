-- m_demo_mapping1 exp_TRANS / exp_TRANS1 with the three connected lookups
-- (lkp_TRANS1 -> lkp_demo_source3, lkp_TRANS2 -> lkp_demo_source1,
--  lkp_TRANS3 -> lkp_demo_source2)
select
    q.acct_id,
    q.acct_typ,
    q.cr8_dt,
    q.clsr_dt,
    q.acct_stat_cd,
    q.tx_id,
    q.last_nm,
    q.tx_dttm,
    q.tx_amt,
    q.bal_amt,
    q.cust_id,
    rtrim(q.acct_typ)  as o_acc_trim,
    ltrim(q.crdt_ln)   as o_crdt_trim,
    l3.tx_type_cd      as o_acct_id,
    rtrim(q.acct_desc) as o_acct_desc,
    l1.first_nm        as first_nm,
    l2.crdt_score      as crdt_score
from {{ ref('int_m1_sq_joined') }} q
left join {{ ref('stg_lkp_demo_source3') }} l3 on l3.acct_id = q.acct_id
left join {{ ref('stg_lkp_demo_source1') }} l1 on l1.acct_id = q.acct_id
left join {{ ref('stg_lkp_demo_source2') }} l2 on l2.cust_id = q.cust_id
