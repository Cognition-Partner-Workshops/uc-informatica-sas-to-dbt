-- REPORTS.CAPITAL_ADEQUACY: capital ratios vs Basel III minimums
-- (CET1 4.5%, Tier1 6%, Total 8%); capital amounts are GL placeholders
-- in the legacy program.
select
    '{{ var("report_month") }}' as report_month,
    sum(rwa) as total_rwa,
    50000000 as cet1_capital,
    65000000 as tier1_capital,
    80000000 as total_capital,
    case when sum(rwa) > 0 then 50000000 / sum(rwa) * 100 end as cet1_ratio,
    case when sum(rwa) > 0 then 65000000 / sum(rwa) * 100 end as tier1_ratio,
    case when sum(rwa) > 0 then 80000000 / sum(rwa) * 100 end
        as total_capital_ratio,
    case when sum(rwa) = 0 then 'PASS'
         when 50000000 / sum(rwa) * 100 >= 4.5 then 'PASS'
         else 'FAIL' end as cet1_status,
    case when sum(rwa) = 0 then 'PASS'
         when 65000000 / sum(rwa) * 100 >= 6.0 then 'PASS'
         else 'FAIL' end as tier1_status,
    case when sum(rwa) = 0 then 'PASS'
         when 80000000 / sum(rwa) * 100 >= 8.0 then 'PASS'
         else 'FAIL' end as total_capital_status
from {{ ref('monthly_rwa') }}
