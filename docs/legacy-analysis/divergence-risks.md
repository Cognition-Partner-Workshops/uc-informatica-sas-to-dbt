# Informatica-to-dbt divergence risks

This is a ranked list of silent-data-impact risks found while reverse
engineering `legacy/informatica/wf_demo_mapping.XML`. Line numbers refer to
the checked-in XML export.

## R1 — SQL-override position changes `CR8_DT`

**XML evidence.** XML line 580 contains the literal
`SYSTIMESTAMP` in the `sq_demo_source4` SQL override. XML line 792 contains
`FROMFIELD ="CR8_DT" FROMINSTANCE ="agg_TRANS"` and
`TOFIELD ="CR8_DT" TOINSTANCE ="demo_target6"`.

**Wrong-but-obvious translation.**

```sql
demo_source4.CR8_DT AS CR8_DT
```

**Correct translation.**

```sql
CAST('2024-01-31 00:00:00' AS TIMESTAMP) AS CR8_DT
```

**Test that catches it.** Reconcile `demo_target6.CR8_DT` to the pinned
business timestamp for every output row; error severity.

## R2 — SQL-override position 14 is a discarded `STRCMP`

**XML evidence.** XML line 580 contains the literal
`STRCMP(demo_source4.ACCT_STAT_CD,demo_source3.TX_TYPE_CD)` as select item 14.
The target connector block contains no connector whose
`FROMINSTANCE` is `sq_demo_source4` and whose `FROMFIELD` is `TX_TYPE_CD`;
the grep for that exact pair returns no match. XML line 794 contains
`FROMFIELD ="CRDT_SCORE2" FROMINSTANCE ="rtr_TRANS"` and
`TOFIELD ="CRDT_SCORE" TOINSTANCE ="demo_target5"`.

**Wrong-but-obvious translation.**

```sql
demo_source3.TX_TYPE_CD AS TX_TYPE_CD
```

**Correct translation.** The positional SQ `TX_TYPE_CD` port is dead and must
not appear in the staging model. The physical target column is populated by
the lookup lineage in R3; it is not populated by this `STRCMP` result.

**Test that catches it.** Assert that the override-only `TX_TYPE_CD` port has
no downstream connector and that target6's value is sourced only through the
lookup described in R3.

## R3 — Target6 transaction type comes from an unconnected lookup

**XML evidence.** XML line 608 contains
`EXPRESSION =":LKP.lkp_TRANS1(ACCT_ID)"` and `NAME ="o_ACCT_ID"`.
XML line 529 contains `NAME ="TX_TYPE_CD"` and
`PORTTYPE ="LOOKUP/RETURN/OUTPUT"`. XML line 533 contains
`NAME ="Lookup table name" VALUE ="lkp_demo_source3"` and line 537 contains
`NAME ="Lookup condition" VALUE ="ACCT_ID =  IN_ACCT_ID"`. XML line 786 contains
`FROMFIELD ="o_ACCT_ID" FROMINSTANCE ="agg_TRANS"` and
`TOFIELD ="TX_TYPE_CD" TOINSTANCE ="demo_target6"`.

**Wrong-but-obvious translation.**

```sql
demo_source3.TX_TYPE_CD AS TX_TYPE_CD
```

**Correct translation.**

```sql
last_value(lkp_demo_source3.TX_TYPE_CD)
  OVER (PARTITION BY lkp_demo_source3.ACCT_ID ORDER BY source_row DESC)
  AS TX_TYPE_CD
```

**Test that catches it.** Reconcile target6 `TX_TYPE_CD` to the last matching
`lkp_demo_source3.TX_TYPE_CD` by account; error severity.

## R4 — Aggregator pass-through ports are last-row values

**XML evidence.** XML line 452 contains
`EXPRESSIONTYPE ="GROUPBY"`. XML line 454 contains
`EXPRESSION ="SUM(TX_AMT)"`; the remaining Aggregator ports are pass-through
ports in the same transformation.

**Wrong-but-obvious translation.**

```sql
GROUP BY ACCT_ID, ACCT_DESC, TX_ID, TX_DTTM, TX_AMT, ...
```

