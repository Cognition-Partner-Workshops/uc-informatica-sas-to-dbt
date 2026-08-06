# Informatica Source-to-Target Mapping (STM)

Derived deterministically from `legacy/informatica/wf_demo_mapping.XML` by `tools/informatica_lineage.py`.

Business/run date is pinned to **2024-01-31** for all SYSDATE / SYSTIMESTAMP references.

## Mapping `m_demo_mapping1`

- Sources: `demo_source3`, `demo_source4`, `demo_source5`
- Target instances: `demo_target3`, `demo_target5`, `demo_target6`

Physical target instance groups: `demo_target3` = demo_target3; `demo_target5` = demo_target5; `demo_target6` = demo_target6

### Transformation `SEQ_GEN` (Sequence)

- **Start Value**: `1`
- **Increment By**: `1`
- **End Value**: `2147483647`
- **Current Value**: `281`
- **Cycle**: `YES`

### Transformation `SQ_demo_source5` (Source Qualifier)


### Transformation `agg_TRANS` (Aggregator)

- GROUPBY ports: ACCT_ID

### Transformation `lkp_TRANS1` (Lookup Procedure)

- **Lookup table name**: `lkp_demo_source3`
- **Lookup policy on multiple match**: `Use Last Value`
- **Lookup condition**: `ACCT_ID = IN_ACCT_ID`

### Transformation `lkp_TRANS2` (Lookup Procedure)

- **Lookup table name**: `lkp_demo_source1`
- **Lookup policy on multiple match**: `Use Last Value`
- **Lookup condition**: `ACCT_ID = IN_ACCT_ID`

### Transformation `lkp_TRANS3` (Lookup Procedure)

- **Lookup table name**: `lkp_demo_source2`
- **Lookup policy on multiple match**: `Use Last Value`
- **Lookup condition**: `CUST_ID = IN_CUST_ID`

### Transformation `rtr_TRANS` (Router)

- Router group `demo_target6_GRP`: `ACCT_TYP = 'SB'`
- Router group `demo_target5_GRP`: `ACCT_TYP != 'SB'`
- Router group `DEFAULT1`: `(default group)`

### Transformation `sq_demo_source4` (Source Qualifier)

- **Sql Query**: `SELECT demo_source4.ACCT_ID, demo_source4.ACCT_TYP, demo_source4.ACCT_DESC, demo_source4.CRDT_LN, SYSTIMESTAMP, demo_source4.CLSR_DT, demo_source4.ACCT_STAT_CD, demo_source3.TX_ID, demo_source3.LAST_NM, demo_source3.TX_DTTM, demo_source3.TX_AMT, demo_source3.BAL_AMT, demo_source3.CUST_ID, STRCMP(demo_source4.ACCT_STAT_CD,demo_source3.TX_TYPE_CD) FROM demo_source3 INNER JOIN demo_source4 ON demo_source3.ACCT_ID = demo_source4.ACCT_ID ORDER BY demo_source4.ACCT_ID`

