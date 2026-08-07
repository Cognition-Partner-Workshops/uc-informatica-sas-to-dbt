# Connector-derived Informatica lineage

All cross-instance hops below come from XML `CONNECTOR` edges; port names are never used to infer them.

## Mapping `m_demo_mapping1`

SQL override for `sq_demo_source4`:

- Select items bound to an unconnected output port: `STRCMP(demo_source4.ACCT_STAT_CD,demo_source3.TX_TYPE_CD)`

### Target instance `demo_target3`

| target column | source column(s) | path | transformation applied | xml lines |
|---|---|---|---|---|
| `PRODUCT_ID` | demo_source5.PRODUCT_ID | exp_TRANS2.PRODUCT_ID → exp_TRANS2.PRODUCT_ID → SQ_demo_source5.PRODUCT_ID → SQ_demo_source5.PRODUCT_ID → demo_source5.PRODUCT_ID → demo_source5.PRODUCT_ID | — | 799, 879, 887 |
| `PRODUCT_NM` | demo_source5.PRODUCT_NM | exp_TRANS2.PRODUCT_NM → exp_TRANS2.PRODUCT_NM → SQ_demo_source5.PRODUCT_NM → SQ_demo_source5.PRODUCT_NM → demo_source5.PRODUCT_NM → demo_source5.PRODUCT_NM | — | 801, 880, 888 |
| `PRODUCT_NO` | demo_source5.PRODUCT_NO | exp_TRANS2.PRODUCT_NO → exp_TRANS2.PRODUCT_NO → SQ_demo_source5.PRODUCT_NO → SQ_demo_source5.PRODUCT_NO → demo_source5.PRODUCT_NO → demo_source5.PRODUCT_NO | — | 800, 881, 889 |
| `COLOR` | demo_source5.COLOR | exp_TRANS2.COLOR → exp_TRANS2.COLOR → SQ_demo_source5.COLOR → SQ_demo_source5.COLOR → demo_source5.COLOR → demo_source5.COLOR | — | 803, 882, 890 |
| `STD_COST` | demo_source5.STD_COST | exp_TRANS2.STD_COST → exp_TRANS2.STD_COST → SQ_demo_source5.STD_COST → SQ_demo_source5.STD_COST → demo_source5.STD_COST → demo_source5.STD_COST | — | 802, 883, 891 |
| `LIST_PRICE` | demo_source5.LIST_PRICE | exp_TRANS2.LIST_PRICE → exp_TRANS2.LIST_PRICE → SQ_demo_source5.LIST_PRICE → SQ_demo_source5.LIST_PRICE → demo_source5.LIST_PRICE → demo_source5.LIST_PRICE | — | 804, 884, 892 |
| `SELL_ST_DT` | NULL | exp_TRANS2.o_SELL_ST_DT → exp_TRANS2.o_SELL_ST_DT → exp_TRANS2.TO_DATE(TO_CHAR(SYSDATE),'DD/MM/YYYY') | TO_DATE(TO_CHAR(SYSDATE),'DD/MM/YYYY') | 662, 805 |
| `SELL_ED_DT` | demo_source5.SELL_ED_DT | exp_TRANS2.o_SELL_ED_DT → exp_TRANS2.o_SELL_ED_DT → SQ_demo_source5.SELL_ED_DT → SQ_demo_source5.SELL_ED_DT → demo_source5.SELL_ED_DT → demo_source5.SELL_ED_DT | TO_DATE(SELL_ED_DT,'DD/MM/YYYY') | 663, 806, 886, 894 |

### Target instance `demo_target5`

| target column | source column(s) | path | transformation applied | xml lines |
|---|---|---|---|---|
| `ACCT_ID` | demo_source4.ACCT_ID | rtr_TRANS.ACCT_ID2 → rtr_TRANS.ACCT_ID2 → exp_TRANS1.ACCT_ID → exp_TRANS1.ACCT_ID → exp_TRANS.ACCT_ID → exp_TRANS.ACCT_ID → sq_demo_source4.ACCT_ID → sq_demo_source4.ACCT_ID → demo_source4.ACCT_ID → demo_source4.ACCT_ID | ACCT_TYP != 'SB'; demo_source4.ACCT_ID | 580, 669, 795, 827, 841, 852, 875 |
| `FIRST_NM` | lkp_demo_source1.FIRST_NM | rtr_TRANS.FIRST_NM2 → rtr_TRANS.FIRST_NM2 → exp_TRANS1.FIRST_NM → exp_TRANS1.FIRST_NM → lkp_TRANS2.FIRST_NM → lkp_TRANS2.FIRST_NM → lkp_demo_source1.FIRST_NM | ACCT_TYP != 'SB' | 669, 797, 832, 848 |
| `LAST_NM` | demo_source3.LAST_NM | rtr_TRANS.LAST_NM2 → rtr_TRANS.LAST_NM2 → exp_TRANS1.LAST_NM → exp_TRANS1.LAST_NM → exp_TRANS.LAST_NM → exp_TRANS.LAST_NM → sq_demo_source4.LAST_NM → sq_demo_source4.LAST_NM → demo_source3.LAST_NM → demo_source3.LAST_NM | ACCT_TYP != 'SB'; demo_source3.LAST_NM | 580, 669, 796, 825, 839, 858, 873 |
| `BAL_AMT` | demo_source3.BAL_AMT | rtr_TRANS.BAL_AMT2 → rtr_TRANS.BAL_AMT2 → exp_TRANS1.BAL_AMT → exp_TRANS1.BAL_AMT → exp_TRANS.BAL_AMT → exp_TRANS.BAL_AMT → sq_demo_source4.BAL_AMT → sq_demo_source4.BAL_AMT → demo_source3.BAL_AMT → demo_source3.BAL_AMT | ACCT_TYP != 'SB'; demo_source3.BAL_AMT | 580, 669, 798, 820, 840, 862, 868 |
| `CRDT_SCORE` | lkp_demo_source2.CRDT_SCORE | rtr_TRANS.CRDT_SCORE2 → rtr_TRANS.CRDT_SCORE2 → exp_TRANS1.CRDT_SCORE → exp_TRANS1.CRDT_SCORE → lkp_TRANS3.CRDT_SCORE → lkp_TRANS3.CRDT_SCORE → lkp_demo_source2.CRDT_SCORE | ACCT_TYP != 'SB' | 669, 794, 833, 849 |

### Target instance `demo_target6`

