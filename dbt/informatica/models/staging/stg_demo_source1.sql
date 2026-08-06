{{ config(tags=['informatica', 's_m_demo_mapping2']) }}

/*
  RECOVERED: all columns are direct source-field pass-throughs from the
  demo_source1 SOURCE and SOURCEFIELD elements in wf_demo_mapping.XML.
*/
select
    LEAD_CO_MNE,
    BRANCH_CO_MNE,
    MIS_DATE,
    ID,
    DESCRIPTION,
    SHORT_NAME
from {{ ref('demo_source1') }}
