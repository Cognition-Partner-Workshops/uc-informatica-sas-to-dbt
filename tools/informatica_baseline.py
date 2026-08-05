#!/usr/bin/env python3
"""Deterministic baseline for the three Informatica mappings.

Executes the legacy semantics documented in docs/stm/informatica_stm.md against
the seed CSVs in legacy/informatica/data/, writing one CSV per target instance
into baseline/informatica/. All SYSDATE/SYSTIMESTAMP references are pinned to
the business date 2024-01-31. DuckDB is used as the execution engine.

Faithful anomalies preserved (see STM notes):
- m_demo_mapping2 MD5_src = AES_DECRYPT(plaintext, 3-char key, 256) is always
  NULL, so Changed_Flag is never 'Update' and demo_target1_UPD gets zero rows.
- m_demo_mapping1 CR8_DT is the pinned SYSTIMESTAMP from the SQL override; the
  STRCMP(...) result in the TX_TYPE_CD port is discarded (never connected).
- m_demo_mapping1 exp_TRANS2.o_SELL_ST_DT (TO_DATE(TO_CHAR(SYSDATE),
  'DD/MM/YYYY')) is unparseable on the run date and yields NULL.
- Aggregator pass-through ports return the last row per ACCT_ID group; "last"
  is defined deterministically as highest TX_ID.
"""
import os

import duckdb
import pandas as pd

DATA = os.path.join("legacy", "informatica", "data")
OUT = os.path.join("baseline", "informatica")
BUSINESS_DATE = "2024-01-31"


