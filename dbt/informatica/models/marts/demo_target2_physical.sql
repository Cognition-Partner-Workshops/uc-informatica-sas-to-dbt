-- Both session writers insert into table demo_target2, neither truncates, and
-- both have TARGETLOADORDER 1, so this is what the legacy run actually
-- produces. Soc_Number null-ness is the branch discriminator; no marker column
-- is added.
{{ config(materialized='table') }}

with physical_load as (
    select
        cast(title as varchar) as "Title",
        cast(gender_code as varchar) as "Gender",
        cast(first_name as varchar) as "First_Name",
        cast(middle_name as varchar) as "Middle_Name",
        cast(last_name as varchar) as "Last_Name",
        cast(member_id as numeric(15,0)) as "Member_Identifier",
        cast(member_suffix as varchar) as "Member_Suffix",
        cast(birth_date as date) as "Date_of_Birth",
        cast(member_record_number as numeric(15,0)) as "Member_Number",
        cast(social_security_number as numeric(15,0)) as "Soc_Number",
        cast(member_type_code as numeric(15,0)) as "Type_Code",
        cast(relationship_to_subscriber_code as numeric(15,0)) as "Relationship_to_Subscriber_Code",
        cast(o_relationship_to_subscriber_code_label as varchar) as "Relationship_to_Subscriber_Code_Label",
        cast(original_effective_date as date) as "Effective_Date"
    from {{ ref('int_m3_exptrans') }}
    where social_security_number is null

    union all

    select
        cast(title as varchar) as "Title",
        cast(gender_code as varchar) as "Gender",
        cast(first_name as varchar) as "First_Name",
        cast(middle_name as varchar) as "Middle_Name",
        cast(last_name as varchar) as "Last_Name",
        cast(member_id as numeric(15,0)) as "Member_Identifier",
        cast(member_suffix as varchar) as "Member_Suffix",
        cast(birth_date as date) as "Date_of_Birth",
        cast(member_record_number as numeric(15,0)) as "Member_Number",
        cast(social_security_number as numeric(15,0)) as "Soc_Number",
        cast(member_type_code as numeric(15,0)) as "Type_Code",
        cast(relationship_to_subscriber_code as numeric(15,0)) as "Relationship_to_Subscriber_Code",
        cast(o_relationship_to_subscriber_code_label as varchar) as "Relationship_to_Subscriber_Code_Label",
        cast(original_effective_date as date) as "Effective_Date"
    from {{ ref('int_m3_exptrans') }}
    where social_security_number is not null
)

select *
from physical_load