| target column | source column(s) | path | transformation applied | xml lines |
|---|---|---|---|---|
| `ACCT_ID` | demo_source4.ACCT_ID | agg_TRANS.ACCT_ID → agg_TRANS.ACCT_ID → rtr_TRANS.ACCT_ID1 → rtr_TRANS.ACCT_ID1 → exp_TRANS1.ACCT_ID → exp_TRANS1.ACCT_ID → exp_TRANS.ACCT_ID → exp_TRANS.ACCT_ID → sq_demo_source4.ACCT_ID → sq_demo_source4.ACCT_ID → demo_source4.ACCT_ID → demo_source4.ACCT_ID | ACCT_TYP = 'SB'; demo_source4.ACCT_ID | 580, 668, 790, 817, 827, 841, 852, 875 |
| `ACCT_TYP` | demo_source4.ACCT_TYP | agg_TRANS.o_acc_trim → agg_TRANS.o_acc_trim → rtr_TRANS.o_acc_trim1 → rtr_TRANS.o_acc_trim1 → exp_TRANS1.o_acc_trim → exp_TRANS1.o_acc_trim → exp_TRANS.o_acc_trim → exp_TRANS.o_acc_trim → sq_demo_source4.ACCT_TYP → sq_demo_source4.ACCT_TYP → demo_source4.ACCT_TYP → demo_source4.ACCT_TYP | ACCT_TYP = 'SB'; RTRIM(ACCT_TYP); demo_source4.ACCT_TYP | 580, 606, 668, 787, 816, 829, 834, 853, 870 |
| `ACCT_DESC` | demo_source4.ACCT_DESC | agg_TRANS.o_ACCT_DESC → agg_TRANS.o_ACCT_DESC → rtr_TRANS.o_ACCT_DESC1 → rtr_TRANS.o_ACCT_DESC1 → exp_TRANS1.o_ACCT_DESC → exp_TRANS1.o_ACCT_DESC → exp_TRANS.ACCT_DESC → exp_TRANS.ACCT_DESC → sq_demo_source4.ACCT_DESC → sq_demo_source4.ACCT_DESC → demo_source4.ACCT_DESC → demo_source4.ACCT_DESC | ACCT_TYP = 'SB'; RTRIM(ACCT_DESC); demo_source4.ACCT_DESC | 479, 580, 668, 793, 807, 821, 845, 854, 869 |
| `CR8_DT` | NULL | agg_TRANS.CR8_DT → agg_TRANS.CR8_DT → rtr_TRANS.CR8_DT1 → rtr_TRANS.CR8_DT1 → exp_TRANS1.CR8_DT → exp_TRANS1.CR8_DT → exp_TRANS.CR8_DT → exp_TRANS.CR8_DT → sq_demo_source4.CR8_DT → sq_demo_source4.CR8_DT → sq_demo_source4.SYSTIMESTAMP | ACCT_TYP = 'SB'; SYSTIMESTAMP | 580, 668, 792, 814, 828, 846, 876 |
| `CRDT_LN` | demo_source4.CRDT_LN | agg_TRANS.o_crdt_trim → agg_TRANS.o_crdt_trim → rtr_TRANS.o_crdt_trim1 → rtr_TRANS.o_crdt_trim1 → exp_TRANS1.o_crdt_trim → exp_TRANS1.o_crdt_trim → exp_TRANS.o_crdt_trim → exp_TRANS.o_crdt_trim → sq_demo_source4.CRDT_LN → sq_demo_source4.CRDT_LN → demo_source4.CRDT_LN → demo_source4.CRDT_LN | ACCT_TYP = 'SB'; LTRIM(CRDT_LN); demo_source4.CRDT_LN | 580, 607, 668, 788, 809, 830, 847, 855, 865 |
| `CLSR_DT` | demo_source4.CLSR_DT | agg_TRANS.CLSR_DT → agg_TRANS.CLSR_DT → rtr_TRANS.CLSR_DT1 → rtr_TRANS.CLSR_DT1 → exp_TRANS1.CLSR_DT → exp_TRANS1.CLSR_DT → exp_TRANS.CLSR_DT → exp_TRANS.CLSR_DT → sq_demo_source4.CLSR_DT → sq_demo_source4.CLSR_DT → demo_source4.CLSR_DT → demo_source4.CLSR_DT | ACCT_TYP = 'SB'; demo_source4.CLSR_DT | 580, 668, 789, 810, 818, 843, 863, 866 |
| `ACCT_STAT_CD` | demo_source4.ACCT_STAT_CD | agg_TRANS.ACCT_STAT_CD → agg_TRANS.ACCT_STAT_CD → rtr_TRANS.ACCT_STAT_CD1 → rtr_TRANS.ACCT_STAT_CD1 → exp_TRANS1.ACCT_STAT_CD → exp_TRANS1.ACCT_STAT_CD → exp_TRANS.ACCT_STAT_CD → exp_TRANS.ACCT_STAT_CD → sq_demo_source4.ACCT_STAT_CD → sq_demo_source4.ACCT_STAT_CD → demo_source4.ACCT_STAT_CD → demo_source4.ACCT_STAT_CD | ACCT_TYP = 'SB'; demo_source4.ACCT_STAT_CD | 580, 668, 783, 812, 823, 844, 864, 871 |
| `TX_ID` | demo_source3.TX_ID | agg_TRANS.TX_ID → agg_TRANS.TX_ID → rtr_TRANS.TX_ID1 → rtr_TRANS.TX_ID1 → exp_TRANS1.TX_ID → exp_TRANS1.TX_ID → exp_TRANS.TX_ID → exp_TRANS.TX_ID → sq_demo_source4.TX_ID → sq_demo_source4.TX_ID → demo_source3.TX_ID → demo_source3.TX_ID | ACCT_TYP = 'SB'; demo_source3.TX_ID | 580, 668, 784, 811, 824, 836, 857, 872 |
| `ACCT_KEY` | NULL | SEQ_GEN.NEXTVAL → SEQ_GEN.NEXTVAL | — | 785 |
| `TX_DTTM` | demo_source3.TX_DTTM | agg_TRANS.TX_DTTM → agg_TRANS.TX_DTTM → rtr_TRANS.TX_DTTM1 → rtr_TRANS.TX_DTTM1 → exp_TRANS1.TX_DTTM → exp_TRANS1.TX_DTTM → exp_TRANS.TX_DTTM → exp_TRANS.TX_DTTM → sq_demo_source4.TX_DTTM → sq_demo_source4.TX_DTTM → demo_source3.TX_DTTM → demo_source3.TX_DTTM | ACCT_TYP = 'SB'; demo_source3.TX_DTTM | 580, 668, 782, 813, 819, 835, 859, 867 |
| `TX_AMT` | demo_source3.TX_AMT | agg_TRANS.o_TX_AMT → agg_TRANS.o_TX_AMT → rtr_TRANS.TX_AMT1 → rtr_TRANS.TX_AMT1 → exp_TRANS1.TX_AMT → exp_TRANS1.TX_AMT → exp_TRANS.TX_AMT → exp_TRANS.TX_AMT → sq_demo_source4.TX_AMT → sq_demo_source4.TX_AMT → demo_source3.TX_AMT → demo_source3.TX_AMT | ACCT_TYP = 'SB'; SUM(TX_AMT); demo_source3.TX_AMT | 454, 580, 668, 791, 808, 826, 838, 860, 874 |
| `TX_TYPE_CD` | demo_source4.ACCT_ID, lkp_demo_source3.TX_TYPE_CD | agg_TRANS.o_ACCT_ID → agg_TRANS.o_ACCT_ID → rtr_TRANS.o_ACCT_ID1 → rtr_TRANS.o_ACCT_ID1 → exp_TRANS1.o_ACCT_ID → exp_TRANS1.o_ACCT_ID → exp_TRANS.o_ACCT_ID → exp_TRANS.o_ACCT_ID → lkp_TRANS1.TX_TYPE_CD → lkp_demo_source3.TX_TYPE_CD<br>agg_TRANS.o_ACCT_ID → agg_TRANS.o_ACCT_ID → rtr_TRANS.o_ACCT_ID1 → rtr_TRANS.o_ACCT_ID1 → exp_TRANS1.o_ACCT_ID → exp_TRANS1.o_ACCT_ID → exp_TRANS.o_ACCT_ID → exp_TRANS.o_ACCT_ID → sq_demo_source4.ACCT_ID → sq_demo_source4.ACCT_ID → demo_source4.ACCT_ID → demo_source4.ACCT_ID | :LKP.lkp_TRANS1(ACCT_ID); ACCT_TYP = 'SB'; demo_source4.ACCT_ID | 580, 608, 668, 786, 815, 831, 842, 852, 875 |

## Mapping `m_demo_mapping2`

### Target instance `demo_target1_INS`

