{{ config(tags=['informatica', 's_m_demo_mapping3']) }}

/*
  RECOVERED: EXPTRANS passes through all SQ_demo_source2 ports and defines
  o_Relationship_to_Subscriber_Code_Label as
  iif(ISNULL(Relationship_to_Subscriber_Code_Label),
  ABORT('Relationship_to_Subscriber_Code_Labe valuel is null'),
  Relationship_to_Subscriber_Code_Label).
  DECISION: ABORT is unrepresentable as a row value, so the label passes
  through here and an ERROR-severity singular test enforces the hard failure.
  The ABORT is NOT implemented as a where filter and NOT as a warn test.
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
    Relationship_to_Subscriber_Code_Label
        as o_Relationship_to_Subscriber_Code_Label
from {{ ref('int_m3__sq_demo_source2') }}
