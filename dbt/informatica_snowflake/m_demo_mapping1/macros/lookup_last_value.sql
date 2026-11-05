{#- Cached lookup with "Use Last Value" on multiple match: per lookup key keep
    the last row in physical seed order (highest SEED_ROW). -#}
{% macro lookup_last_value(relation, key) -%}
select * exclude (__lkp_rn)
from (
    select *,
           row_number() over (partition by {{ key }} order by SEED_ROW desc) as __lkp_rn
    from {{ relation }}
) as ranked
where __lkp_rn = 1
{%- endmacro %}
