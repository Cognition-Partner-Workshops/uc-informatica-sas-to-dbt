{{ config(tags=['informatica', 's_m_demo_mapping3']) }}

/*
  RECOVERED: all columns are direct source-field pass-throughs from the
  demo_source2 SOURCE and SOURCEFIELD elements in wf_demo_mapping.XML.
*/
select *
from {{ ref('demo_source2') }}
