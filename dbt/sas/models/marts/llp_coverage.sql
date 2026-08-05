-- REPORTS.LLP_COVERAGE: loan loss provision coverage (inner join to loan
-- details, lending products only).
select
    '{{ var("report_month") }}' as report_month,
    account_type,
    count(*) as n_loans,
    sum(current_balance) as gross_loans,
    sum(allowance_amt) as total_allowance,
    case
        when sum(current_balance) > 0
            then sum(allowance_amt) / sum(current_balance) * 100
        else 0
    end as coverage_pct,
    sum(case when days_past_due >= 90 then current_balance else 0 end)
        as npl_balance,
    case
        when sum(case when days_past_due >= 90 then current_balance else 0 end) > 0
            then sum(allowance_amt)
                 / sum(case when days_past_due >= 90 then current_balance
                            else 0 end) * 100
        else 0
    end as npl_coverage_pct
from {{ ref('int_rwa_weighted') }}
where account_type in ('MTG', 'AUTO', 'PERS', 'CC', 'LOC', 'HELC')
  and has_loan_detail = 1
group by 1, 2
