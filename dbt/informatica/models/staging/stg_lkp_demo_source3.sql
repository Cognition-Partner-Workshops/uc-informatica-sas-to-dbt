{{ config(tags=['informatica', 's_m_demo_mapping1']) }}

/*
  RECOVERED: columns are direct lookup SOURCEFIELD pass-throughs from
  lkp_demo_source3 in wf_demo_mapping.XML.
  DECISION: SEED_ROW is a warehouse-portable ordinal generated from the
  legacy file's physical data-row order; physical file order is not otherwise
  representable in a warehouse table.
  RECOVERED: the "Use Last Value" lookup policy orders by SEED_ROW desc on
  ACCT_ID.
*/
with ranked as (
    select
        ACCT_ID,
        TX_TYPE_CD,
        TX_TYPE_DESC,
        SEED_ROW,
        row_number() over (
            partition by ACCT_ID
            order by SEED_ROW desc
        ) as __deterministic_row_order
    from {{ ref('lkp_demo_source3') }}
)
select
    ACCT_ID,
    TX_TYPE_CD,
    TX_TYPE_DESC
from ranked
where __deterministic_row_order = 1
