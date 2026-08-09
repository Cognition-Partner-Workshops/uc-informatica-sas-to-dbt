# Informatica connector lineage

## m_demo_mapping2

### demo_target1_UPD (`demo_target1`)
- `Key`: `demo_target1_UPD.Key` [XML line 356] <- `UPDTRANS.Key2` [XML line 423] <- `RTRTRANS.Key3`
- `LEAD_CO_MNE`: `demo_target1_UPD.LEAD_CO_MNE` [XML line 357] <- `UPDTRANS.LEAD_CO_MNE3` [XML line 411] <- `RTRTRANS.LEAD_CO_MNE4`
- `BRANCH_CO_MNE`: `demo_target1_UPD.BRANCH_CO_MNE` [XML line 358] <- `UPDTRANS.BRANCH_CO_MNE3` [XML line 412] <- `RTRTRANS.BRANCH_CO_MNE4`
- `MIS_DATE`: `demo_target1_UPD.MIS_DATE` [XML line 359] <- `UPDTRANS.MIS_DATE3` [XML line 413] <- `RTRTRANS.MIS_DATE4`
- `ID`: `demo_target1_UPD.ID` [XML line 360] <- `UPDTRANS.ID2` [XML line 414] <- `RTRTRANS.ID3`
- `DESCRIPTION`: `demo_target1_UPD.DESCRIPTION` [XML line 361] <- `UPDTRANS.DESCRIPTION3` [XML line 415] <- `RTRTRANS.DESCRIPTION4`
- `SHORT_NAME`: `demo_target1_UPD.SHORT_NAME` [XML line 362] <- `UPDTRANS.SHORT_NAME3` [XML line 416] <- `RTRTRANS.SHORT_NAME4`
- `CREATED_BY`: `demo_target1_UPD.CREATED_BY`
- `CREATED_TIME`: `demo_target1_UPD.CREATED_TIME`
- `UPDATED_BY`: `demo_target1_UPD.UPDATED_BY` [XML line 363] <- `UPDTRANS.o_UPDATED_BY2` [XML line 421] <- `RTRTRANS.o_UPDATED_BY3`
- `UPDATED_TIME`: `demo_target1_UPD.UPDATED_TIME` [XML line 364] <- `UPDTRANS.o_UPDATED_TIME2` [XML line 422] <- `RTRTRANS.o_UPDATED_TIME3`
- `ACTIVE_FLAG`: `demo_target1_UPD.ACTIVE_FLAG`
- `START_DATE`: `demo_target1_UPD.START_DATE`
- `END_DATE`: `demo_target1_UPD.END_DATE`

### demo_target1_INS (`demo_target1`)
- `Key`: `demo_target1_INS.Key` [XML line 373] <- `SEQTRANS.NEXTVAL`
- `LEAD_CO_MNE`: `demo_target1_INS.LEAD_CO_MNE` [XML line 365] <- `RTRTRANS.LEAD_CO_MNE2`
- `BRANCH_CO_MNE`: `demo_target1_INS.BRANCH_CO_MNE` [XML line 366] <- `RTRTRANS.BRANCH_CO_MNE2`
- `MIS_DATE`: `demo_target1_INS.MIS_DATE` [XML line 367] <- `RTRTRANS.MIS_DATE2`
- `ID`: `demo_target1_INS.ID` [XML line 368] <- `RTRTRANS.ID1`
- `DESCRIPTION`: `demo_target1_INS.DESCRIPTION` [XML line 369] <- `RTRTRANS.DESCRIPTION2`
- `SHORT_NAME`: `demo_target1_INS.SHORT_NAME` [XML line 370] <- `RTRTRANS.SHORT_NAME2`
- `CREATED_BY`: `demo_target1_INS.CREATED_BY` [XML line 371] <- `RTRTRANS.o_CREATED_BY1`
- `CREATED_TIME`: `demo_target1_INS.CREATED_TIME` [XML line 372] <- `RTRTRANS.o_CREATED_TIME1`
- `UPDATED_BY`: `demo_target1_INS.UPDATED_BY`
- `UPDATED_TIME`: `demo_target1_INS.UPDATED_TIME`
- `ACTIVE_FLAG`: `demo_target1_INS.ACTIVE_FLAG`
- `START_DATE`: `demo_target1_INS.START_DATE`
- `END_DATE`: `demo_target1_INS.END_DATE`

