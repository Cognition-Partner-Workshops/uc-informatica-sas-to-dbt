select * from {{ source('ora_dw', 'loan_details') }}
