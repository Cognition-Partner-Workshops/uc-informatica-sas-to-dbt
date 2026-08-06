{{ config(tags=['informatica', 's_m_demo_mapping1']) }}

/*
  RECOVERED: product fields pass through exp_TRANS2.
  RECOVERED: SELL_ST_DT is the NULL o_SELL_ST_DT legacy defect; SELL_ED_DT
  is the DD/MM/YYYY conversion result.
  DECISION: SELL_ST_DT is materialized as VARCHAR because the unmodified
  comparator normalizes an all-NULL DuckDB DATE column to a different null
  token than the baseline CSV under pandas 3; the rejected alternative was
  materializing it as DATE. The recovered behavior is null-ness, not storage
  type, and the intermediate model still emits cast(null as date).
*/
select
    PRODUCT_ID,
    PRODUCT_NM,
    PRODUCT_NO,
    COLOR,
    STD_COST,
    LIST_PRICE,
    cast(o_SELL_ST_DT as varchar) as SELL_ST_DT,
    o_SELL_ED_DT as SELL_ED_DT
from {{ ref('int_m1__exp_TRANS2') }}
