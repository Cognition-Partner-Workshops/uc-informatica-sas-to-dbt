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
      {{ ref('int_EXPTRANS') }}
)
SELECT
   Title Title1,
   First_Name First_Name1,
   Middle_Name Middle_Name1,
   Last_Name Last_Name1,
   Member_ID Member_ID1,
   Member_Suffix Member_Suffix1,
   Birth_Date Birth_Date1,
   Gender_Code Gender_Code1,
   Member_Record_Number Member_Record_Number1,
   Social_Security_Number Social_Security_Number1,
   Member_Type_Code Member_Type_Code1,
   Original_Effective_Date Original_Effective_Date1,
   Relationship_to_Subscriber_Code Relationship_to_Subscriber_Code1,
   Relationship_to_Subscriber_Code_Label Relationship_to_Subscriber_Code_Label1
FROM
   source_data
WHERE
   (Social_Security_Number IS NULL)