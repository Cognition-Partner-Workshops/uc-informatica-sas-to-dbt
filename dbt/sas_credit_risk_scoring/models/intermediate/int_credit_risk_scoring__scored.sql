with woe as (
    select
        *,
        case
            when FICO_SCORE is null then 0.198
            when FICO_SCORE >= 760 then -1.204
            when FICO_SCORE >= 720 then -0.812
            when FICO_SCORE >= 680 then -0.356
            when FICO_SCORE >= 640 then 0.198
            when FICO_SCORE >= 600 then 0.654
            else 1.102
        end as WOE_FICO,
        case
            when UTILIZATION_PCT is null then 0
            when UTILIZATION_PCT <= 10 then -0.956
            when UTILIZATION_PCT <= 30 then -0.521
            when UTILIZATION_PCT <= 50 then -0.102
            when UTILIZATION_PCT <= 70 then 0.334
            when UTILIZATION_PCT <= 90 then 0.789
            else 1.245
        end as WOE_UTIL,
        case
            when PMT_LATE_90_12MO is null then 0
            when PMT_LATE_90_12MO = 0 then -0.678
            when PMT_LATE_90_12MO = 1 then 0.445
            else 1.567
        end as WOE_DPD,
        case
            when ACCT_AGE_MONTHS is null then 0
            when ACCT_AGE_MONTHS >= 120 then -0.534
            when ACCT_AGE_MONTHS >= 60 then -0.289
            when ACCT_AGE_MONTHS >= 24 then 0.045
            else 0.456
        end as WOE_AGE,
        case
            when ACCOUNT_TYPE not in ('MTG', 'AUTO', 'HELC') then 0
            when LTV is null then 0
            when LTV <= 0.60 then -0.712
            when LTV <= 0.80 then -0.234
            when LTV <= 1.00 then 0.356
            else 0.889
        end as WOE_LTV
    from {{ ref('int_credit_risk_scoring__score_input') }}
),

pd_calc as (
    select
        *,
        cast(1 / (1 + exp(-(
            -3.2145
            + 0.412 * WOE_FICO
            + 0.198 * WOE_UTIL
            + 0.289 * WOE_DPD
            + 0.067 * WOE_AGE
            + 0.134 * WOE_LTV
        ))) as float) as PD,
        cast(case
            when ACCOUNT_TYPE in ('MTG', 'AUTO', 'HELC') then
                case
                    when LTV is not null then greatest(0, least(1, (LTV - 0.5) * 0.8))
                    else 0.40
                end
            when ACCOUNT_TYPE = 'CC' then 0.75
            else 0.50
        end as float) as LGD,
        cast(case
            when ACCOUNT_TYPE in ('CC', 'LOC', 'HELC')
                then CURRENT_BALANCE + 0.50 * (CREDIT_LIMIT - CURRENT_BALANCE)
            else CURRENT_BALANCE
        end as float) as EAD
    from woe
)

select
    ACCOUNT_ID,
    CUSTOMER_ID,
    ACCOUNT_TYPE,
    CURRENT_BALANCE,
    CREDIT_LIMIT,
    ACCT_AGE_MONTHS,
    DAYS_INACTIVE,
    UTILIZATION_PCT,
    CUSTOMER_SEGMENT,
    REGION_CODE,
    FICO_SCORE,
    VANTAGE_SCORE,
    BUREAU_INQS_6MO,
    BUREAU_TRADES_OPEN,
    BUREAU_DEROGS,
    BUREAU_UTIL_PCT,
    BUREAU_OLDEST_TRADE_MO,
    PMT_ONTIME_12MO,
    PMT_LATE_30_12MO,
    PMT_LATE_60_12MO,
    PMT_LATE_90_12MO,
    MAX_DAYS_PAST_DUE_EVER,
    MONTHS_SINCE_LAST_DPD,
    AVG_PMT_RATIO_12MO,
    COLLATERAL_VALUE,
    LAST_APPRAISAL_DATE,
    LTV,
    PD,
    LGD,
    EAD,
    PD * LGD * EAD as EXPECTED_LOSS,
    case
        when PD < 0.005 then 1
        when PD < 0.01 then 2
        when PD < 0.03 then 3
        when PD < 0.07 then 4
        when PD < 0.15 then 5
        when PD < 0.30 then 6
        else 7
    end as NEW_RISK_RATING,
    cast('{{ var("score_date") }}' as date) as SCORE_DATE,
    '{{ var("model_id") }}' as MODEL_ID
from pd_calc
