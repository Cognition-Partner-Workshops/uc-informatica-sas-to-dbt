select * from {{ ref('int_m_demo_mapping2__exptrans') }}
where NEW_FLAG = 'Insert'