| target column | source column(s) | path | transformation applied | xml lines |
|---|---|---|---|---|
| `Key` | NULL | SEQTRANS.NEXTVAL → SEQTRANS.NEXTVAL | — | 373 |
| `LEAD_CO_MNE` | demo_source1.LEAD_CO_MNE | RTRTRANS.LEAD_CO_MNE2 → RTRTRANS.LEAD_CO_MNE2 → EXPTRANS.LEAD_CO_MNE → EXPTRANS.LEAD_CO_MNE → SQ_demo_source1.LEAD_CO_MNE → SQ_demo_source1.LEAD_CO_MNE → demo_source1.LEAD_CO_MNE → demo_source1.LEAD_CO_MNE | New_Flag='Insert' | 188, 365, 374, 380, 393 |
| `BRANCH_CO_MNE` | demo_source1.BRANCH_CO_MNE | RTRTRANS.BRANCH_CO_MNE2 → RTRTRANS.BRANCH_CO_MNE2 → EXPTRANS.BRANCH_CO_MNE → EXPTRANS.BRANCH_CO_MNE → SQ_demo_source1.BRANCH_CO_MNE → SQ_demo_source1.BRANCH_CO_MNE → demo_source1.BRANCH_CO_MNE → demo_source1.BRANCH_CO_MNE | New_Flag='Insert' | 188, 366, 375, 381, 394 |
| `MIS_DATE` | demo_source1.MIS_DATE | RTRTRANS.MIS_DATE2 → RTRTRANS.MIS_DATE2 → EXPTRANS.MIS_DATE → EXPTRANS.MIS_DATE → SQ_demo_source1.MIS_DATE → SQ_demo_source1.MIS_DATE → demo_source1.MIS_DATE → demo_source1.MIS_DATE | New_Flag='Insert' | 188, 367, 376, 382, 410 |
| `ID` | demo_source1.ID | RTRTRANS.ID1 → RTRTRANS.ID1 → EXPTRANS.ID → EXPTRANS.ID → SQ_demo_source1.ID → SQ_demo_source1.ID → demo_source1.ID → demo_source1.ID | New_Flag='Insert' | 188, 368, 377, 383, 395 |
| `DESCRIPTION` | demo_source1.DESCRIPTION | RTRTRANS.DESCRIPTION2 → RTRTRANS.DESCRIPTION2 → EXPTRANS.DESCRIPTION → EXPTRANS.DESCRIPTION → SQ_demo_source1.DESCRIPTION → SQ_demo_source1.DESCRIPTION → demo_source1.DESCRIPTION → demo_source1.DESCRIPTION | New_Flag='Insert' | 188, 369, 378, 384, 396 |
| `SHORT_NAME` | demo_source1.SHORT_NAME | RTRTRANS.SHORT_NAME2 → RTRTRANS.SHORT_NAME2 → EXPTRANS.SHORT_NAME → EXPTRANS.SHORT_NAME → SQ_demo_source1.SHORT_NAME → SQ_demo_source1.SHORT_NAME → demo_source1.SHORT_NAME → demo_source1.SHORT_NAME | New_Flag='Insert' | 188, 370, 379, 385, 397 |
| `CREATED_BY` | NULL | RTRTRANS.o_CREATED_BY1 → RTRTRANS.o_CREATED_BY1 → EXPTRANS.o_CREATED_BY → EXPTRANS.o_CREATED_BY → EXPTRANS.'IDWUSER' | 'IDWUSER'; New_Flag='Insert' | 180, 188, 371, 405 |
| `CREATED_TIME` | NULL | RTRTRANS.o_CREATED_TIME1 → RTRTRANS.o_CREATED_TIME1 → EXPTRANS.o_CREATED_TIME → EXPTRANS.o_CREATED_TIME → EXPTRANS.SYSDATE | New_Flag='Insert'; SYSDATE | 181, 188, 372, 406 |
| `UPDATED_BY` | NULL | — | — | — |
| `UPDATED_TIME` | NULL | — | — | — |
| `ACTIVE_FLAG` | NULL | — | — | — |
| `START_DATE` | NULL | — | — | — |
| `END_DATE` | NULL | — | — | — |

### Target instance `demo_target1_UPD`

| target column | source column(s) | path | transformation applied | xml lines |
|---|---|---|---|---|
| `Key` | demo_target1.Key | UPDTRANS.Key2 → UPDTRANS.Key2 → RTRTRANS.Key3 → RTRTRANS.Key3 → EXPTRANS.Key → EXPTRANS.Key → LKPTRANS.Key → LKPTRANS.Key → demo_target1.Key | Changed_Flag='Update' | 190, 356, 392, 409, 423 |
| `LEAD_CO_MNE` | demo_source1.LEAD_CO_MNE | UPDTRANS.LEAD_CO_MNE3 → UPDTRANS.LEAD_CO_MNE3 → RTRTRANS.LEAD_CO_MNE4 → RTRTRANS.LEAD_CO_MNE4 → EXPTRANS.LEAD_CO_MNE → EXPTRANS.LEAD_CO_MNE → SQ_demo_source1.LEAD_CO_MNE → SQ_demo_source1.LEAD_CO_MNE → demo_source1.LEAD_CO_MNE → demo_source1.LEAD_CO_MNE | Changed_Flag='Update' | 190, 357, 374, 380, 393, 411 |
| `BRANCH_CO_MNE` | demo_source1.BRANCH_CO_MNE | UPDTRANS.BRANCH_CO_MNE3 → UPDTRANS.BRANCH_CO_MNE3 → RTRTRANS.BRANCH_CO_MNE4 → RTRTRANS.BRANCH_CO_MNE4 → EXPTRANS.BRANCH_CO_MNE → EXPTRANS.BRANCH_CO_MNE → SQ_demo_source1.BRANCH_CO_MNE → SQ_demo_source1.BRANCH_CO_MNE → demo_source1.BRANCH_CO_MNE → demo_source1.BRANCH_CO_MNE | Changed_Flag='Update' | 190, 358, 375, 381, 394, 412 |
| `MIS_DATE` | demo_source1.MIS_DATE | UPDTRANS.MIS_DATE3 → UPDTRANS.MIS_DATE3 → RTRTRANS.MIS_DATE4 → RTRTRANS.MIS_DATE4 → EXPTRANS.MIS_DATE → EXPTRANS.MIS_DATE → SQ_demo_source1.MIS_DATE → SQ_demo_source1.MIS_DATE → demo_source1.MIS_DATE → demo_source1.MIS_DATE | Changed_Flag='Update' | 190, 359, 376, 382, 410, 413 |
| `ID` | demo_source1.ID | UPDTRANS.ID2 → UPDTRANS.ID2 → RTRTRANS.ID3 → RTRTRANS.ID3 → EXPTRANS.ID → EXPTRANS.ID → SQ_demo_source1.ID → SQ_demo_source1.ID → demo_source1.ID → demo_source1.ID | Changed_Flag='Update' | 190, 360, 377, 383, 395, 414 |
| `DESCRIPTION` | demo_source1.DESCRIPTION | UPDTRANS.DESCRIPTION3 → UPDTRANS.DESCRIPTION3 → RTRTRANS.DESCRIPTION4 → RTRTRANS.DESCRIPTION4 → EXPTRANS.DESCRIPTION → EXPTRANS.DESCRIPTION → SQ_demo_source1.DESCRIPTION → SQ_demo_source1.DESCRIPTION → demo_source1.DESCRIPTION → demo_source1.DESCRIPTION | Changed_Flag='Update' | 190, 361, 378, 384, 396, 415 |
| `SHORT_NAME` | demo_source1.SHORT_NAME | UPDTRANS.SHORT_NAME3 → UPDTRANS.SHORT_NAME3 → RTRTRANS.SHORT_NAME4 → RTRTRANS.SHORT_NAME4 → EXPTRANS.SHORT_NAME → EXPTRANS.SHORT_NAME → SQ_demo_source1.SHORT_NAME → SQ_demo_source1.SHORT_NAME → demo_source1.SHORT_NAME → demo_source1.SHORT_NAME | Changed_Flag='Update' | 190, 362, 379, 385, 397, 416 |
| `CREATED_BY` | NULL | — | — | — |
| `CREATED_TIME` | NULL | — | — | — |
| `UPDATED_BY` | NULL | UPDTRANS.o_UPDATED_BY2 → UPDTRANS.o_UPDATED_BY2 → RTRTRANS.o_UPDATED_BY3 → RTRTRANS.o_UPDATED_BY3 → EXPTRANS.o_UPDATED_BY → EXPTRANS.o_UPDATED_BY → EXPTRANS.'IDWUSER' | 'IDWUSER'; Changed_Flag='Update' | 182, 190, 363, 407, 421 |
| `UPDATED_TIME` | NULL | UPDTRANS.o_UPDATED_TIME2 → UPDTRANS.o_UPDATED_TIME2 → RTRTRANS.o_UPDATED_TIME3 → RTRTRANS.o_UPDATED_TIME3 → EXPTRANS.o_UPDATED_TIME → EXPTRANS.o_UPDATED_TIME → EXPTRANS.SYSDATE | Changed_Flag='Update'; SYSDATE | 183, 190, 364, 408, 422 |
| `ACTIVE_FLAG` | NULL | — | — | — |
| `START_DATE` | NULL | — | — | — |
| `END_DATE` | NULL | — | — | — |

