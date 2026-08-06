{{ config(severity='error') }}

select *
from {{ ref(var('m3_abort_test_relation', 'int_m3__exptrans')) }}
where o_Relationship_to_Subscriber_Code_Label is null
