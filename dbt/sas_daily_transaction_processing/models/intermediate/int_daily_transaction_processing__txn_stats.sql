with run_parameters as (
    select to_date('{{ var("txn_date") }}') as txn_date
),
curated_history as (
    select *
    from {{ ref('stg_daily_transaction_processing__curated_daily_transactions') }}
)
select
    h.ACCOUNT_ID,
    avg(abs(h.TRANSACTION_AMOUNT)) as AVG_TXN_AMT,
    stddev_samp(abs(h.TRANSACTION_AMOUNT)) as STD_TXN_AMT,
    count(*) as TXN_COUNT
from curated_history h
cross join run_parameters p
where h.TRANSACTION_DATE >= dateadd('day', -90, p.txn_date)
group by h.ACCOUNT_ID
