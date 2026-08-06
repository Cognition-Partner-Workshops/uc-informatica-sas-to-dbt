{{ config(tags=['informatica', 's_m_demo_mapping1']) }}

/*
  RECOVERED: all columns are direct source-field pass-throughs from the
  demo_source3 SOURCE and SOURCEFIELD elements in wf_demo_mapping.XML.
*/
select *
from {{ ref('demo_source3') }}