## Mapping `m_demo_mapping3`

### Target instance `demo_target2`

| target column | source column(s) | path | transformation applied | xml lines |
|---|---|---|---|---|
| `Title` | demo_source2.Title | RTRTRANS.Title1 → RTRTRANS.Title1 → EXPTRANS.Title → EXPTRANS.Title → SQ_demo_source2.Title → SQ_demo_source2.Title → demo_source2.Title → demo_source2.Title | ISNULL(Social_Security_Number); demo_source2.Title | 916, 948, 1031, 1045, 1059, 1073 |
| `Gender` | demo_source2.Gender_Code | RTRTRANS.Gender_Code1 → RTRTRANS.Gender_Code1 → EXPTRANS.Gender_Code → EXPTRANS.Gender_Code → SQ_demo_source2.Gender_Code → SQ_demo_source2.Gender_Code → demo_source2.Gender_Code → demo_source2.Gender_Code | ISNULL(Social_Security_Number); demo_source2.Gender_Code | 916, 948, 1044, 1052, 1066, 1080 |
| `First_Name` | demo_source2.First_Name | RTRTRANS.First_Name1 → RTRTRANS.First_Name1 → EXPTRANS.First_Name → EXPTRANS.First_Name → SQ_demo_source2.First_Name → SQ_demo_source2.First_Name → demo_source2.First_Name → demo_source2.First_Name | ISNULL(Social_Security_Number); demo_source2.First_Name | 916, 948, 1032, 1046, 1060, 1074 |
| `Middle_Name` | demo_source2.Middle_Name | RTRTRANS.Middle_Name1 → RTRTRANS.Middle_Name1 → EXPTRANS.Middle_Name → EXPTRANS.Middle_Name → SQ_demo_source2.Middle_Name → SQ_demo_source2.Middle_Name → demo_source2.Middle_Name → demo_source2.Middle_Name | ISNULL(Social_Security_Number); demo_source2.Middle_Name | 916, 948, 1033, 1047, 1061, 1075 |
| `Last_Name` | demo_source2.Last_Name | RTRTRANS.Last_Name1 → RTRTRANS.Last_Name1 → EXPTRANS.Last_Name → EXPTRANS.Last_Name → SQ_demo_source2.Last_Name → SQ_demo_source2.Last_Name → demo_source2.Last_Name → demo_source2.Last_Name | ISNULL(Social_Security_Number); demo_source2.Last_Name | 916, 948, 1034, 1048, 1062, 1076 |
| `Member_Identifier` | demo_source2.Member_ID | RTRTRANS.Member_ID1 → RTRTRANS.Member_ID1 → EXPTRANS.Member_ID → EXPTRANS.Member_ID → SQ_demo_source2.Member_ID → SQ_demo_source2.Member_ID → demo_source2.Member_ID → demo_source2.Member_ID | ISNULL(Social_Security_Number); demo_source2.Member_ID | 916, 948, 1035, 1049, 1063, 1077 |
| `Member_Suffix` | demo_source2.Member_Suffix | RTRTRANS.Member_Suffix1 → RTRTRANS.Member_Suffix1 → EXPTRANS.Member_Suffix → EXPTRANS.Member_Suffix → SQ_demo_source2.Member_Suffix → SQ_demo_source2.Member_Suffix → demo_source2.Member_Suffix → demo_source2.Member_Suffix | ISNULL(Social_Security_Number); demo_source2.Member_Suffix | 916, 948, 1036, 1050, 1064, 1078 |
| `Date_of_Birth` | demo_source2.Birth_Date | RTRTRANS.Birth_Date1 → RTRTRANS.Birth_Date1 → EXPTRANS.Birth_Date → EXPTRANS.Birth_Date → SQ_demo_source2.Birth_Date → SQ_demo_source2.Birth_Date → demo_source2.Birth_Date → demo_source2.Birth_Date | ISNULL(Social_Security_Number); demo_source2.Birth_Date | 916, 948, 1037, 1051, 1065, 1079 |
| `Member_Number` | demo_source2.Member_Record_Number | RTRTRANS.Member_Record_Number1 → RTRTRANS.Member_Record_Number1 → EXPTRANS.Member_Record_Number → EXPTRANS.Member_Record_Number → SQ_demo_source2.Member_Record_Number → SQ_demo_source2.Member_Record_Number → demo_source2.Member_Record_Number → demo_source2.Member_Record_Number | ISNULL(Social_Security_Number); demo_source2.Member_Record_Number | 916, 948, 1043, 1053, 1067, 1081 |
| `Soc_Number` | demo_source2.Social_Security_Number | RTRTRANS.Social_Security_Number1 → RTRTRANS.Social_Security_Number1 → EXPTRANS.Social_Security_Number → EXPTRANS.Social_Security_Number → SQ_demo_source2.Social_Security_Number → SQ_demo_source2.Social_Security_Number → demo_source2.Social_Security_Number → demo_source2.Social_Security_Number | ISNULL(Social_Security_Number); demo_source2.Social_Security_Number | 916, 948, 1042, 1054, 1068, 1082 |
| `Type_Code` | demo_source2.Member_Type_Code | RTRTRANS.Member_Type_Code1 → RTRTRANS.Member_Type_Code1 → EXPTRANS.Member_Type_Code → EXPTRANS.Member_Type_Code → SQ_demo_source2.Member_Type_Code → SQ_demo_source2.Member_Type_Code → demo_source2.Member_Type_Code → demo_source2.Member_Type_Code | ISNULL(Social_Security_Number); demo_source2.Member_Type_Code | 916, 948, 1041, 1055, 1069, 1083 |
| `Relationship_to_Subscriber_Code` | demo_source2.Relationship_to_Subscriber_Code | RTRTRANS.Relationship_to_Subscriber_Code1 → RTRTRANS.Relationship_to_Subscriber_Code1 → EXPTRANS.Relationship_to_Subscriber_Code → EXPTRANS.Relationship_to_Subscriber_Code → SQ_demo_source2.Relationship_to_Subscriber_Code → SQ_demo_source2.Relationship_to_Subscriber_Code → demo_source2.Relationship_to_Subscriber_Code → demo_source2.Relationship_to_Subscriber_Code | ISNULL(Social_Security_Number); demo_source2.Relationship_to_Subscriber_Code | 916, 948, 1038, 1057, 1071, 1085 |
| `Relationship_to_Subscriber_Code_Label` | demo_source2.Relationship_to_Subscriber_Code_Label | RTRTRANS.Relationship_to_Subscriber_Code_Label1 → RTRTRANS.Relationship_to_Subscriber_Code_Label1 → EXPTRANS.o_Relationship_to_Subscriber_Code_Label → EXPTRANS.o_Relationship_to_Subscriber_Code_Label → SQ_demo_source2.Relationship_to_Subscriber_Code_Label → SQ_demo_source2.Relationship_to_Subscriber_Code_Label → demo_source2.Relationship_to_Subscriber_Code_Label → demo_source2.Relationship_to_Subscriber_Code_Label | ISNULL(Social_Security_Number); demo_source2.Relationship_to_Subscriber_Code_Label; iif(ISNULL(Relationship_to_Subscriber_Code_Label),ABORT('Relationship_to_Subscriber_Code_Labe valuel is null'),Relationship_to_Subscriber_Code_Label) | 916, 943, 948, 1039, 1058, 1072, 1086 |
| `Effective_Date` | demo_source2.Original_Effective_Date | RTRTRANS.Original_Effective_Date1 → RTRTRANS.Original_Effective_Date1 → EXPTRANS.Original_Effective_Date → EXPTRANS.Original_Effective_Date → SQ_demo_source2.Original_Effective_Date → SQ_demo_source2.Original_Effective_Date → demo_source2.Original_Effective_Date → demo_source2.Original_Effective_Date | ISNULL(Social_Security_Number); demo_source2.Original_Effective_Date | 916, 948, 1040, 1056, 1070, 1084 |