- Lookup `lkp_TRANS1`: table `lkp_demo_source3` (exists in export: **False**), condition `ACCT_ID =  IN_ACCT_ID`, multiple-match policy `Use Last Value`.
- Lookup `lkp_TRANS2`: table `lkp_demo_source1` (exists in export: **False**), condition `ACCT_ID = IN_ACCT_ID`, multiple-match policy `Use Last Value`.
- Lookup `lkp_TRANS3`: table `lkp_demo_source2` (exists in export: **False**), condition `CUST_ID = IN_CUST_ID`, multiple-match policy `Use Last Value`.
- SQL override `sq_demo_source4` positional bindings: 1 → `ACCT_ID` = `demo_source4.ACCT_ID`; 2 → `ACCT_TYP` = `demo_source4.ACCT_TYP`; 3 → `ACCT_DESC` = `demo_source4.ACCT_DESC`; 4 → `CRDT_LN` = `demo_source4.CRDT_LN`; 5 → `CR8_DT` = `SYSTIMESTAMP`; 6 → `CLSR_DT` = `demo_source4.CLSR_DT`; 7 → `ACCT_STAT_CD` = `demo_source4.ACCT_STAT_CD`; 8 → `TX_ID` = `demo_source3.TX_ID`; 9 → `LAST_NM` = `demo_source3.LAST_NM`; 10 → `TX_DTTM` = `demo_source3.TX_DTTM`; 11 → `TX_AMT` = `demo_source3.TX_AMT`; 12 → `BAL_AMT` = `demo_source3.BAL_AMT`; 13 → `CUST_ID` = `demo_source3.CUST_ID`; 14 → `TX_TYPE_CD` = `STRCMP(demo_source4.ACCT_STAT_CD,demo_source3.TX_TYPE_CD)`
- Unconnected lookup call `exp_TRANS.o_ACCT_ID`: `:LKP.lkp_TRANS1(ACCT_ID)`.
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
| demo_target5 | ACCT_ID | rtr_TRANS.ACCT_ID2 [router group demo_target5_GRP WHERE ACCT_TYP != 'SB'] → exp_TRANS1.ACCT_ID → exp_TRANS.ACCT_ID → sq_demo_source4.ACCT_ID → demo_source4.ACCT_ID | demo_source4.ACCT_ID |
| demo_target5 | FIRST_NM | rtr_TRANS.FIRST_NM2 [router group demo_target5_GRP WHERE ACCT_TYP != 'SB'] → exp_TRANS1.FIRST_NM → lkp_TRANS2.FIRST_NM [lookup lkp_demo_source1.FIRST_NM ON ACCT_ID = IN_ACCT_ID] | demo_source4.ACCT_ID (lookup key); lkp_demo_source1.FIRST_NM (lookup) |
| demo_target5 | LAST_NM | rtr_TRANS.LAST_NM2 [router group demo_target5_GRP WHERE ACCT_TYP != 'SB'] → exp_TRANS1.LAST_NM → exp_TRANS.LAST_NM → sq_demo_source4.LAST_NM → demo_source3.LAST_NM | demo_source3.LAST_NM |
| demo_target5 | BAL_AMT | rtr_TRANS.BAL_AMT2 [router group demo_target5_GRP WHERE ACCT_TYP != 'SB'] → exp_TRANS1.BAL_AMT → exp_TRANS.BAL_AMT → sq_demo_source4.BAL_AMT → demo_source3.BAL_AMT | demo_source3.BAL_AMT |
| demo_target5 | CRDT_SCORE | rtr_TRANS.CRDT_SCORE2 [router group demo_target5_GRP WHERE ACCT_TYP != 'SB'] → exp_TRANS1.CRDT_SCORE → lkp_TRANS3.CRDT_SCORE [lookup lkp_demo_source2.CRDT_SCORE ON CUST_ID = IN_CUST_ID] | demo_source3.CUST_ID (lookup key); lkp_demo_source2.CRDT_SCORE (lookup) |

