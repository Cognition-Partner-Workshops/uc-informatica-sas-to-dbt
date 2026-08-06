{{ config(tags=['informatica', 's_m_demo_mapping1']) }}

/*
  RECOVERED: columns are direct lookup SOURCEFIELD pass-throughs from
  lkp_demo_source2 in wf_demo_mapping.XML.
  DECISION: SEED_ROW is a warehouse-portable ordinal generated from the
  legacy file's physical data-row order; physical file order is not otherwise
  representable in a warehouse table.
  RECOVERED: the "Use Last Value" lookup policy orders by SEED_ROW desc on
  CUST_ID.
*/
with ranked as (
    select
        CUST_ID,
        CRDT_SCORE,
        MAX_CRDT_SCORE,
        MIN_CRDT_SCORE,
        MAX_CRDT_LMT,
        CURR_CRDT_BAL_AMT,
        AVG_INC_AMT,
        SEED_ROW,
        row_number() over (
            partition by CUST_ID
            order by SEED_ROW desc
        ) as __deterministic_row_order
    from {{ ref('lkp_demo_source2') }}
)
select
    CUST_ID,
    CRDT_SCORE,
    MAX_CRDT_SCORE,
    MIN_CRDT_SCORE,
    MAX_CRDT_LMT,
    CURR_CRDT_BAL_AMT,
    AVG_INC_AMT
from ranked
where __deterministic_row_order = 1
