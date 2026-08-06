{{ config(tags=['informatica', 's_m_demo_mapping3']) }}

/*
  RECOVERED: RTRTRANS NEWGROUP2 routes rows where
  NOT ISNULL(Social_Security_Number) to target instance demo_target21.
  DECISION: Preserve router/port-side names until the target connector
  projection rather than applying target names in this intermediate model.
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
    Relationship_to_Subscriber_Code_Label,
    o_Relationship_to_Subscriber_Code_Label
from {{ ref('int_m3__exptrans') }}
where Social_Security_Number is not null
