from pyspark.sql.types import (
    DateType,
    DoubleType,
    LongType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)


def _schema(fields):
    return StructType([StructField(name, typ, True) for name, typ in fields])


SOURCE_SCHEMAS = {
    "demo_source1": _schema([(x, StringType()) for x in
        ("LEAD_CO_MNE", "BRANCH_CO_MNE", "MIS_DATE", "ID", "DESCRIPTION", "SHORT_NAME")]),
    "demo_source2": _schema([
        ("Title", StringType()), ("First_Name", StringType()), ("Middle_Name", StringType()),
        ("Last_Name", StringType()), ("Member_ID", DoubleType()), ("Member_Suffix", StringType()),
        ("Birth_Date", TimestampType()), ("Gender_Code", StringType()),
        ("Member_Record_Number", DoubleType()), ("Social_Security_Number", DoubleType()),
        ("Member_Type_Code", DoubleType()), ("Original_Effective_Date", TimestampType()),
        ("Relationship_to_Subscriber_Code", DoubleType()),
        ("Relationship_to_Subscriber_Code_Label", StringType()),
    ]),
    "demo_source3": _schema([
        ("TX_ID", LongType()), ("ACCT_ID", LongType()), ("FIRST_NM", StringType()),
        ("LAST_NM", StringType()), ("TX_DTTM", TimestampType()), ("TX_AMT", DoubleType()),
        ("TX_TYPE_CD", StringType()), ("BAL_AMT", DoubleType()), ("TX_DESC", StringType()),
        ("CRDT_SCORE", LongType()), ("CUST_ID", LongType()),
    ]),
    "demo_source4": _schema([
        ("ACCT_ID", LongType()), ("ACCT_TYP", StringType()), ("ACCT_DESC", StringType()),
        ("CRDT_LN", StringType()), ("CR8_DT", DateType()), ("CLSR_DT", DateType()),
        ("ACCT_STAT_CD", StringType()),
    ]),
    "demo_source5": _schema([(x, StringType()) for x in
        ("PRODUCT_ID", "PRODUCT_NM", "PRODUCT_NO", "COLOR", "STD_COST", "LIST_PRICE",
         "SELL_ST_DT", "SELL_ED_DT")]),
}
LOOKUP_SCHEMAS = {
    "lkp_demo_source1": _schema([
        ("ACCT_ID", LongType()), ("CUST_ID", LongType()), ("FIRST_NM", StringType()),
        ("LAST_NM", StringType()), ("CUST_ADDR", StringType()), ("CUST_PHN", StringType()),
        ("CUST_EML_ADDR", StringType()), ("AGE", StringType()), ("DOB", StringType()),
        ("CUST_TYP", StringType()),
    ]),
    "lkp_demo_source2": _schema([
        ("CUST_ID", LongType()), ("CRDT_SCORE", LongType()), ("MAX_CRDT_SCORE", LongType()),
        ("MIN_CRDT_SCORE", LongType()), ("MAX_CRDT_LMT", LongType()),
        ("CURR_CRDT_BAL_AMT", DoubleType()), ("AVG_INC_AMT", DoubleType()),
    ]),
    "lkp_demo_source3": _schema([
        ("ACCT_ID", LongType()), ("TX_TYPE_CD", StringType()), ("TX_TYPE_DESC", StringType()),
    ]),
}
TARGET_SCHEMAS = {
    "demo_target1": _schema([
        ("Key", DoubleType()), ("LEAD_CO_MNE", StringType()), ("BRANCH_CO_MNE", StringType()),
        ("MIS_DATE", StringType()), ("ID", StringType()), ("DESCRIPTION", StringType()),
        ("SHORT_NAME", StringType()), ("CREATED_BY", StringType()), ("CREATED_TIME", TimestampType()),
        ("UPDATED_BY", StringType()), ("UPDATED_TIME", TimestampType()), ("ACTIVE_FLAG", StringType()),
        ("START_DATE", TimestampType()), ("END_DATE", TimestampType()),
    ]),
    "demo_target2": _schema([
        ("Title", StringType()), ("Gender", StringType()), ("First_Name", StringType()),
        ("Middle_Name", StringType()), ("Last_Name", StringType()), ("Member_Identifier", DoubleType()),
        ("Member_Suffix", StringType()), ("Date_of_Birth", TimestampType()), ("Member_Number", DoubleType()),
        ("Soc_Number", DoubleType()), ("Type_Code", DoubleType()), ("Relationship_to_Subscriber_Code", DoubleType()),
        ("Relationship_to_Subscriber_Code_Label", StringType()), ("Effective_Date", TimestampType()),
    ]),
    "demo_target21": _schema([
        ("Title", StringType()), ("Gender", StringType()), ("First_Name", StringType()),
        ("Middle_Name", StringType()), ("Last_Name", StringType()), ("Member_Identifier", DoubleType()),
        ("Member_Suffix", StringType()), ("Date_of_Birth", TimestampType()), ("Member_Number", DoubleType()),
        ("Soc_Number", DoubleType()), ("Type_Code", DoubleType()), ("Relationship_to_Subscriber_Code", DoubleType()),
        ("Relationship_to_Subscriber_Code_Label", StringType()), ("Effective_Date", TimestampType()),
    ]),
    "demo_target3": _schema([
        ("PRODUCT_ID", StringType()), ("PRODUCT_NM", StringType()),
        ("PRODUCT_NO", StringType()), ("COLOR", StringType()),
        ("STD_COST", StringType()), ("LIST_PRICE", StringType()),
        ("SELL_ST_DT", DateType()), ("SELL_ED_DT", DateType()),
    ]),
    "demo_target5": _schema([
        ("ACCT_ID", LongType()), ("FIRST_NM", StringType()),
        ("LAST_NM", StringType()), ("BAL_AMT", DoubleType()),
        ("CRDT_SCORE", LongType()),
    ]),
    "demo_target6": _schema([
        ("ACCT_ID", LongType()), ("ACCT_TYP", StringType()), ("ACCT_DESC", StringType()),
        ("CR8_DT", DateType()), ("CRDT_LN", StringType()), ("CLSR_DT", DateType()),
        ("ACCT_STAT_CD", StringType()), ("TX_ID", LongType()), ("ACCT_KEY", LongType()),
        ("TX_DTTM", TimestampType()), ("TX_AMT", DoubleType()), ("TX_TYPE_CD", StringType()),
    ]),
}
TARGET_SCHEMAS["demo_target1_INS"] = TARGET_SCHEMAS["demo_target1"]
TARGET_SCHEMAS["demo_target1_UPD"] = TARGET_SCHEMAS["demo_target1"]
