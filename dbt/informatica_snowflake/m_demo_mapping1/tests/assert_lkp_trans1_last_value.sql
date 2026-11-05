-- lkp_TRANS1 "Use Last Value": ACCT_ID 1002 has TR then DR in lkp_demo_source3.
select ACCT_ID, TX_TYPE_CD
from {{ ref('DEMO_TARGET6') }}
where ACCT_ID = 1002 and TX_TYPE_CD is distinct from 'DR'
union all
select 1002, null
where not exists (select 1 from {{ ref('DEMO_TARGET6') }} where ACCT_ID = 1002)
