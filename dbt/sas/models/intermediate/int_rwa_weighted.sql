-- monthly_regulatory_reporting step 1a: Basel III standardized risk weights
-- per account. SAS missing ordering: a NULL LTV satisfies "LTV <= 0.80",
-- so MTG accounts without loan details get weight 0.35.
select
    a.account_type,
    a.customer_segment,
    a.region_code,
    a.current_balance,
    l.ltv,
    l.days_past_due,
    l.past_due_amount,
    l.allowance_amt,
    case
        when a.account_type in ('CHK', 'SAV', 'MMA') then 0.00
        when a.account_type = 'CD' then 0.00
        when a.account_type = 'MTG' and (l.ltv <= 0.80 or l.ltv is null) then 0.35
        when a.account_type = 'MTG' and l.ltv > 0.80 then 0.50
        when a.account_type = 'HELC' then 0.50
        when a.account_type in ('AUTO', 'PERS') then 0.75
        when a.account_type = 'CC' then 0.75
        when a.account_type = 'LOC' then 1.00
        else 1.00
    end as risk_weight,
    case when l.account_id is not null then 1 else 0 end as has_loan_detail
from {{ ref('cust_accounts_daily') }} a
left join {{ ref('stg_loan_details') }} l
    on a.account_id = l.account_id
where a.snapshot_date = cast('{{ var("run_date") }}' as date)
