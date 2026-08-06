{{ config(tags=['informatica', 's_m_demo_mapping1']) }}

/*
  RECOVERED: target receives one row per connected demo_target5 router row.
  FIRST_NM and CRDT_SCORE come from connected lkp_TRANS2 and lkp_TRANS3;
  LAST_NM and BAL_AMT pass through from demo_source3 via the SQ.
*/
select
    ACCT_ID,
    FIRST_NM,
    LAST_NM,
    BAL_AMT,
    CRDT_SCORE
from {{ ref('int_m1__rtr_TRANS_demo_target5_GRP') }}
