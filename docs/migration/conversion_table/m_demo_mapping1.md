# Conversion table — `m_demo_mapping1`

Targets: `demo_target3`, `demo_target5`, `demo_target6`. XML: `legacy/informatica/wf_demo_mapping.XML`
(mapping spans L428–L899). Converted module:
`pyspark/informatica/informatica_pyspark/mappings/m_demo_mapping1.py`.

One row per transformation expression in the XML: every `TRANSFORMFIELD` with a non-empty `EXPRESSION`,
plus the Source Qualifier SQL override, every lookup condition and multiple-match policy, every router
group condition, the aggregator group-by and aggregate ports, and the sequence generator's state.

## Rubric (verbatim from `docs/migration/01_confidence_rubric.md`)

* **HIGH** — semantics are unambiguous in the XML **and** at least one baseline row would fail parity
  if the conversion were wrong.
* **MEDIUM** — unambiguous, but weakly exercised: the output is constant or degenerate in the seed
  data, so parity cannot catch a wrong conversion.
* **LOW** — the conversion rests on a judgement call the XML does not determine; the row must name the
  alternative that was rejected.
* **NOT MIGRATED** — deliberately not converted (e.g. a port with no outgoing CONNECTOR); every such
  element must be named.

## Counts

| Rating | Rows |
|---|---:|
| HIGH | 51 |
| MEDIUM | 12 |
| LOW | 11 |
| NOT MIGRATED | 10 |
| **Total** | **84** |

Two NOT MIGRATED elements (`SEQ_GEN.CURRVAL` and the `sq_demo_source4.TX_TYPE_CD` port) appear twice:
once where they arise and once in the dead-port list at the end, so there are 82 distinct elements.

## Source Qualifier `sq_demo_source4`

| Mapping | Transformation | Port / element | Informatica code (verbatim) | XML line | PySpark conversion (snippet or `file:lines`) | Confidence | Reason (required unless HIGH) |
|---|---|---|---|---:|---|---|---|
| m_demo_mapping1 | sq_demo_source4 | `Sql Query` (join + projection) | `SELECT demo_source4.ACCT_ID, demo_source4.ACCT_TYP, demo_source4.ACCT_DESC, demo_source4.CRDT_LN, SYSTIMESTAMP, demo_source4.CLSR_DT, demo_source4.ACCT_STAT_CD, demo_source3.TX_ID, demo_source3.LAST_NM, demo_source3.TX_DTTM, demo_source3.TX_AMT, demo_source3.BAL_AMT, demo_source3.CUST_ID, STRCMP(demo_source4.ACCT_STAT_CD,demo_source3.TX_TYPE_CD) FROM demo_source3 INNER JOIN demo_source4 ON demo_source3.ACCT_ID = demo_source4.ACCT_ID ORDER BY demo_source4.ACCT_ID` | 580 | `source4.join(source3, F.col("source4.ACCT_ID") == F.col("source3.ACCT_ID"), "inner").select(...)` — the 13 live ports projected in SQ port order | HIGH | |
| m_demo_mapping1 | sq_demo_source4 | select item 5 → port `CR8_DT` (**DEF-1**) | `SYSTIMESTAMP` | 580 | `F.lit(ctx.cfg.business_date).cast("date").alias("CR8_DT")` | HIGH | |
| m_demo_mapping1 | sq_demo_source4 | select item 14 → port `TX_TYPE_CD` (**DEF-1b**) | `STRCMP(demo_source4.ACCT_STAT_CD,demo_source3.TX_TYPE_CD)` | 580 | not converted | NOT MIGRATED | The SQ port `TX_TYPE_CD` (L579) has no outgoing `CONNECTOR`: Informatica computes the comparison and discards it. Converting it would add a column no target reads. Note `demo_target6.TX_TYPE_CD` is fed by `lkp_TRANS1`, not by this port — a name-matched conversion would silently put a string-comparison integer in that column. |
| m_demo_mapping1 | sq_demo_source4 | `ORDER BY` / `Number Of Sorted Ports` | `ORDER BY demo_source4.ACCT_ID` / `Number Of Sorted Ports = 1` | 580, 583 | not converted | NOT MIGRATED | Row order carries no meaning downstream: the only consumer of arrival order would be the aggregator's pass-through ports, and the SQ itself declares `Output is deterministic = NO` / `Output is repeatable = Never` (L589–590), which is precisely why DECISION-1 replaces arrival order with highest `TX_ID`. The comparator aligns rows by key, so output order is not observable either. |

