-- daily_transaction_processing step 4a: 90-day per-account statistics from
-- the curated history (before the day's feed is appended).
select
    account_id,
    avg(abs(transaction_amount)) as avg_txn_amt,
    stddev_samp(abs(transaction_amount)) as std_txn_amt,
    count(*) as txn_count
from {{ ref('stg_daily_transactions_hist') }}
where transaction_date >= cast('{{ var("run_date") }}' as date)
                           - interval '{{ var("txn_history_days") }} days'
group by account_id
