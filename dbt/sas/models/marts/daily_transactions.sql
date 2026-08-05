-- CURATED.DAILY_TRANSACTIONS: history plus the day's validated feed.
-- PROC APPEND FORCE keeps only the base table's 10 feed columns.
select
    transaction_id, account_id, transaction_date, transaction_type,
    transaction_amount, channel, merchant_category, description,
    post_date, currency_code
from {{ ref('stg_daily_transactions_hist') }}

union all

select
    transaction_id, account_id, transaction_date, transaction_type,
    transaction_amount, channel, merchant_category, description,
    post_date, currency_code
from {{ ref('int_txn_with_balance') }}
