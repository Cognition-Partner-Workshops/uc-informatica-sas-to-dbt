# Informatica field-level lineage

Edges below are traversed from target ports through XML CONNECTOR edges.

## demo_target1_UPD

### demo_target1_UPD.Key
- demo_target1_UPD.Key (XML line 81)
- UPDTRANS.Key2 (XML line 340)
- RTRTRANS.Key3 [Update] (XML line 244)
- EXPTRANS.Key = Key (XML line 170)
- LKPTRANS.Key (XML line 266)
- demo_target1.Key [lookup condition: ID = ID1; policy: Use Any Value] (XML line 81)

### demo_target1_UPD.LEAD_CO_MNE
- demo_target1_UPD.LEAD_CO_MNE (XML line 82)
- UPDTRANS.LEAD_CO_MNE3 (XML line 328)
- RTRTRANS.LEAD_CO_MNE4 [Update] (XML line 227)
- EXPTRANS.LEAD_CO_MNE = LEAD_CO_MNE (XML line 164)
- SQ_demo_source1.LEAD_CO_MNE (XML line 145)
- demo_source1.LEAD_CO_MNE (XML line 16)

### demo_target1_UPD.BRANCH_CO_MNE
- demo_target1_UPD.BRANCH_CO_MNE (XML line 83)
- UPDTRANS.BRANCH_CO_MNE3 (XML line 329)
- RTRTRANS.BRANCH_CO_MNE4 [Update] (XML line 228)
- EXPTRANS.BRANCH_CO_MNE = BRANCH_CO_MNE (XML line 165)
- SQ_demo_source1.BRANCH_CO_MNE (XML line 146)
- demo_source1.BRANCH_CO_MNE (XML line 17)

### demo_target1_UPD.MIS_DATE
- demo_target1_UPD.MIS_DATE (XML line 84)
- UPDTRANS.MIS_DATE3 (XML line 330)
- RTRTRANS.MIS_DATE4 [Update] (XML line 229)
- EXPTRANS.MIS_DATE = MIS_DATE (XML line 166)
- SQ_demo_source1.MIS_DATE (XML line 147)
- demo_source1.MIS_DATE (XML line 18)

### demo_target1_UPD.ID
- demo_target1_UPD.ID (XML line 85)
- UPDTRANS.ID2 (XML line 331)
- RTRTRANS.ID3 [Update] (XML line 230)
- EXPTRANS.ID = ID (XML line 167)
- SQ_demo_source1.ID (XML line 148)
- demo_source1.ID (XML line 19)

### demo_target1_UPD.DESCRIPTION
- demo_target1_UPD.DESCRIPTION (XML line 86)
- UPDTRANS.DESCRIPTION3 (XML line 332)
- RTRTRANS.DESCRIPTION4 [Update] (XML line 231)
- EXPTRANS.DESCRIPTION = DESCRIPTION (XML line 168)
- SQ_demo_source1.DESCRIPTION (XML line 149)
- demo_source1.DESCRIPTION (XML line 20)

### demo_target1_UPD.SHORT_NAME
- demo_target1_UPD.SHORT_NAME (XML line 87)
- UPDTRANS.SHORT_NAME3 (XML line 333)
- RTRTRANS.SHORT_NAME4 [Update] (XML line 232)
- EXPTRANS.SHORT_NAME = SHORT_NAME (XML line 169)
- SQ_demo_source1.SHORT_NAME (XML line 150)
- demo_source1.SHORT_NAME (XML line 21)

### demo_target1_UPD.CREATED_BY
- demo_target1_UPD.CREATED_BY (XML line 88)

### demo_target1_UPD.CREATED_TIME
- demo_target1_UPD.CREATED_TIME (XML line 89)

### demo_target1_UPD.UPDATED_BY
- demo_target1_UPD.UPDATED_BY (XML line 90)
- UPDTRANS.o_UPDATED_BY2 (XML line 338)
- RTRTRANS.o_UPDATED_BY3 [Update] (XML line 242)
- EXPTRANS.o_UPDATED_BY = 'IDWUSER' (XML line 182)

### demo_target1_UPD.UPDATED_TIME
- demo_target1_UPD.UPDATED_TIME (XML line 91)
- UPDTRANS.o_UPDATED_TIME2 (XML line 339)
- RTRTRANS.o_UPDATED_TIME3 [Update] (XML line 243)
- EXPTRANS.o_UPDATED_TIME = SYSDATE (XML line 183)

### demo_target1_UPD.ACTIVE_FLAG
- demo_target1_UPD.ACTIVE_FLAG (XML line 92)

### demo_target1_UPD.START_DATE
- demo_target1_UPD.START_DATE (XML line 93)

### demo_target1_UPD.END_DATE
- demo_target1_UPD.END_DATE (XML line 94)

