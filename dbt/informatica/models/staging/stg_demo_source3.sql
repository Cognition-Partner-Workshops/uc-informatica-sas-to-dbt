select
    "TX_ID"      as tx_id,
    "ACCT_ID"    as acct_id,
    "FIRST_NM"   as first_nm,
    "LAST_NM"    as last_nm,
    "TX_DTTM"    as tx_dttm,
    "TX_AMT"     as tx_amt,
    "TX_TYPE_CD" as tx_type_cd,
    "BAL_AMT"    as bal_amt,
    "TX_DESC"    as tx_desc,
    "CRDT_SCORE" as crdt_score,
    "CUST_ID"    as cust_id
from {{ ref('demo_source3') }}
