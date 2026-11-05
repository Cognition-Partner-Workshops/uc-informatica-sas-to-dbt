# m_demo_mapping1 source-to-target mapping

Reference: legacy/informatica/wf_demo_mapping.XML, mapping m_demo_mapping1;
CONNECTORs and TARGET instances confirm demo_target3, demo_target5 and demo_target6.
Execution contract: tools/informatica_baseline.py load() and mapping1(),
business date 2024-01-31. No baseline relation is read by the dbt DAG.

## Steps and lookup rules

All SQL models have prefix int_m_demo_mapping1__. Legacy names are retained
case-insensitively. sq_demo_source4 joins DEMO_SOURCE3 t to DEMO_SOURCE4 a
on t.ACCT_ID = a.ACCT_ID (inner join), projecting exactly baseline m1_sq.
exp_TRANS applies RTRIM(ACCT_TYP), LTRIM(CRDT_LN) and the unconnected
lkp_TRANS1 return. lkp_TRANS2 and lkp_TRANS3 feed exp_TRANS1, which
also applies RTRIM(ACCT_DESC). The three lookup views deduplicate before
their left joins in the expression models (unmatched returns stay NULL).

| Legacy lookup | Source | Condition | Return | Multiple match |
|---|---|---|---|---|
| lkp_TRANS1 | LKP_DEMO_SOURCE3 | ACCT_ID = IN_ACCT_ID (account) | TX_TYPE_CD as o_ACCT_ID | Use Last Value: highest SEED_ROW per ACCT_ID |
| lkp_TRANS2 | LKP_DEMO_SOURCE1 | ACCT_ID = IN_ACCT_ID (account) | FIRST_NM | Use Last Value: highest SEED_ROW per ACCT_ID |
| lkp_TRANS3 | LKP_DEMO_SOURCE2 | CUST_ID = IN_CUST_ID (transaction customer) | CRDT_SCORE | Use Last Value: highest SEED_ROW per CUST_ID |

rtr_TRANS groups: demo_target6_GRP is ACCT_TYP = 'SB';
demo_target5_GRP is ACCT_TYP != 'SB'; DEFAULT1 is unwritten.
The predicates use the untrimmed input, not o_acc_trim. NULL ACCT_TYP
enters DEFAULT1 and neither target. The only declared target code domain
is DEMO_TARGET6.ACCT_TYP = ['SB']; no inferred seed-only code lists.

agg_TRANS groups only by ACCT_ID, sums TX_AMT into o_TX_AMT and
uses the highest-TX_ID row for all nonaggregate ports. SEQ_GEN supplies
ACCT_KEY: 280 + DENSE_RANK() over ACCT_ID after aggregation.
SQ_demo_source5 is a passthrough to exp_TRANS2, independently of the router.

## Column lineage (target order)

For DEMO_TARGET6 every row follows sq_demo_source4 → exp_TRANS →
exp_TRANS1 → rtr_TRANS.demo_target6_GRP → agg_TRANS → SEQ_GEN.
Nonaggregate fields below come from the highest-TX_ID row per ACCT_ID.

| DEMO_TARGET6 column | Source and expression |
|---|---|
| ACCT_ID | a.ACCT_ID, aggregate group key |
| ACCT_TYP | a.ACCT_TYP → exp_TRANS.o_acc_trim = RTRIM(ACCT_TYP) |
| ACCT_DESC | a.ACCT_DESC → exp_TRANS1.o_ACCT_DESC = RTRIM(ACCT_DESC) |
| CR8_DT | SQL override SYSTIMESTAMP → pinned timestamp 2024-01-31 00:00:00 → DATE |
| CRDT_LN | a.CRDT_LN → exp_TRANS.o_crdt_trim = LTRIM(CRDT_LN) → NUMBER(38,0) |
| CLSR_DT | a.CLSR_DT, DATE passthrough |
| ACCT_STAT_CD | a.ACCT_STAT_CD passthrough |
| TX_ID | t.TX_ID, highest in account |
| ACCT_KEY | SEQ_GEN.NEXTVAL, deterministic 280 + DENSE_RANK() by ACCT_ID |
| TX_DTTM | t.TX_DTTM passthrough, TIMESTAMP_NTZ |
| TX_AMT | t.TX_AMT → agg_TRANS.o_TX_AMT = SUM(TX_AMT), FLOAT |
| TX_TYPE_CD | lkp_TRANS1.TX_TYPE_CD → exp_TRANS.o_ACCT_ID (not t.TX_TYPE_CD) |

For DEMO_TARGET5 every row follows sq_demo_source4 → exp_TRANS →
exp_TRANS1 → rtr_TRANS.demo_target5_GRP, without aggregation.

