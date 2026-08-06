{{ config(tags=['informatica', 's_m_demo_mapping1']) }}

/*
  RECOVERED: exp_TRANS2 passes through the six VARCHAR product ports.
  RECOVERED: o_SELL_ST_DT evaluates TO_DATE(TO_CHAR(SYSDATE),'DD/MM/YYYY'),
  which is NULL because Informatica's default timestamp text does not match
  the mask; the populated SELL_ST_DT input is unused.
  RECOVERED: o_SELL_ED_DT parses SELL_ED_DT with DD/MM/YYYY.
*/
select
    PRODUCT_ID,
    PRODUCT_NM,
    PRODUCT_NO,
    COLOR,
    STD_COST,
    LIST_PRICE,
    cast(null as date) as o_SELL_ST_DT,
    {{ ddmmyyyy_to_date('SELL_ED_DT') }} as o_SELL_ED_DT
from {{ ref('stg_demo_source5') }}
