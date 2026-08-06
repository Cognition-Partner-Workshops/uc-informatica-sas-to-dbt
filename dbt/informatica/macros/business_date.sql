{% macro business_date() %}
cast('{{ var("business_date") }}' as date)
{% endmacro %}

{% macro business_timestamp() %}
cast('{{ var("business_date") }} 00:00:00' as timestamp)
{% endmacro %}
