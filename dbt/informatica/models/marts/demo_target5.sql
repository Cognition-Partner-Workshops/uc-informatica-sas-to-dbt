-- m_demo_mapping1 rtr_TRANS demo_target5_GRP (ACCT_TYP != 'SB'); rows with a
-- NULL ACCT_TYP fall to the unconnected DEFAULT group and are dropped.
select
    acct_id    as "ACCT_ID",
    first_nm   as "FIRST_NM",
    last_nm    as "LAST_NM",
    bal_amt    as "BAL_AMT",
    crdt_score as "CRDT_SCORE"
from {{ ref('int_m1_enriched') }}
where acct_typ != 'SB'
