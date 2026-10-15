select
    cast(TRANSACTION_ID as varchar) as TRANSACTION_ID,
    cast(ACCOUNT_ID as varchar) as ACCOUNT_ID,
    cast(TRANSACTION_DATE as date) as TRANSACTION_DATE,
    cast(TRANSACTION_TYPE as varchar) as TRANSACTION_TYPE,
    cast(TRANSACTION_AMOUNT as float) as TRANSACTION_AMOUNT,
    cast(CHANNEL as varchar) as CHANNEL,
    cast(MERCHANT_CATEGORY as number) as MERCHANT_CATEGORY,
    cast(DESCRIPTION as varchar) as DESCRIPTION,
    cast(POST_DATE as date) as POST_DATE,
    cast(CURRENCY_CODE as varchar) as CURRENCY_CODE
from {{ source('source_sf', 'CURATED_DAILY_TRANSACTIONS') }}
