-- m_demo_mapping3 RTRTRANS NEWGROUP2 (NOT ISNULL(Social_Security_Number)) ->
-- demo_target21.
select
    title                     as "Title",
    gender_code               as "Gender",
    first_name                as "First_Name",
    middle_name               as "Middle_Name",
    last_name                 as "Last_Name",
    member_id                 as "Member_Identifier",
    member_suffix             as "Member_Suffix",
    birth_date                as "Date_of_Birth",
    member_record_number      as "Member_Number",
    social_security_number    as "Soc_Number",
    member_type_code          as "Type_Code",
    relationship_to_subscriber_code           as "Relationship_to_Subscriber_Code",
    o_relationship_to_subscriber_code_label   as "Relationship_to_Subscriber_Code_Label",
    original_effective_date   as "Effective_Date"
from {{ ref('int_m3_filtered') }}
where social_security_number is not null
