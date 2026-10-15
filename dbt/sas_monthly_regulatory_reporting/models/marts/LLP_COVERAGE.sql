with loan_totals as (
    select
        ACCOUNT_TYPE,
        count(*) as N_LOANS,
        sum(CURRENT_BALANCE) as GROSS_LOANS,
        sum(ALLOWANCE_AMT) as TOTAL_ALLOWANCE,
        sum(case when DAYS_PAST_DUE >= 90 then CURRENT_BALANCE else 0 end) as NPL_BALANCE
    from {{ ref('int_monthly_regulatory_reporting__llp_loans') }}
    group by ACCOUNT_TYPE
)

select
    '{{ var("report_month") }}'::varchar(6) as REPORT_MONTH,
    ACCOUNT_TYPE,
    N_LOANS,
    cast(GROSS_LOANS as float) as GROSS_LOANS,
    cast(TOTAL_ALLOWANCE as float) as TOTAL_ALLOWANCE,
    cast(
        case when GROSS_LOANS > 0 then TOTAL_ALLOWANCE / GROSS_LOANS * 100 else 0 end
        as float
    ) as COVERAGE_PCT,
    cast(NPL_BALANCE as float) as NPL_BALANCE,
    cast(
        case when NPL_BALANCE > 0 then TOTAL_ALLOWANCE / NPL_BALANCE * 100 else 0 end
        as float
    ) as NPL_COVERAGE_PCT
from loan_totals