**Correct translation.**

```sql
QUALIFY ROW_NUMBER() OVER (PARTITION BY ACCT_ID ORDER BY TX_ID DESC) = 1
-- with SUM(TX_AMT) OVER (PARTITION BY ACCT_ID) for the aggregate output
```

**Test that catches it.** Assert one target6 row per `ACCT_ID`, and reconcile
pass-through values to the documented highest-`TX_ID` baseline row.

## R5 — Router default and NULL rows are discarded

**XML evidence.** The router group definitions include the literal
`NAME ="DEFAULT1"` at XML line 670. The default output port
`GROUP ="DEFAULT1"` is present at XML line 730. The connector block contains
no connector from a `rtr_TRANS` `DEFAULT1` output to a target; the grep for
`FROMINSTANCE ="rtr_TRANS".*FROMFIELD =".*3"` returns no default-group
target connector.

**Wrong-but-obvious translation.**

```sql
CASE WHEN ACCT_TYP = 'SB' THEN target6 ELSE target5 END
```

**Correct translation.**

```sql
-- independently emit only the explicit groups:
WHERE ACCT_TYP = 'SB'
WHERE ACCT_TYP <> 'SB'
-- NULL matches neither predicate and is discarded
```

**Test that catches it.** Assert that NULL `ACCT_TYP` produces no target5 or
target6 row; error severity.

## R6 — Router groups are independent, not an if/else chain

**XML evidence.** XML line 807 contains
`FROMFIELD ="o_ACCT_DESC1" FROMINSTANCE ="rtr_TRANS"` and
`TOINSTANCE ="agg_TRANS"`; separate router output connectors occur elsewhere
in the connector block. The independent group definitions are represented by
the router groups in the router transformation.

**Wrong-but-obvious translation.**

```sql
CASE WHEN condition_1 THEN branch_1 ELSE branch_2 END
```

**Correct translation.**

```sql
SELECT ... FROM input WHERE condition_1
UNION ALL
SELECT ... FROM input WHERE condition_2
```

**Test that catches it.** Assert mutual exclusivity only where explicitly
required; separately assert router output counts by group and permit a row to
occur in more than one branch.

## R7 — `MD5_src` and `MD5_tgt` are not comparable change hashes

**XML evidence.** XML line 177 contains
`AES_DECRYPT(LEAD_CO_MNE1, SUBSTR(SHORT_NAME,1,3), 256)`.
XML line 178 contains
`MD5(LEAD_CO_MNE || BRANCH_CO_MNE || MIS_DATE || DESCRIPTION || SHORT_NAME)`;
XML line 179 contains `MD5_tgt != MD5_src`.

**Wrong-but-obvious translation.**

```sql
CASE WHEN md5(source_columns) <> md5(target_columns) THEN 'Update' END
```

**Correct translation.**

```sql
CASE WHEN existing_key IS NOT NULL
          AND MD5(source_columns) <> AES_DECRYPT(existing_value, key, 256)
     THEN 'Update'
END
```

**Test that catches it.** Assert that every matched lookup row is routed to the
update branch for this export; severity error. Do not replace this with a
real MD5-vs-MD5 comparison.

## R8 — IIF without ELSE yields NULL and drives data-driven routing

**XML evidence.** XML line 176 contains
`IIF(ISNULL(Key),&apos;Insert&apos;)` and XML line 179 contains
`IIF(NOT ISNULL(Key) AND  (MD5_tgt != MD5_src),&apos;Update&apos;)`;
neither expression has an ELSE branch.
The session uses `VALUE ="Data driven"` at XML line 1434 and the update
strategy is `VALUE ="DD_UPDATE"` at XML line 341.

**Wrong-but-obvious translation.**

```sql
COALESCE(CASE WHEN ... THEN 'Insert' END, 'N')
```

**Correct translation.**

```sql
CASE WHEN key IS NULL THEN 'Insert' END
-- NULL remains NULL when the predicate is false
```

**Test that catches it.** Assert branch counts and assert no synthetic `'N'`
values appear in the routing ports.

