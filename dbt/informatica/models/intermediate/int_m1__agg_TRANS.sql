{{ config(tags=['informatica', 's_m_demo_mapping1']) }}

/*
  RECOVERED: agg_TRANS groups by ACCT_ID and sums TX_AMT into o_TX_AMT.
  DECISION: aggregator pass-through ports use the row with highest TX_ID
  per ACCT_ID to represent Informatica's LAST row. The rejected alternative
  was a physical-file-order ordinal on demo_source3 (no SEED_ROW exists
  there; TX_ID ascending coincides with physical order in this input, and
  the SQL override only orders by ACCT_ID).
*/
with ranked as (
    select
        ACCT_ID,
        o_ACCT_DESC,
        o_acc_trim,
        o_crdt_trim,
        CLSR_DT,
        TX_ID,
        ACCT_STAT_CD,
        TX_DTTM,
        CR8_DT,
        o_ACCT_ID,
        TX_AMT,
        row_number() over (
            partition by ACCT_ID
            order by TX_ID desc
        ) as __last_row
    from {{ ref('int_m1__rtr_TRANS_demo_target6_GRP') }}
),
totals as (
    select
        ACCT_ID,
        sum(TX_AMT) as o_TX_AMT
    from ranked
    group by ACCT_ID
)
select
    latest.ACCT_ID,
    latest.o_ACCT_DESC,
    latest.o_acc_trim,
    latest.o_crdt_trim,
    latest.CLSR_DT,
    latest.TX_ID,
    latest.ACCT_STAT_CD,
    latest.TX_DTTM,
    latest.CR8_DT,
    latest.o_ACCT_ID,
    totals.o_TX_AMT
from ranked latest
inner join totals
    on latest.ACCT_ID = totals.ACCT_ID
where latest.__last_row = 1
