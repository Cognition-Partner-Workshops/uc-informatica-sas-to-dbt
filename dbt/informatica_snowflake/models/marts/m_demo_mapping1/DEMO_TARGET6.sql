select acct_id, o_acc_trim as acct_typ, o_acct_desc as acct_desc,
    cast(cr8_dt as date) as cr8_dt,
    cast(o_crdt_trim as number(38,0)) as crdt_ln, clsr_dt, acct_stat_cd, tx_id,
    acct_key, tx_dttm, o_tx_amt as tx_amt, o_acct_id as tx_type_cd
from {{ ref('int_m_demo_mapping1__seq_gen') }}
