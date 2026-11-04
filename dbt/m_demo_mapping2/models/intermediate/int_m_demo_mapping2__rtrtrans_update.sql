select * from {{ ref('int_m_demo_mapping2__exptrans') }}
where CHANGED_FLAG = 'Update'
