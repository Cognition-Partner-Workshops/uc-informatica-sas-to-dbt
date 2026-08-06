# Informatica transformation-expression inventory and confidence report

Ground truth: `legacy/informatica/wf_demo_mapping.XML` (1594 lines), parsed programmatically with Python expat. This report changes documentation only; no model SQL, legacy artifact, comparator, baseline, published parity, or published evidence file was changed.

## 1. Headline counts

| Measure | Count |
|---|---:|
| `TRANSFORMFIELD` expressions with non-empty `EXPRESSION` | **89** |
| Migrated `TRANSFORMFIELD` expressions | **86** |
| Deliberately omitted `TRANSFORMFIELD` expressions | **3** |
| Additional requested control items (SQL overrides, lookup conditions, router conditions, aggregator GROUP BY/aggregate, sequence values) | **16** |
| Total inventory rows in the full table | **105** |
| Migrated inventory rows | **102** |
| NOT MIGRATED — deliberate inventory rows | **3** |

Confidence split below is over all 105 inventory rows; the three deliberate omissions are not scored as recovered logic.

| Confidence | Count | Share of inventory |
|---|---:|---:|
| HIGH | 69 | 65.7% |
| MEDIUM | 13 | 12.4% |
| LOW | 20 | 19.0% |
| NOT MIGRATED | 3 | 2.9% |

Expression counts by mapping (the 89 expression rows only):

| Mapping | Expressions | Additional control rows | Total inventory rows |
|---|---:|---:|---:|
| `m_demo_mapping1` | 54 | 8 | 62 |
| `m_demo_mapping2` | 20 | 5 | 25 |
| `m_demo_mapping3` | 15 | 3 | 18 |

## 2. Review these first

Every LOW item precedes MEDIUM items. XML lines are direct references for manual review.

1. **LOW — `m_demo_mapping2` / `EXPTRANS.MD5_src` (XML line 177)** — AES_DECRYPT plaintext is unrecoverable; a wrong sentinel/decryption choice would alter match/update classification, and current controls only prove seven final target values. Read `AES_DECRYPT(LEAD_CO_MNE1, SUBSTR(SHORT_NAME,1,3), 256)`; lands in `int_m2__exptrans.MD5_src`.
2. **LOW — `m_demo_mapping2` / `EXPTRANS.MD5_tgt` (XML line 178)** — NULL-concat portability is a judgement call; a wrong NULL treatment would change MD5_tgt/Changed_Flag, but current seeds contain no NULL in these five source ports. Read `MD5(LEAD_CO_MNE || BRANCH_CO_MNE || MIS_DATE || DESCRIPTION || SHORT_NAME)`; lands in `int_m2__exptrans.MD5_tgt`.
3. **LOW — `m_demo_mapping2` / `LKPTRANS.Lookup condition` (XML line 286)** — Lookup policy/row winner depends on warehouse ordering; a wrong winner changes lookup-derived fields, while duplicate-key fixtures provide only one expected final winner. Read `ID = ID1`; lands in `stg_demo_target1 / int_m2__exptrans join`.
4. **LOW — `m_demo_mapping2` / `SEQTRANS.Start Value` (XML line 317)** — Sequence state is recovered but row assignment order is a portability decision; a wrong ordering changes keys, and current parity only checks the deterministic seeded rows. Read `0`; lands in `int_m2__rtr_insert.Key / demo_target1_INS.Key`.
5. **LOW — `m_demo_mapping2` / `SEQTRANS.Current Value` (XML line 320)** — Sequence state is recovered but row assignment order is a portability decision; a wrong ordering changes keys, and current parity only checks the deterministic seeded rows. Read `57`; lands in `int_m2__rtr_insert.Key / demo_target1_INS.Key`.
6. **LOW — `m_demo_mapping1` / `SEQ_GEN.Start Value` (XML line 432)** — Sequence state is recovered but row assignment order is a portability decision; a wrong ordering changes keys, and current parity only checks the deterministic seeded rows. Read `1`; lands in `demo_target6.ACCT_KEY`.
7. **LOW — `m_demo_mapping1` / `SEQ_GEN.Current Value` (XML line 435)** — Sequence state is recovered but row assignment order is a portability decision; a wrong ordering changes keys, and current parity only checks the deterministic seeded rows. Read `281`; lands in `demo_target6.ACCT_KEY`.
8. **LOW — `m_demo_mapping1` / `agg_TRANS.o_ACCT_DESC` (XML line 443)** — Aggregator LAST-row pass-through is inferred with a TX_ID tie-break; a wrong tie-break changes non-aggregate columns, and current data has no tied TX_ID within an account. Read `o_ACCT_DESC`; lands in `int_m1__agg_TRANS.o_ACCT_DESC / demo_target6.ACCT_DESC`.
9. **LOW — `m_demo_mapping1` / `agg_TRANS.o_crdt_trim` (XML line 445)** — Aggregator LAST-row pass-through is inferred with a TX_ID tie-break; a wrong tie-break changes non-aggregate columns, and current data has no tied TX_ID within an account. Read `o_crdt_trim`; lands in `int_m1__agg_TRANS.o_crdt_trim / demo_target6.CRDT_LN`.
10. **LOW — `m_demo_mapping1` / `agg_TRANS.CLSR_DT` (XML line 446)** — Aggregator LAST-row pass-through is inferred with a TX_ID tie-break; a wrong tie-break changes non-aggregate columns, and current data has no tied TX_ID within an account. Read `CLSR_DT`; lands in `int_m1__agg_TRANS.CLSR_DT / demo_target6.CLSR_DT`.
11. **LOW — `m_demo_mapping1` / `agg_TRANS.TX_ID` (XML line 447)** — Aggregator LAST-row pass-through is inferred with a TX_ID tie-break; a wrong tie-break changes non-aggregate columns, and current data has no tied TX_ID within an account. Read `TX_ID`; lands in `int_m1__agg_TRANS.TX_ID / demo_target6.TX_ID`.
12. **LOW — `m_demo_mapping1` / `agg_TRANS.ACCT_STAT_CD` (XML line 448)** — Aggregator LAST-row pass-through is inferred with a TX_ID tie-break; a wrong tie-break changes non-aggregate columns, and current data has no tied TX_ID within an account. Read `ACCT_STAT_CD`; lands in `int_m1__agg_TRANS.ACCT_STAT_CD / demo_target6.ACCT_STAT_CD`.
13. **LOW — `m_demo_mapping1` / `agg_TRANS.TX_DTTM` (XML line 449)** — Aggregator LAST-row pass-through is inferred with a TX_ID tie-break; a wrong tie-break changes non-aggregate columns, and current data has no tied TX_ID within an account. Read `TX_DTTM`; lands in `int_m1__agg_TRANS.TX_DTTM / demo_target6.TX_DTTM`.
14. **LOW — `m_demo_mapping1` / `agg_TRANS.CR8_DT` (XML line 450)** — Aggregator LAST-row pass-through is inferred with a TX_ID tie-break; a wrong tie-break changes non-aggregate columns, and current data has no tied TX_ID within an account. Read `CR8_DT`; lands in `int_m1__agg_TRANS.CR8_DT / demo_target6.CR8_DT`.
15. **LOW — `m_demo_mapping1` / `agg_TRANS.o_ACCT_ID` (XML line 451)** — Aggregator LAST-row pass-through is inferred with a TX_ID tie-break; a wrong tie-break changes non-aggregate columns, and current data has no tied TX_ID within an account. Read `o_ACCT_ID`; lands in `int_m1__agg_TRANS.o_ACCT_ID / demo_target6.TX_TYPE_CD`.
16. **LOW — `m_demo_mapping1` / `agg_TRANS.ACCT_ID` (XML line 452)** — Aggregator LAST-row pass-through is inferred with a TX_ID tie-break; a wrong tie-break changes non-aggregate columns, and current data has no tied TX_ID within an account. Read `ACCT_ID`; lands in `int_m1__agg_TRANS.ACCT_ID / demo_target6.ACCT_ID`.
17. **LOW — `m_demo_mapping1` / `agg_TRANS.o_acc_trim` (XML line 453)** — Aggregator LAST-row pass-through is inferred with a TX_ID tie-break; a wrong tie-break changes non-aggregate columns, and current data has no tied TX_ID within an account. Read `o_acc_trim`; lands in `int_m1__agg_TRANS.o_acc_trim / demo_target6.ACCT_TYP`.
18. **LOW — `m_demo_mapping1` / `lkp_TRANS2.Lookup condition` (XML line 499)** — Lookup policy/row winner depends on warehouse ordering; a wrong winner changes lookup-derived fields, while duplicate-key fixtures provide only one expected final winner. Read `ACCT_ID = IN_ACCT_ID`; lands in `stg_lkp_demo_source1 / int_m1__exp_TRANS1.FIRST_NM`.