def load(con):
    def path(f):
        return os.path.join(DATA, f).replace("\\", "/")

    con.execute(f"""
        CREATE OR REPLACE TABLE demo_source1 AS
        SELECT * FROM read_csv('{path('demo_source1.csv')}', header=true, columns={{
            'LEAD_CO_MNE':'VARCHAR','BRANCH_CO_MNE':'VARCHAR','MIS_DATE':'VARCHAR',
            'ID':'VARCHAR','DESCRIPTION':'VARCHAR','SHORT_NAME':'VARCHAR'}})""")
    con.execute(f"""
        CREATE OR REPLACE TABLE demo_target1_pre AS
        SELECT * FROM read_csv('{path('demo_target1.csv')}', header=true, columns={{
            'Key':'DOUBLE','LEAD_CO_MNE':'VARCHAR','BRANCH_CO_MNE':'VARCHAR',
            'MIS_DATE':'VARCHAR','ID':'VARCHAR','DESCRIPTION':'VARCHAR',
            'SHORT_NAME':'VARCHAR','CREATED_BY':'VARCHAR','CREATED_TIME':'TIMESTAMP',
            'UPDATED_BY':'VARCHAR','UPDATED_TIME':'TIMESTAMP','ACTIVE_FLAG':'VARCHAR',
            'START_DATE':'TIMESTAMP','END_DATE':'TIMESTAMP'}})""")
    con.execute(f"""
        CREATE OR REPLACE TABLE demo_source4 AS
        SELECT * FROM read_csv('{path('demo_source4.csv')}', header=true, columns={{
            'ACCT_ID':'BIGINT','ACCT_TYP':'VARCHAR','ACCT_DESC':'VARCHAR',
            'CRDT_LN':'VARCHAR','CR8_DT':'DATE','CLSR_DT':'DATE',
            'ACCT_STAT_CD':'VARCHAR'}})""")
    con.execute(f"""
        CREATE OR REPLACE TABLE demo_source3 AS
        SELECT * FROM read_csv('{path('demo_source3.csv')}', header=true, columns={{
            'TX_ID':'BIGINT','ACCT_ID':'BIGINT','FIRST_NM':'VARCHAR',
            'LAST_NM':'VARCHAR','TX_DTTM':'TIMESTAMP','TX_AMT':'DOUBLE',
            'TX_TYPE_CD':'VARCHAR','BAL_AMT':'DOUBLE','TX_DESC':'VARCHAR',
            'CRDT_SCORE':'BIGINT','CUST_ID':'BIGINT'}})""")
    con.execute(f"""
        CREATE OR REPLACE TABLE lkp_demo_source1 AS
        SELECT * FROM read_csv('{path('lkp_demo_source1.csv')}', header=true, columns={{
            'ACCT_ID':'BIGINT','CUST_ID':'BIGINT','FIRST_NM':'VARCHAR',
            'LAST_NM':'VARCHAR','CUST_ADDR':'VARCHAR','CUST_PHN':'VARCHAR',
            'CUST_EML_ADDR':'VARCHAR','AGE':'VARCHAR','DOB':'VARCHAR',
            'CUST_TYP':'VARCHAR'}})""")
    con.execute(f"""
        CREATE OR REPLACE TABLE lkp_demo_source2 AS
        SELECT * FROM read_csv('{path('lkp_demo_source2.csv')}', header=true, columns={{
            'CUST_ID':'BIGINT','CRDT_SCORE':'BIGINT','MAX_CRDT_SCORE':'BIGINT',
            'MIN_CRDT_SCORE':'BIGINT','MAX_CRDT_LMT':'BIGINT',
            'CURR_CRDT_BAL_AMT':'DOUBLE','AVG_INC_AMT':'DOUBLE'}})""")
    con.execute(f"""
        CREATE OR REPLACE TABLE lkp_demo_source3 AS
        SELECT * FROM read_csv('{path('lkp_demo_source3.csv')}', header=true, columns={{
            'ACCT_ID':'BIGINT','TX_TYPE_CD':'VARCHAR','TX_TYPE_DESC':'VARCHAR'}})""")
    con.execute(f"""
        CREATE OR REPLACE TABLE demo_source5 AS
        SELECT * FROM read_csv('{path('demo_source5.csv')}', header=true, columns={{
            'PRODUCT_ID':'VARCHAR','PRODUCT_NM':'VARCHAR','PRODUCT_NO':'VARCHAR',
            'COLOR':'VARCHAR','STD_COST':'VARCHAR','LIST_PRICE':'VARCHAR',
            'SELL_ST_DT':'VARCHAR','SELL_ED_DT':'VARCHAR'}})""")
    con.execute(f"""
        CREATE OR REPLACE TABLE demo_source2 AS
        SELECT * FROM read_csv('{path('demo_source2.csv')}', header=true, columns={{
            'Title':'VARCHAR','First_Name':'VARCHAR','Middle_Name':'VARCHAR',
            'Last_Name':'VARCHAR','Member_ID':'DOUBLE','Member_Suffix':'VARCHAR',
            'Birth_Date':'TIMESTAMP','Gender_Code':'VARCHAR',
            'Member_Record_Number':'DOUBLE','Social_Security_Number':'DOUBLE',
            'Member_Type_Code':'DOUBLE','Original_Effective_Date':'TIMESTAMP',
            'Relationship_to_Subscriber_Code':'DOUBLE',
            'Relationship_to_Subscriber_Code_Label':'VARCHAR'}})""")