## demo_target1_INS

### demo_target1_INS.Key
- demo_target1_INS.Key (XML line 81)
- SEQTRANS.NEXTVAL (XML line 315)

### demo_target1_INS.LEAD_CO_MNE
- demo_target1_INS.LEAD_CO_MNE (XML line 82)
- RTRTRANS.LEAD_CO_MNE2 [Insert] (XML line 209)
- EXPTRANS.LEAD_CO_MNE = LEAD_CO_MNE (XML line 164)
- SQ_demo_source1.LEAD_CO_MNE (XML line 145)
- demo_source1.LEAD_CO_MNE (XML line 16)

### demo_target1_INS.BRANCH_CO_MNE
- demo_target1_INS.BRANCH_CO_MNE (XML line 83)
- RTRTRANS.BRANCH_CO_MNE2 [Insert] (XML line 210)
- EXPTRANS.BRANCH_CO_MNE = BRANCH_CO_MNE (XML line 165)
- SQ_demo_source1.BRANCH_CO_MNE (XML line 146)
- demo_source1.BRANCH_CO_MNE (XML line 17)

### demo_target1_INS.MIS_DATE
- demo_target1_INS.MIS_DATE (XML line 84)
- RTRTRANS.MIS_DATE2 [Insert] (XML line 211)
- EXPTRANS.MIS_DATE = MIS_DATE (XML line 166)
- SQ_demo_source1.MIS_DATE (XML line 147)
- demo_source1.MIS_DATE (XML line 18)

### demo_target1_INS.ID
- demo_target1_INS.ID (XML line 85)
- RTRTRANS.ID1 [Insert] (XML line 212)
- EXPTRANS.ID = ID (XML line 167)
- SQ_demo_source1.ID (XML line 148)
- demo_source1.ID (XML line 19)

### demo_target1_INS.DESCRIPTION
- demo_target1_INS.DESCRIPTION (XML line 86)
- RTRTRANS.DESCRIPTION2 [Insert] (XML line 213)
- EXPTRANS.DESCRIPTION = DESCRIPTION (XML line 168)
- SQ_demo_source1.DESCRIPTION (XML line 149)
- demo_source1.DESCRIPTION (XML line 20)

### demo_target1_INS.SHORT_NAME
- demo_target1_INS.SHORT_NAME (XML line 87)
- RTRTRANS.SHORT_NAME2 [Insert] (XML line 214)
- EXPTRANS.SHORT_NAME = SHORT_NAME (XML line 169)
- SQ_demo_source1.SHORT_NAME (XML line 150)
- demo_source1.SHORT_NAME (XML line 21)

### demo_target1_INS.CREATED_BY
- demo_target1_INS.CREATED_BY (XML line 88)
- RTRTRANS.o_CREATED_BY1 [Insert] (XML line 222)
- EXPTRANS.o_CREATED_BY = 'IDWUSER' (XML line 180)

### demo_target1_INS.CREATED_TIME
- demo_target1_INS.CREATED_TIME (XML line 89)
- RTRTRANS.o_CREATED_TIME1 [Insert] (XML line 223)
- EXPTRANS.o_CREATED_TIME = SYSDATE (XML line 181)

### demo_target1_INS.UPDATED_BY
- demo_target1_INS.UPDATED_BY (XML line 90)

### demo_target1_INS.UPDATED_TIME
- demo_target1_INS.UPDATED_TIME (XML line 91)

### demo_target1_INS.ACTIVE_FLAG
- demo_target1_INS.ACTIVE_FLAG (XML line 92)

### demo_target1_INS.START_DATE
- demo_target1_INS.START_DATE (XML line 93)

### demo_target1_INS.END_DATE
- demo_target1_INS.END_DATE (XML line 94)

## demo_target6

### demo_target6.ACCT_ID
- demo_target6.ACCT_ID (XML line 111)
- agg_TRANS.ACCT_ID = ACCT_ID (XML line 452)
- rtr_TRANS.ACCT_ID1 [demo_target6_GRP] (XML line 688)
- exp_TRANS1.ACCT_ID = ACCT_ID (XML line 473)
- exp_TRANS.ACCT_ID = ACCT_ID (XML line 603)
- sq_demo_source4.ACCT_ID (XML line 566)
- demo_source4.ACCT_ID (XML line 24)

### demo_target6.ACCT_TYP
- demo_target6.ACCT_TYP (XML line 98)
- agg_TRANS.o_acc_trim = o_acc_trim (XML line 453)
- rtr_TRANS.o_acc_trim1 [demo_target6_GRP] (XML line 690)
- exp_TRANS1.o_acc_trim = o_acc_trim (XML line 475)
- exp_TRANS.o_acc_trim = RTRIM(ACCT_TYP) (XML line 606)