## R9 — Unconnected UPDATE ports preserve existing values

**XML evidence.** XML line 88 contains `NAME ="CREATED_BY"` and XML line 89
contains `NAME ="CREATED_TIME"`. A grep of the complete connector block for
`TOINSTANCE ="demo_target1_UPD"` with either target field returns no match.

**Wrong-but-obvious translation.**

```sql
UPDATE target SET CREATED_BY = NULL, CREATED_TIME = NULL, ...
```

**Correct translation.**

```sql
UPDATE target
SET UPDATED_BY = 'IDWUSER', UPDATED_TIME = CURRENT_TIMESTAMP
-- omit unconnected CREATED_* columns from SET
```

**Test that catches it.** Reconcile update rows against pre-run target state and
assert `CREATED_*` preservation. Baseline CSVs are row images, not merged
table state.

## R10 — Target instances share physical tables

**XML evidence.** XML line 345 contains
`NAME ="demo_target1_UPD" TRANSFORMATION_NAME ="demo_target1"` and XML line
346 contains the corresponding `demo_target1_INS` instance. The two
`demo_target2` instances likewise carry `TRANSFORMATION_NAME ="demo_target2"`
in their target-instance definitions.

**Wrong-but-obvious translation.**

```sql
ASSERT UNIQUE (instance_name, key)
```

**Correct translation.**

```sql
ASSERT UNIQUE (physical_table, key)
-- validate the union of all instances writing that table
```

**Test that catches it.** Run uniqueness checks over the union of insert/update
instances for each physical target.

## R11 — Source qualifier WHERE filter is not a Filter transformation

**XML evidence.** Line 916 contains the `SQ_demo_source2` override ending in
`where demo_source2.Member_Type_Code is not null`.

**Wrong-but-obvious translation.**

```sql
SELECT * FROM demo_source2
```

**Correct translation.**

```sql
SELECT * FROM demo_source2
WHERE Member_Type_Code IS NOT NULL
```

**Test that catches it.** Assert that no output row has a NULL
`Member_Type_Code`; error severity.

## R12 — ABORT is a hard failure, not a filter or NULL fill

**XML evidence.** XML line 942 contains the passthrough
`NAME ="Relationship_to_Subscriber_Code_Label"`; XML line 943 contains
`NAME ="o_Relationship_to_Subscriber_Code_Label"` and
`ABORT(&apos;Relationship_to_Subscriber_Code_Labe valuel is null&apos;)`.
XML line 1086 contains `FROMFIELD ="o_Relationship_to_Subscriber_Code_Label"`
and connects only that `o_` port to the router.

**Wrong-but-obvious translation.**

```sql
WHERE Relationship_to_Subscriber_Code_Label IS NOT NULL
-- or COALESCE(Relationship_to_Subscriber_Code_Label, 'UNKNOWN')
```

**Correct translation.**

```sql
CASE WHEN Relationship_to_Subscriber_Code_Label IS NULL
     THEN ERROR('Relationship_to_Subscriber_Code_Label is null')
     ELSE Relationship_to_Subscriber_Code_Label
END
```

**Test that catches it.** An error-severity `not_null` test on filtered-in
rows must fail the run, not filter rows or fill NULLs.

## R13 — Sell-start expression's incompatible date conversion yields NULL

**XML evidence.** XML line 662 defines
`TO_DATE(TO_CHAR(SYSDATE),'DD/MM/YYYY')` on `o_SELL_ST_DT`; XML line 805
contains `FROMFIELD ="o_SELL_ST_DT"` and `TOFIELD ="SELL_ST_DT"`. The port is
connected; the baseline NULL results from the incompatible conversion mask.

**Wrong-but-obvious translation.**

```sql
TRY_TO_DATE(TO_CHAR(CURRENT_TIMESTAMP), 'DD/MM/YYYY') AS SELL_ST_DT
```

**Correct translation.**

```sql
CAST(NULL AS DATE) AS SELL_ST_DT -- result of the legacy conversion
```

