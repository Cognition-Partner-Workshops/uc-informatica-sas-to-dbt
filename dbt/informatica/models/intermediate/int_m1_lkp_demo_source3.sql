select
    ACCT_ID,
    TX_TYPE_CD,
    TX_TYPE_DESC
from (
    select
        s.*,
        row_number() over (
            partition by ACCT_ID
            order by __seed_row desc
        ) as __rn
    from {{ ref('stg_m1_lkp_demo_source3') }} s
)
where __rn = 1
