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
from (
    select
        s.*,
        row_number() over (
            partition by ACCT_ID
            order by __seed_row desc
        ) as __rn
    from {{ ref('stg_m1_lkp_demo_source1') }} s
)
where __rn = 1
