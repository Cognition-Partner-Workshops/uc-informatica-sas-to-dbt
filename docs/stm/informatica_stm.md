# Informatica Source-to-Target Mapping (STM)

Derived deterministically from `legacy/informatica/wf_demo_mapping.XML` by `tools/informatica_lineage.py`.

Business/run date is pinned to **2024-01-31** for all SYSDATE / SYSTIMESTAMP references.

## Workflow and session execution order

- `Decision2` → `Failed_Email2` (condition `$Decision2.Condition = 0`)
- `Decision3` → `SuccessEmail` (condition `$Decision3.Condition = 1`)
- `Decision1` → `Failed_Email1` (condition `$Decision1.Condition = 0`)
- `Failed_Email2` → `Control`
- `Decision2` → `s_m_demo_mapping3` (condition `$Decision2.Condition = 1`)
- `Decision1` → `s_m_demo_mapping1`
- `Start` → `s_m_demo_mapping2`
- `s_m_demo_mapping1` → `Decision2`
- `s_m_demo_mapping2` → `Decision1`
- `s_m_demo_mapping3` → `Decision3`
- `Decision3` → `Failed_Email3` (condition `$Decision3.Condition = 0`)

PowerCenter evaluates Router output groups independently rather than as an if/else chain. Mapping-specific session details below therefore determine execution order and pre-run lookup state.

### Session `s_m_demo_mapping3` (mapping `m_demo_mapping3`)

- Treat source rows as: `Insert`
- Writer `demo_target21`: Target load type=`Bulk`; Insert=`YES`; Update as Update=`YES`; Update as Insert=`NO`; Update else Insert=`NO`; Delete=`YES`; Truncate target table option=`NO`; Reject filename=`demo_target211.bad`
- Writer `demo_target2`: Target load type=`Bulk`; Insert=`YES`; Update as Update=`YES`; Update as Insert=`NO`; Update else Insert=`NO`; Delete=`YES`; Truncate target table option=`NO`; Reject filename=`demo_target21.bad`

### Session `s_m_demo_mapping1` (mapping `m_demo_mapping1`)

- Treat source rows as: `Insert`
- Writer `demo_target6`: Target load type=`Bulk`; Insert=`YES`; Update as Update=`YES`; Update as Insert=`NO`; Update else Insert=`NO`; Delete=`YES`; Truncate target table option=`NO`; Reject filename=`demo_target61.bad`
- Writer `demo_target5`: Target load type=`Bulk`; Insert=`YES`; Update as Update=`YES`; Update as Insert=`NO`; Update else Insert=`NO`; Delete=`YES`; Truncate target table option=`NO`; Reject filename=`demo_target51.bad`
- Writer `demo_target3`: Target load type=`Bulk`; Insert=`YES`; Update as Update=`YES`; Update as Insert=`NO`; Update else Insert=`NO`; Delete=`YES`; Truncate target table option=`NO`; Reject filename=`demo_target31.bad`
- Flat-file reader `demo_source5`: SKIPROWS=`0`; CONSECDELIMITERSASONE=`YES`; NULL_CHARACTER=`*`; Datetime Format=`A 19 mm/dd/yyyy hh24:mi:ss`

### Session `s_m_demo_mapping2` (mapping `m_demo_mapping2`)

- Treat source rows as: `Data driven`
- Writer `demo_target1_INS`: Target load type=`Bulk`; Insert=`YES`; Update as Update=`YES`; Update as Insert=`NO`; Update else Insert=`NO`; Delete=`YES`; Truncate target table option=`NO`; Reject filename=`demo_target1_ins1.bad`
- Writer `demo_target1_UPD`: Target load type=`Bulk`; Insert=`YES`; Update as Update=`YES`; Update as Insert=`NO`; Update else Insert=`NO`; Delete=`YES`; Truncate target table option=`NO`; Reject filename=`demo_target1_upd1.bad`
- Flat-file reader `demo_source1`: SKIPROWS=`1`; CONSECDELIMITERSASONE=`NO`; NULL_CHARACTER=`*`; Datetime Format=`A 19 mm/dd/yyyy hh24:mi:ss`

## Mapping `m_demo_mapping1`

- Sources: `demo_source3`, `demo_source4`, `demo_source5`
- Target instances: `demo_target3`, `demo_target5`, `demo_target6`

Physical target instance groups: `demo_target3` = demo_target3; `demo_target5` = demo_target5; `demo_target6` = demo_target6

### SQL overrides

- `sq_demo_source4` SQL: `SELECT demo_source4.ACCT_ID, demo_source4.ACCT_TYP, demo_source4.ACCT_DESC, demo_source4.CRDT_LN, SYSTIMESTAMP, demo_source4.CLSR_DT, demo_source4.ACCT_STAT_CD, demo_source3.TX_ID, demo_source3.LAST_NM, demo_source3.TX_DTTM, demo_source3.TX_AMT, demo_source3.BAL_AMT, demo_source3.CUST_ID, STRCMP(demo_source4.ACCT_STAT_CD,demo_source3.TX_TYPE_CD) FROM demo_source3 INNER JOIN demo_source4 ON demo_source3.ACCT_ID = demo_source4.ACCT_ID ORDER BY demo_source4.ACCT_ID`
  - join: `demo_source3.ACCT_ID = demo_source4.ACCT_ID`
  - order_by: `demo_source4.ACCT_ID`
- Positional bindings: 1 → `ACCT_ID` = `demo_source4.ACCT_ID`; 2 → `ACCT_TYP` = `demo_source4.ACCT_TYP`; 3 → `ACCT_DESC` = `demo_source4.ACCT_DESC`; 4 → `CRDT_LN` = `demo_source4.CRDT_LN`; 5 → `CR8_DT` = `SYSTIMESTAMP`; 6 → `CLSR_DT` = `demo_source4.CLSR_DT`; 7 → `ACCT_STAT_CD` = `demo_source4.ACCT_STAT_CD`; 8 → `TX_ID` = `demo_source3.TX_ID`; 9 → `LAST_NM` = `demo_source3.LAST_NM`; 10 → `TX_DTTM` = `demo_source3.TX_DTTM`; 11 → `TX_AMT` = `demo_source3.TX_AMT`; 12 → `BAL_AMT` = `demo_source3.BAL_AMT`; 13 → `CUST_ID` = `demo_source3.CUST_ID`; 14 → `TX_TYPE_CD` = `STRCMP(demo_source4.ACCT_STAT_CD,demo_source3.TX_TYPE_CD)`

### Misleading or name-sensitive bindings