The densest transformation instances by expression count are listed in the volume section; they are useful review starting points, but volume is not risk.

## 3. Full inventory

`Outgoing` is based on a matching `CONNECTOR` whose `FROMINSTANCE` and `FROMFIELD` equal the transformation and port. “Target reaches” is represented by the dbt landing column or row-set model; a dead port is explicitly NOT MIGRATED.

| # | Mapping | Transformation | Port / attribute | Port type | Outgoing | XML expression (verbatim; long SQL truncated) | XML line | Kind | dbt model.column / deliberate reason | Confidence | Reason / control weakness |
|---:|---|---|---|---|:---:|---|---:|---|---|---|---|
| 1 | `m_demo_mapping2` | `EXPTRANS` | `LEAD_CO_MNE` | `INPUT/OUTPUT` | yes | `LEAD_CO_MNE` | 164 | pass-through/rename | int_m2__exptrans.LEAD_CO_MNE | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 2 | `m_demo_mapping2` | `EXPTRANS` | `BRANCH_CO_MNE` | `INPUT/OUTPUT` | yes | `BRANCH_CO_MNE` | 165 | pass-through/rename | int_m2__exptrans.BRANCH_CO_MNE | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 3 | `m_demo_mapping2` | `EXPTRANS` | `MIS_DATE` | `INPUT/OUTPUT` | yes | `MIS_DATE` | 166 | pass-through/rename | int_m2__exptrans.MIS_DATE | **MEDIUM** | Every baseline output value is constant or NULL; a wrong implementation producing the same degenerate value would pass parity. |
| 4 | `m_demo_mapping2` | `EXPTRANS` | `ID` | `INPUT/OUTPUT` | yes | `ID` | 167 | pass-through/rename | int_m2__exptrans.ID | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 5 | `m_demo_mapping2` | `EXPTRANS` | `DESCRIPTION` | `INPUT/OUTPUT` | yes | `DESCRIPTION` | 168 | pass-through/rename | int_m2__exptrans.DESCRIPTION | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 6 | `m_demo_mapping2` | `EXPTRANS` | `SHORT_NAME` | `INPUT/OUTPUT` | yes | `SHORT_NAME` | 169 | pass-through/rename | int_m2__exptrans.SHORT_NAME | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 7 | `m_demo_mapping2` | `EXPTRANS` | `Key` | `INPUT/OUTPUT` | yes | `Key` | 170 | pass-through/rename | int_m2__exptrans.Key | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 8 | `m_demo_mapping2` | `EXPTRANS` | `LEAD_CO_MNE1` | `INPUT/OUTPUT` | yes | `LEAD_CO_MNE1` | 171 | pass-through/rename | int_m2__exptrans.LEAD_CO_MNE1 | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 9 | `m_demo_mapping2` | `EXPTRANS` | `BRANCH_CO_MNE1` | `INPUT/OUTPUT` | yes | `BRANCH_CO_MNE1` | 172 | pass-through/rename | int_m2__exptrans.BRANCH_CO_MNE1 | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 10 | `m_demo_mapping2` | `EXPTRANS` | `MIS_DATE1` | `INPUT/OUTPUT` | yes | `MIS_DATE1` | 173 | pass-through/rename | int_m2__exptrans.MIS_DATE1 | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 11 | `m_demo_mapping2` | `EXPTRANS` | `DESCRIPTION1` | `INPUT/OUTPUT` | yes | `DESCRIPTION1` | 174 | pass-through/rename | int_m2__exptrans.DESCRIPTION1 | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 12 | `m_demo_mapping2` | `EXPTRANS` | `SHORT_NAME1` | `INPUT/OUTPUT` | yes | `SHORT_NAME1` | 175 | pass-through/rename | int_m2__exptrans.SHORT_NAME1 | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 13 | `m_demo_mapping2` | `EXPTRANS` | `New_Flag` | `OUTPUT` | yes | `IIF(ISNULL(Key),'Insert')` | 176 | conditional IIF/DECODE | int_m2__exptrans.New_Flag | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 14 | `m_demo_mapping2` | `EXPTRANS` | `MD5_src` | `LOCAL VARIABLE` | no | `AES_DECRYPT(LEAD_CO_MNE1, SUBSTR(SHORT_NAME,1,3), 256)` | 177 | hash/crypto | int_m2__exptrans.MD5_src | **LOW** | AES_DECRYPT plaintext is unrecoverable; a wrong sentinel/decryption choice would alter match/update classification, and current controls only prove seven final target values. |
| 15 | `m_demo_mapping2` | `EXPTRANS` | `MD5_tgt` | `LOCAL VARIABLE` | no | `MD5(LEAD_CO_MNE \|\| BRANCH_CO_MNE \|\| MIS_DATE \|\| DESCRIPTION \|\| SHORT_NAME)` | 178 | hash/crypto | int_m2__exptrans.MD5_tgt | **LOW** | NULL-concat portability is a judgement call; a wrong NULL treatment would change MD5_tgt/Changed_Flag, but current seeds contain no NULL in these five source ports. |
| 16 | `m_demo_mapping2` | `EXPTRANS` | `Changed_Flag` | `OUTPUT` | yes | `IIF(NOT ISNULL(Key) AND (MD5_tgt != MD5_src),'Update')` | 179 | conditional IIF/DECODE | int_m2__exptrans.Changed_Flag | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 17 | `m_demo_mapping2` | `EXPTRANS` | `o_CREATED_BY` | `OUTPUT` | yes | `'IDWUSER'` | 180 | literal | int_m2__exptrans.o_CREATED_BY | **MEDIUM** | Every baseline output value is constant or NULL; a wrong implementation producing the same degenerate value would pass parity. |
| 18 | `m_demo_mapping2` | `EXPTRANS` | `o_CREATED_TIME` | `OUTPUT` | yes | `SYSDATE` | 181 | date | int_m2__exptrans.o_CREATED_TIME | **MEDIUM** | Every baseline output value is constant or NULL; a wrong implementation producing the same degenerate value would pass parity. |
| 19 | `m_demo_mapping2` | `EXPTRANS` | `o_UPDATED_BY` | `OUTPUT` | yes | `'IDWUSER'` | 182 | literal | int_m2__exptrans.o_UPDATED_BY | **MEDIUM** | Every baseline output value is constant or NULL; a wrong implementation producing the same degenerate value would pass parity. |
| 20 | `m_demo_mapping2` | `EXPTRANS` | `o_UPDATED_TIME` | `OUTPUT` | yes | `SYSDATE` | 183 | date | int_m2__exptrans.o_UPDATED_TIME | **MEDIUM** | Every baseline output value is constant or NULL; a wrong implementation producing the same degenerate value would pass parity. |
| 21 | `m_demo_mapping2` | `RTRTRANS` | `Insert` | `GROUP` | — | `New_Flag='Insert'` | 188 | router condition | None | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 22 | `m_demo_mapping2` | `RTRTRANS` | `Update` | `GROUP` | — | `Changed_Flag='Update'` | 190 | router condition | None | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 23 | `m_demo_mapping2` | `LKPTRANS` | `Lookup condition` | `ATTRIBUTE` | — | `ID = ID1` | 286 | lookup call | stg_demo_target1 / int_m2__exptrans join | **LOW** | Lookup policy/row winner depends on warehouse ordering; a wrong winner changes lookup-derived fields, while duplicate-key fixtures provide only one expected final winner. |
| 24 | `m_demo_mapping2` | `SEQTRANS` | `Start Value` | `ATTRIBUTE` | — | `0` | 317 | sequence | int_m2__rtr_insert.Key / demo_target1_INS.Key | **LOW** | Sequence state is recovered but row assignment order is a portability decision; a wrong ordering changes keys, and current parity only checks the deterministic seeded rows. |
| 25 | `m_demo_mapping2` | `SEQTRANS` | `Current Value` | `ATTRIBUTE` | — | `57` | 320 | sequence | int_m2__rtr_insert.Key / demo_target1_INS.Key | **LOW** | Sequence state is recovered but row assignment order is a portability decision; a wrong ordering changes keys, and current parity only checks the deterministic seeded rows. |
| 26 | `m_demo_mapping1` | `SEQ_GEN` | `Start Value` | `ATTRIBUTE` | — | `1` | 432 | sequence | demo_target6.ACCT_KEY | **LOW** | Sequence state is recovered but row assignment order is a portability decision; a wrong ordering changes keys, and current parity only checks the deterministic seeded rows. |
| 27 | `m_demo_mapping1` | `SEQ_GEN` | `Current Value` | `ATTRIBUTE` | — | `281` | 435 | sequence | demo_target6.ACCT_KEY | **LOW** | Sequence state is recovered but row assignment order is a portability decision; a wrong ordering changes keys, and current parity only checks the deterministic seeded rows. |
| 28 | `m_demo_mapping1` | `agg_TRANS` | `o_ACCT_DESC` | `INPUT/OUTPUT` | yes | `o_ACCT_DESC` | 443 | pass-through/rename | int_m1__agg_TRANS.o_ACCT_DESC / demo_target6.ACCT_DESC | **LOW** | Aggregator LAST-row pass-through is inferred with a TX_ID tie-break; a wrong tie-break changes non-aggregate columns, and current data has no tied TX_ID within an account. |
| 29 | `m_demo_mapping1` | `agg_TRANS` | `TX_AMT` | `INPUT/OUTPUT` | no | `TX_AMT` | 444 | pass-through/rename | NOT MIGRATED — dead aggregator input port (no outgoing connector) | **NOT MIGRATED** | The XML port has no outgoing CONNECTOR; no target row can observe it, so it is deliberately omitted as a distinct implementation. |
| 30 | `m_demo_mapping1` | `agg_TRANS` | `o_crdt_trim` | `INPUT/OUTPUT` | yes | `o_crdt_trim` | 445 | pass-through/rename | int_m1__agg_TRANS.o_crdt_trim / demo_target6.CRDT_LN | **LOW** | Aggregator LAST-row pass-through is inferred with a TX_ID tie-break; a wrong tie-break changes non-aggregate columns, and current data has no tied TX_ID within an account. |
| 31 | `m_demo_mapping1` | `agg_TRANS` | `CLSR_DT` | `INPUT/OUTPUT` | yes | `CLSR_DT` | 446 | pass-through/rename | int_m1__agg_TRANS.CLSR_DT / demo_target6.CLSR_DT | **LOW** | Aggregator LAST-row pass-through is inferred with a TX_ID tie-break; a wrong tie-break changes non-aggregate columns, and current data has no tied TX_ID within an account. |
| 32 | `m_demo_mapping1` | `agg_TRANS` | `TX_ID` | `INPUT/OUTPUT` | yes | `TX_ID` | 447 | pass-through/rename | int_m1__agg_TRANS.TX_ID / demo_target6.TX_ID | **LOW** | Aggregator LAST-row pass-through is inferred with a TX_ID tie-break; a wrong tie-break changes non-aggregate columns, and current data has no tied TX_ID within an account. |
| 33 | `m_demo_mapping1` | `agg_TRANS` | `ACCT_STAT_CD` | `INPUT/OUTPUT` | yes | `ACCT_STAT_CD` | 448 | pass-through/rename | int_m1__agg_TRANS.ACCT_STAT_CD / demo_target6.ACCT_STAT_CD | **LOW** | Aggregator LAST-row pass-through is inferred with a TX_ID tie-break; a wrong tie-break changes non-aggregate columns, and current data has no tied TX_ID within an account. |
| 34 | `m_demo_mapping1` | `agg_TRANS` | `TX_DTTM` | `INPUT/OUTPUT` | yes | `TX_DTTM` | 449 | pass-through/rename | int_m1__agg_TRANS.TX_DTTM / demo_target6.TX_DTTM | **LOW** | Aggregator LAST-row pass-through is inferred with a TX_ID tie-break; a wrong tie-break changes non-aggregate columns, and current data has no tied TX_ID within an account. |
| 35 | `m_demo_mapping1` | `agg_TRANS` | `CR8_DT` | `INPUT/OUTPUT` | yes | `CR8_DT` | 450 | pass-through/rename | int_m1__agg_TRANS.CR8_DT / demo_target6.CR8_DT | **LOW** | Aggregator LAST-row pass-through is inferred with a TX_ID tie-break; a wrong tie-break changes non-aggregate columns, and current data has no tied TX_ID within an account. |
| 36 | `m_demo_mapping1` | `agg_TRANS` | `o_ACCT_ID` | `INPUT/OUTPUT` | yes | `o_ACCT_ID` | 451 | pass-through/rename | int_m1__agg_TRANS.o_ACCT_ID / demo_target6.TX_TYPE_CD | **LOW** | Aggregator LAST-row pass-through is inferred with a TX_ID tie-break; a wrong tie-break changes non-aggregate columns, and current data has no tied TX_ID within an account. |
| 37 | `m_demo_mapping1` | `agg_TRANS` | `ACCT_ID` | `INPUT/OUTPUT` | yes | `ACCT_ID` | 452 | aggregate | int_m1__agg_TRANS.ACCT_ID / demo_target6.ACCT_ID | **LOW** | Aggregator LAST-row pass-through is inferred with a TX_ID tie-break; a wrong tie-break changes non-aggregate columns, and current data has no tied TX_ID within an account. |
| 38 | `m_demo_mapping1` | `agg_TRANS` | `o_acc_trim` | `INPUT/OUTPUT` | yes | `o_acc_trim` | 453 | pass-through/rename | int_m1__agg_TRANS.o_acc_trim / demo_target6.ACCT_TYP | **LOW** | Aggregator LAST-row pass-through is inferred with a TX_ID tie-break; a wrong tie-break changes non-aggregate columns, and current data has no tied TX_ID within an account. |
| 39 | `m_demo_mapping1` | `agg_TRANS` | `o_TX_AMT` | `OUTPUT` | yes | `SUM(TX_AMT)` | 454 | aggregate | int_m1__agg_TRANS.o_TX_AMT / demo_target6.TX_AMT | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 40 | `m_demo_mapping1` | `exp_TRANS1` | `FIRST_NM` | `INPUT/OUTPUT` | yes | `FIRST_NM` | 463 | pass-through/rename | int_m1__exp_TRANS1.FIRST_NM | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 41 | `m_demo_mapping1` | `exp_TRANS1` | `CLSR_DT` | `INPUT/OUTPUT` | yes | `CLSR_DT` | 464 | pass-through/rename | int_m1__exp_TRANS1.CLSR_DT | **MEDIUM** | Every baseline output value is constant or NULL; a wrong implementation producing the same degenerate value would pass parity. |
| 42 | `m_demo_mapping1` | `exp_TRANS1` | `TX_DTTM` | `INPUT/OUTPUT` | yes | `TX_DTTM` | 465 | pass-through/rename | int_m1__exp_TRANS1.TX_DTTM | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 43 | `m_demo_mapping1` | `exp_TRANS1` | `BAL_AMT` | `INPUT/OUTPUT` | yes | `BAL_AMT` | 466 | pass-through/rename | int_m1__exp_TRANS1.BAL_AMT | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 44 | `m_demo_mapping1` | `exp_TRANS1` | `ACCT_DESC` | `INPUT/OUTPUT` | no | `ACCT_DESC` | 467 | pass-through/rename | NOT MIGRATED — dead expression port (no outgoing connector) | **NOT MIGRATED** | The XML port has no outgoing CONNECTOR; no target row can observe it, so it is deliberately omitted as a distinct implementation. |
| 45 | `m_demo_mapping1` | `exp_TRANS1` | `ACCT_TYP` | `INPUT/OUTPUT` | yes | `ACCT_TYP` | 468 | pass-through/rename | int_m1__exp_TRANS1.ACCT_TYP | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 46 | `m_demo_mapping1` | `exp_TRANS1` | `ACCT_STAT_CD` | `INPUT/OUTPUT` | yes | `ACCT_STAT_CD` | 469 | pass-through/rename | int_m1__exp_TRANS1.ACCT_STAT_CD | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 47 | `m_demo_mapping1` | `exp_TRANS1` | `TX_ID` | `INPUT/OUTPUT` | yes | `TX_ID` | 470 | pass-through/rename | int_m1__exp_TRANS1.TX_ID | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 48 | `m_demo_mapping1` | `exp_TRANS1` | `LAST_NM` | `INPUT/OUTPUT` | yes | `LAST_NM` | 471 | pass-through/rename | int_m1__exp_TRANS1.LAST_NM | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 49 | `m_demo_mapping1` | `exp_TRANS1` | `TX_AMT` | `INPUT/OUTPUT` | yes | `TX_AMT` | 472 | pass-through/rename | int_m1__exp_TRANS1.TX_AMT | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 50 | `m_demo_mapping1` | `exp_TRANS1` | `ACCT_ID` | `INPUT/OUTPUT` | yes | `ACCT_ID` | 473 | pass-through/rename | int_m1__exp_TRANS1.ACCT_ID | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 51 | `m_demo_mapping1` | `exp_TRANS1` | `CR8_DT` | `INPUT/OUTPUT` | yes | `CR8_DT` | 474 | pass-through/rename | int_m1__exp_TRANS1.CR8_DT | **MEDIUM** | Every baseline output value is constant or NULL; a wrong implementation producing the same degenerate value would pass parity. |
| 52 | `m_demo_mapping1` | `exp_TRANS1` | `o_acc_trim` | `INPUT/OUTPUT` | yes | `o_acc_trim` | 475 | pass-through/rename | int_m1__exp_TRANS1.o_acc_trim | **MEDIUM** | Every baseline output value is constant or NULL; a wrong implementation producing the same degenerate value would pass parity. |
| 53 | `m_demo_mapping1` | `exp_TRANS1` | `o_crdt_trim` | `INPUT/OUTPUT` | yes | `o_crdt_trim` | 476 | pass-through/rename | int_m1__exp_TRANS1.o_crdt_trim | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 54 | `m_demo_mapping1` | `exp_TRANS1` | `o_ACCT_ID` | `INPUT/OUTPUT` | yes | `o_ACCT_ID` | 477 | pass-through/rename | int_m1__exp_TRANS1.o_ACCT_ID | **MEDIUM** | Every baseline output value is constant or NULL; a wrong implementation producing the same degenerate value would pass parity. |
| 55 | `m_demo_mapping1` | `exp_TRANS1` | `CRDT_SCORE` | `INPUT/OUTPUT` | yes | `CRDT_SCORE` | 478 | pass-through/rename | int_m1__exp_TRANS1.CRDT_SCORE | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 56 | `m_demo_mapping1` | `exp_TRANS1` | `o_ACCT_DESC` | `OUTPUT` | yes | `RTRIM(ACCT_DESC)` | 479 | string | int_m1__exp_TRANS1.o_ACCT_DESC | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 57 | `m_demo_mapping1` | `lkp_TRANS2` | `IN_ACCT_ID` | `INPUT/OUTPUT` | no | `IN_ACCT_ID` | 483 | pass-through/rename | UNMAPPED | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 58 | `m_demo_mapping1` | `lkp_TRANS2` | `Lookup condition` | `ATTRIBUTE` | — | `ACCT_ID = IN_ACCT_ID` | 499 | lookup call | stg_lkp_demo_source1 / int_m1__exp_TRANS1.FIRST_NM | **LOW** | Lookup policy/row winner depends on warehouse ordering; a wrong winner changes lookup-derived fields, while duplicate-key fixtures provide only one expected final winner. |
| 59 | `m_demo_mapping1` | `lkp_TRANS1` | `Lookup condition` | `ATTRIBUTE` | — | `ACCT_ID = IN_ACCT_ID` | 537 | lookup call | stg_lkp_demo_source3 / int_m1__exp_TRANS.o_ACCT_ID | **LOW** | Lookup policy/row winner depends on warehouse ordering; a wrong winner changes lookup-derived fields, while duplicate-key fixtures provide only one expected final winner. |
| 60 | `m_demo_mapping1` | `sq_demo_source4` | `Sql Query` | `ATTRIBUTE` | — | `SELECT demo_source4.ACCT_ID, demo_source4.ACCT_TYP, demo_source4.ACCT_DESC, demo_source4.CRDT_LN, SYSTIMESTAMP, demo_source4.CLSR_DT, demo_source4.ACCT_STAT_CD, demo_source3.TX_ID…` | 580 | pass-through/rename | int_m1__sq_demo_source4 (joined source rowset) | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 61 | `m_demo_mapping1` | `exp_TRANS` | `CLSR_DT` | `INPUT/OUTPUT` | yes | `CLSR_DT` | 594 | pass-through/rename | int_m1__exp_TRANS.CLSR_DT | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 62 | `m_demo_mapping1` | `exp_TRANS` | `TX_DTTM` | `INPUT/OUTPUT` | yes | `TX_DTTM` | 595 | pass-through/rename | int_m1__exp_TRANS.TX_DTTM | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 63 | `m_demo_mapping1` | `exp_TRANS` | `BAL_AMT` | `INPUT/OUTPUT` | yes | `BAL_AMT` | 596 | pass-through/rename | int_m1__exp_TRANS.BAL_AMT | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 64 | `m_demo_mapping1` | `exp_TRANS` | `ACCT_DESC` | `INPUT/OUTPUT` | yes | `ACCT_DESC` | 597 | pass-through/rename | int_m1__exp_TRANS.ACCT_DESC | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 65 | `m_demo_mapping1` | `exp_TRANS` | `ACCT_TYP` | `INPUT/OUTPUT` | yes | `ACCT_TYP` | 598 | pass-through/rename | int_m1__exp_TRANS.ACCT_TYP | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 66 | `m_demo_mapping1` | `exp_TRANS` | `ACCT_STAT_CD` | `INPUT/OUTPUT` | yes | `ACCT_STAT_CD` | 599 | pass-through/rename | int_m1__exp_TRANS.ACCT_STAT_CD | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 67 | `m_demo_mapping1` | `exp_TRANS` | `TX_ID` | `INPUT/OUTPUT` | yes | `TX_ID` | 600 | pass-through/rename | int_m1__exp_TRANS.TX_ID | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 68 | `m_demo_mapping1` | `exp_TRANS` | `LAST_NM` | `INPUT/OUTPUT` | yes | `LAST_NM` | 601 | pass-through/rename | int_m1__exp_TRANS.LAST_NM | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 69 | `m_demo_mapping1` | `exp_TRANS` | `TX_AMT` | `INPUT/OUTPUT` | yes | `TX_AMT` | 602 | pass-through/rename | int_m1__exp_TRANS.TX_AMT | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 70 | `m_demo_mapping1` | `exp_TRANS` | `ACCT_ID` | `INPUT/OUTPUT` | yes | `ACCT_ID` | 603 | pass-through/rename | int_m1__exp_TRANS.ACCT_ID | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 71 | `m_demo_mapping1` | `exp_TRANS` | `CR8_DT` | `INPUT/OUTPUT` | yes | `CR8_DT` | 604 | pass-through/rename | int_m1__exp_TRANS.CR8_DT | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 72 | `m_demo_mapping1` | `exp_TRANS` | `CUST_ID` | `INPUT/OUTPUT` | yes | `CUST_ID` | 605 | pass-through/rename | int_m1__exp_TRANS.CUST_ID | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 73 | `m_demo_mapping1` | `exp_TRANS` | `o_acc_trim` | `OUTPUT` | yes | `RTRIM(ACCT_TYP)` | 606 | string | int_m1__exp_TRANS.o_acc_trim | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 74 | `m_demo_mapping1` | `exp_TRANS` | `o_crdt_trim` | `OUTPUT` | yes | `LTRIM(CRDT_LN)` | 607 | string | int_m1__exp_TRANS.o_crdt_trim | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 75 | `m_demo_mapping1` | `exp_TRANS` | `o_ACCT_ID` | `OUTPUT` | yes | `:LKP.lkp_TRANS1(ACCT_ID)` | 608 | lookup call | int_m1__exp_TRANS.o_ACCT_ID | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 76 | `m_demo_mapping1` | `lkp_TRANS3` | `IN_CUST_ID` | `INPUT/OUTPUT` | no | `IN_CUST_ID` | 612 | pass-through/rename | UNMAPPED | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 77 | `m_demo_mapping1` | `lkp_TRANS3` | `Lookup condition` | `ATTRIBUTE` | — | `CUST_ID = IN_CUST_ID` | 625 | lookup call | stg_lkp_demo_source2 / int_m1__exp_TRANS1.CRDT_SCORE | **LOW** | Lookup policy/row winner depends on warehouse ordering; a wrong winner changes lookup-derived fields, while duplicate-key fixtures provide only one expected final winner. |
| 78 | `m_demo_mapping1` | `exp_TRANS2` | `PRODUCT_NO` | `INPUT/OUTPUT` | yes | `PRODUCT_NO` | 654 | pass-through/rename | int_m1__exp_TRANS2.PRODUCT_NO / demo_target3.PRODUCT_NO | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 79 | `m_demo_mapping1` | `exp_TRANS2` | `STD_COST` | `INPUT/OUTPUT` | yes | `STD_COST` | 655 | pass-through/rename | int_m1__exp_TRANS2.STD_COST / demo_target3.STD_COST | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 80 | `m_demo_mapping1` | `exp_TRANS2` | `COLOR` | `INPUT/OUTPUT` | yes | `COLOR` | 656 | pass-through/rename | int_m1__exp_TRANS2.COLOR / demo_target3.COLOR | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 81 | `m_demo_mapping1` | `exp_TRANS2` | `PRODUCT_ID` | `INPUT/OUTPUT` | yes | `PRODUCT_ID` | 659 | pass-through/rename | int_m1__exp_TRANS2.PRODUCT_ID / demo_target3.PRODUCT_ID | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 82 | `m_demo_mapping1` | `exp_TRANS2` | `PRODUCT_NM` | `INPUT/OUTPUT` | yes | `PRODUCT_NM` | 660 | pass-through/rename | int_m1__exp_TRANS2.PRODUCT_NM / demo_target3.PRODUCT_NM | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 83 | `m_demo_mapping1` | `exp_TRANS2` | `LIST_PRICE` | `INPUT/OUTPUT` | yes | `LIST_PRICE` | 661 | pass-through/rename | int_m1__exp_TRANS2.LIST_PRICE / demo_target3.LIST_PRICE | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 84 | `m_demo_mapping1` | `exp_TRANS2` | `o_SELL_ST_DT` | `OUTPUT` | yes | `TO_DATE(TO_CHAR(SYSDATE),'DD/MM/YYYY')` | 662 | date | int_m1__exp_TRANS2.o_SELL_ST_DT / demo_target3.SELL_ST_DT | **MEDIUM** | Every baseline output value is constant or NULL; a wrong implementation producing the same degenerate value would pass parity. |
| 85 | `m_demo_mapping1` | `exp_TRANS2` | `o_SELL_ED_DT` | `OUTPUT` | yes | `TO_DATE(SELL_ED_DT,'DD/MM/YYYY')` | 663 | date | int_m1__exp_TRANS2.o_SELL_ED_DT / demo_target3.SELL_ED_DT | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 86 | `m_demo_mapping1` | `rtr_TRANS` | `demo_target6_GRP` | `GROUP` | — | `ACCT_TYP = 'SB'` | 668 | router condition | None | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 87 | `m_demo_mapping1` | `rtr_TRANS` | `demo_target5_GRP` | `GROUP` | — | `ACCT_TYP != 'SB'` | 669 | router condition | None | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 88 | `m_demo_mapping3` | `SQ_demo_source2` | `Sql Query` | `ATTRIBUTE` | — | `SELECT demo_source2.Title, demo_source2.First_Name, demo_source2.Middle_Name, demo_source2.Last_Name, demo_source2.Member_ID, demo_source2.Member_Suffix, demo_source2.Birth_Date, …` | 916 | pass-through/rename | int_m3__sq_demo_source2 (filtered source rowset) | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 89 | `m_demo_mapping3` | `EXPTRANS` | `Title` | `INPUT/OUTPUT` | yes | `Title` | 929 | pass-through/rename | int_m3__exptrans.Title | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 90 | `m_demo_mapping3` | `EXPTRANS` | `First_Name` | `INPUT/OUTPUT` | yes | `First_Name` | 930 | pass-through/rename | int_m3__exptrans.First_Name | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 91 | `m_demo_mapping3` | `EXPTRANS` | `Middle_Name` | `INPUT/OUTPUT` | yes | `Middle_Name` | 931 | pass-through/rename | int_m3__exptrans.Middle_Name | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 92 | `m_demo_mapping3` | `EXPTRANS` | `Last_Name` | `INPUT/OUTPUT` | yes | `Last_Name` | 932 | pass-through/rename | int_m3__exptrans.Last_Name | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 93 | `m_demo_mapping3` | `EXPTRANS` | `Member_ID` | `INPUT/OUTPUT` | yes | `Member_ID` | 933 | pass-through/rename | int_m3__exptrans.Member_ID | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 94 | `m_demo_mapping3` | `EXPTRANS` | `Member_Suffix` | `INPUT/OUTPUT` | yes | `Member_Suffix` | 934 | pass-through/rename | int_m3__exptrans.Member_Suffix | **MEDIUM** | Every baseline output value is constant or NULL; a wrong implementation producing the same degenerate value would pass parity. |
| 95 | `m_demo_mapping3` | `EXPTRANS` | `Birth_Date` | `INPUT/OUTPUT` | yes | `Birth_Date` | 935 | pass-through/rename | int_m3__exptrans.Birth_Date | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 96 | `m_demo_mapping3` | `EXPTRANS` | `Gender_Code` | `INPUT/OUTPUT` | yes | `Gender_Code` | 936 | pass-through/rename | int_m3__exptrans.Gender_Code | **MEDIUM** | Every baseline output value is constant or NULL; a wrong implementation producing the same degenerate value would pass parity. |
| 97 | `m_demo_mapping3` | `EXPTRANS` | `Member_Record_Number` | `INPUT/OUTPUT` | yes | `Member_Record_Number` | 937 | pass-through/rename | int_m3__exptrans.Member_Record_Number | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 98 | `m_demo_mapping3` | `EXPTRANS` | `Social_Security_Number` | `INPUT/OUTPUT` | yes | `Social_Security_Number` | 938 | pass-through/rename | int_m3__exptrans.Social_Security_Number | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 99 | `m_demo_mapping3` | `EXPTRANS` | `Member_Type_Code` | `INPUT/OUTPUT` | yes | `Member_Type_Code` | 939 | pass-through/rename | int_m3__exptrans.Member_Type_Code | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 100 | `m_demo_mapping3` | `EXPTRANS` | `Original_Effective_Date` | `INPUT/OUTPUT` | yes | `Original_Effective_Date` | 940 | pass-through/rename | int_m3__exptrans.Original_Effective_Date | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 101 | `m_demo_mapping3` | `EXPTRANS` | `Relationship_to_Subscriber_Code` | `INPUT/OUTPUT` | yes | `Relationship_to_Subscriber_Code` | 941 | pass-through/rename | int_m3__exptrans.Relationship_to_Subscriber_Code | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 102 | `m_demo_mapping3` | `EXPTRANS` | `Relationship_to_Subscriber_Code_Label` | `INPUT/OUTPUT` | no | `Relationship_to_Subscriber_Code_Label` | 942 | pass-through/rename | NOT MIGRATED — dead expression port (no outgoing connector) | **NOT MIGRATED** | The XML port has no outgoing CONNECTOR; no target row can observe it, so it is deliberately omitted as a distinct implementation. |
| 103 | `m_demo_mapping3` | `EXPTRANS` | `o_Relationship_to_Subscriber_Code_Label` | `OUTPUT` | yes | `iif(ISNULL(Relationship_to_Subscriber_Code_Label),ABORT('Relationship_to_Subscriber_Code_Labe valuel is null'),Relationship_to_Subscriber_Code_Label)` | 943 | ABORT | int_m3__exptrans.o_Relationship_to_Subscriber_Code_Label | **MEDIUM** | Only the abort fixture exercises the null branch; a wrong hard-failure implementation would be caught only by that fixture, not the normal-seed parity rows. |
| 104 | `m_demo_mapping3` | `RTRTRANS` | `NEWGROUP1` | `GROUP` | — | `ISNULL(Social_Security_Number)` | 948 | router condition | None | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |
| 105 | `m_demo_mapping3` | `RTRTRANS` | `NEWGROUP2` | `GROUP` | — | `NOT ISNULL(Social_Security_Number)` | 950 | router condition | None | **HIGH** | XML semantics are explicit and baseline output varies across multiple rows, so parity would expose a wrong implementation. |