### Target instance `demo_target21`

| target column | source column(s) | path | transformation applied | xml lines |
|---|---|---|---|---|
| `Title` | demo_source2.Title | RTRTRANS.Title3 → RTRTRANS.Title3 → EXPTRANS.Title → EXPTRANS.Title → SQ_demo_source2.Title → SQ_demo_source2.Title → demo_source2.Title → demo_source2.Title | NOT ISNULL(Social_Security_Number); demo_source2.Title | 916, 950, 1017, 1045, 1059, 1073 |
| `Gender` | demo_source2.Gender_Code | RTRTRANS.Gender_Code3 → RTRTRANS.Gender_Code3 → EXPTRANS.Gender_Code → EXPTRANS.Gender_Code → SQ_demo_source2.Gender_Code → SQ_demo_source2.Gender_Code → demo_source2.Gender_Code → demo_source2.Gender_Code | NOT ISNULL(Social_Security_Number); demo_source2.Gender_Code | 916, 950, 1024, 1052, 1066, 1080 |
| `First_Name` | demo_source2.First_Name | RTRTRANS.First_Name3 → RTRTRANS.First_Name3 → EXPTRANS.First_Name → EXPTRANS.First_Name → SQ_demo_source2.First_Name → SQ_demo_source2.First_Name → demo_source2.First_Name → demo_source2.First_Name | NOT ISNULL(Social_Security_Number); demo_source2.First_Name | 916, 950, 1018, 1046, 1060, 1074 |
| `Middle_Name` | demo_source2.Middle_Name | RTRTRANS.Middle_Name3 → RTRTRANS.Middle_Name3 → EXPTRANS.Middle_Name → EXPTRANS.Middle_Name → SQ_demo_source2.Middle_Name → SQ_demo_source2.Middle_Name → demo_source2.Middle_Name → demo_source2.Middle_Name | NOT ISNULL(Social_Security_Number); demo_source2.Middle_Name | 916, 950, 1019, 1047, 1061, 1075 |
| `Last_Name` | demo_source2.Last_Name | RTRTRANS.Last_Name3 → RTRTRANS.Last_Name3 → EXPTRANS.Last_Name → EXPTRANS.Last_Name → SQ_demo_source2.Last_Name → SQ_demo_source2.Last_Name → demo_source2.Last_Name → demo_source2.Last_Name | NOT ISNULL(Social_Security_Number); demo_source2.Last_Name | 916, 950, 1020, 1048, 1062, 1076 |
| `Member_Identifier` | demo_source2.Member_ID | RTRTRANS.Member_ID3 → RTRTRANS.Member_ID3 → EXPTRANS.Member_ID → EXPTRANS.Member_ID → SQ_demo_source2.Member_ID → SQ_demo_source2.Member_ID → demo_source2.Member_ID → demo_source2.Member_ID | NOT ISNULL(Social_Security_Number); demo_source2.Member_ID | 916, 950, 1021, 1049, 1063, 1077 |
| `Member_Suffix` | demo_source2.Member_Suffix | RTRTRANS.Member_Suffix3 → RTRTRANS.Member_Suffix3 → EXPTRANS.Member_Suffix → EXPTRANS.Member_Suffix → SQ_demo_source2.Member_Suffix → SQ_demo_source2.Member_Suffix → demo_source2.Member_Suffix → demo_source2.Member_Suffix | NOT ISNULL(Social_Security_Number); demo_source2.Member_Suffix | 916, 950, 1022, 1050, 1064, 1078 |
| `Date_of_Birth` | demo_source2.Birth_Date | RTRTRANS.Birth_Date3 → RTRTRANS.Birth_Date3 → EXPTRANS.Birth_Date → EXPTRANS.Birth_Date → SQ_demo_source2.Birth_Date → SQ_demo_source2.Birth_Date → demo_source2.Birth_Date → demo_source2.Birth_Date | NOT ISNULL(Social_Security_Number); demo_source2.Birth_Date | 916, 950, 1023, 1051, 1065, 1079 |
| `Member_Number` | demo_source2.Member_Record_Number | RTRTRANS.Member_Record_Number3 → RTRTRANS.Member_Record_Number3 → EXPTRANS.Member_Record_Number → EXPTRANS.Member_Record_Number → SQ_demo_source2.Member_Record_Number → SQ_demo_source2.Member_Record_Number → demo_source2.Member_Record_Number → demo_source2.Member_Record_Number | NOT ISNULL(Social_Security_Number); demo_source2.Member_Record_Number | 916, 950, 1026, 1053, 1067, 1081 |
| `Soc_Number` | demo_source2.Social_Security_Number | RTRTRANS.Social_Security_Number3 → RTRTRANS.Social_Security_Number3 → EXPTRANS.Social_Security_Number → EXPTRANS.Social_Security_Number → SQ_demo_source2.Social_Security_Number → SQ_demo_source2.Social_Security_Number → demo_source2.Social_Security_Number → demo_source2.Social_Security_Number | NOT ISNULL(Social_Security_Number); demo_source2.Social_Security_Number | 916, 950, 1025, 1054, 1068, 1082 |
| `Type_Code` | demo_source2.Member_Type_Code | RTRTRANS.Member_Type_Code3 → RTRTRANS.Member_Type_Code3 → EXPTRANS.Member_Type_Code → EXPTRANS.Member_Type_Code → SQ_demo_source2.Member_Type_Code → SQ_demo_source2.Member_Type_Code → demo_source2.Member_Type_Code → demo_source2.Member_Type_Code | NOT ISNULL(Social_Security_Number); demo_source2.Member_Type_Code | 916, 950, 1027, 1055, 1069, 1083 |
| `Relationship_to_Subscriber_Code` | demo_source2.Relationship_to_Subscriber_Code | RTRTRANS.Relationship_to_Subscriber_Code3 → RTRTRANS.Relationship_to_Subscriber_Code3 → EXPTRANS.Relationship_to_Subscriber_Code → EXPTRANS.Relationship_to_Subscriber_Code → SQ_demo_source2.Relationship_to_Subscriber_Code → SQ_demo_source2.Relationship_to_Subscriber_Code → demo_source2.Relationship_to_Subscriber_Code → demo_source2.Relationship_to_Subscriber_Code | NOT ISNULL(Social_Security_Number); demo_source2.Relationship_to_Subscriber_Code | 916, 950, 1029, 1057, 1071, 1085 |
| `Relationship_to_Subscriber_Code_Label` | demo_source2.Relationship_to_Subscriber_Code_Label | RTRTRANS.Relationship_to_Subscriber_Code_Label3 → RTRTRANS.Relationship_to_Subscriber_Code_Label3 → EXPTRANS.o_Relationship_to_Subscriber_Code_Label → EXPTRANS.o_Relationship_to_Subscriber_Code_Label → SQ_demo_source2.Relationship_to_Subscriber_Code_Label → SQ_demo_source2.Relationship_to_Subscriber_Code_Label → demo_source2.Relationship_to_Subscriber_Code_Label → demo_source2.Relationship_to_Subscriber_Code_Label | NOT ISNULL(Social_Security_Number); demo_source2.Relationship_to_Subscriber_Code_Label; iif(ISNULL(Relationship_to_Subscriber_Code_Label),ABORT('Relationship_to_Subscriber_Code_Labe valuel is null'),Relationship_to_Subscriber_Code_Label) | 916, 943, 950, 1030, 1058, 1072, 1086 |
| `Effective_Date` | demo_source2.Original_Effective_Date | RTRTRANS.Original_Effective_Date3 → RTRTRANS.Original_Effective_Date3 → EXPTRANS.Original_Effective_Date → EXPTRANS.Original_Effective_Date → SQ_demo_source2.Original_Effective_Date → SQ_demo_source2.Original_Effective_Date → demo_source2.Original_Effective_Date → demo_source2.Original_Effective_Date | NOT ISNULL(Social_Security_Number); demo_source2.Original_Effective_Date | 916, 950, 1028, 1056, 1070, 1084 |

