{{ config(tags=['informatica', 's_m_demo_mapping1']) }}

/*
  RECOVERED: lkp_TRANS2 supplies FIRST_NM by ACCT_ID, and lkp_TRANS3
  supplies CRDT_SCORE by CUST_ID. Both are connected left lookups.
  RECOVERED: o_ACCT_DESC is RTRIM(ACCT_DESC); all other downstream ports
  pass through exp_TRANS values.
*/
select
    e1.ACCT_ID,
    e1.ACCT_TYP,
    e1.o_acc_trim,
    e1.o_crdt_trim,
    e1.o_ACCT_ID,
    e1.CR8_DT,
    e1.CLSR_DT,
    e1.ACCT_STAT_CD,
    e1.TX_ID,
    e1.LAST_NM,
    e1.TX_DTTM,
    e1.TX_AMT,
    e1.BAL_AMT,
    rtrim(e1.ACCT_DESC) as o_ACCT_DESC,
    lkp1.FIRST_NM,
    lkp2.CRDT_SCORE
from {{ ref('int_m1__exp_TRANS') }} e1
left join {{ ref('stg_lkp_demo_source1') }} lkp1
    on e1.ACCT_ID = lkp1.ACCT_ID
left join {{ ref('stg_lkp_demo_source2') }} lkp2
    on e1.CUST_ID = lkp2.CUST_ID