## Lookups

| Mapping | Transformation | Port / element | Informatica code (verbatim) | XML line | PySpark conversion (snippet or `file:lines`) | Confidence | Reason (required unless HIGH) |
|---|---|---|---|---:|---|---|---|
| m_demo_mapping1 | lkp_TRANS2 (`lkp_demo_source1`) | `Lookup condition` | `ACCT_ID = IN_ACCT_ID` | 499 | `sq.join(first_name, "ACCT_ID", "left")` | HIGH | |
| m_demo_mapping1 | lkp_TRANS2 | `Lookup policy on multiple match` | `Use Last Value` | 498 | `lookup(lkp_source1, ["ACCT_ID"], policy="Use Last Value")` (highest `__line_ordinal`) | MEDIUM | The only duplicated `ACCT_ID` in `lkp_demo_source1` is 1002 (`NINA` / `ZOE`), and account 1002 is `ACCT_TYP = 'SB'`, so it routes to `demo_target6` — which does not consume `FIRST_NM`. `Use First Value` would produce a byte-identical `demo_target5`. |
| m_demo_mapping1 | lkp_TRANS2 | `IN_ACCT_ID` | `IN_ACCT_ID` | 483 | join key `ACCT_ID` in the same expression | HIGH | |
| m_demo_mapping1 | lkp_TRANS2 | connected output `FIRST_NM` → `demo_target5.FIRST_NM` | *(lookup port, L486)* | 486 | `.select("ACCT_ID", F.col("FIRST_NM").alias("lkp_FIRST_NM"))`, later aliased to `FIRST_NM` | HIGH | |
| m_demo_mapping1 | lkp_TRANS3 (`lkp_demo_source2`) | `Lookup condition` | `CUST_ID = IN_CUST_ID` | 625 | `.join(credit_score, "CUST_ID", "left")` | HIGH | |
| m_demo_mapping1 | lkp_TRANS3 | `Lookup policy on multiple match` | `Use Last Value` | 624 | `lookup(lkp_source2, ["CUST_ID"], policy="Use Last Value")` | MEDIUM | The only duplicated `CUST_ID` in `lkp_demo_source2` is 70032 (`435` / `450`), which belongs to account 1002 — an `SB` account routed to `demo_target6`, which does not consume `CRDT_SCORE`. `Use First Value` would produce a byte-identical `demo_target5`. |
| m_demo_mapping1 | lkp_TRANS3 | `IN_CUST_ID` | `IN_CUST_ID` | 612 | join key `CUST_ID` in the same expression | HIGH | |
| m_demo_mapping1 | lkp_TRANS3 | connected output `CRDT_SCORE` → `demo_target5.CRDT_SCORE` | *(lookup port, L614)* | 614 | `.select("CUST_ID", F.col("CRDT_SCORE").alias("lkp_CRDT_SCORE"))` | HIGH | |
| m_demo_mapping1 | lkp_TRANS1 (`lkp_demo_source3`) | `Lookup condition` | `ACCT_ID =  IN_ACCT_ID` | 537 | `.join(transaction_type, "ACCT_ID", "left")` | HIGH | |
| m_demo_mapping1 | lkp_TRANS1 | `Lookup policy on multiple match` | `Use Last Value` | 536 | `lookup(lkp_source3, ["ACCT_ID"], policy="Use Last Value")` | HIGH | |
| m_demo_mapping1 | lkp_TRANS1 | RETURN port `TX_TYPE_CD` | *(`PORTTYPE = "LOOKUP/RETURN/OUTPUT"`)* | 529 | `F.col("TX_TYPE_CD").alias("lkp_TX_TYPE_CD")` — the unconnected call's return value | HIGH | |

## Expression `exp_TRANS`

