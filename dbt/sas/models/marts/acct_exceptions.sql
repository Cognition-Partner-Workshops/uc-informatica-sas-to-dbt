-- STG_BANK.ACCT_EXCEPTIONS: exception rows fired by the three sequential
-- data-quality rules. The legacy DATA-step DROP removes the exception
-- code/description from the output, and SNAPSHOT_DATE is not yet assigned
-- when exception rows are output (so it is null here).
select b.*, cast(null as date) as snapshot_date
from {{ ref('int_acct_base') }} b
where b.account_type in ('CHK', 'SAV', 'MMA', 'CD') and b.current_balance < 0

union all

select b.*, cast(null as date) as snapshot_date
from {{ ref('int_acct_base') }} b
where b.utilization_pct > 95

union all

select b.*, cast(null as date) as snapshot_date
from {{ ref('int_acct_base') }} b
where b.risk_rating is null
