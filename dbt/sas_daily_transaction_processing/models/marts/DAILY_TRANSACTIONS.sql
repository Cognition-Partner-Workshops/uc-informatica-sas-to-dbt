with curated_history as (
    select
        TRANSACTION_ID,
        ACCOUNT_ID,
        TRANSACTION_DATE,
        TRANSACTION_TYPE,
        TRANSACTION_AMOUNT,
        CHANNEL,
        MERCHANT_CATEGORY,
        DESCRIPTION,
        POST_DATE,
        CURRENCY_CODE
    from {{ ref('stg_daily_transaction_processing__curated_daily_transactions') }}
),
current_transactions as (
    select
        TRANSACTION_ID,
        ACCOUNT_ID,
        TRANSACTION_DATE,
        TRANSACTION_TYPE,
        TRANSACTION_AMOUNT,
        CHANNEL,
        MERCHANT_CATEGORY,
        DESCRIPTION,
        POST_DATE,
        CURRENCY_CODE
    from {{ ref('int_daily_transaction_processing__txn_with_balance') }}
)
select
    TRANSACTION_ID,
    ACCOUNT_ID,
    TRANSACTION_DATE,
    TRANSACTION_TYPE,
    TRANSACTION_AMOUNT,
    CHANNEL,
    MERCHANT_CATEGORY,
    DESCRIPTION,
    POST_DATE,
    CURRENCY_CODE
from curated_history
union all
select
    TRANSACTION_ID,
    ACCOUNT_ID,
    TRANSACTION_DATE,
    TRANSACTION_TYPE,
    TRANSACTION_AMOUNT,
    CHANNEL,
    MERCHANT_CATEGORY,
    DESCRIPTION,
    POST_DATE,
    CURRENCY_CODE
from current_transactions
