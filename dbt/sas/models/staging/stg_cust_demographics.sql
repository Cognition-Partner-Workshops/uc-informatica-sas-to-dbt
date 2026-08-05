select * from {{ source('ora_dw', 'cust_demographics') }}
