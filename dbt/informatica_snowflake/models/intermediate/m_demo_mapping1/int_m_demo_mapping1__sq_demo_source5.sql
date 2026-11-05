select product_id, product_nm, product_no, color, std_cost, list_price, sell_st_dt, sell_ed_dt
from {{ ref('stg_informatica__demo_source5') }}
