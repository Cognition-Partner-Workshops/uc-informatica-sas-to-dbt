-- Step 2 (PROC SQL): claims experience over the trailing 12-month window
select
    POLICY_ID,
    count(distinct CLAIM_ID) as NUM_CLAIMS,
    sum(INCURRED_AMOUNT) as TOTAL_INCURRED,
    sum(PAID_AMOUNT) as TOTAL_PAID,
    sum(RESERVED_AMOUNT) as TOTAL_RESERVED,
    max(LOSS_DATE) as LAST_CLAIM_DATE,
    sum(case when CLAIM_STATUS in ('OPEN', 'INV', 'ADJ', 'PEND')
        then RESERVED_AMOUNT else 0 end) as OPEN_RESERVES,
    sum(case when CLAIM_STATUS = 'DENY' then 1 else 0 end) as DENIED_CLAIMS
from {{ ref('stg_policy_valuation__raw_ins_claims') }}
where LOSS_DATE >= dateadd('month', -12, date_trunc('month', '{{ var("val_date") }}'::date))
    and LOSS_DATE <= '{{ var("val_date") }}'::date
group by POLICY_ID
