WITH source_data AS
(
   SELECT
      *
   FROM
      {{ ref('int_m_demo_mapping2__rtrtrans__insert') }}
),
sequence_data AS
(
   SELECT
      *,
      -- SEQTRANS: Current Value 57, Increment By 1, Cycle NO
      56 + ROW_NUMBER()
      OVER (
      ORDER BY
         ID1) AS NEXTVAL
   FROM
      source_data
)
SELECT
   *
FROM
   sequence_data