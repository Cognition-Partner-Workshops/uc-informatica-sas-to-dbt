{{ config(tags=['informatica', 's_m_demo_mapping1']) }}

/*
  RECOVERED: all columns are direct source-field pass-throughs from the
  demo_source3 SOURCE and SOURCEFIELD elements in wf_demo_mapping.XML.
*/
select
    TX_ID,
    ACCT_ID,
    FIRST_NM,
    LAST_NM,
    TX_DTTM,
    TX_AMT,
    TX_TYPE_CD,
    BAL_AMT,
    TX_DESC,
    CRDT_SCORE,
    CUST_ID
from {{ ref('demo_source3') }}