### Target instance `demo_target6` (table `demo_target6`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| demo_target6 | ACCT_ID | agg_TRANS.ACCT_ID → rtr_TRANS.ACCT_ID1 [router group demo_target6_GRP WHERE ACCT_TYP = 'SB'] → exp_TRANS1.ACCT_ID → exp_TRANS.ACCT_ID → sq_demo_source4.ACCT_ID → demo_source4.ACCT_ID | demo_source4.ACCT_ID |
| demo_target6 | ACCT_TYP | agg_TRANS.o_acc_trim → rtr_TRANS.o_acc_trim1 [router group demo_target6_GRP WHERE ACCT_TYP = 'SB'] → exp_TRANS1.o_acc_trim → exp_TRANS.o_acc_trim = RTRIM(ACCT_TYP) → sq_demo_source4.ACCT_TYP → demo_source4.ACCT_TYP | demo_source4.ACCT_TYP |
| demo_target6 | ACCT_DESC | agg_TRANS.o_ACCT_DESC → rtr_TRANS.o_ACCT_DESC1 [router group demo_target6_GRP WHERE ACCT_TYP = 'SB'] → exp_TRANS1.o_ACCT_DESC = RTRIM(ACCT_DESC) → exp_TRANS.ACCT_DESC → sq_demo_source4.ACCT_DESC → demo_source4.ACCT_DESC | demo_source4.ACCT_DESC |
| demo_target6 | CR8_DT | agg_TRANS.CR8_DT → rtr_TRANS.CR8_DT1 [router group demo_target6_GRP WHERE ACCT_TYP = 'SB'] → exp_TRANS1.CR8_DT → exp_TRANS.CR8_DT → sq_demo_source4.CR8_DT → demo_source4.CR8_DT | demo_source4.CR8_DT |
| demo_target6 | CRDT_LN | agg_TRANS.o_crdt_trim → rtr_TRANS.o_crdt_trim1 [router group demo_target6_GRP WHERE ACCT_TYP = 'SB'] → exp_TRANS1.o_crdt_trim → exp_TRANS.o_crdt_trim = LTRIM(CRDT_LN) → sq_demo_source4.CRDT_LN → demo_source4.CRDT_LN | demo_source4.CRDT_LN |
| demo_target6 | CLSR_DT | agg_TRANS.CLSR_DT → rtr_TRANS.CLSR_DT1 [router group demo_target6_GRP WHERE ACCT_TYP = 'SB'] → exp_TRANS1.CLSR_DT → exp_TRANS.CLSR_DT → sq_demo_source4.CLSR_DT → demo_source4.CLSR_DT | demo_source4.CLSR_DT |
| demo_target6 | ACCT_STAT_CD | agg_TRANS.ACCT_STAT_CD → rtr_TRANS.ACCT_STAT_CD1 [router group demo_target6_GRP WHERE ACCT_TYP = 'SB'] → exp_TRANS1.ACCT_STAT_CD → exp_TRANS.ACCT_STAT_CD → sq_demo_source4.ACCT_STAT_CD → demo_source4.ACCT_STAT_CD | demo_source4.ACCT_STAT_CD |
| demo_target6 | TX_ID | agg_TRANS.TX_ID → rtr_TRANS.TX_ID1 [router group demo_target6_GRP WHERE ACCT_TYP = 'SB'] → exp_TRANS1.TX_ID → exp_TRANS.TX_ID → sq_demo_source4.TX_ID → demo_source3.TX_ID | demo_source3.TX_ID |
| demo_target6 | ACCT_KEY | SEQ_GEN.NEXTVAL [sequence start=1 increment=1 current=281 cycle=YES] | SEQ_GEN (generated) |
| demo_target6 | TX_DTTM | agg_TRANS.TX_DTTM → rtr_TRANS.TX_DTTM1 [router group demo_target6_GRP WHERE ACCT_TYP = 'SB'] → exp_TRANS1.TX_DTTM → exp_TRANS.TX_DTTM → sq_demo_source4.TX_DTTM → demo_source3.TX_DTTM | demo_source3.TX_DTTM |
| demo_target6 | TX_AMT | agg_TRANS.o_TX_AMT = SUM(TX_AMT) → rtr_TRANS.TX_AMT1 [router group demo_target6_GRP WHERE ACCT_TYP = 'SB'] → exp_TRANS1.TX_AMT → exp_TRANS.TX_AMT → sq_demo_source4.TX_AMT → demo_source3.TX_AMT | demo_source3.TX_AMT |
| demo_target6 | TX_TYPE_CD | agg_TRANS.o_ACCT_ID → rtr_TRANS.o_ACCT_ID1 [router group demo_target6_GRP WHERE ACCT_TYP = 'SB'] → exp_TRANS1.o_ACCT_ID → exp_TRANS.o_ACCT_ID = :LKP.lkp_TRANS1(ACCT_ID) → sq_demo_source4.ACCT_ID → demo_source4.ACCT_ID | demo_source4.ACCT_ID |

## Mapping `m_demo_mapping2`

- Sources: `demo_source1`
- Target instances: `demo_target1_INS`, `demo_target1_UPD`

Physical target instance groups: `demo_target1` = demo_target1_INS, demo_target1_UPD

### Transformation `LKPTRANS` (Lookup Procedure)

- **Lookup table name**: `demo_target1`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `ID = ID1`

### Transformation `RTRTRANS` (Router)

- Router group `Insert`: `New_Flag='Insert'`
- Router group `DEFAULT1`: `(default group)`
- Router group `Update`: `Changed_Flag='Update'`

### Transformation `SEQTRANS` (Sequence)

