{{ config(tags=['informatica', 's_m_demo_mapping2']) }}

/*
  RECOVERED: demo_target1_UPD receives the UPDTRANS Key from LKPTRANS, not
  SEQTRANS, together with source fields and updated audit ports.
  RECOVERED: CREATED_BY, CREATED_TIME, ACTIVE_FLAG, START_DATE, and END_DATE
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
    cast(null as VARCHAR) as CREATED_BY,
    cast(null as TIMESTAMP) as CREATED_TIME,
    o_UPDATED_BY as UPDATED_BY,
    o_UPDATED_TIME as UPDATED_TIME,
    cast(null as VARCHAR) as ACTIVE_FLAG,
    cast(null as TIMESTAMP) as START_DATE,
    cast(null as TIMESTAMP) as END_DATE
from {{ ref('int_m2__updtrans') }}