### Deliberate non-migration set

The three inventory ports with no outgoing connector are: `m_demo_mapping1.agg_TRANS.TX_AMT` (XML 444), `m_demo_mapping1.exp_TRANS1.ACCT_DESC` (XML 467), and `m_demo_mapping3.EXPTRANS.Relationship_to_Subscriber_Code_Label` (XML 942). They cannot affect a target row. In addition, the XML has three router `DEFAULT1` groups with no target connector: `RTRTRANS.DEFAULT1` in mapping2 (XML 189), `rtr_TRANS.DEFAULT1` in mapping1 (XML 670), and `RTRTRANS.DEFAULT1` in mapping3 (XML 949); rows reaching those groups are discarded. Workflow Email and Control tasks have no dbt model counterpart; dbt preserves session dependency/failure semantics, not those operational side effects.

## 4. Per-column baseline cardinality

Classification is data-backed: `rows` is CSV row count, `nonnull` excludes empty CSV fields, and `distinct` counts distinct non-null values. `NON-DEGENERATE` means at least two distinct non-null values; `WEAK` means one distinct value or only one non-null row; `ALL-NULL` means zero non-null values.

| Target | Column | Rows | Non-null | Distinct non-null | Exercise classification |
|---|---|---:|---:|---:|---|
| `demo_target1_INS` | `Key` | 4 | 4 | 4 | NON-DEGENERATE |
| `demo_target1_INS` | `LEAD_CO_MNE` | 4 | 4 | 4 | NON-DEGENERATE |
| `demo_target1_INS` | `BRANCH_CO_MNE` | 4 | 4 | 4 | NON-DEGENERATE |
| `demo_target1_INS` | `MIS_DATE` | 4 | 4 | 1 | WEAK |
| `demo_target1_INS` | `ID` | 4 | 4 | 4 | NON-DEGENERATE |
| `demo_target1_INS` | `DESCRIPTION` | 4 | 4 | 4 | NON-DEGENERATE |
| `demo_target1_INS` | `SHORT_NAME` | 4 | 4 | 4 | NON-DEGENERATE |
| `demo_target1_INS` | `CREATED_BY` | 4 | 4 | 1 | WEAK |
| `demo_target1_INS` | `CREATED_TIME` | 4 | 4 | 1 | WEAK |
| `demo_target1_INS` | `UPDATED_BY` | 4 | 0 | 0 | ALL-NULL |
| `demo_target1_INS` | `UPDATED_TIME` | 4 | 0 | 0 | ALL-NULL |
| `demo_target1_INS` | `ACTIVE_FLAG` | 4 | 0 | 0 | ALL-NULL |
| `demo_target1_INS` | `START_DATE` | 4 | 0 | 0 | ALL-NULL |
| `demo_target1_INS` | `END_DATE` | 4 | 0 | 0 | ALL-NULL |
| `demo_target1_UPD` | `Key` | 3 | 3 | 3 | NON-DEGENERATE |
| `demo_target1_UPD` | `LEAD_CO_MNE` | 3 | 3 | 3 | NON-DEGENERATE |
| `demo_target1_UPD` | `BRANCH_CO_MNE` | 3 | 3 | 3 | NON-DEGENERATE |
| `demo_target1_UPD` | `MIS_DATE` | 3 | 3 | 1 | WEAK |
| `demo_target1_UPD` | `ID` | 3 | 3 | 3 | NON-DEGENERATE |
| `demo_target1_UPD` | `DESCRIPTION` | 3 | 3 | 3 | NON-DEGENERATE |
| `demo_target1_UPD` | `SHORT_NAME` | 3 | 3 | 3 | NON-DEGENERATE |
| `demo_target1_UPD` | `CREATED_BY` | 3 | 0 | 0 | ALL-NULL |
| `demo_target1_UPD` | `CREATED_TIME` | 3 | 0 | 0 | ALL-NULL |
| `demo_target1_UPD` | `UPDATED_BY` | 3 | 3 | 1 | WEAK |
| `demo_target1_UPD` | `UPDATED_TIME` | 3 | 3 | 1 | WEAK |
| `demo_target1_UPD` | `ACTIVE_FLAG` | 3 | 0 | 0 | ALL-NULL |
| `demo_target1_UPD` | `START_DATE` | 3 | 0 | 0 | ALL-NULL |
| `demo_target1_UPD` | `END_DATE` | 3 | 0 | 0 | ALL-NULL |
| `demo_target2` | `Title` | 3 | 3 | 2 | NON-DEGENERATE |
| `demo_target2` | `Gender` | 3 | 3 | 1 | WEAK |
| `demo_target2` | `First_Name` | 3 | 3 | 3 | NON-DEGENERATE |
| `demo_target2` | `Middle_Name` | 3 | 3 | 3 | NON-DEGENERATE |
| `demo_target2` | `Last_Name` | 3 | 3 | 3 | NON-DEGENERATE |
| `demo_target2` | `Member_Identifier` | 3 | 3 | 3 | NON-DEGENERATE |
| `demo_target2` | `Member_Suffix` | 3 | 1 | 1 | WEAK |
| `demo_target2` | `Date_of_Birth` | 3 | 3 | 3 | NON-DEGENERATE |
| `demo_target2` | `Member_Number` | 3 | 3 | 3 | NON-DEGENERATE |
| `demo_target2` | `Soc_Number` | 3 | 0 | 0 | ALL-NULL |
| `demo_target2` | `Type_Code` | 3 | 3 | 2 | NON-DEGENERATE |
| `demo_target2` | `Relationship_to_Subscriber_Code` | 3 | 3 | 3 | NON-DEGENERATE |
| `demo_target2` | `Relationship_to_Subscriber_Code_Label` | 3 | 3 | 2 | NON-DEGENERATE |
| `demo_target2` | `Effective_Date` | 3 | 3 | 3 | NON-DEGENERATE |
| `demo_target21` | `Title` | 3 | 3 | 2 | NON-DEGENERATE |
| `demo_target21` | `Gender` | 3 | 3 | 1 | WEAK |
| `demo_target21` | `First_Name` | 3 | 3 | 3 | NON-DEGENERATE |
| `demo_target21` | `Middle_Name` | 3 | 3 | 3 | NON-DEGENERATE |
| `demo_target21` | `Last_Name` | 3 | 3 | 3 | NON-DEGENERATE |
| `demo_target21` | `Member_Identifier` | 3 | 3 | 3 | NON-DEGENERATE |
| `demo_target21` | `Member_Suffix` | 3 | 0 | 0 | ALL-NULL |
| `demo_target21` | `Date_of_Birth` | 3 | 3 | 3 | NON-DEGENERATE |
| `demo_target21` | `Member_Number` | 3 | 3 | 3 | NON-DEGENERATE |
| `demo_target21` | `Soc_Number` | 3 | 3 | 3 | NON-DEGENERATE |
| `demo_target21` | `Type_Code` | 3 | 3 | 2 | NON-DEGENERATE |
| `demo_target21` | `Relationship_to_Subscriber_Code` | 3 | 3 | 3 | NON-DEGENERATE |
| `demo_target21` | `Relationship_to_Subscriber_Code_Label` | 3 | 3 | 3 | NON-DEGENERATE |
| `demo_target21` | `Effective_Date` | 3 | 3 | 3 | NON-DEGENERATE |
| `demo_target3` | `PRODUCT_ID` | 4 | 4 | 4 | NON-DEGENERATE |
| `demo_target3` | `PRODUCT_NM` | 4 | 4 | 4 | NON-DEGENERATE |
| `demo_target3` | `PRODUCT_NO` | 4 | 4 | 4 | NON-DEGENERATE |
| `demo_target3` | `COLOR` | 4 | 4 | 3 | NON-DEGENERATE |
| `demo_target3` | `STD_COST` | 4 | 4 | 4 | NON-DEGENERATE |
| `demo_target3` | `LIST_PRICE` | 4 | 4 | 4 | NON-DEGENERATE |
| `demo_target3` | `SELL_ST_DT` | 4 | 0 | 0 | ALL-NULL |
| `demo_target3` | `SELL_ED_DT` | 4 | 4 | 4 | NON-DEGENERATE |
| `demo_target5` | `ACCT_ID` | 2 | 2 | 2 | NON-DEGENERATE |
| `demo_target5` | `FIRST_NM` | 2 | 2 | 2 | NON-DEGENERATE |
| `demo_target5` | `LAST_NM` | 2 | 2 | 2 | NON-DEGENERATE |
| `demo_target5` | `BAL_AMT` | 2 | 2 | 2 | NON-DEGENERATE |
| `demo_target5` | `CRDT_SCORE` | 2 | 2 | 2 | NON-DEGENERATE |
| `demo_target6` | `ACCT_ID` | 2 | 2 | 2 | NON-DEGENERATE |
| `demo_target6` | `ACCT_TYP` | 2 | 2 | 1 | WEAK |
| `demo_target6` | `ACCT_DESC` | 2 | 2 | 2 | NON-DEGENERATE |
| `demo_target6` | `CR8_DT` | 2 | 2 | 1 | WEAK |
| `demo_target6` | `CRDT_LN` | 2 | 2 | 2 | NON-DEGENERATE |
| `demo_target6` | `CLSR_DT` | 2 | 1 | 1 | WEAK |
| `demo_target6` | `ACCT_STAT_CD` | 2 | 2 | 2 | NON-DEGENERATE |
| `demo_target6` | `TX_ID` | 2 | 2 | 2 | NON-DEGENERATE |
| `demo_target6` | `ACCT_KEY` | 2 | 2 | 2 | NON-DEGENERATE |
| `demo_target6` | `TX_DTTM` | 2 | 2 | 2 | NON-DEGENERATE |
| `demo_target6` | `TX_AMT` | 2 | 2 | 2 | NON-DEGENERATE |
| `demo_target6` | `TX_TYPE_CD` | 2 | 2 | 1 | WEAK |

