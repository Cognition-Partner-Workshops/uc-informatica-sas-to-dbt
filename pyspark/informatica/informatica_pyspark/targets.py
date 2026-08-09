PHYSICAL_TARGETS = {
    "demo_target1": ["Key", "LEAD_CO_MNE", "BRANCH_CO_MNE", "MIS_DATE", "ID", "DESCRIPTION",
                     "SHORT_NAME", "CREATED_BY", "CREATED_TIME", "UPDATED_BY", "UPDATED_TIME",
                     "ACTIVE_FLAG", "START_DATE", "END_DATE"],
    "demo_target6": ["ACCT_ID", "ACCT_TYP", "ACCT_DESC", "CR8_DT", "CRDT_LN", "CLSR_DT",
                     "ACCT_STAT_CD", "TX_ID", "ACCT_KEY", "TX_DTTM", "TX_AMT", "TX_TYPE_CD"],
    "demo_target5": ["ACCT_ID", "FIRST_NM", "LAST_NM", "BAL_AMT", "CRDT_SCORE"],
    "demo_target3": ["PRODUCT_ID", "PRODUCT_NM", "PRODUCT_NO", "COLOR", "STD_COST",
                     "LIST_PRICE", "SELL_ST_DT", "SELL_ED_DT"],
    "demo_target2": ["Title", "Gender", "First_Name", "Middle_Name", "Last_Name",
                     "Member_Identifier", "Member_Suffix", "Date_of_Birth", "Member_Number",
                     "Soc_Number", "Type_Code", "Relationship_to_Subscriber_Code",
                     "Relationship_to_Subscriber_Code_Label", "Effective_Date"],
}

TARGET_INSTANCES = {
    "demo_target1_INS": "demo_target1",
    "demo_target1_UPD": "demo_target1",
    "demo_target2": "demo_target2",
    "demo_target21": "demo_target2",
    "demo_target3": "demo_target3",
    "demo_target5": "demo_target5",
    "demo_target6": "demo_target6",
}


def columns_for(instance: str) -> list[str]:
    return PHYSICAL_TARGETS[TARGET_INSTANCES[instance]].copy()
