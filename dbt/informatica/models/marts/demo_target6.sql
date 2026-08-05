with grouped as (
    select
        r.*,
        row_number() over (
            partition by r.ACCT_ID
            order by r.TX_ID desc
        ) as __pass_through_rank,
        sum(r.TX_AMT) over (
            partition by r.ACCT_ID
        ) as __sum_tx_amt,
        dense_rank() over (
            order by r.ACCT_ID
        ) as __acct_rank
    from {{ ref('int_m1_rtr_trans') }} r
    where r.router_group = 'demo_target6_GRP'
)
select
    ACCT_ID,
    o_acc_trim as ACCT_TYP,
    o_ACCT_DESC as ACCT_DESC,
    CR8_DT,
    cast(o_crdt_trim as bigint) as CRDT_LN,
    CLSR_DT,
    ACCT_STAT_CD,
    TX_ID,
    280 + __acct_rank as ACCT_KEY,
    TX_DTTM,
    __sum_tx_amt as TX_AMT,
    o_ACCT_ID as TX_TYPE_CD
from grouped
where __pass_through_rank = 1