**Test that catches it.** Assert target3 `SELL_ST_DT IS NULL`; error severity
if any non-NULL value appears.

## R14 — Sell-end date mask disagrees with the flat-file format

**XML evidence.** XML line 663 uses
`TO_DATE(SELL_ED_DT,&apos;DD/MM/YYYY&apos;)`. XML line 50 declares
`NAME ="Datetime Format" VALUE ="A  19 mm/dd/yyyy hh24:mi:ss"`.

**Wrong-but-obvious translation.**

```sql
TRY_TO_DATE(SELL_ED_DT, 'MM/DD/YYYY HH24:MI:SS')
```

**Correct translation.**

```sql
TRY_TO_DATE(SELL_ED_DT, 'DD/MM/YYYY')
```

**Test that catches it.** Reconcile parsed dates against the PowerCenter
baseline, including dates where day and month are both <= 12 and dates that
must error under the legacy mask.

## R15 — `$Target` lookup reads pre-run target state

**XML evidence.** XML line 287 contains
`NAME ="Connection Information" VALUE ="$Target"`. XML line 386 contains
`TOINSTANCE ="LKPTRANS"` and XML line 392 contains
`FROMINSTANCE ="LKPTRANS"` and `TOINSTANCE ="EXPTRANS"`.

**Wrong-but-obvious translation.**

```sql
JOIN {{ ref('demo_target1') }} current_target USING (ID)
```

**Correct translation.**

```sql
JOIN demo_target1_pre_run USING (ID)
-- snapshot the target before this session writes it
```

**Test that catches it.** Execute mapping2 against a frozen pre-run target
fixture and assert lookup values do not include rows inserted in the same run.

## R16 — `Use Last Value` requires deterministic deduplication

**XML evidence.** XML lines 498, 536, and 624 each contain
`NAME ="Lookup policy on multiple match" VALUE ="Use Last Value"` for the
three lookup transformations.

**Wrong-but-obvious translation.**

```sql
LEFT JOIN lookup USING (key)
```

**Correct translation.**

```sql
QUALIFY ROW_NUMBER() OVER (PARTITION BY key ORDER BY legacy_row_order DESC) = 1
```

**Test that catches it.** Assert one lookup row per key and reconcile duplicate
keys to the last-row fixture.

## R17 — Lookup comparisons are case-insensitive with explicit NULL ordering

**XML evidence.** XML line 646 contains
`NAME ="Case Sensitive String Comparison" VALUE ="NO"`; line 647 contains
`NAME ="Null ordering" VALUE ="Null Is Highest Value"`; line 648 contains
`NAME ="Sorted Input" VALUE ="NO"`.

**Wrong-but-obvious translation.**

```sql
ON left.key = right.key
```

**Correct translation.**

```sql
ON UPPER(left.key) = UPPER(right.key)
-- rank NULL explicitly as the highest lookup value where applicable
```

**Test that catches it.** Include mixed-case keys and NULL lookup keys in
reconciliation fixtures.

## R18 — Same-named target columns come from different lookup tables

**XML evidence.** XML line 832 contains
`FROMFIELD ="FIRST_NM" FROMINSTANCE ="lkp_TRANS2"` and XML line 833 contains
`FROMFIELD ="CRDT_SCORE" FROMINSTANCE ="lkp_TRANS3"`. XML line 797 contains
`TOFIELD ="FIRST_NM" TOINSTANCE ="demo_target5"` and XML line 794 contains
`TOFIELD ="CRDT_SCORE" TOINSTANCE ="demo_target5"`.

**Wrong-but-obvious translation.**

```sql
demo_source3.FIRST_NM, demo_source3.CRDT_SCORE
```

**Correct translation.**

```sql
lkp_demo_source1.FIRST_NM,
lkp_demo_source2.CRDT_SCORE
```

**Test that catches it.** Seed deliberately conflicting same-named source and
lookup values and reconcile target5 to the lookup values.

## R19 — Sequence generators have live current values and cycling semantics

