{{ config(tags=['informatica', 's_m_demo_mapping1']) }}

/*
  RECOVERED: connected router output group demo_target6_GRP uses
  ACCT_TYP = 'SB'.
  RECOVERED: NULL ACCT_TYP makes this predicate UNKNOWN and is routed to
  DEFAULT1, which has no connector; DEFAULT1 is intentionally discarded.
*/
select *
from {{ ref('int_m1__exp_TRANS1') }}
where ACCT_TYP = 'SB'
