WITH source_data AS
(
   SELECT
      *
   FROM
      {{ ref('int_m_demo_mapping1__agg_trans') }}
),
sequence_data AS
(
   SELECT
      *,
      -- SEQ_GEN: Current Value 281, End Value 2147483647, Cycle YES
      MOD(281 + ROW_NUMBER()
      OVER (
      ORDER BY
         ACCT_ID) - 2, 2147483647) + 1 AS NEXTVAL
   FROM
      source_data
)
SELECT
   *
FROM
   sequence_data