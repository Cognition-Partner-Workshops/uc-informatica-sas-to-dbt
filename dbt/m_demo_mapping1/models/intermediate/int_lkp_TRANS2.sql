WITH lookup_reference AS
(
   SELECT
      CUST_ID ,
      ACCT_ID ,
      FIRST_NM ,
      LAST_NM ,
      CUST_ADDR ,
      CUST_PHN ,
      CUST_EML_ADDR ,
      AGE ,
      DOB ,
      CUST_TYP
   FROM
      {{ source('raw', 'lkp_demo_source1') }}
   QUALIFY
      ROW_NUMBER() OVER (
      PARTITION BY
         ACCT_ID
      ORDER BY
         (
            SELECT
               --** SSC-FDM-INF0001 - Use Last Value POLICY REQUIRES PROPER ORDERING WHEN MULTIPLE ROWS MATCH. REPLACE NULL WITH APPROPRIATE ORDER BY COLUMN(S) TO ENSURE DETERMINISTIC MATCH SELECTION. **
               null
         )) = 1
),
input_data AS
(
   SELECT
      ACCT_ID IN_ACCT_ID,
      CLSR_DT exp_TRANS__CLSR_DT,
      TX_DTTM exp_TRANS__TX_DTTM,
      BAL_AMT exp_TRANS__BAL_AMT,
      ACCT_DESC exp_TRANS__ACCT_DESC,
      ACCT_TYP exp_TRANS__ACCT_TYP,
      ACCT_STAT_CD exp_TRANS__ACCT_STAT_CD,
      TX_ID exp_TRANS__TX_ID,
      LAST_NM exp_TRANS__LAST_NM,
      TX_AMT exp_TRANS__TX_AMT,
      ACCT_ID exp_TRANS__ACCT_ID,
      CR8_DT exp_TRANS__CR8_DT,
      o_acc_trim exp_TRANS__o_acc_trim,
      o_crdt_trim exp_TRANS__o_crdt_trim,
      o_ACCT_ID exp_TRANS__o_ACCT_ID,
      CUST_ID exp_TRANS__IN_CUST_ID
   FROM
      {{ ref('int_exp_TRANS') }}
)
SELECT
   input_data.IN_ACCT_ID ,
   input_data.exp_TRANS__CLSR_DT ,
   input_data.exp_TRANS__TX_DTTM ,
   input_data.exp_TRANS__BAL_AMT ,
   input_data.exp_TRANS__ACCT_DESC ,
   input_data.exp_TRANS__ACCT_TYP ,
   input_data.exp_TRANS__ACCT_STAT_CD ,
   input_data.exp_TRANS__TX_ID ,
   input_data.exp_TRANS__LAST_NM ,
   input_data.exp_TRANS__TX_AMT ,
   input_data.exp_TRANS__ACCT_ID ,
   input_data.exp_TRANS__CR8_DT ,
   input_data.exp_TRANS__o_acc_trim ,
   input_data.exp_TRANS__o_crdt_trim ,
   input_data.exp_TRANS__o_ACCT_ID ,
   input_data.exp_TRANS__IN_CUST_ID ,
   lookup_reference.CUST_ID,
   lookup_reference.ACCT_ID,
   lookup_reference.FIRST_NM,
   lookup_reference.LAST_NM,
   lookup_reference.CUST_ADDR,
   lookup_reference.CUST_PHN,
   lookup_reference.CUST_EML_ADDR,
   lookup_reference.AGE,
   lookup_reference.DOB,
   lookup_reference.CUST_TYP
FROM
   input_data
   LEFT JOIN
      lookup_reference
      ON lookup_reference.ACCT_ID = input_data.IN_ACCT_ID