select
    CUST_ID,
    CRDT_SCORE,
    MAX_CRDT_SCORE,
    MIN_CRDT_SCORE,
    MAX_CRDT_LMT,
    CURR_CRDT_BAL_AMT,
    AVG_INC_AMT
from (
    select
        s.*,
        row_number() over (
            partition by CUST_ID
            order by __seed_row desc
        ) as __rn
    from {{ ref('stg_m1_lkp_demo_source2') }} s
)
where __rn = 1
