-- EXPTRANS: iif(ISNULL(Relationship_to_Subscriber_Code_Label),
-- ABORT('Relationship_to_Subscriber_Code_Labe valuel is null'),
-- Relationship_to_Subscriber_Code_Label).
-- An ABORT is a hard run failure, never a null-fill or a filter.
{{ config(severity='error') }}

select *
from {{ ref('int_m3_exptrans') }}
where o_relationship_to_subscriber_code_label is null
