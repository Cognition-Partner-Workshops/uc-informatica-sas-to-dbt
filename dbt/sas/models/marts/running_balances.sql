-- CURATED.RUNNING_BALANCES: per-transaction cumulative balance.
select
    account_id,
    transaction_date,
    transaction_id,
    running_balance
from {{ ref('int_txn_with_balance') }}
