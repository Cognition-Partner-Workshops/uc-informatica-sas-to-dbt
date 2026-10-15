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
      {{ ref('int_m_demo_mapping1__exp_trans1') }}
)
SELECT
   BAL_AMT BAL_AMT1,
   ACCT_ID ACCT_ID1,
   o_ACCT_ID o_ACCT_ID1,
   o_acc_trim o_acc_trim1,
   TX_DTTM TX_DTTM1,
   TX_ID TX_ID1,
   ACCT_TYP ACCT_TYP1,
   TX_AMT TX_AMT1,
   LAST_NM LAST_NM1,
   CLSR_DT CLSR_DT1,
   ACCT_STAT_CD ACCT_STAT_CD1,
   o_ACCT_DESC o_ACCT_DESC1,
   CR8_DT CR8_DT1,
   o_crdt_trim o_crdt_trim1,
   FIRST_NM FIRST_NM1,
   CRDT_SCORE CRDT_SCORE1
FROM
   source_data
WHERE
   ACCT_TYP = 'SB'