- **Start Value**: `0`
- **Increment By**: `1`
- **End Value**: `9223372036854775807`
- **Current Value**: `57`
- **Cycle**: `NO`

### Transformation `SQ_demo_source1` (Source Qualifier)


### Transformation `UPDTRANS` (Update Strategy)

- **Update Strategy Expression**: `DD_UPDATE`
- **Forward Rejected Rows**: `YES`

- Lookup `LKPTRANS`: table `demo_target1` (exists in export: **True**), condition `ID = ID1`, multiple-match policy `Use Any Value`.
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

### Transformation `RTRTRANS` (Router)

- Router group `NEWGROUP1`: `ISNULL(Social_Security_Number)`
- Router group `DEFAULT1`: `(default group)`
- Router group `NEWGROUP2`: `NOT ISNULL(Social_Security_Number)`

### Transformation `SQ_demo_source2` (Source Qualifier)

- **Sql Query**: `SELECT demo_source2.Title, demo_source2.First_Name, demo_source2.Middle_Name, demo_source2.Last_Name, demo_source2.Member_ID, demo_source2.Member_Suffix, demo_source2.Birth_Date, demo_source2.Gender_Code, demo_source2.Member_Record_Number, demo_source2.Social_Security_Number, demo_source2.Member_Type_Code, demo_source2.Original_Effective_Date, demo_source2.Relationship_to_Subscriber_Code, demo_source2.Relationship_to_Subscriber_Code_Label FROM demo_source2 where demo_source2.Member_Type_Code is not null`

- SQL override `SQ_demo_source2` positional bindings: 1 → `Title` = `demo_source2.Title`; 2 → `First_Name` = `demo_source2.First_Name`; 3 → `Middle_Name` = `demo_source2.Middle_Name`; 4 → `Last_Name` = `demo_source2.Last_Name`; 5 → `Member_ID` = `demo_source2.Member_ID`; 6 → `Member_Suffix` = `demo_source2.Member_Suffix`; 7 → `Birth_Date` = `demo_source2.Birth_Date`; 8 → `Gender_Code` = `demo_source2.Gender_Code`; 9 → `Member_Record_Number` = `demo_source2.Member_Record_Number`; 10 → `Social_Security_Number` = `demo_source2.Social_Security_Number`; 11 → `Member_Type_Code` = `demo_source2.Member_Type_Code`; 12 → `Original_Effective_Date` = `demo_source2.Original_Effective_Date`; 13 → `Relationship_to_Subscriber_Code` = `demo_source2.Relationship_to_Subscriber_Code`; 14 → `Relationship_to_Subscriber_Code_Label` = `demo_source2.Relationship_to_Subscriber_Code_Label`
- Target columns with no connector: `demo_target2`: (none); `demo_target21`: (none)

