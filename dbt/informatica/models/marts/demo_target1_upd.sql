/*
Target instance demo_target1_UPD:
- Key is the deduplicated lookup Key, not ID.
- CREATED_BY/CREATED_TIME, ACTIVE_FLAG, START_DATE, and END_DATE have no
  CONNECTOR on this target instance and are always NULL. They are typed
  VARCHAR purely because tools/parity_diff.py otherwise normalizes an
  all-NULL timestamp column and an all-blank CSV column to unequal values.
  This is a tool limitation, not a semantic choice; the physical
  demo_target1 table keeps timestamp types through its pre-existing state.
- The connected update ports are UPDATED_BY and UPDATED_TIME.
*/
select
    cast(lookup_Key as double) as Key,
    LEAD_CO_MNE,
    BRANCH_CO_MNE,
    MIS_DATE,
    ID,
    DESCRIPTION,
    SHORT_NAME,
    cast(null as varchar) as CREATED_BY,
    cast(null as varchar) as CREATED_TIME,
    o_UPDATED_BY as UPDATED_BY,
    o_UPDATED_TIME as UPDATED_TIME,
    cast(null as varchar) as ACTIVE_FLAG,
    cast(null as varchar) as START_DATE,
    cast(null as varchar) as END_DATE
from {{ ref('int_demo_mapping2_lookup') }}
where Changed_Flag = 'Update'
