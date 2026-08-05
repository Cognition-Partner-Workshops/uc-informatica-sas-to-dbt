-- daily_transaction_processing step 1: sequential validation rules
-- (required fields, amount threshold, valid type, no future dating).
select f.*
from {{ ref('stg_txn_feed') }} f
where f.transaction_id is not null
  and f.account_id is not null
  and f.transaction_amount is not null
  and abs(f.transaction_amount) <= 10000000
  and f.transaction_type in ('DEP','WDR','TRF','PMT','FEE','INT','ADJ','REV','CHG','REF')
  -- SAS rejects only future-dated rows; a missing date sorts low and passes
  and (f.transaction_date <= cast('{{ var("run_date") }}' as date)
       or f.transaction_date is null)
