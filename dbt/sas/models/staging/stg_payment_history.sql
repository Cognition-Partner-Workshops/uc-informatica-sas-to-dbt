select * from {{ source('ora_dw', 'payment_history') }}
