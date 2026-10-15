WITH source_data AS
(
   SELECT
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
   FROM
      {{ ref('stg_m_demo_mapping3__sq_demo_source2') }}
)
SELECT
   Title AS Title,
   First_Name AS First_Name,
   Middle_Name AS Middle_Name,
   Last_Name AS Last_Name,
   Member_ID AS Member_ID,
   Member_Suffix AS Member_Suffix,
   Birth_Date AS Birth_Date,
   Gender_Code AS Gender_Code,
   Member_Record_Number AS Member_Record_Number,
   Social_Security_Number AS Social_Security_Number,
   Member_Type_Code AS Member_Type_Code,
   Original_Effective_Date AS Original_Effective_Date,
   Relationship_to_Subscriber_Code AS Relationship_to_Subscriber_Code,
   Relationship_to_Subscriber_Code_Label AS Relationship_to_Subscriber_Code_Label,
   -- ABORT('Relationship_to_Subscriber_Code_Labe valuel is null') is enforced by the not_null test on
   -- stg_m_demo_mapping3__sq_demo_source2: dbt build fails before any target is written.
   Relationship_to_Subscriber_Code_Label AS o_Relationship_to_Subscriber_Code_Label
FROM
   source_data