- **high** `sq_demo_source4.CR8_DT` = `SYSTIMESTAMP`: bound expression is not table.port with the same port name.
- **high** `sq_demo_source4.TX_TYPE_CD` = `STRCMP(demo_source4.ACCT_STAT_CD,demo_source3.TX_TYPE_CD)`: bound expression is not table.port with the same port name.
- **note** `sq_demo_source4.TX_ID` = `demo_source3.TX_ID`: same-named port comes from sibling table demo_source3, rather than sibling table demo_source4.
- **note** `sq_demo_source4.LAST_NM` = `demo_source3.LAST_NM`: same-named port comes from sibling table demo_source3, rather than sibling table demo_source4.
- **note** `sq_demo_source4.TX_DTTM` = `demo_source3.TX_DTTM`: same-named port comes from sibling table demo_source3, rather than sibling table demo_source4.
- **note** `sq_demo_source4.TX_AMT` = `demo_source3.TX_AMT`: same-named port comes from sibling table demo_source3, rather than sibling table demo_source4.
- **note** `sq_demo_source4.BAL_AMT` = `demo_source3.BAL_AMT`: same-named port comes from sibling table demo_source3, rather than sibling table demo_source4.
- **note** `sq_demo_source4.CUST_ID` = `demo_source3.CUST_ID`: same-named port comes from sibling table demo_source3, rather than sibling table demo_source4.
- **high** `exp_TRANS.o_ACCT_ID` = `:LKP.lkp_TRANS1(ACCT_ID)`: named port yields lkp_demo_source3.TX_TYPE_CD; return port `TX_TYPE_CD`, table `lkp_demo_source3`.

### Lookup details

- `lkp_TRANS1`: table `lkp_demo_source3`; condition `ACCT_ID = IN_ACCT_ID`; multiple-match `Use Last Value`; connection `test`; cache `YES`; case-sensitive `NO`; sorted input `NO`; null ordering `Null Is Highest Value`; RETURN port `TX_TYPE_CD`; exists in export **False**.
- `lkp_TRANS2`: table `lkp_demo_source1`; condition `ACCT_ID = IN_ACCT_ID`; multiple-match `Use Last Value`; connection `test`; cache `YES`; case-sensitive `NO`; sorted input `NO`; null ordering `Null Is Highest Value`; RETURN port (none — connected lookup, outputs flow through connectors); exists in export **False**.
- `lkp_TRANS3`: table `lkp_demo_source2`; condition `CUST_ID = IN_CUST_ID`; multiple-match `Use Last Value`; connection `test`; cache `YES`; case-sensitive `NO`; sorted input `NO`; null ordering `Null Is Highest Value`; RETURN port (none — connected lookup, outputs flow through connectors); exists in export **False**.

### Router `rtr_TRANS`

- PowerCenter evaluates output groups independently; a row can satisfy multiple groups.
- Group `demo_target6_GRP`: condition `ACCT_TYP = 'SB'`; expanded `ACCT_TYP = 'SB'`; output ports BAL_AMT1, ACCT_ID1, o_ACCT_ID1, o_acc_trim1, TX_DTTM1, TX_ID1, ACCT_TYP1, TX_AMT1, LAST_NM1, CLSR_DT1, ACCT_STAT_CD1, o_ACCT_DESC1, CR8_DT1, o_crdt_trim1, FIRST_NM1, CRDT_SCORE1; has outgoing connectors; downstream `agg_TRANS`.
  - `ACCT_TYP` definition: exp_TRANS1.ACCT_TYP → exp_TRANS.ACCT_TYP → sq_demo_source4.ACCT_TYP = demo_source4.ACCT_TYP [SQL override position 2]
- Group `demo_target5_GRP`: condition `ACCT_TYP != 'SB'`; expanded `ACCT_TYP != 'SB'`; output ports BAL_AMT2, ACCT_ID2, o_ACCT_ID2, o_acc_trim2, TX_DTTM2, TX_ID2, ACCT_TYP2, TX_AMT2, LAST_NM2, CLSR_DT2, ACCT_STAT_CD2, o_ACCT_DESC2, CR8_DT2, o_crdt_trim2, FIRST_NM2, CRDT_SCORE2; has outgoing connectors; downstream `demo_target5`.
  - `ACCT_TYP` definition: exp_TRANS1.ACCT_TYP → exp_TRANS.ACCT_TYP → sq_demo_source4.ACCT_TYP = demo_source4.ACCT_TYP [SQL override position 2]
- Group `DEFAULT1`: condition `(default group)`; expanded `(default group — no condition)`; output ports BAL_AMT3, ACCT_ID3, o_ACCT_ID3, o_acc_trim3, TX_DTTM3, TX_ID3, ACCT_TYP3, TX_AMT3, LAST_NM3, CLSR_DT3, ACCT_STAT_CD3, o_ACCT_DESC3, CR8_DT3, o_crdt_trim3, FIRST_NM3, CRDT_SCORE3; has zero outgoing connectors; downstream (none).
  - Rows reaching this group are discarded.

### Transformation `agg_TRANS` (Aggregator)

Ports are rendered in XML order, which is PowerCenter's variable evaluation order.
- `o_ACCT_DESC` (INPUT/OUTPUT): `o_ACCT_DESC`
- `TX_AMT` (INPUT/OUTPUT): `TX_AMT`
- `o_crdt_trim` (INPUT/OUTPUT): `o_crdt_trim`
- `CLSR_DT` (INPUT/OUTPUT): `CLSR_DT`
- `TX_ID` (INPUT/OUTPUT): `TX_ID`
- `ACCT_STAT_CD` (INPUT/OUTPUT): `ACCT_STAT_CD`
- `TX_DTTM` (INPUT/OUTPUT): `TX_DTTM`
- `CR8_DT` (INPUT/OUTPUT): `CR8_DT`
- `o_ACCT_ID` (INPUT/OUTPUT): `o_ACCT_ID`
- `ACCT_ID` (INPUT/OUTPUT): `ACCT_ID`
- `o_acc_trim` (INPUT/OUTPUT): `o_acc_trim`
- `o_TX_AMT` (OUTPUT): `SUM(TX_AMT)`
- **Sorted Input**: `YES`
- **Transformation Scope**: `All Input`
- GROUPBY ports: ACCT_ID
- Non-group-by pass-through ports yield the last row received per group; with no GROUPBY port, one row is returned for the whole input.

### Transformation `exp_TRANS` (Expression)

Ports are rendered in XML order, which is PowerCenter's variable evaluation order.
- `CLSR_DT` (INPUT/OUTPUT): `CLSR_DT`
- `TX_DTTM` (INPUT/OUTPUT): `TX_DTTM`
- `BAL_AMT` (INPUT/OUTPUT): `BAL_AMT`
- `ACCT_DESC` (INPUT/OUTPUT): `ACCT_DESC`
- `ACCT_TYP` (INPUT/OUTPUT): `ACCT_TYP`
- `ACCT_STAT_CD` (INPUT/OUTPUT): `ACCT_STAT_CD`
- `TX_ID` (INPUT/OUTPUT): `TX_ID`
- `LAST_NM` (INPUT/OUTPUT): `LAST_NM`
- `TX_AMT` (INPUT/OUTPUT): `TX_AMT`
- `ACCT_ID` (INPUT/OUTPUT): `ACCT_ID`
- `CR8_DT` (INPUT/OUTPUT): `CR8_DT`
- `CUST_ID` (INPUT/OUTPUT): `CUST_ID`
- `o_acc_trim` (OUTPUT): `RTRIM(ACCT_TYP)`
- `o_crdt_trim` (OUTPUT): `LTRIM(CRDT_LN)`
- `o_ACCT_ID` (OUTPUT): `:LKP.lkp_TRANS1(ACCT_ID)`

