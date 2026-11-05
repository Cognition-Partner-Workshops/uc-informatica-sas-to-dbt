-- rtr_TRANS group demo_target6_GRP (ACCT_TYP = 'SB') -> agg_TRANS -> demo_target6.
-- agg_TRANS groups by ACCT_ID with sorted input: TX_AMT = SUM(TX_AMT) and every
-- other port passes through from the last row of the group (highest TX_ID).
-- SEQ_GEN NEXTVAL (Current Value 281, Increment By 1) feeds ACCT_KEY per
-- aggregated row in ACCT_ID order.
with sb as (
    select *
    from {{ ref('exp_trans1') }}
    where ACCT_TYP = 'SB'
),

agg_trans as (
    select
        *,
        sum(TX_AMT) over (partition by ACCT_ID) as o_TX_AMT,
        row_number() over (partition by ACCT_ID order by TX_ID desc) as group_last_rn
    from sb
)

select
    ACCT_ID,
    o_acc_trim as ACCT_TYP,
    o_ACCT_DESC as ACCT_DESC,
    CR8_DT,
    o_crdt_trim as CRDT_LN,
    CLSR_DT,
    ACCT_STAT_CD,
    TX_ID,
    280 + row_number() over (order by ACCT_ID) as ACCT_KEY,
    TX_DTTM,
    o_TX_AMT as TX_AMT,
    o_ACCT_ID as TX_TYPE_CD
from agg_trans
where group_last_rn = 1
order by ACCT_ID
