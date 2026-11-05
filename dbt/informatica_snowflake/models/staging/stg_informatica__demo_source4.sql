select
    cast("ACCT_ID" as number(38,0)) as acct_id,
    cast("ACCT_TYP" as varchar) as acct_typ,
    cast("ACCT_DESC" as varchar) as acct_desc,
    cast("CRDT_LN" as varchar) as crdt_ln,
    cast("CR8_DT" as date) as cr8_dt,
    cast("CLSR_DT" as date) as clsr_dt,
    cast("ACCT_STAT_CD" as varchar) as acct_stat_cd
from {{ source('infa_source', 'DEMO_SOURCE4') }}
