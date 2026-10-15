with classified_columns as (
    select *
    from {{ ref('pii_classification') }}
),
policy_references as (
    {{ pii_policy_references() }}
)
select classified_columns.*
from classified_columns
left join policy_references
    on upper(classified_columns.schema_name) = upper(policy_references.schema_name)
    and upper(classified_columns.table_name) = upper(policy_references.table_name)
    and upper(classified_columns.column_name) = upper(policy_references.column_name)
    and policy_references.tag_name = 'PII_CATEGORY'
where policy_references.column_name is null
