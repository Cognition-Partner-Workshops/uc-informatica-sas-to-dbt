with classified_columns as (
    select *
    from {{ ref('pii_classification') }}
),
tag_references as (
    {{ pii_tag_references() }}
)
select
    classified_columns.*,
    case
        when tag_references.column_name is null then 'missing PII_CATEGORY tag'
        else 'tag value ' || tag_references.tag_value || ', expected ' || classified_columns.pii_category
    end as reason
from classified_columns
left join tag_references
    on upper(classified_columns.schema_name) = upper(tag_references.schema_name)
    and upper(classified_columns.table_name) = upper(tag_references.table_name)
    and upper(classified_columns.column_name) = upper(tag_references.column_name)
where tag_references.column_name is null
   or tag_references.tag_value is null
   or upper(tag_references.tag_value) <> upper(classified_columns.pii_category)
