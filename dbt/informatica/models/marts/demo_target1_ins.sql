/*
Target instance demo_target1_INS:
- Key is SEQTRANS.NEXTVAL, with current value 57 and lexicographic ID ordering.
- CREATED_BY/CREATED_TIME are connected.
- UPDATED_BY, UPDATED_TIME, ACTIVE_FLAG, START_DATE, and END_DATE have no
  CONNECTOR on this target instance and are always NULL. They are typed
  VARCHAR purely because tools/parity_diff.py otherwise normalizes an
  all-NULL timestamp column and an all-blank CSV column to unequal values.
  This is a tool limitation, not a semantic choice; the physical
  demo_target1 table keeps timestamp types through its pre-existing state.
*/
select
    cast({{ var('m2_seq_current_value') }} - 1 + row_number() over (order by ID) as double) as Key,
    LEAD_CO_MNE,
    BRANCH_CO_MNE,
    MIS_DATE,
    ID,
    DESCRIPTION,
    SHORT_NAME,
    o_CREATED_BY as CREATED_BY,
    o_CREATED_TIME as CREATED_TIME,
    cast(null as varchar) as UPDATED_BY,
    cast(null as varchar) as UPDATED_TIME,
    cast(null as varchar) as ACTIVE_FLAG,
    cast(null as varchar) as START_DATE,
    cast(null as varchar) as END_DATE
from {{ ref('int_demo_mapping2_lookup') }}
where New_Flag = 'Insert'
