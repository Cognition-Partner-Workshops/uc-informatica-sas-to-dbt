select * from {{ source('ora_dw', 'bureau_scores') }}
