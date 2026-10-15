with validated as (
    select *
    from {{ ref('int_daily_transaction_processing__txn_validated') }}
),
accounts as (
    select *
    from {{ ref('stg_daily_transaction_processing__cust_accounts_daily') }}
)
select
    t.TRANSACTION_ID,
    t.ACCOUNT_ID,
    t.TRANSACTION_DATE,
    t.TRANSACTION_TYPE,
    t.TRANSACTION_AMOUNT,
    t.CHANNEL,
    t.MERCHANT_CATEGORY,
    t.DESCRIPTION,
    t.POST_DATE,
    t.CURRENCY_CODE,
    a.ACCOUNT_TYPE,
    a.CUSTOMER_ID,
    a.CUSTOMER_SEGMENT,
    a.REGION_CODE,
    a.BRANCH_ID,
    a.CURRENT_BALANCE as PRE_TXN_BALANCE,
    case
        when t.TRANSACTION_TYPE in ('DEP', 'INT', 'REF', 'REV')
            then a.CURRENT_BALANCE + t.TRANSACTION_AMOUNT
        when t.TRANSACTION_TYPE in ('WDR', 'PMT', 'FEE', 'CHG')
            then a.CURRENT_BALANCE - abs(t.TRANSACTION_AMOUNT)
        when t.TRANSACTION_TYPE in ('TRF', 'ADJ')
            then a.CURRENT_BALANCE + t.TRANSACTION_AMOUNT
        else a.CURRENT_BALANCE
    end as POST_TXN_BALANCE,
    a.RISK_RATING
from validated t
left join accounts a
    on t.ACCOUNT_ID = a.ACCOUNT_ID