### Transformation `exp_TRANS1` (Expression)

Ports are rendered in XML order, which is PowerCenter's variable evaluation order.
- `FIRST_NM` (INPUT/OUTPUT): `FIRST_NM`
- `CLSR_DT` (INPUT/OUTPUT): `CLSR_DT`
- `TX_DTTM` (INPUT/OUTPUT): `TX_DTTM`
- `BAL_AMT` (INPUT/OUTPUT): `BAL_AMT`
- `ACCT_DESC` (INPUT/OUTPUT): `ACCT_DESC`
- `ACCT_TYP` (INPUT/OUTPUT): `ACCT_TYP`
- `ACCT_STAT_CD` (INPUT/OUTPUT): `ACCT_STAT_CD`
- `TX_ID` (INPUT/OUTPUT): `TX_ID`
- `LAST_NM` (INPUT/OUTPUT): `LAST_NM`
- `TX_AMT` (INPUT/OUTPUT): `TX_AMT`
- `ACCT_ID` (INPUT/OUTPUT): `ACCT_ID`
- `CR8_DT` (INPUT/OUTPUT): `CR8_DT`
- `o_acc_trim` (INPUT/OUTPUT): `o_acc_trim`
- `o_crdt_trim` (INPUT/OUTPUT): `o_crdt_trim`
- `o_ACCT_ID` (INPUT/OUTPUT): `o_ACCT_ID`
- `CRDT_SCORE` (INPUT/OUTPUT): `CRDT_SCORE`
- `o_ACCT_DESC` (OUTPUT): `RTRIM(ACCT_DESC)`

### Transformation `exp_TRANS2` (Expression)

Ports are rendered in XML order, which is PowerCenter's variable evaluation order.
- `PRODUCT_NO` (INPUT/OUTPUT): `PRODUCT_NO`
- `STD_COST` (INPUT/OUTPUT): `STD_COST`
- `COLOR` (INPUT/OUTPUT): `COLOR`
- `PRODUCT_ID` (INPUT/OUTPUT): `PRODUCT_ID`
- `PRODUCT_NM` (INPUT/OUTPUT): `PRODUCT_NM`
- `LIST_PRICE` (INPUT/OUTPUT): `LIST_PRICE`
- `o_SELL_ST_DT` (OUTPUT): `TO_DATE(TO_CHAR(SYSDATE),'DD/MM/YYYY')`
- `o_SELL_ED_DT` (OUTPUT): `TO_DATE(SELL_ED_DT,'DD/MM/YYYY')`

### Notes

- Unconnected lookup call `exp_TRANS.o_ACCT_ID` calling `lkp_TRANS1`: `:LKP.lkp_TRANS1(ACCT_ID)`; yields `lkp_demo_source3.TX_TYPE_CD`, RETURN port `TX_TYPE_CD`.
- Target columns with no connector: `demo_target3`: (none); `demo_target5`: (none); `demo_target6`: (none)

### Target instance `demo_target3` (table `demo_target3`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| demo_target3 | PRODUCT_ID | exp_TRANS2.PRODUCT_ID → SQ_demo_source5.PRODUCT_ID → demo_source5.PRODUCT_ID | demo_source5.PRODUCT_ID |
| demo_target3 | PRODUCT_NM | exp_TRANS2.PRODUCT_NM → SQ_demo_source5.PRODUCT_NM → demo_source5.PRODUCT_NM | demo_source5.PRODUCT_NM |
| demo_target3 | PRODUCT_NO | exp_TRANS2.PRODUCT_NO → SQ_demo_source5.PRODUCT_NO → demo_source5.PRODUCT_NO | demo_source5.PRODUCT_NO |
| demo_target3 | COLOR | exp_TRANS2.COLOR → SQ_demo_source5.COLOR → demo_source5.COLOR | demo_source5.COLOR |
| demo_target3 | STD_COST | exp_TRANS2.STD_COST → SQ_demo_source5.STD_COST → demo_source5.STD_COST | demo_source5.STD_COST |
| demo_target3 | LIST_PRICE | exp_TRANS2.LIST_PRICE → SQ_demo_source5.LIST_PRICE → demo_source5.LIST_PRICE | demo_source5.LIST_PRICE |
| demo_target3 | SELL_ST_DT | exp_TRANS2.o_SELL_ST_DT = TO_DATE(TO_CHAR(SYSDATE),'DD/MM/YYYY') | literal/expression: TO_DATE(TO_CHAR(SYSDATE),'DD/MM/YYYY') |
| demo_target3 | SELL_ED_DT | exp_TRANS2.o_SELL_ED_DT = TO_DATE(SELL_ED_DT,'DD/MM/YYYY') → SQ_demo_source5.SELL_ED_DT → demo_source5.SELL_ED_DT | demo_source5.SELL_ED_DT |

### Target instance `demo_target5` (table `demo_target5`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| demo_target5 | ACCT_ID | rtr_TRANS.ACCT_ID2 [router group demo_target5_GRP WHERE ACCT_TYP != 'SB'] → exp_TRANS1.ACCT_ID → exp_TRANS.ACCT_ID → sq_demo_source4.ACCT_ID = demo_source4.ACCT_ID [SQL override position 1] | demo_source4.ACCT_ID |
| demo_target5 | FIRST_NM | rtr_TRANS.FIRST_NM2 [router group demo_target5_GRP WHERE ACCT_TYP != 'SB'] → exp_TRANS1.FIRST_NM → lkp_TRANS2.FIRST_NM [lookup lkp_demo_source1.FIRST_NM ON ACCT_ID = IN_ACCT_ID] | demo_source4.ACCT_ID (lookup key); lkp_demo_source1.FIRST_NM (lookup) |
| demo_target5 | LAST_NM | rtr_TRANS.LAST_NM2 [router group demo_target5_GRP WHERE ACCT_TYP != 'SB'] → exp_TRANS1.LAST_NM → exp_TRANS.LAST_NM → sq_demo_source4.LAST_NM = demo_source3.LAST_NM [SQL override position 9] | demo_source3.LAST_NM |
| demo_target5 | BAL_AMT | rtr_TRANS.BAL_AMT2 [router group demo_target5_GRP WHERE ACCT_TYP != 'SB'] → exp_TRANS1.BAL_AMT → exp_TRANS.BAL_AMT → sq_demo_source4.BAL_AMT = demo_source3.BAL_AMT [SQL override position 12] | demo_source3.BAL_AMT |
| demo_target5 | CRDT_SCORE | rtr_TRANS.CRDT_SCORE2 [router group demo_target5_GRP WHERE ACCT_TYP != 'SB'] → exp_TRANS1.CRDT_SCORE → lkp_TRANS3.CRDT_SCORE [lookup lkp_demo_source2.CRDT_SCORE ON CUST_ID = IN_CUST_ID] | demo_source3.CUST_ID (lookup key); lkp_demo_source2.CRDT_SCORE (lookup) |

