select
    s4.ACCT_ID,
    s4.ACCT_TYP,
    s4.ACCT_DESC,
    s4.CRDT_LN,
    cast('{{ var("m1_business_date", "2024-01-31") }} 00:00:00' as timestamp) as CR8_DT,
    s4.CLSR_DT,
    s4.ACCT_STAT_CD,
    s3.TX_ID,
    s3.LAST_NM,
    s3.TX_DTTM,
    s3.TX_AMT,
    s3.BAL_AMT,
    s3.CUST_ID
    -- The SQL override's STRCMP(...) is the unconnected 14th TX_TYPE_CD
    -- expression and is intentionally not carried downstream.
from {{ ref('stg_m1_demo_source3') }} s3
inner join {{ ref('stg_m1_demo_source4') }} s4
    on s3.ACCT_ID = s4.ACCT_ID