## 5. Volume and distribution

Volume is not risk: counts identify dense surfaces and test inventory, while confidence and cardinality determine where manual review pays off.

### dbt models, SQL, and tests

| Layer | Models | SQL lines | Schema tests | Singular tests |
|---|---:|---:|---:|---:|
| staging | 9 | 248 | 9 | 0 |
| intermediate | 16 | 456 | 0 | 0 |
| marts | 7 | 179 | 17 | 0 |
| **Total** | **32** | **883** | **26** | **2** |

The 26 schema-test declarations are 17 `accepted_values` and 9 `not_null`; the two singular tests are the mapping3 relationship-label and Soc-number controls.

### Models by mapping/layer

| Mapping / shared layer | Staging models | Intermediate models | Mart models | SQL lines in intermediate + marts |
|---|---:|---:|---:|---:|
| Shared staging (used by all mappings) | 9 | — | — | — |
| `m_demo_mapping1` | — | 7 | 3 | 234 |
| `m_demo_mapping2` | — | 4 | 2 | 173 |
| `m_demo_mapping3` | — | 5 | 2 | 228 |

### Expressions per transformation instance

| Transformation instance | Mapping | Expression/control rows |
|---|---|---:|
| `EXPTRANS` | `m_demo_mapping2` | 20 |
| `exp_TRANS1` | `m_demo_mapping1` | 17 |
| `exp_TRANS` | `m_demo_mapping1` | 15 |
| `EXPTRANS` | `m_demo_mapping3` | 15 |
| `agg_TRANS` | `m_demo_mapping1` | 12 |
| `exp_TRANS2` | `m_demo_mapping1` | 8 |
| `SEQ_GEN` | `m_demo_mapping1` | 2 |
| `lkp_TRANS2` | `m_demo_mapping1` | 2 |
| `lkp_TRANS3` | `m_demo_mapping1` | 2 |
| `rtr_TRANS` | `m_demo_mapping1` | 2 |
| `RTRTRANS` | `m_demo_mapping2` | 2 |
| `SEQTRANS` | `m_demo_mapping2` | 2 |
| `RTRTRANS` | `m_demo_mapping3` | 2 |
| `lkp_TRANS1` | `m_demo_mapping1` | 1 |
| `sq_demo_source4` | `m_demo_mapping1` | 1 |
| `LKPTRANS` | `m_demo_mapping2` | 1 |
| `SQ_demo_source2` | `m_demo_mapping3` | 1 |

