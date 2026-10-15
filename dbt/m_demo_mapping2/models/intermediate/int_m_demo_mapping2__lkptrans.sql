WITH lookup_reference AS
(
   SELECT
      Key ,
      LEAD_CO_MNE ,
      BRANCH_CO_MNE ,
      MIS_DATE ,
      ID ,
      DESCRIPTION ,
      SHORT_NAME ,
      CREATED_BY ,
      CREATED_TIME ,
      UPDATED_BY ,
      UPDATED_TIME ,
      ACTIVE_FLAG ,
      START_DATE ,
      END_DATE
   FROM
      {{ source('lkptrans', 'demo_target1') }}
   QUALIFY
      ROW_NUMBER() OVER (
      PARTITION BY
         UPPER(ID)
      ORDER BY
         Key DESC, SEED_ROW DESC) = 1
),
input_data AS
(
   SELECT
      ID ID1,
      LEAD_CO_MNE SQ_demo_source1__LEAD_CO_MNE,
      BRANCH_CO_MNE SQ_demo_source1__BRANCH_CO_MNE,
      MIS_DATE SQ_demo_source1__MIS_DATE,
      ID SQ_demo_source1__ID,
      DESCRIPTION SQ_demo_source1__DESCRIPTION,
      SHORT_NAME SQ_demo_source1__SHORT_NAME
   FROM
      {{ ref('stg_m_demo_mapping2__sq_demo_source1') }}
)
SELECT
   input_data.ID1 ,
   input_data.SQ_demo_source1__LEAD_CO_MNE ,
   input_data.SQ_demo_source1__BRANCH_CO_MNE ,
   input_data.SQ_demo_source1__MIS_DATE ,
   input_data.SQ_demo_source1__ID ,
   input_data.SQ_demo_source1__DESCRIPTION ,
   input_data.SQ_demo_source1__SHORT_NAME ,
   lookup_reference.Key,
   lookup_reference.LEAD_CO_MNE,
   lookup_reference.BRANCH_CO_MNE,
   lookup_reference.MIS_DATE,
   lookup_reference.ID,
   lookup_reference.DESCRIPTION,
   lookup_reference.SHORT_NAME,
   lookup_reference.CREATED_BY,
   lookup_reference.CREATED_TIME,
   lookup_reference.UPDATED_BY,
   lookup_reference.UPDATED_TIME,
   lookup_reference.ACTIVE_FLAG,
   lookup_reference.START_DATE,
   lookup_reference.END_DATE
FROM
   --** SSC-FDM-INF0088 - CONNECTED LOOKUP 'LKPTRANS' USES CASE-INSENSITIVE STRING COMPARISON ('CASE SENSITIVE STRING COMPARISON' = NO), BUT THE EMITTED JOIN CONDITION IS CASE-SENSITIVE. LOOKUP MATCHES MAY DIFFER FROM POWERCENTER. **
   input_data
   LEFT JOIN
      lookup_reference
      ON UPPER(lookup_reference.ID) = UPPER(input_data.ID1)