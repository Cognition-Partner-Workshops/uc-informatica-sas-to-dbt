WITH lookup_reference AS
(
   SELECT
      CUST_ID ,
      CRDT_SCORE ,
      MAX_CRDT_SCORE ,
      MIN_CRDT_SCORE ,
      MAX_CRDT_LMT ,
      CURR_CRDT_BAL_AMT ,
      AVG_INC_AMT
   FROM
      {{ source('raw', 'lkp_demo_source2') }}
   QUALIFY
      ROW_NUMBER() OVER (
      PARTITION BY
         CUST_ID
      ORDER BY
         SEED_ROW DESC) = 1
),
input_data AS
(
   SELECT
      exp_TRANS__IN_CUST_ID IN_CUST_ID,
      exp_TRANS__CLSR_DT ,
      exp_TRANS__TX_DTTM ,
      exp_TRANS__BAL_AMT ,
      exp_TRANS__ACCT_DESC ,
      exp_TRANS__ACCT_TYP ,
      exp_TRANS__ACCT_STAT_CD ,
      exp_TRANS__TX_ID ,
      exp_TRANS__LAST_NM ,
      exp_TRANS__TX_AMT ,
      exp_TRANS__ACCT_ID ,
      exp_TRANS__CR8_DT ,
      exp_TRANS__o_acc_trim ,
      exp_TRANS__o_crdt_trim ,
      exp_TRANS__o_ACCT_ID ,
      FIRST_NM lkp_TRANS2__FIRST_NM
   FROM
      {{ ref('int_m_demo_mapping1__lkp_trans2') }}
)
SELECT
   input_data.IN_CUST_ID ,
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
   input_data.lkp_TRANS2__FIRST_NM ,
   lookup_reference.CUST_ID,
   lookup_reference.CRDT_SCORE,
   lookup_reference.MAX_CRDT_SCORE,
   lookup_reference.MIN_CRDT_SCORE,
   lookup_reference.MAX_CRDT_LMT,
   lookup_reference.CURR_CRDT_BAL_AMT,
   lookup_reference.AVG_INC_AMT
FROM
   input_data
   LEFT JOIN
      lookup_reference
      ON lookup_reference.CUST_ID = input_data.IN_CUST_ID