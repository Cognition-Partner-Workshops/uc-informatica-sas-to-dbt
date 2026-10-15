-- Step 5 (PROC MEANS NWAY CLASS POLICY_TYPE): CLASS drops missing levels,
-- n= binds to the first VAR (YTD_EARNED_PREMIUM)
select
    POLICY_TYPE,
    count(YTD_EARNED_PREMIUM) as N_POLICIES,
    sum(YTD_EARNED_PREMIUM) as TOTAL_EARNED,
    sum(TOTAL_INCURRED) as TOTAL_INCURRED,
    sum(TOTAL_PAID) as TOTAL_PAID,
    sum(TOTAL_RESERVE) as TOTAL_RESERVES,
    sum(IBNR_ESTIMATE) as TOTAL_IBNR
from {{ ref('int_policy_valuation__valuation') }}
where nullif(trim(POLICY_TYPE), '') is not null
group by POLICY_TYPE