## m_demo_mapping1

### demo_target6 (`demo_target6`)
- `ACCT_ID`: `demo_target6.ACCT_ID` [XML line 790] <- `agg_TRANS.ACCT_ID` [XML line 817] <- `exp_TRANS1.ACCT_ID` [XML line 827] <- `exp_TRANS.ACCT_ID` [XML line 875] <- `sq_demo_source4.ACCT_ID` [XML line 852] <- `demo_source4.ACCT_ID`
- `ACCT_TYP`: `demo_target6.ACCT_TYP` [XML line 787] <- `agg_TRANS.o_acc_trim` [XML line 816] <- `exp_TRANS1.o_acc_trim` [XML line 829] <- `exp_TRANS.o_acc_trim`
- `ACCT_DESC`: `demo_target6.ACCT_DESC` [XML line 793] <- `agg_TRANS.o_ACCT_DESC` [XML line 807] <- `exp_TRANS1.o_ACCT_DESC`
- `CR8_DT`: `demo_target6.CR8_DT` [XML line 792] <- `agg_TRANS.CR8_DT` [XML line 814] <- `exp_TRANS1.CR8_DT` [XML line 828] <- `exp_TRANS.CR8_DT` [XML line 876] <- `sq_demo_source4.CR8_DT` [XML line 856] <- `demo_source4.CR8_DT`
- `CRDT_LN`: `demo_target6.CRDT_LN` [XML line 788] <- `agg_TRANS.o_crdt_trim` [XML line 809] <- `exp_TRANS1.o_crdt_trim` [XML line 830] <- `exp_TRANS.o_crdt_trim`
- `CLSR_DT`: `demo_target6.CLSR_DT` [XML line 789] <- `agg_TRANS.CLSR_DT` [XML line 810] <- `exp_TRANS1.CLSR_DT` [XML line 818] <- `exp_TRANS.CLSR_DT` [XML line 866] <- `sq_demo_source4.CLSR_DT` [XML line 863] <- `demo_source4.CLSR_DT`
- `ACCT_STAT_CD`: `demo_target6.ACCT_STAT_CD` [XML line 783] <- `agg_TRANS.ACCT_STAT_CD` [XML line 812] <- `exp_TRANS1.ACCT_STAT_CD` [XML line 823] <- `exp_TRANS.ACCT_STAT_CD` [XML line 871] <- `sq_demo_source4.ACCT_STAT_CD` [XML line 864] <- `demo_source4.ACCT_STAT_CD`
- `TX_ID`: `demo_target6.TX_ID` [XML line 784] <- `agg_TRANS.TX_ID` [XML line 811] <- `exp_TRANS1.TX_ID` [XML line 824] <- `exp_TRANS.TX_ID` [XML line 872] <- `sq_demo_source4.TX_ID` [XML line 857] <- `demo_source3.TX_ID`
- `ACCT_KEY`: `demo_target6.ACCT_KEY` [XML line 785] <- `SEQ_GEN.NEXTVAL`
- `TX_DTTM`: `demo_target6.TX_DTTM` [XML line 782] <- `agg_TRANS.TX_DTTM` [XML line 813] <- `exp_TRANS1.TX_DTTM` [XML line 819] <- `exp_TRANS.TX_DTTM` [XML line 867] <- `sq_demo_source4.TX_DTTM` [XML line 859] <- `demo_source3.TX_DTTM`
- `TX_AMT`: `demo_target6.TX_AMT` [XML line 791] <- `agg_TRANS.o_TX_AMT`
- `TX_TYPE_CD`: `demo_target6.TX_TYPE_CD` [XML line 786] <- `agg_TRANS.o_ACCT_ID` [XML line 815] <- `exp_TRANS1.o_ACCT_ID` [XML line 831] <- `exp_TRANS.o_ACCT_ID`

