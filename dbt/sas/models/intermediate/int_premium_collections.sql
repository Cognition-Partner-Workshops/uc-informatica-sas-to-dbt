-- policy_valuation step 3: fiscal-year-to-date premium collections
-- (window = intnx('year', val_date, 0, 'B') .. val_date).
select
    policy_id,
    sum(premium_amount) as collected_premium,
    sum(case when payment_status = 'RETURNED' then premium_amount else 0 end)
        as returned_premium,
    max(payment_date) as last_payment_date,
    count(case when payment_status = 'LATE' then 1 end) as late_payments
from {{ ref('stg_premiums') }}
where payment_date >= cast('{{ var("year_start") }}' as date)
  and payment_date <= cast('{{ var("run_date") }}' as date)
group by policy_id
