select
    *, cast(56 + row_number() over (order by ID) as {{ 'decimal(38,0)' if target.type == 'duckdb' else 'number(38,0)' }}) as NEXTVAL
from {{ ref('int_m_demo_mapping2__rtrtrans_insert') }}
