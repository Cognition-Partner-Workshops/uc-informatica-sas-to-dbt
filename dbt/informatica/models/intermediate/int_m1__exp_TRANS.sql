{{ config(tags=['informatica', 's_m_demo_mapping1']) }}

/*
  RECOVERED: exp_TRANS trims ACCT_TYP with RTRIM and CRDT_LN with LTRIM.
  RECOVERED: unconnected lkp_TRANS1 returns lkp_demo_source3.TX_TYPE_CD
  on ACCT_ID; the result is named o_ACCT_ID despite that misleading name.
  RECOVERED: remaining ports pass through the SQ output.
*/
select
    sq.ACCT_ID,
    sq.ACCT_TYP,
    rtrim(sq.ACCT_TYP) as o_acc_trim,
    ltrim(sq.CRDT_LN) as o_crdt_trim,
    lkp3.TX_TYPE_CD as o_ACCT_ID,
    sq.CR8_DT,
    sq.CLSR_DT,
    sq.ACCT_STAT_CD,
    sq.TX_ID,
    sq.LAST_NM,
    sq.TX_DTTM,
    sq.TX_AMT,
    sq.BAL_AMT,
    sq.ACCT_DESC,
    sq.CUST_ID
from {{ ref('int_m1__sq_demo_source4') }} sq
left join {{ ref('stg_lkp_demo_source3') }} lkp3
    on sq.ACCT_ID = lkp3.ACCT_ID