### Target instance `demo_target6` (table `demo_target6`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| demo_target6 | ACCT_ID | agg_TRANS.ACCT_ID → rtr_TRANS.ACCT_ID1 [router group demo_target6_GRP WHERE ACCT_TYP = 'SB'] → exp_TRANS1.ACCT_ID → exp_TRANS.ACCT_ID → sq_demo_source4.ACCT_ID = demo_source4.ACCT_ID [SQL override position 1] | demo_source4.ACCT_ID |
| demo_target6 | ACCT_TYP | agg_TRANS.o_acc_trim → rtr_TRANS.o_acc_trim1 [router group demo_target6_GRP WHERE ACCT_TYP = 'SB'] → exp_TRANS1.o_acc_trim → exp_TRANS.o_acc_trim = RTRIM(ACCT_TYP) → sq_demo_source4.ACCT_TYP = demo_source4.ACCT_TYP [SQL override position 2] | demo_source4.ACCT_TYP |
| demo_target6 | ACCT_DESC | agg_TRANS.o_ACCT_DESC → rtr_TRANS.o_ACCT_DESC1 [router group demo_target6_GRP WHERE ACCT_TYP = 'SB'] → exp_TRANS1.o_ACCT_DESC = RTRIM(ACCT_DESC) → exp_TRANS.ACCT_DESC → sq_demo_source4.ACCT_DESC = demo_source4.ACCT_DESC [SQL override position 3] | demo_source4.ACCT_DESC |
| demo_target6 | CR8_DT | agg_TRANS.CR8_DT → rtr_TRANS.CR8_DT1 [router group demo_target6_GRP WHERE ACCT_TYP = 'SB'] → exp_TRANS1.CR8_DT → exp_TRANS.CR8_DT → sq_demo_source4.CR8_DT = SYSTIMESTAMP [SQL override position 5] | literal/expression: SYSTIMESTAMP |
| demo_target6 | CRDT_LN | agg_TRANS.o_crdt_trim → rtr_TRANS.o_crdt_trim1 [router group demo_target6_GRP WHERE ACCT_TYP = 'SB'] → exp_TRANS1.o_crdt_trim → exp_TRANS.o_crdt_trim = LTRIM(CRDT_LN) → sq_demo_source4.CRDT_LN = demo_source4.CRDT_LN [SQL override position 4] | demo_source4.CRDT_LN |
| demo_target6 | CLSR_DT | agg_TRANS.CLSR_DT → rtr_TRANS.CLSR_DT1 [router group demo_target6_GRP WHERE ACCT_TYP = 'SB'] → exp_TRANS1.CLSR_DT → exp_TRANS.CLSR_DT → sq_demo_source4.CLSR_DT = demo_source4.CLSR_DT [SQL override position 6] | demo_source4.CLSR_DT |
| demo_target6 | ACCT_STAT_CD | agg_TRANS.ACCT_STAT_CD → rtr_TRANS.ACCT_STAT_CD1 [router group demo_target6_GRP WHERE ACCT_TYP = 'SB'] → exp_TRANS1.ACCT_STAT_CD → exp_TRANS.ACCT_STAT_CD → sq_demo_source4.ACCT_STAT_CD = demo_source4.ACCT_STAT_CD [SQL override position 7] | demo_source4.ACCT_STAT_CD |
| demo_target6 | TX_ID | agg_TRANS.TX_ID → rtr_TRANS.TX_ID1 [router group demo_target6_GRP WHERE ACCT_TYP = 'SB'] → exp_TRANS1.TX_ID → exp_TRANS.TX_ID → sq_demo_source4.TX_ID = demo_source3.TX_ID [SQL override position 8] | demo_source3.TX_ID |
| demo_target6 | ACCT_KEY | SEQ_GEN.NEXTVAL [sequence start=1 increment=1 current=281 cycle=YES] | SEQ_GEN (generated) |
| demo_target6 | TX_DTTM | agg_TRANS.TX_DTTM → rtr_TRANS.TX_DTTM1 [router group demo_target6_GRP WHERE ACCT_TYP = 'SB'] → exp_TRANS1.TX_DTTM → exp_TRANS.TX_DTTM → sq_demo_source4.TX_DTTM = demo_source3.TX_DTTM [SQL override position 10] | demo_source3.TX_DTTM |
| demo_target6 | TX_AMT | agg_TRANS.o_TX_AMT = SUM(TX_AMT) → rtr_TRANS.TX_AMT1 [router group demo_target6_GRP WHERE ACCT_TYP = 'SB'] → exp_TRANS1.TX_AMT → exp_TRANS.TX_AMT → sq_demo_source4.TX_AMT = demo_source3.TX_AMT [SQL override position 11] | demo_source3.TX_AMT |
| demo_target6 | TX_TYPE_CD | agg_TRANS.o_ACCT_ID → rtr_TRANS.o_ACCT_ID1 [router group demo_target6_GRP WHERE ACCT_TYP = 'SB'] → exp_TRANS1.o_ACCT_ID → exp_TRANS.o_ACCT_ID = :LKP.lkp_TRANS1(ACCT_ID) [yields lkp_demo_source3.TX_TYPE_CD; lookup lkp_TRANS1 ON ACCT_ID =  IN_ACCT_ID; multiple-match Use Last Value] | demo_source4.ACCT_ID (lookup key); lkp_demo_source3.TX_TYPE_CD (lookup return) |

## Mapping `m_demo_mapping2`

- Sources: `demo_source1`
- Target instances: `demo_target1_INS`, `demo_target1_UPD`

Physical target instance groups: `demo_target1` = demo_target1_INS, demo_target1_UPD

### Lookup details

- `LKPTRANS`: table `demo_target1`; condition `ID = ID1`; multiple-match `Use Any Value`; connection `$Target`; cache `YES`; case-sensitive `NO`; sorted input `NO`; null ordering `Null Is Highest Value`; RETURN port (none — connected lookup, outputs flow through connectors); exists in export **True**.
  - `$Target` means the mapping's own target table and therefore pre-run target state.

### Router `RTRTRANS`

