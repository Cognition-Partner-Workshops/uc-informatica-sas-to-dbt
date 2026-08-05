-- CURATED.TXN_ANOMALIES: z-score and rule-based anomaly detection.
-- SAS missing-value ordering is reproduced explicitly: a NULL running
-- balance satisfies "< 0" (OVERDRAFT), and a NULL pre-balance makes the
-- large-withdrawal comparison true.
select *
from (
    select
        e.*,
        s.avg_txn_amt,
        s.std_txn_amt,
        case
            when s.std_txn_amt > 0
                then (abs(e.transaction_amount) - s.avg_txn_amt) / s.std_txn_amt
        end as z_score,
        case
            when (case
                      when s.std_txn_amt > 0
                          then (abs(e.transaction_amount) - s.avg_txn_amt)
                               / s.std_txn_amt
                  end) > 3 then 'HIGH_AMOUNT'
            when e.running_balance < 0 or e.running_balance is null
                then 'OVERDRAFT'
            when e.transaction_type = 'WDR'
                 and (e.pre_txn_balance is null
                      or abs(e.transaction_amount) > e.pre_txn_balance * 0.9)
                then 'LARGE_WITHDRAWAL'
            when e.customer_id is null then 'ORPHAN_ACCOUNT'
            else ''
        end as anomaly_type
    from {{ ref('int_txn_with_balance') }} e
    left join {{ ref('int_txn_stats') }} s
        on e.account_id = s.account_id
)
where anomaly_type <> ''
