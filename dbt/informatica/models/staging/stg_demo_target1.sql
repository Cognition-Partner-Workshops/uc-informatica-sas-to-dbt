{{ config(tags=['informatica', 's_m_demo_mapping2']) }}

/*
  RECOVERED: columns are direct target-field pass-throughs from the
  demo_target1 TARGET and TARGETFIELD elements in wf_demo_mapping.XML.
  DECISION: __deterministic_row_order uses descending "KEY" and then
  descending data values instead of physical file order. This reproduces
  Informatica's Use Any Value behavior as resolved by the baseline.
  RECOVERED: mapping 2 lookup policy is "Use Any Value" on ID.
*/
with ranked as (
    select
        "Key" as "KEY",
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
        END_DATE,
        row_number() over (
            partition by ID
            order by
                "Key" desc nulls last,
                LEAD_CO_MNE desc nulls last,
                BRANCH_CO_MNE desc nulls last,
                MIS_DATE desc nulls last,
                DESCRIPTION desc nulls last,
                SHORT_NAME desc nulls last,
                CREATED_BY desc nulls last,
                CREATED_TIME desc nulls last,
                UPDATED_BY desc nulls last,
                UPDATED_TIME desc nulls last,
                ACTIVE_FLAG desc nulls last,
                START_DATE desc nulls last,
                END_DATE desc nulls last
        ) as __deterministic_row_order
    from {{ ref('demo_target1') }}
)
select
    "KEY",
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
from ranked
where __deterministic_row_order = 1