## Workflow

Execution order derived from WORKFLOWLINK edges: **s_m_demo_mapping2 → s_m_demo_mapping1 → s_m_demo_mapping3**.

```json
{
  "decisions": [
    {
      "expression": "$s_m_demo_mapping2.Status = 1",
      "task": "Decision1",
      "xml_line": 1158
    },
    {
      "expression": "$s_m_demo_mapping1.Status = 1",
      "task": "Decision2",
      "xml_line": 1155
    },
    {
      "expression": "$s_m_demo_mapping3.Status = 1",
      "task": "Decision3",
      "xml_line": 1161
    }
  ],
  "execution_order": [
    "Start",
    "s_m_demo_mapping2",
    "Decision1",
    "s_m_demo_mapping1",
    "Decision2",
    "s_m_demo_mapping3",
    "Decision3",
    "SuccessEmail"
  ],
  "execution_session_order": [
    "s_m_demo_mapping2",
    "s_m_demo_mapping1",
    "s_m_demo_mapping3"
  ],
  "links": [
    {
      "condition": "$Decision2.Condition = 0",
      "from": "Decision2",
      "to": "Failed_Email2",
      "xml_line": 1465
    },
    {
      "condition": "$Decision3.Condition = 1",
      "from": "Decision3",
      "to": "SuccessEmail",
      "xml_line": 1466
    },
    {
      "condition": "$Decision1.Condition = 0",
      "from": "Decision1",
      "to": "Failed_Email1",
      "xml_line": 1467
    },
    {
      "condition": "",
      "from": "Failed_Email2",
      "to": "Control",
      "xml_line": 1468
    },
    {
      "condition": "$Decision2.Condition = 1",
      "from": "Decision2",
      "to": "s_m_demo_mapping3",
      "xml_line": 1469
    },
    {
      "condition": "",
      "from": "Decision1",
      "to": "s_m_demo_mapping1",
      "xml_line": 1470
    },
    {
      "condition": "",
      "from": "Start",
      "to": "s_m_demo_mapping2",
      "xml_line": 1471
    },
    {
      "condition": "",
      "from": "s_m_demo_mapping1",
      "to": "Decision2",
      "xml_line": 1472
    },
    {
      "condition": "",
      "from": "s_m_demo_mapping2",
      "to": "Decision1",
      "xml_line": 1473
    },
    {
      "condition": "",
      "from": "s_m_demo_mapping3",
      "to": "Decision3",
      "xml_line": 1474
    },
    {
      "condition": "$Decision3.Condition = 0",
      "from": "Decision3",
      "to": "Failed_Email3",
      "xml_line": 1475
    }
  ],
  "name": "wf_demo_mapping",
  "sessions": [
    {
      "attributes": [
        {
          "name": "Treat source rows as",
          "value": "Insert",
          "xml_line": 1346
        },
        {
          "name": "Insert",
          "value": "YES",
          "xml_line": 1278
        },
        {
          "name": "Update as Update",
          "value": "YES",
          "xml_line": 1279
        },
        {
          "name": "Insert",
          "value": "YES",
          "xml_line": 1290
        },
        {
          "name": "Update as Update",
          "value": "YES",
          "xml_line": 1291
        },
        {
          "name": "Insert",
          "value": "YES",
          "xml_line": 1316
        },
        {
          "name": "Update as Update",
          "value": "YES",
          "xml_line": 1317
        }
      ],
      "mapping": "m_demo_mapping1",
      "session": "s_m_demo_mapping1",
      "target_load_order": [
        [
          "demo_target6",
          2
        ],
        [
          "demo_target5",
          3
        ],
        [
          "demo_target3",
          6
        ]
      ],
      "targets": [
        "demo_target6",
        "demo_target5",
        "demo_target3"
      ],
      "xml_line": 1236
    },
    {
      "attributes": [
        {
          "name": "Treat source rows as",
          "value": "Data driven",
          "xml_line": 1434
        },
        {
          "name": "Insert",
          "value": "YES",
          "xml_line": 1389
        },
        {
          "name": "Update as Update",
          "value": "YES",
          "xml_line": 1390
        },
        {
          "name": "Insert",
          "value": "YES",
          "xml_line": 1401
        },
        {
          "name": "Update as Update",
          "value": "YES",
          "xml_line": 1402
        }
      ],
      "mapping": "m_demo_mapping2",
      "session": "s_m_demo_mapping2",
      "target_load_order": [
        [
          "demo_target1_INS",
          1
        ],
        [
          "demo_target1_UPD",
          2
        ]
      ],
      "targets": [
        "demo_target1_INS",
        "demo_target1_UPD"
      ],
      "xml_line": 1365
    },
    {
      "attributes": [
        {
          "name": "Treat source rows as",
          "value": "Insert",
          "xml_line": 1217
        },
        {
          "name": "Insert",
          "value": "YES",
          "xml_line": 1184
        },
        {
          "name": "Update as Update",
          "value": "YES",
          "xml_line": 1185
        },
        {
          "name": "Insert",
          "value": "YES",
          "xml_line": 1196
        },
        {
          "name": "Update as Update",
          "value": "YES",
          "xml_line": 1197
        }
      ],
      "mapping": "m_demo_mapping3",
      "session": "s_m_demo_mapping3",
      "target_load_order": [
        [
          "demo_target21",
          1
        ],
        [
          "demo_target2",
          2
        ]
      ],
      "targets": [
        "demo_target21",
        "demo_target2"
      ],
      "xml_line": 1169
    }
  ]
}
```

