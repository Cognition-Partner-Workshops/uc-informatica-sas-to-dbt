select
    cast("TX_ID" as number(38,0)) as tx_id,
    cast("ACCT_ID" as number(38,0)) as acct_id,
    cast("FIRST_NM" as varchar) as first_nm,
    cast("LAST_NM" as varchar) as last_nm,
    cast("TX_DTTM" as timestamp_ntz) as tx_dttm,
    cast("TX_AMT" as float) as tx_amt,
    cast("TX_TYPE_CD" as varchar) as tx_type_cd,
    cast("BAL_AMT" as float) as bal_amt,
    cast("TX_DESC" as varchar) as tx_desc,
    cast("CRDT_SCORE" as number(38,0)) as crdt_score,
    cast("CUST_ID" as number(38,0)) as cust_id
from {{ source('infa_source', 'DEMO_SOURCE3') }}
