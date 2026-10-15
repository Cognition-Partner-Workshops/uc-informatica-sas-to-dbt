{{ config(alias='CUST_ACCOUNTS_DAILY') }}

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
    a.FIRST_NAME,
    a.LAST_NAME,
    a.SSN_HASH,
    a.DATE_OF_BIRTH,
    a.CUSTOMER_SEGMENT,
    a.RISK_RATING,
    a.REGION_CODE,
    a.PRIMARY_EMAIL,
    a.PHONE_NUMBER,
    a.ACCT_AGE_MONTHS,
    a.DAYS_INACTIVE,
    a.UTILIZATION_PCT,
    a.DORMANCY_FLAG,
    a.HIGH_BALANCE_FLAG,
    coalesce(accttype.label, 'Unknown') as ACCOUNT_TYPE_DESC,
    coalesce(acctstat.label, 'Unknown') as ACCOUNT_STATUS_DESC,
    coalesce(riskrate.label, 'Not Rated') as RISK_RATING_DESC,
    coalesce(custseg.label, 'Unclassified') as CUSTOMER_SEGMENT_DESC,
    coalesce(region.label, 'Unknown') as REGION_CODE_DESC,
    '{{ var("run_date") }}'::date as SNAPSHOT_DATE
from {{ ref('int_load_customer_accounts__acct_derived') }} as a
left join {{ ref('load_customer_accounts__fmt_accttype') }} as accttype
    on a.ACCOUNT_TYPE = accttype.code
left join {{ ref('load_customer_accounts__fmt_acctstat') }} as acctstat
    on a.ACCOUNT_STATUS = acctstat.code
left join {{ ref('load_customer_accounts__fmt_riskrate') }} as riskrate
    on a.RISK_RATING = riskrate.code
left join {{ ref('load_customer_accounts__fmt_custseg') }} as custseg
    on a.CUSTOMER_SEGMENT = custseg.code
left join {{ ref('load_customer_accounts__fmt_region') }} as region
    on a.REGION_CODE = region.code
