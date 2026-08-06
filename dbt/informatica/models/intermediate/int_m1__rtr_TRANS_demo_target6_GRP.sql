{{ config(tags=['informatica', 's_m_demo_mapping1']) }}

/*
  RECOVERED: connected router output group demo_target6_GRP uses
  ACCT_TYP = 'SB'.
  RECOVERED: NULL ACCT_TYP makes both complementary router predicates
  UNKNOWN, so the row is routed to DEFAULT1 (XML lines 668-670), which has
  no connector and is intentionally discarded. Every non-NULL ACCT_TYP
  satisfies exactly one of the two connected predicates.
*/
select *
from {{ ref('int_m1__exp_TRANS1') }}
where ACCT_TYP = 'SB'
