with outputs as (
    select ID from {{ ref('DEMO_TARGET1_INS') }}
    union all
    select ID from {{ ref('DEMO_TARGET1_UPD') }}
), compared as (
    select ID, count(*) as n from {{ ref('stg_m_demo_mapping2__demo_source1') }} group by ID
    except
    select ID, count(*) as n from outputs group by ID
), unexpected as (
    select ID, count(*) as n from outputs group by ID
    except
    select ID, count(*) as n from {{ ref('stg_m_demo_mapping2__demo_source1') }} group by ID
)
select * from compared union all select * from unexpected
