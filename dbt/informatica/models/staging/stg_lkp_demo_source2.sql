select
    "CUST_ID"    as cust_id,
    "CRDT_SCORE" as crdt_score
from {{ ref('lkp_demo_source2') }}
