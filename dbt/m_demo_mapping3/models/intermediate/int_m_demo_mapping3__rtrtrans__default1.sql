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
      o_Relationship_to_Subscriber_Code_Label AS Relationship_to_Subscriber_Code_Label
   FROM
      {{ ref('int_m_demo_mapping3__exptrans') }}
)
SELECT
   Title Title2,
   First_Name First_Name2,
   Middle_Name Middle_Name2,
   Last_Name Last_Name2,
   Member_ID Member_ID2,
   Member_Suffix Member_Suffix2,
   Birth_Date Birth_Date2,
   Gender_Code Gender_Code2,
   Member_Record_Number Member_Record_Number2,
   Social_Security_Number Social_Security_Number2,
   Member_Type_Code Member_Type_Code2,
   Original_Effective_Date Original_Effective_Date2,
   Relationship_to_Subscriber_Code Relationship_to_Subscriber_Code2,
   Relationship_to_Subscriber_Code_Label Relationship_to_Subscriber_Code_Label2
FROM
   source_data
WHERE
   NOT COALESCE((Social_Security_Number IS NULL), FALSE)
   AND NOT COALESCE(NOT (Social_Security_Number IS NULL), FALSE)