select
    cast("SEED_ROW" as number(38,0)) as seed_row,
    cast("ACCT_ID" as number(38,0)) as acct_id,
    cast("CUST_ID" as number(38,0)) as cust_id,
    cast("FIRST_NM" as varchar) as first_nm,
    cast("LAST_NM" as varchar) as last_nm,
    cast("CUST_ADDR" as varchar) as cust_addr,
    cast("CUST_PHN" as varchar) as cust_phn,
    cast("CUST_EML_ADDR" as varchar) as cust_eml_addr,
    cast("AGE" as varchar) as age,
    cast("DOB" as varchar) as dob,
    cast("CUST_TYP" as varchar) as cust_typ
from {{ source('infa_source', 'LKP_DEMO_SOURCE1') }}
