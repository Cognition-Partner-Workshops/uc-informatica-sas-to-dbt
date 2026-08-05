select
    "ACCT_ID"    as acct_id,
    "TX_TYPE_CD" as tx_type_cd
from {{ ref('lkp_demo_source3') }}