### Target instance `demo_target2` (table `demo_target2`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| demo_target2 | Title | RTRTRANS.Title1 [router group NEWGROUP1 WHERE ISNULL(Social_Security_Number)] → EXPTRANS.Title → SQ_demo_source2.Title → demo_source2.Title | demo_source2.Title |
| demo_target2 | Gender | RTRTRANS.Gender_Code1 [router group NEWGROUP1 WHERE ISNULL(Social_Security_Number)] → EXPTRANS.Gender_Code → SQ_demo_source2.Gender_Code → demo_source2.Gender_Code | demo_source2.Gender_Code |
| demo_target2 | First_Name | RTRTRANS.First_Name1 [router group NEWGROUP1 WHERE ISNULL(Social_Security_Number)] → EXPTRANS.First_Name → SQ_demo_source2.First_Name → demo_source2.First_Name | demo_source2.First_Name |
| demo_target2 | Middle_Name | RTRTRANS.Middle_Name1 [router group NEWGROUP1 WHERE ISNULL(Social_Security_Number)] → EXPTRANS.Middle_Name → SQ_demo_source2.Middle_Name → demo_source2.Middle_Name | demo_source2.Middle_Name |
| demo_target2 | Last_Name | RTRTRANS.Last_Name1 [router group NEWGROUP1 WHERE ISNULL(Social_Security_Number)] → EXPTRANS.Last_Name → SQ_demo_source2.Last_Name → demo_source2.Last_Name | demo_source2.Last_Name |
| demo_target2 | Member_Identifier | RTRTRANS.Member_ID1 [router group NEWGROUP1 WHERE ISNULL(Social_Security_Number)] → EXPTRANS.Member_ID → SQ_demo_source2.Member_ID → demo_source2.Member_ID | demo_source2.Member_ID |
| demo_target2 | Member_Suffix | RTRTRANS.Member_Suffix1 [router group NEWGROUP1 WHERE ISNULL(Social_Security_Number)] → EXPTRANS.Member_Suffix → SQ_demo_source2.Member_Suffix → demo_source2.Member_Suffix | demo_source2.Member_Suffix |
| demo_target2 | Date_of_Birth | RTRTRANS.Birth_Date1 [router group NEWGROUP1 WHERE ISNULL(Social_Security_Number)] → EXPTRANS.Birth_Date → SQ_demo_source2.Birth_Date → demo_source2.Birth_Date | demo_source2.Birth_Date |
| demo_target2 | Member_Number | RTRTRANS.Member_Record_Number1 [router group NEWGROUP1 WHERE ISNULL(Social_Security_Number)] → EXPTRANS.Member_Record_Number → SQ_demo_source2.Member_Record_Number → demo_source2.Member_Record_Number | demo_source2.Member_Record_Number |
| demo_target2 | Soc_Number | RTRTRANS.Social_Security_Number1 [router group NEWGROUP1 WHERE ISNULL(Social_Security_Number)] → EXPTRANS.Social_Security_Number → SQ_demo_source2.Social_Security_Number → demo_source2.Social_Security_Number | demo_source2.Social_Security_Number |
| demo_target2 | Type_Code | RTRTRANS.Member_Type_Code1 [router group NEWGROUP1 WHERE ISNULL(Social_Security_Number)] → EXPTRANS.Member_Type_Code → SQ_demo_source2.Member_Type_Code → demo_source2.Member_Type_Code | demo_source2.Member_Type_Code |
| demo_target2 | Relationship_to_Subscriber_Code | RTRTRANS.Relationship_to_Subscriber_Code1 [router group NEWGROUP1 WHERE ISNULL(Social_Security_Number)] → EXPTRANS.Relationship_to_Subscriber_Code → SQ_demo_source2.Relationship_to_Subscriber_Code → demo_source2.Relationship_to_Subscriber_Code | demo_source2.Relationship_to_Subscriber_Code |
| demo_target2 | Relationship_to_Subscriber_Code_Label | RTRTRANS.Relationship_to_Subscriber_Code_Label1 [router group NEWGROUP1 WHERE ISNULL(Social_Security_Number)] → EXPTRANS.o_Relationship_to_Subscriber_Code_Label = iif(ISNULL(Relationship_to_Subscriber_Code_Label),ABORT('Relationship_to_Subscriber_Code_Labe valuel is null'),Relationship_to_Subscriber_Code_Label) → SQ_demo_source2.Relationship_to_Subscriber_Code_Label → demo_source2.Relationship_to_Subscriber_Code_Label | demo_source2.Relationship_to_Subscriber_Code_Label |
| demo_target2 | Effective_Date | RTRTRANS.Original_Effective_Date1 [router group NEWGROUP1 WHERE ISNULL(Social_Security_Number)] → EXPTRANS.Original_Effective_Date → SQ_demo_source2.Original_Effective_Date → demo_source2.Original_Effective_Date | demo_source2.Original_Effective_Date |