**XML evidence.** XML line 429 contains `NAME ="SEQ_GEN"`; line 435 contains
`NAME ="Current Value" VALUE ="281"` and line 436 contains
`NAME ="Cycle" VALUE ="YES"`. XML line 314 contains `NAME ="SEQTRANS"` and
line 320 contains `NAME ="Current Value" VALUE ="57"`.
The sequence connectors are XML line 785
(`FROMFIELD ="NEXTVAL" FROMINSTANCE ="SEQ_GEN"`) and XML line 373
(`FROMFIELD ="NEXTVAL" FROMINSTANCE ="SEQTRANS"`).

**Wrong-but-obvious translation.**

```sql
ROW_NUMBER() OVER () AS Key
```

**Correct translation.**

```sql
280 + ROW_NUMBER() OVER (ORDER BY ACCT_ID) AS ACCT_KEY
56 + ROW_NUMBER() OVER (ORDER BY ID) AS Key
```

**Test that catches it.** Reconcile generated keys exactly to the seeded
current values: the baseline has `min(ACCT_KEY) = 281` and `min(Key) = 57`.
Assert cycle behavior at the boundary.

## R20 — Updates retain lookup keys; inserts generate keys

**XML evidence.** XML line 392 contains
`FROMFIELD ="Key" FROMINSTANCE ="LKPTRANS"` into `EXPTRANS`, and XML line 423
contains `FROMFIELD ="Key3" FROMINSTANCE ="RTRTRANS"` into `UPDTRANS`. XML
line 373 contains `FROMFIELD ="NEXTVAL" FROMINSTANCE ="SEQTRANS"` and
`TOFIELD ="Key" TOINSTANCE ="demo_target1_INS"`.

**Wrong-but-obvious translation.**

```sql
SEQTRANS.NEXTVAL AS Key -- for both branches
```

**Correct translation.**

```sql
existing_target.Key AS Key -- UPDATE
SEQTRANS.NEXTVAL AS Key    -- INSERT
```

**Test that catches it.** Assert update keys equal pre-run target keys and
insert keys do not overwrite them.

## R21 — Port precision truncates before the target

**XML evidence.** XML line 55 contains `NAME ="PRODUCT_ID"` and
`PRECISION ="256"`; line 659 contains `NAME ="PRODUCT_ID"` and
`PRECISION ="8"`. XML line 99 contains `NAME ="ACCT_DESC"` and
`PRECISION ="10"`; line 26 contains `NAME ="ACCT_DESC"` and
`PRECISION ="50"`.

**Wrong-but-obvious translation.**

```sql
source_value AS PRODUCT_ID
```

**Correct translation.**

```sql
SUBSTR(source_value, 1, 8) AS PRODUCT_ID
SUBSTR(RTRIM(ACCT_DESC), 1, 10) AS ACCT_DESC
```

**Test that catches it.** Include over-precision fixtures and reconcile
truncated port values, not only target-column casts.

## R22 — Expression output names are misleading

**XML evidence.** XML line 606 contains `EXPRESSION ="RTRIM(ACCT_TYP)"`;
line 607 contains `EXPRESSION ="LTRIM(CRDT_LN)"`; line 479 contains
`EXPRESSION ="RTRIM(ACCT_DESC)"`. The generated STM traces these outputs to
their target6 columns; the connector block has no name-based substitution.

**Wrong-but-obvious translation.**

```sql
o_acc_trim AS ACCT_DESC
o_crdt_trim AS ACCT_TYP
```

**Correct translation.**

```sql
RTRIM(ACCT_TYP) AS ACCT_TYP
LTRIM(CRDT_LN) AS CRDT_LN
RTRIM(ACCT_DESC) AS ACCT_DESC
```

**Test that catches it.** Reconcile each target6 column to its defining
expression and include values that distinguish trimming direction.

## R23 — Unconnected target columns remain NULL

**XML evidence.** XML line 92 contains `NAME ="ACTIVE_FLAG"`, line 93
contains `NAME ="START_DATE"`, and line 94 contains `NAME ="END_DATE"`. Grep
of all target connector `TOFIELD` values returns no match for those three
columns.

**Wrong-but-obvious translation.**