| DEMO_TARGET5 column | Source and expression |
|---|---|
| ACCT_ID | a.ACCT_ID passthrough |
| FIRST_NM | lkp_TRANS2.FIRST_NM by a.ACCT_ID, not t.FIRST_NM |
| LAST_NM | t.LAST_NM passthrough |
| BAL_AMT | t.BAL_AMT passthrough, FLOAT |
| CRDT_SCORE | lkp_TRANS3.CRDT_SCORE by t.CUST_ID, not t.CRDT_SCORE; NUMBER(38,0) |

For DEMO_TARGET3 every row follows DEMO_SOURCE5 → SQ_demo_source5 →
exp_TRANS2; no filter, join or aggregation.

| DEMO_TARGET3 column | Source and expression |
|---|---|
| PRODUCT_ID | DEMO_SOURCE5.PRODUCT_ID passthrough, VARCHAR |
| PRODUCT_NM | DEMO_SOURCE5.PRODUCT_NM passthrough, VARCHAR |
| PRODUCT_NO | DEMO_SOURCE5.PRODUCT_NO passthrough, VARCHAR |
| COLOR | DEMO_SOURCE5.COLOR passthrough, VARCHAR |
| STD_COST | DEMO_SOURCE5.STD_COST → NUMBER(38,0) |
| LIST_PRICE | DEMO_SOURCE5.LIST_PRICE → NUMBER(38,0) |
| SELL_ST_DT | exp_TRANS2.o_SELL_ST_DT = TO_DATE(TO_CHAR(SYSDATE),'DD/MM/YYYY'); reproduced as NULL DATE |
| SELL_ED_DT | DEMO_SOURCE5.SELL_ED_DT → exp_TRANS2.o_SELL_ED_DT = TO_DATE(SELL_ED_DT,'DD/MM/YYYY'); substrings 7:4, 4:2, 1:2 form ISO DATE |

## SQL override (verbatim XML value, line endings normalized)

```sql
SELECT demo_source4.ACCT_ID, demo_source4.ACCT_TYP, demo_source4.ACCT_DESC, demo_source4.CRDT_LN, SYSTIMESTAMP, demo_source4.CLSR_DT, demo_source4.ACCT_STAT_CD, demo_source3.TX_ID, demo_source3.LAST_NM, demo_source3.TX_DTTM, demo_source3.TX_AMT, demo_source3.BAL_AMT, demo_source3.CUST_ID, STRCMP(demo_source4.ACCT_STAT_CD,demo_source3.TX_TYPE_CD)
FROM
 demo_source3 INNER JOIN demo_source4 ON demo_source3.ACCT_ID = demo_source4.ACCT_ID
ORDER BY
 demo_source4.ACCT_ID
```

## Legacy anomalies and physical contract

- The SQL override substitutes SYSTIMESTAMP for source CR8_DT; deterministic
  baseline pins it to midnight 2024-01-31. The intermediate retains a timestamp;
  the mart casts to DATE to match landed INFA_BASELINE.
- The final override expression STRCMP occupies TX_TYPE_CD but has no
  downstream consumer; it is discarded. Actual target TX_TYPE_CD is lookup-derived.
- o_SELL_ST_DT ignores source SELL_ST_DT; its legacy date/string roundtrip is
  unparseable under the baseline contract and remains NULL, not today's date.
- XML aggregator GENERAL ports use last-row semantics; baseline resolves that
  to highest TX_ID. XML only orders accounts, not transaction ties; no stronger
  tie rule is asserted. SUM is not rounded to the XML decimal port scale.
- XML SEQ_GEN current value is 281, reset NO, cycle YES. Baseline makes this
  repeatable by assigning 281 onward in account order instead of mutable state.
- Snowflake information_schema.columns was inspected for all three baseline
  targets. Numeric-looking strings STD_COST, LIST_PRICE and CRDT_LN are NUMBER;
  CR8_DT is DATE. All-null SELL_ST_DT landed as TEXT, while the model expresses
  the intended DATE type with identical NULL values. Other types match sensibly.
- Mart filenames use uppercase names and unquoted Snowflake identifiers resolve
  to DEMO_TARGET3/5/6. Existing generate_schema_name returns INFA_TARGET;
  folder materializations, RUN tag and legacy_unit metadata are inherited.
- Keys: PRODUCT_ID (target3), ACCT_ID (target5/6), tested not-null and unique.
  Relationships test target5 ACCT_ID/FIRST_NM to lkp_TRANS2 and CRDT_SCORE
  to lkp_TRANS3, and target6 ACCT_ID/TX_TYPE_CD to lkp_TRANS1. Customer ID is
  not projected by target5, so a direct customer-key relationship is unavailable.
  A value relationship for CRDT_SCORE cannot independently prove customer
  alignment; the keyed parity report verifies that association.
