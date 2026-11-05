-- SQ_demo_source5 -> exp_TRANS2 -> demo_target3.
-- o_SELL_ST_DT = TO_DATE(TO_CHAR(SYSDATE), 'DD/MM/YYYY'): TO_CHAR(SYSDATE) uses the
-- session default date format, which does not parse as DD/MM/YYYY, so it is NULL
-- (the source SELL_ST_DT port is unconnected).
-- o_SELL_ED_DT = TO_DATE(SELL_ED_DT, 'DD/MM/YYYY').
select
    PRODUCT_ID,
    PRODUCT_NM,
    PRODUCT_NO,
    COLOR,
    STD_COST,
    LIST_PRICE,
    cast(null as date) as SELL_ST_DT,
    cast(strptime(SELL_ED_DT, '%d/%m/%Y') as date) as SELL_ED_DT
from {{ ref('sq_demo_source5') }}
order by PRODUCT_ID
