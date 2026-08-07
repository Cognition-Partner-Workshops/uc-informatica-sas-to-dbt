# m_demo_mapping1 decisions

## Recovered legacy behaviour (reproduced on purpose)

### Positional Source Qualifier binding

The SQL override at XML line 580 selects `SYSTIMESTAMP` as item 5. The
Source Qualifier ports are positional (XML lines 566-579), so item 5 binds to
`CR8_DT`, not the source's `CR8_DT` value. The implementation uses
`cfg.business_date`, producing `2024-01-31` for the target run. The source
create date is therefore intentionally not propagated.

The 14th select item is
`STRCMP(demo_source4.ACCT_STAT_CD,demo_source3.TX_TYPE_CD)`. It binds to
`TX_TYPE_CD`, but that SQ port has no outgoing connector (the connector list
was checked at XML lines 865-877). It is recorded as NOT MIGRATED and is not
used downstream.

### Unconnected lookup return and target-port name trap

`lkp_TRANS1` uses `ACCT_ID =  IN_ACCT_ID` (including the double space) at XML
line 537 and returns `TX_TYPE_CD` at line 529. The call at line 608 is named
`o_ACCT_ID`, but the connector at line 786 sends that value to target
`TX_TYPE_CD`. The implementation follows the connector graph, so
`demo_target6.TX_TYPE_CD` contains the lookup transaction code, not an
account ID.

### Lookup name traps

`exp_TRANS1.FIRST_NM` is fed by `lkp_TRANS2` at connector line 832, and
`exp_TRANS1.CRDT_SCORE` is fed by `lkp_TRANS3` at connector line 833.
Consequently, target 5's `FIRST_NM` and `CRDT_SCORE` intentionally come from
the lookups rather than the similarly named source 3 columns.

### NULL router row

The router conditions are `ACCT_TYP = 'SB'` and `ACCT_TYP != 'SB'` (XML
lines 668-669). The router input comes from the untrimmed `ACCT_TYP`
pass-through at connector line 837. Account 1005 has NULL `ACCT_TYP` under
the declared `StringType` schema, so both predicates evaluate to NULL. The
DEFAULT1 group at line 670 has no outgoing connectors, and the account is
intentionally absent from both targets.

### `o_SELL_ST_DT` defect

The expression at XML line 662 is
`TO_DATE(TO_CHAR(SYSDATE),'DD/MM/YYYY')`. The implementation resolves
`SYSDATE` from `cfg.business_date`, renders the default date string as
`01/31/2024 00:00:00.000000`, and passes it through
`inf_to_date_ddmmyyyy`. The month/day positions do not match `DD/MM/YYYY`,
so the result is NULL for every row. The source `SELL_ST_DT` input at line
658 is deliberately unused; the output does not hard-code NULL.

## Decisions required because XML is ambiguous

### Aggregator pass-through row

XML lines 443-453 mark the aggregator pass-through ports as
`INPUT/OUTPUT`, while line 452 groups by `ACCT_ID` and line 457 says sorted
input is YES. The SQ only orders by account ID at line 580; it does not
define the order of transactions within an account group. The XML therefore
does not determine which transaction supplies the pass-through values.

The implementation chooses the row with the highest `TX_ID` in each account
group. This matches the baseline: account 1001 uses transaction 5002 and
its timestamp `2024-01-15 11:00:00`. The affected pass-through conversion
rows are rated LOW.

Rejected alternatives:

* First row in the group: rejected because it would select transaction 5001
  for account 1001 and fail parity.
* File-order-last using `__ROW_ORD`: rejected as the implementation rule
  because the XML does not establish that the physical file order is the
  aggregator's within-group order. On this seed data, file-order-last
  happens to be the same row as highest `TX_ID`, so parity does not
  discriminate between those two choices.

### Sequence generator row order

The sequence state is explicit at XML lines 432-438: current value 281,
increment 1, and no reset. The XML does not define a distributed Spark
partition order for the two aggregator output rows. The implementation
derives `ACCT_KEY` as `280 + row_number()` ordered by `ACCT_ID`, yielding
281 for account 1001 and 282 for account 1002. This decision is rated LOW.

The rejected alternative is arbitrary or partition order, which would not
be deterministic. The implementation does not use
`monotonically_increasing_id` for sequence assignment because it is a
partition-derived identifier and does not guarantee the required account
ordering.

## Lookup policy disagreement with the milestone brief

The three lookup transformations all specify `Use Last Value`:

* `lkp_TRANS1`, XML line 536, source `lkp_demo_source3`
* `lkp_TRANS2`, XML line 498, source `lkp_demo_source1`
* `lkp_TRANS3`, XML line 624, source `lkp_demo_source2`

All three are collapsed to one row per key before a plain left join using
`lookup_use_last_value(..., order_col="__ROW_ORD")`. This collapse is
parity-critical because an uncollapsed join would fan out account 1002.

The seed data confirms the milestone disagreement:

* `lkp_demo_source3` has account 1002 values `TR` then `DR`; the last value
  is observable in `demo_target6.TX_TYPE_CD`, so the last-vs-first policy
  for `lkp_TRANS1` is HIGH confidence.
* `lkp_demo_source1` has account 1002 values NINA then ZOE, and
  `lkp_demo_source2` has customer 70032 twice. Those duplicate keys route
  to `demo_target6`, while the lookup outputs `FIRST_NM` and `CRDT_SCORE`
  are consumed by `demo_target5`. Therefore the last-vs-first choice for
  `lkp_TRANS2` and `lkp_TRANS3` is not exercised by the baseline. Those
  policy rows are MEDIUM confidence, while collapse remains required.

The rejected implementation for all three is a direct uncollapsed join,
because it would create duplicate account rows. For the two unexercised
policies, first-value versus last-value is also rejected as an unverified
substitution; the implementation retains the explicit XML policy.

## Time discipline

Both `SYSTIMESTAMP` in the Source Qualifier override and `SYSDATE` in
`exp_TRANS2` use `cfg.business_date` / `cfg.business_timestamp` semantics.
No wall-clock function is used by the mapping or its tests.