### demo_target6.ACCT_DESC
- demo_target6.ACCT_DESC (XML line 99)
- agg_TRANS.o_ACCT_DESC = o_ACCT_DESC (XML line 443)
- rtr_TRANS.o_ACCT_DESC1 [demo_target6_GRP] (XML line 698)
- exp_TRANS1.o_ACCT_DESC = RTRIM(ACCT_DESC) (XML line 479)

### demo_target6.CR8_DT
- demo_target6.CR8_DT (XML line 100)
- agg_TRANS.CR8_DT = CR8_DT (XML line 450)
- rtr_TRANS.CR8_DT1 [demo_target6_GRP] (XML line 699)
- exp_TRANS1.CR8_DT = CR8_DT (XML line 474)
- exp_TRANS.CR8_DT = CR8_DT (XML line 604)
- sq_demo_source4.CR8_DT (XML line 570)
- demo_source4.CR8_DT (XML line 28)
- SQL override: SYSTIMESTAMP (positional SQL override) (XML line 580)

### demo_target6.CRDT_LN
- demo_target6.CRDT_LN (XML line 101)
- agg_TRANS.o_crdt_trim = o_crdt_trim (XML line 445)
- rtr_TRANS.o_crdt_trim1 [demo_target6_GRP] (XML line 700)
- exp_TRANS1.o_crdt_trim = o_crdt_trim (XML line 476)
- exp_TRANS.o_crdt_trim = LTRIM(CRDT_LN) (XML line 607)

### demo_target6.CLSR_DT
- demo_target6.CLSR_DT (XML line 102)
- agg_TRANS.CLSR_DT = CLSR_DT (XML line 446)
- rtr_TRANS.CLSR_DT1 [demo_target6_GRP] (XML line 696)
- exp_TRANS1.CLSR_DT = CLSR_DT (XML line 464)
- exp_TRANS.CLSR_DT = CLSR_DT (XML line 594)
- sq_demo_source4.CLSR_DT (XML line 571)
- demo_source4.CLSR_DT (XML line 29)

### demo_target6.ACCT_STAT_CD
- demo_target6.ACCT_STAT_CD (XML line 103)
- agg_TRANS.ACCT_STAT_CD = ACCT_STAT_CD (XML line 448)
- rtr_TRANS.ACCT_STAT_CD1 [demo_target6_GRP] (XML line 697)
- exp_TRANS1.ACCT_STAT_CD = ACCT_STAT_CD (XML line 469)
- exp_TRANS.ACCT_STAT_CD = ACCT_STAT_CD (XML line 599)
- sq_demo_source4.ACCT_STAT_CD (XML line 572)
- demo_source4.ACCT_STAT_CD (XML line 30)

### demo_target6.TX_ID
- demo_target6.TX_ID (XML line 104)
- agg_TRANS.TX_ID = TX_ID (XML line 447)
- rtr_TRANS.TX_ID1 [demo_target6_GRP] (XML line 692)
- exp_TRANS1.TX_ID = TX_ID (XML line 470)
- exp_TRANS.TX_ID = TX_ID (XML line 600)
- sq_demo_source4.TX_ID (XML line 573)
- demo_source3.TX_ID (XML line 33)

### demo_target6.ACCT_KEY
- demo_target6.ACCT_KEY (XML line 105)
- SEQ_GEN.NEXTVAL (XML line 430)

### demo_target6.TX_DTTM
- demo_target6.TX_DTTM (XML line 106)
- agg_TRANS.TX_DTTM = TX_DTTM (XML line 449)
- rtr_TRANS.TX_DTTM1 [demo_target6_GRP] (XML line 691)
- exp_TRANS1.TX_DTTM = TX_DTTM (XML line 465)
- exp_TRANS.TX_DTTM = TX_DTTM (XML line 595)
- sq_demo_source4.TX_DTTM (XML line 575)
- demo_source3.TX_DTTM (XML line 37)

### demo_target6.TX_AMT
- demo_target6.TX_AMT (XML line 107)
- agg_TRANS.o_TX_AMT = SUM(TX_AMT) (XML line 454)

### demo_target6.TX_TYPE_CD
- demo_target6.TX_TYPE_CD (XML line 108)
- agg_TRANS.o_ACCT_ID = o_ACCT_ID (XML line 451)
- rtr_TRANS.o_ACCT_ID1 [demo_target6_GRP] (XML line 689)
- exp_TRANS1.o_ACCT_ID = o_ACCT_ID (XML line 477)
- exp_TRANS.o_ACCT_ID = :LKP.lkp_TRANS1(ACCT_ID) (XML line 608)
- :LKP.lkp_TRANS1(ACCT_ID) -> lkp_demo_source3.TX_TYPE_CD (XML line 608)

