{% macro apply_pii_tags() %}
  {% if execute %}
    {% set rows = run_query(
      "select schema_name, table_name, column_name, pii_category from " ~ ref('pii_classification')
    ) %}
    {% set state = namespace(applied=0, skipped=0, table_pairs=[]) %}

    {% if rows is not none and rows | length > 0 %}
      {% for row in rows %}
        {% set pair = [row[0] | upper, row[1] | upper] %}
        {% if pair not in state.table_pairs %}
          {% do state.table_pairs.append(pair) %}
        {% endif %}
      {% endfor %}

      {% set predicates = [] %}
      {% for pair in state.table_pairs %}
        {% do predicates.append(
          "(table_schema = '" ~ pair[0] ~ "' and table_name = '" ~ pair[1] ~ "')"
        ) %}
      {% endfor %}
      {% set existing = run_query(
        "select table_schema, table_name from DEVIN_MIGRATION_DEMO.information_schema.tables where " ~ predicates | join(" or ")
      ) %}
      {% set existing_pairs = namespace(values=[]) %}
      {% for row in existing %}
        {% do existing_pairs.values.append([row[0] | upper, row[1] | upper]) %}
      {% endfor %}

      {% for row in rows %}
        {% set schema_name = row[0] | upper %}
        {% set table_name = row[1] | upper %}
        {% set column_name = row[2] | upper %}
        {% set category = row[3] | upper %}
        {% if [schema_name, table_name] in existing_pairs.values %}
          {% do run_query(
            "alter table DEVIN_MIGRATION_DEMO." ~ schema_name ~ "." ~ table_name ~
            " modify column " ~ column_name ~
            " set tag DEVIN_MIGRATION_DEMO.DBT_SF_20261015_DS.PII_CATEGORY = '" ~ category ~ "'"
          ) %}
          {% set state.applied = state.applied + 1 %}
        {% else %}
          {% do log(
            "apply_pii_tags: skipping missing table " ~ schema_name ~ "." ~ table_name ~ "." ~ column_name,
            info=true
          ) %}
          {% set state.skipped = state.skipped + 1 %}
        {% endif %}
      {% endfor %}
    {% endif %}

    {% do log(
      "apply_pii_tags: applied " ~ state.applied ~ " column tags; skipped " ~ state.skipped ~ " rows for missing tables",
      info=true
    ) %}
  {% endif %}
{% endmacro %}