def mapping1(con):
    # sq_demo_source4 SQL override: inner join + pinned SYSTIMESTAMP into
    # CR8_DT; the STRCMP(...) column is computed but never used downstream.
    con.execute(f"""
        CREATE OR REPLACE TEMP VIEW m1_sq AS
        SELECT s4.ACCT_ID, s4.ACCT_TYP, s4.ACCT_DESC, s4.CRDT_LN,
               TIMESTAMP '{BUSINESS_DATE} 00:00:00' AS CR8_DT,
               s4.CLSR_DT, s4.ACCT_STAT_CD,
               s3.TX_ID, s3.LAST_NM, s3.TX_DTTM, s3.TX_AMT, s3.BAL_AMT, s3.CUST_ID
        FROM demo_source3 s3
        INNER JOIN demo_source4 s4 ON s3.ACCT_ID = s4.ACCT_ID""")
    con.execute("""
        CREATE OR REPLACE TEMP VIEW m1_enriched AS
        SELECT q.*,
               RTRIM(q.ACCT_TYP) AS o_acc_trim,
               LTRIM(q.CRDT_LN)  AS o_crdt_trim,
               l3.TX_TYPE_CD     AS o_ACCT_ID,
               RTRIM(q.ACCT_DESC) AS o_ACCT_DESC,
               l1.FIRST_NM       AS FIRST_NM,
               l2.CRDT_SCORE     AS CRDT_SCORE
        FROM m1_sq q
        LEFT JOIN lkp_demo_source3 l3 ON l3.ACCT_ID = q.ACCT_ID
        LEFT JOIN lkp_demo_source1 l1 ON l1.ACCT_ID = q.ACCT_ID
        LEFT JOIN lkp_demo_source2 l2 ON l2.CUST_ID = q.CUST_ID""")

    t5 = con.execute("""
        SELECT ACCT_ID, FIRST_NM, LAST_NM, BAL_AMT, CRDT_SCORE
        FROM m1_enriched WHERE ACCT_TYP != 'SB'
        ORDER BY ACCT_ID, BAL_AMT""").fetch_df()
    save(t5, "demo_target5")

    t6 = con.execute("""
        WITH sb AS (
            SELECT *,
                   ROW_NUMBER() OVER (PARTITION BY ACCT_ID ORDER BY TX_ID DESC) AS rn,
                   SUM(TX_AMT) OVER (PARTITION BY ACCT_ID) AS sum_tx_amt
            FROM m1_enriched WHERE ACCT_TYP = 'SB'
        )
        SELECT ACCT_ID,
               o_acc_trim  AS ACCT_TYP,
               o_ACCT_DESC AS ACCT_DESC,
               CR8_DT,
               CAST(o_crdt_trim AS BIGINT) AS CRDT_LN,
               CLSR_DT,
               ACCT_STAT_CD,
               TX_ID,
               280 + ROW_NUMBER() OVER (ORDER BY ACCT_ID) AS ACCT_KEY,
               TX_DTTM,
               sum_tx_amt AS TX_AMT,
               o_ACCT_ID  AS TX_TYPE_CD
        FROM sb WHERE rn = 1
        ORDER BY ACCT_ID""").fetch_df()
    save(t6, "demo_target6")

    t3 = con.execute("""
        SELECT PRODUCT_ID, PRODUCT_NM, PRODUCT_NO, COLOR,
               CAST(STD_COST AS BIGINT) AS STD_COST,
               CAST(LIST_PRICE AS BIGINT) AS LIST_PRICE,
               CAST(NULL AS DATE) AS SELL_ST_DT,
               CAST(SUBSTR(SELL_ED_DT,7,4) || '-' || SUBSTR(SELL_ED_DT,4,2)
                    || '-' || SUBSTR(SELL_ED_DT,1,2) AS DATE) AS SELL_ED_DT
        FROM demo_source5 ORDER BY PRODUCT_ID""").fetch_df()
    save(t3, "demo_target3")


