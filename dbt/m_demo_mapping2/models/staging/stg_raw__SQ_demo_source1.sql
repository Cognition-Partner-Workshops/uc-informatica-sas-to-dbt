SELECT
   demo_source1.LEAD_CO_MNE AS LEAD_CO_MNE,
   demo_source1.BRANCH_CO_MNE AS BRANCH_CO_MNE,
   demo_source1.MIS_DATE AS MIS_DATE,
   demo_source1.ID AS ID,
   demo_source1.DESCRIPTION AS DESCRIPTION,
   demo_source1.SHORT_NAME AS SHORT_NAME
FROM
   {{ ref('stg_flat_file__demo_source1') }} AS demo_source1