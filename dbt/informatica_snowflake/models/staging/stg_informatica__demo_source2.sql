select
    cast("TITLE" as varchar) as title,
    cast("FIRST_NAME" as varchar) as first_name,
    cast("MIDDLE_NAME" as varchar) as middle_name,
    cast("LAST_NAME" as varchar) as last_name,
    cast("MEMBER_ID" as float) as member_id,
    cast("MEMBER_SUFFIX" as varchar) as member_suffix,
    cast("BIRTH_DATE" as timestamp_ntz) as birth_date,
    cast("GENDER_CODE" as varchar) as gender_code,
    cast("MEMBER_RECORD_NUMBER" as float) as member_record_number,
    cast("SOCIAL_SECURITY_NUMBER" as float) as social_security_number,
    cast("MEMBER_TYPE_CODE" as float) as member_type_code,
    cast("ORIGINAL_EFFECTIVE_DATE" as timestamp_ntz) as original_effective_date,
    cast("RELATIONSHIP_TO_SUBSCRIBER_CODE" as float) as relationship_to_subscriber_code,
    cast("RELATIONSHIP_TO_SUBSCRIBER_CODE_LABEL" as varchar) as relationship_to_subscriber_code_label
from {{ source('infa_source', 'DEMO_SOURCE2') }}