| Mapping | Transformation | Port / element | Informatica code (verbatim) | XML line | PySpark conversion (snippet or `file:lines`) | Confidence | Reason (required unless HIGH) |
|---|---|---|---|---:|---|---|---|
| m_demo_mapping1 | exp_TRANS | `CLSR_DT` | `CLSR_DT` | 594 | pass-through to `demo_target6.CLSR_DT` | HIGH | |
| m_demo_mapping1 | exp_TRANS | `TX_DTTM` | `TX_DTTM` | 595 | pass-through to `demo_target6.TX_DTTM` | HIGH | |
| m_demo_mapping1 | exp_TRANS | `BAL_AMT` | `BAL_AMT` | 596 | pass-through to `demo_target5.BAL_AMT` | HIGH | |
| m_demo_mapping1 | exp_TRANS | `ACCT_DESC` | `ACCT_DESC` | 597 | pass-through into `exp_TRANS1.o_ACCT_DESC` | HIGH | |
| m_demo_mapping1 | exp_TRANS | `ACCT_TYP` | `ACCT_TYP` | 598 | pass-through; drives the router group conditions | HIGH | |
| m_demo_mapping1 | exp_TRANS | `ACCT_STAT_CD` | `ACCT_STAT_CD` | 599 | pass-through to `demo_target6.ACCT_STAT_CD` | HIGH | |
| m_demo_mapping1 | exp_TRANS | `TX_ID` | `TX_ID` | 600 | pass-through to `demo_target6.TX_ID`; also the DECISION-1 ordering key | HIGH | |
| m_demo_mapping1 | exp_TRANS | `LAST_NM` | `LAST_NM` | 601 | pass-through to `demo_target5.LAST_NM` | HIGH | |
| m_demo_mapping1 | exp_TRANS | `TX_AMT` | `TX_AMT` | 602 | pass-through into `agg_TRANS.o_TX_AMT` | HIGH | |
| m_demo_mapping1 | exp_TRANS | `ACCT_ID` | `ACCT_ID` | 603 | pass-through to `demo_target5.ACCT_ID` / `demo_target6.ACCT_ID`; aggregator group-by key | HIGH | |
| m_demo_mapping1 | exp_TRANS | `CR8_DT` | `CR8_DT` | 604 | pass-through of the DEF-1 pinned business date to `demo_target6.CR8_DT` | MEDIUM | The value is the constant `2024-01-31` for every row (DEF-1 replaced the source column upstream), so any conversion that carries a single constant through unchanged passes parity; only the DEF-1 row above is actually exercised. |
| m_demo_mapping1 | exp_TRANS | `CUST_ID` | `CUST_ID` | 605 | pass-through; join key for `lkp_TRANS3` | HIGH | |
| m_demo_mapping1 | exp_TRANS | `o_acc_trim` | `RTRIM(ACCT_TYP)` | 606 | `.withColumn("o_acc_trim", rtrim("ACCT_TYP"))` | MEDIUM | No `ACCT_TYP` value in `demo_source4` has trailing blanks (`SB`, `CA`, NULL), so dropping the `RTRIM` entirely — or using a full `trim` — yields identical `demo_target6.ACCT_TYP` values and parity still passes. |
| m_demo_mapping1 | exp_TRANS | `o_crdt_trim` | `LTRIM(CRDT_LN)` | 607 | `.withColumn("o_crdt_trim", ltrim("CRDT_LN"))` | HIGH | |
| m_demo_mapping1 | exp_TRANS | `o_ACCT_ID` (unconnected lookup call) | `:LKP.lkp_TRANS1(ACCT_ID)` | 608 | `F.col("lkp_TX_TYPE_CD")`, ultimately aliased to `demo_target6.TX_TYPE_CD` | HIGH | |

## Expression `exp_TRANS1`

