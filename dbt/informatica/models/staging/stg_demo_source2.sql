select
    "Title"                                 as title,
    "First_Name"                            as first_name,
    "Middle_Name"                           as middle_name,
    "Last_Name"                             as last_name,
    "Member_ID"                             as member_id,
    "Member_Suffix"                         as member_suffix,
    "Birth_Date"                            as birth_date,
    "Gender_Code"                           as gender_code,
    "Member_Record_Number"                  as member_record_number,
    "Social_Security_Number"                as social_security_number,
    "Member_Type_Code"                      as member_type_code,
    "Original_Effective_Date"               as original_effective_date,
    "Relationship_to_Subscriber_Code"       as relationship_to_subscriber_code,
    "Relationship_to_Subscriber_Code_Label" as relationship_to_subscriber_code_label
from {{ ref('demo_source2') }}