## Name traps

Empirical discriminators from the seed CSVs:

| trap | row | connector value | name-matched value |
|---|---|---|---|
| m1 demo_target5.FIRST_NM | account 1004 | `AVA` | `NINA` |
| m1 demo_target5.CRDT_SCORE | account 1003 | `677` | `715` |
| m1 demo_target6.TX_TYPE_CD | TX_ID 5003 / account 1002 | `DR` | `CR` |
| m1 demo_target6.CR8_DT | account 1001 | `2024-01-31 (baseline run date)` | `2023-08-18` |
| m1 SQ STRCMP select item | all rows | `dead / no target row` | `not discriminable` |
| m2 UPDTRANS input names vs Update router connectors | REC00001 | `General ledger account 1` | `no DEFAULT1 target row (unconnected)` |
| m2 demo_target1_UPD.DESCRIPTION | REC00002 | `General ledger account 2` | `lookup DESCRIPTION1 does not reach target` |
| m3 router groups / demo_target2 | Member_Record_Number 500000 | `NEWGROUP1 -> demo_target2 (Eli)` | `suffix *2/default group would be NULL / no row` |
| m3 router groups / demo_target21 | Member_Record_Number 500001 | `NEWGROUP2 -> demo_target21 (Omar)` | `suffix *2/default group would be NULL / no row` |

## Unconnected / dead field inventory