- PowerCenter evaluates output groups independently; a row can satisfy multiple groups.
- Group `Insert`: condition `New_Flag='Insert'`; expanded `New_Flag='Insert'`; output ports LEAD_CO_MNE2, BRANCH_CO_MNE2, MIS_DATE2, ID1, DESCRIPTION2, SHORT_NAME2, LEAD_CO_MNE11, BRANCH_CO_MNE11, MIS_DATE11, DESCRIPTION11, SHORT_NAME11, New_Flag1, Changed_Flag1, o_CREATED_BY1, o_CREATED_TIME1, o_UPDATED_BY1, o_UPDATED_TIME1, Key1; has outgoing connectors; downstream `demo_target1_INS`.
  - `New_Flag` definition: EXPTRANS.New_Flag = IIF(ISNULL(Key),'Insert') → LKPTRANS.Key [lookup demo_target1.Key ON ID = ID1]
- Group `DEFAULT1`: condition `(default group)`; expanded `(default group — no condition)`; output ports LEAD_CO_MNE3, BRANCH_CO_MNE3, MIS_DATE3, ID2, DESCRIPTION3, SHORT_NAME3, LEAD_CO_MNE12, BRANCH_CO_MNE12, MIS_DATE12, DESCRIPTION12, SHORT_NAME12, New_Flag2, Changed_Flag2, o_CREATED_BY2, o_CREATED_TIME2, o_UPDATED_BY2, o_UPDATED_TIME2, Key2; has zero outgoing connectors; downstream (none).
  - Rows reaching this group are discarded.
- Group `Update`: condition `Changed_Flag='Update'`; expanded `Changed_Flag='Update'`; output ports LEAD_CO_MNE4, BRANCH_CO_MNE4, MIS_DATE4, ID3, DESCRIPTION4, SHORT_NAME4, LEAD_CO_MNE13, BRANCH_CO_MNE13, MIS_DATE13, DESCRIPTION13, SHORT_NAME13, New_Flag3, Changed_Flag3, o_CREATED_BY3, o_CREATED_TIME3, o_UPDATED_BY3, o_UPDATED_TIME3, Key3; has outgoing connectors; downstream `UPDTRANS`.
  - `Changed_Flag` definition: EXPTRANS.Changed_Flag = IIF(NOT ISNULL(Key) AND  (MD5_tgt != MD5_src),'Update') → LKPTRANS.Key [lookup demo_target1.Key ON ID = ID1]

### Transformation `EXPTRANS` (Expression)

Ports are rendered in XML order, which is PowerCenter's variable evaluation order.
- `LEAD_CO_MNE` (INPUT/OUTPUT): `LEAD_CO_MNE`
- `BRANCH_CO_MNE` (INPUT/OUTPUT): `BRANCH_CO_MNE`
- `MIS_DATE` (INPUT/OUTPUT): `MIS_DATE`
- `ID` (INPUT/OUTPUT): `ID`
- `DESCRIPTION` (INPUT/OUTPUT): `DESCRIPTION`
- `SHORT_NAME` (INPUT/OUTPUT): `SHORT_NAME`
- `Key` (INPUT/OUTPUT): `Key`
- `LEAD_CO_MNE1` (INPUT/OUTPUT): `LEAD_CO_MNE1`
- `BRANCH_CO_MNE1` (INPUT/OUTPUT): `BRANCH_CO_MNE1`
- `MIS_DATE1` (INPUT/OUTPUT): `MIS_DATE1`
- `DESCRIPTION1` (INPUT/OUTPUT): `DESCRIPTION1`
- `SHORT_NAME1` (INPUT/OUTPUT): `SHORT_NAME1`
- `New_Flag` (OUTPUT): `IIF(ISNULL(Key),'Insert')`
- `MD5_src` (LOCAL VARIABLE): `AES_DECRYPT(LEAD_CO_MNE1, SUBSTR(SHORT_NAME,1,3), 256)`
- `MD5_tgt` (LOCAL VARIABLE): `MD5(LEAD_CO_MNE || BRANCH_CO_MNE || MIS_DATE || DESCRIPTION || SHORT_NAME)`
- `Changed_Flag` (OUTPUT): `IIF(NOT ISNULL(Key) AND (MD5_tgt != MD5_src),'Update')`
- `o_CREATED_BY` (OUTPUT): `'IDWUSER'`
- `o_CREATED_TIME` (OUTPUT): `SYSDATE`
- `o_UPDATED_BY` (OUTPUT): `'IDWUSER'`
- `o_UPDATED_TIME` (OUTPUT): `SYSDATE`

### Notes

- Target columns with no connector: `demo_target1_INS`: UPDATED_BY, UPDATED_TIME, ACTIVE_FLAG, START_DATE, END_DATE; `demo_target1_UPD`: CREATED_BY, CREATED_TIME, ACTIVE_FLAG, START_DATE, END_DATE

### Target instance `demo_target1_INS` (table `demo_target1`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| demo_target1_INS | Key | SEQTRANS.NEXTVAL [sequence start=0 increment=1 current=57 cycle=NO] | SEQTRANS (generated) |
| demo_target1_INS | LEAD_CO_MNE | RTRTRANS.LEAD_CO_MNE2 [router group Insert WHERE New_Flag='Insert'] → EXPTRANS.LEAD_CO_MNE → SQ_demo_source1.LEAD_CO_MNE → demo_source1.LEAD_CO_MNE | demo_source1.LEAD_CO_MNE |
| demo_target1_INS | BRANCH_CO_MNE | RTRTRANS.BRANCH_CO_MNE2 [router group Insert WHERE New_Flag='Insert'] → EXPTRANS.BRANCH_CO_MNE → SQ_demo_source1.BRANCH_CO_MNE → demo_source1.BRANCH_CO_MNE | demo_source1.BRANCH_CO_MNE |
| demo_target1_INS | MIS_DATE | RTRTRANS.MIS_DATE2 [router group Insert WHERE New_Flag='Insert'] → EXPTRANS.MIS_DATE → SQ_demo_source1.MIS_DATE → demo_source1.MIS_DATE | demo_source1.MIS_DATE |
| demo_target1_INS | ID | RTRTRANS.ID1 [router group Insert WHERE New_Flag='Insert'] → EXPTRANS.ID → SQ_demo_source1.ID → demo_source1.ID | demo_source1.ID |
| demo_target1_INS | DESCRIPTION | RTRTRANS.DESCRIPTION2 [router group Insert WHERE New_Flag='Insert'] → EXPTRANS.DESCRIPTION → SQ_demo_source1.DESCRIPTION → demo_source1.DESCRIPTION | demo_source1.DESCRIPTION |
| demo_target1_INS | SHORT_NAME | RTRTRANS.SHORT_NAME2 [router group Insert WHERE New_Flag='Insert'] → EXPTRANS.SHORT_NAME → SQ_demo_source1.SHORT_NAME → demo_source1.SHORT_NAME | demo_source1.SHORT_NAME |
| demo_target1_INS | CREATED_BY | RTRTRANS.o_CREATED_BY1 [router group Insert WHERE New_Flag='Insert'] → EXPTRANS.o_CREATED_BY = 'IDWUSER' | literal/expression: 'IDWUSER' |
| demo_target1_INS | CREATED_TIME | RTRTRANS.o_CREATED_TIME1 [router group Insert WHERE New_Flag='Insert'] → EXPTRANS.o_CREATED_TIME = SYSDATE | literal/expression: SYSDATE |
| demo_target1_INS | UPDATED_BY | (not connected — NULL) | — |
| demo_target1_INS | UPDATED_TIME | (not connected — NULL) | — |
| demo_target1_INS | ACTIVE_FLAG | (not connected — NULL) | — |
| demo_target1_INS | START_DATE | (not connected — NULL) | — |
| demo_target1_INS | END_DATE | (not connected — NULL) | — |

