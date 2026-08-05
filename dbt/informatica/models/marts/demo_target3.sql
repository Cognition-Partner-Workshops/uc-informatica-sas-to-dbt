select
    PRODUCT_ID,
    PRODUCT_NM,
    PRODUCT_NO,
    COLOR,
    cast(STD_COST as bigint) as STD_COST,
    cast(LIST_PRICE as bigint) as LIST_PRICE,
    -- TO_CHAR(SYSDATE) renders the pinned date as MM/DD/YYYY; parsing that
    -- string as DD/MM/YYYY makes 31 an invalid month, yielding NULL.
    cast(null as varchar) as SELL_ST_DT,
    try_cast(
        substr(SELL_ED_DT, 7, 4) || '-' ||
        substr(SELL_ED_DT, 4, 2) || '-' ||
        substr(SELL_ED_DT, 1, 2)
        as date
    ) as SELL_ED_DT
from {{ ref('stg_m1_demo_source5') }}
