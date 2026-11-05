select *,
    case when acct_typ = 'SB' then 'demo_target6_GRP'
        when acct_typ != 'SB' then 'demo_target5_GRP'
        else 'DEFAULT1' end as router_group
from {{ ref('int_m_demo_mapping1__exp_trans1') }}
