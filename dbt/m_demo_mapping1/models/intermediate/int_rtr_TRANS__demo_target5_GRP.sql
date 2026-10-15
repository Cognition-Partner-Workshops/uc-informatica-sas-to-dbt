WITH source_data AS
(
   SELECT
      BAL_AMT,
      ACCT_ID,
      o_ACCT_ID,
      o_acc_trim,
      TX_DTTM,
      TX_ID,
      ACCT_TYP,
      TX_AMT,
      LAST_NM,
      CLSR_DT,
      ACCT_STAT_CD,
      o_ACCT_DESC,
      CR8_DT,
      o_crdt_trim,
      FIRST_NM,
      CRDT_SCORE
   FROM
      {{ ref('int_exp_TRANS1') }}
)
SELECT
   BAL_AMT BAL_AMT2,
   ACCT_ID ACCT_ID2,
   o_ACCT_ID o_ACCT_ID2,
   o_acc_trim o_acc_trim2,
   TX_DTTM TX_DTTM2,
   TX_ID TX_ID2,
   ACCT_TYP ACCT_TYP2,
   TX_AMT TX_AMT2,
   LAST_NM LAST_NM2,
   CLSR_DT CLSR_DT2,
   ACCT_STAT_CD ACCT_STAT_CD2,
   o_ACCT_DESC o_ACCT_DESC2,
   CR8_DT CR8_DT2,
   o_crdt_trim o_crdt_trim2,
   FIRST_NM FIRST_NM2,
   CRDT_SCORE CRDT_SCORE2
FROM
   source_data
WHERE
   ACCT_TYP <> 'SB'