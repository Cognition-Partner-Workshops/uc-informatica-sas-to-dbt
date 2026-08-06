{{ config(tags=['informatica', 's_m_demo_mapping2']) }}

/*
  RECOVERED: UPDTRANS uses DD_UPDATE and passes the Update router branch
  through to the target. DD_UPDATE is a row flag, not a column value; this
  model therefore represents the set of rows marked for update.
*/
select
    Key,
    LEAD_CO_MNE,
    BRANCH_CO_MNE,
    MIS_DATE,
    ID,
    DESCRIPTION,
    SHORT_NAME,
    o_UPDATED_BY,
    o_UPDATED_TIME
from {{ ref('int_m2__rtr_upd') }}
