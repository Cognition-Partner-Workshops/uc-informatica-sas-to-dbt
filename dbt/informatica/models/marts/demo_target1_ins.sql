{{ config(tags=['informatica', 's_m_demo_mapping2']) }}

/*
  RECOVERED: demo_target1_INS receives the Insert router group and the
  SEQTRANS-generated Key, source fields, and created audit ports.
  RECOVERED: UPDATED_BY, UPDATED_TIME, ACTIVE_FLAG, START_DATE, and END_DATE
  have no connectors for this target instance and are typed NULLs.
*/
select
    Key,
    LEAD_CO_MNE,
    BRANCH_CO_MNE,
    MIS_DATE,
    ID,
    DESCRIPTION,
    SHORT_NAME,
    o_CREATED_BY as CREATED_BY,
    o_CREATED_TIME as CREATED_TIME,
    cast(null as VARCHAR) as UPDATED_BY,
    cast(null as TIMESTAMP) as UPDATED_TIME,
    cast(null as VARCHAR) as ACTIVE_FLAG,
    cast(null as TIMESTAMP) as START_DATE,
    cast(null as TIMESTAMP) as END_DATE
from {{ ref('int_m2__rtr_insert') }}
