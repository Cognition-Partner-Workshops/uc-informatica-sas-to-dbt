select
    "ACCT_ID"      as acct_id,
    "ACCT_TYP"     as acct_typ,
    "ACCT_DESC"    as acct_desc,
    "CRDT_LN"      as crdt_ln,
    "CR8_DT"       as cr8_dt,
    "CLSR_DT"      as clsr_dt,
    "ACCT_STAT_CD" as acct_stat_cd
from {{ ref('demo_source4') }}
