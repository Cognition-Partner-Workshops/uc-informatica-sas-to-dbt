select
    a.acct_id, a.acct_typ, a.acct_desc, a.crdt_ln,
    cast('2024-01-31 00:00:00' as timestamp_ntz) as cr8_dt,
    a.clsr_dt, a.acct_stat_cd,
    t.tx_id, t.last_nm, t.tx_dttm, t.tx_amt, t.bal_amt, t.cust_id
from {{ ref('stg_informatica__demo_source3') }} t
inner join {{ ref('stg_informatica__demo_source4') }} a on t.acct_id = a.acct_id
