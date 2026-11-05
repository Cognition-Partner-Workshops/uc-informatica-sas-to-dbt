select LEAD_CO_MNE, BRANCH_CO_MNE, MIS_DATE, ID, DESCRIPTION, SHORT_NAME
from {{ ref('stg_m_demo_mapping2__demo_source1') }}
