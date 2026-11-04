select DIM_KEY, LEAD_CO_MNE, BRANCH_CO_MNE, MIS_DATE, ID, DESCRIPTION, SHORT_NAME
from {{ ref('stg_m_demo_mapping2__demo_target1') }}
qualify row_number() over (
    partition by ID order by DIM_KEY desc nulls last, SEED_ROW desc
) = 1