## demo_target5

### demo_target5.ACCT_ID
- demo_target5.ACCT_ID (XML line 111)
- rtr_TRANS.ACCT_ID2 [demo_target5_GRP] (XML line 704)
- exp_TRANS1.ACCT_ID = ACCT_ID (XML line 473)
- exp_TRANS.ACCT_ID = ACCT_ID (XML line 603)
- sq_demo_source4.ACCT_ID (XML line 566)
- demo_source4.ACCT_ID (XML line 24)

### demo_target5.FIRST_NM
- demo_target5.FIRST_NM (XML line 112)
- rtr_TRANS.FIRST_NM2 [demo_target5_GRP] (XML line 717)
- exp_TRANS1.FIRST_NM = FIRST_NM (XML line 463)
- lkp_TRANS2.FIRST_NM (XML line 486)
- lkp_demo_source1.FIRST_NM [lookup condition: ACCT_ID = IN_ACCT_ID; policy: Use Last Value] (XML line 35)

### demo_target5.LAST_NM
- demo_target5.LAST_NM (XML line 113)
- rtr_TRANS.LAST_NM2 [demo_target5_GRP] (XML line 711)
- exp_TRANS1.LAST_NM = LAST_NM (XML line 471)
- exp_TRANS.LAST_NM = LAST_NM (XML line 601)
- sq_demo_source4.LAST_NM (XML line 574)
- demo_source3.LAST_NM (XML line 36)

### demo_target5.BAL_AMT
- demo_target5.BAL_AMT (XML line 114)
- rtr_TRANS.BAL_AMT2 [demo_target5_GRP] (XML line 703)
- exp_TRANS1.BAL_AMT = BAL_AMT (XML line 466)
- exp_TRANS.BAL_AMT = BAL_AMT (XML line 596)
- sq_demo_source4.BAL_AMT (XML line 577)
- demo_source3.BAL_AMT (XML line 40)

### demo_target5.CRDT_SCORE
- demo_target5.CRDT_SCORE (XML line 115)
- rtr_TRANS.CRDT_SCORE2 [demo_target5_GRP] (XML line 718)
- exp_TRANS1.CRDT_SCORE = CRDT_SCORE (XML line 478)
- lkp_TRANS3.CRDT_SCORE (XML line 614)
- lkp_demo_source2.CRDT_SCORE [lookup condition: CUST_ID = IN_CUST_ID; policy: Use Last Value] (XML line 42)

## demo_target3

### demo_target3.PRODUCT_ID
- demo_target3.PRODUCT_ID (XML line 118)
- exp_TRANS2.PRODUCT_ID = PRODUCT_ID (XML line 659)
- SQ_demo_source5.PRODUCT_ID (XML line 738)
- demo_source5.PRODUCT_ID (XML line 55)

### demo_target3.PRODUCT_NM
- demo_target3.PRODUCT_NM (XML line 119)
- exp_TRANS2.PRODUCT_NM = PRODUCT_NM (XML line 660)
- SQ_demo_source5.PRODUCT_NM (XML line 739)
- demo_source5.PRODUCT_NM (XML line 56)

### demo_target3.PRODUCT_NO
- demo_target3.PRODUCT_NO (XML line 120)
- exp_TRANS2.PRODUCT_NO = PRODUCT_NO (XML line 654)
- SQ_demo_source5.PRODUCT_NO (XML line 740)
- demo_source5.PRODUCT_NO (XML line 57)

### demo_target3.COLOR
- demo_target3.COLOR (XML line 121)
- exp_TRANS2.COLOR = COLOR (XML line 656)
- SQ_demo_source5.COLOR (XML line 741)
- demo_source5.COLOR (XML line 58)

### demo_target3.STD_COST
- demo_target3.STD_COST (XML line 122)
- exp_TRANS2.STD_COST = STD_COST (XML line 655)
- SQ_demo_source5.STD_COST (XML line 742)
- demo_source5.STD_COST (XML line 59)

### demo_target3.LIST_PRICE
- demo_target3.LIST_PRICE (XML line 123)
- exp_TRANS2.LIST_PRICE = LIST_PRICE (XML line 661)
- SQ_demo_source5.LIST_PRICE (XML line 743)
- demo_source5.LIST_PRICE (XML line 60)

### demo_target3.SELL_ST_DT
- demo_target3.SELL_ST_DT (XML line 124)
- exp_TRANS2.o_SELL_ST_DT = TO_DATE(TO_CHAR(SYSDATE),'DD/MM/YYYY') (XML line 662)

### demo_target3.SELL_ED_DT
- demo_target3.SELL_ED_DT (XML line 125)
- exp_TRANS2.o_SELL_ED_DT = TO_DATE(SELL_ED_DT,'DD/MM/YYYY') (XML line 663)

