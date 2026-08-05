-- m_demo_mapping1 exp_TRANS2 -> demo_target3.
-- SELL_ST_DT: the legacy TO_DATE(TO_CHAR(SYSDATE),'DD/MM/YYYY') is
-- unparseable on the pinned run date and yields NULL (see STM notes).
-- SELL_ED_DT: parsed from the DD/MM/YYYY source string via substrings so the
-- SQL stays portable between DuckDB and Snowflake.
select
    product_id as "PRODUCT_ID",
    product_nm as "PRODUCT_NM",
    product_no as "PRODUCT_NO",
    color      as "COLOR",
    std_cost   as "STD_COST",
    list_price as "LIST_PRICE",
    cast(null as date) as "SELL_ST_DT",
    cast(substr(sell_ed_dt, 7, 4) || '-' || substr(sell_ed_dt, 4, 2)
         || '-' || substr(sell_ed_dt, 1, 2) as date) as "SELL_ED_DT"
from {{ ref('stg_demo_source5') }}
