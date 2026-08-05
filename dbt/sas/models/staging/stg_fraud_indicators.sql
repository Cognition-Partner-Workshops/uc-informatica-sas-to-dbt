select * from {{ source('raw_ins', 'fraud_indicators') }}