Densest inventory instances are mapping2 `EXPTRANS` (20 rows), mapping1 `exp_TRANS1` (17), mapping1 `exp_TRANS` (15), mapping3 `EXPTRANS` (15), and mapping1 `agg_TRANS` (12). These are the fattest logic surfaces in the extracted inventory; inspect them before smaller pass-through transformations.

### Expression-kind distribution

| Kind | Count | Share of 105 inventory rows |
|---|---:|---:|
| pass-through/rename | 74 | 70.5% |
| router condition | 6 | 5.7% |
| lookup call | 5 | 4.8% |
| date | 4 | 3.8% |
| sequence | 4 | 3.8% |
| string | 3 | 2.9% |
| conditional IIF/DECODE | 2 | 1.9% |
| hash/crypto | 2 | 1.9% |
| literal | 2 | 1.9% |
| aggregate | 2 | 1.9% |
| ABORT | 1 | 1.0% |

No zero-count category is shown. `Sql Query` overrides are counted under pass-through/rename because they define the recovered source port rowset rather than a separate expression language.

### Mapping lineage and volumes

| Mapping | Targets / columns | Source tables | Lookups | Router groups |
|---|---|---|---|---|
| `m_demo_mapping1` | `demo_target3` (8), `demo_target5` (5), `demo_target6` (12) | `demo_source3`, `demo_source4`, `demo_source5` | `lkp_demo_source1`, `lkp_demo_source2`, `lkp_demo_source3` | `demo_target6_GRP`, `demo_target5_GRP` (plus unreachable DEFAULT1) |
| `m_demo_mapping2` | `demo_target1_INS` (14), `demo_target1_UPD` (14) | `demo_source1`, target-state `demo_target1` | target-state `demo_target1` | `Insert`, `Update` (plus unreachable DEFAULT1) |
| `m_demo_mapping3` | `demo_target2` (14), `demo_target21` (14) | `demo_source2` | none | `NEWGROUP1`, `NEWGROUP2` (plus unreachable DEFAULT1) |

