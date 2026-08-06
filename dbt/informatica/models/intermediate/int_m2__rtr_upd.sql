{{ config(tags=['informatica', 's_m_demo_mapping2']) }}

/*
  RECOVERED: RTRTRANS Update group filters Changed_Flag='Update' and forwards
  the lookup Key plus source and updated audit ports.
  RECOVERED + defect: every matched row reaches this group because the legacy
  AES_DECRYPT lookup value and MD5 source digest cannot compare meaningfully.
*/
select
    Key,
    LEAD_CO_MNE,
    BRANCH_CO_MNE,
    MIS_DATE,
    ID,
    DESCRIPTION,
    SHORT_NAME,
    o_UPDATED_BY,
    o_UPDATED_TIME
from {{ ref('int_m2__exptrans') }}
where Changed_Flag = 'Update'
