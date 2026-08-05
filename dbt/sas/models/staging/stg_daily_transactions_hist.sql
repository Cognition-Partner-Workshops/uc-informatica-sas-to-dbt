select * from {{ source('curated_src', 'daily_transactions') }}
