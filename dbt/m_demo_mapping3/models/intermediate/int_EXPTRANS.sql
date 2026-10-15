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
      {{ ref('stg_raw__SQ_demo_source2') }}
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
   NVL(Relationship_to_Subscriber_Code_Label,
   !!!RESOLVE EWI!!! /*** SSC-EWI-INF0060 - INFORMATICA POWERCENTER ABORT() IMMEDIATELY STOPS THE INTEGRATION SERVICE SESSION AND MARKS IT AS FAILED. THERE IS NO EQUIVALENT SESSION-ABORT MECHANISM IN SNOWFLAKE SQL. THE FUNCTION IS REPLACED WITH NULL. IMPLEMENT THE REQUIRED ERROR-HANDLING LOGIC USING SNOWFLAKE STREAMS, TASKS, OR PRE/POST SQL SCRIPTS. ***/!!!
   NULL) AS o_Relationship_to_Subscriber_Code_Label
FROM
   source_data