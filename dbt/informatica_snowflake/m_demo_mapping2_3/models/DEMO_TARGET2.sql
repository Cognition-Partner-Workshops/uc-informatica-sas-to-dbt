select * from {{ ref('m3_expression') }} where Soc_Number is null
