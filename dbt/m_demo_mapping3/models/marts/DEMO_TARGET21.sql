--** SSC-FDM-INF0029 - INFORMATICA LOADS TARGETS SEQUENTIALLY PER TARGETLOADORDER. THE TRANSLATED DBT MODEL USES UNION ALL TO COMBINE ALL PIPELINES INTO A SINGLE ATOMIC QUERY. IF PIPELINE EXECUTION ORDER AFFECTS THE FINAL RESULT, REVIEW THE GENERATED MODEL. **
WITH source_1 AS
(
   SELECT
      Title3,
      Gender_Code3,
      First_Name3,
      Middle_Name3,
      Last_Name3,
      Member_ID3,
      Member_Suffix3,
      Birth_Date3,
      Member_Record_Number3,
      Social_Security_Number3,
      Member_Type_Code3,
      Relationship_to_Subscriber_Code3,
      Relationship_to_Subscriber_Code_Label3,
      Original_Effective_Date3
   FROM
      {{ ref('int_m_demo_mapping3__rtrtrans__newgroup2') }}
)
SELECT
   sd.Title3 AS Title,
   sd.Gender_Code3 AS Gender,
   sd.First_Name3 AS First_Name,
   sd.Middle_Name3 AS Middle_Name,
   sd.Last_Name3 AS Last_Name,
   sd.Member_ID3 AS Member_Identifier,
   sd.Member_Suffix3 AS Member_Suffix,
   sd.Birth_Date3 AS Date_of_Birth,
   sd.Member_Record_Number3 AS Member_Number,
   sd.Social_Security_Number3 AS Soc_Number,
   sd.Member_Type_Code3 AS Type_Code,
   sd.Relationship_to_Subscriber_Code3 AS Relationship_to_Subscriber_Code,
   sd.Relationship_to_Subscriber_Code_Label3 AS Relationship_to_Subscriber_Code_Label,
   sd.Original_Effective_Date3 AS Effective_Date
FROM
   source_1 AS sd