| Mapping | Transformation | Port / element | Informatica code (verbatim) | XML line | PySpark conversion (snippet or `file:lines`) | Confidence | Reason (required unless HIGH) |
|---|---|---|---|---:|---|---|---|
| m_demo_mapping1 | exp_TRANS1 | `FIRST_NM` | `FIRST_NM` | 463 | pass-through of the `lkp_TRANS2` value to `demo_target5.FIRST_NM` | HIGH | |
| m_demo_mapping1 | exp_TRANS1 | `CLSR_DT` | `CLSR_DT` | 464 | pass-through to `demo_target6.CLSR_DT` | HIGH | |
| m_demo_mapping1 | exp_TRANS1 | `TX_DTTM` | `TX_DTTM` | 465 | pass-through to `demo_target6.TX_DTTM` | HIGH | |
| m_demo_mapping1 | exp_TRANS1 | `BAL_AMT` | `BAL_AMT` | 466 | pass-through to `demo_target5.BAL_AMT` | HIGH | |
| m_demo_mapping1 | exp_TRANS1 | `ACCT_DESC` | `ACCT_DESC` | 467 | pass-through into `o_ACCT_DESC` | HIGH | |
| m_demo_mapping1 | exp_TRANS1 | `ACCT_TYP` | `ACCT_TYP` | 468 | pass-through; drives the router group conditions | HIGH | |
| m_demo_mapping1 | exp_TRANS1 | `ACCT_STAT_CD` | `ACCT_STAT_CD` | 469 | pass-through to `demo_target6.ACCT_STAT_CD` | HIGH | |
| m_demo_mapping1 | exp_TRANS1 | `TX_ID` | `TX_ID` | 470 | pass-through to `demo_target6.TX_ID` | HIGH | |
| m_demo_mapping1 | exp_TRANS1 | `LAST_NM` | `LAST_NM` | 471 | pass-through to `demo_target5.LAST_NM` | HIGH | |
| m_demo_mapping1 | exp_TRANS1 | `TX_AMT` | `TX_AMT` | 472 | pass-through into `agg_TRANS.o_TX_AMT` | HIGH | |
| m_demo_mapping1 | exp_TRANS1 | `ACCT_ID` | `ACCT_ID` | 473 | pass-through to both targets' `ACCT_ID` | HIGH | |
| m_demo_mapping1 | exp_TRANS1 | `CR8_DT` | `CR8_DT` | 474 | pass-through of the DEF-1 constant | MEDIUM | Same as `exp_TRANS.CR8_DT` (L604): a single constant value for every row, so a wrong pass-through cannot be distinguished by parity. |
| m_demo_mapping1 | exp_TRANS1 | `o_acc_trim` | `o_acc_trim` | 475 | pass-through to `demo_target6.ACCT_TYP` | HIGH | |
| m_demo_mapping1 | exp_TRANS1 | `o_crdt_trim` | `o_crdt_trim` | 476 | pass-through to `demo_target6.CRDT_LN` | HIGH | |
| m_demo_mapping1 | exp_TRANS1 | `o_ACCT_ID` | `o_ACCT_ID` | 477 | pass-through to `demo_target6.TX_TYPE_CD` | HIGH | |
| m_demo_mapping1 | exp_TRANS1 | `CRDT_SCORE` | `CRDT_SCORE` | 478 | pass-through of the `lkp_TRANS3` value to `demo_target5.CRDT_SCORE` | HIGH | |
| m_demo_mapping1 | exp_TRANS1 | `o_ACCT_DESC` | `RTRIM(ACCT_DESC)` | 479 | `.withColumn("o_ACCT_DESC", rtrim("ACCT_DESC"))` | MEDIUM | No `ACCT_DESC` value in `demo_source4` has trailing blanks (`Account 1001 ledger`, …), so omitting the `RTRIM` — or using a full `trim` — produces identical `demo_target6.ACCT_DESC` values and parity still passes. |

## Router `rtr_TRANS`