### Target instance `demo_target21` (table `demo_target2`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| demo_target21 | Title | RTRTRANS.Title3 [router group NEWGROUP2 WHERE NOT ISNULL(Social_Security_Number)] → EXPTRANS.Title → SQ_demo_source2.Title → demo_source2.Title | demo_source2.Title |
| demo_target21 | Gender | RTRTRANS.Gender_Code3 [router group NEWGROUP2 WHERE NOT ISNULL(Social_Security_Number)] → EXPTRANS.Gender_Code → SQ_demo_source2.Gender_Code → demo_source2.Gender_Code | demo_source2.Gender_Code |
| demo_target21 | First_Name | RTRTRANS.First_Name3 [router group NEWGROUP2 WHERE NOT ISNULL(Social_Security_Number)] → EXPTRANS.First_Name → SQ_demo_source2.First_Name → demo_source2.First_Name | demo_source2.First_Name |
| demo_target21 | Middle_Name | RTRTRANS.Middle_Name3 [router group NEWGROUP2 WHERE NOT ISNULL(Social_Security_Number)] → EXPTRANS.Middle_Name → SQ_demo_source2.Middle_Name → demo_source2.Middle_Name | demo_source2.Middle_Name |
| demo_target21 | Last_Name | RTRTRANS.Last_Name3 [router group NEWGROUP2 WHERE NOT ISNULL(Social_Security_Number)] → EXPTRANS.Last_Name → SQ_demo_source2.Last_Name → demo_source2.Last_Name | demo_source2.Last_Name |
| demo_target21 | Member_Identifier | RTRTRANS.Member_ID3 [router group NEWGROUP2 WHERE NOT ISNULL(Social_Security_Number)] → EXPTRANS.Member_ID → SQ_demo_source2.Member_ID → demo_source2.Member_ID | demo_source2.Member_ID |
| demo_target21 | Member_Suffix | RTRTRANS.Member_Suffix3 [router group NEWGROUP2 WHERE NOT ISNULL(Social_Security_Number)] → EXPTRANS.Member_Suffix → SQ_demo_source2.Member_Suffix → demo_source2.Member_Suffix | demo_source2.Member_Suffix |
| demo_target21 | Date_of_Birth | RTRTRANS.Birth_Date3 [router group NEWGROUP2 WHERE NOT ISNULL(Social_Security_Number)] → EXPTRANS.Birth_Date → SQ_demo_source2.Birth_Date → demo_source2.Birth_Date | demo_source2.Birth_Date |
| demo_target21 | Member_Number | RTRTRANS.Member_Record_Number3 [router group NEWGROUP2 WHERE NOT ISNULL(Social_Security_Number)] → EXPTRANS.Member_Record_Number → SQ_demo_source2.Member_Record_Number → demo_source2.Member_Record_Number | demo_source2.Member_Record_Number |
| demo_target21 | Soc_Number | RTRTRANS.Social_Security_Number3 [router group NEWGROUP2 WHERE NOT ISNULL(Social_Security_Number)] → EXPTRANS.Social_Security_Number → SQ_demo_source2.Social_Security_Number → demo_source2.Social_Security_Number | demo_source2.Social_Security_Number |
| demo_target21 | Type_Code | RTRTRANS.Member_Type_Code3 [router group NEWGROUP2 WHERE NOT ISNULL(Social_Security_Number)] → EXPTRANS.Member_Type_Code → SQ_demo_source2.Member_Type_Code → demo_source2.Member_Type_Code | demo_source2.Member_Type_Code |
| demo_target21 | Relationship_to_Subscriber_Code | RTRTRANS.Relationship_to_Subscriber_Code3 [router group NEWGROUP2 WHERE NOT ISNULL(Social_Security_Number)] → EXPTRANS.Relationship_to_Subscriber_Code → SQ_demo_source2.Relationship_to_Subscriber_Code → demo_source2.Relationship_to_Subscriber_Code | demo_source2.Relationship_to_Subscriber_Code |
| demo_target21 | Relationship_to_Subscriber_Code_Label | RTRTRANS.Relationship_to_Subscriber_Code_Label3 [router group NEWGROUP2 WHERE NOT ISNULL(Social_Security_Number)] → EXPTRANS.o_Relationship_to_Subscriber_Code_Label = iif(ISNULL(Relationship_to_Subscriber_Code_Label),ABORT('Relationship_to_Subscriber_Code_Labe valuel is null'),Relationship_to_Subscriber_Code_Label) → SQ_demo_source2.Relationship_to_Subscriber_Code_Label → demo_source2.Relationship_to_Subscriber_Code_Label | demo_source2.Relationship_to_Subscriber_Code_Label |
| demo_target21 | Effective_Date | RTRTRANS.Original_Effective_Date3 [router group NEWGROUP2 WHERE NOT ISNULL(Social_Security_Number)] → EXPTRANS.Original_Effective_Date → SQ_demo_source2.Original_Effective_Date → demo_source2.Original_Effective_Date | demo_source2.Original_Effective_Date |