### m_demo_mapping1
- `SEQ_GEN.CURRVAL` (Sequence), no outgoing CONNECTOR (XML line 431)
- `agg_TRANS.TX_AMT` (Aggregator), no outgoing CONNECTOR (XML line 444)
- `exp_TRANS1.ACCT_DESC` (Expression), no outgoing CONNECTOR (XML line 467)
- `lkp_TRANS1.IN_ACCT_ID` (Lookup Procedure), no outgoing CONNECTOR (XML line 528)
- `lkp_TRANS1.TX_TYPE_CD` (Lookup Procedure), no outgoing CONNECTOR (XML line 529)
- `lkp_TRANS1.ACCT_ID` (Lookup Procedure), no outgoing CONNECTOR (XML line 530)
- `lkp_TRANS1.TX_TYPE_DESC` (Lookup Procedure), no outgoing CONNECTOR (XML line 531)
- `lkp_TRANS2.IN_ACCT_ID` (Lookup Procedure), no outgoing CONNECTOR (XML line 483)
- `lkp_TRANS2.CUST_ID` (Lookup Procedure), no outgoing CONNECTOR (XML line 484)
- `lkp_TRANS2.ACCT_ID` (Lookup Procedure), no outgoing CONNECTOR (XML line 485)
- `lkp_TRANS2.LAST_NM` (Lookup Procedure), no outgoing CONNECTOR (XML line 487)
- `lkp_TRANS2.CUST_ADDR` (Lookup Procedure), no outgoing CONNECTOR (XML line 488)
- `lkp_TRANS2.CUST_PHN` (Lookup Procedure), no outgoing CONNECTOR (XML line 489)
- `lkp_TRANS2.CUST_EML_ADDR` (Lookup Procedure), no outgoing CONNECTOR (XML line 490)
- `lkp_TRANS2.AGE` (Lookup Procedure), no outgoing CONNECTOR (XML line 491)
- `lkp_TRANS2.DOB` (Lookup Procedure), no outgoing CONNECTOR (XML line 492)
- `lkp_TRANS2.CUST_TYP` (Lookup Procedure), no outgoing CONNECTOR (XML line 493)
- `lkp_TRANS3.IN_CUST_ID` (Lookup Procedure), no outgoing CONNECTOR (XML line 612)
- `lkp_TRANS3.CUST_ID` (Lookup Procedure), no outgoing CONNECTOR (XML line 613)
- `lkp_TRANS3.MAX_CRDT_SCORE` (Lookup Procedure), no outgoing CONNECTOR (XML line 615)
- `lkp_TRANS3.MIN_CRDT_SCORE` (Lookup Procedure), no outgoing CONNECTOR (XML line 616)
- `lkp_TRANS3.MAX_CRDT_LMT` (Lookup Procedure), no outgoing CONNECTOR (XML line 617)
- `lkp_TRANS3.CURR_CRDT_BAL_AMT` (Lookup Procedure), no outgoing CONNECTOR (XML line 618)
- `lkp_TRANS3.AVG_INC_AMT` (Lookup Procedure), no outgoing CONNECTOR (XML line 619)
- `rtr_TRANS.BAL_AMT1` (Router), no outgoing CONNECTOR (XML line 687)
- `rtr_TRANS.ACCT_TYP1` (Router), no outgoing CONNECTOR (XML line 693)
- `rtr_TRANS.LAST_NM1` (Router), no outgoing CONNECTOR (XML line 695)
- `rtr_TRANS.FIRST_NM1` (Router), no outgoing CONNECTOR (XML line 701)
- `rtr_TRANS.CRDT_SCORE1` (Router), no outgoing CONNECTOR (XML line 702)
- `rtr_TRANS.o_ACCT_ID2` (Router), no outgoing CONNECTOR (XML line 705)
- `rtr_TRANS.o_acc_trim2` (Router), no outgoing CONNECTOR (XML line 706)
- `rtr_TRANS.TX_DTTM2` (Router), no outgoing CONNECTOR (XML line 707)
- `rtr_TRANS.TX_ID2` (Router), no outgoing CONNECTOR (XML line 708)
- `rtr_TRANS.ACCT_TYP2` (Router), no outgoing CONNECTOR (XML line 709)
- `rtr_TRANS.TX_AMT2` (Router), no outgoing CONNECTOR (XML line 710)
- `rtr_TRANS.CLSR_DT2` (Router), no outgoing CONNECTOR (XML line 712)
- `rtr_TRANS.ACCT_STAT_CD2` (Router), no outgoing CONNECTOR (XML line 713)
- `rtr_TRANS.o_ACCT_DESC2` (Router), no outgoing CONNECTOR (XML line 714)
- `rtr_TRANS.CR8_DT2` (Router), no outgoing CONNECTOR (XML line 715)
- `rtr_TRANS.o_crdt_trim2` (Router), no outgoing CONNECTOR (XML line 716)
- `rtr_TRANS.BAL_AMT3` (Router), no outgoing CONNECTOR (XML line 719)
- `rtr_TRANS.ACCT_ID3` (Router), no outgoing CONNECTOR (XML line 720)
- `rtr_TRANS.o_ACCT_ID3` (Router), no outgoing CONNECTOR (XML line 721)
- `rtr_TRANS.o_acc_trim3` (Router), no outgoing CONNECTOR (XML line 722)
- `rtr_TRANS.TX_DTTM3` (Router), no outgoing CONNECTOR (XML line 723)
- `rtr_TRANS.TX_ID3` (Router), no outgoing CONNECTOR (XML line 724)
- `rtr_TRANS.ACCT_TYP3` (Router), no outgoing CONNECTOR (XML line 725)
- `rtr_TRANS.TX_AMT3` (Router), no outgoing CONNECTOR (XML line 726)
- `rtr_TRANS.LAST_NM3` (Router), no outgoing CONNECTOR (XML line 727)
- `rtr_TRANS.CLSR_DT3` (Router), no outgoing CONNECTOR (XML line 728)
- `rtr_TRANS.ACCT_STAT_CD3` (Router), no outgoing CONNECTOR (XML line 729)
- `rtr_TRANS.o_ACCT_DESC3` (Router), no outgoing CONNECTOR (XML line 730)
- `rtr_TRANS.CR8_DT3` (Router), no outgoing CONNECTOR (XML line 731)
- `rtr_TRANS.o_crdt_trim3` (Router), no outgoing CONNECTOR (XML line 732)
- `rtr_TRANS.FIRST_NM3` (Router), no outgoing CONNECTOR (XML line 733)
- `rtr_TRANS.CRDT_SCORE3` (Router), no outgoing CONNECTOR (XML line 734)
- `sq_demo_source4.TX_TYPE_CD` (Source Qualifier), no outgoing CONNECTOR (XML line 579)
### m_demo_mapping2
- `LKPTRANS.ID` (Lookup Procedure), no outgoing CONNECTOR (XML line 270)
- `LKPTRANS.CREATED_BY` (Lookup Procedure), no outgoing CONNECTOR (XML line 273)
- `LKPTRANS.CREATED_TIME` (Lookup Procedure), no outgoing CONNECTOR (XML line 274)
- `LKPTRANS.UPDATED_BY` (Lookup Procedure), no outgoing CONNECTOR (XML line 275)
- `LKPTRANS.UPDATED_TIME` (Lookup Procedure), no outgoing CONNECTOR (XML line 276)
- `LKPTRANS.ACTIVE_FLAG` (Lookup Procedure), no outgoing CONNECTOR (XML line 277)
- `LKPTRANS.START_DATE` (Lookup Procedure), no outgoing CONNECTOR (XML line 278)
- `LKPTRANS.END_DATE` (Lookup Procedure), no outgoing CONNECTOR (XML line 279)
- `LKPTRANS.ID1` (Lookup Procedure), no outgoing CONNECTOR (XML line 280)
- `RTRTRANS.LEAD_CO_MNE11` (Router), no outgoing CONNECTOR (XML line 215)
- `RTRTRANS.BRANCH_CO_MNE11` (Router), no outgoing CONNECTOR (XML line 216)
- `RTRTRANS.MIS_DATE11` (Router), no outgoing CONNECTOR (XML line 217)
- `RTRTRANS.DESCRIPTION11` (Router), no outgoing CONNECTOR (XML line 218)
- `RTRTRANS.SHORT_NAME11` (Router), no outgoing CONNECTOR (XML line 219)
- `RTRTRANS.New_Flag1` (Router), no outgoing CONNECTOR (XML line 220)
- `RTRTRANS.Changed_Flag1` (Router), no outgoing CONNECTOR (XML line 221)
- `RTRTRANS.o_UPDATED_BY1` (Router), no outgoing CONNECTOR (XML line 224)
- `RTRTRANS.o_UPDATED_TIME1` (Router), no outgoing CONNECTOR (XML line 225)
- `RTRTRANS.Key1` (Router), no outgoing CONNECTOR (XML line 226)
- `RTRTRANS.LEAD_CO_MNE13` (Router), no outgoing CONNECTOR (XML line 233)
- `RTRTRANS.BRANCH_CO_MNE13` (Router), no outgoing CONNECTOR (XML line 234)
- `RTRTRANS.MIS_DATE13` (Router), no outgoing CONNECTOR (XML line 235)
- `RTRTRANS.DESCRIPTION13` (Router), no outgoing CONNECTOR (XML line 236)
- `RTRTRANS.SHORT_NAME13` (Router), no outgoing CONNECTOR (XML line 237)
- `RTRTRANS.LEAD_CO_MNE3` (Router), no outgoing CONNECTOR (XML line 245)
- `RTRTRANS.BRANCH_CO_MNE3` (Router), no outgoing CONNECTOR (XML line 246)
- `RTRTRANS.MIS_DATE3` (Router), no outgoing CONNECTOR (XML line 247)
- `RTRTRANS.ID2` (Router), no outgoing CONNECTOR (XML line 248)
- `RTRTRANS.DESCRIPTION3` (Router), no outgoing CONNECTOR (XML line 249)
- `RTRTRANS.SHORT_NAME3` (Router), no outgoing CONNECTOR (XML line 250)
- `RTRTRANS.LEAD_CO_MNE12` (Router), no outgoing CONNECTOR (XML line 251)
- `RTRTRANS.BRANCH_CO_MNE12` (Router), no outgoing CONNECTOR (XML line 252)
- `RTRTRANS.MIS_DATE12` (Router), no outgoing CONNECTOR (XML line 253)
- `RTRTRANS.DESCRIPTION12` (Router), no outgoing CONNECTOR (XML line 254)
- `RTRTRANS.SHORT_NAME12` (Router), no outgoing CONNECTOR (XML line 255)
- `RTRTRANS.New_Flag2` (Router), no outgoing CONNECTOR (XML line 256)
- `RTRTRANS.Changed_Flag2` (Router), no outgoing CONNECTOR (XML line 257)
- `RTRTRANS.o_CREATED_BY2` (Router), no outgoing CONNECTOR (XML line 258)
- `RTRTRANS.o_CREATED_TIME2` (Router), no outgoing CONNECTOR (XML line 259)
- `RTRTRANS.o_UPDATED_BY2` (Router), no outgoing CONNECTOR (XML line 260)
- `RTRTRANS.o_UPDATED_TIME2` (Router), no outgoing CONNECTOR (XML line 261)
- `RTRTRANS.Key2` (Router), no outgoing CONNECTOR (XML line 262)
- `SEQTRANS.CURRVAL` (Sequence), no outgoing CONNECTOR (XML line 316)
- `UPDTRANS.New_Flag2` (Update Strategy), no outgoing CONNECTOR (XML line 334)
- `UPDTRANS.Changed_Flag2` (Update Strategy), no outgoing CONNECTOR (XML line 335)
- `UPDTRANS.o_CREATED_BY2` (Update Strategy), no outgoing CONNECTOR (XML line 336)
- `UPDTRANS.o_CREATED_TIME2` (Update Strategy), no outgoing CONNECTOR (XML line 337)
### m_demo_mapping3
- `EXPTRANS.Relationship_to_Subscriber_Code_Label` (Expression), no outgoing CONNECTOR (XML line 942)
- `RTRTRANS.Title2` (Router), no outgoing CONNECTOR (XML line 993)
- `RTRTRANS.First_Name2` (Router), no outgoing CONNECTOR (XML line 994)
- `RTRTRANS.Middle_Name2` (Router), no outgoing CONNECTOR (XML line 995)
- `RTRTRANS.Last_Name2` (Router), no outgoing CONNECTOR (XML line 996)
- `RTRTRANS.Member_ID2` (Router), no outgoing CONNECTOR (XML line 997)
- `RTRTRANS.Member_Suffix2` (Router), no outgoing CONNECTOR (XML line 998)
- `RTRTRANS.Birth_Date2` (Router), no outgoing CONNECTOR (XML line 999)
- `RTRTRANS.Gender_Code2` (Router), no outgoing CONNECTOR (XML line 1000)
- `RTRTRANS.Member_Record_Number2` (Router), no outgoing CONNECTOR (XML line 1001)
- `RTRTRANS.Social_Security_Number2` (Router), no outgoing CONNECTOR (XML line 1002)
- `RTRTRANS.Member_Type_Code2` (Router), no outgoing CONNECTOR (XML line 1003)
- `RTRTRANS.Original_Effective_Date2` (Router), no outgoing CONNECTOR (XML line 1004)
- `RTRTRANS.Relationship_to_Subscriber_Code2` (Router), no outgoing CONNECTOR (XML line 1005)
- `RTRTRANS.Relationship_to_Subscriber_Code_Label2` (Router), no outgoing CONNECTOR (XML line 1006)
