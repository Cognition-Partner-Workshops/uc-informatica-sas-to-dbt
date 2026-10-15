SELECT
   demo_source5.PRODUCT_ID AS PRODUCT_ID,
   demo_source5.PRODUCT_NM AS PRODUCT_NM,
   demo_source5.PRODUCT_NO AS PRODUCT_NO,
   demo_source5.COLOR AS COLOR,
   demo_source5.STD_COST AS STD_COST,
   demo_source5.LIST_PRICE AS LIST_PRICE,
   demo_source5.SELL_ST_DT AS SELL_ST_DT,
   demo_source5.SELL_ED_DT AS SELL_ED_DT
FROM
   {{ ref('stg_flat_file__demo_source5') }} AS demo_source5