select
    cast("SEED_ROW" as number(38,0)) as seed_row,
    cast("ACCT_ID" as number(38,0)) as acct_id,
    cast("TX_TYPE_CD" as varchar) as tx_type_cd,
    cast("TX_TYPE_DESC" as varchar) as tx_type_desc
from {{ source('infa_source', 'LKP_DEMO_SOURCE3') }}