| Mapping | Transformation | Port / element | Informatica code (verbatim) | XML line | PySpark conversion (snippet or `file:lines`) | Confidence | Reason (required unless HIGH) |
|---|---|---|---|---:|---|---|---|
| m_demo_mapping1 | rtr_TRANS | `demo_target6_GRP` group condition | `ACCT_TYP = 'SB'` | 668 | `joined.where(F.col("ACCT_TYP") == F.lit("SB"))` | HIGH | |
| m_demo_mapping1 | rtr_TRANS | `demo_target5_GRP` group condition | `ACCT_TYP != 'SB'` | 669 | `joined.where(F.col("ACCT_TYP") != F.lit("SB"))` | HIGH | |
| m_demo_mapping1 | rtr_TRANS | `DEFAULT1` group | *(`TYPE = "OUTPUT/DEFAULT"`, no `EXPRESSION`)* | 670 | not converted | NOT MIGRATED | Every `DEFAULT1` port (L719–734) is unconnected, so no baseline row can originate from this group. |
| m_demo_mapping1 | rtr_TRANS | NULL-`ACCT_TYP` rows silently dropped (**DEF-4**) | *(consequence of the two group conditions plus the unconnected `DEFAULT1`)* | 668–670 | Spark three-valued logic: `ACCT_TYP != 'SB'` and `ACCT_TYP = 'SB'` are both NULL when `ACCT_TYP` is NULL, so neither branch keeps the row; no null handling is added | MEDIUM | Account 1005 (`ACCT_TYP` empty) is the only affected row and it is simply absent from both targets. Parity therefore only proves the row is *missing*, not that it was dropped by an unconnected router default: an explicit `WHERE ACCT_TYP IS NOT NULL` filter, or any other rule excluding NULL, produces the same two baseline files. Nothing in the seed distinguishes them. |

## Aggregator `agg_TRANS`

All pass-through ports below are `INPUT/OUTPUT` with `EXPRESSIONTYPE = "GENERAL"` and no aggregate
function, which in Informatica means "the last row of the group". The input is sorted by `ACCT_ID`
only, so "last row" within an account is undefined, and every one of these rows rests on the same
judgement call:

> **DECISION-1** — last = the row with the highest `TX_ID` in the account.
> *Rejected alternative:* the physical arrival order of the join, which the Source Qualifier itself
> declares non-repeatable (`Output is deterministic = NO`, `Output is repeatable = Never`, L589–590).

| Mapping | Transformation | Port / element | Informatica code (verbatim) | XML line | PySpark conversion (snippet or `file:lines`) | Confidence | Reason (required unless HIGH) |
|---|---|---|---|---:|---|---|---|
| m_demo_mapping1 | agg_TRANS | `ACCT_ID` (group-by) | `ACCT_ID` (`EXPRESSIONTYPE = "GROUPBY"`) | 452 | `Window.partitionBy("ACCT_ID")` for both the SUM and the DECISION-1 row pick | HIGH | |
| m_demo_mapping1 | agg_TRANS | `o_TX_AMT` (aggregate) | `SUM(TX_AMT)` | 454 | `F.sum("TX_AMT").over(account_window)` → `demo_target6.TX_AMT` | HIGH | |
| m_demo_mapping1 | agg_TRANS | `TX_ID` (pass-through) | `TX_ID` | 447 | `row_number().over(partitionBy("ACCT_ID").orderBy(F.col("TX_ID").desc())) == 1` | LOW | **DECISION-1.** Account 1001 has two transactions (`TX_ID` 5001 / 5002); arrival order would emit 5001, DECISION-1 emits 5002. Directly observable, and the XML does not determine which is correct. |
| m_demo_mapping1 | agg_TRANS | `TX_DTTM` (pass-through) | `TX_DTTM` | 449 | carried by the same DECISION-1 row pick | LOW | **DECISION-1.** Varies within account 1001 (`2024-01-14 10:28:00` vs `2024-01-15 11:00:00`), so the rejected alternative would emit a different value here too. |
| m_demo_mapping1 | agg_TRANS | `o_ACCT_DESC` (pass-through) | `o_ACCT_DESC` | 443 | carried by the same DECISION-1 row pick | LOW | **DECISION-1.** Account-invariant in the seed, so parity cannot distinguish DECISION-1 from the rejected arrival-order alternative for this port; it is rated with its group because it rests on the same undetermined semantics. |
| m_demo_mapping1 | agg_TRANS | `TX_AMT` (pass-through, superseded) | `TX_AMT` | 444 | not carried to the target — `demo_target6.TX_AMT` is fed by `o_TX_AMT` (L454) per the connector graph | LOW | **DECISION-1.** The port exists and would carry the group's last-row `TX_AMT`, but the only `CONNECTOR` into `demo_target6.TX_AMT` comes from `o_TX_AMT`; converting this port instead would emit `-100.0` rather than the `2031.24` sum for account 1001. Rated with its group because the pass-through semantics it encodes are the undetermined ones. |
| m_demo_mapping1 | agg_TRANS | `o_crdt_trim` (pass-through) | `o_crdt_trim` | 445 | carried by the same DECISION-1 row pick | LOW | **DECISION-1.** Account-invariant in the seed; see `o_ACCT_DESC`. |
| m_demo_mapping1 | agg_TRANS | `CLSR_DT` (pass-through) | `CLSR_DT` | 446 | carried by the same DECISION-1 row pick | LOW | **DECISION-1.** Account-invariant in the seed; see `o_ACCT_DESC`. |
| m_demo_mapping1 | agg_TRANS | `ACCT_STAT_CD` (pass-through) | `ACCT_STAT_CD` | 448 | carried by the same DECISION-1 row pick | LOW | **DECISION-1.** Account-invariant in the seed; see `o_ACCT_DESC`. |
| m_demo_mapping1 | agg_TRANS | `CR8_DT` (pass-through) | `CR8_DT` | 450 | carried by the same DECISION-1 row pick | LOW | **DECISION-1.** Constant `2024-01-31` for every row (DEF-1); see `o_ACCT_DESC`. |
| m_demo_mapping1 | agg_TRANS | `o_ACCT_ID` (pass-through) | `o_ACCT_ID` | 451 | carried by the same DECISION-1 row pick → `demo_target6.TX_TYPE_CD` | LOW | **DECISION-1.** Account-invariant in the seed (the lookup is keyed on `ACCT_ID`); see `o_ACCT_DESC`. |
| m_demo_mapping1 | agg_TRANS | `o_acc_trim` (pass-through) | `o_acc_trim` | 453 | carried by the same DECISION-1 row pick → `demo_target6.ACCT_TYP` | LOW | **DECISION-1.** Account-invariant in the seed; see `o_ACCT_DESC`. |

