{{ config(tags=['informatica', 's_m_demo_mapping2']) }}

/*
  RECOVERED: RTRTRANS Insert group filters New_Flag='Insert' and forwards the
  source and created audit ports to demo_target1_INS.
  RECOVERED: SEQTRANS has start 0 and current 57, so the first emitted key is
  57 and the key expression is 56 + row_number().
  DECISION: order inserted rows by ID to make sequence assignment repeatable;
  physical source-file order or arbitrary order was rejected because it is not
  portable or deterministic in a warehouse.
*/
select
    56 + row_number() over (order by ID) as Key,
    LEAD_CO_MNE,
    BRANCH_CO_MNE,
    MIS_DATE,
    ID,
    DESCRIPTION,
    SHORT_NAME,
    o_CREATED_BY,
    o_CREATED_TIME
from {{ ref('int_m2__exptrans') }}
where New_Flag = 'Insert'
