{% macro lkp_trans1(in_acct_id) %}
(
    SELECT MAX_BY(TX_TYPE_CD, SEED_ROW)
    FROM {{ source('raw', 'lkp_demo_source3') }} AS lkp
    WHERE
   lkp.ACCT_ID = {{ in_acct_id }}
)
{% endmacro %}