## demo_target21

### demo_target21.Title
- demo_target21.Title (XML line 128)
- RTRTRANS.Title3 [NEWGROUP2] (XML line 1)
- EXPTRANS.Title = Title (XML line 1)
- SQ_demo_source2.Title (XML line 902)
- demo_source2.Title (XML line 65)

### demo_target21.Gender
- demo_target21.Gender (XML line 129)
- RTRTRANS.Gender_Code3 [NEWGROUP2] (XML line 1)
- EXPTRANS.Gender_Code = Gender_Code (XML line 1)
- SQ_demo_source2.Gender_Code (XML line 909)
- demo_source2.Gender_Code (XML line 72)

### demo_target21.First_Name
- demo_target21.First_Name (XML line 130)
- RTRTRANS.First_Name3 [NEWGROUP2] (XML line 1)
- EXPTRANS.First_Name = First_Name (XML line 1)
- SQ_demo_source2.First_Name (XML line 903)
- demo_source2.First_Name (XML line 66)

### demo_target21.Middle_Name
- demo_target21.Middle_Name (XML line 131)
- RTRTRANS.Middle_Name3 [NEWGROUP2] (XML line 1)
- EXPTRANS.Middle_Name = Middle_Name (XML line 1)
- SQ_demo_source2.Middle_Name (XML line 904)
- demo_source2.Middle_Name (XML line 67)

### demo_target21.Last_Name
- demo_target21.Last_Name (XML line 132)
- RTRTRANS.Last_Name3 [NEWGROUP2] (XML line 1)
- EXPTRANS.Last_Name = Last_Name (XML line 1)
- SQ_demo_source2.Last_Name (XML line 905)
- demo_source2.Last_Name (XML line 68)

### demo_target21.Member_Identifier
- demo_target21.Member_Identifier (XML line 133)
- RTRTRANS.Member_ID3 [NEWGROUP2] (XML line 1)
- EXPTRANS.Member_ID = Member_ID (XML line 1)
- SQ_demo_source2.Member_ID (XML line 906)
- demo_source2.Member_ID (XML line 69)

### demo_target21.Member_Suffix
- demo_target21.Member_Suffix (XML line 134)
- RTRTRANS.Member_Suffix3 [NEWGROUP2] (XML line 1)
- EXPTRANS.Member_Suffix = Member_Suffix (XML line 1)
- SQ_demo_source2.Member_Suffix (XML line 907)
- demo_source2.Member_Suffix (XML line 70)

### demo_target21.Date_of_Birth
- demo_target21.Date_of_Birth (XML line 135)
- RTRTRANS.Birth_Date3 [NEWGROUP2] (XML line 1)
- EXPTRANS.Birth_Date = Birth_Date (XML line 1)
- SQ_demo_source2.Birth_Date (XML line 908)
- demo_source2.Birth_Date (XML line 71)

### demo_target21.Member_Number
- demo_target21.Member_Number (XML line 136)
- RTRTRANS.Member_Record_Number3 [NEWGROUP2] (XML line 1)
- EXPTRANS.Member_Record_Number = Member_Record_Number (XML line 1)
- SQ_demo_source2.Member_Record_Number (XML line 910)
- demo_source2.Member_Record_Number (XML line 73)

### demo_target21.Soc_Number
- demo_target21.Soc_Number (XML line 137)
- RTRTRANS.Social_Security_Number3 [NEWGROUP2] (XML line 1)
- EXPTRANS.Social_Security_Number = Social_Security_Number (XML line 1)
- SQ_demo_source2.Social_Security_Number (XML line 911)
- demo_source2.Social_Security_Number (XML line 74)

### demo_target21.Type_Code
- demo_target21.Type_Code (XML line 138)
- RTRTRANS.Member_Type_Code3 [NEWGROUP2] (XML line 1)
- EXPTRANS.Member_Type_Code = Member_Type_Code (XML line 1)
- SQ_demo_source2.Member_Type_Code (XML line 912)
- demo_source2.Member_Type_Code (XML line 75)

### demo_target21.Relationship_to_Subscriber_Code
- demo_target21.Relationship_to_Subscriber_Code (XML line 139)
- RTRTRANS.Relationship_to_Subscriber_Code3 [NEWGROUP2] (XML line 1)
- EXPTRANS.Relationship_to_Subscriber_Code = Relationship_to_Subscriber_Code (XML line 1)
- SQ_demo_source2.Relationship_to_Subscriber_Code (XML line 914)
- demo_source2.Relationship_to_Subscriber_Code (XML line 77)

