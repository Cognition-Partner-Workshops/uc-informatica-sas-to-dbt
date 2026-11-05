-- exp_TRANS (trims + lkp_TRANS1 return) and exp_TRANS1 (adds lkp_TRANS2.FIRST_NM
-- and lkp_TRANS3.CRDT_SCORE). Connected lookups are left outer: no match -> NULL.
-- This is the single input group of rtr_TRANS.
select
    sq.ACCT_ID,
    sq.ACCT_TYP,
    sq.ACCT_DESC,
    sq.CR8_DT,
    sq.CLSR_DT,
    sq.ACCT_STAT_CD,
    sq.TX_ID,
    sq.LAST_NM,
    sq.TX_DTTM,
    sq.TX_AMT,
    sq.BAL_AMT,
    sq.CUST_ID,
    rtrim(sq.ACCT_TYP) as o_acc_trim,
    ltrim(sq.CRDT_LN) as o_crdt_trim,
    l1.TX_TYPE_CD as o_ACCT_ID,
    rtrim(sq.ACCT_DESC) as o_ACCT_DESC,
    l2.FIRST_NM,
    l3.CRDT_SCORE
from {{ ref('sq_demo_source4') }} as sq
left join {{ ref('lkp_trans1') }} as l1
    on l1.ACCT_ID = sq.ACCT_ID
left join {{ ref('lkp_trans2') }} as l2
    on l2.ACCT_ID = sq.ACCT_ID
left join {{ ref('lkp_trans3') }} as l3
    on l3.CUST_ID = sq.CUST_ID
