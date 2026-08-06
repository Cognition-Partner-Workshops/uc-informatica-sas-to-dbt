{{ config(tags=['informatica', 's_m_demo_mapping1']) }}

/*
  RECOVERED: product fields pass through exp_TRANS2.
  RECOVERED: SELL_ST_DT is the NULL o_SELL_ST_DT legacy defect; SELL_ED_DT
  is the DD/MM/YYYY conversion result. RECOVERED: SELL_ST_DT is a DATE
  port whose expression yields NULL; the intermediate model emits
  cast(null as date). Parity comparison requires pandas<3 as an environment
  requirement, not a modeling decision.
*/
select
    PRODUCT_ID,
    PRODUCT_NM,
    PRODUCT_NO,
    COLOR,
    STD_COST,
    LIST_PRICE,
    o_SELL_ST_DT as SELL_ST_DT,
    o_SELL_ED_DT as SELL_ED_DT
from {{ ref('int_m1__exp_TRANS2') }}
