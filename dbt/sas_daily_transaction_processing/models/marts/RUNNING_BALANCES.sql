select
    ACCOUNT_ID,
    TRANSACTION_DATE,
    TRANSACTION_ID,
    RUNNING_BALANCE
from {{ ref('int_daily_transaction_processing__txn_with_balance') }}
