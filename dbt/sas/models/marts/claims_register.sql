-- STG_INS.CLAIMS_REGISTER: all adjudicated claims with processing date and
-- claim status; the $CLMSTAT display format is materialized as
-- CLAIM_STATUS_DESC via a seed lookup.
select
    a.*,
    cast('{{ var("run_date") }}' as date) as processing_date,
    a.adjudication_result as claim_status,
    coalesce(f.label, 'Unknown') as claim_status_desc
from {{ ref('int_claims_adjudicated') }} a
left join {{ ref('fmt_claim_status') }} f
    on a.adjudication_result = f.code
