select
    "PRODUCT_ID" as product_id,
    "PRODUCT_NM" as product_nm,
    "PRODUCT_NO" as product_no,
    "COLOR"      as color,
    "STD_COST"   as std_cost,
    "LIST_PRICE" as list_price,
    "SELL_ST_DT" as sell_st_dt,
    "SELL_ED_DT" as sell_ed_dt
from {{ ref('demo_source5') }}
