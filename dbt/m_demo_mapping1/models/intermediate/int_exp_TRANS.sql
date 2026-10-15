WITH source_data AS
(
   SELECT
      CRDT_LN,
      CLSR_DT,
      TX_DTTM,
      BAL_AMT,
      ACCT_DESC,
      ACCT_TYP,
      ACCT_STAT_CD,
      TX_ID,
      LAST_NM,
      TX_AMT,
      ACCT_ID,
      CR8_DT,
      CUST_ID
   FROM
      {{ ref('stg_raw__sq_demo_source4') }}
)
SELECT
   CLSR_DT AS CLSR_DT,
   TX_DTTM AS TX_DTTM,
   BAL_AMT AS BAL_AMT,
   ACCT_DESC AS ACCT_DESC,
   ACCT_TYP AS ACCT_TYP,
   ACCT_STAT_CD AS ACCT_STAT_CD,
   TX_ID AS TX_ID,
   LAST_NM AS LAST_NM,
   TX_AMT AS TX_AMT,
   ACCT_ID AS ACCT_ID,
   CR8_DT AS CR8_DT,
   CUST_ID AS CUST_ID,
   RTRIM(ACCT_TYP) AS o_acc_trim,
   LTRIM(CRDT_LN) AS o_crdt_trim,
   {{ lkp_trans1('source_data.ACCT_ID') }} AS o_ACCT_ID
FROM
   source_data