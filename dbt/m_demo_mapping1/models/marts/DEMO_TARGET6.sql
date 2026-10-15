WITH source_data AS
(
   SELECT
      ACCT_ID,
      o_acc_trim,
      o_ACCT_DESC,
      CR8_DT,
      o_crdt_trim,
      CLSR_DT,
      ACCT_STAT_CD,
      TX_ID,
      NEXTVAL,
      TX_DTTM,
      o_TX_AMT,
      o_ACCT_ID
   FROM
      {{ ref('int_m_demo_mapping1__seq_gen') }}
)
SELECT
   sd.ACCT_ID AS ACCT_ID,
   sd.o_acc_trim AS ACCT_TYP,
   sd.o_ACCT_DESC AS ACCT_DESC,
   sd.CR8_DT AS CR8_DT,
   sd.o_crdt_trim AS CRDT_LN,
   sd.CLSR_DT AS CLSR_DT,
   sd.ACCT_STAT_CD AS ACCT_STAT_CD,
   sd.TX_ID AS TX_ID,
   sd.NEXTVAL AS ACCT_KEY,
   sd.TX_DTTM AS TX_DTTM,
   sd.o_TX_AMT AS TX_AMT,
   sd.o_ACCT_ID AS TX_TYPE_CD
FROM
   source_data AS sd