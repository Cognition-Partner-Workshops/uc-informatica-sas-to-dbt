{{ config(materialized='ephemeral', tags=['informatica', 's_m_demo_mapping3']) }}

/*
  RECOVERED: literal row reproduced from legacy/informatica/data/abort/
  demo_source2.csv, then passed through SQ_demo_source2's
  Member_Type_Code IS NOT NULL filter with the same port names and types.
  DECISION: Keep this fixture ephemeral so it creates no warehouse object
  and remains excluded from a normal build.
*/
with abort_source as (
    select
        cast('MS' as varchar) as Title,
        cast('Tara' as varchar) as First_Name,
        cast('S' as varchar) as Middle_Name,
        cast('Young' as varchar) as Last_Name,
        cast(40001 as double) as Member_ID,
        cast(null as varchar) as Member_Suffix,
        cast('1982-11-01' as timestamp) as Birth_Date,
        cast('F' as varchar) as Gender_Code,
        cast(600001 as double) as Member_Record_Number,
        cast(100000222 as double) as Social_Security_Number,
        cast(1 as double) as Member_Type_Code,
        cast('2021-07-01' as timestamp) as Original_Effective_Date,
        cast(1 as double) as Relationship_to_Subscriber_Code,
        cast(null as varchar) as Relationship_to_Subscriber_Code_Label
)
select
    Title,
    First_Name,
    Middle_Name,
    Last_Name,
    Member_ID,
    Member_Suffix,
    Birth_Date,
    Gender_Code,
    Member_Record_Number,
    Social_Security_Number,
    Member_Type_Code,
    Original_Effective_Date,
    Relationship_to_Subscriber_Code,
    Relationship_to_Subscriber_Code_Label,
    Relationship_to_Subscriber_Code_Label
        as o_Relationship_to_Subscriber_Code_Label
from abort_source
where Member_Type_Code is not null
