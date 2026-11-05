with qualified as (
    select * from {{ source('infa_m23', 'demo_source2') }}
    where Member_Type_Code is not null
), validation as (
    select case when count(*) filter (
        where Relationship_to_Subscriber_Code_Label is null
    ) > 0 then error('ABORT: Relationship_to_Subscriber_Code_Labe valuel is null')
    else true end as valid
    from qualified
)
select Title, Gender_Code as Gender, First_Name, Middle_Name, Last_Name,
       cast(Member_ID as double) as Member_Identifier, Member_Suffix,
       cast(Birth_Date as timestamp) as Date_of_Birth,
       cast(Member_Record_Number as double) as Member_Number,
       cast(Social_Security_Number as double) as Soc_Number,
       cast(Member_Type_Code as double) as Type_Code,
       cast(Relationship_to_Subscriber_Code as double) as Relationship_to_Subscriber_Code,
       Relationship_to_Subscriber_Code_Label,
       cast(Original_Effective_Date as timestamp) as Effective_Date
from qualified cross join validation
where valid
