{{ config(severity='error', tags=['RUN:FSX_20261105'], meta={'legacy_unit': 'm_demo_mapping3'}) }}
select *
from {{ ref('int_m_demo_mapping3__sq') }}
where relationship_to_subscriber_code_label is null
