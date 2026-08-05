-- STG_BANK.CUST_ACCOUNTS_DAILY: daily account snapshot. PROC FORMAT display
-- recodes are materialized as *_DESC columns via seed lookup joins.
select
    b.*,
    coalesce(ft.label, 'Unknown') as account_type_desc,
    coalesce(fs.label, 'Unknown') as account_status_desc,
    coalesce(fr.label, 'Not Rated') as risk_rating_desc,
    coalesce(fc.label, 'Unclassified') as customer_segment_desc,
    coalesce(fg.label, 'Unknown') as region_code_desc,
    cast('{{ var("run_date") }}' as date) as snapshot_date
from {{ ref('int_acct_base') }} b
left join {{ ref('fmt_account_type') }} ft on b.account_type = ft.code
left join {{ ref('fmt_account_status') }} fs on b.account_status = fs.code
left join {{ ref('fmt_risk_rating') }} fr on b.risk_rating = fr.code
left join {{ ref('fmt_customer_segment') }} fc on b.customer_segment = fc.code
left join {{ ref('fmt_region') }} fg on b.region_code = fg.code
