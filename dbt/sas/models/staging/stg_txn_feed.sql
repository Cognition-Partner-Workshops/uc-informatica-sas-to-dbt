select * from {{ source('raw_bank', 'txn_feed_20240131') }}