### demo_target5 (`demo_target5`)
- `ACCT_ID`: `demo_target5.ACCT_ID` [XML line 795] <- `exp_TRANS1.ACCT_ID` [XML line 827] <- `exp_TRANS.ACCT_ID` [XML line 875] <- `sq_demo_source4.ACCT_ID` [XML line 852] <- `demo_source4.ACCT_ID`
- `FIRST_NM`: `demo_target5.FIRST_NM` [XML line 797] <- `exp_TRANS1.FIRST_NM` [XML line 832] <- `lkp_TRANS2.FIRST_NM`
- `LAST_NM`: `demo_target5.LAST_NM` [XML line 796] <- `exp_TRANS1.LAST_NM` [XML line 825] <- `exp_TRANS.LAST_NM` [XML line 873] <- `sq_demo_source4.LAST_NM` [XML line 858] <- `demo_source3.LAST_NM`
- `BAL_AMT`: `demo_target5.BAL_AMT` [XML line 798] <- `exp_TRANS1.BAL_AMT` [XML line 820] <- `exp_TRANS.BAL_AMT` [XML line 868] <- `sq_demo_source4.BAL_AMT` [XML line 862] <- `demo_source3.BAL_AMT`
- `CRDT_SCORE`: `demo_target5.CRDT_SCORE` [XML line 794] <- `exp_TRANS1.CRDT_SCORE` [XML line 833] <- `lkp_TRANS3.CRDT_SCORE`

### demo_target3 (`demo_target3`)
- `PRODUCT_ID`: `demo_target3.PRODUCT_ID` [XML line 799] <- `exp_TRANS2.PRODUCT_ID` [XML line 879] <- `SQ_demo_source5.PRODUCT_ID` [XML line 887] <- `demo_source5.PRODUCT_ID`
- `PRODUCT_NM`: `demo_target3.PRODUCT_NM` [XML line 801] <- `exp_TRANS2.PRODUCT_NM` [XML line 880] <- `SQ_demo_source5.PRODUCT_NM` [XML line 888] <- `demo_source5.PRODUCT_NM`
- `PRODUCT_NO`: `demo_target3.PRODUCT_NO` [XML line 800] <- `exp_TRANS2.PRODUCT_NO` [XML line 881] <- `SQ_demo_source5.PRODUCT_NO` [XML line 889] <- `demo_source5.PRODUCT_NO`
- `COLOR`: `demo_target3.COLOR` [XML line 803] <- `exp_TRANS2.COLOR` [XML line 882] <- `SQ_demo_source5.COLOR` [XML line 890] <- `demo_source5.COLOR`
- `STD_COST`: `demo_target3.STD_COST` [XML line 802] <- `exp_TRANS2.STD_COST` [XML line 883] <- `SQ_demo_source5.STD_COST` [XML line 891] <- `demo_source5.STD_COST`
- `LIST_PRICE`: `demo_target3.LIST_PRICE` [XML line 804] <- `exp_TRANS2.LIST_PRICE` [XML line 884] <- `SQ_demo_source5.LIST_PRICE` [XML line 892] <- `demo_source5.LIST_PRICE`
- `SELL_ST_DT`: `demo_target3.SELL_ST_DT` [XML line 805] <- `exp_TRANS2.o_SELL_ST_DT`
- `SELL_ED_DT`: `demo_target3.SELL_ED_DT` [XML line 806] <- `exp_TRANS2.o_SELL_ED_DT`

## m_demo_mapping3

