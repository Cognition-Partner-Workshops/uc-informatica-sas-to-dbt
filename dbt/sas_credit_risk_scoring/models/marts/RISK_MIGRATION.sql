-- CURATED.RISK_MIGRATION: PROC APPEND of WORK.RISK_MIGRATION; prior CURATED state is not in SOURCE_ and is treated as empty.
select
    SCORE_DATE, ACCOUNT_ID, PREV_RATING, CURR_RATING, MIGRATION_DIRECTION, PD, EXPECTED_LOSS
from {{ ref('int_credit_risk_scoring__risk_migration') }}
