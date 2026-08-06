{{ config(tags=['informatica', 's_m_demo_mapping3']) }}

/*
  RECOVERED: all columns are direct source-field pass-throughs from the
  demo_source2 SOURCE and SOURCEFIELD elements in wf_demo_mapping.XML.
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
from {{ ref('demo_source2') }}
