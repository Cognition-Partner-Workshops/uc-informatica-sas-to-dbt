{{ config(tags=['informatica', 's_m_demo_mapping1']) }}

/*
  RECOVERED: columns are direct lookup SOURCEFIELD pass-throughs from
  lkp_demo_source3 in wf_demo_mapping.XML.
  DECISION: __deterministic_row_order uses descending lexicographic values
  instead of physical file order, which is unavailable in Snowflake.
  RECOVERED: the lookup policy is "Use Last Value" on ACCT_ID.
*/
with ranked as (
    select
        ACCT_ID,
        TX_TYPE_CD,
        TX_TYPE_DESC,
        row_number() over (
            partition by ACCT_ID
            order by
                TX_TYPE_DESC desc nulls last,
                TX_TYPE_CD desc nulls last
        ) as __deterministic_row_order
    from {{ ref('lkp_demo_source3') }}
)
select
    ACCT_ID,
    TX_TYPE_CD,
    TX_TYPE_DESC
from ranked
where __deterministic_row_order = 1
