select
    ACCOUNT_ID,
    CUSTOMER_ID,
    ACCOUNT_TYPE,
    ACCOUNT_STATUS,
    OPEN_DATE,
    CLOSE_DATE,
    CURRENT_BALANCE,
    AVAILABLE_BALANCE,
    CREDIT_LIMIT,
    INTEREST_RATE,
    BRANCH_ID,
    OFFICER_ID,
    LAST_ACTIVITY_DATE,
    FIRST_NAME,
    LAST_NAME,
    SSN_HASH,
    DATE_OF_BIRTH,
    CUSTOMER_SEGMENT,
    RISK_RATING,
    REGION_CODE,
    PRIMARY_EMAIL,
    PHONE_NUMBER,
    datediff('month', OPEN_DATE, '{{ var("run_date") }}'::date) as ACCT_AGE_MONTHS,
    datediff('day', LAST_ACTIVITY_DATE, '{{ var("run_date") }}'::date) as DAYS_INACTIVE,
    case
        when ACCOUNT_TYPE in ('CC', 'LOC', 'HELC') and CREDIT_LIMIT > 0
            then (CURRENT_BALANCE / CREDIT_LIMIT) * 100
        else null
    end::float as UTILIZATION_PCT,
    case
        when datediff('day', LAST_ACTIVITY_DATE, '{{ var("run_date") }}'::date) > 365
            and ACCOUNT_STATUS = 'A'
            then 'Y'
        else 'N'
    end as DORMANCY_FLAG,
    case
        when CURRENT_BALANCE >= 250000 then 'Y'
        else 'N'
    end as HIGH_BALANCE_FLAG
from {{ ref('int_load_customer_accounts__acct_raw') }}
