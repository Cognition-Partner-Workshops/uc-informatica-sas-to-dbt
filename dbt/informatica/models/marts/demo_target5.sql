select
    ACCT_ID,
    FIRST_NM,
    LAST_NM,
    BAL_AMT,
    CRDT_SCORE
from {{ ref('int_m1_rtr_trans') }}
where router_group = 'demo_target5_GRP'
