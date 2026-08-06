{{ config(tags=['informatica', 's_m_demo_mapping3']) }}

/*
  RECOVERED: CONNECTOR elements map NEWGROUP2 router ports to these target
  columns in this order: Title, Gender, First_Name, Middle_Name, Last_Name,
  Member_Identifier, Member_Suffix, Date_of_Birth, Member_Number, Soc_Number,
  Type_Code, Relationship_to_Subscriber_Code,
  Relationship_to_Subscriber_Code_Label, Effective_Date.
  DECISION: Although demo_target21 and demo_target2 share physical table
  demo_target2 in the legacy session, retain two dbt models as required by
  the milestone and represent each target instance independently.
*/
select
    Title,
    Gender_Code as Gender,
    First_Name,
    Middle_Name,
    Last_Name,
    Member_ID as Member_Identifier,
    Member_Suffix,
    Birth_Date as Date_of_Birth,
    Member_Record_Number as Member_Number,
    Social_Security_Number as Soc_Number,
    Member_Type_Code as Type_Code,
    Relationship_to_Subscriber_Code,
    o_Relationship_to_Subscriber_Code_Label as Relationship_to_Subscriber_Code_Label,
    Original_Effective_Date as Effective_Date
from {{ ref('int_m3__rtr_newgroup2') }}
