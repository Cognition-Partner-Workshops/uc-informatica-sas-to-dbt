-- rtr_TRANS: NULL ACCT_TYP (ACCT_ID 1005) falls to the unconnected DEFAULT1 group.
select ACCT_ID from {{ ref('DEMO_TARGET5') }} where ACCT_ID = 1005
union all
select ACCT_ID from {{ ref('DEMO_TARGET6') }} where ACCT_ID = 1005
