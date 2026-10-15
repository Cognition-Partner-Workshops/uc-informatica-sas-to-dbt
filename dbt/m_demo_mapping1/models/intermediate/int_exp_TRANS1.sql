WITH source_data AS
(
   SELECT
      lkp_TRANS2__FIRST_NM AS FIRST_NM,
      exp_TRANS__CLSR_DT AS CLSR_DT,
      exp_TRANS__TX_DTTM AS TX_DTTM,
      exp_TRANS__BAL_AMT AS BAL_AMT,
      exp_TRANS__ACCT_DESC AS ACCT_DESC,
      exp_TRANS__ACCT_TYP AS ACCT_TYP,
      exp_TRANS__ACCT_STAT_CD AS ACCT_STAT_CD,
      exp_TRANS__TX_ID AS TX_ID,
      exp_TRANS__LAST_NM AS LAST_NM,
      exp_TRANS__TX_AMT AS TX_AMT,
      exp_TRANS__ACCT_ID AS ACCT_ID,
      exp_TRANS__CR8_DT AS CR8_DT,
      exp_TRANS__o_acc_trim AS o_acc_trim,
      exp_TRANS__o_crdt_trim AS o_crdt_trim,
      exp_TRANS__o_ACCT_ID AS o_ACCT_ID,
      CRDT_SCORE
   FROM
      {{ ref('int_lkp_TRANS3') }}
)
SELECT
   FIRST_NM AS FIRST_NM,
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
   o_acc_trim AS o_acc_trim,
   o_crdt_trim AS o_crdt_trim,
   o_ACCT_ID AS o_ACCT_ID,
   CRDT_SCORE AS CRDT_SCORE,
   RTRIM(ACCT_DESC) AS o_ACCT_DESC
FROM
   source_data