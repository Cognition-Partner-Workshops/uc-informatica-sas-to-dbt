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
   BAL_AMT BAL_AMT3,
   ACCT_ID ACCT_ID3,
   o_ACCT_ID o_ACCT_ID3,
   o_acc_trim o_acc_trim3,
   TX_DTTM TX_DTTM3,
   TX_ID TX_ID3,
   ACCT_TYP ACCT_TYP3,
   TX_AMT TX_AMT3,
   LAST_NM LAST_NM3,
   CLSR_DT CLSR_DT3,
   ACCT_STAT_CD ACCT_STAT_CD3,
   o_ACCT_DESC o_ACCT_DESC3,
   CR8_DT CR8_DT3,
   o_crdt_trim o_crdt_trim3,
   FIRST_NM FIRST_NM3,
   CRDT_SCORE CRDT_SCORE3
FROM
   source_data
WHERE
   NOT COALESCE(ACCT_TYP = 'SB', FALSE)
   AND NOT COALESCE(ACCT_TYP <> 'SB', FALSE)