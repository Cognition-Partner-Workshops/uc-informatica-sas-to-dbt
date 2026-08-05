select
    LEAD_CO_MNE,
    BRANCH_CO_MNE,
    MIS_DATE,
    ID,
    DESCRIPTION,
    SHORT_NAME
from {% if target.type == 'duckdb' %}{{ source('legacy_informatica_m2', 'demo_source1') }}{% else %}{{ ref('demo_source1') }}{% endif %}
