-- STG_INS.CLAIMS_REVIEW_QUEUE: manual review queue (denied high-fraud
-- claims plus pending claims).
select *
from {{ ref('int_claims_adjudicated') }}
where adjudication_result in ('DENY', 'PEND')