### Target instance `demo_target1_UPD` (table `demo_target1`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| demo_target1_UPD | Key | UPDTRANS.Key2 → RTRTRANS.Key3 [router group Update WHERE Changed_Flag='Update'] → EXPTRANS.Key → LKPTRANS.Key [lookup demo_target1.Key ON ID = ID1] | demo_source1.ID (lookup key); demo_target1.Key (lookup) |
| demo_target1_UPD | LEAD_CO_MNE | UPDTRANS.LEAD_CO_MNE3 → RTRTRANS.LEAD_CO_MNE4 [router group Update WHERE Changed_Flag='Update'] → EXPTRANS.LEAD_CO_MNE → SQ_demo_source1.LEAD_CO_MNE → demo_source1.LEAD_CO_MNE | demo_source1.LEAD_CO_MNE |
| demo_target1_UPD | BRANCH_CO_MNE | UPDTRANS.BRANCH_CO_MNE3 → RTRTRANS.BRANCH_CO_MNE4 [router group Update WHERE Changed_Flag='Update'] → EXPTRANS.BRANCH_CO_MNE → SQ_demo_source1.BRANCH_CO_MNE → demo_source1.BRANCH_CO_MNE | demo_source1.BRANCH_CO_MNE |
| demo_target1_UPD | MIS_DATE | UPDTRANS.MIS_DATE3 → RTRTRANS.MIS_DATE4 [router group Update WHERE Changed_Flag='Update'] → EXPTRANS.MIS_DATE → SQ_demo_source1.MIS_DATE → demo_source1.MIS_DATE | demo_source1.MIS_DATE |
| demo_target1_UPD | ID | UPDTRANS.ID2 → RTRTRANS.ID3 [router group Update WHERE Changed_Flag='Update'] → EXPTRANS.ID → SQ_demo_source1.ID → demo_source1.ID | demo_source1.ID |
| demo_target1_UPD | DESCRIPTION | UPDTRANS.DESCRIPTION3 → RTRTRANS.DESCRIPTION4 [router group Update WHERE Changed_Flag='Update'] → EXPTRANS.DESCRIPTION → SQ_demo_source1.DESCRIPTION → demo_source1.DESCRIPTION | demo_source1.DESCRIPTION |
| demo_target1_UPD | SHORT_NAME | UPDTRANS.SHORT_NAME3 → RTRTRANS.SHORT_NAME4 [router group Update WHERE Changed_Flag='Update'] → EXPTRANS.SHORT_NAME → SQ_demo_source1.SHORT_NAME → demo_source1.SHORT_NAME | demo_source1.SHORT_NAME |
| demo_target1_UPD | CREATED_BY | (not connected — NULL) | — |
| demo_target1_UPD | CREATED_TIME | (not connected — NULL) | — |
| demo_target1_UPD | UPDATED_BY | UPDTRANS.o_UPDATED_BY2 → RTRTRANS.o_UPDATED_BY3 [router group Update WHERE Changed_Flag='Update'] → EXPTRANS.o_UPDATED_BY = 'IDWUSER' | literal/expression: 'IDWUSER' |
| demo_target1_UPD | UPDATED_TIME | UPDTRANS.o_UPDATED_TIME2 → RTRTRANS.o_UPDATED_TIME3 [router group Update WHERE Changed_Flag='Update'] → EXPTRANS.o_UPDATED_TIME = SYSDATE | literal/expression: SYSDATE |
| demo_target1_UPD | ACTIVE_FLAG | (not connected — NULL) | — |
| demo_target1_UPD | START_DATE | (not connected — NULL) | — |
| demo_target1_UPD | END_DATE | (not connected — NULL) | — |

## Mapping `m_demo_mapping3`

- Sources: `demo_source2`
- Target instances: `demo_target2`, `demo_target21`

Physical target instance groups: `demo_target2` = demo_target2, demo_target21

### SQL overrides

- `SQ_demo_source2` SQL: `SELECT demo_source2.Title, demo_source2.First_Name, demo_source2.Middle_Name, demo_source2.Last_Name, demo_source2.Member_ID, demo_source2.Member_Suffix, demo_source2.Birth_Date, demo_source2.Gender_Code, demo_source2.Member_Record_Number, demo_source2.Social_Security_Number, demo_source2.Member_Type_Code, demo_source2.Original_Effective_Date, demo_source2.Relationship_to_Subscriber_Code, demo_source2.Relationship_to_Subscriber_Code_Label FROM demo_source2 where demo_source2.Member_Type_Code is not null`
  - row_filter: `demo_source2.Member_Type_Code is not null`
- Positional bindings: 1 → `Title` = `demo_source2.Title`; 2 → `First_Name` = `demo_source2.First_Name`; 3 → `Middle_Name` = `demo_source2.Middle_Name`; 4 → `Last_Name` = `demo_source2.Last_Name`; 5 → `Member_ID` = `demo_source2.Member_ID`; 6 → `Member_Suffix` = `demo_source2.Member_Suffix`; 7 → `Birth_Date` = `demo_source2.Birth_Date`; 8 → `Gender_Code` = `demo_source2.Gender_Code`; 9 → `Member_Record_Number` = `demo_source2.Member_Record_Number`; 10 → `Social_Security_Number` = `demo_source2.Social_Security_Number`; 11 → `Member_Type_Code` = `demo_source2.Member_Type_Code`; 12 → `Original_Effective_Date` = `demo_source2.Original_Effective_Date`; 13 → `Relationship_to_Subscriber_Code` = `demo_source2.Relationship_to_Subscriber_Code`; 14 → `Relationship_to_Subscriber_Code_Label` = `demo_source2.Relationship_to_Subscriber_Code_Label`

### Router `RTRTRANS`

- PowerCenter evaluates output groups independently; a row can satisfy multiple groups.
- Group `NEWGROUP1`: condition `ISNULL(Social_Security_Number)`; expanded `ISNULL(Social_Security_Number)`; output ports Title1, First_Name1, Middle_Name1, Last_Name1, Member_ID1, Member_Suffix1, Birth_Date1, Gender_Code1, Member_Record_Number1, Social_Security_Number1, Member_Type_Code1, Original_Effective_Date1, Relationship_to_Subscriber_Code1, Relationship_to_Subscriber_Code_Label1; has outgoing connectors; downstream `demo_target2`.
  - `Social_Security_Number` definition: EXPTRANS.Social_Security_Number → SQ_demo_source2.Social_Security_Number = demo_source2.Social_Security_Number [SQL override position 10]
