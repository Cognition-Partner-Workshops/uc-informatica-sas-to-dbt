select
    q.*,
    rtrim(q.ACCT_TYP) as o_acc_trim,
    ltrim(q.CRDT_LN) as o_crdt_trim,
    rtrim(q.ACCT_DESC) as o_ACCT_DESC,
    l3.TX_TYPE_CD as o_ACCT_ID,
    l1.FIRST_NM,
    l2.CRDT_SCORE
from {{ ref('int_m1_sq_demo_source4') }} q
left join {{ ref('int_m1_lkp_demo_source3') }} l3
    on l3.ACCT_ID = q.ACCT_ID
left join {{ ref('int_m1_lkp_demo_source1') }} l1
    on l1.ACCT_ID = q.ACCT_ID
left join {{ ref('int_m1_lkp_demo_source2') }} l2
    on l2.CUST_ID = q.CUST_ID
