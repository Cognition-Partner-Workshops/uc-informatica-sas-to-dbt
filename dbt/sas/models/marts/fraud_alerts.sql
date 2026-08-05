-- STG_INS.FRAUD_ALERTS: high fraud-risk claims routed to SIU.
select
    *,
    case
        when indicator_flags is not null and trim(indicator_flags) <> ''
            then 'Fraud score: ' || cast(cast(fraud_score as integer) as varchar)
                 || '; ' || indicator_flags
        else 'Fraud score: ' || cast(cast(fraud_score as integer) as varchar)
    end as alert_reason,
    cast('{{ var("run_date") }}' as date) as alert_date
from {{ ref('int_fraud_check') }}
where fraud_risk = 'HIGH'
