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
   Title Title3,
   First_Name First_Name3,
   Middle_Name Middle_Name3,
   Last_Name Last_Name3,
   Member_ID Member_ID3,
   Member_Suffix Member_Suffix3,
   Birth_Date Birth_Date3,
   Gender_Code Gender_Code3,
   Member_Record_Number Member_Record_Number3,
   Social_Security_Number Social_Security_Number3,
   Member_Type_Code Member_Type_Code3,
   Original_Effective_Date Original_Effective_Date3,
   Relationship_to_Subscriber_Code Relationship_to_Subscriber_Code3,
   Relationship_to_Subscriber_Code_Label Relationship_to_Subscriber_Code_Label3
FROM
   source_data
WHERE
   NOT (Social_Security_Number IS NULL)