{% macro pii_policy_references() %}
  {% if execute %}
    {% set tables = run_query("select distinct schema_name, table_name from " ~ ref('pii_classification')) %}
    {% if tables is not none and tables | length > 0 %}
      {% for row in tables %}
        select '{{ row[0] }}' as schema_name,
               '{{ row[1] }}' as table_name,
               ref_column_name as column_name,
               policy_name,
               tag_name
        from table(DEVIN_MIGRATION_DEMO.information_schema.policy_references(
          ref_entity_name => 'DEVIN_MIGRATION_DEMO.{{ row[0] }}.{{ row[1] }}',
          ref_entity_domain => 'table'
        ))
        where policy_kind = 'MASKING_POLICY'
        {% if not loop.last %}union all{% endif %}
      {% endfor %}
    {% else %}
      select cast(null as varchar) as schema_name,
             cast(null as varchar) as table_name,
             cast(null as varchar) as column_name,
             cast(null as varchar) as policy_name,
             cast(null as varchar) as tag_name
      where 1 = 0
    {% endif %}
  {% else %}
    select cast(null as varchar) as schema_name,
           cast(null as varchar) as table_name,
           cast(null as varchar) as column_name,
           cast(null as varchar) as policy_name,
           cast(null as varchar) as tag_name
    where 1 = 0
  {% endif %}
{% endmacro %}
