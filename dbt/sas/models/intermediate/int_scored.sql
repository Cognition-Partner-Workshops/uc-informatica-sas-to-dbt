-- credit_risk_scoring steps 1-2: assemble scoring features (latest bureau
-- pull on/before the score date) and apply the CRM-2023-Q4-v2 scorecard:
-- WOE bands -> logistic PD -> LGD / EAD / expected loss -> risk rating.
with run as (
    select cast('{{ var("run_date") }}' as date) as run_date
),

latest_bureau as (
    select *
    from (
        select
            b.*,
            row_number() over (
                partition by b.customer_id
                order by b.score_date desc
            ) as rn
        from {{ ref('stg_bureau_scores') }} b
        where b.score_date <= (select run_date from run)
    )
    where rn = 1
),

score_input as (
    select
        a.account_id,
        a.customer_id,
        a.account_type,
        a.current_balance,
        a.credit_limit,
        a.acct_age_months,
        a.days_inactive,
        a.utilization_pct,
        a.customer_segment,
        a.region_code,
        b.fico_score,
        b.vantage_score,
        b.bureau_inqs_6mo,
        b.bureau_trades_open,
        b.bureau_derogs,
        b.bureau_util_pct,
        b.bureau_oldest_trade_mo,
        p.pmt_ontime_12mo,
        p.pmt_late_30_12mo,
        p.pmt_late_60_12mo,
        p.pmt_late_90_12mo,
        p.max_days_past_due_ever,
        p.months_since_last_dpd,
        p.avg_pmt_ratio_12mo,
        c.collateral_value,
        c.last_appraisal_date,
        case
            when c.collateral_value > 0
                then a.current_balance / c.collateral_value
        end as ltv
    from {{ ref('cust_accounts_daily') }} a
    left join latest_bureau b
        on a.customer_id = b.customer_id
    left join {{ ref('stg_payment_history') }} p
        on a.account_id = p.account_id
    left join {{ ref('stg_collateral') }} c
        on a.account_id = c.account_id
    where a.snapshot_date = (select run_date from run)
      and a.account_type in ('MTG', 'AUTO', 'PERS', 'CC', 'LOC', 'HELC')
),

woe as (
    select
        *,
        case
            when fico_score is null then 0.198  -- population average
            when fico_score >= 760 then -1.204
            when fico_score >= 720 then -0.812
            when fico_score >= 680 then -0.356
            when fico_score >= 640 then 0.198
            when fico_score >= 600 then 0.654
            else 1.102
        end as woe_fico,
        case
            when utilization_pct is null then 0
            when utilization_pct <= 10 then -0.956
            when utilization_pct <= 30 then -0.521
            when utilization_pct <= 50 then -0.102
            when utilization_pct <= 70 then 0.334
            when utilization_pct <= 90 then 0.789
            else 1.245
        end as woe_util,
        case
            when pmt_late_90_12mo is null then 0
            when pmt_late_90_12mo = 0 then -0.678
            when pmt_late_90_12mo = 1 then 0.445
            else 1.567
        end as woe_dpd,
        case
            when acct_age_months is null then 0
            when acct_age_months >= 120 then -0.534
            when acct_age_months >= 60 then -0.289
            when acct_age_months >= 24 then 0.045
            else 0.456
        end as woe_age,
        case
            when account_type not in ('MTG', 'AUTO', 'HELC') then 0
            when ltv is null then 0
            when ltv <= 0.60 then -0.712
            when ltv <= 0.80 then -0.234
            when ltv <= 1.00 then 0.356
            else 0.889
        end as woe_ltv
    from score_input
),

pd_calc as (
    select
        *,
        1 / (1 + exp(-(-3.2145 + 0.412 * woe_fico + 0.198 * woe_util
                       + 0.289 * woe_dpd + 0.067 * woe_age
                       + 0.134 * woe_ltv))) as pd
    from woe
),

risk_measures as (
    select
        *,
        case
            when account_type in ('MTG', 'AUTO', 'HELC') then
                case
                    when ltv is null then 0.40
                    else greatest(0, least(1, (ltv - 0.5) * 0.8))
                end
            when account_type = 'CC' then 0.75
            else 0.50
        end as lgd,
        case
            when account_type in ('CC', 'LOC', 'HELC')
                then current_balance + 0.50 * (credit_limit - current_balance)
            else current_balance
        end as ead
    from pd_calc
)

select
    account_id,
    customer_id,
    account_type,
    current_balance,
    credit_limit,
    acct_age_months,
    days_inactive,
    utilization_pct,
    customer_segment,
    region_code,
    fico_score,
    vantage_score,
    bureau_inqs_6mo,
    bureau_trades_open,
    bureau_derogs,
    bureau_util_pct,
    bureau_oldest_trade_mo,
    pmt_ontime_12mo,
    pmt_late_30_12mo,
    pmt_late_60_12mo,
    pmt_late_90_12mo,
    max_days_past_due_ever,
    months_since_last_dpd,
    avg_pmt_ratio_12mo,
    collateral_value,
    last_appraisal_date,
    ltv,
    pd,
    lgd,
    ead,
    pd * lgd * ead as expected_loss,
    case
        when pd < 0.005 then 1
        when pd < 0.01 then 2
        when pd < 0.03 then 3
        when pd < 0.07 then 4
        when pd < 0.15 then 5
        when pd < 0.30 then 6
        else 7
    end as new_risk_rating,
    cast('{{ var("run_date") }}' as date) as score_date,
    '{{ var("model_id") }}' as model_id
from risk_measures
