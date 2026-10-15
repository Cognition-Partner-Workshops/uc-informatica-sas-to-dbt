select
    POLICY_TYPE,
    N_POLICIES,
    TOTAL_EARNED,
    TOTAL_INCURRED,
    TOTAL_PAID,
    TOTAL_RESERVES,
    TOTAL_IBNR,
    case when TOTAL_EARNED > 0 then TOTAL_INCURRED / TOTAL_EARNED end
        as AGG_LOSS_RATIO,
    case when TOTAL_EARNED > 0 then TOTAL_INCURRED / TOTAL_EARNED + 0.30 end
        as AGG_COMBINED_RATIO
from {{ ref('int_policy_valuation__loss_ratio_means') }}
