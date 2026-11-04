# m_demo_mapping2 — Source-to-target mapping

Derived by `tools/informatica_lineage.py`, scoped to this mapping.

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
