-- REPORTS.MONTHLY_RWA: risk-weighted assets by type/segment/weight.
select
    '{{ var("report_month") }}' as report_month,
    account_type,
    customer_segment,
    risk_weight,
    count(*) as n_accounts,
    sum(current_balance) as total_exposure,
    sum(current_balance * risk_weight) as rwa
from {{ ref('int_rwa_weighted') }}
group by 1, 2, 3, 4
