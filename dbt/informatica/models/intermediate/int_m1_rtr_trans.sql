select
    e.*,
    case
        when e.ACCT_TYP = 'SB' then 'demo_target6_GRP'
        when e.ACCT_TYP != 'SB' then 'demo_target5_GRP'
        -- DEFAULT1 is connected to no target and therefore is dropped.
        -- NULL ACCT_TYP matches neither SQL predicate and is also dropped.
    end as router_group
from {{ ref('int_m1_exp_trans') }} e
where e.ACCT_TYP = 'SB'
   or e.ACCT_TYP != 'SB'
