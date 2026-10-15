WITH source_data AS
(
   SELECT
      PRODUCT_ID,
      PRODUCT_NM,
      PRODUCT_NO,
      COLOR,
      STD_COST,
      LIST_PRICE,
      o_SELL_ST_DT,
      o_SELL_ED_DT
   FROM
      {{ ref('int_exp_TRANS2') }}
)
SELECT
   sd.PRODUCT_ID AS PRODUCT_ID,
   sd.PRODUCT_NM AS PRODUCT_NM,
   sd.PRODUCT_NO AS PRODUCT_NO,
   sd.COLOR AS COLOR,
   sd.STD_COST AS STD_COST,
   sd.LIST_PRICE AS LIST_PRICE,
   sd.o_SELL_ST_DT AS SELL_ST_DT,
   sd.o_SELL_ED_DT AS SELL_ED_DT
FROM
   source_data AS sd