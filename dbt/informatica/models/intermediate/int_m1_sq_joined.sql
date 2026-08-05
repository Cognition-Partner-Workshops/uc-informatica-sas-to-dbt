-- m_demo_mapping1 sq_demo_source4 SQL override: inner join of demo_source3 and
-- demo_source4; SYSTIMESTAMP is pinned to the business date. The legacy
-- override also computed STRCMP(ACCT_STAT_CD, TX_TYPE_CD) into an unconnected
-- port, which is omitted here (documented no-op in the STM).
select
    s4.acct_id,
    s4.acct_typ,
    s4.acct_desc,
    s4.crdt_ln,
    cast('{{ var("business_date") }} 00:00:00' as timestamp) as cr8_dt,
    s4.clsr_dt,
    s4.acct_stat_cd,
    s3.tx_id,
    s3.last_nm,
    s3.tx_dttm,
    s3.tx_amt,
    s3.bal_amt,
    s3.cust_id
from {{ ref('stg_demo_source3') }} s3
inner join {{ ref('stg_demo_source4') }} s4
    on s3.acct_id = s4.acct_id