### demo_target21 (`demo_target2`)
- `Title`: `demo_target21.Title` [XML line 1017] <- `RTRTRANS.Title3`
- `Gender`: `demo_target21.Gender` [XML line 1024] <- `RTRTRANS.Gender_Code3`
- `First_Name`: `demo_target21.First_Name` [XML line 1018] <- `RTRTRANS.First_Name3`
- `Middle_Name`: `demo_target21.Middle_Name` [XML line 1019] <- `RTRTRANS.Middle_Name3`
- `Last_Name`: `demo_target21.Last_Name` [XML line 1020] <- `RTRTRANS.Last_Name3`
- `Member_Identifier`: `demo_target21.Member_Identifier` [XML line 1021] <- `RTRTRANS.Member_ID3`
- `Member_Suffix`: `demo_target21.Member_Suffix` [XML line 1022] <- `RTRTRANS.Member_Suffix3`
- `Date_of_Birth`: `demo_target21.Date_of_Birth` [XML line 1023] <- `RTRTRANS.Birth_Date3`
- `Member_Number`: `demo_target21.Member_Number` [XML line 1026] <- `RTRTRANS.Member_Record_Number3`
- `Soc_Number`: `demo_target21.Soc_Number` [XML line 1025] <- `RTRTRANS.Social_Security_Number3`
- `Type_Code`: `demo_target21.Type_Code` [XML line 1027] <- `RTRTRANS.Member_Type_Code3`
- `Relationship_to_Subscriber_Code`: `demo_target21.Relationship_to_Subscriber_Code` [XML line 1029] <- `RTRTRANS.Relationship_to_Subscriber_Code3`
- `Relationship_to_Subscriber_Code_Label`: `demo_target21.Relationship_to_Subscriber_Code_Label` [XML line 1030] <- `RTRTRANS.Relationship_to_Subscriber_Code_Label3`
- `Effective_Date`: `demo_target21.Effective_Date` [XML line 1028] <- `RTRTRANS.Original_Effective_Date3`

### demo_target2 (`demo_target2`)
- `Title`: `demo_target2.Title` [XML line 1031] <- `RTRTRANS.Title1`
- `Gender`: `demo_target2.Gender` [XML line 1044] <- `RTRTRANS.Gender_Code1`
- `First_Name`: `demo_target2.First_Name` [XML line 1032] <- `RTRTRANS.First_Name1`
- `Middle_Name`: `demo_target2.Middle_Name` [XML line 1033] <- `RTRTRANS.Middle_Name1`
- `Last_Name`: `demo_target2.Last_Name` [XML line 1034] <- `RTRTRANS.Last_Name1`
- `Member_Identifier`: `demo_target2.Member_Identifier` [XML line 1035] <- `RTRTRANS.Member_ID1`
- `Member_Suffix`: `demo_target2.Member_Suffix` [XML line 1036] <- `RTRTRANS.Member_Suffix1`
- `Date_of_Birth`: `demo_target2.Date_of_Birth` [XML line 1037] <- `RTRTRANS.Birth_Date1`
- `Member_Number`: `demo_target2.Member_Number` [XML line 1043] <- `RTRTRANS.Member_Record_Number1`
- `Soc_Number`: `demo_target2.Soc_Number` [XML line 1042] <- `RTRTRANS.Social_Security_Number1`
- `Type_Code`: `demo_target2.Type_Code` [XML line 1041] <- `RTRTRANS.Member_Type_Code1`
- `Relationship_to_Subscriber_Code`: `demo_target2.Relationship_to_Subscriber_Code` [XML line 1038] <- `RTRTRANS.Relationship_to_Subscriber_Code1`
- `Relationship_to_Subscriber_Code_Label`: `demo_target2.Relationship_to_Subscriber_Code_Label` [XML line 1039] <- `RTRTRANS.Relationship_to_Subscriber_Code_Label1`
- `Effective_Date`: `demo_target2.Effective_Date` [XML line 1040] <- `RTRTRANS.Original_Effective_Date1`