- Group `DEFAULT1`: condition `(default group)`; expanded `(default group — no condition)`; output ports Title2, First_Name2, Middle_Name2, Last_Name2, Member_ID2, Member_Suffix2, Birth_Date2, Gender_Code2, Member_Record_Number2, Social_Security_Number2, Member_Type_Code2, Original_Effective_Date2, Relationship_to_Subscriber_Code2, Relationship_to_Subscriber_Code_Label2; has zero outgoing connectors; downstream (none).
  - Rows reaching this group are discarded.
- Group `NEWGROUP2`: condition `NOT ISNULL(Social_Security_Number)`; expanded `NOT ISNULL(Social_Security_Number)`; output ports Title3, First_Name3, Middle_Name3, Last_Name3, Member_ID3, Member_Suffix3, Birth_Date3, Gender_Code3, Member_Record_Number3, Social_Security_Number3, Member_Type_Code3, Original_Effective_Date3, Relationship_to_Subscriber_Code3, Relationship_to_Subscriber_Code_Label3; has outgoing connectors; downstream `demo_target21`.
  - `Social_Security_Number` definition: EXPTRANS.Social_Security_Number → SQ_demo_source2.Social_Security_Number = demo_source2.Social_Security_Number [SQL override position 10]

### Transformation `EXPTRANS` (Expression)

Ports are rendered in XML order, which is PowerCenter's variable evaluation order.
- `Title` (INPUT/OUTPUT): `Title`
- `First_Name` (INPUT/OUTPUT): `First_Name`
- `Middle_Name` (INPUT/OUTPUT): `Middle_Name`
- `Last_Name` (INPUT/OUTPUT): `Last_Name`
- `Member_ID` (INPUT/OUTPUT): `Member_ID`
- `Member_Suffix` (INPUT/OUTPUT): `Member_Suffix`
- `Birth_Date` (INPUT/OUTPUT): `Birth_Date`
- `Gender_Code` (INPUT/OUTPUT): `Gender_Code`
- `Member_Record_Number` (INPUT/OUTPUT): `Member_Record_Number`
- `Social_Security_Number` (INPUT/OUTPUT): `Social_Security_Number`
- `Member_Type_Code` (INPUT/OUTPUT): `Member_Type_Code`
- `Original_Effective_Date` (INPUT/OUTPUT): `Original_Effective_Date`
- `Relationship_to_Subscriber_Code` (INPUT/OUTPUT): `Relationship_to_Subscriber_Code`
- `Relationship_to_Subscriber_Code_Label` (INPUT/OUTPUT): `Relationship_to_Subscriber_Code_Label`
- `o_Relationship_to_Subscriber_Code_Label` (OUTPUT): `iif(ISNULL(Relationship_to_Subscriber_Code_Label),ABORT('Relationship_to_Subscriber_Code_Labe valuel is null'),Relationship_to_Subscriber_Code_Label)`

### Notes

- Target columns with no connector: `demo_target2`: (none); `demo_target21`: (none)

### Target instance `demo_target2` (table `demo_target2`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| demo_target2 | Title | RTRTRANS.Title1 [router group NEWGROUP1 WHERE ISNULL(Social_Security_Number)] → EXPTRANS.Title → SQ_demo_source2.Title = demo_source2.Title [SQL override position 1] | demo_source2.Title |
| demo_target2 | Gender | RTRTRANS.Gender_Code1 [router group NEWGROUP1 WHERE ISNULL(Social_Security_Number)] → EXPTRANS.Gender_Code → SQ_demo_source2.Gender_Code = demo_source2.Gender_Code [SQL override position 8] | demo_source2.Gender_Code |
| demo_target2 | First_Name | RTRTRANS.First_Name1 [router group NEWGROUP1 WHERE ISNULL(Social_Security_Number)] → EXPTRANS.First_Name → SQ_demo_source2.First_Name = demo_source2.First_Name [SQL override position 2] | demo_source2.First_Name |
| demo_target2 | Middle_Name | RTRTRANS.Middle_Name1 [router group NEWGROUP1 WHERE ISNULL(Social_Security_Number)] → EXPTRANS.Middle_Name → SQ_demo_source2.Middle_Name = demo_source2.Middle_Name [SQL override position 3] | demo_source2.Middle_Name |
| demo_target2 | Last_Name | RTRTRANS.Last_Name1 [router group NEWGROUP1 WHERE ISNULL(Social_Security_Number)] → EXPTRANS.Last_Name → SQ_demo_source2.Last_Name = demo_source2.Last_Name [SQL override position 4] | demo_source2.Last_Name |
| demo_target2 | Member_Identifier | RTRTRANS.Member_ID1 [router group NEWGROUP1 WHERE ISNULL(Social_Security_Number)] → EXPTRANS.Member_ID → SQ_demo_source2.Member_ID = demo_source2.Member_ID [SQL override position 5] | demo_source2.Member_ID |
| demo_target2 | Member_Suffix | RTRTRANS.Member_Suffix1 [router group NEWGROUP1 WHERE ISNULL(Social_Security_Number)] → EXPTRANS.Member_Suffix → SQ_demo_source2.Member_Suffix = demo_source2.Member_Suffix [SQL override position 6] | demo_source2.Member_Suffix |
| demo_target2 | Date_of_Birth | RTRTRANS.Birth_Date1 [router group NEWGROUP1 WHERE ISNULL(Social_Security_Number)] → EXPTRANS.Birth_Date → SQ_demo_source2.Birth_Date = demo_source2.Birth_Date [SQL override position 7] | demo_source2.Birth_Date |
| demo_target2 | Member_Number | RTRTRANS.Member_Record_Number1 [router group NEWGROUP1 WHERE ISNULL(Social_Security_Number)] → EXPTRANS.Member_Record_Number → SQ_demo_source2.Member_Record_Number = demo_source2.Member_Record_Number [SQL override position 9] | demo_source2.Member_Record_Number |
| demo_target2 | Soc_Number | RTRTRANS.Social_Security_Number1 [router group NEWGROUP1 WHERE ISNULL(Social_Security_Number)] → EXPTRANS.Social_Security_Number → SQ_demo_source2.Social_Security_Number = demo_source2.Social_Security_Number [SQL override position 10] | demo_source2.Social_Security_Number |
| demo_target2 | Type_Code | RTRTRANS.Member_Type_Code1 [router group NEWGROUP1 WHERE ISNULL(Social_Security_Number)] → EXPTRANS.Member_Type_Code → SQ_demo_source2.Member_Type_Code = demo_source2.Member_Type_Code [SQL override position 11] | demo_source2.Member_Type_Code |
| demo_target2 | Relationship_to_Subscriber_Code | RTRTRANS.Relationship_to_Subscriber_Code1 [router group NEWGROUP1 WHERE ISNULL(Social_Security_Number)] → EXPTRANS.Relationship_to_Subscriber_Code → SQ_demo_source2.Relationship_to_Subscriber_Code = demo_source2.Relationship_to_Subscriber_Code [SQL override position 13] | demo_source2.Relationship_to_Subscriber_Code |
| demo_target2 | Relationship_to_Subscriber_Code_Label | RTRTRANS.Relationship_to_Subscriber_Code_Label1 [router group NEWGROUP1 WHERE ISNULL(Social_Security_Number)] → EXPTRANS.o_Relationship_to_Subscriber_Code_Label = iif(ISNULL(Relationship_to_Subscriber_Code_Label),ABORT('Relationship_to_Subscriber_Code_Labe valuel is null'),Relationship_to_Subscriber_Code_Label) → SQ_demo_source2.Relationship_to_Subscriber_Code_Label = demo_source2.Relationship_to_Subscriber_Code_Label [SQL override position 14] | demo_source2.Relationship_to_Subscriber_Code_Label |
| demo_target2 | Effective_Date | RTRTRANS.Original_Effective_Date1 [router group NEWGROUP1 WHERE ISNULL(Social_Security_Number)] → EXPTRANS.Original_Effective_Date → SQ_demo_source2.Original_Effective_Date = demo_source2.Original_Effective_Date [SQL override position 12] | demo_source2.Original_Effective_Date |

