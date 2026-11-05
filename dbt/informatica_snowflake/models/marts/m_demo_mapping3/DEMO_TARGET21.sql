select
    title as "TITLE",
    gender_code as "GENDER",
    first_name as "FIRST_NAME",
    middle_name as "MIDDLE_NAME",
    last_name as "LAST_NAME",
    member_id as "MEMBER_IDENTIFIER",
    member_suffix as "MEMBER_SUFFIX",
    birth_date as "DATE_OF_BIRTH",
    member_record_number as "MEMBER_NUMBER",
    social_security_number as "SOC_NUMBER",
    member_type_code as "TYPE_CODE",
    relationship_to_subscriber_code as "RELATIONSHIP_TO_SUBSCRIBER_CODE",
    relationship_to_subscriber_code_label as "RELATIONSHIP_TO_SUBSCRIBER_CODE_LABEL",
    original_effective_date as "EFFECTIVE_DATE"
from {{ ref('int_m_demo_mapping3__router') }}
where route = 'NEWGROUP2'
