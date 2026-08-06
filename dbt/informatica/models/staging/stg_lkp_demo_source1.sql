{{ config(tags=['informatica', 's_m_demo_mapping1']) }}

/*
  RECOVERED: columns are direct lookup SOURCEFIELD pass-throughs from
  lkp_demo_source1 in wf_demo_mapping.XML.
  DECISION: SEED_ROW is a warehouse-portable ordinal generated from the
  legacy file's physical data-row order; physical file order is not otherwise
  representable in a warehouse table.
  RECOVERED: the "Use Last Value" lookup policy orders by SEED_ROW desc on
  ACCT_ID.
*/
with ranked as (
    select
        ACCT_ID,
        CUST_ID,
        FIRST_NM,
        LAST_NM,
        CUST_ADDR,
        CUST_PHN,
        CUST_EML_ADDR,
        AGE,
        DOB,
        CUST_TYP,
        SEED_ROW,
        row_number() over (
            partition by ACCT_ID
            order by SEED_ROW desc
        ) as __deterministic_row_order
    from {{ ref('lkp_demo_source1') }}
)
select
    ACCT_ID,
    CUST_ID,
    FIRST_NM,
    LAST_NM,
    CUST_ADDR,
    CUST_PHN,
    CUST_EML_ADDR,
    AGE,
    DOB,
    CUST_TYP
from ranked
where __deterministic_row_order = 1
