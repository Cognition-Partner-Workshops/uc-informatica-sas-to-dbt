with enriched as (
    select *
    from {{ ref('int_daily_transaction_processing__txn_enriched') }}
),
transaction_deltas as (
    select
        e.*,
        case
            when e.TRANSACTION_TYPE in ('DEP', 'INT', 'REF', 'REV') then e.TRANSACTION_AMOUNT
            when e.TRANSACTION_TYPE in ('WDR', 'PMT', 'FEE', 'CHG') then -abs(e.TRANSACTION_AMOUNT)
            when e.TRANSACTION_TYPE in ('TRF', 'ADJ') then e.TRANSACTION_AMOUNT
            else 0
        end as TXN_BALANCE_DELTA
    from enriched e
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
    t.ACCOUNT_TYPE,
    t.CUSTOMER_ID,
    t.CUSTOMER_SEGMENT,
    t.REGION_CODE,
    t.BRANCH_ID,
    t.PRE_TXN_BALANCE,
    t.POST_TXN_BALANCE,
    t.RISK_RATING,
    t.PRE_TXN_BALANCE
        + sum(t.TXN_BALANCE_DELTA) over (
            partition by t.ACCOUNT_ID
            order by t.TRANSACTION_DATE nulls first, t.TRANSACTION_ID nulls first
            rows between unbounded preceding and current row
        ) as RUNNING_BALANCE
from transaction_deltas t
