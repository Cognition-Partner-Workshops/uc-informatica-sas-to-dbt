-- lkp_TRANS1: lkp_demo_source3, condition ACCT_ID = IN_ACCT_ID, Use Last Value.
-- Return port TX_TYPE_CD.
{{ lookup_last_value(source('infa_src', 'LKP_DEMO_SOURCE3'), 'ACCT_ID') }}