### demo_target21.Relationship_to_Subscriber_Code_Label
- demo_target21.Relationship_to_Subscriber_Code_Label (XML line 140)
- RTRTRANS.Relationship_to_Subscriber_Code_Label3 [NEWGROUP2] (XML line 1)
- EXPTRANS.o_Relationship_to_Subscriber_Code_Label = iif(ISNULL(Relationship_to_Subscriber_Code_Label),ABORT('Relationship_to_Subscriber_Code_Labe valuel is null'),Relationship_to_Subscriber_Code_Label) (XML line 1)

### demo_target21.Effective_Date
- demo_target21.Effective_Date (XML line 141)
- RTRTRANS.Original_Effective_Date3 [NEWGROUP2] (XML line 1)
- EXPTRANS.Original_Effective_Date = Original_Effective_Date (XML line 1)
- SQ_demo_source2.Original_Effective_Date (XML line 913)
- demo_source2.Original_Effective_Date (XML line 76)

## demo_target2

### demo_target2.Title
- demo_target2.Title (XML line 128)
- RTRTRANS.Title1 [NEWGROUP1] (XML line 1)
- EXPTRANS.Title = Title (XML line 1)
- SQ_demo_source2.Title (XML line 902)
- demo_source2.Title (XML line 65)

### demo_target2.Gender
- demo_target2.Gender (XML line 129)
- RTRTRANS.Gender_Code1 [NEWGROUP1] (XML line 1)
- EXPTRANS.Gender_Code = Gender_Code (XML line 1)
- SQ_demo_source2.Gender_Code (XML line 909)
- demo_source2.Gender_Code (XML line 72)

### demo_target2.First_Name
- demo_target2.First_Name (XML line 130)
- RTRTRANS.First_Name1 [NEWGROUP1] (XML line 1)
- EXPTRANS.First_Name = First_Name (XML line 1)
- SQ_demo_source2.First_Name (XML line 903)
- demo_source2.First_Name (XML line 66)

### demo_target2.Middle_Name
- demo_target2.Middle_Name (XML line 131)
- RTRTRANS.Middle_Name1 [NEWGROUP1] (XML line 1)
- EXPTRANS.Middle_Name = Middle_Name (XML line 1)
- SQ_demo_source2.Middle_Name (XML line 904)
- demo_source2.Middle_Name (XML line 67)

### demo_target2.Last_Name
- demo_target2.Last_Name (XML line 132)
- RTRTRANS.Last_Name1 [NEWGROUP1] (XML line 1)
- EXPTRANS.Last_Name = Last_Name (XML line 1)
- SQ_demo_source2.Last_Name (XML line 905)
- demo_source2.Last_Name (XML line 68)

### demo_target2.Member_Identifier
- demo_target2.Member_Identifier (XML line 133)
- RTRTRANS.Member_ID1 [NEWGROUP1] (XML line 1)
- EXPTRANS.Member_ID = Member_ID (XML line 1)
- SQ_demo_source2.Member_ID (XML line 906)
- demo_source2.Member_ID (XML line 69)

### demo_target2.Member_Suffix
- demo_target2.Member_Suffix (XML line 134)
- RTRTRANS.Member_Suffix1 [NEWGROUP1] (XML line 1)
- EXPTRANS.Member_Suffix = Member_Suffix (XML line 1)
- SQ_demo_source2.Member_Suffix (XML line 907)
- demo_source2.Member_Suffix (XML line 70)

### demo_target2.Date_of_Birth
- demo_target2.Date_of_Birth (XML line 135)
- RTRTRANS.Birth_Date1 [NEWGROUP1] (XML line 1)
- EXPTRANS.Birth_Date = Birth_Date (XML line 1)
- SQ_demo_source2.Birth_Date (XML line 908)
- demo_source2.Birth_Date (XML line 71)

### demo_target2.Member_Number
- demo_target2.Member_Number (XML line 136)
- RTRTRANS.Member_Record_Number1 [NEWGROUP1] (XML line 1)
- EXPTRANS.Member_Record_Number = Member_Record_Number (XML line 1)
- SQ_demo_source2.Member_Record_Number (XML line 910)
- demo_source2.Member_Record_Number (XML line 73)

### demo_target2.Soc_Number
- demo_target2.Soc_Number (XML line 137)
- RTRTRANS.Social_Security_Number1 [NEWGROUP1] (XML line 1)
- EXPTRANS.Social_Security_Number = Social_Security_Number (XML line 1)
- SQ_demo_source2.Social_Security_Number (XML line 911)
- demo_source2.Social_Security_Number (XML line 74)

### demo_target2.Type_Code
- demo_target2.Type_Code (XML line 138)
- RTRTRANS.Member_Type_Code1 [NEWGROUP1] (XML line 1)
- EXPTRANS.Member_Type_Code = Member_Type_Code (XML line 1)
- SQ_demo_source2.Member_Type_Code (XML line 912)
- demo_source2.Member_Type_Code (XML line 75)

