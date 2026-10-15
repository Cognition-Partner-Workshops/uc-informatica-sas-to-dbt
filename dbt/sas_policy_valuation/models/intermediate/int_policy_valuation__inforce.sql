-- Step 1 (PROC SQL): in-force policies at the valuation date
{% if var('lob') not in ['ALL', 'AUTO', 'HOME', 'WL', 'TL', 'UL', 'HLTH'] %}
{{ exceptions.raise_compiler_error("Invalid lob value: " ~ var('lob')) }}
{% endif %}
select
    POLICY_ID,
    CUSTOMER_ID,
    POLICY_TYPE,
    EFFECTIVE_DATE,
    EXPIRATION_DATE,
    ANNUAL_PREMIUM,
    SUM_INSURED,
    DEDUCTIBLE,
    RISK_CATEGORY,
    UNDERWRITING_CLASS,
    AGENT_ID,
    BRANCH_CODE,
    datediff('month', EFFECTIVE_DATE, '{{ var("val_date") }}'::date) as POLICY_AGE_MONTHS,
    datediff('month', '{{ var("val_date") }}'::date, EXPIRATION_DATE) as MONTHS_TO_EXPIRY,
    -- intnx('month', val_date, 3) with default BEGINNING alignment
    case
        when EXPIRATION_DATE <= dateadd('month', 3, date_trunc('month', '{{ var("val_date") }}'::date))
            then 'Y'
        else 'N'
    end as RENEWAL_DUE_FLAG,
    ANNUAL_PREMIUM / 12 * least(
        12,
        datediff('month',
            greatest(
                coalesce(EFFECTIVE_DATE, date_trunc('year', '{{ var("val_date") }}'::date)),
                date_trunc('year', '{{ var("val_date") }}'::date)
            ),
            least('{{ var("val_date") }}'::date, EXPIRATION_DATE))
    ) as YTD_EARNED_PREMIUM
from {{ ref('stg_policy_valuation__raw_ins_policies') }}
where STATUS = 'ACTIVE'
    and (EFFECTIVE_DATE is null or EFFECTIVE_DATE <= '{{ var("val_date") }}'::date)
    and EXPIRATION_DATE >= '{{ var("val_date") }}'::date
    {% if var('lob') != 'ALL' %}
    and POLICY_TYPE = '{{ var("lob") }}'
    {% endif %}
