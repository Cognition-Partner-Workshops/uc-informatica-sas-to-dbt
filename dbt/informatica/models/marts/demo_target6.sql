-- m_demo_mapping1 rtr_TRANS demo_target6_GRP (ACCT_TYP = 'SB') -> agg_TRANS ->
-- demo_target6. The aggregator groups by ACCT_ID, sums TX_AMT and returns the
-- last row per group (deterministically: highest TX_ID). ACCT_KEY comes from
-- SEQ_GEN (current value 281, increment 1) assigned in ACCT_ID order.
with sb as (
    select
        *,
        row_number() over (partition by acct_id order by tx_id desc) as rn,
        sum(tx_amt) over (partition by acct_id) as sum_tx_amt
    from {{ ref('int_m1_enriched') }}
    where acct_typ = 'SB'
)

select
    acct_id      as "ACCT_ID",
    o_acc_trim   as "ACCT_TYP",
    o_acct_desc  as "ACCT_DESC",
    cr8_dt       as "CR8_DT",
    cast(o_crdt_trim as bigint) as "CRDT_LN",
    clsr_dt      as "CLSR_DT",
    acct_stat_cd as "ACCT_STAT_CD",
    tx_id        as "TX_ID",
    280 + row_number() over (order by acct_id) as "ACCT_KEY",
    tx_dttm      as "TX_DTTM",
    sum_tx_amt   as "TX_AMT",
    o_acct_id    as "TX_TYPE_CD"
from sb
where rn = 1
