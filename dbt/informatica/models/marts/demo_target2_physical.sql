-- The legacy session writes both router instances to physical table demo_target2:
-- both writers insert, neither truncates, and both have target load order 1.
{{ config(materialized='view') }}

select * from {{ ref('demo_target2') }}
union all
select * from {{ ref('demo_target21') }}
