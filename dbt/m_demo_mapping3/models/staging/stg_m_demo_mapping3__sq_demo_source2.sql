--** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "demo_source2" **
SELECT
   demo_source2.Title,
   demo_source2.First_Name,
   demo_source2.Middle_Name,
   demo_source2.Last_Name,
   demo_source2.Member_ID,
   demo_source2.Member_Suffix,
   TO_DATE({{ epoch_us_repair('demo_source2.Birth_Date') }}) AS Birth_Date,
   demo_source2.Gender_Code,
   demo_source2.Member_Record_Number,
   demo_source2.Social_Security_Number,
   demo_source2.Member_Type_Code,
   TO_DATE({{ epoch_us_repair('demo_source2.Original_Effective_Date') }}) AS Original_Effective_Date,
   demo_source2.Relationship_to_Subscriber_Code,
   demo_source2.Relationship_to_Subscriber_Code_Label
FROM
   {{ source('raw', 'demo_source2') }} AS demo_source2
where
   demo_source2.Member_Type_Code is not null