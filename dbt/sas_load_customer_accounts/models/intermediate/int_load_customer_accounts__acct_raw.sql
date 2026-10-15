select
    a.ACCOUNT_ID,
    a.CUSTOMER_ID,
    a.ACCOUNT_TYPE,
    a.ACCOUNT_STATUS,
    a.OPEN_DATE,
    a.CLOSE_DATE,
    a.CURRENT_BALANCE,
    a.AVAILABLE_BALANCE,
    a.CREDIT_LIMIT,
    a.INTEREST_RATE,
    a.BRANCH_ID,
    a.OFFICER_ID,
    a.LAST_ACTIVITY_DATE,
    d.FIRST_NAME,
    d.LAST_NAME,
    d.SSN_HASH,
    d.DATE_OF_BIRTH,
    d.CUSTOMER_SEGMENT,
    d.RISK_RATING,
    d.REGION_CODE,
    d.PRIMARY_EMAIL,
    d.PHONE_NUMBER
from {{ ref('stg_load_customer_accounts__cust_accounts') }} as a
inner join {{ ref('stg_load_customer_accounts__cust_demographics') }} as d
    on a.CUSTOMER_ID = d.CUSTOMER_ID
where (a.ACCOUNT_STATUS is null or a.ACCOUNT_STATUS not in ('W', 'C'))
  and (
      a.OPEN_DATE <= '{{ var("run_date") }}'::date
      or a.OPEN_DATE is null
  )
