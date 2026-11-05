select
    cast("PRODUCT_ID" as varchar) as product_id,
    cast("PRODUCT_NM" as varchar) as product_nm,
    cast("PRODUCT_NO" as varchar) as product_no,
    cast("COLOR" as varchar) as color,
    cast("STD_COST" as varchar) as std_cost,
    cast("LIST_PRICE" as varchar) as list_price,
    cast("SELL_ST_DT" as varchar) as sell_st_dt,
    cast("SELL_ED_DT" as varchar) as sell_ed_dt
from {{ source('infa_source', 'DEMO_SOURCE5') }}
