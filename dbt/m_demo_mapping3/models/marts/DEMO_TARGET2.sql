--** SSC-FDM-INF0029 - INFORMATICA LOADS TARGETS SEQUENTIALLY PER TARGETLOADORDER. THE TRANSLATED DBT MODEL USES UNION ALL TO COMBINE ALL PIPELINES INTO A SINGLE ATOMIC QUERY. IF PIPELINE EXECUTION ORDER AFFECTS THE FINAL RESULT, REVIEW THE GENERATED MODEL. **
WITH source_2 AS
(
   SELECT
      Title1,
      Gender_Code1,
      First_Name1,
      Middle_Name1,
      Last_Name1,
      Member_ID1,
      Member_Suffix1,
      Birth_Date1,
      Member_Record_Number1,
      Social_Security_Number1,
      Member_Type_Code1,
      Relationship_to_Subscriber_Code1,
      Relationship_to_Subscriber_Code_Label1,
      Original_Effective_Date1
   FROM
      {{ ref('int_m_demo_mapping3__rtrtrans__newgroup1') }}
)
SELECT
   sd.Title1 AS Title,
   sd.Gender_Code1 AS Gender,
   sd.First_Name1 AS First_Name,
   sd.Middle_Name1 AS Middle_Name,
   sd.Last_Name1 AS Last_Name,
   sd.Member_ID1 AS Member_Identifier,
   sd.Member_Suffix1 AS Member_Suffix,
   sd.Birth_Date1 AS Date_of_Birth,
   sd.Member_Record_Number1 AS Member_Number,
   sd.Social_Security_Number1 AS Soc_Number,
   sd.Member_Type_Code1 AS Type_Code,
   sd.Relationship_to_Subscriber_Code1 AS Relationship_to_Subscriber_Code,
   sd.Relationship_to_Subscriber_Code_Label1 AS Relationship_to_Subscriber_Code_Label,
   sd.Original_Effective_Date1 AS Effective_Date
FROM
   source_2 AS sd