### demo_target2.Relationship_to_Subscriber_Code
- demo_target2.Relationship_to_Subscriber_Code (XML line 139)
- RTRTRANS.Relationship_to_Subscriber_Code1 [NEWGROUP1] (XML line 1)
- EXPTRANS.Relationship_to_Subscriber_Code = Relationship_to_Subscriber_Code (XML line 1)
- SQ_demo_source2.Relationship_to_Subscriber_Code (XML line 914)
- demo_source2.Relationship_to_Subscriber_Code (XML line 77)

### demo_target2.Relationship_to_Subscriber_Code_Label
- demo_target2.Relationship_to_Subscriber_Code_Label (XML line 140)
- RTRTRANS.Relationship_to_Subscriber_Code_Label1 [NEWGROUP1] (XML line 1)
- EXPTRANS.o_Relationship_to_Subscriber_Code_Label = iif(ISNULL(Relationship_to_Subscriber_Code_Label),ABORT('Relationship_to_Subscriber_Code_Labe valuel is null'),Relationship_to_Subscriber_Code_Label) (XML line 1)

### demo_target2.Effective_Date
- demo_target2.Effective_Date (XML line 141)
- RTRTRANS.Original_Effective_Date1 [NEWGROUP1] (XML line 1)
- EXPTRANS.Original_Effective_Date = Original_Effective_Date (XML line 1)
- SQ_demo_source2.Original_Effective_Date (XML line 913)
- demo_source2.Original_Effective_Date (XML line 76)

## Dead ports (no outgoing CONNECTOR)

- `RTRTRANS.LEAD_CO_MNE11` (XML line 215)
- `RTRTRANS.BRANCH_CO_MNE11` (XML line 216)
- `RTRTRANS.MIS_DATE11` (XML line 217)
- `RTRTRANS.DESCRIPTION11` (XML line 218)
- `RTRTRANS.SHORT_NAME11` (XML line 219)
- `RTRTRANS.New_Flag1` (XML line 220)
- `RTRTRANS.Changed_Flag1` (XML line 221)
- `RTRTRANS.o_UPDATED_BY1` (XML line 224)
- `RTRTRANS.o_UPDATED_TIME1` (XML line 225)
- `RTRTRANS.Key1` (XML line 226)
- `RTRTRANS.LEAD_CO_MNE13` (XML line 233)
- `RTRTRANS.BRANCH_CO_MNE13` (XML line 234)
- `RTRTRANS.MIS_DATE13` (XML line 235)
- `RTRTRANS.DESCRIPTION13` (XML line 236)
- `RTRTRANS.SHORT_NAME13` (XML line 237)
- `RTRTRANS.LEAD_CO_MNE3` (XML line 245)
- `RTRTRANS.BRANCH_CO_MNE3` (XML line 246)
- `RTRTRANS.MIS_DATE3` (XML line 247)
- `RTRTRANS.ID2` (XML line 248)
- `RTRTRANS.DESCRIPTION3` (XML line 249)
- `RTRTRANS.SHORT_NAME3` (XML line 250)
- `RTRTRANS.LEAD_CO_MNE12` (XML line 251)
- `RTRTRANS.BRANCH_CO_MNE12` (XML line 252)
- `RTRTRANS.MIS_DATE12` (XML line 253)
- `RTRTRANS.DESCRIPTION12` (XML line 254)
- `RTRTRANS.SHORT_NAME12` (XML line 255)
- `RTRTRANS.New_Flag2` (XML line 256)
- `RTRTRANS.Changed_Flag2` (XML line 257)
- `RTRTRANS.o_CREATED_BY2` (XML line 258)
- `RTRTRANS.o_CREATED_TIME2` (XML line 259)
- `RTRTRANS.o_UPDATED_BY2` (XML line 260)
- `RTRTRANS.o_UPDATED_TIME2` (XML line 261)
- `RTRTRANS.Key2` (XML line 262)
- `SEQTRANS.CURRVAL` (XML line 431)
- `SEQ_GEN.CURRVAL` (XML line 431)
- `rtr_TRANS.BAL_AMT1` (XML line 687)
- `rtr_TRANS.ACCT_TYP1` (XML line 693)
- `rtr_TRANS.LAST_NM1` (XML line 695)
- `rtr_TRANS.FIRST_NM1` (XML line 701)
- `rtr_TRANS.CRDT_SCORE1` (XML line 702)
- `rtr_TRANS.o_ACCT_ID2` (XML line 705)
- `rtr_TRANS.o_acc_trim2` (XML line 706)
- `rtr_TRANS.TX_DTTM2` (XML line 707)
- `rtr_TRANS.TX_ID2` (XML line 708)
- `rtr_TRANS.ACCT_TYP2` (XML line 709)
- `rtr_TRANS.TX_AMT2` (XML line 710)
- `rtr_TRANS.CLSR_DT2` (XML line 712)
- `rtr_TRANS.ACCT_STAT_CD2` (XML line 713)
- `rtr_TRANS.o_ACCT_DESC2` (XML line 714)
- `rtr_TRANS.CR8_DT2` (XML line 715)
- `rtr_TRANS.o_crdt_trim2` (XML line 716)
- `rtr_TRANS.BAL_AMT3` (XML line 719)
- `rtr_TRANS.ACCT_ID3` (XML line 720)
- `rtr_TRANS.o_ACCT_ID3` (XML line 721)
- `rtr_TRANS.o_acc_trim3` (XML line 722)
- `rtr_TRANS.TX_DTTM3` (XML line 723)
- `rtr_TRANS.TX_ID3` (XML line 724)
- `rtr_TRANS.ACCT_TYP3` (XML line 725)
- `rtr_TRANS.TX_AMT3` (XML line 726)
- `rtr_TRANS.LAST_NM3` (XML line 727)
- `rtr_TRANS.CLSR_DT3` (XML line 728)
- `rtr_TRANS.ACCT_STAT_CD3` (XML line 729)
- `rtr_TRANS.o_ACCT_DESC3` (XML line 730)
- `rtr_TRANS.CR8_DT3` (XML line 731)
- `rtr_TRANS.o_crdt_trim3` (XML line 732)
- `rtr_TRANS.FIRST_NM3` (XML line 733)
- `rtr_TRANS.CRDT_SCORE3` (XML line 734)
- `RTRTRANS.Title2` (XML line 993)
- `RTRTRANS.First_Name2` (XML line 994)
- `RTRTRANS.Middle_Name2` (XML line 995)
- `RTRTRANS.Last_Name2` (XML line 996)
- `RTRTRANS.Member_ID2` (XML line 997)
- `RTRTRANS.Member_Suffix2` (XML line 998)
- `RTRTRANS.Birth_Date2` (XML line 999)
- `RTRTRANS.Gender_Code2` (XML line 1000)
- `RTRTRANS.Member_Record_Number2` (XML line 1001)
- `RTRTRANS.Social_Security_Number2` (XML line 1002)
- `RTRTRANS.Member_Type_Code2` (XML line 1003)
- `RTRTRANS.Original_Effective_Date2` (XML line 1004)
- `RTRTRANS.Relationship_to_Subscriber_Code2` (XML line 1005)
- `RTRTRANS.Relationship_to_Subscriber_Code_Label2` (XML line 1006)

