-- daily_transaction_processing steps 2-3: enrich with the account snapshot
-- and compute the RETAIN/BY-group running balance as a window sum seeded
-- from the account's snapshot balance.
with enriched as (
    select
        t.transaction_id,
        t.account_id,
        t.transaction_date,
        t.transaction_type,
        t.transaction_amount,
        t.channel,
        t.merchant_category,
        t.description,
        t.post_date,
        t.currency_code,
        a.account_type,
        a.customer_id,
        a.customer_segment,
        a.region_code,
        a.branch_id,
        a.current_balance as pre_txn_balance,
        case
            when t.transaction_type in ('DEP', 'INT', 'REF', 'REV')
                then a.current_balance + t.transaction_amount
            when t.transaction_type in ('WDR', 'PMT', 'FEE', 'CHG')
                then a.current_balance - abs(t.transaction_amount)
            when t.transaction_type in ('TRF', 'ADJ')
                then a.current_balance + t.transaction_amount
            else a.current_balance
        end as post_txn_balance,
        a.risk_rating,
        case
            when t.transaction_type in ('DEP', 'INT', 'REF', 'REV')
                then t.transaction_amount
            when t.transaction_type in ('WDR', 'PMT', 'FEE', 'CHG')
                then -abs(t.transaction_amount)
            when t.transaction_type in ('TRF', 'ADJ')
                then t.transaction_amount
            else 0
        end as bal_delta
    from {{ ref('int_txn_validated') }} t
    left join {{ ref('cust_accounts_daily') }} a
        on t.account_id = a.account_id
)

select
    transaction_id,
    account_id,
    transaction_date,
    transaction_type,
    transaction_amount,
    channel,
    merchant_category,
    description,
    post_date,
    currency_code,
    account_type,
    customer_id,
    customer_segment,
    region_code,
    branch_id,
    pre_txn_balance,
    post_txn_balance,
    risk_rating,
    pre_txn_balance + sum(bal_delta) over (
        partition by account_id
        order by transaction_date, transaction_id
        rows between unbounded preceding and current row
    ) as running_balance
from enriched
