-- SQ_demo_source5: default source qualifier over the demo_source5 flat file.
select
    PRODUCT_ID,
    PRODUCT_NM,
    PRODUCT_NO,
    COLOR,
    STD_COST,
    LIST_PRICE,
    SELL_ST_DT,
    SELL_ED_DT
from {{ source('infa_src', 'DEMO_SOURCE5') }}
