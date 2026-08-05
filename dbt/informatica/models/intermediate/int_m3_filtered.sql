-- m_demo_mapping3 SQ_demo_source2 SQL override (WHERE Member_Type_Code IS NOT
-- NULL) plus EXPTRANS. The legacy o_Relationship_to_Subscriber_Code_Label
-- expression ABORTs the session when the label is NULL on a filtered-in row;
-- a not_null schema test on this model enforces the same contract.
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
    relationship_to_subscriber_code_label as o_relationship_to_subscriber_code_label
from {{ ref('stg_demo_source2') }}
where member_type_code is not null
