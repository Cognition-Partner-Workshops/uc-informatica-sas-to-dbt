{{ config(tags=['informatica', 's_m_demo_mapping1']) }}

/*
  RECOVERED: target columns connect to agg_TRANS ports as listed below.
  DECISION: SEQ_GEN current value 281 means emitted keys begin at 281;
  dense_rank ordered by ACCT_ID represents the recovered sorted input order.
*/
select
    ACCT_ID,
    o_acc_trim as ACCT_TYP,
    o_ACCT_DESC as ACCT_DESC,
    CR8_DT,
    o_crdt_trim as CRDT_LN,
    CLSR_DT,
    ACCT_STAT_CD,
    TX_ID,
    280 + dense_rank() over (order by ACCT_ID) as ACCT_KEY,
    TX_DTTM,
    o_TX_AMT as TX_AMT,
    o_ACCT_ID as TX_TYPE_CD
from {{ ref('int_m1__agg_TRANS') }}
