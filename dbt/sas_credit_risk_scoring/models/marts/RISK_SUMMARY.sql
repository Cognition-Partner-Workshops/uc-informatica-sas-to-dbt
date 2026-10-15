select
    ACCOUNT_TYPE, NEW_RISK_RATING, N_ACCOUNTS, AVG_PD, AVG_LGD, TOTAL_EAD, TOTAL_EL
from {{ ref('int_credit_risk_scoring__risk_summary') }}
