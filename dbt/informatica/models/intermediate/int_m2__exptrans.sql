{{ config(tags=['informatica', 's_m_demo_mapping2']) }}

/*
  RECOVERED: EXPTRANS passes through demo_source1 fields and receives Key and
  lookup LEAD_CO_MNE as LEAD_CO_MNE1 from LKPTRANS on ID = ID1.
  RECOVERED: New_Flag is IIF(ISNULL(Key),'Insert'); o_CREATED_BY and
  o_UPDATED_BY are 'IDWUSER'; the time ports are SYSDATE.
  RECOVERED + defect: the legacy MD5_src local variable decrypts lookup
  LEAD_CO_MNE1 while MD5_tgt hashes source fields, so their value spaces are
  incomparable and every matched row is an Update. This intentionally models
  Changed_Flag as matched-row presence, rather than implementing real change
  detection, as in tools/informatica_baseline.py.
*/
select
    s.LEAD_CO_MNE,
    s.BRANCH_CO_MNE,
    s.MIS_DATE,
    s.ID,
    s.DESCRIPTION,
    s.SHORT_NAME,
    p.Key,
    p.LEAD_CO_MNE as LEAD_CO_MNE1,
    case when p.Key is null then 'Insert' else null end as New_Flag,
    case when p.Key is not null then 'Update' else null end as Changed_Flag,
    'IDWUSER' as o_CREATED_BY,
    {{ business_timestamp() }} as o_CREATED_TIME,
    'IDWUSER' as o_UPDATED_BY,
    {{ business_timestamp() }} as o_UPDATED_TIME
from {{ ref('stg_demo_source1') }} s
left join {{ ref('stg_demo_target1') }} p
    on p.ID = s.ID
