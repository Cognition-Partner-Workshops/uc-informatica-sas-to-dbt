{{ config(tags=['informatica', 's_m_demo_mapping2']) }}

/*
  RECOVERED: all columns are direct source-field pass-throughs from the
  demo_source1 SOURCE and SOURCEFIELD elements in wf_demo_mapping.XML.
*/
select *
from {{ ref('demo_source1') }}
