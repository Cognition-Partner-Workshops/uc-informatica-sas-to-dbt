-- rtr_TRANS group demo_target5_GRP: ACCT_TYP != 'SB'. A NULL ACCT_TYP satisfies
-- neither output group and falls to the unconnected DEFAULT1 group (dropped).
select
    ACCT_ID,
    FIRST_NM,
    LAST_NM,
    BAL_AMT,
    CRDT_SCORE
from {{ ref('exp_trans1') }}
where ACCT_TYP != 'SB'
order by ACCT_ID, BAL_AMT
