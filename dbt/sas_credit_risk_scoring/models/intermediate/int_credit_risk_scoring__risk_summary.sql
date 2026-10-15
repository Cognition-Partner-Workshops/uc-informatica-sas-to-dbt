-- PROC MEANS NWAY: missing CLASS values are excluded; n= binds to the first VAR (PD)
select
    ACCOUNT_TYPE,
    NEW_RISK_RATING,
    count(PD) as N_ACCOUNTS,
    avg(PD) as AVG_PD,
    avg(LGD) as AVG_LGD,
    sum(EAD) as TOTAL_EAD,
    sum(EXPECTED_LOSS) as TOTAL_EL
from {{ ref('int_credit_risk_scoring__scored') }}
where ACCOUNT_TYPE is not null
  and NEW_RISK_RATING is not null
group by ACCOUNT_TYPE, NEW_RISK_RATING
