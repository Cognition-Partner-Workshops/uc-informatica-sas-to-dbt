-- Step 3 (PROC SQL): premium collections year-to-date
select
    POLICY_ID,
    sum(PREMIUM_AMOUNT) as COLLECTED_PREMIUM,
    sum(case when PAYMENT_STATUS = 'RETURNED' then PREMIUM_AMOUNT else 0 end)
        as RETURNED_PREMIUM,
    max(PAYMENT_DATE) as LAST_PAYMENT_DATE,
    count(case when PAYMENT_STATUS = 'LATE' then 1 end) as LATE_PAYMENTS
from {{ ref('stg_policy_valuation__raw_ins_premiums') }}
where PAYMENT_DATE >= date_trunc('year', '{{ var("val_date") }}'::date)
    and PAYMENT_DATE <= '{{ var("val_date") }}'::date
group by POLICY_ID