## Sequence generator `SEQ_GEN`

| Mapping | Transformation | Port / element | Informatica code (verbatim) | XML line | PySpark conversion (snippet or `file:lines`) | Confidence | Reason (required unless HIGH) |
|---|---|---|---|---:|---|---|---|
| m_demo_mapping1 | SEQ_GEN | `Current Value` | `<TABLEATTRIBUTE NAME ="Current Value" VALUE ="281"/>` | 435 | `sequence_nextval(aggregated, ["ACCT_ID"], 281)` | HIGH | |
| m_demo_mapping1 | SEQ_GEN | `NEXTVAL` → `demo_target6.ACCT_KEY` (consumption order) | `<TRANSFORMFIELD … NAME ="NEXTVAL" PORTTYPE ="OUTPUT" …/>` | 430 | `F.lit(281) + F.row_number().over(Window.orderBy("ACCT_ID")) - F.lit(1)` inside `sequence_nextval` | LOW | **DECISION-2** — groups consume `NEXTVAL` in ascending `ACCT_ID` order, giving `ACCT_KEY = 281 + rank(ACCT_ID) - 1`. *Rejected alternative:* arrival order of the aggregated groups, which the SQ declares non-repeatable. With only two accounts in the seed, ascending `ACCT_ID` and arrival order happen to coincide, so parity would not catch the wrong choice on a larger input. |
| m_demo_mapping1 | SEQ_GEN | `Increment By` | `<TABLEATTRIBUTE NAME ="Increment By" VALUE ="1"/>` | 433 | the `+ row_number() - 1` step inside `sequence_nextval` | MEDIUM | Only two values are generated (281, 282); an increment of 1 is indistinguishable from several other step rules over a two-row output — e.g. "index within the sorted group list" — so parity cannot catch a wrong increment. |
| m_demo_mapping1 | SEQ_GEN | `Start Value` | `<TABLEATTRIBUTE NAME ="Start Value" VALUE ="1"/>` | 432 | not used — `Current Value` (281) is the live counter | MEDIUM | `Start Value` only matters after a reset or a cycle, neither of which occurs; a conversion that wrongly started from 1 would be caught, but a conversion that simply ignores this attribute (as this one does) is indistinguishable from any other handling of it. |
| m_demo_mapping1 | SEQ_GEN | `End Value` | `<TABLEATTRIBUTE NAME ="End Value" VALUE ="2147483647"/>` | 434 | not converted | MEDIUM | Two values are consumed against a ceiling of 2^31−1; the bound is unreachable on any realistic input, so omitting it cannot be caught by parity. |
| m_demo_mapping1 | SEQ_GEN | `Cycle` | `<TABLEATTRIBUTE NAME ="Cycle" VALUE ="YES"/>` | 436 | not converted | MEDIUM | Cycling only takes effect at `End Value`, which is never reached, so the wrap-around branch is dead in the seed data and in any plausible input. |
| m_demo_mapping1 | SEQ_GEN | `CURRVAL` | `<TRANSFORMFIELD … NAME ="CURRVAL" PORTTYPE ="OUTPUT" …/>` | 431 | not converted | NOT MIGRATED | Listed in the lineage doc's dead-port list: no outgoing `CONNECTOR`. |

