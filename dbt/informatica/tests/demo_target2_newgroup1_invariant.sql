-- RTRTRANS NEWGROUP1 = ISNULL(Social_Security_Number)
select *
from {{ ref('demo_target2') }}
where "Soc_Number" is not null
