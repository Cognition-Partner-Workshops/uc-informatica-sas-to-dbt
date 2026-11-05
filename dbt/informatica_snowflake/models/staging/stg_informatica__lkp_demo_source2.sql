select
    cast("SEED_ROW" as number(38,0)) as seed_row,
    cast("CUST_ID" as number(38,0)) as cust_id,
    cast("CRDT_SCORE" as number(38,0)) as crdt_score,
    cast("MAX_CRDT_SCORE" as number(38,0)) as max_crdt_score,
    cast("MIN_CRDT_SCORE" as number(38,0)) as min_crdt_score,
    cast("MAX_CRDT_LMT" as number(38,0)) as max_crdt_lmt,
    cast("CURR_CRDT_BAL_AMT" as float) as curr_crdt_bal_amt,
    cast("AVG_INC_AMT" as float) as avg_inc_amt
from {{ source('infa_source', 'LKP_DEMO_SOURCE2') }}