def mapping2(con):
    con.execute("""
        CREATE OR REPLACE TEMP VIEW m2_exp AS
        SELECT s.*,
               p."Key" AS Key,
               p.LEAD_CO_MNE AS LEAD_CO_MNE1,
               CASE WHEN p."Key" IS NULL THEN 'Insert' END AS New_Flag,
               -- AES_DECRYPT of a plaintext value with a 3-char key: always NULL
               CAST(NULL AS VARCHAR) AS MD5_src,
               MD5(s.LEAD_CO_MNE || s.BRANCH_CO_MNE || s.MIS_DATE
                   || s.DESCRIPTION || s.SHORT_NAME) AS MD5_tgt,
               -- (MD5_tgt != NULL) is NULL, so Changed_Flag is never 'Update'
               CAST(NULL AS VARCHAR) AS Changed_Flag,
               'IDWUSER' AS o_CREATED_BY,
               TIMESTAMP '2024-01-31 00:00:00' AS o_CREATED_TIME,
               'IDWUSER' AS o_UPDATED_BY,
               TIMESTAMP '2024-01-31 00:00:00' AS o_UPDATED_TIME
        FROM demo_source1 s
        LEFT JOIN demo_target1_pre p ON p.ID = s.ID""")

    ins = con.execute("""
        SELECT 56 + ROW_NUMBER() OVER (ORDER BY ID) AS "Key",
               LEAD_CO_MNE, BRANCH_CO_MNE, MIS_DATE, ID, DESCRIPTION, SHORT_NAME,
               o_CREATED_BY AS CREATED_BY, o_CREATED_TIME AS CREATED_TIME,
               CAST(NULL AS VARCHAR) AS UPDATED_BY,
               CAST(NULL AS TIMESTAMP) AS UPDATED_TIME,
               CAST(NULL AS VARCHAR) AS ACTIVE_FLAG,
               CAST(NULL AS TIMESTAMP) AS START_DATE,
               CAST(NULL AS TIMESTAMP) AS END_DATE
        FROM m2_exp WHERE New_Flag = 'Insert' ORDER BY ID""").fetch_df()
    save(ins, "demo_target1_INS")

    upd = con.execute("""
        SELECT "Key", LEAD_CO_MNE, BRANCH_CO_MNE, MIS_DATE, ID, DESCRIPTION,
               SHORT_NAME,
               CAST(NULL AS VARCHAR) AS CREATED_BY,
               CAST(NULL AS TIMESTAMP) AS CREATED_TIME,
               o_UPDATED_BY AS UPDATED_BY, o_UPDATED_TIME AS UPDATED_TIME,
               CAST(NULL AS VARCHAR) AS ACTIVE_FLAG,
               CAST(NULL AS TIMESTAMP) AS START_DATE,
               CAST(NULL AS TIMESTAMP) AS END_DATE
        FROM m2_exp WHERE Changed_Flag = 'Update' ORDER BY ID""").fetch_df()
    save(upd, "demo_target1_UPD")


def mapping3(con):
    n_bad = con.execute("""
        SELECT COUNT(*) FROM demo_source2
        WHERE Member_Type_Code IS NOT NULL
          AND Relationship_to_Subscriber_Code_Label IS NULL""").fetchone()[0]
    if n_bad:
        raise SystemExit(
            "ABORT('Relationship_to_Subscriber_Code_Labe valuel is null') — "
            f"{n_bad} filtered-in rows have a NULL label")

    base = """
        SELECT Title, Gender_Code AS Gender, First_Name, Middle_Name, Last_Name,
               Member_ID AS Member_Identifier, Member_Suffix,
               Birth_Date AS Date_of_Birth,
               Member_Record_Number AS Member_Number,
               Social_Security_Number AS Soc_Number,
               Member_Type_Code AS Type_Code,
               Relationship_to_Subscriber_Code,
               Relationship_to_Subscriber_Code_Label,
               Original_Effective_Date AS Effective_Date
        FROM demo_source2
        WHERE Member_Type_Code IS NOT NULL AND Social_Security_Number IS {}
        ORDER BY Member_ID"""
    save(con.execute(base.format("NULL")).fetch_df(), "demo_target2")
    save(con.execute(base.format("NOT NULL")).fetch_df(), "demo_target21")


def save(df: pd.DataFrame, name: str):
    os.makedirs(OUT, exist_ok=True)
    df = df.copy()
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime("%Y-%m-%d %H:%M:%S").str.replace(
                " 00:00:00", "", regex=False)
    path = os.path.join(OUT, f"{name}.csv")
    df.to_csv(path, index=False)
    print(f"wrote {path} ({len(df)} rows)")


def main():
    con = duckdb.connect()
    load(con)
    mapping1(con)
    mapping2(con)
    mapping3(con)


if __name__ == "__main__":
    main()