### Target instance `demo_target21` (table `demo_target2`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| demo_target21 | Title | RTRTRANS.Title3 [router group NEWGROUP2 WHERE NOT ISNULL(Social_Security_Number)] → EXPTRANS.Title → SQ_demo_source2.Title = demo_source2.Title [SQL override position 1] | demo_source2.Title |
| demo_target21 | Gender | RTRTRANS.Gender_Code3 [router group NEWGROUP2 WHERE NOT ISNULL(Social_Security_Number)] → EXPTRANS.Gender_Code → SQ_demo_source2.Gender_Code = demo_source2.Gender_Code [SQL override position 8] | demo_source2.Gender_Code |
| demo_target21 | First_Name | RTRTRANS.First_Name3 [router group NEWGROUP2 WHERE NOT ISNULL(Social_Security_Number)] → EXPTRANS.First_Name → SQ_demo_source2.First_Name = demo_source2.First_Name [SQL override position 2] | demo_source2.First_Name |
| demo_target21 | Middle_Name | RTRTRANS.Middle_Name3 [router group NEWGROUP2 WHERE NOT ISNULL(Social_Security_Number)] → EXPTRANS.Middle_Name → SQ_demo_source2.Middle_Name = demo_source2.Middle_Name [SQL override position 3] | demo_source2.Middle_Name |
| demo_target21 | Last_Name | RTRTRANS.Last_Name3 [router group NEWGROUP2 WHERE NOT ISNULL(Social_Security_Number)] → EXPTRANS.Last_Name → SQ_demo_source2.Last_Name = demo_source2.Last_Name [SQL override position 4] | demo_source2.Last_Name |
| demo_target21 | Member_Identifier | RTRTRANS.Member_ID3 [router group NEWGROUP2 WHERE NOT ISNULL(Social_Security_Number)] → EXPTRANS.Member_ID → SQ_demo_source2.Member_ID = demo_source2.Member_ID [SQL override position 5] | demo_source2.Member_ID |
| demo_target21 | Member_Suffix | RTRTRANS.Member_Suffix3 [router group NEWGROUP2 WHERE NOT ISNULL(Social_Security_Number)] → EXPTRANS.Member_Suffix → SQ_demo_source2.Member_Suffix = demo_source2.Member_Suffix [SQL override position 6] | demo_source2.Member_Suffix |
| demo_target21 | Date_of_Birth | RTRTRANS.Birth_Date3 [router group NEWGROUP2 WHERE NOT ISNULL(Social_Security_Number)] → EXPTRANS.Birth_Date → SQ_demo_source2.Birth_Date = demo_source2.Birth_Date [SQL override position 7] | demo_source2.Birth_Date |
| demo_target21 | Member_Number | RTRTRANS.Member_Record_Number3 [router group NEWGROUP2 WHERE NOT ISNULL(Social_Security_Number)] → EXPTRANS.Member_Record_Number → SQ_demo_source2.Member_Record_Number = demo_source2.Member_Record_Number [SQL override position 9] | demo_source2.Member_Record_Number |
| demo_target21 | Soc_Number | RTRTRANS.Social_Security_Number3 [router group NEWGROUP2 WHERE NOT ISNULL(Social_Security_Number)] → EXPTRANS.Social_Security_Number → SQ_demo_source2.Social_Security_Number = demo_source2.Social_Security_Number [SQL override position 10] | demo_source2.Social_Security_Number |
| demo_target21 | Type_Code | RTRTRANS.Member_Type_Code3 [router group NEWGROUP2 WHERE NOT ISNULL(Social_Security_Number)] → EXPTRANS.Member_Type_Code → SQ_demo_source2.Member_Type_Code = demo_source2.Member_Type_Code [SQL override position 11] | demo_source2.Member_Type_Code |
| demo_target21 | Relationship_to_Subscriber_Code | RTRTRANS.Relationship_to_Subscriber_Code3 [router group NEWGROUP2 WHERE NOT ISNULL(Social_Security_Number)] → EXPTRANS.Relationship_to_Subscriber_Code → SQ_demo_source2.Relationship_to_Subscriber_Code = demo_source2.Relationship_to_Subscriber_Code [SQL override position 13] | demo_source2.Relationship_to_Subscriber_Code |
| demo_target21 | Relationship_to_Subscriber_Code_Label | RTRTRANS.Relationship_to_Subscriber_Code_Label3 [router group NEWGROUP2 WHERE NOT ISNULL(Social_Security_Number)] → EXPTRANS.o_Relationship_to_Subscriber_Code_Label = iif(ISNULL(Relationship_to_Subscriber_Code_Label),ABORT('Relationship_to_Subscriber_Code_Labe valuel is null'),Relationship_to_Subscriber_Code_Label) → SQ_demo_source2.Relationship_to_Subscriber_Code_Label = demo_source2.Relationship_to_Subscriber_Code_Label [SQL override position 14] | demo_source2.Relationship_to_Subscriber_Code_Label |
| demo_target21 | Effective_Date | RTRTRANS.Original_Effective_Date3 [router group NEWGROUP2 WHERE NOT ISNULL(Social_Security_Number)] → EXPTRANS.Original_Effective_Date → SQ_demo_source2.Original_Effective_Date = demo_source2.Original_Effective_Date [SQL override position 12] | demo_source2.Original_Effective_Date |

