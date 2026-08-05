-- CURATED.RISK_SCORES: scored portfolio with PD/LGD/EAD, expected loss,
-- and new risk rating. The legacy wall-clock SCORE_TIMESTAMP is excluded
-- (non-deterministic; see STM notes).
select * from {{ ref('int_scored') }}
