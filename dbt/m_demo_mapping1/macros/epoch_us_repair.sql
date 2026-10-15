{#- SOURCE_<token> TIMESTAMP_NTZ columns were loaded with epoch microseconds read as epoch
    seconds (years like 54041295). Rescale those to the nearest second; in-range values pass through. -#}
{% macro epoch_us_repair(col) -%}
IFF(ABS(DATE_PART(EPOCH_SECOND, {{ col }})) > 253402300799,
    TO_TIMESTAMP_NTZ(ROUND(DATE_PART(EPOCH_SECOND, {{ col }}) / 1000000)),
    {{ col }})
{%- endmacro %}
