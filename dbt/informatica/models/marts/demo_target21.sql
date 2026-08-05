select
    cast(title as varchar) as "Title",
    cast(gender_code as varchar) as "Gender",
    cast(first_name as varchar) as "First_Name",
    cast(middle_name as varchar) as "Middle_Name",
    cast(last_name as varchar) as "Last_Name",
    cast(member_id as varchar) as "Member_Identifier",
    cast(member_suffix as varchar) as "Member_Suffix",
    cast(birth_date as varchar) as "Date_of_Birth",
    cast(member_record_number as varchar) as "Member_Number",
    cast(social_security_number as varchar) as "Soc_Number",
    cast(member_type_code as varchar) as "Type_Code",
    cast(relationship_to_subscriber_code as varchar) as "Relationship_to_Subscriber_Code",
    cast(o_relationship_to_subscriber_code_label as varchar) as "Relationship_to_Subscriber_Code_Label",
    cast(original_effective_date as varchar) as "Effective_Date"
from {{ ref('int_m3_exptrans') }}
where social_security_number is not null
