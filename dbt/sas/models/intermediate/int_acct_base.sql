-- load_customer_accounts step 1-2: join accounts to demographics, apply
-- business-rule filters, and compute derived account metrics.
with run as (
    select cast('{{ var("run_date") }}' as date) as run_date
)

select
    a.account_id,
    a.customer_id,
    a.account_type,
    a.account_status,
    a.open_date,
    a.close_date,
    a.current_balance,
    a.available_balance,
    a.credit_limit,
    a.interest_rate,
    a.branch_id,
    a.officer_id,
    a.last_activity_date,
    d.first_name,
    d.last_name,
    d.ssn_hash,
    d.date_of_birth,
    d.customer_segment,
    d.risk_rating,
    d.region_code,
    d.primary_email,
    d.phone_number,
    datediff('month', a.open_date, r.run_date) as acct_age_months,
    datediff('day', a.last_activity_date, r.run_date) as days_inactive,
    case
        when a.account_type in ('CC', 'LOC', 'HELC') and a.credit_limit > 0
            then (a.current_balance / a.credit_limit) * 100
    end as utilization_pct,
    case
        when datediff('day', a.last_activity_date, r.run_date) > 365
             and a.account_status = 'A'
            then 'Y' else 'N'
    end as dormancy_flag,
    case when a.current_balance >= 250000 then 'Y' else 'N' end as high_balance_flag
from {{ ref('stg_cust_accounts') }} a
inner join {{ ref('stg_cust_demographics') }} d
    on a.customer_id = d.customer_id
cross join run r
where a.account_status not in ('W', 'C')
  -- SAS missing-value ordering: a missing OPEN_DATE satisfies "<= run_date"
  and (a.open_date <= r.run_date or a.open_date is null)
