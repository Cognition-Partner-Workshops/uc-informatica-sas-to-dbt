{% macro pii_tag_references() %}
  {% if execute %}
    {% set tables = run_query("select distinct schema_name, table_name from " ~ ref('pii_classification')) %}
    {% if tables is not none and tables | length > 0 %}
      {% for row in tables %}
        select '{{ row[0] }}' as schema_name,
               '{{ row[1] }}' as table_name,
               column_name,
               tag_value
        from table(DEVIN_MIGRATION_DEMO.information_schema.tag_references_all_columns(
          'DEVIN_MIGRATION_DEMO.{{ row[0] }}.{{ row[1] }}',
          'table'
        ))
        where tag_database = 'DEVIN_MIGRATION_DEMO'
          and tag_schema = 'DBT_SF_20261015_DS'
          and tag_name = 'PII_CATEGORY'
        {% if not loop.last %}union all{% endif %}
      {% endfor %}
    {% else %}
      select cast(null as varchar) as schema_name,
             cast(null as varchar) as table_name,
             cast(null as varchar) as column_name,
             cast(null as varchar) as tag_value
      where 1 = 0
    {% endif %}
  {% else %}
    select cast(null as varchar) as schema_name,
           cast(null as varchar) as table_name,
           cast(null as varchar) as column_name,
           cast(null as varchar) as tag_value
    where 1 = 0
  {% endif %}
{% endmacro %}
