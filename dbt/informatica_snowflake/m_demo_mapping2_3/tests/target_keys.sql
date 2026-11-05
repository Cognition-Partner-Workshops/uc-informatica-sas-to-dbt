select 'DEMO_TARGET1_INS' as target from {{ ref('DEMO_TARGET1_INS') }}
group by "Key" having count(*) > 1 or "Key" is null
union all
select 'DEMO_TARGET1_UPD' from {{ ref('DEMO_TARGET1_UPD') }}
group by "Key" having count(*) > 1 or "Key" is null
union all
select 'DEMO_TARGET2' from {{ ref('DEMO_TARGET2') }}
group by Member_Identifier having count(*) > 1 or Member_Identifier is null
union all
select 'DEMO_TARGET21' from {{ ref('DEMO_TARGET21') }}
group by Member_Identifier having count(*) > 1 or Member_Identifier is null
