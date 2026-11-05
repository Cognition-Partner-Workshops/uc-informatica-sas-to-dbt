select
    s.*,
    p.key,
    p.lead_co_mne as lead_co_mne1,
    case when p.key is null then 'Insert' end as new_flag,
    cast('LEGACY_AES_VALUE' as varchar) as md5_src,
    md5(s.lead_co_mne || s.branch_co_mne || s.mis_date || s.description || s.short_name) as md5_tgt,
    case when p.key is not null then 'Update' end as changed_flag,
    'IDWUSER' as o_created_by,
    '2024-01-31 00:00:00'::timestamp_ntz as o_created_time,
    'IDWUSER' as o_updated_by,
    '2024-01-31 00:00:00'::timestamp_ntz as o_updated_time
from {{ ref('int_m_demo_mapping2__sq') }} s
left join {{ ref('int_m_demo_mapping2__lookup') }} p on p.id = s.id
