select
    s.LEAD_CO_MNE, s.BRANCH_CO_MNE, s.MIS_DATE, s.ID, s.DESCRIPTION, s.SHORT_NAME,
    p.DIM_KEY,
    case when p.DIM_KEY is null then 'Insert' end as NEW_FLAG,
    md5(s.LEAD_CO_MNE || s.BRANCH_CO_MNE || s.MIS_DATE || s.DESCRIPTION || s.SHORT_NAME) as MD5_TGT,
    -- Preserve the supplied baseline's AES-vs-MD5 anomaly, not normal SCD detection.
    case when p.DIM_KEY is not null then 'Update' end as CHANGED_FLAG,
    cast('IDWUSER' as varchar) as O_CREATED_BY,
    cast('2024-01-31 00:00:00' as {{ 'timestamp' if target.type == 'duckdb' else 'timestamp_ntz(6)' }}) as O_CREATED_TIME,
    cast('IDWUSER' as varchar) as O_UPDATED_BY,
    cast('2024-01-31 00:00:00' as {{ 'timestamp' if target.type == 'duckdb' else 'timestamp_ntz(6)' }}) as O_UPDATED_TIME
from {{ ref('int_m_demo_mapping2__sq_demo_source1') }} s
left join {{ ref('int_m_demo_mapping2__lkptrans') }} p on p.ID = s.ID
