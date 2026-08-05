-- REPORTS.DELINQUENCY_AGING: delinquency buckets for lending products.
-- A missing DAYS_PAST_DUE (no loan-details row) falls through to 'Unknown'.
select
    '{{ var("report_month") }}' as report_month,
    account_type,
    region_code,
    case
        when days_past_due = 0 then 'Current'
        when days_past_due between 1 and 29 then '1-29'
        when days_past_due between 30 and 59 then '30-59'
        when days_past_due between 60 and 89 then '60-89'
        when days_past_due between 90 and 119 then '90-119'
        when days_past_due between 120 and 179 then '120-179'
        when days_past_due >= 180 then '180+'
        else 'Unknown'
    end as delinq_bucket,
    count(*) as n_accounts,
    sum(current_balance) as total_balance,
    sum(past_due_amount) as total_past_due
from {{ ref('int_rwa_weighted') }}
where account_type in ('MTG', 'AUTO', 'PERS', 'CC', 'LOC', 'HELC')
group by 1, 2, 3, 4
