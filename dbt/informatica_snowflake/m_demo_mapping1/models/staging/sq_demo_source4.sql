-- sq_demo_source4 SQL override: demo_source3 INNER JOIN demo_source4 on ACCT_ID.
-- SYSTIMESTAMP is bound positionally to the CR8_DT port and pinned to the
-- business date. The trailing STRCMP(ACCT_STAT_CD, TX_TYPE_CD) column binds to
-- the TX_TYPE_CD port, which is never connected downstream, so it is dropped.
select
    s4.ACCT_ID,
    s4.ACCT_TYP,
    s4.ACCT_DESC,
    s4.CRDT_LN,
    cast('{{ var("business_date") }} 00:00:00' as timestamp) as CR8_DT,
    s4.CLSR_DT,
    s4.ACCT_STAT_CD,
    s3.TX_ID,
    s3.LAST_NM,
    s3.TX_DTTM,
    s3.TX_AMT,
    s3.BAL_AMT,
    s3.CUST_ID
from {{ source('infa_src', 'DEMO_SOURCE3') }} as s3
inner join {{ source('infa_src', 'DEMO_SOURCE4') }} as s4
    on s3.ACCT_ID = s4.ACCT_ID
