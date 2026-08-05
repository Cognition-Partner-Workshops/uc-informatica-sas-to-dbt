select * from {{ source('ora_dw', 'collateral') }}
