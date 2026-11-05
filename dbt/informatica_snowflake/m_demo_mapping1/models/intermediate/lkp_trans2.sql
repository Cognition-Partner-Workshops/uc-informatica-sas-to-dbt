-- lkp_TRANS2: lkp_demo_source1, condition ACCT_ID = IN_ACCT_ID, Use Last Value.
-- Only FIRST_NM is connected downstream.
{{ lookup_last_value(source('infa_src', 'LKP_DEMO_SOURCE1'), 'ACCT_ID') }}
