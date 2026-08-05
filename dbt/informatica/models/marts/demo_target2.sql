-- RTRTRANS NEWGROUP1 = ISNULL(Social_Security_Number); compared with
-- baseline/informatica/demo_target2.csv.
{{ config(materialized='view') }}

select
    *
from {{ ref('demo_target2_physical') }}
where "Soc_Number" is null
