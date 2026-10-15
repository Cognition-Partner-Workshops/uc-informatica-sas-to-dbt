with txn_feed as (
    select *
    from {{ ref('stg_daily_transaction_processing__txn_feed') }}
),
run_parameters as (
    select to_date('{{ var("txn_date") }}') as txn_date
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
    t.CURRENCY_CODE
from txn_feed t
cross join run_parameters p
where nullif(trim(t.TRANSACTION_ID), '') is not null
  and nullif(trim(t.ACCOUNT_ID), '') is not null
  and t.TRANSACTION_AMOUNT is not null
  and abs(t.TRANSACTION_AMOUNT) <= 10000000
  and t.TRANSACTION_TYPE in ('DEP', 'WDR', 'TRF', 'PMT', 'FEE', 'INT', 'ADJ', 'REV', 'CHG', 'REF')
  and (t.TRANSACTION_DATE <= p.txn_date or t.TRANSACTION_DATE is null)
