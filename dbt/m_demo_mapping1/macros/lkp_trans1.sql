{% macro lkp_trans1(in_acct_id) %}
(
    SELECT MAX(TX_TYPE_CD)
    FROM {{ source('raw', 'lkp_demo_source3') }} AS lkp
    WHERE
   lkp.ACCT_ID = {{ in_acct_id }}
)
{% endmacro %}