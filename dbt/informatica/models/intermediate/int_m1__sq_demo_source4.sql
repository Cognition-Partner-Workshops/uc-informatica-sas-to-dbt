{{ config(tags=['informatica', 's_m_demo_mapping1']) }}

/*
  RECOVERED: Source Qualifier override joins stg_demo_source3 to
  stg_demo_source4 on ACCT_ID and binds its select list positionally.
  RECOVERED: position 5 binds CR8_DT to SYSTIMESTAMP, not source CR8_DT.
  RECOVERED: position 14 is the dead TX_TYPE_CD port (STRCMP of account
  status and transaction type); it has no outgoing connector and is omitted.
  RECOVERED: ORDER BY s4.ACCT_ID supplies the sorted input for agg_TRANS.
*/
select
    s4.ACCT_ID,
    s4.ACCT_TYP,
    s4.ACCT_DESC,
    s4.CRDT_LN,
    {{ business_timestamp() }} as CR8_DT,
    s4.CLSR_DT,
    s4.ACCT_STAT_CD,
    s3.TX_ID,
    s3.LAST_NM,
    s3.TX_DTTM,
    s3.TX_AMT,
    s3.BAL_AMT,
    s3.CUST_ID
from {{ ref('stg_demo_source3') }} s3
inner join {{ ref('stg_demo_source4') }} s4
    on s3.ACCT_ID = s4.ACCT_ID
order by s4.ACCT_ID