## Recovered connector-graph checks

- **demo_target5 lookup FIRST_NM: ASSERTION PASS** — demo_target5.FIRST_NM (XML line 112); rtr_TRANS.FIRST_NM2 [demo_target5_GRP] (XML line 717); exp_TRANS1.FIRST_NM = FIRST_NM (XML line 463); lkp_TRANS2.FIRST_NM (XML line 486); lkp_demo_source1.FIRST_NM [lookup condition: ACCT_ID = IN_ACCT_ID; policy: Use Last Value] (XML line 35)
- **demo_target5 lookup CRDT_SCORE: ASSERTION PASS** — demo_target5.CRDT_SCORE (XML line 115); rtr_TRANS.CRDT_SCORE2 [demo_target5_GRP] (XML line 718); exp_TRANS1.CRDT_SCORE = CRDT_SCORE (XML line 478); lkp_TRANS3.CRDT_SCORE (XML line 614); lkp_demo_source2.CRDT_SCORE [lookup condition: CUST_ID = IN_CUST_ID; policy: Use Last Value] (XML line 42)
- **demo_target6 lookup TX_TYPE_CD: ASSERTION PASS** — demo_target6.TX_TYPE_CD (XML line 108); agg_TRANS.o_ACCT_ID = o_ACCT_ID (XML line 451); rtr_TRANS.o_ACCT_ID1 [demo_target6_GRP] (XML line 689); exp_TRANS1.o_ACCT_ID = o_ACCT_ID (XML line 477); exp_TRANS.o_ACCT_ID = :LKP.lkp_TRANS1(ACCT_ID) (XML line 608); :LKP.lkp_TRANS1(ACCT_ID) -> lkp_demo_source3.TX_TYPE_CD (XML line 608)
- **demo_target6 positional SYSTIMESTAMP: ASSERTION PASS** — derived from the connector graph and XML transformation metadata
- **mapping2 router GROUP: ASSERTION PASS** — derived from the connector graph and XML transformation metadata
- **mapping3 router groups: ASSERTION PASS** — derived from the connector graph and XML transformation metadata
