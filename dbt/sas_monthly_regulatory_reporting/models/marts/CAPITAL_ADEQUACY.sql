select
    '{{ var("report_month") }}'::varchar(6) as REPORT_MONTH,
    cast(sum(RWA) as float) as TOTAL_RWA,
    50000000::number as CET1_CAPITAL,
    65000000::number as TIER1_CAPITAL,
    80000000::number as TOTAL_CAPITAL,
    cast(
        case when sum(RWA) > 0 then 50000000::float / sum(RWA) * 100 else null end
        as float
    ) as CET1_RATIO,
    cast(
        case when sum(RWA) > 0 then 65000000::float / sum(RWA) * 100 else null end
        as float
    ) as TIER1_RATIO,
    cast(
        case when sum(RWA) > 0 then 80000000::float / sum(RWA) * 100 else null end
        as float
    ) as TOTAL_CAPITAL_RATIO,
    cast(
        case
            when sum(RWA) = 0 then 'PASS'
            when 50000000::float / sum(RWA) * 100 >= 4.5 then 'PASS'
            else 'FAIL'
        end as varchar(4)
    ) as CET1_STATUS,
    cast(
        case
            when sum(RWA) = 0 then 'PASS'
            when 65000000::float / sum(RWA) * 100 >= 6.0 then 'PASS'
            else 'FAIL'
        end as varchar(4)
    ) as TIER1_STATUS,
    cast(
        case
            when sum(RWA) = 0 then 'PASS'
            when 80000000::float / sum(RWA) * 100 >= 8.0 then 'PASS'
            else 'FAIL'
        end as varchar(4)
    ) as TOTAL_CAPITAL_STATUS
from {{ ref('MONTHLY_RWA') }}
