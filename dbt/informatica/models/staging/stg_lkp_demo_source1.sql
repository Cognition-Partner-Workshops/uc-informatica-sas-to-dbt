select
    "ACCT_ID"  as acct_id,
    "CUST_ID"  as cust_id,
    "FIRST_NM" as first_nm,
    "LAST_NM"  as last_nm
from {{ ref('lkp_demo_source1') }}
