select product_id, product_nm, product_no, color,
    cast(std_cost as number(38,0)) as std_cost,
    cast(list_price as number(38,0)) as list_price,
    o_sell_st_dt as sell_st_dt, o_sell_ed_dt as sell_ed_dt
from {{ ref('int_m_demo_mapping1__exp_trans2') }}
