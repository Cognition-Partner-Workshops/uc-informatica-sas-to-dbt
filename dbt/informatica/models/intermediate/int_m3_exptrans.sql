select
    title,
    first_name,
    middle_name,
    last_name,
    member_id,
    member_suffix,
    birth_date,
    gender_code,
    member_record_number,
    social_security_number,
    member_type_code,
    original_effective_date,
    relationship_to_subscriber_code,
    relationship_to_subscriber_code_label,
    relationship_to_subscriber_code_label as o_relationship_to_subscriber_code_label
from {{ ref('stg_demo_source2') }}
where member_type_code is not null
