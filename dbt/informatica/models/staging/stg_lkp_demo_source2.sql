{{ config(tags=['informatica', 's_m_demo_mapping1']) }}

/*
  RECOVERED: columns are direct lookup SOURCEFIELD pass-throughs from
  lkp_demo_source2 in wf_demo_mapping.XML.
  DECISION: __deterministic_row_order uses descending lexicographic values
  instead of physical file order, which is unavailable in Snowflake.
  RECOVERED: the lookup policy is "Use Last Value" on CUST_ID.
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
        row_number() over (
            partition by CUST_ID
            order by
                CRDT_SCORE desc nulls last,
                MAX_CRDT_SCORE desc nulls last,
                MIN_CRDT_SCORE desc nulls last,
                MAX_CRDT_LMT desc nulls last,
                CURR_CRDT_BAL_AMT desc nulls last,
                AVG_INC_AMT desc nulls last
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
