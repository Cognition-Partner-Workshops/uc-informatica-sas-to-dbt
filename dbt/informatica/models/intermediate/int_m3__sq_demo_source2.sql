{{ config(tags=['informatica', 's_m_demo_mapping3']) }}

/*
  RECOVERED: SQ_demo_source2 SQL override selects the 14 demo_source2
  ports and filters Member_Type_Code IS NOT NULL.
  DECISION: Keep the recovered port names and source casing unchanged;
  renaming is deferred to the target connectors.
*/
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
    Relationship_to_Subscriber_Code_Label
from {{ ref('stg_demo_source2') }}
where Member_Type_Code is not null
