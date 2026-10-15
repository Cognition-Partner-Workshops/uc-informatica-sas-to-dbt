SELECT
   $1 :: VARCHAR(50) AS LEAD_CO_MNE,
   $2 :: VARCHAR(50) AS BRANCH_CO_MNE,
   $3 :: VARCHAR(29) AS MIS_DATE,
   $4 :: VARCHAR(50) AS ID,
   $5 :: VARCHAR(120) AS DESCRIPTION,
   $6 :: VARCHAR(50) AS SHORT_NAME
FROM
   @public.landing_stage/infpc/sources/RTUS/demo_source1/demo_source1 (FILE_FORMAT => 'RTUS_m_demo_mapping2_demo_source1')