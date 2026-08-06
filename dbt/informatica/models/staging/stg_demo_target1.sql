{{ config(tags=['informatica', 's_m_demo_mapping2']) }}

/*
  RECOVERED: columns are direct target-field pass-throughs from the
  demo_target1 TARGET and TARGETFIELD elements in wf_demo_mapping.XML.
  DECISION: SEED_ROW is a warehouse-portable ordinal generated from the
  legacy file's physical data-row order; physical file order is not otherwise
  representable in a warehouse table.
  RECOVERED: mapping 2's "Use Any Value" policy selects highest Key per ID,
  with SEED_ROW desc as the recovered physical-row tie-breaker.
*/
with ranked as (
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
        END_DATE,
        SEED_ROW,
        row_number() over (
            partition by ID
            order by
                Key desc,
                SEED_ROW desc
        ) as __deterministic_row_order
    from {{ ref('demo_target1') }}
)
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
from ranked
where __deterministic_row_order = 1