| Data volume | Rows |
|---|---:|
| demo_source1 seed | 7 |
| demo_source2 seed | 7 |
| demo_source3 seed | 6 |
| demo_source4 seed | 5 |
| demo_source5 seed | 4 |
| demo_target1 state seed | 5 |
| lkp_demo_source1 seed | 6 |
| lkp_demo_source2 seed | 6 |
| lkp_demo_source3 seed | 6 |
| **all dbt seed rows** | 52 |
| demo_target1_INS baseline | 4 |
| demo_target1_UPD baseline | 3 |
| demo_target2 baseline | 3 |
| demo_target21 baseline | 3 |
| demo_target3 baseline | 4 |
| demo_target5 baseline | 2 |
| demo_target6 baseline | 2 |
| **all baseline target rows** | 21 |

### Milestone effort and divergence attribution

The divergence count and attribution below are copied from `/home/ubuntu/informatica_migration_report.md`; they are not re-derived here.

| Milestone | Models delivered | Accepted after correction rounds | Divergences caught / attributed |
|---|---:|---:|---|
| Scaffold / shared integration (orchestrator) | 9 seeds + 9 staging + shared workflow/profile | pre-fan-out; integration accepted after shared fixes | 5: lookup ordering, quoted identifiers/select-star, workflow seeding, plus shared setup corrections |
| A — mapping1 | 10 (7 intermediate + 3 marts) | 2 | all-null DATE comparator type; ordering-in-view issue (plus mapping1 review fixes) |
| B — mapping2 | 6 (4 intermediate + 2 marts) | 1 | change-detection legacy bug hidden behind output-equivalent shortcut |
| C — mapping3 | 7 (5 intermediate incl. fixture + 2 marts) | 1 | target-instance rationale corrected against XML |
| D — Snowflake | verification/scripts; no new marts | 0 | warehouse value/type limitation documented; no model divergence |
| **Published total** | — | — | **8 divergences** |