```sql
COALESCE(ACTIVE_FLAG, 'Y'), CURRENT_DATE, NULL
```

**Correct translation.**

```sql
CAST(NULL AS VARCHAR) AS ACTIVE_FLAG,
CAST(NULL AS TIMESTAMP) AS START_DATE,
CAST(NULL AS TIMESTAMP) AS END_DATE
```

**Test that catches it.** Assert all three columns are NULL in both insert and
update row images.

## R24 — Sorted input makes last-row selection order-sensitive

**XML evidence.** XML line 457 contains `NAME ="Sorted Input" VALUE ="YES"`.
XML line 580 contains `ORDER BY` and `demo_source4.ACCT_ID` in the SQL
override.

**Wrong-but-obvious translation.**

```sql
ANY_VALUE(column) OVER (PARTITION BY ACCT_ID)
```

**Correct translation.**

```sql
ROW_NUMBER() OVER (PARTITION BY ACCT_ID ORDER BY TX_ID DESC) = 1
```

**Test that catches it.** State and test the baseline tie-break explicitly:
highest `TX_ID` within an account. Do not rely on warehouse input order.

## R25 — Flat-file reader settings change parsing

**XML evidence.** XML line 7 contains
`CONSECDELIMITERSASONE ="NO"` and `SKIPROWS ="1"`; line 46 contains
`CONSECDELIMITERSASONE ="YES"` and `SKIPROWS ="0"`. Both lines contain
`NULL_CHARACTER ="*"`. XML lines 11 and 50 contain the two
`Datetime Format` attributes.

**Wrong-but-obvious translation.**

```sql
read_csv(path, header = true, nullstr = '')
```

**Correct translation.**

```sql
# Pseudocode: apply these reader settings before relational transforms.
read_csv(source1, skiprows=1, nullstr='*', delim=',')
read_csv(source5, skiprows=0, nullstr='*', delim=',')
configure_consecutive_delimiter_handling(source1, false)
configure_consecutive_delimiter_handling(source5, true)
```

**Test that catches it.** Reconcile row counts, literal-star fields, repeated
delimiters, and date parsing separately for both readers.

## R26 — `ERROR()` rejection differs from `ABORT()`

**XML evidence.** XML line 176 contains
`DEFAULTVALUE ="ERROR(&apos;transformation error&apos;)"`; line 179 contains
the same default. XML line 1114 contains `NAME ="Stop on errors" VALUE ="0"`;
the update strategy's `NAME ="Forward Rejected Rows" VALUE ="YES"` attribute is in the same
transformation configuration as `DD_UPDATE` at XML line 342.

**Wrong-but-obvious translation.**

```sql
RAISE_ERROR(...) -- for every transformation error
```

**Correct translation.**

```sql
-- reject the bad row, continue the session, and preserve reject accounting
```

**Test that catches it.** Use separate fixtures for transformation errors and
the mapping3 ABORT condition; assert rejection/continuation for the former
and hard session failure for the latter.

## R27 — Workflow order and target load order are semantic

**XML evidence.** XML line 1469 contains
`CONDITION ="$Decision2.Condition = 1"` and `TOTASK ="s_m_demo_mapping3"`;
line 1470 contains `CONDITION ="" FROMTASK ="Decision1"` and
`TOTASK ="s_m_demo_mapping1"`. XML line 895 contains
`TARGETINSTANCE ="demo_target6"`, line 896 contains
`TARGETINSTANCE ="demo_target5"`, and line 897 contains
`TARGETINSTANCE ="demo_target3"`. Mapping2's `$Target`
lookup is the attribute at XML line 287.

**Wrong-but-obvious translation.**

```sql
dbt run --select +all_targets  -- let dependency inference choose order
```

**Correct translation.**

```sql
run mapping2
run mapping1  -- unconditional after mapping2 decision task
run mapping3  -- only when mapping1 succeeds
```

**Test that catches it.** Execute a workflow-level reconciliation asserting
session order, decision conditions, pre-run lookup snapshots, and target6 /
target5-before-target3 writer ordering.
