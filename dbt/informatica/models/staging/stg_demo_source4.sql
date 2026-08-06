{{ config(tags=['informatica', 's_m_demo_mapping1']) }}

/*
  RECOVERED: all columns are direct source-field pass-throughs from the
  demo_source4 SOURCE and SOURCEFIELD elements in wf_demo_mapping.XML.
*/
select
    ACCT_ID,
    ACCT_TYP,
    ACCT_DESC,
    CRDT_LN,
    CR8_DT,
    CLSR_DT,
    ACCT_STAT_CD
from {{ ref('demo_source4') }}
