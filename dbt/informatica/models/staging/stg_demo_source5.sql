{{ config(tags=['informatica', 's_m_demo_mapping1']) }}

/*
  RECOVERED: all columns are direct source-field pass-throughs from the
  demo_source5 SOURCE and SOURCEFIELD elements in wf_demo_mapping.XML.
*/
select
    PRODUCT_ID,
    PRODUCT_NM,
    PRODUCT_NO,
    COLOR,
    STD_COST,
    LIST_PRICE,
    SELL_ST_DT,
    SELL_ED_DT
from {{ ref('demo_source5') }}
