SELECT
   $1 :: VARCHAR(256) AS PRODUCT_ID,
   $2 :: VARCHAR(256) AS PRODUCT_NM,
   $3 :: VARCHAR(4) AS PRODUCT_NO,
   $4 :: VARCHAR(256) AS COLOR,
   $5 :: VARCHAR(3) AS STD_COST,
   $6 :: VARCHAR(3) AS LIST_PRICE,
   $7 :: VARCHAR(29) AS SELL_ST_DT,
   $8 :: VARCHAR(29) AS SELL_ED_DT
FROM
   @public.landing_stage/infpc/sources/RTUS/demo_source5/PRODUCT (FILE_FORMAT => 'RTUS_m_demo_mapping1_demo_source5')