select *
from {{ ref('demo_target2') }}
where Soc_Number is not null
