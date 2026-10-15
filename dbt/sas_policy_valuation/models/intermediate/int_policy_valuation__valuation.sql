-- Step 4 (DATA step MERGE ... if a): valuation metrics per in-force policy
with merged as (
    select
        i.POLICY_ID,
        i.CUSTOMER_ID,
        i.POLICY_TYPE,
        i.EFFECTIVE_DATE,
        i.EXPIRATION_DATE,
        i.ANNUAL_PREMIUM,
        i.SUM_INSURED,
        i.DEDUCTIBLE,
        i.RISK_CATEGORY,
        i.UNDERWRITING_CLASS,
        i.AGENT_ID,
        i.BRANCH_CODE,
        i.POLICY_AGE_MONTHS,
        i.MONTHS_TO_EXPIRY,
        i.RENEWAL_DUE_FLAG,
        i.YTD_EARNED_PREMIUM,
        c.NUM_CLAIMS,
        c.TOTAL_INCURRED,
        c.TOTAL_PAID,
        c.TOTAL_RESERVED,
        c.LAST_CLAIM_DATE,
        c.OPEN_RESERVES,
        c.DENIED_CLAIMS,
        m.COLLECTED_PREMIUM,
        m.RETURNED_PREMIUM,
        m.LAST_PAYMENT_DATE,
        m.LATE_PAYMENTS
    from {{ ref('int_policy_valuation__inforce') }} i
    left join {{ ref('int_policy_valuation__claims_exp') }} c
        on i.POLICY_ID = c.POLICY_ID
    left join {{ ref('int_policy_valuation__premium_coll') }} m
        on i.POLICY_ID = m.POLICY_ID
),
ratios as (
    select
        *,
        case when YTD_EARNED_PREMIUM > 0
            then coalesce(TOTAL_INCURRED, 0) / YTD_EARNED_PREMIUM
        end as LOSS_RATIO
    from merged
),
combined as (
    select
        *,
        case when YTD_EARNED_PREMIUM > 0
            then LOSS_RATIO + 0.30
        end as COMBINED_RATIO
    from ratios
),
reserved as (
    select
        *,
        -- SAS max() ignores missing arguments; TOTAL_PAID is coalesced first
        coalesce(greatest(0, YTD_EARNED_PREMIUM * 0.15 - coalesce(TOTAL_PAID, 0)), 0)
            as IBNR_ESTIMATE
    from combined
)
select
    r.POLICY_ID,
    r.CUSTOMER_ID,
    r.POLICY_TYPE,
    r.EFFECTIVE_DATE,
    r.EXPIRATION_DATE,
    r.ANNUAL_PREMIUM,
    r.SUM_INSURED,
    r.DEDUCTIBLE,
    r.RISK_CATEGORY,
    r.UNDERWRITING_CLASS,
    r.AGENT_ID,
    r.BRANCH_CODE,
    r.POLICY_AGE_MONTHS,
    r.MONTHS_TO_EXPIRY,
    r.RENEWAL_DUE_FLAG,
    r.YTD_EARNED_PREMIUM,
    r.NUM_CLAIMS,
    r.TOTAL_INCURRED,
    r.TOTAL_PAID,
    r.TOTAL_RESERVED,
    r.LAST_CLAIM_DATE,
    r.OPEN_RESERVES,
    r.DENIED_CLAIMS,
    r.COLLECTED_PREMIUM,
    r.RETURNED_PREMIUM,
    r.LAST_PAYMENT_DATE,
    r.LATE_PAYMENTS,
    r.LOSS_RATIO,
    r.COMBINED_RATIO,
    case when r.COMBINED_RATIO is null then 'N'
         when r.COMBINED_RATIO > 1.0 then 'N'
         else 'Y' end as PREMIUM_ADEQUATE,
    r.IBNR_ESTIMATE,
    coalesce(r.OPEN_RESERVES, 0) + r.IBNR_ESTIMATE as TOTAL_RESERVE,
    '{{ var("val_date") }}'::date as VALUATION_DATE,
    -- 'Unknown' is the $POLTYPE format's OTHER= label
    coalesce(pt.LABEL, 'Unknown') as POLICY_TYPE_DESC,
    -- 'Unrated' is the $RISKCAT format's OTHER= label
    coalesce(rc.LABEL, 'Unrated') as RISK_CATEGORY_DESC
from reserved r
left join {{ ref('policy_valuation__fmt_poltype') }} pt
    on r.POLICY_TYPE = pt.CODE
left join {{ ref('policy_valuation__fmt_riskcat') }} rc
    on r.RISK_CATEGORY = rc.CODE
