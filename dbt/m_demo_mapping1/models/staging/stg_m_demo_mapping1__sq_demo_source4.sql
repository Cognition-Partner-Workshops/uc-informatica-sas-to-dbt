--** SSC-FDM-0007 - MISSING DEPENDENT OBJECTS "STRCMP", "demo_source3", "demo_source4" **
SELECT
   demo_source4.ACCT_ID,
   demo_source4.ACCT_TYP,
   demo_source4.ACCT_DESC,
   demo_source4.CRDT_LN,
   TO_TIMESTAMP_NTZ('{{ var("business_date") }}') AS CR8_DT,
   demo_source4.CLSR_DT,
   demo_source4.ACCT_STAT_CD,
   demo_source3.TX_ID,
   demo_source3.LAST_NM,
   {{ epoch_us_repair('demo_source3.TX_DTTM') }} AS TX_DTTM,
   demo_source3.TX_AMT,
   demo_source3.BAL_AMT,
   demo_source3.CUST_ID,
   CASE
      WHEN demo_source4.ACCT_STAT_CD IS NULL OR demo_source3.TX_TYPE_CD IS NULL THEN NULL
      WHEN demo_source4.ACCT_STAT_CD < demo_source3.TX_TYPE_CD THEN -1
      WHEN demo_source4.ACCT_STAT_CD > demo_source3.TX_TYPE_CD THEN 1
      ELSE 0
   END AS TX_TYPE_CD
FROM
   {{ source('raw', 'demo_source3') }} AS demo_source3
   INNER JOIN
      {{ source('raw', 'demo_source4') }} AS demo_source4
      ON demo_source3.ACCT_ID = demo_source4.ACCT_ID
ORDER BY demo_source4.ACCT_ID