## 6. Coverage gaps

- All three mapping2 lookup/change-detection rows are matched by the current seeds, but the `AES_DECRYPT` plaintext is unrecoverable and the sentinel is never exercised as a true decrypted value. A wrong decryption strategy would not be isolated by the current seven-target parity.
- Mapping2 `MD5_tgt` NULL-concat behavior has no baseline row with NULL in any of its five source operands; the `coalesce(..., '')` decision is therefore LOW despite parity.
- Lookup duplicate winners are represented by the physical `SEED_ROW` decision, but no separate adversarial fixture permutes physical order or creates a tie for the `Use Any Value` Key tie-break.
- Aggregator pass-through tie-breaking has no equal-`TX_ID` rows within an `ACCT_ID`; the highest-`TX_ID` choice is not independently exercised.
- `demo_target3.SELL_ST_DT` is all NULL, so the date expression’s output cannot distinguish a wrong implementation. `demo_target1_INS/UPD` audit/null target columns are similarly weak or all NULL.
- Mapping3 `ABORT` is exercised by a dedicated fixture, not normal seeds. The normal seeds exercise the non-null branch only.
- Router defaults are unreachable/discarded for the supplied rows and have no target output. Workflow Email and Control tasks are not value-level dbt expressions.
- Snowflake `MINUS` proves values, not declared types: `load_baseline_snowflake.py` derives baseline types from the migrated table `INFORMATION_SCHEMA.COLUMNS`. Datatype contradictions are covered by dbt tests, model headers, and the documented XML review.

## Verification

The report was prepared against the existing branch and is intended to be followed by the required unchanged-project checks: `source /home/ubuntu/venv-dbt/bin/activate && cd dbt/informatica && dbt build --target dev`; `PARITY_PYTHON=/home/ubuntu/venv-p2/bin/python ./dbt/informatica/run_parity.sh`; and `git diff --exit-code legacy/ tools/ baseline/`.
