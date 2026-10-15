with transactions_with_balance as (
    select *
    from {{ ref('int_daily_transaction_processing__txn_with_balance') }}
),
transaction_stats as (
    select *
    from {{ ref('int_daily_transaction_processing__txn_stats') }}
),
scored_transactions as (
    select
        e.*,
        s.AVG_TXN_AMT,
        s.STD_TXN_AMT,
        case
            when s.STD_TXN_AMT > 0
                then (abs(e.TRANSACTION_AMOUNT) - s.AVG_TXN_AMT) / s.STD_TXN_AMT
        end as Z_SCORE
    from transactions_with_balance e
    left join transaction_stats s
        on e.ACCOUNT_ID = s.ACCOUNT_ID
),
classified_transactions as (
    select
        s.*,
        case
            when s.Z_SCORE > 3 then 'HIGH_AMOUNT'
            when s.RUNNING_BALANCE < 0 or s.RUNNING_BALANCE is null then 'OVERDRAFT'
            when s.TRANSACTION_TYPE = 'WDR'
                and (s.PRE_TXN_BALANCE is null or abs(s.TRANSACTION_AMOUNT) > s.PRE_TXN_BALANCE * 0.9)
                then 'LARGE_WITHDRAWAL'
            when nullif(trim(s.CUSTOMER_ID), '') is null then 'ORPHAN_ACCOUNT'
            else ''
        end as ANOMALY_TYPE
    from scored_transactions s
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
    CURRENCY_CODE,
    ACCOUNT_TYPE,
    CUSTOMER_ID,
    CUSTOMER_SEGMENT,
    REGION_CODE,
    BRANCH_ID,
    PRE_TXN_BALANCE,
    POST_TXN_BALANCE,
    RISK_RATING,
    RUNNING_BALANCE,
    AVG_TXN_AMT,
    STD_TXN_AMT,
    Z_SCORE,
    ANOMALY_TYPE
from classified_transactions
where ANOMALY_TYPE <> ''
