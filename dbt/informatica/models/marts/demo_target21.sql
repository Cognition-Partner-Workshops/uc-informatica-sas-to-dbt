{{ config(tags=['informatica', 's_m_demo_mapping3']) }}

/*
  RECOVERED: CONNECTOR elements map NEWGROUP2 router ports to these target
  columns in this order: Title, Gender, First_Name, Middle_Name, Last_Name,
  Member_Identifier, Member_Suffix, Date_of_Birth, Member_Number, Soc_Number,
  Type_Code, Relationship_to_Subscriber_Code,
  Relationship_to_Subscriber_Code_Label, Effective_Date.
  RECOVERED: the export holds one target DEFINITION, TARGET NAME="demo_target2"
  DATABASETYPE="Oracle", and two INSTANCEs of it, NAME="demo_target21" and
  NAME="demo_target2", both TRANSFORMATION_NAME="demo_target2" and both
  TARGETLOADORDER ORDER="1". Each instance is fed by its own router group and
  has its own SESSIONEXTENSION Relational Writer with its own reject file
  (demo_target211.bad for this instance, demo_target21.bad for demo_target2),
  so the legacy writes one physical Oracle table, demo_target2, from two
  writers.
  DECISION: dbt has no equivalent of two models writing one relation, so each
  target instance is modelled as its own table. Rejected alternative: a single
  unioned model carrying a group/instance discriminator, which changes the
  shape of the delivered object and cannot be compared per instance against
  the baseline.
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
