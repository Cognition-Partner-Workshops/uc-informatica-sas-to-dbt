{{ config(tags=['informatica', 's_m_demo_mapping1']) }}

/*
  RECOVERED: columns are direct lookup SOURCEFIELD pass-throughs from
  lkp_demo_source1 in wf_demo_mapping.XML.
  DECISION: __deterministic_row_order uses descending lexicographic values
  instead of physical file order, which is unavailable in Snowflake.
  RECOVERED: the lookup policy is "Use Last Value" on ACCT_ID.
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
        row_number() over (
            partition by ACCT_ID
            order by
                CUST_ADDR desc nulls last,
                FIRST_NM desc nulls last,
                CUST_ID desc nulls last,
                LAST_NM desc nulls last,
                CUST_PHN desc nulls last,
                CUST_EML_ADDR desc nulls last,
                AGE desc nulls last,
                DOB desc nulls last,
                CUST_TYP desc nulls last
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
