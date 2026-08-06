{% macro ddmmyyyy_to_date(value_expression) %}
cast(
  substring({{ value_expression }}, 7, 4) || '-' ||
  substring({{ value_expression }}, 4, 2) || '-' ||
  substring({{ value_expression }}, 1, 2)
  as date
)
{% endmacro %}
