-- depends_on: {{ ref('demo_target1_ins') }}
-- depends_on: {{ ref('demo_target1_upd') }}
-- depends_on: {{ ref('stg_demo_target1_pre') }}

{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key='Key',
        merge_update_columns=[
            'LEAD_CO_MNE',
            'BRANCH_CO_MNE',
            'MIS_DATE',
            'ID',
            'DESCRIPTION',
            'SHORT_NAME',
            'UPDATED_BY',
            'UPDATED_TIME'
        ]
    )
}}

/*
The first/full-refresh run is the pre-existing target state. Incremental runs
merge the union of the INSERT and UPDATE target payloads by surrogate Key.
The update column list intentionally preserves CREATED_*, ACTIVE_FLAG,
START_DATE, and END_DATE from the pre-existing row.
*/
{% if is_incremental() %}
select * from {{ ref('demo_target1_ins') }}
union all
select * from {{ ref('demo_target1_upd') }}
{% else %}
select
    Key,
    LEAD_CO_MNE,
    BRANCH_CO_MNE,
    MIS_DATE,
    ID,
    DESCRIPTION,
    SHORT_NAME,
    CREATED_BY,
    CREATED_TIME,
    UPDATED_BY,
    UPDATED_TIME,
    ACTIVE_FLAG,
    START_DATE,
    END_DATE
from {{ ref('stg_demo_target1_pre') }}
{% endif %}
