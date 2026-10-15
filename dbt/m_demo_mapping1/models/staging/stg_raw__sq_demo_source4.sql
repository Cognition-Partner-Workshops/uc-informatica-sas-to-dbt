--** SSC-FDM-0007 - MISSING DEPENDENT OBJECTS "STRCMP", "demo_source3", "demo_source4" **
SELECT
   demo_source4.ACCT_ID,
   demo_source4.ACCT_TYP,
   demo_source4.ACCT_DESC,
   demo_source4.CRDT_LN,
   CURRENT_TIMESTAMP() /*** SSC-FDM-OR0047 - YOU MAY NEED TO SET TIMESTAMP OUTPUT FORMAT ('DD-MON-YY HH24.MI.SS.FF AM TZH:TZM') ***/ AS CR8_DT,
   demo_source4.CLSR_DT,
   demo_source4.ACCT_STAT_CD,
   demo_source3.TX_ID,
   demo_source3.LAST_NM,
   demo_source3.TX_DTTM,
   demo_source3.TX_AMT,
   demo_source3.BAL_AMT,
   demo_source3.CUST_ID,
   STRCMP(demo_source4.ACCT_STAT_CD, demo_source3.TX_TYPE_CD) !!!RESOLVE EWI!!! /*** SSC-EWI-0130 - 'STRCMP' IS NOT DEFINED IN THE PROVIDED SOURCE. INCLUDE ITS DEFINITION IN THE CONVERSION SCOPE OR REVIEW THE GENERATED CODE. ***/!!! AS TX_TYPE_CD
FROM
   {{ source('raw', 'demo_source3') }} AS demo_source3
   INNER JOIN
      {{ source('raw', 'demo_source4') }} AS demo_source4
      ON demo_source3.ACCT_ID = demo_source4.ACCT_ID
ORDER BY demo_source4.ACCT_ID