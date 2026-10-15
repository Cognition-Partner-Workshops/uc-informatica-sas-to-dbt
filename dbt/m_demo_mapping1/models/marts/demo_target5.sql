WITH source_data AS
(
   SELECT
      ACCT_ID2,
      FIRST_NM2,
      LAST_NM2,
      BAL_AMT2,
      CRDT_SCORE2
   FROM
      {{ ref('int_rtr_TRANS__demo_target5_GRP') }}
)
SELECT
   sd.ACCT_ID2 AS ACCT_ID,
   sd.FIRST_NM2 AS FIRST_NM,
   sd.LAST_NM2 AS LAST_NM,
   sd.BAL_AMT2 AS BAL_AMT,
   sd.CRDT_SCORE2 AS CRDT_SCORE
FROM
   source_data AS sd