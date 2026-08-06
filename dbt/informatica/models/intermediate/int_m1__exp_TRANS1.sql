{{ config(tags=['informatica', 's_m_demo_mapping1']) }}

/*
  RECOVERED: lkp_TRANS2 supplies FIRST_NM by ACCT_ID, and lkp_TRANS3
  supplies CRDT_SCORE by CUST_ID. Both are connected left lookups.
  RECOVERED: o_ACCT_DESC is RTRIM(ACCT_DESC); all other downstream ports
  pass through exp_TRANS values.
*/
select
    exp.ACCT_ID,
    exp.ACCT_TYP,
    exp.o_acc_trim,
    exp.o_crdt_trim,
    exp.o_ACCT_ID,
    exp.CR8_DT,
    exp.CLSR_DT,
    exp.ACCT_STAT_CD,
    exp.TX_ID,
    exp.LAST_NM,
    exp.TX_DTTM,
    exp.TX_AMT,
    exp.BAL_AMT,
    rtrim(exp.ACCT_DESC) as o_ACCT_DESC,
    lkp1.FIRST_NM,
    lkp2.CRDT_SCORE
from {{ ref('int_m1__exp_TRANS') }} exp
left join {{ ref('stg_lkp_demo_source1') }} lkp1
    on exp.ACCT_ID = lkp1.ACCT_ID
left join {{ ref('stg_lkp_demo_source2') }} lkp2
    on exp.CUST_ID = lkp2.CUST_ID