## Expression `exp_TRANS2` (pipeline 2 → `demo_target3`)

| Mapping | Transformation | Port / element | Informatica code (verbatim) | XML line | PySpark conversion (snippet or `file:lines`) | Confidence | Reason (required unless HIGH) |
|---|---|---|---|---:|---|---|---|
| m_demo_mapping1 | exp_TRANS2 | `PRODUCT_NO` | `PRODUCT_NO` | 654 | pass-through to `demo_target3.PRODUCT_NO` | HIGH | |
| m_demo_mapping1 | exp_TRANS2 | `STD_COST` | `STD_COST` | 655 | pass-through to `demo_target3.STD_COST` | HIGH | |
| m_demo_mapping1 | exp_TRANS2 | `COLOR` | `COLOR` | 656 | pass-through to `demo_target3.COLOR` | HIGH | |
| m_demo_mapping1 | exp_TRANS2 | `PRODUCT_ID` | `PRODUCT_ID` | 659 | pass-through to `demo_target3.PRODUCT_ID` | HIGH | |
| m_demo_mapping1 | exp_TRANS2 | `PRODUCT_NM` | `PRODUCT_NM` | 660 | pass-through to `demo_target3.PRODUCT_NM` | HIGH | |
| m_demo_mapping1 | exp_TRANS2 | `LIST_PRICE` | `LIST_PRICE` | 661 | pass-through to `demo_target3.LIST_PRICE` | HIGH | |
| m_demo_mapping1 | exp_TRANS2 | `o_SELL_ED_DT` | `TO_DATE(SELL_ED_DT,'DD/MM/YYYY')` | 663 | `infa_to_date("SELL_ED_DT", "DD/MM/YYYY").alias("SELL_ED_DT")` | HIGH | |
| m_demo_mapping1 | exp_TRANS2 | `o_SELL_ST_DT` (**DEF-3**) | `TO_DATE(TO_CHAR(SYSDATE),'DD/MM/YYYY')` | 662 | `infa_to_date(F.date_format(F.lit(ctx.cfg.business_date), "MM/dd/yyyy HH:mm:ss.SSSSSS"), "DD/MM/YYYY")` — the mask mismatch yields NULL for every row | MEDIUM | The resulting column is all-NULL, i.e. degenerate: a bare `F.lit(None).cast("date")`, or a conversion that fails to parse for a completely unrelated reason, produces a byte-identical `demo_target3.SELL_ST_DT`. Parity proves the column is empty, not that the emptiness comes from `TO_CHAR(SYSDATE)`'s `MM/DD/YYYY HH24:MI:SS.US` output failing the `DD/MM/YYYY` mask. The conversion is written to make the mismatch explicit rather than hard-coding NULL, and it is pinned by `test_mapping1_defect3_sell_start_date_is_null`. |
| m_demo_mapping1 | exp_TRANS2 | `SELL_ST_DT` (input port) | *(`PORTTYPE = "INPUT"`, no `EXPRESSION`)* | 658 | not converted | NOT MIGRATED | The source's real `SELL_ST_DT` is read by `SQ_demo_source5` and passed into `exp_TRANS2`, but no `CONNECTOR` leaves this input port — DEF-3 means `demo_target3.SELL_ST_DT` is fed by `o_SELL_ST_DT` instead. Wiring the source column here (the obvious name match) would fill the column with real dates and fail parity on all four rows. |

