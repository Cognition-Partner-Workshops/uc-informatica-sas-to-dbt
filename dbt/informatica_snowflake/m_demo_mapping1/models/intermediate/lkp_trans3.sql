-- lkp_TRANS3: lkp_demo_source2, condition CUST_ID = IN_CUST_ID, Use Last Value.
-- Only CRDT_SCORE is connected downstream.
{{ lookup_last_value(source('infa_src', 'LKP_DEMO_SOURCE2'), 'CUST_ID') }}
