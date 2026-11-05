select product_id, product_nm, product_no, color, std_cost, list_price,
    cast(null as date) as o_sell_st_dt,
    cast(substr(sell_ed_dt, 7, 4) || '-' || substr(sell_ed_dt, 4, 2)
        || '-' || substr(sell_ed_dt, 1, 2) as date) as o_sell_ed_dt
from {{ ref('int_m_demo_mapping1__sq_demo_source5') }}