## Deliberately unconverted ports (dead-port list)

Taken from the "Dead ports (no outgoing `CONNECTOR`)" section of `docs/lineage/informatica_field_lineage.md`.

| Mapping | Transformation | Port / element | Informatica code (verbatim) | XML line | PySpark conversion (snippet or `file:lines`) | Confidence | Reason (required unless HIGH) |
|---|---|---|---|---:|---|---|---|
| m_demo_mapping1 | rtr_TRANS | `demo_target6_GRP` dead ports: `BAL_AMT1`, `ACCT_TYP1`, `LAST_NM1`, `FIRST_NM1`, `CRDT_SCORE1` | *(`PORTTYPE = "OUTPUT"`, `GROUP = "demo_target6_GRP"`)* | 687, 693, 695, 701, 702 | not converted | NOT MIGRATED | The `SB` branch feeds `demo_target6`, which has no `BAL_AMT`, `FIRST_NM` or `CRDT_SCORE` column; `ACCT_TYP1`/`LAST_NM1` are superseded by `o_acc_trim1` and by `demo_target6` not having a `LAST_NM` column. None has an outgoing `CONNECTOR`. |
| m_demo_mapping1 | rtr_TRANS | `demo_target5_GRP` dead ports: `o_ACCT_ID2`, `o_acc_trim2`, `TX_DTTM2`, `TX_ID2`, `ACCT_TYP2`, `TX_AMT2`, `CLSR_DT2`, `ACCT_STAT_CD2`, `o_ACCT_DESC2`, `CR8_DT2`, `o_crdt_trim2` | *(`PORTTYPE = "OUTPUT"`, `GROUP = "demo_target5_GRP"`)* | 705–710, 712–716 | not converted | NOT MIGRATED | `demo_target5` has only five columns (`ACCT_ID`, `FIRST_NM`, `LAST_NM`, `BAL_AMT`, `CRDT_SCORE`), fed by `ACCT_ID2`, `FIRST_NM2`, `LAST_NM2`, `BAL_AMT2`, `CRDT_SCORE2`. The eleven ports listed here carry the account-level attributes the non-`SB` branch never writes; `LAST_NM2` (L711) sits inside the same block but is live, which is why the line range skips it. |
| m_demo_mapping1 | rtr_TRANS | `DEFAULT1` dead ports: `BAL_AMT3`, `ACCT_ID3`, `o_ACCT_ID3`, `o_acc_trim3`, `TX_DTTM3`, `TX_ID3`, `ACCT_TYP3`, `TX_AMT3`, `LAST_NM3`, `CLSR_DT3`, `ACCT_STAT_CD3`, `o_ACCT_DESC3`, `CR8_DT3`, `o_crdt_trim3`, `FIRST_NM3`, `CRDT_SCORE3` | *(`PORTTYPE = "OUTPUT"`, `GROUP = "DEFAULT1"`)* | 719–734 | not converted | NOT MIGRATED | The entire default group is unconnected — this is DEF-4. Note `FIRST_NM3` / `CRDT_SCORE3` / `LAST_NM3` share names with live `demo_target5_GRP` ports, so a name-matched conversion would wire the discarded-row group to `demo_target5`. |
| m_demo_mapping1 | sq_demo_source4 | `TX_TYPE_CD` (SQ port) | *(`PORTTYPE = "INPUT/OUTPUT"`, no `EXPRESSION`; fed by select item 14)* | 579 | not converted | NOT MIGRATED | DEF-1b, see the SQL override section. |
| m_demo_mapping1 | SEQ_GEN | `CURRVAL` | *(see above)* | 431 | not converted | NOT MIGRATED | Repeated here for completeness of the dead-port list. |
