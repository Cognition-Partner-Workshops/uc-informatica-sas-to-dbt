-- RTRTRANS NEWGROUP2 = NOT ISNULL(Social_Security_Number); compared with
-- baseline/informatica/demo_target21.csv.
{{ config(materialized='view') }}

select
    *
from {{ ref('demo_target2_physical') }}
where "Soc_Number" is not null
