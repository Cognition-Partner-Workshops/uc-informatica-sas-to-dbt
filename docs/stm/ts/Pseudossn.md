# PowerCenter STM: `Pseudossn`

Derived deterministically from `legacy/informatica_ts/Pseudossn` by `tools/ts_lineage.py`. Personal identifiers are redacted as `<owner>`, `<path>`, `<email>`.

| Mappings | Sessions | Sources | Targets | Transformations | Mapplets |
|---|---|---|---|---|---|
| 10 | 10 | 5 | 9 | 74 | 0 |

Transformations by type: Aggregator 2, Expression 32, Filter 10, Joiner 1, Lookup Procedure 12, Normalizer 2, Router 1, Sorter 2, Source Qualifier 11, Update Strategy 1

## Workflow `wf_Pseudossn`

Session order:

1. `s_Pseudossn_Verify_Header_Date_Current_Pay_Period` → mapping `m_Pseudossn_Verify_Header_Date_Current_Pay_Period`
2. `s_Pseudossn_Verify_Record_Count` → mapping `m_Pseudossn_Verify_Record_Count`
3. `s_Pseudossn_Verify_Header_Date_Current_Pay_Period_Pseudossn_From_SDA` → mapping `m_Pseudossn_Verify_Header_Date_Current_Pay_Period_Pseudossn_From_SDA`
4. `s_Pseudossn_Current_Pay_Period` → mapping `m_Pseudossn_Current_Pay_Period`
5. `s_Pseudossn_Load_Archive_Pseudossn_Tbl` → mapping `m_Pseudossn_Load_Archive_Pseudossn_Tbl_v1`
6. `s_Pseudossn_Load_Pseudossn_Tbl` → mapping `m_Pseudossn_Load_Pseudossn_Tbl`
7. `s_Pseudossn_Load_Pseudossn_From_SDA_Tbl` → mapping `m_Pseudossn_Load_Pseudossn_From_SDA_Tbl`
8. `s_Pseudossn_Update_Timekeeper_Number` → mapping `m_Pseudossn_Update_Timekeeper_Number`
9. `s_Pseudossn_Load_SDA_Records_Pseudossn_Tbl` → mapping `m_Pseudossn_Load_SDA_Records_Pseudossn_Tbl`
10. `s_Pseudossn_Counters` → mapping `m_Pseudossn_Counters`

| From | To | Condition |
|---|---|---|
| s_Pseudossn_Counters | Email_Pseudossn | $s_Pseudossn_Counters.Status = Succeeded |
| Start | s_Pseudossn_Verify_Header_Date_Current_Pay_Period | — |
| s_Pseudossn_Load_SDA_Records_Pseudossn_Tbl | s_Pseudossn_Counters | $s_Pseudossn_Load_SDA_Records_Pseudossn_Tbl.Status = Succeeded |
| s_Pseudossn_Verify_Header_Date_Current_Pay_Period | s_Pseudossn_Verify_Record_Count | $s_Pseudossn_Verify_Header_Date_Current_Pay_Period.Status = Succeeded |
| s_Pseudossn_Load_Archive_Pseudossn_Tbl | s_Pseudossn_Load_Pseudossn_Tbl | $s_Pseudossn_Load_Archive_Pseudossn_Tbl.Status = Succeeded |
| s_Pseudossn_Current_Pay_Period | s_Pseudossn_Load_Archive_Pseudossn_Tbl | $s_Pseudossn_Current_Pay_Period.Status = Succeeded |
| s_Pseudossn_Verify_Header_Date_Current_Pay_Period_Pseudossn_From_SDA | s_Pseudossn_Current_Pay_Period | $s_Pseudossn_Verify_Header_Date_Current_Pay_Period_Pseudossn_From_SDA.Status = Succeeded |
| s_Pseudossn_Verify_Record_Count | s_Pseudossn_Verify_Header_Date_Current_Pay_Period_Pseudossn_From_SDA | $s_Pseudossn_Verify_Record_Count.Status = Succeeded |
| s_Pseudossn_Load_Pseudossn_From_SDA_Tbl | s_Pseudossn_Update_Timekeeper_Number | $s_Pseudossn_Load_Pseudossn_From_SDA_Tbl.Status = Succeeded |
| s_Pseudossn_Update_Timekeeper_Number | s_Pseudossn_Load_SDA_Records_Pseudossn_Tbl | $s_Pseudossn_Update_Timekeeper_Number.Status = Succeeded |
| s_Pseudossn_Load_Pseudossn_Tbl | s_Pseudossn_Load_Pseudossn_From_SDA_Tbl | $s_Pseudossn_Load_Pseudossn_Tbl.Status = Succeeded |

Command tasks:

- `s_Pseudossn_Counters` / Post-session success command `post_session_success_command`: `Command1` = `mv $Param_Root_Directory/data/int/in/PSEUDO/$Param_PSEUDOSSN_file $Param_Root_Directory/data/archive/PSEUDO/PSEUDO_P$$WF_PP_YEAR_NUM.txt`; `Command2` = `mv $Param_Root_Directory/data/int/in/PSEUDO/$Param_PSEUDOSSN_Backup_file $Param_Root_Directory/data/archive/PSEUDO/bkup.pseudssn.P$$WF_PP_YEAR_NUM.txt`
- `s_Pseudossn_Counters` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_SUBJECT` = `$$WF_SUBJECT`; `$$MAP_MESSAGE` = `$$WF_MESSAGE`
- `s_Pseudossn_Counters` / Post-session success variable assignment `postsession_success_variable_assignment`: `$$WF_SUBJECT` = `$$MAP_SUBJECT`; `$$WF_MESSAGE` = `$$MAP_MESSAGE`
- `s_Pseudossn_Current_Pay_Period` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_YEAR_NUM` = `$$WF_PP_YEAR_NUM`
- `s_Pseudossn_Current_Pay_Period` / Post-session success variable assignment `postsession_success_variable_assignment`: `$$WF_PP_YEAR_NUM` = `$$MAP_PP_YEAR_NUM`

- Session `s_Pseudossn_Verify_Header_Date_Current_Pay_Period`: WRITER `PSEUDO_HDR_DATE_FILE` Append if Exists=`NO`, Output Type=`File`, Output file directory=`$PMTargetFileDir\`, Output filename=`pseudo_hdr_date.txt`; READER `PSEUDOSSN_FILE` Input Type=`File`, Source file directory=`$Param_Root_Directory\data\int\in\PSEUDO`, Source filename=`$Param_PSEUDOSSN_file`
- Session `s_Pseudossn_Verify_Record_Count`: WRITER `PSEUDO_RECORD_COUNT` Append if Exists=`NO`, Output Type=`File`, Output file directory=`$PMTargetFileDir\`, Output filename=`pseudo_record_count.txt`; READER `PSEUDOSSN_FILE` Input Type=`File`, Source file directory=`$Param_Root_Directory\data\int\in\PSEUDO`, Source filename=`$Param_PSEUDOSSN_file`; READER `PSEUDOSSN_FILE1` Input Type=`File`, Source file directory=`$Param_Root_Directory\data\int\in\PSEUDO`, Source filename=`$Param_PSEUDOSSN_file`
- Session `s_Pseudossn_Verify_Header_Date_Current_Pay_Period_Pseudossn_From_SDA`: WRITER `PSEUDO_HDR_DATE_FILE` Append if Exists=`NO`, Output Type=`File`, Output file directory=`$PMTargetFileDir\`, Output filename=`pseudo_hdr_date_from_sda.txt`; READER `PSEUDOSSN_FILE_TK_NUM` Input Type=`File`, Source file directory=`$Param_Root_Directory\data\int\in\PSEUDO`, Source filename=`$Param_PSEUDOSSN_Backup_file`
- Session `s_Pseudossn_Current_Pay_Period`: WRITER `PAY_PERIOD_DATE_FILE` Append if Exists=`NO`, Output Type=`File`, Output file directory=`$PMTargetFileDir\`, Output filename=`pay_period.txt`
- Session `s_Pseudossn_Load_Archive_Pseudossn_Tbl`: WRITER `HI_ARCH_PSEUDOSSN_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`
- Session `s_Pseudossn_Load_Pseudossn_Tbl`: WRITER `PSEUDOSSN_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`YES`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`; READER `PSEUDOSSN_FILE` Input Type=`File`, Source file directory=`$Param_Root_Directory\data\int\in\PSEUDO`, Source filename=`$Param_PSEUDOSSN_file`; WRITER `ERROR_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`
- Session `s_Pseudossn_Load_Pseudossn_From_SDA_Tbl`: WRITER `PSEUDOSSN_FROM_SDA_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`YES`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`; READER `PSEUDOSSN_FILE_TK_NUM` Input Type=`File`, Source file directory=`$Param_Root_Directory\data\int\in\PSEUDO`, Source filename=`$Param_PSEUDOSSN_Backup_file`
- Session `s_Pseudossn_Update_Timekeeper_Number`: WRITER `PSEUDOSSN_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`
- Session `s_Pseudossn_Load_SDA_Records_Pseudossn_Tbl`: WRITER `PSEUDOSSN_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`
- Session `s_Pseudossn_Counters`: READER `PSEUDOSSN_FILE` Input Type=`File`, Source file directory=`$Param_Root_Directory\data\int\in\PSEUDO`, Source filename=`$Param_PSEUDOSSN_file`; WRITER `PSEUDOSSN_MESSAGE_FILE` Append if Exists=`NO`, Output Type=`File`, Output file directory=`$PMTargetFileDir\`, Output filename=`pseudossn_message_file.txt`; WRITER `COUNTER_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`

## Source definitions

| Source | Database type | Fields |
|---|---|---|
| PAY_PERIOD | Oracle | 10 |
| PSEUDOSSN_FILE | Flat File | 66 |
| PSEUDOSSN_FILE_TK_NUM | Flat File | 67 |
| PSEUDOSSN_FROM_SDA_TBL | Oracle | 63 |
| PSEUDOSSN_TBL | Oracle | 63 |

## Target definitions

| Target | Database type | Fields |
|---|---|---|
| COUNTER_TBL | Oracle | 7 |
| ERROR_TBL | Oracle | 8 |
| HI_ARCH_PSEUDOSSN_TBL | Oracle | 63 |
| PAY_PERIOD_DATE_FILE | Flat File | 1 |
| PSEUDOSSN_FROM_SDA_TBL | Oracle | 63 |
| PSEUDOSSN_MESSAGE_FILE | Flat File | 2 |
| PSEUDOSSN_TBL | Oracle | 63 |
| PSEUDO_HDR_DATE_FILE | Flat File | 1 |
| PSEUDO_RECORD_COUNT | Oracle | 3 |

## Mapping `m_Pseudossn_Verify_Header_Date_Current_Pay_Period`

- Sessions: `s_Pseudossn_Verify_Header_Date_Current_Pay_Period` (#1)
- Sources: `PSEUDOSSN_FILE`
- Target instances: `PSEUDO_HDR_DATE_FILE`

### Transformation `SQ_PSEUDOSSN_FILE` (Source Qualifier)

- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `fil_Header` (Filter)

- **Filter Condition**: `RECORD_TYPE_FLAG = 'H'`

### Transformation `lkp_Current_Pay_Period` (Lookup Procedure)

- **Lookup table name**: `PAY_PERIOD`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `CURR_PP_FLAG = in_CURR_PP_FLAG`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `lkp_Pay_Period_Header_Date` (Lookup Procedure)

- **Lookup Sql Override**: `SELECT PAY_PERIOD.PP_NUM as PP_NUM, PAY_PERIOD.PP_END_YEAR as PP_END_YEAR, PAY_PERIOD.CURR_PP_FLAG as CURR_PP_FLAG, PAY_PERIOD.PP_START_DTE as PP_START_DTE, PAY_PERIOD.PP_END_DTE as PP_END_DTE FROM PAY_PERIOD WHERE CURR_PP_FLAG = 'Y'`
- **Lookup table name**: `PAY_PERIOD`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `PP_START_DTE <= in_HEADER_DATE AND PP_END_DTE >= in_HEADER_DATE`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

- Lookup `lkp_Current_Pay_Period`: table `PAY_PERIOD` (exists in export: **True**), condition `CURR_PP_FLAG = in_CURR_PP_FLAG`, multiple-match policy `Use Any Value`.
- Lookup `lkp_Pay_Period_Header_Date`: table `PAY_PERIOD` (exists in export: **True**), condition `PP_START_DTE <= in_HEADER_DATE AND PP_END_DTE >= in_HEADER_DATE`, multiple-match policy `Use Any Value`.

### Target instance `PSEUDO_HDR_DATE_FILE` (table `PSEUDO_HDR_DATE_FILE`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| PSEUDO_HDR_DATE_FILE | PSEUDO_DATE | exp_Final.o_PSEUDO_DATE = v_PSEUDO_DATE → exp_Final.v_PSEUDO_DATE = SUBSTR(in_PSEUDO_DATE, 1, 4) \|\| SUBSTR(in_PSEUDO_DATE, 6, 2) \|\| SUBSTR(in_PSEUDO_DATE, 9, 2) --Remove dashes from date to prepare for file rename. → fil_Header.PSEUDO_DATE → exp_Verify_Header_Date.o_PSEUDO_DATE = IIF(IS_DATE(v_PSEUDO_DATE_STRING, 'YYYY-MM-DD'), v_PSEUDO_DATE_STRING, 'BAD DATE') → exp_Verify_Header_Date.v_PSEUDO_DATE_STRING = IIF(v_RECORD_TYPE_FLAG ='H', SUBSTR(CAN_CD, 1, 8) \|\| SUBSTR(PSEUDO_SSN, 1, 2) , NULL) → exp_Verify_Header_Date.v_RECORD_TYPE_FLAG = DECODE (TRUE, SUBSTR(SSN,1, 6) = 'HEADER', 'H', SUBSTR(SSN,1, 7) = 'TRAILER', 'T', 'D') --Ignore detail records. Only test for header and trailer → exp_Initial.SSN → SQ_PSEUDOSSN_FILE.SSN → PSEUDOSSN_FILE.SSN → exp_Initial.CAN_CD → SQ_PSEUDOSSN_FILE.CAN_CD → PSEUDOSSN_FILE.CAN_CD → exp_Initial.PSEUDO_SSN → SQ_PSEUDOSSN_FILE.PSEUDO_SSN → PSEUDOSSN_FILE.PSEUDO_SSN | PSEUDOSSN_FILE.CAN_CD; PSEUDOSSN_FILE.PSEUDO_SSN; PSEUDOSSN_FILE.SSN |

## Mapping `m_Pseudossn_Verify_Record_Count`

- Sessions: `s_Pseudossn_Verify_Record_Count` (#2)
- Sources: `PSEUDOSSN_FILE`, `PSEUDOSSN_FILE1`
- Target instances: `PSEUDO_RECORD_COUNT`

### Transformation `SQ_PSEUDOSSN_FILE` (Source Qualifier)

- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `SQ_PSEUDOSSN_FILE1` (Source Qualifier)

- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `agg_ALL_RECORDS` (Aggregator)

- **Sorted Input**: `NO`

### Transformation `fil_DETAIL` (Filter)

- **Filter Condition**: `RECORD_TYPE_FLAG = 'D' --RECORD_TYPE_FLAG = 'H' OR`

### Transformation `fil_TRAILER` (Filter)

- **Filter Condition**: `RECORD_TYPE_FLAG = 'T'`

### Transformation `jnr_RECORD_CONSTANTS` (Joiner)

- **Join Condition**: `TRAILER_CONSTANT = DETAIL_CONSTANT`
- **Join Type**: `Normal Join`
- **Null ordering in master**: `Null Is Highest Value`
- **Null ordering in detail**: `Null Is Highest Value`
- **Sorted Input**: `NO`

- Joiner `jnr_RECORD_CONSTANTS`: Normal Join ON `TRAILER_CONSTANT = DETAIL_CONSTANT`

### Target instance `PSEUDO_RECORD_COUNT` (table `PSEUDO_RECORD_COUNT`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| PSEUDO_RECORD_COUNT | TRAILER_RECORD_COUNT | exp_COMPARE.TRAILER_RECORD_COUNT → jnr_RECORD_CONSTANTS.TRAILER_RECORD_COUNT → fil_TRAILER.RECORD_COUNT → exp_DETERMINE_HEADER_TRAILER.o_RECORD_COUNT = IIF(IS_NUMBER(v_RECORD_COUNT), v_RECORD_COUNT, 'BAD_NUMBER') → exp_DETERMINE_HEADER_TRAILER.v_RECORD_COUNT = IIF(v_RECORD_TYPE_FLAG = 'T', SUBSTR(CAN_CD, 1, 6), NULL) → exp_DETERMINE_HEADER_TRAILER.v_RECORD_TYPE_FLAG = DECODE (TRUE, SUBSTR(SSN,1, 6) = 'HEADER', 'H', SUBSTR(SSN,1, 7) = 'TRAILER', 'T', 'D') --Ignore detail records. Only test for header and trailer → SQ_PSEUDOSSN_FILE.SSN → PSEUDOSSN_FILE.SSN → SQ_PSEUDOSSN_FILE.CAN_CD → PSEUDOSSN_FILE.CAN_CD | PSEUDOSSN_FILE.CAN_CD; PSEUDOSSN_FILE.SSN |
| PSEUDO_RECORD_COUNT | DETAIL_RECORD_COUNT | exp_COMPARE.DETAIL_RECORD_COUNT → jnr_RECORD_CONSTANTS.DETAIL_RECORD_COUNT → agg_ALL_RECORDS.o_DETAIL_RECORD_COUNT = COUNT(SSN) → fil_DETAIL.SSN → exp_DETERMINE_DETAIL.SSN → SQ_PSEUDOSSN_FILE1.SSN → PSEUDOSSN_FILE1.SSN | PSEUDOSSN_FILE1.SSN |
| PSEUDO_RECORD_COUNT | MESSAGE | exp_COMPARE.o_RECORD_COUNT_MATCH_MESSAGE = IIF(v_RECORD_COUNT_MATCH = TRUE, 'Record Counts Match', ABORT('!!!! The record count in the trailer: ' \|\| TRAILER_RECORD_COUNT \|\| ' does not match the detail record count of the file: ' \|\| TO_CHAR(DETAIL_RECORD_COUNT) ) ) → exp_COMPARE.v_RECORD_COUNT_MATCH = IIF(v_TRAILER_RECORD_COUNT = DETAIL_RECORD_COUNT, TRUE, FALSE) → exp_COMPARE.v_TRAILER_RECORD_COUNT = IIF(IS_NUMBER(TRAILER_RECORD_COUNT), TO_INTEGER(TRAILER_RECORD_COUNT), 0) → jnr_RECORD_CONSTANTS.TRAILER_RECORD_COUNT → fil_TRAILER.RECORD_COUNT → exp_DETERMINE_HEADER_TRAILER.o_RECORD_COUNT = IIF(IS_NUMBER(v_RECORD_COUNT), v_RECORD_COUNT, 'BAD_NUMBER') → exp_DETERMINE_HEADER_TRAILER.v_RECORD_COUNT = IIF(v_RECORD_TYPE_FLAG = 'T', SUBSTR(CAN_CD, 1, 6), NULL) → exp_DETERMINE_HEADER_TRAILER.v_RECORD_TYPE_FLAG = DECODE (TRUE, SUBSTR(SSN,1, 6) = 'HEADER', 'H', SUBSTR(SSN,1, 7) = 'TRAILER', 'T', 'D') --Ignore detail records. Only test for header and trailer → SQ_PSEUDOSSN_FILE.SSN → PSEUDOSSN_FILE.SSN → SQ_PSEUDOSSN_FILE.CAN_CD → PSEUDOSSN_FILE.CAN_CD → jnr_RECORD_CONSTANTS.DETAIL_RECORD_COUNT → agg_ALL_RECORDS.o_DETAIL_RECORD_COUNT = COUNT(SSN) → fil_DETAIL.SSN → exp_DETERMINE_DETAIL.SSN → SQ_PSEUDOSSN_FILE1.SSN → PSEUDOSSN_FILE1.SSN | PSEUDOSSN_FILE.CAN_CD; PSEUDOSSN_FILE.SSN; PSEUDOSSN_FILE1.SSN |

## Mapping `m_Pseudossn_Verify_Header_Date_Current_Pay_Period_Pseudossn_From_SDA`

- Sessions: `s_Pseudossn_Verify_Header_Date_Current_Pay_Period_Pseudossn_From_SDA` (#3)
- Sources: `PSEUDOSSN_FILE_TK_NUM`
- Target instances: `PSEUDO_HDR_DATE_FILE`

### Transformation `SQ_PSEUDOSSN_FILE_TK_NUM` (Source Qualifier)

- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `fil_Header` (Filter)

- **Filter Condition**: `RECORD_TYPE_FLAG = 'H'`

### Transformation `lkp_Current_Pay_Period` (Lookup Procedure)

- **Lookup table name**: `PAY_PERIOD`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `CURR_PP_FLAG = in_CURR_PP_FLAG`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `lkp_Pay_Period_Header_Date` (Lookup Procedure)

- **Lookup Sql Override**: `SELECT PAY_PERIOD.PP_NUM as PP_NUM, PAY_PERIOD.PP_END_YEAR as PP_END_YEAR, PAY_PERIOD.CURR_PP_FLAG as CURR_PP_FLAG, PAY_PERIOD.PP_START_DTE as PP_START_DTE, PAY_PERIOD.PP_END_DTE as PP_END_DTE FROM PAY_PERIOD WHERE CURR_PP_FLAG = 'Y'`
- **Lookup table name**: `PAY_PERIOD`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `PP_START_DTE <= in_HEADER_DATE AND PP_END_DTE >= in_HEADER_DATE`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

- Lookup `lkp_Current_Pay_Period`: table `PAY_PERIOD` (exists in export: **True**), condition `CURR_PP_FLAG = in_CURR_PP_FLAG`, multiple-match policy `Use Any Value`.
- Lookup `lkp_Pay_Period_Header_Date`: table `PAY_PERIOD` (exists in export: **True**), condition `PP_START_DTE <= in_HEADER_DATE AND PP_END_DTE >= in_HEADER_DATE`, multiple-match policy `Use Any Value`.

### Target instance `PSEUDO_HDR_DATE_FILE` (table `PSEUDO_HDR_DATE_FILE`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| PSEUDO_HDR_DATE_FILE | PSEUDO_DATE | exp_Final.o_PSEUDO_DATE = v_PSEUDO_DATE → exp_Final.v_PSEUDO_DATE = SUBSTR(in_PSEUDO_DATE, 1, 4) \|\| SUBSTR(in_PSEUDO_DATE, 6, 2) \|\| SUBSTR(in_PSEUDO_DATE, 9, 2) --Remove dashes from date to prepare for file rename. → fil_Header.PSEUDO_DATE → exp_Verify_Header_Date.o_PSEUDO_DATE = IIF(IS_DATE(v_PSEUDO_DATE_STRING, 'YYYY-MM-DD'), v_PSEUDO_DATE_STRING, 'BAD DATE') → exp_Verify_Header_Date.v_PSEUDO_DATE_STRING = IIF(v_RECORD_TYPE_FLAG ='H', SUBSTR(SSN, 8, 2) \|\| SUBSTR(CAN_CD, 1, 8), NULL) -- SUBSTR(CAN_CD, 1, 8) \|\| SUBSTR(PSEUDO_SSN, 1, 2), → exp_Verify_Header_Date.v_RECORD_TYPE_FLAG = DECODE (TRUE, SUBSTR(SSN,1, 6) = 'HEADER', 'H', SUBSTR(SSN,1, 7) = 'TRAILER', 'T', 'D') --Ignore detail records. Only test for header and trailer → exp_Initial.SSN → SQ_PSEUDOSSN_FILE_TK_NUM.SSN → PSEUDOSSN_FILE_TK_NUM.SSN → exp_Initial.CAN_CD → SQ_PSEUDOSSN_FILE_TK_NUM.CAN_CD → PSEUDOSSN_FILE_TK_NUM.CAN_CD → exp_Initial.PSEUDO_SSN → SQ_PSEUDOSSN_FILE_TK_NUM.PSEUDO_SSN → PSEUDOSSN_FILE_TK_NUM.PSEUDO_SSN | PSEUDOSSN_FILE_TK_NUM.CAN_CD; PSEUDOSSN_FILE_TK_NUM.PSEUDO_SSN; PSEUDOSSN_FILE_TK_NUM.SSN |

## Mapping `m_Pseudossn_Current_Pay_Period`

- Sessions: `s_Pseudossn_Current_Pay_Period` (#4)
- Sources: `PAY_PERIOD`
- Target instances: `PAY_PERIOD_DATE_FILE`

### Transformation `SQ_PAY_PERIOD` (Source Qualifier)

- **Source Filter**: `PAY_PERIOD.CURR_PP_FLAG = 'Y'`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`


### Target instance `PAY_PERIOD_DATE_FILE` (table `PAY_PERIOD_DATE_FILE`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| PAY_PERIOD_DATE_FILE | PAY_PERIOD | exp_Final.PAY_PERIOD → exp_Build_Pay_Period.o_PAY_PERIOD = TO_CHAR(PP_END_YEAR) \|\| v_PP_NUM → SQ_PAY_PERIOD.PP_END_YEAR → PAY_PERIOD.PP_END_YEAR → exp_Build_Pay_Period.v_PP_NUM = IIF(PP_NUM < 10, LPAD(TO_CHAR(PP_NUM), 2, '0'), TO_CHAR(PP_NUM) ) → SQ_PAY_PERIOD.PP_NUM → PAY_PERIOD.PP_NUM | PAY_PERIOD.PP_END_YEAR; PAY_PERIOD.PP_NUM |

## Mapping `m_Pseudossn_Load_Archive_Pseudossn_Tbl_v1`

- Sessions: `s_Pseudossn_Load_Archive_Pseudossn_Tbl` (#5)
- Sources: `PSEUDOSSN_TBL`
- Target instances: `HI_ARCH_PSEUDOSSN_TBL`

### Transformation `SQ_PSEUDOSSN_TBL` (Source Qualifier)

- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`


### Target instance `HI_ARCH_PSEUDOSSN_TBL` (table `HI_ARCH_PSEUDOSSN_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| HI_ARCH_PSEUDOSSN_TBL | SSN | exp_PSEUDOSSN_TBL.SSN → SQ_PSEUDOSSN_TBL.SSN → PSEUDOSSN_TBL.SSN | PSEUDOSSN_TBL.SSN |
| HI_ARCH_PSEUDOSSN_TBL | CAN_CD | exp_PSEUDOSSN_TBL.CAN_CD → SQ_PSEUDOSSN_TBL.CAN_CD → PSEUDOSSN_TBL.CAN_CD | PSEUDOSSN_TBL.CAN_CD |
| HI_ARCH_PSEUDOSSN_TBL | PSEUDOSSN | exp_PSEUDOSSN_TBL.PSEUDOSSN → SQ_PSEUDOSSN_TBL.PSEUDOSSN → PSEUDOSSN_TBL.PSEUDOSSN | PSEUDOSSN_TBL.PSEUDOSSN |
| HI_ARCH_PSEUDOSSN_TBL | EMPLID | exp_PSEUDOSSN_TBL.EMPLID → SQ_PSEUDOSSN_TBL.EMPLID → PSEUDOSSN_TBL.EMPLID | PSEUDOSSN_TBL.EMPLID |
| HI_ARCH_PSEUDOSSN_TBL | EMPL_RCD | exp_PSEUDOSSN_TBL.EMPL_RCD → SQ_PSEUDOSSN_TBL.EMPL_RCD → PSEUDOSSN_TBL.EMPL_RCD | PSEUDOSSN_TBL.EMPL_RCD |
| HI_ARCH_PSEUDOSSN_TBL | APPT_NUM | exp_PSEUDOSSN_TBL.APPT_NUM → SQ_PSEUDOSSN_TBL.APPT_NUM → PSEUDOSSN_TBL.APPT_NUM | PSEUDOSSN_TBL.APPT_NUM |
| HI_ARCH_PSEUDOSSN_TBL | EMP_FIRST_NAME | exp_PSEUDOSSN_TBL.EMP_FIRST_NAME → SQ_PSEUDOSSN_TBL.EMP_FIRST_NAME → PSEUDOSSN_TBL.EMP_FIRST_NAME | PSEUDOSSN_TBL.EMP_FIRST_NAME |
| HI_ARCH_PSEUDOSSN_TBL | EMP_MID_INIT | exp_PSEUDOSSN_TBL.EMP_MID_INIT → SQ_PSEUDOSSN_TBL.EMP_MID_INIT → PSEUDOSSN_TBL.EMP_MID_INIT | PSEUDOSSN_TBL.EMP_MID_INIT |
| HI_ARCH_PSEUDOSSN_TBL | EMP_LAST_NAME | exp_PSEUDOSSN_TBL.EMP_LAST_NAME → SQ_PSEUDOSSN_TBL.EMP_LAST_NAME → PSEUDOSSN_TBL.EMP_LAST_NAME | PSEUDOSSN_TBL.EMP_LAST_NAME |
| HI_ARCH_PSEUDOSSN_TBL | SEX | exp_PSEUDOSSN_TBL.SEX → SQ_PSEUDOSSN_TBL.SEX → PSEUDOSSN_TBL.SEX | PSEUDOSSN_TBL.SEX |
| HI_ARCH_PSEUDOSSN_TBL | VETERANS_PREFERENCE_CD | exp_PSEUDOSSN_TBL.VETERANS_PREFERENCE_CD → SQ_PSEUDOSSN_TBL.VETERANS_PREFERENCE_CD → PSEUDOSSN_TBL.VETERANS_PREFERENCE_CD | PSEUDOSSN_TBL.VETERANS_PREFERENCE_CD |
| HI_ARCH_PSEUDOSSN_TBL | TENURE_CD | exp_PSEUDOSSN_TBL.TENURE_CD → SQ_PSEUDOSSN_TBL.TENURE_CD → PSEUDOSSN_TBL.TENURE_CD | PSEUDOSSN_TBL.TENURE_CD |
| HI_ARCH_PSEUDOSSN_TBL | POSITION_NUM | exp_PSEUDOSSN_TBL.POSITION_NUM → SQ_PSEUDOSSN_TBL.POSITION_NUM → PSEUDOSSN_TBL.POSITION_NUM | PSEUDOSSN_TBL.POSITION_NUM |
| HI_ARCH_PSEUDOSSN_TBL | US_CITIZENSHIP_CD | exp_PSEUDOSSN_TBL.US_CITIZENSHIP_CD → SQ_PSEUDOSSN_TBL.US_CITIZENSHIP_CD → PSEUDOSSN_TBL.US_CITIZENSHIP_CD | PSEUDOSSN_TBL.US_CITIZENSHIP_CD |
| HI_ARCH_PSEUDOSSN_TBL | APPT_TYPE_CD | exp_PSEUDOSSN_TBL.APPT_TYPE_CD → SQ_PSEUDOSSN_TBL.APPT_TYPE_CD → PSEUDOSSN_TBL.APPT_TYPE_CD | PSEUDOSSN_TBL.APPT_TYPE_CD |
| HI_ARCH_PSEUDOSSN_TBL | HIRE_DATE | exp_PSEUDOSSN_TBL.HIRE_DATE → SQ_PSEUDOSSN_TBL.HIRE_DATE → PSEUDOSSN_TBL.HIRE_DATE | PSEUDOSSN_TBL.HIRE_DATE |
| HI_ARCH_PSEUDOSSN_TBL | HANDICAP_CD | exp_PSEUDOSSN_TBL.HANDICAP_CD → SQ_PSEUDOSSN_TBL.HANDICAP_CD → PSEUDOSSN_TBL.HANDICAP_CD | PSEUDOSSN_TBL.HANDICAP_CD |
| HI_ARCH_PSEUDOSSN_TBL | UNF_ALLOW_CD | exp_PSEUDOSSN_TBL.UNF_ALLOW_CD → SQ_PSEUDOSSN_TBL.UNF_ALLOW_CD → PSEUDOSSN_TBL.UNF_ALLOW_CD | PSEUDOSSN_TBL.UNF_ALLOW_CD |
| HI_ARCH_PSEUDOSSN_TBL | UNIF_ALLOW_DATE | exp_PSEUDOSSN_TBL.UNIF_ALLOW_DATE → SQ_PSEUDOSSN_TBL.UNIF_ALLOW_DATE → PSEUDOSSN_TBL.UNIF_ALLOW_DATE | PSEUDOSSN_TBL.UNIF_ALLOW_DATE |
| HI_ARCH_PSEUDOSSN_TBL | UNIF_ALLOW_AMT | exp_PSEUDOSSN_TBL.UNIF_ALLOW_AMT → SQ_PSEUDOSSN_TBL.UNIF_ALLOW_AMT → PSEUDOSSN_TBL.UNIF_ALLOW_AMT | PSEUDOSSN_TBL.UNIF_ALLOW_AMT |
| HI_ARCH_PSEUDOSSN_TBL | RSSSDP | exp_PSEUDOSSN_TBL.RSSSDP → SQ_PSEUDOSSN_TBL.RSSSDP → PSEUDOSSN_TBL.RSSSDP | PSEUDOSSN_TBL.RSSSDP |
| HI_ARCH_PSEUDOSSN_TBL | CEIL_REPORTING_CD | exp_PSEUDOSSN_TBL.CEIL_REPORTING_CD → SQ_PSEUDOSSN_TBL.CEIL_REPORTING_CD → PSEUDOSSN_TBL.CEIL_REPORTING_CD | PSEUDOSSN_TBL.CEIL_REPORTING_CD |
| HI_ARCH_PSEUDOSSN_TBL | FUNCTNL_CLASSFCTN_CD | exp_PSEUDOSSN_TBL.FUNCTNL_CLASSFCTN_CD → SQ_PSEUDOSSN_TBL.FUNCTNL_CLASSFCTN_CD → PSEUDOSSN_TBL.FUNCTNL_CLASSFCTN_CD | PSEUDOSSN_TBL.FUNCTNL_CLASSFCTN_CD |
| HI_ARCH_PSEUDOSSN_TBL | EMP_STATUS | exp_PSEUDOSSN_TBL.EMP_STATUS → SQ_PSEUDOSSN_TBL.EMP_STATUS → PSEUDOSSN_TBL.EMP_STATUS | PSEUDOSSN_TBL.EMP_STATUS |
| HI_ARCH_PSEUDOSSN_TBL | MANAGER_STATUS | exp_PSEUDOSSN_TBL.MANAGER_STATUS → SQ_PSEUDOSSN_TBL.MANAGER_STATUS → PSEUDOSSN_TBL.MANAGER_STATUS | PSEUDOSSN_TBL.MANAGER_STATUS |
| HI_ARCH_PSEUDOSSN_TBL | POSITION_SENSITIVITY_CD | exp_PSEUDOSSN_TBL.POSITION_SENSITIVITY_CD → SQ_PSEUDOSSN_TBL.POSITION_SENSITIVITY_CD → PSEUDOSSN_TBL.POSITION_SENSITIVITY_CD | PSEUDOSSN_TBL.POSITION_SENSITIVITY_CD |
| HI_ARCH_PSEUDOSSN_TBL | CAREER_START_DATE | exp_PSEUDOSSN_TBL.CAREER_START_DATE → SQ_PSEUDOSSN_TBL.CAREER_START_DATE → PSEUDOSSN_TBL.CAREER_START_DATE | PSEUDOSSN_TBL.CAREER_START_DATE |
| HI_ARCH_PSEUDOSSN_TBL | CAREER_CONV_DATE | exp_PSEUDOSSN_TBL.CAREER_CONV_DATE → SQ_PSEUDOSSN_TBL.CAREER_CONV_DATE → PSEUDOSSN_TBL.CAREER_CONV_DATE | PSEUDOSSN_TBL.CAREER_CONV_DATE |
| HI_ARCH_PSEUDOSSN_TBL | PROBATION_DATE | exp_PSEUDOSSN_TBL.PROBATION_DATE → SQ_PSEUDOSSN_TBL.PROBATION_DATE → PSEUDOSSN_TBL.PROBATION_DATE | PSEUDOSSN_TBL.PROBATION_DATE |
| HI_ARCH_PSEUDOSSN_TBL | ABNORMAL_RATE_CD | exp_PSEUDOSSN_TBL.ABNORMAL_RATE_CD → SQ_PSEUDOSSN_TBL.ABNORMAL_RATE_CD → PSEUDOSSN_TBL.ABNORMAL_RATE_CD | PSEUDOSSN_TBL.ABNORMAL_RATE_CD |
| HI_ARCH_PSEUDOSSN_TBL | APPT_LIMIT_HRS | exp_PSEUDOSSN_TBL.APPT_LIMIT_HRS → SQ_PSEUDOSSN_TBL.APPT_LIMIT_HRS → PSEUDOSSN_TBL.APPT_LIMIT_HRS | PSEUDOSSN_TBL.APPT_LIMIT_HRS |
| HI_ARCH_PSEUDOSSN_TBL | APPT_LIMIT_PAY | exp_PSEUDOSSN_TBL.APPT_LIMIT_PAY → SQ_PSEUDOSSN_TBL.APPT_LIMIT_PAY → PSEUDOSSN_TBL.APPT_LIMIT_PAY | PSEUDOSSN_TBL.APPT_LIMIT_PAY |
| HI_ARCH_PSEUDOSSN_TBL | LAST_PAY_CHANGE | exp_PSEUDOSSN_TBL.LAST_PAY_CHANGE → SQ_PSEUDOSSN_TBL.LAST_PAY_CHANGE → PSEUDOSSN_TBL.LAST_PAY_CHANGE | PSEUDOSSN_TBL.LAST_PAY_CHANGE |
| HI_ARCH_PSEUDOSSN_TBL | CHARITY_AREA_CD | exp_PSEUDOSSN_TBL.CHARITY_AREA_CD → SQ_PSEUDOSSN_TBL.CHARITY_AREA_CD → PSEUDOSSN_TBL.CHARITY_AREA_CD | PSEUDOSSN_TBL.CHARITY_AREA_CD |
| HI_ARCH_PSEUDOSSN_TBL | CHARITY_EFF_DATE | exp_PSEUDOSSN_TBL.CHARITY_EFF_DATE → SQ_PSEUDOSSN_TBL.CHARITY_EFF_DATE → PSEUDOSSN_TBL.CHARITY_EFF_DATE | PSEUDOSSN_TBL.CHARITY_EFF_DATE |
| HI_ARCH_PSEUDOSSN_TBL | CHARITY_DED_AMT | exp_PSEUDOSSN_TBL.CHARITY_DED_AMT → SQ_PSEUDOSSN_TBL.CHARITY_DED_AMT → PSEUDOSSN_TBL.CHARITY_DED_AMT | PSEUDOSSN_TBL.CHARITY_DED_AMT |
| HI_ARCH_PSEUDOSSN_TBL | LAST_NOA_CD | exp_PSEUDOSSN_TBL.LAST_NOA_CD → SQ_PSEUDOSSN_TBL.LAST_NOA_CD → PSEUDOSSN_TBL.LAST_NOA_CD | PSEUDOSSN_TBL.LAST_NOA_CD |
| HI_ARCH_PSEUDOSSN_TBL | QUARTERS_DED_AMT | exp_PSEUDOSSN_TBL.QUARTERS_DED_AMT → SQ_PSEUDOSSN_TBL.QUARTERS_DED_AMT → PSEUDOSSN_TBL.QUARTERS_DED_AMT | PSEUDOSSN_TBL.QUARTERS_DED_AMT |
| HI_ARCH_PSEUDOSSN_TBL | SUBSIST_DED_AMT | exp_PSEUDOSSN_TBL.SUBSIST_DED_AMT → SQ_PSEUDOSSN_TBL.SUBSIST_DED_AMT → PSEUDOSSN_TBL.SUBSIST_DED_AMT | PSEUDOSSN_TBL.SUBSIST_DED_AMT |
| HI_ARCH_PSEUDOSSN_TBL | PAY_BASIS_CD | exp_PSEUDOSSN_TBL.PAY_BASIS_CD → SQ_PSEUDOSSN_TBL.PAY_BASIS_CD → PSEUDOSSN_TBL.PAY_BASIS_CD | PSEUDOSSN_TBL.PAY_BASIS_CD |
| HI_ARCH_PSEUDOSSN_TBL | WORK_SCHEDULE_CD | exp_PSEUDOSSN_TBL.WORK_SCHEDULE_CD → SQ_PSEUDOSSN_TBL.WORK_SCHEDULE_CD → PSEUDOSSN_TBL.WORK_SCHEDULE_CD | PSEUDOSSN_TBL.WORK_SCHEDULE_CD |
| HI_ARCH_PSEUDOSSN_TBL | OCCUPATION_CD | exp_PSEUDOSSN_TBL.OCCUPATION_CD → SQ_PSEUDOSSN_TBL.OCCUPATION_CD → PSEUDOSSN_TBL.OCCUPATION_CD | PSEUDOSSN_TBL.OCCUPATION_CD |
| HI_ARCH_PSEUDOSSN_TBL | DUTY_STATION | exp_PSEUDOSSN_TBL.DUTY_STATION → SQ_PSEUDOSSN_TBL.DUTY_STATION → PSEUDOSSN_TBL.DUTY_STATION | PSEUDOSSN_TBL.DUTY_STATION |
| HI_ARCH_PSEUDOSSN_TBL | JOB_IND | exp_PSEUDOSSN_TBL.JOB_IND → SQ_PSEUDOSSN_TBL.JOB_IND → PSEUDOSSN_TBL.JOB_IND | PSEUDOSSN_TBL.JOB_IND |
| HI_ARCH_PSEUDOSSN_TBL | REG_TEMP_CD | exp_PSEUDOSSN_TBL.REG_TEMP_CD → SQ_PSEUDOSSN_TBL.REG_TEMP_CD → PSEUDOSSN_TBL.REG_TEMP_CD | PSEUDOSSN_TBL.REG_TEMP_CD |
| HI_ARCH_PSEUDOSSN_TBL | SEPERATION_DATE | exp_PSEUDOSSN_TBL.SEPERATION_DATE → SQ_PSEUDOSSN_TBL.SEPERATION_DATE → PSEUDOSSN_TBL.SEPERATION_DATE | PSEUDOSSN_TBL.SEPERATION_DATE |
| HI_ARCH_PSEUDOSSN_TBL | PCA_CONTR_EFF_START_DATE | exp_PSEUDOSSN_TBL.PCA_CONTR_EFF_START_DATE → SQ_PSEUDOSSN_TBL.PCA_CONTR_EFF_START_DATE → PSEUDOSSN_TBL.PCA_CONTR_EFF_START_DATE | PSEUDOSSN_TBL.PCA_CONTR_EFF_START_DATE |
| HI_ARCH_PSEUDOSSN_TBL | PCA_CONTR_EFF_END_DATE | exp_PSEUDOSSN_TBL.PCA_CONTR_EFF_END_DATE → SQ_PSEUDOSSN_TBL.PCA_CONTR_EFF_END_DATE → PSEUDOSSN_TBL.PCA_CONTR_EFF_END_DATE | PSEUDOSSN_TBL.PCA_CONTR_EFF_END_DATE |
| HI_ARCH_PSEUDOSSN_TBL | MAX_ANNUAL_PAY | exp_PSEUDOSSN_TBL.MAX_ANNUAL_PAY → SQ_PSEUDOSSN_TBL.MAX_ANNUAL_PAY → PSEUDOSSN_TBL.MAX_ANNUAL_PAY | PSEUDOSSN_TBL.MAX_ANNUAL_PAY |
| HI_ARCH_PSEUDOSSN_TBL | PCA_BIWEEKLY_AMT | exp_PSEUDOSSN_TBL.PCA_BIWEEKLY_AMT → SQ_PSEUDOSSN_TBL.PCA_BIWEEKLY_AMT → PSEUDOSSN_TBL.PCA_BIWEEKLY_AMT | PSEUDOSSN_TBL.PCA_BIWEEKLY_AMT |
| HI_ARCH_PSEUDOSSN_TBL | PAY_PLAN_CD | exp_PSEUDOSSN_TBL.PAY_PLAN_CD → SQ_PSEUDOSSN_TBL.PAY_PLAN_CD → PSEUDOSSN_TBL.PAY_PLAN_CD | PSEUDOSSN_TBL.PAY_PLAN_CD |
| HI_ARCH_PSEUDOSSN_TBL | APPT_NTE_DTE | exp_PSEUDOSSN_TBL.APPT_NTE_DTE → SQ_PSEUDOSSN_TBL.APPT_NTE_DTE → PSEUDOSSN_TBL.APPT_NTE_DTE | PSEUDOSSN_TBL.APPT_NTE_DTE |
| HI_ARCH_PSEUDOSSN_TBL | SPECIAL_PROGRAM_CD | exp_PSEUDOSSN_TBL.SPECIAL_PROGRAM_CD → SQ_PSEUDOSSN_TBL.SPECIAL_PROGRAM_CD → PSEUDOSSN_TBL.SPECIAL_PROGRAM_CD | PSEUDOSSN_TBL.SPECIAL_PROGRAM_CD |
| HI_ARCH_PSEUDOSSN_TBL | TERM_ID | exp_PSEUDOSSN_TBL.TERM_ID → SQ_PSEUDOSSN_TBL.TERM_ID → PSEUDOSSN_TBL.TERM_ID | PSEUDOSSN_TBL.TERM_ID |
| HI_ARCH_PSEUDOSSN_TBL | EFFECTIVE_DATE | exp_PSEUDOSSN_TBL.EFFECTIVE_DATE → SQ_PSEUDOSSN_TBL.EFFECTIVE_DATE → PSEUDOSSN_TBL.EFFECTIVE_DATE | PSEUDOSSN_TBL.EFFECTIVE_DATE |
| HI_ARCH_PSEUDOSSN_TBL | EFFECTIVE_SEQ | exp_PSEUDOSSN_TBL.EFFECTIVE_SEQ → SQ_PSEUDOSSN_TBL.EFFECTIVE_SEQ → PSEUDOSSN_TBL.EFFECTIVE_SEQ | PSEUDOSSN_TBL.EFFECTIVE_SEQ |
| HI_ARCH_PSEUDOSSN_TBL | PAY_TABL_NO | exp_PSEUDOSSN_TBL.PAY_TABL_NO → SQ_PSEUDOSSN_TBL.PAY_TABL_NO → PSEUDOSSN_TBL.PAY_TABL_NO | PSEUDOSSN_TBL.PAY_TABL_NO |
| HI_ARCH_PSEUDOSSN_TBL | BUSINESS_UNIT | exp_PSEUDOSSN_TBL.BUSINESS_UNIT → SQ_PSEUDOSSN_TBL.BUSINESS_UNIT → PSEUDOSSN_TBL.BUSINESS_UNIT | PSEUDOSSN_TBL.BUSINESS_UNIT |
| HI_ARCH_PSEUDOSSN_TBL | DEPTID | exp_PSEUDOSSN_TBL.DEPTID → SQ_PSEUDOSSN_TBL.DEPTID → PSEUDOSSN_TBL.DEPTID | PSEUDOSSN_TBL.DEPTID |
| HI_ARCH_PSEUDOSSN_TBL | PCA_CONTR_LEN_YEAR | exp_PSEUDOSSN_TBL.PCA_CONTR_LEN_YEAR → SQ_PSEUDOSSN_TBL.PCA_CONTR_LEN_YEAR → PSEUDOSSN_TBL.PCA_CONTR_LEN_YEAR | PSEUDOSSN_TBL.PCA_CONTR_LEN_YEAR |
| HI_ARCH_PSEUDOSSN_TBL | TK_NUM | exp_PSEUDOSSN_TBL.TK_NUM → SQ_PSEUDOSSN_TBL.TK_NUM → PSEUDOSSN_TBL.TK_NUM | PSEUDOSSN_TBL.TK_NUM |
| HI_ARCH_PSEUDOSSN_TBL | PP_NUM | exp_PSEUDOSSN_TBL.PP_NUM → SQ_PSEUDOSSN_TBL.PP_NUM → PSEUDOSSN_TBL.PP_NUM | PSEUDOSSN_TBL.PP_NUM |
| HI_ARCH_PSEUDOSSN_TBL | PP_END_YEAR | exp_PSEUDOSSN_TBL.PP_END_YEAR → SQ_PSEUDOSSN_TBL.PP_END_YEAR → PSEUDOSSN_TBL.PP_END_YEAR | PSEUDOSSN_TBL.PP_END_YEAR |

## Mapping `m_Pseudossn_Load_Pseudossn_Tbl`

- Sessions: `s_Pseudossn_Load_Pseudossn_Tbl` (#6)
- Sources: `PSEUDOSSN_FILE`
- Target instances: `ERROR_TBL`, `PSEUDOSSN_TBL`

### Transformation `SQ_PSEUDOSSN_FILE` (Source Qualifier)

- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `fil_Detail_Records` (Filter)

- **Filter Condition**: `o_RECORD_TYPE_FLAG = 'D'`

### Transformation `fil_Error_Message` (Filter)

- **Filter Condition**: `NOT ISNULL(ERROR_MESSAGE) AND LENGTH(LTRIM(ERROR_MESSAGE)) > 0`

### Transformation `lkp_Current_Pay_Period` (Lookup Procedure)

- **Lookup table name**: `PAY_PERIOD`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `CURR_PP_FLAG = in_CURR_PP_FLAG`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `lkp_Current_Pay_Period1` (Lookup Procedure)

- **Lookup table name**: `PAY_PERIOD`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `CURR_PP_FLAG = in_CURR_PP_FLAG`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `nrm_Errors` (Normalizer)

- **Reset**: `NO`
- **Restart**: `NO`

### Transformation `rtr_Good_Bad_Records` (Router)

- Router group `GOOD_RECORDS`: `ERROR_FLAG = FALSE`
- Router group `DEFAULT1`: `(default group)`
- Router group `BAD_RECORDS`: `ERROR_FLAG = TRUE`

### Transformation `srt_PSEUDOSSN_EFF_DT` (Sorter)

- **Case Sensitive**: `YES`
- **Distinct**: `NO`
- **Null Treated Low**: `NO`

- Sorter `srt_PSEUDOSSN_EFF_DT` keys: PSEUDO_SSN ASCENDING, EMPLOYEE_STATUS ASCENDING, EFFECTIVE_DATE_CONV DESCENDING; distinct=NO
- Normalizer `nrm_Errors` (vsam=False) occurs: ERROR_MESSAGE×6; generated: GK_ERROR_MESSAGE, GCID_ERROR_MESSAGE
- Lookup `lkp_Current_Pay_Period`: table `PAY_PERIOD` (exists in export: **True**), condition `CURR_PP_FLAG = in_CURR_PP_FLAG`, multiple-match policy `Use Any Value`.
- Lookup `lkp_Current_Pay_Period1`: table `PAY_PERIOD` (exists in export: **True**), condition `CURR_PP_FLAG = in_CURR_PP_FLAG`, multiple-match policy `Use Any Value`.

### Target instance `ERROR_TBL` (table `ERROR_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| ERROR_TBL | PROCESS_NAME | exp_Final_Errors.PROCESS_NAME → exp_Pay_Period.MAPPING_NAME → fil_Error_Message.MAPPING_NAME → nrm_Errors.MAPPING_NAME [normalizer: one row per occurrence of MAPPING_NAME_in] → rtr_Good_Bad_Records.MAPPING_NAME3 [router group BAD_RECORDS WHERE ERROR_FLAG = TRUE] → exp_Determine_Errors.o_MAPPING_NAME = $PMMappingName | literal/expression: $PMMappingName |
| ERROR_TBL | ERROR_MESSAGE | exp_Final_Errors.ERROR_MESSAGE → exp_Pay_Period.ERROR_MESSAGE → fil_Error_Message.ERROR_MESSAGE → nrm_Errors.ERROR_MESSAGE [normalizer: one row per occurrence of ERROR_MESSAGE_in1, ERROR_MESSAGE_in2, ERROR_MESSAGE_in3, ERROR_MESSAGE_in4, ERROR_MESSAGE_in5, ERROR_MESSAGE_in6] → rtr_Good_Bad_Records.ERROR_MESSAGE_13 [router group BAD_RECORDS WHERE ERROR_FLAG = TRUE] → exp_Determine_Errors.o_ERROR_MESSAGE_1 = IIF(v_ERROR_FLAG_1 = TRUE, 'A duplicate has been detected for Social Security: ' \|\| SSN \|\| ' and Can Code: ' \|\| CAN_CD \|\| '.') → exp_Determine_Errors.v_ERROR_FLAG_1 = IIF(v_CURR_KEY = v_PREV_KEY, TRUE, FALSE) → exp_Determine_Errors.v_CURR_KEY = PSEUDO_SSN --PSEUDO_SSN\|\|EMPLOYEE_STATUS --SSN\|\|CAN_CD → srt_PSEUDOSSN_EFF_DT.PSEUDO_SSN → fil_Detail_Records.PSEUDO_SSN → exp_Determine_Record_Type.PSEUDO_SSN → SQ_PSEUDOSSN_FILE.PSEUDO_SSN → PSEUDOSSN_FILE.PSEUDO_SSN → srt_PSEUDOSSN_EFF_DT.EMPLOYEE_STATUS → fil_Detail_Records.EMPLOYEE_STATUS → exp_Determine_Record_Type.EMPLOYEE_STATUS → SQ_PSEUDOSSN_FILE.EMPLOYEE_STATUS → PSEUDOSSN_FILE.EMPLOYEE_STATUS → srt_PSEUDOSSN_EFF_DT.SSN → fil_Detail_Records.SSN → exp_Determine_Record_Type.SSN → SQ_PSEUDOSSN_FILE.SSN → PSEUDOSSN_FILE.SSN → srt_PSEUDOSSN_EFF_DT.CAN_CD → fil_Detail_Records.CAN_CD → exp_Determine_Record_Type.CAN_CD → SQ_PSEUDOSSN_FILE.CAN_CD → PSEUDOSSN_FILE.CAN_CD → exp_Determine_Errors.v_PREV_KEY = PSEUDO_SSN --PSEUDO_SSN\|\|EMPLOYEE_STATUS --SSN\|\|CAN_CD → rtr_Good_Bad_Records.ERROR_MESSAGE_23 [router group BAD_RECORDS WHERE ERROR_FLAG = TRUE] → exp_Determine_Errors.o_ERROR_MESSAGE_2 = IIF(v_ERROR_FLAG_2 = TRUE, 'SSN is not found.') → exp_Determine_Errors.v_ERROR_FLAG_2 = IIF(ISNULL(SSN) OR LENGTH(LTRIM(SSN)) = 0, TRUE, FALSE) → rtr_Good_Bad_Records.ERROR_MESSAGE_33 [router group BAD_RECORDS WHERE ERROR_FLAG = TRUE] → exp_Determine_Errors.o_ERROR_MESSAGE_3 = IIF(v_ERROR_FLAG_3 = TRUE, 'CAN_CD is not found.') → exp_Determine_Errors.v_ERROR_FLAG_3 = IIF(ISNULL(CAN_CD) OR LENGTH(LTRIM(CAN_CD)) = 0, TRUE, FALSE) → rtr_Good_Bad_Records.ERROR_MESSAGE_43 [router group BAD_RECORDS WHERE ERROR_FLAG = TRUE] → exp_Determine_Errors.o_ERROR_MESSAGE_4 = IIF(v_ERROR_FLAG_4 = TRUE, 'PSEUDOSSN is not found.') → exp_Determine_Errors.v_ERROR_FLAG_4 = IIF(ISNULL(PSEUDO_SSN) OR LENGTH(LTRIM(PSEUDO_SSN)) = 0, TRUE, FALSE) → rtr_Good_Bad_Records.ERROR_MESSAGE_53 [router group BAD_RECORDS WHERE ERROR_FLAG = TRUE] → exp_Determine_Errors.o_ERROR_MESSAGE_5 = IIF(v_ERROR_FLAG_5 = TRUE, 'EFFECTIVE_DATE is not found.') → exp_Determine_Errors.v_ERROR_FLAG_5 = IIF(ISNULL(EFFECTIVE_DATE) OR LENGTH(LTRIM(EFFECTIVE_DATE)) = 0, TRUE, FALSE) → srt_PSEUDOSSN_EFF_DT.EFFECTIVE_DATE → fil_Detail_Records.EFFECTIVE_DATE → exp_Determine_Record_Type.EFFECTIVE_DATE → SQ_PSEUDOSSN_FILE.EFFECTIVE_DATE → PSEUDOSSN_FILE.EFFECTIVE_DATE → rtr_Good_Bad_Records.ERROR_MESSAGE_63 [router group BAD_RECORDS WHERE ERROR_FLAG = TRUE] → exp_Determine_Errors.o_ERROR_MESSAGE_6 = IIF(v_ERROR_FLAG_6 = TRUE, 'EFFECTIVE_DATE is not a valid date. Value: '\|\| EFFECTIVE_DATE) → exp_Determine_Errors.v_ERROR_FLAG_6 = IIF(NOT IS_DATE( SUBSTR(EFFECTIVE_DATE, 5, 2) \|\| '/' \|\| SUBSTR(EFFECTIVE_DATE, 7, 2) \|\| '/' \|\| SUBSTR(EFFECTIVE_DATE, 1, 4) ,'MM/DD/YYYY'), TRUE, FALSE) | PSEUDOSSN_FILE.CAN_CD; PSEUDOSSN_FILE.EFFECTIVE_DATE; PSEUDOSSN_FILE.EMPLOYEE_STATUS; PSEUDOSSN_FILE.PSEUDO_SSN; PSEUDOSSN_FILE.SSN |
| ERROR_TBL | SOURCE_KEY | exp_Final_Errors.SOURCE_KEY → exp_Pay_Period.SOURCE_KEY → fil_Error_Message.SOURCE_KEY → nrm_Errors.SRC_KEY [normalizer: one row per occurrence of SRC_KEY_in] → rtr_Good_Bad_Records.SRC_KEY3 [router group BAD_RECORDS WHERE ERROR_FLAG = TRUE] → exp_Determine_Errors.o_SRC_KEY = SSN \|\| ' \|\| ' \|\| CAN_CD \|\| ' \|\| ' \|\| EFFECTIVE_DATE \|\| ' \|\| ' → srt_PSEUDOSSN_EFF_DT.SSN → fil_Detail_Records.SSN → exp_Determine_Record_Type.SSN → SQ_PSEUDOSSN_FILE.SSN → PSEUDOSSN_FILE.SSN → srt_PSEUDOSSN_EFF_DT.CAN_CD → fil_Detail_Records.CAN_CD → exp_Determine_Record_Type.CAN_CD → SQ_PSEUDOSSN_FILE.CAN_CD → PSEUDOSSN_FILE.CAN_CD → srt_PSEUDOSSN_EFF_DT.EFFECTIVE_DATE → fil_Detail_Records.EFFECTIVE_DATE → exp_Determine_Record_Type.EFFECTIVE_DATE → SQ_PSEUDOSSN_FILE.EFFECTIVE_DATE → PSEUDOSSN_FILE.EFFECTIVE_DATE | PSEUDOSSN_FILE.CAN_CD; PSEUDOSSN_FILE.EFFECTIVE_DATE; PSEUDOSSN_FILE.SSN |
| ERROR_TBL | ERROR_DATE | exp_Final_Errors.o_ERROR_DATE = SESSSTARTTIME | literal/expression: SESSSTARTTIME |
| ERROR_TBL | PP_END_YEAR | exp_Final_Errors.lkp_PP_END_YEAR → lkp_Current_Pay_Period1.PP_END_YEAR [lookup PAY_PERIOD.PP_END_YEAR ON CURR_PP_FLAG = in_CURR_PP_FLAG] | PAY_PERIOD.PP_END_YEAR (lookup); literal/expression: 'Y' (lookup key) |
| ERROR_TBL | PP_NUM | exp_Final_Errors.lkp_PP_NUM → lkp_Current_Pay_Period1.PP_NUM [lookup PAY_PERIOD.PP_NUM ON CURR_PP_FLAG = in_CURR_PP_FLAG] | PAY_PERIOD.PP_NUM (lookup); literal/expression: 'Y' (lookup key) |
| ERROR_TBL | CYCLE_ID | (not connected — NULL) | — |
| ERROR_TBL | ERROR_CODE | (not connected — NULL) | — |

### Target instance `PSEUDOSSN_TBL` (table `PSEUDOSSN_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| PSEUDOSSN_TBL | SSN | exp_Final.SSN → exp_Conversions.SSN → rtr_Good_Bad_Records.SSN1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.SSN → srt_PSEUDOSSN_EFF_DT.SSN → fil_Detail_Records.SSN → exp_Determine_Record_Type.SSN → SQ_PSEUDOSSN_FILE.SSN → PSEUDOSSN_FILE.SSN | PSEUDOSSN_FILE.SSN |
| PSEUDOSSN_TBL | CAN_CD | exp_Final.CAN_CD → exp_Conversions.CAN_CD → rtr_Good_Bad_Records.CAN_CD1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.CAN_CD → srt_PSEUDOSSN_EFF_DT.CAN_CD → fil_Detail_Records.CAN_CD → exp_Determine_Record_Type.CAN_CD → SQ_PSEUDOSSN_FILE.CAN_CD → PSEUDOSSN_FILE.CAN_CD | PSEUDOSSN_FILE.CAN_CD |
| PSEUDOSSN_TBL | PSEUDOSSN | exp_Final.PSEUDOSSN → exp_Conversions.PSEUDOSSN → rtr_Good_Bad_Records.PSEUDO_SSN1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.PSEUDO_SSN → srt_PSEUDOSSN_EFF_DT.PSEUDO_SSN → fil_Detail_Records.PSEUDO_SSN → exp_Determine_Record_Type.PSEUDO_SSN → SQ_PSEUDOSSN_FILE.PSEUDO_SSN → PSEUDOSSN_FILE.PSEUDO_SSN | PSEUDOSSN_FILE.PSEUDO_SSN |
| PSEUDOSSN_TBL | EMPLID | exp_Final.EMPLID → exp_Conversions.EMPLID → rtr_Good_Bad_Records.EIN1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.EIN → srt_PSEUDOSSN_EFF_DT.EIN → fil_Detail_Records.EIN → exp_Determine_Record_Type.EIN → SQ_PSEUDOSSN_FILE.EIN → PSEUDOSSN_FILE.EIN | PSEUDOSSN_FILE.EIN |
| PSEUDOSSN_TBL | EMPL_RCD | exp_Final.EMPL_RCD → exp_Conversions.EMPL_RCD → rtr_Good_Bad_Records.EMP_REC_NO1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.EMP_REC_NO → srt_PSEUDOSSN_EFF_DT.EMP_REC_NO → fil_Detail_Records.EMP_REC_NO → exp_Determine_Record_Type.EMP_REC_NO → SQ_PSEUDOSSN_FILE.EMP_REC_NO → PSEUDOSSN_FILE.EMP_REC_NO | PSEUDOSSN_FILE.EMP_REC_NO |
| PSEUDOSSN_TBL | APPT_NUM | exp_Final.APPT_NUM → exp_Conversions.APPT_NUM → rtr_Good_Bad_Records.LEGACY_APPT_NO1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.LEGACY_APPT_NO → srt_PSEUDOSSN_EFF_DT.LEGACY_APPT_NO → fil_Detail_Records.LEGACY_APPT_NO → exp_Determine_Record_Type.LEGACY_APPT_NO → SQ_PSEUDOSSN_FILE.LEGACY_APPT_NO → PSEUDOSSN_FILE.LEGACY_APPT_NO | PSEUDOSSN_FILE.LEGACY_APPT_NO |
| PSEUDOSSN_TBL | EMP_FIRST_NAME | exp_Final.EMP_FIRST_NAME → exp_Conversions.EMP_FIRST_NAME → rtr_Good_Bad_Records.FIRST_NAME1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.FIRST_NAME → srt_PSEUDOSSN_EFF_DT.FIRST_NAME → fil_Detail_Records.FIRST_NAME → exp_Determine_Record_Type.FIRST_NAME → SQ_PSEUDOSSN_FILE.FIRST_NAME → PSEUDOSSN_FILE.FIRST_NAME | PSEUDOSSN_FILE.FIRST_NAME |
| PSEUDOSSN_TBL | EMP_MID_INIT | exp_Final.EMP_MID_INIT → exp_Conversions.EMP_MID_INIT → rtr_Good_Bad_Records.MIDDLE_INIT1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.MIDDLE_INIT → srt_PSEUDOSSN_EFF_DT.MIDDLE_INIT → fil_Detail_Records.MIDDLE_INIT → exp_Determine_Record_Type.MIDDLE_INIT → SQ_PSEUDOSSN_FILE.MIDDLE_INIT → PSEUDOSSN_FILE.MIDDLE_INIT | PSEUDOSSN_FILE.MIDDLE_INIT |
| PSEUDOSSN_TBL | EMP_LAST_NAME | exp_Final.EMP_LAST_NAME → exp_Conversions.EMP_LAST_NAME → rtr_Good_Bad_Records.LAST_NAME1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.LAST_NAME → srt_PSEUDOSSN_EFF_DT.LAST_NAME → fil_Detail_Records.LAST_NAME → exp_Determine_Record_Type.LAST_NAME → SQ_PSEUDOSSN_FILE.LAST_NAME → PSEUDOSSN_FILE.LAST_NAME | PSEUDOSSN_FILE.LAST_NAME |
| PSEUDOSSN_TBL | SEX | exp_Final.SEX → exp_Conversions.SEX → rtr_Good_Bad_Records.SEX1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.SEX → srt_PSEUDOSSN_EFF_DT.SEX → fil_Detail_Records.SEX → exp_Determine_Record_Type.SEX → SQ_PSEUDOSSN_FILE.SEX → PSEUDOSSN_FILE.SEX | PSEUDOSSN_FILE.SEX |
| PSEUDOSSN_TBL | VETERANS_PREFERENCE_CD | exp_Final.VETERANS_PREFERENCE_CD → exp_Conversions.VETERANS_PREFERENCE_CD → rtr_Good_Bad_Records.VET_PREF1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.VET_PREF → srt_PSEUDOSSN_EFF_DT.VET_PREF → fil_Detail_Records.VET_PREF → exp_Determine_Record_Type.VET_PREF → SQ_PSEUDOSSN_FILE.VET_PREF → PSEUDOSSN_FILE.VET_PREF | PSEUDOSSN_FILE.VET_PREF |
| PSEUDOSSN_TBL | TENURE_CD | exp_Final.TENURE_CD → exp_Conversions.TENURE_CD → rtr_Good_Bad_Records.TENURE_CD1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.TENURE_CD → srt_PSEUDOSSN_EFF_DT.TENURE_CD → fil_Detail_Records.TENURE_CD → exp_Determine_Record_Type.TENURE_CD → SQ_PSEUDOSSN_FILE.TENURE_CD → PSEUDOSSN_FILE.TENURE_CD | PSEUDOSSN_FILE.TENURE_CD |
| PSEUDOSSN_TBL | POSITION_NUM | exp_Final.POSITION_NUM → exp_Conversions.POSITION_NUM → rtr_Good_Bad_Records.POSITION_CD1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.POSITION_CD → srt_PSEUDOSSN_EFF_DT.POSITION_CD → fil_Detail_Records.POSITION_CD → exp_Determine_Record_Type.POSITION_CD → SQ_PSEUDOSSN_FILE.POSITION_CD → PSEUDOSSN_FILE.POSITION_CD | PSEUDOSSN_FILE.POSITION_CD |
| PSEUDOSSN_TBL | US_CITIZENSHIP_CD | exp_Final.US_CITIZENSHIP_CD → exp_Conversions.US_CITIZENSHIP_CD → rtr_Good_Bad_Records.CITIZENSHIP_STATUS1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.CITIZENSHIP_STATUS → srt_PSEUDOSSN_EFF_DT.CITIZENSHIP_STATUS → fil_Detail_Records.CITIZENSHIP_STATUS → exp_Determine_Record_Type.CITIZENSHIP_STATUS → SQ_PSEUDOSSN_FILE.CITIZENSHIP_STATUS → PSEUDOSSN_FILE.CITIZENSHIP_STATUS | PSEUDOSSN_FILE.CITIZENSHIP_STATUS |
| PSEUDOSSN_TBL | APPT_TYPE_CD | exp_Final.APPT_TYPE_CD → exp_Conversions.APPT_TYPE_CD → rtr_Good_Bad_Records.APPT_TYPE_CD1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.APPT_TYPE_CD → srt_PSEUDOSSN_EFF_DT.APPT_TYPE_CD → fil_Detail_Records.APPT_TYPE_CD → exp_Determine_Record_Type.APPT_TYPE_CD → SQ_PSEUDOSSN_FILE.APPT_TYPE_CD → PSEUDOSSN_FILE.APPT_TYPE_CD | PSEUDOSSN_FILE.APPT_TYPE_CD |
| PSEUDOSSN_TBL | HIRE_DATE | exp_Final.HIRE_DATE → exp_Conversions.o_HIRE_DATE = IIF(IS_DATE(v_HIRE_DATE, 'MM/DD/YYYY'), TO_DATE(v_HIRE_DATE, 'MM/DD/YYYY')) → exp_Conversions.v_HIRE_DATE = SUBSTR(in_HIRE_DATE, 1, 2) \|\| '/' \|\| SUBSTR(in_HIRE_DATE, 3, 2) \|\| '/' \|\| SUBSTR(in_HIRE_DATE, 5, 4) -- Builds date in 'MM/DD/YYYY' format, source date format is MMDDYYYY → rtr_Good_Bad_Records.HIRE_DATE1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.HIRE_DATE → srt_PSEUDOSSN_EFF_DT.HIRE_DATE → fil_Detail_Records.HIRE_DATE → exp_Determine_Record_Type.HIRE_DATE → SQ_PSEUDOSSN_FILE.HIRE_DATE → PSEUDOSSN_FILE.HIRE_DATE | PSEUDOSSN_FILE.HIRE_DATE |
| PSEUDOSSN_TBL | HANDICAP_CD | exp_Final.HANDICAP_CD → exp_Conversions.HANDICAP_CD → rtr_Good_Bad_Records.HANDICAP_CODE1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.HANDICAP_CODE → srt_PSEUDOSSN_EFF_DT.HANDICAP_CODE → fil_Detail_Records.HANDICAP_CODE → exp_Determine_Record_Type.HANDICAP_CODE → SQ_PSEUDOSSN_FILE.HANDICAP_CODE → PSEUDOSSN_FILE.HANDICAP_CODE | PSEUDOSSN_FILE.HANDICAP_CODE |
| PSEUDOSSN_TBL | UNF_ALLOW_CD | exp_Final.UNF_ALLOW_CD → exp_Conversions.UNF_ALLOW_CD → rtr_Good_Bad_Records.UNIF_ALLOW_CODE1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.UNIF_ALLOW_CODE → srt_PSEUDOSSN_EFF_DT.UNIF_ALLOW_CODE → fil_Detail_Records.UNIF_ALLOW_CODE → exp_Determine_Record_Type.UNIF_ALLOW_CODE → SQ_PSEUDOSSN_FILE.UNIF_ALLOW_CODE → PSEUDOSSN_FILE.UNIF_ALLOW_CODE | PSEUDOSSN_FILE.UNIF_ALLOW_CODE |
| PSEUDOSSN_TBL | UNIF_ALLOW_DATE | exp_Final.UNIF_ALLOW_DATE → exp_Conversions.o_UNIF_ALLOW_DATE = IIF(IS_DATE(v_UNIF_ALLOW_DATE, 'MM/DD/YYYY'), TO_DATE(v_UNIF_ALLOW_DATE, 'MM/DD/YYYY')) → exp_Conversions.v_UNIF_ALLOW_DATE = SUBSTR(in_UNIF_ALLOW_DATE, 5, 2) \|\| '/' \|\| SUBSTR(in_UNIF_ALLOW_DATE, 7, 2) \|\| '/' \|\| SUBSTR(in_UNIF_ALLOW_DATE, 1, 4) -- Builds date in 'MM/DD/YYYY' format, source date format is YYYYMMDD → rtr_Good_Bad_Records.UNIF_ALLOW_DATE1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.UNIF_ALLOW_DATE → srt_PSEUDOSSN_EFF_DT.UNIF_ALLOW_DATE → fil_Detail_Records.UNIF_ALLOW_DATE → exp_Determine_Record_Type.UNIF_ALLOW_DATE → SQ_PSEUDOSSN_FILE.UNIF_ALLOW_DATE → PSEUDOSSN_FILE.UNIF_ALLOW_DATE | PSEUDOSSN_FILE.UNIF_ALLOW_DATE |
| PSEUDOSSN_TBL | UNIF_ALLOW_AMT | exp_Final.UNIF_ALLOW_AMT → exp_Conversions.o_UNIF_ALLOW_AMT = DECODE(TRUE, IS_NUMBER(v_UNIF_ALLOW_AMT) AND v_UNIF_ALLOW_AMT_SIGN = '+', TO_DECIMAL(v_UNIF_ALLOW_AMT, 2), IS_NUMBER(v_UNIF_ALLOW_AMT) AND v_UNIF_ALLOW_AMT_SIGN = '-', TO_DECIMAL(v_UNIF_ALLOW_AMT, 2) * -1, IS_NUMBER(v_UNIF_ALLOW_AMT), TO_DECIMAL(v_UNIF_ALLOW_AMT, 2), 0) → exp_Conversions.v_UNIF_ALLOW_AMT = SUBSTR(in_UNIF_ALLOW_AMT,1, 3) \|\| '.' \|\| SUBSTR(in_UNIF_ALLOW_AMT,4, 2) → rtr_Good_Bad_Records.UNIF_ALLOW_AMT1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.UNIF_ALLOW_AMT → srt_PSEUDOSSN_EFF_DT.UNIF_ALLOW_AMT → fil_Detail_Records.UNIF_ALLOW_AMT → exp_Determine_Record_Type.UNIF_ALLOW_AMT → SQ_PSEUDOSSN_FILE.UNIF_ALLOW_AMT → PSEUDOSSN_FILE.UNIF_ALLOW_AMT → exp_Conversions.v_UNIF_ALLOW_AMT_SIGN = SUBSTR(in_UNIF_ALLOW_AMT, 6, 1) | PSEUDOSSN_FILE.UNIF_ALLOW_AMT |
| PSEUDOSSN_TBL | RSSSDP | exp_Final.RSSSDP → exp_Conversions.RSSSDP → rtr_Good_Bad_Records.RSSSDP1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.RSSSDP → srt_PSEUDOSSN_EFF_DT.RSSSDP → fil_Detail_Records.RSSSDP → exp_Determine_Record_Type.RSSSDP → SQ_PSEUDOSSN_FILE.RSSSDP → PSEUDOSSN_FILE.RSSSDP | PSEUDOSSN_FILE.RSSSDP |
| PSEUDOSSN_TBL | CEIL_REPORTING_CD | exp_Final.CEIL_REPORTING_CD → exp_Conversions.CEIL_REPORTING_CODE → rtr_Good_Bad_Records.CEILING_CODE1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.CEILING_CODE → srt_PSEUDOSSN_EFF_DT.CEILING_CODE → fil_Detail_Records.CEILING_CODE → exp_Determine_Record_Type.CEILING_CODE → SQ_PSEUDOSSN_FILE.CEILING_CODE → PSEUDOSSN_FILE.CEILING_CODE | PSEUDOSSN_FILE.CEILING_CODE |
| PSEUDOSSN_TBL | FUNCTNL_CLASSFCTN_CD | exp_Final.FUNCTNL_CLASSFCTN_CD → exp_Conversions.FUNCTNL_CLASSFCTN_CODE → rtr_Good_Bad_Records.FUNCTION_CODE1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.FUNCTION_CODE → srt_PSEUDOSSN_EFF_DT.FUNCTION_CODE → fil_Detail_Records.FUNCTION_CODE → exp_Determine_Record_Type.FUNCTION_CODE → SQ_PSEUDOSSN_FILE.FUNCTION_CODE → PSEUDOSSN_FILE.FUNCTION_CODE | PSEUDOSSN_FILE.FUNCTION_CODE |
| PSEUDOSSN_TBL | EMP_STATUS | exp_Final.EMP_STATUS → exp_Conversions.EMP_STATUS → rtr_Good_Bad_Records.EMPLOYEE_STATUS1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.EMPLOYEE_STATUS → srt_PSEUDOSSN_EFF_DT.EMPLOYEE_STATUS → fil_Detail_Records.EMPLOYEE_STATUS → exp_Determine_Record_Type.EMPLOYEE_STATUS → SQ_PSEUDOSSN_FILE.EMPLOYEE_STATUS → PSEUDOSSN_FILE.EMPLOYEE_STATUS | PSEUDOSSN_FILE.EMPLOYEE_STATUS |
| PSEUDOSSN_TBL | MANAGER_STATUS | exp_Final.MANAGER_STATUS → exp_Conversions.MANAGER_STATUS → rtr_Good_Bad_Records.MANAGER_STATUS1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.MANAGER_STATUS → srt_PSEUDOSSN_EFF_DT.MANAGER_STATUS → fil_Detail_Records.MANAGER_STATUS → exp_Determine_Record_Type.MANAGER_STATUS → SQ_PSEUDOSSN_FILE.MANAGER_STATUS → PSEUDOSSN_FILE.MANAGER_STATUS | PSEUDOSSN_FILE.MANAGER_STATUS |
| PSEUDOSSN_TBL | POSITION_SENSITIVITY_CD | exp_Final.POSITION_SENSITIVITY_CD → exp_Conversions.POSITION_SENSITIVITY_CD → rtr_Good_Bad_Records.POSITION_SENS_CODE1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.POSITION_SENS_CODE → srt_PSEUDOSSN_EFF_DT.POSITION_SENS_CODE → fil_Detail_Records.POSITION_SENS_CODE → exp_Determine_Record_Type.POSITION_SENS_CODE → SQ_PSEUDOSSN_FILE.POSITION_SENS_CODE → PSEUDOSSN_FILE.POSITION_SENS_CODE | PSEUDOSSN_FILE.POSITION_SENS_CODE |
| PSEUDOSSN_TBL | CAREER_START_DATE | exp_Final.CAREER_START_DATE → exp_Conversions.o_CAREER_START_DATE = IIF(IS_DATE(v_CAREER_START_DATE, 'MM/DD/YYYY'), TO_DATE(v_CAREER_START_DATE, 'MM/DD/YYYY')) → exp_Conversions.v_CAREER_START_DATE = SUBSTR(in_CAREER_START_DATE, 1, 2) \|\| '/' \|\| SUBSTR(in_CAREER_START_DATE, 3, 2) \|\| '/' \|\| SUBSTR(in_CAREER_START_DATE, 5, 4) -- Builds date in 'MM/DD/YYYY' format, source date format is MMDDYYYY → rtr_Good_Bad_Records.CAREER_START_DATE1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.CAREER_START_DATE → srt_PSEUDOSSN_EFF_DT.CAREER_START_DATE → fil_Detail_Records.CAREER_START_DATE → exp_Determine_Record_Type.CAREER_START_DATE → SQ_PSEUDOSSN_FILE.CAREER_START_DATE → PSEUDOSSN_FILE.CAREER_START_DATE | PSEUDOSSN_FILE.CAREER_START_DATE |
| PSEUDOSSN_TBL | CAREER_CONV_DATE | exp_Final.CAREER_CONV_DATE → exp_Conversions.o_CAREER_CONV_DATE = IIF(IS_DATE(v_CAREER_CONV_DATE, 'MM/DD/YYYY'), TO_DATE(v_CAREER_CONV_DATE, 'MM/DD/YYYY')) → exp_Conversions.v_CAREER_CONV_DATE = SUBSTR(in_CAREER_CONV_DATE, 1, 2) \|\| '/' \|\| SUBSTR(in_CAREER_CONV_DATE, 3, 2) \|\| '/' \|\| SUBSTR(in_CAREER_CONV_DATE, 5, 4) -- Builds date in 'MM/DD/YYYY' format, source date format is MMDDYYYY → rtr_Good_Bad_Records.CAREER_CONV_DATE1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.CAREER_CONV_DATE → srt_PSEUDOSSN_EFF_DT.CAREER_CONV_DATE → fil_Detail_Records.CAREER_CONV_DATE → exp_Determine_Record_Type.CAREER_CONV_DATE → SQ_PSEUDOSSN_FILE.CAREER_CONV_DATE → PSEUDOSSN_FILE.CAREER_CONV_DATE | PSEUDOSSN_FILE.CAREER_CONV_DATE |
| PSEUDOSSN_TBL | PROBATION_DATE | exp_Final.PROBATION_DATE → exp_Conversions.o_PROBATION_DATE = IIF(IS_DATE(v_PROBATION_DATE, 'MM/DD/YYYY'), TO_DATE(v_PROBATION_DATE, 'MM/DD/YYYY')) → exp_Conversions.v_PROBATION_DATE = SUBSTR(in_PROBATION_DATE, 1, 2) \|\| '/' \|\| SUBSTR(in_PROBATION_DATE, 3, 2) \|\| '/' \|\| SUBSTR(in_PROBATION_DATE, 5, 4) -- Builds date in 'MM/DD/YYYY' format, source date format is MMDDYYYY → rtr_Good_Bad_Records.PROBATION_DATE1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.PROBATION_DATE → srt_PSEUDOSSN_EFF_DT.PROBATION_DATE → fil_Detail_Records.PROBATION_DATE → exp_Determine_Record_Type.PROBATION_DATE → SQ_PSEUDOSSN_FILE.PROBATION_DATE → PSEUDOSSN_FILE.PROBATION_DATE | PSEUDOSSN_FILE.PROBATION_DATE |
| PSEUDOSSN_TBL | ABNORMAL_RATE_CD | exp_Final.ABNORMAL_RATE_CD → exp_Conversions.ABNORMAL_RATE_CD → rtr_Good_Bad_Records.ABNORMAL_RATE_CODE1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.ABNORMAL_RATE_CODE → srt_PSEUDOSSN_EFF_DT.ABNORMAL_RATE_CODE → fil_Detail_Records.ABNORMAL_RATE_CODE → exp_Determine_Record_Type.ABNORMAL_RATE_CODE → SQ_PSEUDOSSN_FILE.ABNORMAL_RATE_CODE → PSEUDOSSN_FILE.ABNORMAL_RATE_CODE | PSEUDOSSN_FILE.ABNORMAL_RATE_CODE |
| PSEUDOSSN_TBL | APPT_LIMIT_HRS | exp_Final.APPT_LIMIT_HRS → exp_Conversions.o_APPT_LIMIT_HRS = DECODE(TRUE, IS_NUMBER(v_APPT_LIMIT_HRS) AND v_APPT_LIMIT_HRS = '+', TO_DECIMAL(v_APPT_LIMIT_HRS, 2), IS_NUMBER(v_APPT_LIMIT_HRS) AND v_APPT_LIMIT_HRS_SIGN = '-', TO_DECIMAL(v_APPT_LIMIT_HRS, 2) * -1, IS_NUMBER(v_APPT_LIMIT_HRS), TO_DECIMAL(v_APPT_LIMIT_HRS, 2), 0) → exp_Conversions.v_APPT_LIMIT_HRS = SUBSTR(in_APPT_LIMIT_HRS,1, 4) \|\| '.' \|\| SUBSTR(in_APPT_LIMIT_HRS,5, 2) → rtr_Good_Bad_Records.APPT_LIMIT_HRS1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.APPT_LIMIT_HRS → srt_PSEUDOSSN_EFF_DT.APPT_LIMIT_HRS → fil_Detail_Records.APPT_LIMIT_HRS → exp_Determine_Record_Type.APPT_LIMIT_HRS → SQ_PSEUDOSSN_FILE.APPT_LIMIT_HRS → PSEUDOSSN_FILE.APPT_LIMIT_HRS → exp_Conversions.v_APPT_LIMIT_HRS_SIGN = SUBSTR(in_APPT_LIMIT_HRS, 7, 1) | PSEUDOSSN_FILE.APPT_LIMIT_HRS |
| PSEUDOSSN_TBL | APPT_LIMIT_PAY | exp_Final.APPT_LIMIT_PAY → exp_Conversions.o_APPT_LIMIT_PAY = DECODE(TRUE, IS_NUMBER(v_APPT_LIMIT_PAY) AND v_APPT_LIMIT_PAY_SIGN = '+', TO_DECIMAL(v_APPT_LIMIT_PAY, 2), IS_NUMBER(v_APPT_LIMIT_PAY) AND v_APPT_LIMIT_PAY_SIGN = '-', TO_DECIMAL(v_APPT_LIMIT_PAY, 2) * -1, IS_NUMBER(v_APPT_LIMIT_PAY), TO_DECIMAL(v_APPT_LIMIT_PAY, 2), 0) → exp_Conversions.v_APPT_LIMIT_PAY = SUBSTR(in_APPT_LIMIT_PAY,1, 5) \|\| '.' \|\| SUBSTR(in_APPT_LIMIT_PAY,6, 2) → rtr_Good_Bad_Records.APPT_LIMIT_PAY1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.APPT_LIMIT_PAY → srt_PSEUDOSSN_EFF_DT.APPT_LIMIT_PAY → fil_Detail_Records.APPT_LIMIT_PAY → exp_Determine_Record_Type.APPT_LIMIT_PAY → SQ_PSEUDOSSN_FILE.APPT_LIMIT_PAY → PSEUDOSSN_FILE.APPT_LIMIT_PAY → exp_Conversions.v_APPT_LIMIT_PAY_SIGN = SUBSTR(in_APPT_LIMIT_PAY, 8, 1) | PSEUDOSSN_FILE.APPT_LIMIT_PAY |
| PSEUDOSSN_TBL | LAST_PAY_CHANGE | exp_Final.LAST_PAY_CHANGE → exp_Conversions.o_LAST_PAY_CHANGE = IIF(IS_DATE(v_LAST_PAY_CHANGE, 'MM/DD/YYYY'), TO_DATE(v_LAST_PAY_CHANGE, 'MM/DD/YYYY')) → exp_Conversions.v_LAST_PAY_CHANGE = SUBSTR(in_LAST_PAY_CHANGE, 1, 2) \|\| '/' \|\| SUBSTR(in_LAST_PAY_CHANGE, 3, 2) \|\| '/' \|\| SUBSTR(in_LAST_PAY_CHANGE, 5, 4) -- Builds date in 'MM/DD/YYYY' format, source date format is MMDDYYYY → rtr_Good_Bad_Records.LAST_PAY_CHANGE1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.LAST_PAY_CHANGE → srt_PSEUDOSSN_EFF_DT.LAST_PAY_CHANGE → fil_Detail_Records.LAST_PAY_CHANGE → exp_Determine_Record_Type.LAST_PAY_CHANGE → SQ_PSEUDOSSN_FILE.LAST_PAY_CHANGE → PSEUDOSSN_FILE.LAST_PAY_CHANGE | PSEUDOSSN_FILE.LAST_PAY_CHANGE |
| PSEUDOSSN_TBL | CHARITY_AREA_CD | exp_Final.CHARITY_AREA_CD → exp_Conversions.CHARITY_AREA_CD → rtr_Good_Bad_Records.CHARITY_AREA_CODE1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.CHARITY_AREA_CODE → srt_PSEUDOSSN_EFF_DT.CHARITY_AREA_CODE → fil_Detail_Records.CHARITY_AREA_CODE → exp_Determine_Record_Type.CHARITY_AREA_CODE → SQ_PSEUDOSSN_FILE.CHARITY_AREA_CODE → PSEUDOSSN_FILE.CHARITY_AREA_CODE | PSEUDOSSN_FILE.CHARITY_AREA_CODE |
| PSEUDOSSN_TBL | CHARITY_EFF_DATE | exp_Final.CHARITY_EFF_DATE → exp_Conversions.o_CHARITY_EFF_DATE = IIF(IS_DATE(v_CHARITY_EFF_DATE, 'MM/DD/YYYY'), TO_DATE(v_CHARITY_EFF_DATE, 'MM/DD/YYYY')) → exp_Conversions.v_CHARITY_EFF_DATE = SUBSTR(in_CHARITY_EFF_DATE, 5, 2) \|\| '/' \|\| SUBSTR(in_CHARITY_EFF_DATE, 7, 2) \|\| '/' \|\| SUBSTR(in_CHARITY_EFF_DATE, 1, 4) -- Builds date in 'MM/DD/YYYY' format, source date format is YYYYDDMM → rtr_Good_Bad_Records.CHARITY_EFF_DATE1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.CHARITY_EFF_DATE → srt_PSEUDOSSN_EFF_DT.CHARITY_EFF_DATE → fil_Detail_Records.CHARITY_EFF_DATE → exp_Determine_Record_Type.CHARITY_EFF_DATE → SQ_PSEUDOSSN_FILE.CHARITY_EFF_DATE → PSEUDOSSN_FILE.CHARITY_EFF_DATE | PSEUDOSSN_FILE.CHARITY_EFF_DATE |
| PSEUDOSSN_TBL | CHARITY_DED_AMT | exp_Final.CHARITY_DED_AMT → exp_Conversions.o_CHARITY_DED_AMT = DECODE(TRUE, IS_NUMBER(v_CHARITY_DED_AMT) AND v_CHARITY_DED_AMT_SIGN = '+', TO_DECIMAL(v_CHARITY_DED_AMT, 2), IS_NUMBER(v_CHARITY_DED_AMT) AND v_CHARITY_DED_AMT_SIGN = '-', TO_DECIMAL(v_CHARITY_DED_AMT, 2) * -1, IS_NUMBER(v_CHARITY_DED_AMT), TO_DECIMAL(v_CHARITY_DED_AMT, 2), 0) → exp_Conversions.v_CHARITY_DED_AMT = SUBSTR(in_CHARITY_DED_AMT,1, 3) \|\| '.' \|\| SUBSTR(in_CHARITY_DED_AMT,4, 2) → rtr_Good_Bad_Records.CHARITY_DED_AMT1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.CHARITY_DED_AMT → srt_PSEUDOSSN_EFF_DT.CHARITY_DED_AMT → fil_Detail_Records.CHARITY_DED_AMT → exp_Determine_Record_Type.CHARITY_DED_AMT → SQ_PSEUDOSSN_FILE.CHARITY_DED_AMT → PSEUDOSSN_FILE.CHARITY_DED_AMT → exp_Conversions.v_CHARITY_DED_AMT_SIGN = SUBSTR(in_CHARITY_DED_AMT, 6, 1) | PSEUDOSSN_FILE.CHARITY_DED_AMT |
| PSEUDOSSN_TBL | LAST_NOA_CD | exp_Final.LAST_NOA_CD → exp_Conversions.LAST_NOA_CD → rtr_Good_Bad_Records.LAST_NOA1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.LAST_NOA → srt_PSEUDOSSN_EFF_DT.LAST_NOA → fil_Detail_Records.LAST_NOA → exp_Determine_Record_Type.LAST_NOA → SQ_PSEUDOSSN_FILE.LAST_NOA → PSEUDOSSN_FILE.LAST_NOA | PSEUDOSSN_FILE.LAST_NOA |
| PSEUDOSSN_TBL | QUARTERS_DED_AMT | exp_Final.QUARTERS_DED_AMT → exp_Conversions.o_QUARTERS_DED_AMT = DECODE(TRUE, IS_NUMBER(v_QUARTERS_DED_AMT) AND v_QUARTERS_DED_AMT_SIGN = '+', TO_DECIMAL(v_QUARTERS_DED_AMT, 2), IS_NUMBER(v_QUARTERS_DED_AMT) AND v_QUARTERS_DED_AMT_SIGN = '-', TO_DECIMAL(v_QUARTERS_DED_AMT, 2) * -1, IS_NUMBER(v_QUARTERS_DED_AMT), TO_DECIMAL(v_QUARTERS_DED_AMT, 2), 0) → exp_Conversions.v_QUARTERS_DED_AMT = SUBSTR(in_QUARTERS_DEDUCTION,1, 5) \|\| '.' \|\| SUBSTR(in_QUARTERS_DEDUCTION,6, 2) → rtr_Good_Bad_Records.QUARTERS_DEDUCTION1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.QUARTERS_DEDUCTION → srt_PSEUDOSSN_EFF_DT.QUARTERS_DEDUCTION → fil_Detail_Records.QUARTERS_DEDUCTION → exp_Determine_Record_Type.QUARTERS_DEDUCTION → SQ_PSEUDOSSN_FILE.QUARTERS_DEDUCTION → PSEUDOSSN_FILE.QUARTERS_DEDUCTION → exp_Conversions.v_QUARTERS_DED_AMT_SIGN = SUBSTR(in_QUARTERS_DEDUCTION, 8, 1) | PSEUDOSSN_FILE.QUARTERS_DEDUCTION |
| PSEUDOSSN_TBL | SUBSIST_DED_AMT | exp_Final.SUBSIST_DED_AMT → exp_Conversions.o_SUBSIST_DED_AMT = DECODE(TRUE, IS_NUMBER(v_SUBSIST_DEDUCTION_AMT) AND v_SUBSIST_DEDUCTION_AMT_SIGN = '+', TO_DECIMAL(v_QUARTERS_DED_AMT, 2), IS_NUMBER(v_SUBSIST_DEDUCTION_AMT) AND v_SUBSIST_DEDUCTION_AMT_SIGN = '-', TO_DECIMAL(v_SUBSIST_DEDUCTION_AMT, 2) * -1, IS_NUMBER(v_SUBSIST_DEDUCTION_AMT), TO_DECIMAL(v_QUARTERS_DED_AMT, 2), 0) → exp_Conversions.v_SUBSIST_DEDUCTION_AMT = SUBSTR(in_SUBSIST_DEDUCTION,1, 5) \|\| '.' \|\| SUBSTR(in_SUBSIST_DEDUCTION,6, 2) → rtr_Good_Bad_Records.SUBSIST_DEDUCTION1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.SUBSIST_DEDUCTION → srt_PSEUDOSSN_EFF_DT.SUBSIST_DEDUCTION → fil_Detail_Records.SUBSIST_DEDUCTION → exp_Determine_Record_Type.SUBSIST_DEDUCTION → SQ_PSEUDOSSN_FILE.SUBSIST_DEDUCTION → PSEUDOSSN_FILE.SUBSIST_DEDUCTION → exp_Conversions.v_SUBSIST_DEDUCTION_AMT_SIGN = SUBSTR(in_SUBSIST_DEDUCTION, 8, 1) → exp_Conversions.v_QUARTERS_DED_AMT = SUBSTR(in_QUARTERS_DEDUCTION,1, 5) \|\| '.' \|\| SUBSTR(in_QUARTERS_DEDUCTION,6, 2) → rtr_Good_Bad_Records.QUARTERS_DEDUCTION1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.QUARTERS_DEDUCTION → srt_PSEUDOSSN_EFF_DT.QUARTERS_DEDUCTION → fil_Detail_Records.QUARTERS_DEDUCTION → exp_Determine_Record_Type.QUARTERS_DEDUCTION → SQ_PSEUDOSSN_FILE.QUARTERS_DEDUCTION → PSEUDOSSN_FILE.QUARTERS_DEDUCTION | PSEUDOSSN_FILE.QUARTERS_DEDUCTION; PSEUDOSSN_FILE.SUBSIST_DEDUCTION |
| PSEUDOSSN_TBL | PAY_BASIS_CD | exp_Final.PAY_BASIS_CD → exp_Conversions.PAY_BASIS_CD → rtr_Good_Bad_Records.PAY_BASIS1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.PAY_BASIS → srt_PSEUDOSSN_EFF_DT.PAY_BASIS → fil_Detail_Records.PAY_BASIS → exp_Determine_Record_Type.PAY_BASIS → SQ_PSEUDOSSN_FILE.PAY_BASIS → PSEUDOSSN_FILE.PAY_BASIS | PSEUDOSSN_FILE.PAY_BASIS |
| PSEUDOSSN_TBL | WORK_SCHEDULE_CD | exp_Final.WORK_SCHEDULE_CD → exp_Conversions.WORK_SCHEDULE_CD → rtr_Good_Bad_Records.WORK_SCHEDULE1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.WORK_SCHEDULE → srt_PSEUDOSSN_EFF_DT.WORK_SCHEDULE → fil_Detail_Records.WORK_SCHEDULE → exp_Determine_Record_Type.WORK_SCHEDULE → SQ_PSEUDOSSN_FILE.WORK_SCHEDULE → PSEUDOSSN_FILE.WORK_SCHEDULE | PSEUDOSSN_FILE.WORK_SCHEDULE |
| PSEUDOSSN_TBL | OCCUPATION_CD | exp_Final.OCCUPATION_CD → exp_Conversions.OCCUPATION_CD → rtr_Good_Bad_Records.OCCUPATION_CODE1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.OCCUPATION_CODE → srt_PSEUDOSSN_EFF_DT.OCCUPATION_CODE → fil_Detail_Records.OCCUPATION_CODE → exp_Determine_Record_Type.OCCUPATION_CODE → SQ_PSEUDOSSN_FILE.OCCUPATION_CODE → PSEUDOSSN_FILE.OCCUPATION_CODE | PSEUDOSSN_FILE.OCCUPATION_CODE |
| PSEUDOSSN_TBL | DUTY_STATION | exp_Final.DUTY_STATION → exp_Conversions.DUTY_STATION → rtr_Good_Bad_Records.GEO_LOCATION1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.GEO_LOCATION → srt_PSEUDOSSN_EFF_DT.GEO_LOCATION → fil_Detail_Records.GEO_LOCATION → exp_Determine_Record_Type.GEO_LOCATION → SQ_PSEUDOSSN_FILE.GEO_LOCATION → PSEUDOSSN_FILE.GEO_LOCATION | PSEUDOSSN_FILE.GEO_LOCATION |
| PSEUDOSSN_TBL | JOB_IND | exp_Final.JOB_IND → exp_Conversions.JOB_IND → rtr_Good_Bad_Records.JOB_INDICATOR1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.JOB_INDICATOR → srt_PSEUDOSSN_EFF_DT.JOB_INDICATOR → fil_Detail_Records.JOB_INDICATOR → exp_Determine_Record_Type.JOB_INDICATOR → SQ_PSEUDOSSN_FILE.JOB_INDICATOR → PSEUDOSSN_FILE.JOB_INDICATOR | PSEUDOSSN_FILE.JOB_INDICATOR |
| PSEUDOSSN_TBL | REG_TEMP_CD | exp_Final.REG_TEMP_CD → exp_Conversions.REG_TEMP_CD → rtr_Good_Bad_Records.REG_TEMP1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.REG_TEMP → srt_PSEUDOSSN_EFF_DT.REG_TEMP → fil_Detail_Records.REG_TEMP → exp_Determine_Record_Type.REG_TEMP → SQ_PSEUDOSSN_FILE.REG_TEMP → PSEUDOSSN_FILE.REG_TEMP | PSEUDOSSN_FILE.REG_TEMP |
| PSEUDOSSN_TBL | SEPERATION_DATE | exp_Final.SEPERATION_DATE → exp_Conversions.o_SEPARATION_DATE = IIF(IS_DATE(v_SEPARATION_DATE, 'MM/DD/YYYY'), TO_DATE(v_SEPARATION_DATE, 'MM/DD/YYYY')) → exp_Conversions.v_SEPARATION_DATE = SUBSTR(in_SEPARATION_DATE, 5, 2) \|\| '/' \|\| SUBSTR(in_SEPARATION_DATE, 7, 2) \|\| '/' \|\| SUBSTR(in_SEPARATION_DATE, 1, 4) -- Builds date in 'MM/DD/YYYY' format, source date format is YYYYMMDD → rtr_Good_Bad_Records.SEPARATION_DATE1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.SEPARATION_DATE → srt_PSEUDOSSN_EFF_DT.SEPARATION_DATE → fil_Detail_Records.SEPARATION_DATE → exp_Determine_Record_Type.SEPARATION_DATE → SQ_PSEUDOSSN_FILE.SEPARATION_DATE → PSEUDOSSN_FILE.SEPARATION_DATE | PSEUDOSSN_FILE.SEPARATION_DATE |
| PSEUDOSSN_TBL | PCA_CONTR_EFF_START_DATE | exp_Final.PCA_CONTR_EFF_START_DATE → exp_Conversions.o_PCA_CONTR_EFF_START_DATE = IIF(IS_DATE(v_PCA_CONTR_EFF_START_DATE, 'MM/DD/YYYY'), TO_DATE(v_PCA_CONTR_EFF_START_DATE, 'MM/DD/YYYY')) → exp_Conversions.v_PCA_CONTR_EFF_START_DATE = SUBSTR(in_PCA_CONTR_EFF_START_DATE, 5, 2) \|\| '/' \|\| SUBSTR(in_PCA_CONTR_EFF_START_DATE, 7, 2) \|\| '/' \|\| SUBSTR(in_PCA_CONTR_EFF_START_DATE, 1, 4) -- Builds date in 'MM/DD/YYYY' format, source date format is YYYYDDMM → rtr_Good_Bad_Records.PCA_CONTR_EFF_START_DATE1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.PCA_CONTR_EFF_START_DATE → srt_PSEUDOSSN_EFF_DT.PCA_CONTR_EFF_START_DATE → fil_Detail_Records.PCA_CONTR_EFF_START_DATE → exp_Determine_Record_Type.PCA_CONTR_EFF_START_DATE → SQ_PSEUDOSSN_FILE.PCA_CONTR_EFF_START_DATE → PSEUDOSSN_FILE.PCA_CONTR_EFF_START_DATE | PSEUDOSSN_FILE.PCA_CONTR_EFF_START_DATE |
| PSEUDOSSN_TBL | PCA_CONTR_EFF_END_DATE | exp_Final.PCA_CONTR_EFF_END_DATE → exp_Conversions.o_PCA_CONTR_EFF_END_DATE = IIF(IS_DATE(v_PCA_CONTR_EFF_END_DATE, 'MM/DD/YYYY'), TO_DATE(v_PCA_CONTR_EFF_END_DATE, 'MM/DD/YYYY')) → exp_Conversions.v_PCA_CONTR_EFF_END_DATE = SUBSTR(in_PCA_CONTR_EFF_END_DATE, 5, 2) \|\| '/' \|\| SUBSTR(in_PCA_CONTR_EFF_END_DATE, 7, 2) \|\| '/' \|\| SUBSTR(in_PCA_CONTR_EFF_END_DATE, 1, 4) -- Builds date in 'MM/DD/YYYY' format, source date format is YYYYDDMM → rtr_Good_Bad_Records.PCA_CONTR_EFF_END_DATE1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.PCA_CONTR_EFF_END_DATE → srt_PSEUDOSSN_EFF_DT.PCA_CONTR_EFF_END_DATE → fil_Detail_Records.PCA_CONTR_EFF_END_DATE → exp_Determine_Record_Type.PCA_CONTR_EFF_END_DATE → SQ_PSEUDOSSN_FILE.PCA_CONTR_EFF_END_DATE → PSEUDOSSN_FILE.PCA_CONTR_EFF_END_DATE | PSEUDOSSN_FILE.PCA_CONTR_EFF_END_DATE |
| PSEUDOSSN_TBL | MAX_ANNUAL_PAY | exp_Final.MAX_ANNUAL_PAY → exp_Conversions.o_MAX_ANNUAL_PAY = DECODE(TRUE, IS_NUMBER(v_MAX_ANNUAL_PAY) AND v_MAX_ANNUAL_PAY_SIGN = '+', TO_DECIMAL(v_MAX_ANNUAL_PAY, 2), IS_NUMBER(v_MAX_ANNUAL_PAY) AND v_MAX_ANNUAL_PAY_SIGN = '-', TO_DECIMAL(v_MAX_ANNUAL_PAY, 2) * -1, IS_NUMBER(v_MAX_ANNUAL_PAY), TO_DECIMAL(v_MAX_ANNUAL_PAY, 2), 0) → exp_Conversions.v_MAX_ANNUAL_PAY = SUBSTR(in_MAX_ANNUAL_PAY,1, 5) \|\| '.' \|\| SUBSTR(in_MAX_ANNUAL_PAY,6, 2) → rtr_Good_Bad_Records.MAX_ANNUAL_PAY1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.MAX_ANNUAL_PAY → srt_PSEUDOSSN_EFF_DT.MAX_ANNUAL_PAY → fil_Detail_Records.MAX_ANNUAL_PAY → exp_Determine_Record_Type.MAX_ANNUAL_PAY → SQ_PSEUDOSSN_FILE.MAX_ANNUAL_PAY → PSEUDOSSN_FILE.MAX_ANNUAL_PAY → exp_Conversions.v_MAX_ANNUAL_PAY_SIGN = SUBSTR(in_MAX_ANNUAL_PAY, 8, 1) | PSEUDOSSN_FILE.MAX_ANNUAL_PAY |
| PSEUDOSSN_TBL | PCA_BIWEEKLY_AMT | exp_Final.PCA_BIWEEKLY_AMT → exp_Conversions.o_PCA_BIWEEKLY_AMOUNT = DECODE(TRUE, IS_NUMBER(v_PCA_BIWEEKLY_AMOUNT) AND v_PCA_BIWEEKLY_AMOUNT_SIGN = '+', TO_DECIMAL(v_PCA_BIWEEKLY_AMOUNT, 2), IS_NUMBER(v_PCA_BIWEEKLY_AMOUNT) AND v_PCA_BIWEEKLY_AMOUNT_SIGN = '-', TO_DECIMAL(v_PCA_BIWEEKLY_AMOUNT, 2) * -1, IS_NUMBER(v_PCA_BIWEEKLY_AMOUNT), TO_DECIMAL(v_PCA_BIWEEKLY_AMOUNT, 2), 0) → exp_Conversions.v_PCA_BIWEEKLY_AMOUNT = SUBSTR(in_PCA_BIWEEKLY_AMOUNT,1, 5) \|\| '.' \|\| SUBSTR(in_PCA_BIWEEKLY_AMOUNT,6, 2) → rtr_Good_Bad_Records.PCA_BIWEEKLY_AMOUNT1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.PCA_BIWEEKLY_AMOUNT → srt_PSEUDOSSN_EFF_DT.PCA_BIWEEKLY_AMOUNT → fil_Detail_Records.PCA_BIWEEKLY_AMOUNT → exp_Determine_Record_Type.PCA_BIWEEKLY_AMOUNT → SQ_PSEUDOSSN_FILE.PCA_BIWEEKLY_AMOUNT → PSEUDOSSN_FILE.PCA_BIWEEKLY_AMOUNT → exp_Conversions.v_PCA_BIWEEKLY_AMOUNT_SIGN = SUBSTR(in_PCA_BIWEEKLY_AMOUNT, 8, 1) | PSEUDOSSN_FILE.PCA_BIWEEKLY_AMOUNT |
| PSEUDOSSN_TBL | PAY_PLAN_CD | exp_Final.PAY_PLAN_CD → exp_Conversions.PAY_PLAN_CD → rtr_Good_Bad_Records.PAY_PLAN_CD1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.PAY_PLAN_CD → srt_PSEUDOSSN_EFF_DT.PAY_PLAN_CD → fil_Detail_Records.PAY_PLAN_CD → exp_Determine_Record_Type.PAY_PLAN_CD → SQ_PSEUDOSSN_FILE.PAY_PLAN_CD → PSEUDOSSN_FILE.PAY_PLAN_CD | PSEUDOSSN_FILE.PAY_PLAN_CD |
| PSEUDOSSN_TBL | APPT_NTE_DTE | exp_Final.APPT_NTE_DTE → exp_Conversions.o_APP_NTE_DATE = IIF(IS_DATE(v_APP_LIMIT_DATE, 'MM/DD/YYYY'), TO_DATE(v_APP_LIMIT_DATE, 'MM/DD/YYYY')) → exp_Conversions.v_APP_LIMIT_DATE = SUBSTR(in_APP_LIMIT_DATE, 5, 2) \|\| '/' \|\| SUBSTR(in_APP_LIMIT_DATE, 7, 2) \|\| '/' \|\| SUBSTR(in_APP_LIMIT_DATE, 1, 4) -- Builds date in 'MM/DD/YYYY' format, source date format is YYYYDDMM → rtr_Good_Bad_Records.APP_LIMIT_DATE1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.APP_LIMIT_DATE → srt_PSEUDOSSN_EFF_DT.APP_LIMIT_DATE → fil_Detail_Records.APP_LIMIT_DATE → exp_Determine_Record_Type.APP_LIMIT_DATE → SQ_PSEUDOSSN_FILE.APP_LIMIT_DATE → PSEUDOSSN_FILE.APP_LIMIT_DATE | PSEUDOSSN_FILE.APP_LIMIT_DATE |
| PSEUDOSSN_TBL | SPECIAL_PROGRAM_CD | exp_Final.SPECIAL_PROGRAM_CD → exp_Conversions.SPECIAL_PROGRAM_CD → rtr_Good_Bad_Records.SPO_CD1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.SPO_CD → srt_PSEUDOSSN_EFF_DT.SPO_CD → fil_Detail_Records.SPO_CD → exp_Determine_Record_Type.SPO_CD → SQ_PSEUDOSSN_FILE.SPO_CD → PSEUDOSSN_FILE.SPO_CD | PSEUDOSSN_FILE.SPO_CD |
| PSEUDOSSN_TBL | TERM_ID | exp_Final.TERM_ID → exp_Conversions.TERM_ID → rtr_Good_Bad_Records.TERM_ID1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.TERM_ID → srt_PSEUDOSSN_EFF_DT.TERM_ID → fil_Detail_Records.TERM_ID → exp_Determine_Record_Type.TERM_ID → SQ_PSEUDOSSN_FILE.TERM_ID → PSEUDOSSN_FILE.TERM_ID | PSEUDOSSN_FILE.TERM_ID |
| PSEUDOSSN_TBL | EFFECTIVE_DATE | exp_Final.EFFECTIVE_DATE → exp_Conversions.o_EFFECTIVE_DATE = IIF(IS_DATE(v_EFFECTIVE_DATE, 'MM/DD/YYYY'), TO_DATE(v_EFFECTIVE_DATE, 'MM/DD/YYYY')) → exp_Conversions.v_EFFECTIVE_DATE = SUBSTR(in_EFFECTIVE_DATE, 5, 2) \|\| '/' \|\| SUBSTR(in_EFFECTIVE_DATE, 7, 2) \|\| '/' \|\| SUBSTR(in_EFFECTIVE_DATE, 1, 4) -- Builds date in 'MM/DD/YYYY' format, source date format is YYYYDDMM -- MS 12/13/2012 Source date format has been changed from YYYYDDMM to YYYYMMDD → rtr_Good_Bad_Records.EFFECTIVE_DATE1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.EFFECTIVE_DATE → srt_PSEUDOSSN_EFF_DT.EFFECTIVE_DATE → fil_Detail_Records.EFFECTIVE_DATE → exp_Determine_Record_Type.EFFECTIVE_DATE → SQ_PSEUDOSSN_FILE.EFFECTIVE_DATE → PSEUDOSSN_FILE.EFFECTIVE_DATE | PSEUDOSSN_FILE.EFFECTIVE_DATE |
| PSEUDOSSN_TBL | EFFECTIVE_SEQ | exp_Final.EFFECTIVE_SEQ → exp_Conversions.o_EFFECTIVE_SEQ = IIF(IS_NUMBER(in_EFFECTIVE_SEQ), TO_INTEGER(in_EFFECTIVE_SEQ), 0) → rtr_Good_Bad_Records.EFFECTIVE_SEQ1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.EFFECTIVE_SEQ → srt_PSEUDOSSN_EFF_DT.EFFECTIVE_SEQ → fil_Detail_Records.EFFECTIVE_SEQ → exp_Determine_Record_Type.EFFECTIVE_SEQ → SQ_PSEUDOSSN_FILE.EFFECTIVE_SEQ → PSEUDOSSN_FILE.EFFECTIVE_SEQ | PSEUDOSSN_FILE.EFFECTIVE_SEQ |
| PSEUDOSSN_TBL | PAY_TABL_NO | exp_Final.PAY_TABL_NO → exp_Conversions.PAY_TABL_NO → rtr_Good_Bad_Records.PAY_TABL_NO1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.PAY_TABL_NO → srt_PSEUDOSSN_EFF_DT.PAY_TABL_NO → fil_Detail_Records.PAY_TABL_NO → exp_Determine_Record_Type.PAY_TABL_NO → SQ_PSEUDOSSN_FILE.PAY_TABL_NO → PSEUDOSSN_FILE.PAY_TABL_NO | PSEUDOSSN_FILE.PAY_TABL_NO |
| PSEUDOSSN_TBL | BUSINESS_UNIT | exp_Final.BUSINESS_UNIT → exp_Conversions.BUSINESS_UNIT → rtr_Good_Bad_Records.BUSINESS_UNIT1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.BUSINESS_UNIT → srt_PSEUDOSSN_EFF_DT.BUSINESS_UNIT → fil_Detail_Records.BUSINESS_UNIT → exp_Determine_Record_Type.BUSINESS_UNIT → SQ_PSEUDOSSN_FILE.BUSINESS_UNIT → PSEUDOSSN_FILE.BUSINESS_UNIT | PSEUDOSSN_FILE.BUSINESS_UNIT |
| PSEUDOSSN_TBL | DEPTID | exp_Final.DEPTID → exp_Conversions.DEPTID → rtr_Good_Bad_Records.DEPTID1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.DEPTID → srt_PSEUDOSSN_EFF_DT.DEPTID → fil_Detail_Records.DEPTID → exp_Determine_Record_Type.DEPTID → SQ_PSEUDOSSN_FILE.DEPTID → PSEUDOSSN_FILE.DEPTID | PSEUDOSSN_FILE.DEPTID |
| PSEUDOSSN_TBL | PCA_CONTR_LEN_YEAR | exp_Final.PCA_CONTR_LEN_YEAR → exp_Conversions.o_PCA_CONTR_LEN_YEAR = IIF(IS_NUMBER(in_PCA_CONTR_YEAR), TO_INTEGER(in_PCA_CONTR_YEAR), 0) → rtr_Good_Bad_Records.PCA_CONTR_YEAR1 [router group GOOD_RECORDS WHERE ERROR_FLAG = FALSE] → exp_Determine_Errors.PCA_CONTR_YEAR → srt_PSEUDOSSN_EFF_DT.PCA_CONTR_YEAR → fil_Detail_Records.PCA_CONTR_YEAR → exp_Determine_Record_Type.PCA_CONTR_YEAR → SQ_PSEUDOSSN_FILE.PCA_CONTR_YEAR → PSEUDOSSN_FILE.PCA_CONTR_YEAR | PSEUDOSSN_FILE.PCA_CONTR_YEAR |
| PSEUDOSSN_TBL | TK_NUM | (not connected — NULL) | — |
| PSEUDOSSN_TBL | PP_NUM | exp_Final.PP_NUM → lkp_Current_Pay_Period.PP_NUM [lookup PAY_PERIOD.PP_NUM ON CURR_PP_FLAG = in_CURR_PP_FLAG] | PAY_PERIOD.PP_NUM (lookup); literal/expression: 'Y' (lookup key) |
| PSEUDOSSN_TBL | PP_END_YEAR | exp_Final.PP_END_YEAR → lkp_Current_Pay_Period.PP_END_YEAR [lookup PAY_PERIOD.PP_END_YEAR ON CURR_PP_FLAG = in_CURR_PP_FLAG] | PAY_PERIOD.PP_END_YEAR (lookup); literal/expression: 'Y' (lookup key) |

## Mapping `m_Pseudossn_Load_Pseudossn_From_SDA_Tbl`

- Sessions: `s_Pseudossn_Load_Pseudossn_From_SDA_Tbl` (#7)
- Sources: `PSEUDOSSN_FILE_TK_NUM`
- Target instances: `PSEUDOSSN_FROM_SDA_TBL`

### Transformation `SQ_PSEUDOSSN_FILE_TK_NUM` (Source Qualifier)

- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `fil_Detail_Records` (Filter)

- **Filter Condition**: `RECORD_TYPE_FLAG = 'D' AND SSN_FLAG = TRUE`

### Transformation `lkp_Current_Pay_Period` (Lookup Procedure)

- **Lookup table name**: `PAY_PERIOD`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `CURR_PP_FLAG = in_CURR_PP_FLAG`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `srt_PSEUDOSSN_EFF_DT` (Sorter)

- **Case Sensitive**: `YES`
- **Distinct**: `NO`
- **Null Treated Low**: `NO`

- Sorter `srt_PSEUDOSSN_EFF_DT` keys: PSEUDO_SSN ASCENDING, EMPLOYEE_STATUS ASCENDING, EFFECTIVE_DATE DESCENDING; distinct=NO
- Lookup `lkp_Current_Pay_Period`: table `PAY_PERIOD` (exists in export: **True**), condition `CURR_PP_FLAG = in_CURR_PP_FLAG`, multiple-match policy `Use Any Value`.

### Target instance `PSEUDOSSN_FROM_SDA_TBL` (table `PSEUDOSSN_FROM_SDA_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| PSEUDOSSN_FROM_SDA_TBL | SSN | exp_Final.SSN → exp_Conversions.SSN → exp_Determine_Errors.SSN → srt_PSEUDOSSN_EFF_DT.SSN → fil_Detail_Records.SSN → exp_Determine_Record_Type.SSN → SQ_PSEUDOSSN_FILE_TK_NUM.SSN → PSEUDOSSN_FILE_TK_NUM.SSN | PSEUDOSSN_FILE_TK_NUM.SSN |
| PSEUDOSSN_FROM_SDA_TBL | CAN_CD | exp_Final.CAN_CD → exp_Conversions.CAN_CD → exp_Determine_Errors.CAN_CD → srt_PSEUDOSSN_EFF_DT.CAN_CD → fil_Detail_Records.CAN_CD → exp_Determine_Record_Type.CAN_CD → SQ_PSEUDOSSN_FILE_TK_NUM.CAN_CD → PSEUDOSSN_FILE_TK_NUM.CAN_CD | PSEUDOSSN_FILE_TK_NUM.CAN_CD |
| PSEUDOSSN_FROM_SDA_TBL | PSEUDOSSN | exp_Final.PSEUDOSSN → exp_Conversions.PSEUDOSSN → exp_Determine_Errors.PSEUDO_SSN → srt_PSEUDOSSN_EFF_DT.PSEUDO_SSN → fil_Detail_Records.PSEUDO_SSN → exp_Determine_Record_Type.PSEUDO_SSN → SQ_PSEUDOSSN_FILE_TK_NUM.PSEUDO_SSN → PSEUDOSSN_FILE_TK_NUM.PSEUDO_SSN | PSEUDOSSN_FILE_TK_NUM.PSEUDO_SSN |
| PSEUDOSSN_FROM_SDA_TBL | EMPLID | exp_Final.EMPLID → exp_Conversions.EMPLID → exp_Determine_Errors.EIN → srt_PSEUDOSSN_EFF_DT.EIN → fil_Detail_Records.EIN → exp_Determine_Record_Type.EIN → SQ_PSEUDOSSN_FILE_TK_NUM.EIN → PSEUDOSSN_FILE_TK_NUM.EIN | PSEUDOSSN_FILE_TK_NUM.EIN |
| PSEUDOSSN_FROM_SDA_TBL | EMPL_RCD | exp_Final.EMPL_RCD → exp_Conversions.EMPL_RCD → exp_Determine_Errors.EMP_REC_NO → srt_PSEUDOSSN_EFF_DT.EMP_REC_NO → fil_Detail_Records.EMP_REC_NO → exp_Determine_Record_Type.EMP_REC_NO → SQ_PSEUDOSSN_FILE_TK_NUM.EMP_REC_NO → PSEUDOSSN_FILE_TK_NUM.EMP_REC_NO | PSEUDOSSN_FILE_TK_NUM.EMP_REC_NO |
| PSEUDOSSN_FROM_SDA_TBL | APPT_NUM | exp_Final.APPT_NUM → exp_Conversions.APPT_NUM → exp_Determine_Errors.LEGACY_APPT_NO → srt_PSEUDOSSN_EFF_DT.LEGACY_APPT_NO → fil_Detail_Records.LEGACY_APPT_NO → exp_Determine_Record_Type.LEGACY_APPT_NO → SQ_PSEUDOSSN_FILE_TK_NUM.LEGACY_APPT_NO → PSEUDOSSN_FILE_TK_NUM.LEGACY_APPT_NO | PSEUDOSSN_FILE_TK_NUM.LEGACY_APPT_NO |
| PSEUDOSSN_FROM_SDA_TBL | EMP_FIRST_NAME | exp_Final.EMP_FIRST_NAME → exp_Conversions.EMP_FIRST_NAME → exp_Determine_Errors.FIRST_NAME → srt_PSEUDOSSN_EFF_DT.FIRST_NAME → fil_Detail_Records.FIRST_NAME → exp_Determine_Record_Type.FIRST_NAME → SQ_PSEUDOSSN_FILE_TK_NUM.FIRST_NAME → PSEUDOSSN_FILE_TK_NUM.FIRST_NAME | PSEUDOSSN_FILE_TK_NUM.FIRST_NAME |
| PSEUDOSSN_FROM_SDA_TBL | EMP_MID_INIT | exp_Final.EMP_MID_INIT → exp_Conversions.EMP_MID_INIT → exp_Determine_Errors.MIDDLE_INIT → srt_PSEUDOSSN_EFF_DT.MIDDLE_INIT → fil_Detail_Records.MIDDLE_INIT → exp_Determine_Record_Type.MIDDLE_INIT → SQ_PSEUDOSSN_FILE_TK_NUM.MIDDLE_INIT → PSEUDOSSN_FILE_TK_NUM.MIDDLE_INIT | PSEUDOSSN_FILE_TK_NUM.MIDDLE_INIT |
| PSEUDOSSN_FROM_SDA_TBL | EMP_LAST_NAME | exp_Final.EMP_LAST_NAME → exp_Conversions.EMP_LAST_NAME → exp_Determine_Errors.LAST_NAME → srt_PSEUDOSSN_EFF_DT.LAST_NAME → fil_Detail_Records.LAST_NAME → exp_Determine_Record_Type.LAST_NAME → SQ_PSEUDOSSN_FILE_TK_NUM.LAST_NAME → PSEUDOSSN_FILE_TK_NUM.LAST_NAME | PSEUDOSSN_FILE_TK_NUM.LAST_NAME |
| PSEUDOSSN_FROM_SDA_TBL | SEX | exp_Final.SEX → exp_Conversions.SEX → exp_Determine_Errors.SEX → srt_PSEUDOSSN_EFF_DT.SEX → fil_Detail_Records.SEX → exp_Determine_Record_Type.SEX → SQ_PSEUDOSSN_FILE_TK_NUM.SEX → PSEUDOSSN_FILE_TK_NUM.SEX | PSEUDOSSN_FILE_TK_NUM.SEX |
| PSEUDOSSN_FROM_SDA_TBL | VETERANS_PREFERENCE_CD | exp_Final.VETERANS_PREFERENCE_CD → exp_Conversions.VETERANS_PREFERENCE_CD → exp_Determine_Errors.VET_PREF → srt_PSEUDOSSN_EFF_DT.VET_PREF → fil_Detail_Records.VET_PREF → exp_Determine_Record_Type.VET_PREF → SQ_PSEUDOSSN_FILE_TK_NUM.VET_PREF → PSEUDOSSN_FILE_TK_NUM.VET_PREF | PSEUDOSSN_FILE_TK_NUM.VET_PREF |
| PSEUDOSSN_FROM_SDA_TBL | TENURE_CD | exp_Final.TENURE_CD → exp_Conversions.TENURE_CD → exp_Determine_Errors.TENURE_CD → srt_PSEUDOSSN_EFF_DT.TENURE_CD → fil_Detail_Records.TENURE_CD → exp_Determine_Record_Type.TENURE_CD → SQ_PSEUDOSSN_FILE_TK_NUM.TENURE_CD → PSEUDOSSN_FILE_TK_NUM.TENURE_CD | PSEUDOSSN_FILE_TK_NUM.TENURE_CD |
| PSEUDOSSN_FROM_SDA_TBL | POSITION_NUM | exp_Final.POSITION_NUM → exp_Conversions.POSITION_NUM → exp_Determine_Errors.POSITION_CD → srt_PSEUDOSSN_EFF_DT.POSITION_CD → fil_Detail_Records.POSITION_CD → exp_Determine_Record_Type.POSITION_CD → SQ_PSEUDOSSN_FILE_TK_NUM.POSITION_CD → PSEUDOSSN_FILE_TK_NUM.POSITION_CD | PSEUDOSSN_FILE_TK_NUM.POSITION_CD |
| PSEUDOSSN_FROM_SDA_TBL | US_CITIZENSHIP_CD | exp_Final.US_CITIZENSHIP_CD → exp_Conversions.US_CITIZENSHIP_CD → exp_Determine_Errors.CITIZENSHIP_STATUS → srt_PSEUDOSSN_EFF_DT.CITIZENSHIP_STATUS → fil_Detail_Records.CITIZENSHIP_STATUS → exp_Determine_Record_Type.CITIZENSHIP_STATUS → SQ_PSEUDOSSN_FILE_TK_NUM.CITIZENSHIP_STATUS → PSEUDOSSN_FILE_TK_NUM.CITIZENSHIP_STATUS | PSEUDOSSN_FILE_TK_NUM.CITIZENSHIP_STATUS |
| PSEUDOSSN_FROM_SDA_TBL | APPT_TYPE_CD | exp_Final.APPT_TYPE_CD → exp_Conversions.APPT_TYPE_CD → exp_Determine_Errors.APPT_TYPE_CD → srt_PSEUDOSSN_EFF_DT.APPT_TYPE_CD → fil_Detail_Records.APPT_TYPE_CD → exp_Determine_Record_Type.APPT_TYPE_CD → SQ_PSEUDOSSN_FILE_TK_NUM.APPT_TYPE_CD → PSEUDOSSN_FILE_TK_NUM.APPT_TYPE_CD | PSEUDOSSN_FILE_TK_NUM.APPT_TYPE_CD |
| PSEUDOSSN_FROM_SDA_TBL | HIRE_DATE | exp_Final.HIRE_DATE → exp_Conversions.o_HIRE_DATE = IIF(IS_DATE(v_HIRE_DATE, 'MM/DD/YYYY'), TO_DATE(v_HIRE_DATE, 'MM/DD/YYYY')) → exp_Conversions.v_HIRE_DATE = SUBSTR(in_HIRE_DATE, 1, 2) \|\| '/' \|\| SUBSTR(in_HIRE_DATE, 3, 2) \|\| '/' \|\| SUBSTR(in_HIRE_DATE, 5, 4) -- Builds date in 'MM/DD/YYYY' format, source date format is MMDDYYYY → exp_Determine_Errors.HIRE_DATE → srt_PSEUDOSSN_EFF_DT.HIRE_DATE → fil_Detail_Records.HIRE_DATE → exp_Determine_Record_Type.HIRE_DATE → SQ_PSEUDOSSN_FILE_TK_NUM.HIRE_DATE → PSEUDOSSN_FILE_TK_NUM.HIRE_DATE | PSEUDOSSN_FILE_TK_NUM.HIRE_DATE |
| PSEUDOSSN_FROM_SDA_TBL | HANDICAP_CD | exp_Final.HANDICAP_CD → exp_Conversions.HANDICAP_CD → exp_Determine_Errors.HANDICAP_CODE → srt_PSEUDOSSN_EFF_DT.HANDICAP_CODE → fil_Detail_Records.HANDICAP_CODE → exp_Determine_Record_Type.HANDICAP_CODE → SQ_PSEUDOSSN_FILE_TK_NUM.HANDICAP_CODE → PSEUDOSSN_FILE_TK_NUM.HANDICAP_CODE | PSEUDOSSN_FILE_TK_NUM.HANDICAP_CODE |
| PSEUDOSSN_FROM_SDA_TBL | UNF_ALLOW_CD | exp_Final.UNF_ALLOW_CD → exp_Conversions.UNF_ALLOW_CD → exp_Determine_Errors.UNIF_ALLOW_CODE → srt_PSEUDOSSN_EFF_DT.UNIF_ALLOW_CODE → fil_Detail_Records.UNIF_ALLOW_CODE → exp_Determine_Record_Type.UNIF_ALLOW_CODE → SQ_PSEUDOSSN_FILE_TK_NUM.UNIF_ALLOW_CODE → PSEUDOSSN_FILE_TK_NUM.UNIF_ALLOW_CODE | PSEUDOSSN_FILE_TK_NUM.UNIF_ALLOW_CODE |
| PSEUDOSSN_FROM_SDA_TBL | UNIF_ALLOW_DATE | exp_Final.UNIF_ALLOW_DATE → exp_Conversions.o_UNIF_ALLOW_DATE = IIF(IS_DATE(v_UNIF_ALLOW_DATE, 'MM/DD/YYYY'), TO_DATE(v_UNIF_ALLOW_DATE, 'MM/DD/YYYY')) → exp_Conversions.v_UNIF_ALLOW_DATE = SUBSTR(in_UNIF_ALLOW_DATE, 5, 2) \|\| '/' \|\| SUBSTR(in_UNIF_ALLOW_DATE, 7, 2) \|\| '/' \|\| SUBSTR(in_UNIF_ALLOW_DATE, 1, 4) -- Builds date in 'MM/DD/YYYY' format, source date format is YYYYMMDD → exp_Determine_Errors.UNIF_ALLOW_DATE → srt_PSEUDOSSN_EFF_DT.UNIF_ALLOW_DATE → fil_Detail_Records.UNIF_ALLOW_DATE → exp_Determine_Record_Type.UNIF_ALLOW_DATE → SQ_PSEUDOSSN_FILE_TK_NUM.UNIF_ALLOW_DATE → PSEUDOSSN_FILE_TK_NUM.UNIF_ALLOW_DATE | PSEUDOSSN_FILE_TK_NUM.UNIF_ALLOW_DATE |
| PSEUDOSSN_FROM_SDA_TBL | UNIF_ALLOW_AMT | exp_Final.UNIF_ALLOW_AMT → exp_Conversions.o_UNIF_ALLOW_AMT = DECODE(TRUE, IS_NUMBER(v_UNIF_ALLOW_AMT) AND v_UNIF_ALLOW_AMT_SIGN = '+', TO_DECIMAL(v_UNIF_ALLOW_AMT, 2), IS_NUMBER(v_UNIF_ALLOW_AMT) AND v_UNIF_ALLOW_AMT_SIGN = '-', TO_DECIMAL(v_UNIF_ALLOW_AMT, 2) * -1, IS_NUMBER(v_UNIF_ALLOW_AMT), TO_DECIMAL(v_UNIF_ALLOW_AMT, 2), 0) → exp_Conversions.v_UNIF_ALLOW_AMT = SUBSTR(in_UNIF_ALLOW_AMT,1, 3) \|\| '.' \|\| SUBSTR(in_UNIF_ALLOW_AMT,4, 2) → exp_Determine_Errors.UNIF_ALLOW_AMT → srt_PSEUDOSSN_EFF_DT.UNIF_ALLOW_AMT → fil_Detail_Records.UNIF_ALLOW_AMT → exp_Determine_Record_Type.UNIF_ALLOW_AMT → SQ_PSEUDOSSN_FILE_TK_NUM.UNIF_ALLOW_AMT → PSEUDOSSN_FILE_TK_NUM.UNIF_ALLOW_AMT → exp_Conversions.v_UNIF_ALLOW_AMT_SIGN = SUBSTR(in_UNIF_ALLOW_AMT, 6, 1) | PSEUDOSSN_FILE_TK_NUM.UNIF_ALLOW_AMT |
| PSEUDOSSN_FROM_SDA_TBL | RSSSDP | exp_Final.RSSSDP → exp_Conversions.RSSSDP → exp_Determine_Errors.RSSSDP → srt_PSEUDOSSN_EFF_DT.RSSSDP → fil_Detail_Records.RSSSDP → exp_Determine_Record_Type.RSSSDP → SQ_PSEUDOSSN_FILE_TK_NUM.RSSSDP → PSEUDOSSN_FILE_TK_NUM.RSSSDP | PSEUDOSSN_FILE_TK_NUM.RSSSDP |
| PSEUDOSSN_FROM_SDA_TBL | CEIL_REPORTING_CD | exp_Final.CEIL_REPORTING_CD → exp_Conversions.CEIL_REPORTING_CODE → exp_Determine_Errors.CEILING_CODE → srt_PSEUDOSSN_EFF_DT.CEILING_CODE → fil_Detail_Records.CEILING_CODE → exp_Determine_Record_Type.CEILING_CODE → SQ_PSEUDOSSN_FILE_TK_NUM.CEILING_CODE → PSEUDOSSN_FILE_TK_NUM.CEILING_CODE | PSEUDOSSN_FILE_TK_NUM.CEILING_CODE |
| PSEUDOSSN_FROM_SDA_TBL | FUNCTNL_CLASSFCTN_CD | exp_Final.FUNCTNL_CLASSFCTN_CD → exp_Conversions.FUNCTNL_CLASSFCTN_CODE → exp_Determine_Errors.FUNCTION_CODE → srt_PSEUDOSSN_EFF_DT.FUNCTION_CODE → fil_Detail_Records.FUNCTION_CODE → exp_Determine_Record_Type.FUNCTION_CODE → SQ_PSEUDOSSN_FILE_TK_NUM.FUNCTION_CODE → PSEUDOSSN_FILE_TK_NUM.FUNCTION_CODE | PSEUDOSSN_FILE_TK_NUM.FUNCTION_CODE |
| PSEUDOSSN_FROM_SDA_TBL | EMP_STATUS | exp_Final.EMP_STATUS → exp_Conversions.EMP_STATUS → exp_Determine_Errors.EMPLOYEE_STATUS → srt_PSEUDOSSN_EFF_DT.EMPLOYEE_STATUS → fil_Detail_Records.EMPLOYEE_STATUS → exp_Determine_Record_Type.EMPLOYEE_STATUS → SQ_PSEUDOSSN_FILE_TK_NUM.EMPLOYEE_STATUS → PSEUDOSSN_FILE_TK_NUM.EMPLOYEE_STATUS | PSEUDOSSN_FILE_TK_NUM.EMPLOYEE_STATUS |
| PSEUDOSSN_FROM_SDA_TBL | MANAGER_STATUS | exp_Final.MANAGER_STATUS → exp_Conversions.MANAGER_STATUS → exp_Determine_Errors.MANAGER_STATUS → srt_PSEUDOSSN_EFF_DT.MANAGER_STATUS → fil_Detail_Records.MANAGER_STATUS → exp_Determine_Record_Type.MANAGER_STATUS → SQ_PSEUDOSSN_FILE_TK_NUM.MANAGER_STATUS → PSEUDOSSN_FILE_TK_NUM.MANAGER_STATUS | PSEUDOSSN_FILE_TK_NUM.MANAGER_STATUS |
| PSEUDOSSN_FROM_SDA_TBL | POSITION_SENSITIVITY_CD | exp_Final.POSITION_SENSITIVITY_CD → exp_Conversions.POSITION_SENSITIVITY_CD → exp_Determine_Errors.POSITION_SENS_CODE → srt_PSEUDOSSN_EFF_DT.POSITION_SENS_CODE → fil_Detail_Records.POSITION_SENS_CODE → exp_Determine_Record_Type.POSITION_SENS_CODE → SQ_PSEUDOSSN_FILE_TK_NUM.POSITION_SENS_CODE → PSEUDOSSN_FILE_TK_NUM.POSITION_SENS_CODE | PSEUDOSSN_FILE_TK_NUM.POSITION_SENS_CODE |
| PSEUDOSSN_FROM_SDA_TBL | CAREER_START_DATE | exp_Final.CAREER_START_DATE → exp_Conversions.o_CAREER_START_DATE = IIF(IS_DATE(v_CAREER_START_DATE, 'MM/DD/YYYY'), TO_DATE(v_CAREER_START_DATE, 'MM/DD/YYYY')) → exp_Conversions.v_CAREER_START_DATE = SUBSTR(in_CAREER_START_DATE, 1, 2) \|\| '/' \|\| SUBSTR(in_CAREER_START_DATE, 3, 2) \|\| '/' \|\| SUBSTR(in_CAREER_START_DATE, 5, 4) -- Builds date in 'MM/DD/YYYY' format, source date format is MMDDYYYY → exp_Determine_Errors.CAREER_START_DATE → srt_PSEUDOSSN_EFF_DT.CAREER_START_DATE → fil_Detail_Records.CAREER_START_DATE → exp_Determine_Record_Type.CAREER_START_DATE → SQ_PSEUDOSSN_FILE_TK_NUM.CAREER_START_DATE → PSEUDOSSN_FILE_TK_NUM.CAREER_START_DATE | PSEUDOSSN_FILE_TK_NUM.CAREER_START_DATE |
| PSEUDOSSN_FROM_SDA_TBL | CAREER_CONV_DATE | exp_Final.CAREER_CONV_DATE → exp_Conversions.o_CAREER_CONV_DATE = IIF(IS_DATE(v_CAREER_CONV_DATE, 'MM/DD/YYYY'), TO_DATE(v_CAREER_CONV_DATE, 'MM/DD/YYYY')) → exp_Conversions.v_CAREER_CONV_DATE = SUBSTR(in_CAREER_CONV_DATE, 1, 2) \|\| '/' \|\| SUBSTR(in_CAREER_CONV_DATE, 3, 2) \|\| '/' \|\| SUBSTR(in_CAREER_CONV_DATE, 5, 4) -- Builds date in 'MM/DD/YYYY' format, source date format is MMDDYYYY → exp_Determine_Errors.CAREER_CONV_DATE → srt_PSEUDOSSN_EFF_DT.CAREER_CONV_DATE → fil_Detail_Records.CAREER_CONV_DATE → exp_Determine_Record_Type.CAREER_CONV_DATE → SQ_PSEUDOSSN_FILE_TK_NUM.CAREER_CONV_DATE → PSEUDOSSN_FILE_TK_NUM.CAREER_CONV_DATE | PSEUDOSSN_FILE_TK_NUM.CAREER_CONV_DATE |
| PSEUDOSSN_FROM_SDA_TBL | PROBATION_DATE | exp_Final.PROBATION_DATE → exp_Conversions.o_PROBATION_DATE = IIF(IS_DATE(v_PROBATION_DATE, 'MM/DD/YYYY'), TO_DATE(v_PROBATION_DATE, 'MM/DD/YYYY')) → exp_Conversions.v_PROBATION_DATE = SUBSTR(in_PROBATION_DATE, 1, 2) \|\| '/' \|\| SUBSTR(in_PROBATION_DATE, 3, 2) \|\| '/' \|\| SUBSTR(in_PROBATION_DATE, 5, 4) -- Builds date in 'MM/DD/YYYY' format, source date format is MMDDYYYY → exp_Determine_Errors.PROBATION_DATE → srt_PSEUDOSSN_EFF_DT.PROBATION_DATE → fil_Detail_Records.PROBATION_DATE → exp_Determine_Record_Type.PROBATION_DATE → SQ_PSEUDOSSN_FILE_TK_NUM.PROBATION_DATE → PSEUDOSSN_FILE_TK_NUM.PROBATION_DATE | PSEUDOSSN_FILE_TK_NUM.PROBATION_DATE |
| PSEUDOSSN_FROM_SDA_TBL | ABNORMAL_RATE_CD | exp_Final.ABNORMAL_RATE_CD → exp_Conversions.ABNORMAL_RATE_CD → exp_Determine_Errors.ABNORMAL_RATE_CODE → srt_PSEUDOSSN_EFF_DT.ABNORMAL_RATE_CODE → fil_Detail_Records.ABNORMAL_RATE_CODE → exp_Determine_Record_Type.ABNORMAL_RATE_CODE → SQ_PSEUDOSSN_FILE_TK_NUM.ABNORMAL_RATE_CODE → PSEUDOSSN_FILE_TK_NUM.ABNORMAL_RATE_CODE | PSEUDOSSN_FILE_TK_NUM.ABNORMAL_RATE_CODE |
| PSEUDOSSN_FROM_SDA_TBL | APPT_LIMIT_HRS | exp_Final.APPT_LIMIT_HRS → exp_Conversions.o_APPT_LIMIT_HRS = DECODE(TRUE, IS_NUMBER(v_APPT_LIMIT_HRS) AND v_APPT_LIMIT_HRS = '+', TO_DECIMAL(v_APPT_LIMIT_HRS, 2), IS_NUMBER(v_APPT_LIMIT_HRS) AND v_APPT_LIMIT_HRS_SIGN = '-', TO_DECIMAL(v_APPT_LIMIT_HRS, 2) * -1, IS_NUMBER(v_APPT_LIMIT_HRS), TO_DECIMAL(v_APPT_LIMIT_HRS, 2), 0) → exp_Conversions.v_APPT_LIMIT_HRS = SUBSTR(in_APPT_LIMIT_HRS,1, 4) \|\| '.' \|\| SUBSTR(in_APPT_LIMIT_HRS,5, 2) → exp_Determine_Errors.APPT_LIMIT_HRS → srt_PSEUDOSSN_EFF_DT.APPT_LIMIT_HRS → fil_Detail_Records.APPT_LIMIT_HRS → exp_Determine_Record_Type.APPT_LIMIT_HRS → SQ_PSEUDOSSN_FILE_TK_NUM.APPT_LIMIT_HRS → PSEUDOSSN_FILE_TK_NUM.APPT_LIMIT_HRS → exp_Conversions.v_APPT_LIMIT_HRS_SIGN = SUBSTR(in_APPT_LIMIT_HRS, 7, 1) | PSEUDOSSN_FILE_TK_NUM.APPT_LIMIT_HRS |
| PSEUDOSSN_FROM_SDA_TBL | APPT_LIMIT_PAY | exp_Final.APPT_LIMIT_PAY → exp_Conversions.o_APPT_LIMIT_PAY = DECODE(TRUE, IS_NUMBER(v_APPT_LIMIT_PAY) AND v_APPT_LIMIT_PAY_SIGN = '+', TO_DECIMAL(v_APPT_LIMIT_PAY, 2), IS_NUMBER(v_APPT_LIMIT_PAY) AND v_APPT_LIMIT_PAY_SIGN = '-', TO_DECIMAL(v_APPT_LIMIT_PAY, 2) * -1, IS_NUMBER(v_APPT_LIMIT_PAY), TO_DECIMAL(v_APPT_LIMIT_PAY, 2), 0) → exp_Conversions.v_APPT_LIMIT_PAY = SUBSTR(in_APPT_LIMIT_PAY,1, 5) \|\| '.' \|\| SUBSTR(in_APPT_LIMIT_PAY,6, 2) → exp_Determine_Errors.APPT_LIMIT_PAY → srt_PSEUDOSSN_EFF_DT.APPT_LIMIT_PAY → fil_Detail_Records.APPT_LIMIT_PAY → exp_Determine_Record_Type.APPT_LIMIT_PAY → SQ_PSEUDOSSN_FILE_TK_NUM.APPT_LIMIT_PAY → PSEUDOSSN_FILE_TK_NUM.APPT_LIMIT_PAY → exp_Conversions.v_APPT_LIMIT_PAY_SIGN = SUBSTR(in_APPT_LIMIT_PAY, 8, 1) | PSEUDOSSN_FILE_TK_NUM.APPT_LIMIT_PAY |
| PSEUDOSSN_FROM_SDA_TBL | LAST_PAY_CHANGE | exp_Final.LAST_PAY_CHANGE → exp_Conversions.o_LAST_PAY_CHANGE = IIF(IS_DATE(v_LAST_PAY_CHANGE, 'MM/DD/YYYY'), TO_DATE(v_LAST_PAY_CHANGE, 'MM/DD/YYYY')) → exp_Conversions.v_LAST_PAY_CHANGE = SUBSTR(in_LAST_PAY_CHANGE, 1, 2) \|\| '/' \|\| SUBSTR(in_LAST_PAY_CHANGE, 3, 2) \|\| '/' \|\| SUBSTR(in_LAST_PAY_CHANGE, 5, 4) -- Builds date in 'MM/DD/YYYY' format, source date format is MMDDYYYY → exp_Determine_Errors.LAST_PAY_CHANGE → srt_PSEUDOSSN_EFF_DT.LAST_PAY_CHANGE → fil_Detail_Records.LAST_PAY_CHANGE → exp_Determine_Record_Type.LAST_PAY_CHANGE → SQ_PSEUDOSSN_FILE_TK_NUM.LAST_PAY_CHANGE → PSEUDOSSN_FILE_TK_NUM.LAST_PAY_CHANGE | PSEUDOSSN_FILE_TK_NUM.LAST_PAY_CHANGE |
| PSEUDOSSN_FROM_SDA_TBL | CHARITY_AREA_CD | exp_Final.CHARITY_AREA_CD → exp_Conversions.CHARITY_AREA_CD → exp_Determine_Errors.CHARITY_AREA_CODE → srt_PSEUDOSSN_EFF_DT.CHARITY_AREA_CODE → fil_Detail_Records.CHARITY_AREA_CODE → exp_Determine_Record_Type.CHARITY_AREA_CODE → SQ_PSEUDOSSN_FILE_TK_NUM.CHARITY_AREA_CODE → PSEUDOSSN_FILE_TK_NUM.CHARITY_AREA_CODE | PSEUDOSSN_FILE_TK_NUM.CHARITY_AREA_CODE |
| PSEUDOSSN_FROM_SDA_TBL | CHARITY_EFF_DATE | exp_Final.CHARITY_EFF_DATE → exp_Conversions.o_CHARITY_EFF_DATE = IIF(IS_DATE(v_CHARITY_EFF_DATE, 'MM/DD/YYYY'), TO_DATE(v_CHARITY_EFF_DATE, 'MM/DD/YYYY')) → exp_Conversions.v_CHARITY_EFF_DATE = SUBSTR(in_CHARITY_EFF_DATE, 5, 2) \|\| '/' \|\| SUBSTR(in_CHARITY_EFF_DATE, 7, 2) \|\| '/' \|\| SUBSTR(in_CHARITY_EFF_DATE, 1, 4) -- Builds date in 'MM/DD/YYYY' format, source date format is YYYYDDMM → exp_Determine_Errors.CHARITY_EFF_DATE → srt_PSEUDOSSN_EFF_DT.CHARITY_EFF_DATE → fil_Detail_Records.CHARITY_EFF_DATE → exp_Determine_Record_Type.CHARITY_EFF_DATE → SQ_PSEUDOSSN_FILE_TK_NUM.CHARITY_EFF_DATE → PSEUDOSSN_FILE_TK_NUM.CHARITY_EFF_DATE | PSEUDOSSN_FILE_TK_NUM.CHARITY_EFF_DATE |
| PSEUDOSSN_FROM_SDA_TBL | CHARITY_DED_AMT | exp_Final.CHARITY_DED_AMT → exp_Conversions.o_CHARITY_DED_AMT = DECODE(TRUE, IS_NUMBER(v_CHARITY_DED_AMT) AND v_CHARITY_DED_AMT_SIGN = '+', TO_DECIMAL(v_CHARITY_DED_AMT, 2), IS_NUMBER(v_CHARITY_DED_AMT) AND v_CHARITY_DED_AMT_SIGN = '-', TO_DECIMAL(v_CHARITY_DED_AMT, 2) * -1, IS_NUMBER(v_CHARITY_DED_AMT), TO_DECIMAL(v_CHARITY_DED_AMT, 2), 0) → exp_Conversions.v_CHARITY_DED_AMT = SUBSTR(in_CHARITY_DED_AMT,1, 3) \|\| '.' \|\| SUBSTR(in_CHARITY_DED_AMT,4, 2) → exp_Determine_Errors.CHARITY_DED_AMT → srt_PSEUDOSSN_EFF_DT.CHARITY_DED_AMT → fil_Detail_Records.CHARITY_DED_AMT → exp_Determine_Record_Type.CHARITY_DED_AMT → SQ_PSEUDOSSN_FILE_TK_NUM.CHARITY_DED_AMT → PSEUDOSSN_FILE_TK_NUM.CHARITY_DED_AMT → exp_Conversions.v_CHARITY_DED_AMT_SIGN = SUBSTR(in_CHARITY_DED_AMT, 6, 1) | PSEUDOSSN_FILE_TK_NUM.CHARITY_DED_AMT |
| PSEUDOSSN_FROM_SDA_TBL | LAST_NOA_CD | exp_Final.LAST_NOA_CD → exp_Conversions.LAST_NOA_CD → exp_Determine_Errors.LAST_NOA → srt_PSEUDOSSN_EFF_DT.LAST_NOA → fil_Detail_Records.LAST_NOA → exp_Determine_Record_Type.LAST_NOA → SQ_PSEUDOSSN_FILE_TK_NUM.LAST_NOA → PSEUDOSSN_FILE_TK_NUM.LAST_NOA | PSEUDOSSN_FILE_TK_NUM.LAST_NOA |
| PSEUDOSSN_FROM_SDA_TBL | QUARTERS_DED_AMT | exp_Final.QUARTERS_DED_AMT → exp_Conversions.o_QUARTERS_DED_AMT = DECODE(TRUE, IS_NUMBER(v_QUARTERS_DED_AMT) AND v_QUARTERS_DED_AMT_SIGN = '+', TO_DECIMAL(v_QUARTERS_DED_AMT, 2), IS_NUMBER(v_QUARTERS_DED_AMT) AND v_QUARTERS_DED_AMT_SIGN = '-', TO_DECIMAL(v_QUARTERS_DED_AMT, 2) * -1, IS_NUMBER(v_QUARTERS_DED_AMT), TO_DECIMAL(v_QUARTERS_DED_AMT, 2), 0) → exp_Conversions.v_QUARTERS_DED_AMT = SUBSTR(in_QUARTERS_DEDUCTION,1, 5) \|\| '.' \|\| SUBSTR(in_QUARTERS_DEDUCTION,6, 2) → exp_Determine_Errors.QUARTERS_DEDUCTION → srt_PSEUDOSSN_EFF_DT.QUARTERS_DEDUCTION → fil_Detail_Records.QUARTERS_DEDUCTION → exp_Determine_Record_Type.QUARTERS_DEDUCTION → SQ_PSEUDOSSN_FILE_TK_NUM.QUARTERS_DEDUCTION → PSEUDOSSN_FILE_TK_NUM.QUARTERS_DEDUCTION → exp_Conversions.v_QUARTERS_DED_AMT_SIGN = SUBSTR(in_QUARTERS_DEDUCTION, 8, 1) | PSEUDOSSN_FILE_TK_NUM.QUARTERS_DEDUCTION |
| PSEUDOSSN_FROM_SDA_TBL | SUBSIST_DED_AMT | exp_Final.SUBSIST_DED_AMT → exp_Conversions.o_SUBSIST_DED_AMT = DECODE(TRUE, IS_NUMBER(v_SUBSIST_DEDUCTION_AMT) AND v_SUBSIST_DEDUCTION_AMT_SIGN = '+', TO_DECIMAL(v_QUARTERS_DED_AMT, 2), IS_NUMBER(v_SUBSIST_DEDUCTION_AMT) AND v_SUBSIST_DEDUCTION_AMT_SIGN = '-', TO_DECIMAL(v_SUBSIST_DEDUCTION_AMT, 2) * -1, IS_NUMBER(v_SUBSIST_DEDUCTION_AMT), TO_DECIMAL(v_QUARTERS_DED_AMT, 2), 0) → exp_Conversions.v_SUBSIST_DEDUCTION_AMT = SUBSTR(in_SUBSIST_DEDUCTION,1, 5) \|\| '.' \|\| SUBSTR(in_SUBSIST_DEDUCTION,6, 2) → exp_Determine_Errors.SUBSIST_DEDUCTION → srt_PSEUDOSSN_EFF_DT.SUBSIST_DEDUCTION → fil_Detail_Records.SUBSIST_DEDUCTION → exp_Determine_Record_Type.SUBSIST_DEDUCTION → SQ_PSEUDOSSN_FILE_TK_NUM.SUBSIST_DEDUCTION → PSEUDOSSN_FILE_TK_NUM.SUBSIST_DEDUCTION → exp_Conversions.v_SUBSIST_DEDUCTION_AMT_SIGN = SUBSTR(in_SUBSIST_DEDUCTION, 8, 1) → exp_Conversions.v_QUARTERS_DED_AMT = SUBSTR(in_QUARTERS_DEDUCTION,1, 5) \|\| '.' \|\| SUBSTR(in_QUARTERS_DEDUCTION,6, 2) → exp_Determine_Errors.QUARTERS_DEDUCTION → srt_PSEUDOSSN_EFF_DT.QUARTERS_DEDUCTION → fil_Detail_Records.QUARTERS_DEDUCTION → exp_Determine_Record_Type.QUARTERS_DEDUCTION → SQ_PSEUDOSSN_FILE_TK_NUM.QUARTERS_DEDUCTION → PSEUDOSSN_FILE_TK_NUM.QUARTERS_DEDUCTION | PSEUDOSSN_FILE_TK_NUM.QUARTERS_DEDUCTION; PSEUDOSSN_FILE_TK_NUM.SUBSIST_DEDUCTION |
| PSEUDOSSN_FROM_SDA_TBL | PAY_BASIS_CD | exp_Final.PAY_BASIS_CD → exp_Conversions.PAY_BASIS_CD → exp_Determine_Errors.PAY_BASIS → srt_PSEUDOSSN_EFF_DT.PAY_BASIS → fil_Detail_Records.PAY_BASIS → exp_Determine_Record_Type.PAY_BASIS → SQ_PSEUDOSSN_FILE_TK_NUM.PAY_BASIS → PSEUDOSSN_FILE_TK_NUM.PAY_BASIS | PSEUDOSSN_FILE_TK_NUM.PAY_BASIS |
| PSEUDOSSN_FROM_SDA_TBL | WORK_SCHEDULE_CD | exp_Final.WORK_SCHEDULE_CD → exp_Conversions.WORK_SCHEDULE_CD → exp_Determine_Errors.WORK_SCHEDULE → srt_PSEUDOSSN_EFF_DT.WORK_SCHEDULE → fil_Detail_Records.WORK_SCHEDULE → exp_Determine_Record_Type.WORK_SCHEDULE → SQ_PSEUDOSSN_FILE_TK_NUM.WORK_SCHEDULE → PSEUDOSSN_FILE_TK_NUM.WORK_SCHEDULE | PSEUDOSSN_FILE_TK_NUM.WORK_SCHEDULE |
| PSEUDOSSN_FROM_SDA_TBL | OCCUPATION_CD | exp_Final.OCCUPATION_CD → exp_Conversions.OCCUPATION_CD → exp_Determine_Errors.OCCUPATION_CODE → srt_PSEUDOSSN_EFF_DT.OCCUPATION_CODE → fil_Detail_Records.OCCUPATION_CODE → exp_Determine_Record_Type.OCCUPATION_CODE → SQ_PSEUDOSSN_FILE_TK_NUM.OCCUPATION_CODE → PSEUDOSSN_FILE_TK_NUM.OCCUPATION_CODE | PSEUDOSSN_FILE_TK_NUM.OCCUPATION_CODE |
| PSEUDOSSN_FROM_SDA_TBL | DUTY_STATION | exp_Final.DUTY_STATION → exp_Conversions.DUTY_STATION → exp_Determine_Errors.GEO_LOCATION → srt_PSEUDOSSN_EFF_DT.GEO_LOCATION → fil_Detail_Records.GEO_LOCATION → exp_Determine_Record_Type.GEO_LOCATION → SQ_PSEUDOSSN_FILE_TK_NUM.GEO_LOCATION → PSEUDOSSN_FILE_TK_NUM.GEO_LOCATION | PSEUDOSSN_FILE_TK_NUM.GEO_LOCATION |
| PSEUDOSSN_FROM_SDA_TBL | JOB_IND | exp_Final.JOB_IND → exp_Conversions.JOB_IND → exp_Determine_Errors.JOB_INDICATOR → srt_PSEUDOSSN_EFF_DT.JOB_INDICATOR → fil_Detail_Records.JOB_INDICATOR → exp_Determine_Record_Type.JOB_INDICATOR → SQ_PSEUDOSSN_FILE_TK_NUM.JOB_INDICATOR → PSEUDOSSN_FILE_TK_NUM.JOB_INDICATOR | PSEUDOSSN_FILE_TK_NUM.JOB_INDICATOR |
| PSEUDOSSN_FROM_SDA_TBL | REG_TEMP_CD | exp_Final.REG_TEMP_CD → exp_Conversions.REG_TEMP_CD → exp_Determine_Errors.REG_TEMP → srt_PSEUDOSSN_EFF_DT.REG_TEMP → fil_Detail_Records.REG_TEMP → exp_Determine_Record_Type.REG_TEMP → SQ_PSEUDOSSN_FILE_TK_NUM.REG_TEMP → PSEUDOSSN_FILE_TK_NUM.REG_TEMP | PSEUDOSSN_FILE_TK_NUM.REG_TEMP |
| PSEUDOSSN_FROM_SDA_TBL | SEPERATION_DATE | exp_Final.SEPERATION_DATE → exp_Conversions.o_SEPARATION_DATE = IIF(IS_DATE(v_SEPARATION_DATE, 'MM/DD/YYYY'), TO_DATE(v_SEPARATION_DATE, 'MM/DD/YYYY')) → exp_Conversions.v_SEPARATION_DATE = SUBSTR(in_SEPARATION_DATE, 5, 2) \|\| '/' \|\| SUBSTR(in_SEPARATION_DATE, 7, 2) \|\| '/' \|\| SUBSTR(in_SEPARATION_DATE, 1, 4) -- Builds date in 'MM/DD/YYYY' format, source date format is YYYYMMDD → exp_Determine_Errors.SEPARATION_DATE → srt_PSEUDOSSN_EFF_DT.SEPARATION_DATE → fil_Detail_Records.SEPARATION_DATE → exp_Determine_Record_Type.SEPARATION_DATE → SQ_PSEUDOSSN_FILE_TK_NUM.SEPARATION_DATE → PSEUDOSSN_FILE_TK_NUM.SEPARATION_DATE | PSEUDOSSN_FILE_TK_NUM.SEPARATION_DATE |
| PSEUDOSSN_FROM_SDA_TBL | PCA_CONTR_EFF_START_DATE | exp_Final.PCA_CONTR_EFF_START_DATE → exp_Conversions.o_PCA_CONTR_EFF_START_DATE = IIF(IS_DATE(v_PCA_CONTR_EFF_START_DATE, 'MM/DD/YYYY'), TO_DATE(v_PCA_CONTR_EFF_START_DATE, 'MM/DD/YYYY')) → exp_Conversions.v_PCA_CONTR_EFF_START_DATE = SUBSTR(in_PCA_CONTR_EFF_START_DATE, 5, 2) \|\| '/' \|\| SUBSTR(in_PCA_CONTR_EFF_START_DATE, 7, 2) \|\| '/' \|\| SUBSTR(in_PCA_CONTR_EFF_START_DATE, 1, 4) -- Builds date in 'MM/DD/YYYY' format, source date format is YYYYDDMM → exp_Determine_Errors.PCA_CONTR_EFF_START_DATE → srt_PSEUDOSSN_EFF_DT.PCA_CONTR_EFF_START_DATE → fil_Detail_Records.PCA_CONTR_EFF_START_DATE → exp_Determine_Record_Type.PCA_CONTR_EFF_START_DATE → SQ_PSEUDOSSN_FILE_TK_NUM.PCA_CONTR_EFF_START_DATE → PSEUDOSSN_FILE_TK_NUM.PCA_CONTR_EFF_START_DATE | PSEUDOSSN_FILE_TK_NUM.PCA_CONTR_EFF_START_DATE |
| PSEUDOSSN_FROM_SDA_TBL | PCA_CONTR_EFF_END_DATE | exp_Final.PCA_CONTR_EFF_END_DATE → exp_Conversions.o_PCA_CONTR_EFF_END_DATE = IIF(IS_DATE(v_PCA_CONTR_EFF_END_DATE, 'MM/DD/YYYY'), TO_DATE(v_PCA_CONTR_EFF_END_DATE, 'MM/DD/YYYY')) → exp_Conversions.v_PCA_CONTR_EFF_END_DATE = SUBSTR(in_PCA_CONTR_EFF_END_DATE, 5, 2) \|\| '/' \|\| SUBSTR(in_PCA_CONTR_EFF_END_DATE, 7, 2) \|\| '/' \|\| SUBSTR(in_PCA_CONTR_EFF_END_DATE, 1, 4) -- Builds date in 'MM/DD/YYYY' format, source date format is YYYYDDMM → exp_Determine_Errors.PCA_CONTR_EFF_END_DATE → srt_PSEUDOSSN_EFF_DT.PCA_CONTR_EFF_END_DATE → fil_Detail_Records.PCA_CONTR_EFF_END_DATE → exp_Determine_Record_Type.PCA_CONTR_EFF_END_DATE → SQ_PSEUDOSSN_FILE_TK_NUM.PCA_CONTR_EFF_END_DATE → PSEUDOSSN_FILE_TK_NUM.PCA_CONTR_EFF_END_DATE | PSEUDOSSN_FILE_TK_NUM.PCA_CONTR_EFF_END_DATE |
| PSEUDOSSN_FROM_SDA_TBL | MAX_ANNUAL_PAY | exp_Final.MAX_ANNUAL_PAY → exp_Conversions.o_MAX_ANNUAL_PAY = DECODE(TRUE, IS_NUMBER(v_MAX_ANNUAL_PAY) AND v_MAX_ANNUAL_PAY_SIGN = '+', TO_DECIMAL(v_MAX_ANNUAL_PAY, 2), IS_NUMBER(v_MAX_ANNUAL_PAY) AND v_MAX_ANNUAL_PAY_SIGN = '-', TO_DECIMAL(v_MAX_ANNUAL_PAY, 2) * -1, IS_NUMBER(v_MAX_ANNUAL_PAY), TO_DECIMAL(v_MAX_ANNUAL_PAY, 2), 0) → exp_Conversions.v_MAX_ANNUAL_PAY = SUBSTR(in_MAX_ANNUAL_PAY,1, 5) \|\| '.' \|\| SUBSTR(in_MAX_ANNUAL_PAY,6, 2) → exp_Determine_Errors.MAX_ANNUAL_PAY → srt_PSEUDOSSN_EFF_DT.MAX_ANNUAL_PAY → fil_Detail_Records.MAX_ANNUAL_PAY → exp_Determine_Record_Type.MAX_ANNUAL_PAY → SQ_PSEUDOSSN_FILE_TK_NUM.MAX_ANNUAL_PAY → PSEUDOSSN_FILE_TK_NUM.MAX_ANNUAL_PAY → exp_Conversions.v_MAX_ANNUAL_PAY_SIGN = SUBSTR(in_MAX_ANNUAL_PAY, 8, 1) | PSEUDOSSN_FILE_TK_NUM.MAX_ANNUAL_PAY |
| PSEUDOSSN_FROM_SDA_TBL | PCA_BIWEEKLY_AMT | exp_Final.PCA_BIWEEKLY_AMT → exp_Conversions.o_PCA_BIWEEKLY_AMOUNT = DECODE(TRUE, IS_NUMBER(v_PCA_BIWEEKLY_AMOUNT) AND v_PCA_BIWEEKLY_AMOUNT_SIGN = '+', TO_DECIMAL(v_PCA_BIWEEKLY_AMOUNT, 2), IS_NUMBER(v_PCA_BIWEEKLY_AMOUNT) AND v_PCA_BIWEEKLY_AMOUNT_SIGN = '-', TO_DECIMAL(v_PCA_BIWEEKLY_AMOUNT, 2) * -1, IS_NUMBER(v_PCA_BIWEEKLY_AMOUNT), TO_DECIMAL(v_PCA_BIWEEKLY_AMOUNT, 2), 0) → exp_Conversions.v_PCA_BIWEEKLY_AMOUNT = SUBSTR(in_PCA_BIWEEKLY_AMOUNT,1, 5) \|\| '.' \|\| SUBSTR(in_PCA_BIWEEKLY_AMOUNT,6, 2) → exp_Determine_Errors.PCA_BIWEEKLY_AMOUNT → srt_PSEUDOSSN_EFF_DT.PCA_BIWEEKLY_AMOUNT → fil_Detail_Records.PCA_BIWEEKLY_AMOUNT → exp_Determine_Record_Type.PCA_BIWEEKLY_AMOUNT → SQ_PSEUDOSSN_FILE_TK_NUM.PCA_BIWEEKLY_AMOUNT → PSEUDOSSN_FILE_TK_NUM.PCA_BIWEEKLY_AMOUNT → exp_Conversions.v_PCA_BIWEEKLY_AMOUNT_SIGN = SUBSTR(in_PCA_BIWEEKLY_AMOUNT, 8, 1) | PSEUDOSSN_FILE_TK_NUM.PCA_BIWEEKLY_AMOUNT |
| PSEUDOSSN_FROM_SDA_TBL | PAY_PLAN_CD | exp_Final.PAY_PLAN_CD → exp_Conversions.PAY_PLAN_CD → exp_Determine_Errors.PAY_PLAN_CD → srt_PSEUDOSSN_EFF_DT.PAY_PLAN_CD → fil_Detail_Records.PAY_PLAN_CD → exp_Determine_Record_Type.PAY_PLAN_CD → SQ_PSEUDOSSN_FILE_TK_NUM.PAY_PLAN_CD → PSEUDOSSN_FILE_TK_NUM.PAY_PLAN_CD | PSEUDOSSN_FILE_TK_NUM.PAY_PLAN_CD |
| PSEUDOSSN_FROM_SDA_TBL | APPT_NTE_DTE | exp_Final.APPT_NTE_DTE → exp_Conversions.o_APP_NTE_DATE = IIF(IS_DATE(v_APP_LIMIT_DATE, 'MM/DD/YYYY'), TO_DATE(v_APP_LIMIT_DATE, 'MM/DD/YYYY')) → exp_Conversions.v_APP_LIMIT_DATE = SUBSTR(in_APP_LIMIT_DATE, 5, 2) \|\| '/' \|\| SUBSTR(in_APP_LIMIT_DATE, 7, 2) \|\| '/' \|\| SUBSTR(in_APP_LIMIT_DATE, 1, 4) -- Builds date in 'MM/DD/YYYY' format, source date format is YYYYDDMM → exp_Determine_Errors.APP_LIMIT_DATE → srt_PSEUDOSSN_EFF_DT.APP_LIMIT_DATE → fil_Detail_Records.APP_LIMIT_DATE → exp_Determine_Record_Type.APP_LIMIT_DATE → SQ_PSEUDOSSN_FILE_TK_NUM.APP_LIMIT_DATE → PSEUDOSSN_FILE_TK_NUM.APP_LIMIT_DATE | PSEUDOSSN_FILE_TK_NUM.APP_LIMIT_DATE |
| PSEUDOSSN_FROM_SDA_TBL | SPECIAL_PROGRAM_CD | exp_Final.SPECIAL_PROGRAM_CD → exp_Conversions.SPECIAL_PROGRAM_CD → exp_Determine_Errors.SPO_CD → srt_PSEUDOSSN_EFF_DT.SPO_CD → fil_Detail_Records.SPO_CD → exp_Determine_Record_Type.SPO_CD → SQ_PSEUDOSSN_FILE_TK_NUM.SPO_CD → PSEUDOSSN_FILE_TK_NUM.SPO_CD | PSEUDOSSN_FILE_TK_NUM.SPO_CD |
| PSEUDOSSN_FROM_SDA_TBL | TERM_ID | exp_Final.TERM_ID → exp_Conversions.TERM_ID → exp_Determine_Errors.TERM_ID → srt_PSEUDOSSN_EFF_DT.TERM_ID → fil_Detail_Records.TERM_ID → exp_Determine_Record_Type.TERM_ID → SQ_PSEUDOSSN_FILE_TK_NUM.TERM_ID → PSEUDOSSN_FILE_TK_NUM.TERM_ID | PSEUDOSSN_FILE_TK_NUM.TERM_ID |
| PSEUDOSSN_FROM_SDA_TBL | EFFECTIVE_DATE | exp_Final.EFFECTIVE_DATE → exp_Conversions.o_EFFECTIVE_DATE = DECODE(TRUE, IS_DATE(v_EFFECTIVE_DATE, 'MM/DD/YYYY'), TO_DATE(v_EFFECTIVE_DATE, 'MM/DD/YYYY'), EMP_FIRST_NAME = 'NOT FROM EH' AND EMP_MID_INIT = 'R', SESSSTARTTIME ) --IIF(IS_DATE(v_EFFECTIVE_DATE, 'MM/DD/YYYY'), -- TO_DATE(v_EFFECTIVE_DATE, 'MM/DD/YYYY')) → exp_Conversions.v_EFFECTIVE_DATE = SUBSTR(in_EFFECTIVE_DATE, 5, 2) \|\| '/' \|\| SUBSTR(in_EFFECTIVE_DATE, 7, 2) \|\| '/' \|\| SUBSTR(in_EFFECTIVE_DATE, 1, 4) -- Builds date in 'MM/DD/YYYY' format, source date format is YYYYDDMM -- MS 12/13/2012 Source date format has been changed from YYYYDDMM to YYYYMMDD → exp_Determine_Errors.EFFECTIVE_DATE → srt_PSEUDOSSN_EFF_DT.EFFECTIVE_DATE → fil_Detail_Records.EFFECTIVE_DATE → exp_Determine_Record_Type.EFFECTIVE_DATE → SQ_PSEUDOSSN_FILE_TK_NUM.EFFECTIVE_DATE → PSEUDOSSN_FILE_TK_NUM.EFFECTIVE_DATE → exp_Determine_Errors.FIRST_NAME → srt_PSEUDOSSN_EFF_DT.FIRST_NAME → fil_Detail_Records.FIRST_NAME → exp_Determine_Record_Type.FIRST_NAME → SQ_PSEUDOSSN_FILE_TK_NUM.FIRST_NAME → PSEUDOSSN_FILE_TK_NUM.FIRST_NAME → exp_Determine_Errors.MIDDLE_INIT → srt_PSEUDOSSN_EFF_DT.MIDDLE_INIT → fil_Detail_Records.MIDDLE_INIT → exp_Determine_Record_Type.MIDDLE_INIT → SQ_PSEUDOSSN_FILE_TK_NUM.MIDDLE_INIT → PSEUDOSSN_FILE_TK_NUM.MIDDLE_INIT | PSEUDOSSN_FILE_TK_NUM.EFFECTIVE_DATE; PSEUDOSSN_FILE_TK_NUM.FIRST_NAME; PSEUDOSSN_FILE_TK_NUM.MIDDLE_INIT |
| PSEUDOSSN_FROM_SDA_TBL | EFFECTIVE_SEQ | exp_Final.EFFECTIVE_SEQ → exp_Conversions.o_EFFECTIVE_SEQ = IIF(IS_NUMBER(in_EFFECTIVE_SEQ), TO_INTEGER(in_EFFECTIVE_SEQ), 0) → exp_Determine_Errors.EFFECTIVE_SEQ → srt_PSEUDOSSN_EFF_DT.EFFECTIVE_SEQ → fil_Detail_Records.EFFECTIVE_SEQ → exp_Determine_Record_Type.EFFECTIVE_SEQ → SQ_PSEUDOSSN_FILE_TK_NUM.EFFECTIVE_SEQ → PSEUDOSSN_FILE_TK_NUM.EFFECTIVE_SEQ | PSEUDOSSN_FILE_TK_NUM.EFFECTIVE_SEQ |
| PSEUDOSSN_FROM_SDA_TBL | PAY_TABL_NO | exp_Final.PAY_TABL_NO → exp_Conversions.PAY_TABL_NO → exp_Determine_Errors.PAY_TABL_NO → srt_PSEUDOSSN_EFF_DT.PAY_TABL_NO → fil_Detail_Records.PAY_TABL_NO → exp_Determine_Record_Type.PAY_TABL_NO → SQ_PSEUDOSSN_FILE_TK_NUM.PAY_TABL_NO → PSEUDOSSN_FILE_TK_NUM.PAY_TABL_NO | PSEUDOSSN_FILE_TK_NUM.PAY_TABL_NO |
| PSEUDOSSN_FROM_SDA_TBL | BUSINESS_UNIT | exp_Final.BUSINESS_UNIT → exp_Conversions.BUSINESS_UNIT → exp_Determine_Errors.BUSINESS_UNIT → srt_PSEUDOSSN_EFF_DT.BUSINESS_UNIT → fil_Detail_Records.BUSINESS_UNIT → exp_Determine_Record_Type.BUSINESS_UNIT → SQ_PSEUDOSSN_FILE_TK_NUM.BUSINESS_UNIT → PSEUDOSSN_FILE_TK_NUM.BUSINESS_UNIT | PSEUDOSSN_FILE_TK_NUM.BUSINESS_UNIT |
| PSEUDOSSN_FROM_SDA_TBL | DEPTID | exp_Final.DEPTID → exp_Conversions.DEPTID → exp_Determine_Errors.DEPTID → srt_PSEUDOSSN_EFF_DT.DEPTID → fil_Detail_Records.DEPTID → exp_Determine_Record_Type.DEPTID → SQ_PSEUDOSSN_FILE_TK_NUM.DEPTID → PSEUDOSSN_FILE_TK_NUM.DEPTID | PSEUDOSSN_FILE_TK_NUM.DEPTID |
| PSEUDOSSN_FROM_SDA_TBL | PCA_CONTR_LEN_YEAR | exp_Final.PCA_CONTR_LEN_YEAR → exp_Conversions.o_PCA_CONTR_LEN_YEAR = IIF(IS_NUMBER(in_PCA_CONTR_YEAR), TO_INTEGER(in_PCA_CONTR_YEAR), 0) → exp_Determine_Errors.PCA_CONTR_YEAR → srt_PSEUDOSSN_EFF_DT.PCA_CONTR_YEAR → fil_Detail_Records.PCA_CONTR_YEAR → exp_Determine_Record_Type.PCA_CONTR_YEAR → SQ_PSEUDOSSN_FILE_TK_NUM.PCA_CONTR_YEAR → PSEUDOSSN_FILE_TK_NUM.PCA_CONTR_YEAR | PSEUDOSSN_FILE_TK_NUM.PCA_CONTR_YEAR |
| PSEUDOSSN_FROM_SDA_TBL | TK_NUM | exp_Final.TK_NUM → exp_Conversions.TK_NUM → exp_Determine_Errors.TK_NUM → srt_PSEUDOSSN_EFF_DT.TK_NUM → fil_Detail_Records.TK_NUM → exp_Determine_Record_Type.o_TK_NUM = TK_NUM --SUBSTR(FILLER_6, 145, 5) → SQ_PSEUDOSSN_FILE_TK_NUM.TK_NUM → PSEUDOSSN_FILE_TK_NUM.TK_NUM | PSEUDOSSN_FILE_TK_NUM.TK_NUM |
| PSEUDOSSN_FROM_SDA_TBL | PP_NUM | exp_Final.PP_NUM → lkp_Current_Pay_Period.PP_NUM [lookup PAY_PERIOD.PP_NUM ON CURR_PP_FLAG = in_CURR_PP_FLAG] | PAY_PERIOD.PP_NUM (lookup); literal/expression: 'Y' (lookup key) |
| PSEUDOSSN_FROM_SDA_TBL | PP_END_YEAR | exp_Final.PP_END_YEAR → lkp_Current_Pay_Period.PP_END_YEAR [lookup PAY_PERIOD.PP_END_YEAR ON CURR_PP_FLAG = in_CURR_PP_FLAG] | PAY_PERIOD.PP_END_YEAR (lookup); literal/expression: 'Y' (lookup key) |

## Mapping `m_Pseudossn_Update_Timekeeper_Number`

- Sessions: `s_Pseudossn_Update_Timekeeper_Number` (#8)
- Sources: `PSEUDOSSN_TBL1`
- Target instances: `PSEUDOSSN_TBL`

### Transformation `SQ_PSEUDOSSN_TBL` (Source Qualifier)

- **Source Filter**: `TK_NUM IS NULL`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `fil_Updates` (Filter)

- **Filter Condition**: `UPDATE_FLAG = TRUE`

### Transformation `lkp_PSEUDOSSN_FROM_SDA_TBL` (Lookup Procedure)

- **Lookup table name**: `PSEUDOSSN_FROM_SDA_TBL`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `PSEUDOSSN = in_PSEUDOSSN`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `upd_Update_TK_NUM` (Update Strategy)

- **Update Strategy Expression**: `DD_UPDATE`
- **Forward Rejected Rows**: `YES`

- Update Strategy `upd_Update_TK_NUM`: `DD_UPDATE` → PSEUDOSSN_TBL
- Lookup `lkp_PSEUDOSSN_FROM_SDA_TBL`: table `PSEUDOSSN_FROM_SDA_TBL` (exists in export: **True**), condition `PSEUDOSSN = in_PSEUDOSSN`, multiple-match policy `Use Any Value`.

### Target instance `PSEUDOSSN_TBL` (table `PSEUDOSSN_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| PSEUDOSSN_TBL | SSN | (not connected — NULL) | — |
| PSEUDOSSN_TBL | CAN_CD | (not connected — NULL) | — |
| PSEUDOSSN_TBL | PSEUDOSSN | upd_Update_TK_NUM.PSEUDOSSN → fil_Updates.PSEUDOSSN → exp_Determine_Updates.PSEUDOSSN → exp_Initial.PSEUDOSSN → SQ_PSEUDOSSN_TBL.PSEUDOSSN → PSEUDOSSN_TBL1.PSEUDOSSN | PSEUDOSSN_TBL1.PSEUDOSSN |
| PSEUDOSSN_TBL | EMPLID | (not connected — NULL) | — |
| PSEUDOSSN_TBL | EMPL_RCD | (not connected — NULL) | — |
| PSEUDOSSN_TBL | APPT_NUM | (not connected — NULL) | — |
| PSEUDOSSN_TBL | EMP_FIRST_NAME | (not connected — NULL) | — |
| PSEUDOSSN_TBL | EMP_MID_INIT | (not connected — NULL) | — |
| PSEUDOSSN_TBL | EMP_LAST_NAME | (not connected — NULL) | — |
| PSEUDOSSN_TBL | SEX | (not connected — NULL) | — |
| PSEUDOSSN_TBL | VETERANS_PREFERENCE_CD | (not connected — NULL) | — |
| PSEUDOSSN_TBL | TENURE_CD | (not connected — NULL) | — |
| PSEUDOSSN_TBL | POSITION_NUM | (not connected — NULL) | — |
| PSEUDOSSN_TBL | US_CITIZENSHIP_CD | (not connected — NULL) | — |
| PSEUDOSSN_TBL | APPT_TYPE_CD | (not connected — NULL) | — |
| PSEUDOSSN_TBL | HIRE_DATE | (not connected — NULL) | — |
| PSEUDOSSN_TBL | HANDICAP_CD | (not connected — NULL) | — |
| PSEUDOSSN_TBL | UNF_ALLOW_CD | (not connected — NULL) | — |
| PSEUDOSSN_TBL | UNIF_ALLOW_DATE | (not connected — NULL) | — |
| PSEUDOSSN_TBL | UNIF_ALLOW_AMT | (not connected — NULL) | — |
| PSEUDOSSN_TBL | RSSSDP | (not connected — NULL) | — |
| PSEUDOSSN_TBL | CEIL_REPORTING_CD | (not connected — NULL) | — |
| PSEUDOSSN_TBL | FUNCTNL_CLASSFCTN_CD | (not connected — NULL) | — |
| PSEUDOSSN_TBL | EMP_STATUS | (not connected — NULL) | — |
| PSEUDOSSN_TBL | MANAGER_STATUS | (not connected — NULL) | — |
| PSEUDOSSN_TBL | POSITION_SENSITIVITY_CD | (not connected — NULL) | — |
| PSEUDOSSN_TBL | CAREER_START_DATE | (not connected — NULL) | — |
| PSEUDOSSN_TBL | CAREER_CONV_DATE | (not connected — NULL) | — |
| PSEUDOSSN_TBL | PROBATION_DATE | (not connected — NULL) | — |
| PSEUDOSSN_TBL | ABNORMAL_RATE_CD | (not connected — NULL) | — |
| PSEUDOSSN_TBL | APPT_LIMIT_HRS | (not connected — NULL) | — |
| PSEUDOSSN_TBL | APPT_LIMIT_PAY | (not connected — NULL) | — |
| PSEUDOSSN_TBL | LAST_PAY_CHANGE | (not connected — NULL) | — |
| PSEUDOSSN_TBL | CHARITY_AREA_CD | (not connected — NULL) | — |
| PSEUDOSSN_TBL | CHARITY_EFF_DATE | (not connected — NULL) | — |
| PSEUDOSSN_TBL | CHARITY_DED_AMT | (not connected — NULL) | — |
| PSEUDOSSN_TBL | LAST_NOA_CD | (not connected — NULL) | — |
| PSEUDOSSN_TBL | QUARTERS_DED_AMT | (not connected — NULL) | — |
| PSEUDOSSN_TBL | SUBSIST_DED_AMT | (not connected — NULL) | — |
| PSEUDOSSN_TBL | PAY_BASIS_CD | (not connected — NULL) | — |
| PSEUDOSSN_TBL | WORK_SCHEDULE_CD | (not connected — NULL) | — |
| PSEUDOSSN_TBL | OCCUPATION_CD | (not connected — NULL) | — |
| PSEUDOSSN_TBL | DUTY_STATION | (not connected — NULL) | — |
| PSEUDOSSN_TBL | JOB_IND | (not connected — NULL) | — |
| PSEUDOSSN_TBL | REG_TEMP_CD | (not connected — NULL) | — |
| PSEUDOSSN_TBL | SEPERATION_DATE | (not connected — NULL) | — |
| PSEUDOSSN_TBL | PCA_CONTR_EFF_START_DATE | (not connected — NULL) | — |
| PSEUDOSSN_TBL | PCA_CONTR_EFF_END_DATE | (not connected — NULL) | — |
| PSEUDOSSN_TBL | MAX_ANNUAL_PAY | (not connected — NULL) | — |
| PSEUDOSSN_TBL | PCA_BIWEEKLY_AMT | (not connected — NULL) | — |
| PSEUDOSSN_TBL | PAY_PLAN_CD | (not connected — NULL) | — |
| PSEUDOSSN_TBL | APPT_NTE_DTE | (not connected — NULL) | — |
| PSEUDOSSN_TBL | SPECIAL_PROGRAM_CD | (not connected — NULL) | — |
| PSEUDOSSN_TBL | TERM_ID | (not connected — NULL) | — |
| PSEUDOSSN_TBL | EFFECTIVE_DATE | (not connected — NULL) | — |
| PSEUDOSSN_TBL | EFFECTIVE_SEQ | (not connected — NULL) | — |
| PSEUDOSSN_TBL | PAY_TABL_NO | (not connected — NULL) | — |
| PSEUDOSSN_TBL | BUSINESS_UNIT | (not connected — NULL) | — |
| PSEUDOSSN_TBL | DEPTID | (not connected — NULL) | — |
| PSEUDOSSN_TBL | PCA_CONTR_LEN_YEAR | (not connected — NULL) | — |
| PSEUDOSSN_TBL | TK_NUM | upd_Update_TK_NUM.TK_NUM → fil_Updates.TK_NUM → exp_Determine_Updates.o_TK_NUM = lkp_TK_NUM → lkp_PSEUDOSSN_FROM_SDA_TBL.TK_NUM [lookup PSEUDOSSN_FROM_SDA_TBL.TK_NUM ON PSEUDOSSN = in_PSEUDOSSN] | PSEUDOSSN_FROM_SDA_TBL.TK_NUM (lookup); PSEUDOSSN_TBL1.PSEUDOSSN (lookup key) |
| PSEUDOSSN_TBL | PP_NUM | (not connected — NULL) | — |
| PSEUDOSSN_TBL | PP_END_YEAR | (not connected — NULL) | — |

## Mapping `m_Pseudossn_Load_SDA_Records_Pseudossn_Tbl`

- Sessions: `s_Pseudossn_Load_SDA_Records_Pseudossn_Tbl` (#9)
- Sources: `PSEUDOSSN_FROM_SDA_TBL`
- Target instances: `PSEUDOSSN_TBL`

### Transformation `SQ_PSEUDOSSN_FROM_SDA_TBL` (Source Qualifier)

- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `fil_Inserts` (Filter)

- **Filter Condition**: `INSERT_FLAG = TRUE`

### Transformation `lkp_PSEUDOSSN_TBL` (Lookup Procedure)

- **Lookup table name**: `PSEUDOSSN_TBL`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `PSEUDOSSN = in_PSEUDOSSN`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

- Lookup `lkp_PSEUDOSSN_TBL`: table `PSEUDOSSN_TBL` (exists in export: **True**), condition `PSEUDOSSN = in_PSEUDOSSN`, multiple-match policy `Use Any Value`.

### Target instance `PSEUDOSSN_TBL` (table `PSEUDOSSN_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| PSEUDOSSN_TBL | SSN | fil_Inserts.SSN → exp_Determine_Inserts.SSN → exp_Initial.SSN → SQ_PSEUDOSSN_FROM_SDA_TBL.SSN → PSEUDOSSN_FROM_SDA_TBL.SSN | PSEUDOSSN_FROM_SDA_TBL.SSN |
| PSEUDOSSN_TBL | CAN_CD | fil_Inserts.CAN_CD → exp_Determine_Inserts.CAN_CD → exp_Initial.CAN_CD → SQ_PSEUDOSSN_FROM_SDA_TBL.CAN_CD → PSEUDOSSN_FROM_SDA_TBL.CAN_CD | PSEUDOSSN_FROM_SDA_TBL.CAN_CD |
| PSEUDOSSN_TBL | PSEUDOSSN | fil_Inserts.PSEUDOSSN → exp_Determine_Inserts.PSEUDOSSN → exp_Initial.PSEUDOSSN → SQ_PSEUDOSSN_FROM_SDA_TBL.PSEUDOSSN → PSEUDOSSN_FROM_SDA_TBL.PSEUDOSSN | PSEUDOSSN_FROM_SDA_TBL.PSEUDOSSN |
| PSEUDOSSN_TBL | EMPLID | fil_Inserts.EMPLID → exp_Determine_Inserts.EMPLID → exp_Initial.EMPLID → SQ_PSEUDOSSN_FROM_SDA_TBL.EMPLID → PSEUDOSSN_FROM_SDA_TBL.EMPLID | PSEUDOSSN_FROM_SDA_TBL.EMPLID |
| PSEUDOSSN_TBL | EMPL_RCD | fil_Inserts.EMPL_RCD → exp_Determine_Inserts.EMPL_RCD → exp_Initial.EMPL_RCD → SQ_PSEUDOSSN_FROM_SDA_TBL.EMPL_RCD → PSEUDOSSN_FROM_SDA_TBL.EMPL_RCD | PSEUDOSSN_FROM_SDA_TBL.EMPL_RCD |
| PSEUDOSSN_TBL | APPT_NUM | fil_Inserts.APPT_NUM → exp_Determine_Inserts.APPT_NUM → exp_Initial.APPT_NUM → SQ_PSEUDOSSN_FROM_SDA_TBL.APPT_NUM → PSEUDOSSN_FROM_SDA_TBL.APPT_NUM | PSEUDOSSN_FROM_SDA_TBL.APPT_NUM |
| PSEUDOSSN_TBL | EMP_FIRST_NAME | fil_Inserts.EMP_FIRST_NAME → exp_Determine_Inserts.EMP_FIRST_NAME → exp_Initial.EMP_FIRST_NAME → SQ_PSEUDOSSN_FROM_SDA_TBL.EMP_FIRST_NAME → PSEUDOSSN_FROM_SDA_TBL.EMP_FIRST_NAME | PSEUDOSSN_FROM_SDA_TBL.EMP_FIRST_NAME |
| PSEUDOSSN_TBL | EMP_MID_INIT | fil_Inserts.EMP_MID_INIT → exp_Determine_Inserts.EMP_MID_INIT → exp_Initial.EMP_MID_INIT → SQ_PSEUDOSSN_FROM_SDA_TBL.EMP_MID_INIT → PSEUDOSSN_FROM_SDA_TBL.EMP_MID_INIT | PSEUDOSSN_FROM_SDA_TBL.EMP_MID_INIT |
| PSEUDOSSN_TBL | EMP_LAST_NAME | fil_Inserts.EMP_LAST_NAME → exp_Determine_Inserts.EMP_LAST_NAME → exp_Initial.EMP_LAST_NAME → SQ_PSEUDOSSN_FROM_SDA_TBL.EMP_LAST_NAME → PSEUDOSSN_FROM_SDA_TBL.EMP_LAST_NAME | PSEUDOSSN_FROM_SDA_TBL.EMP_LAST_NAME |
| PSEUDOSSN_TBL | SEX | fil_Inserts.SEX → exp_Determine_Inserts.SEX → exp_Initial.SEX → SQ_PSEUDOSSN_FROM_SDA_TBL.SEX → PSEUDOSSN_FROM_SDA_TBL.SEX | PSEUDOSSN_FROM_SDA_TBL.SEX |
| PSEUDOSSN_TBL | VETERANS_PREFERENCE_CD | fil_Inserts.VETERANS_PREFERENCE_CD → exp_Determine_Inserts.VETERANS_PREFERENCE_CD → exp_Initial.VETERANS_PREFERENCE_CD → SQ_PSEUDOSSN_FROM_SDA_TBL.VETERANS_PREFERENCE_CD → PSEUDOSSN_FROM_SDA_TBL.VETERANS_PREFERENCE_CD | PSEUDOSSN_FROM_SDA_TBL.VETERANS_PREFERENCE_CD |
| PSEUDOSSN_TBL | TENURE_CD | fil_Inserts.TENURE_CD → exp_Determine_Inserts.TENURE_CD → exp_Initial.TENURE_CD → SQ_PSEUDOSSN_FROM_SDA_TBL.TENURE_CD → PSEUDOSSN_FROM_SDA_TBL.TENURE_CD | PSEUDOSSN_FROM_SDA_TBL.TENURE_CD |
| PSEUDOSSN_TBL | POSITION_NUM | fil_Inserts.POSITION_NUM → exp_Determine_Inserts.POSITION_NUM → exp_Initial.POSITION_NUM → SQ_PSEUDOSSN_FROM_SDA_TBL.POSITION_NUM → PSEUDOSSN_FROM_SDA_TBL.POSITION_NUM | PSEUDOSSN_FROM_SDA_TBL.POSITION_NUM |
| PSEUDOSSN_TBL | US_CITIZENSHIP_CD | fil_Inserts.US_CITIZENSHIP_CD → exp_Determine_Inserts.US_CITIZENSHIP_CD → exp_Initial.US_CITIZENSHIP_CD → SQ_PSEUDOSSN_FROM_SDA_TBL.US_CITIZENSHIP_CD → PSEUDOSSN_FROM_SDA_TBL.US_CITIZENSHIP_CD | PSEUDOSSN_FROM_SDA_TBL.US_CITIZENSHIP_CD |
| PSEUDOSSN_TBL | APPT_TYPE_CD | fil_Inserts.APPT_TYPE_CD → exp_Determine_Inserts.APPT_TYPE_CD → exp_Initial.APPT_TYPE_CD → SQ_PSEUDOSSN_FROM_SDA_TBL.APPT_TYPE_CD → PSEUDOSSN_FROM_SDA_TBL.APPT_TYPE_CD | PSEUDOSSN_FROM_SDA_TBL.APPT_TYPE_CD |
| PSEUDOSSN_TBL | HIRE_DATE | fil_Inserts.HIRE_DATE → exp_Determine_Inserts.HIRE_DATE → exp_Initial.HIRE_DATE → SQ_PSEUDOSSN_FROM_SDA_TBL.HIRE_DATE → PSEUDOSSN_FROM_SDA_TBL.HIRE_DATE | PSEUDOSSN_FROM_SDA_TBL.HIRE_DATE |
| PSEUDOSSN_TBL | HANDICAP_CD | fil_Inserts.HANDICAP_CD → exp_Determine_Inserts.HANDICAP_CD → exp_Initial.HANDICAP_CD → SQ_PSEUDOSSN_FROM_SDA_TBL.HANDICAP_CD → PSEUDOSSN_FROM_SDA_TBL.HANDICAP_CD | PSEUDOSSN_FROM_SDA_TBL.HANDICAP_CD |
| PSEUDOSSN_TBL | UNF_ALLOW_CD | fil_Inserts.UNF_ALLOW_CD → exp_Determine_Inserts.UNF_ALLOW_CD → exp_Initial.UNF_ALLOW_CD → SQ_PSEUDOSSN_FROM_SDA_TBL.UNF_ALLOW_CD → PSEUDOSSN_FROM_SDA_TBL.UNF_ALLOW_CD | PSEUDOSSN_FROM_SDA_TBL.UNF_ALLOW_CD |
| PSEUDOSSN_TBL | UNIF_ALLOW_DATE | fil_Inserts.UNIF_ALLOW_DATE → exp_Determine_Inserts.UNIF_ALLOW_DATE → exp_Initial.UNIF_ALLOW_DATE → SQ_PSEUDOSSN_FROM_SDA_TBL.UNIF_ALLOW_DATE → PSEUDOSSN_FROM_SDA_TBL.UNIF_ALLOW_DATE | PSEUDOSSN_FROM_SDA_TBL.UNIF_ALLOW_DATE |
| PSEUDOSSN_TBL | UNIF_ALLOW_AMT | fil_Inserts.UNIF_ALLOW_AMT → exp_Determine_Inserts.UNIF_ALLOW_AMT → exp_Initial.UNIF_ALLOW_AMT → SQ_PSEUDOSSN_FROM_SDA_TBL.UNIF_ALLOW_AMT → PSEUDOSSN_FROM_SDA_TBL.UNIF_ALLOW_AMT | PSEUDOSSN_FROM_SDA_TBL.UNIF_ALLOW_AMT |
| PSEUDOSSN_TBL | RSSSDP | fil_Inserts.RSSSDP → exp_Determine_Inserts.RSSSDP → exp_Initial.RSSSDP → SQ_PSEUDOSSN_FROM_SDA_TBL.RSSSDP → PSEUDOSSN_FROM_SDA_TBL.RSSSDP | PSEUDOSSN_FROM_SDA_TBL.RSSSDP |
| PSEUDOSSN_TBL | CEIL_REPORTING_CD | fil_Inserts.CEIL_REPORTING_CD → exp_Determine_Inserts.CEIL_REPORTING_CD → exp_Initial.CEIL_REPORTING_CD → SQ_PSEUDOSSN_FROM_SDA_TBL.CEIL_REPORTING_CD → PSEUDOSSN_FROM_SDA_TBL.CEIL_REPORTING_CD | PSEUDOSSN_FROM_SDA_TBL.CEIL_REPORTING_CD |
| PSEUDOSSN_TBL | FUNCTNL_CLASSFCTN_CD | fil_Inserts.FUNCTNL_CLASSFCTN_CD → exp_Determine_Inserts.FUNCTNL_CLASSFCTN_CD → exp_Initial.FUNCTNL_CLASSFCTN_CD → SQ_PSEUDOSSN_FROM_SDA_TBL.FUNCTNL_CLASSFCTN_CD → PSEUDOSSN_FROM_SDA_TBL.FUNCTNL_CLASSFCTN_CD | PSEUDOSSN_FROM_SDA_TBL.FUNCTNL_CLASSFCTN_CD |
| PSEUDOSSN_TBL | EMP_STATUS | fil_Inserts.EMP_STATUS → exp_Determine_Inserts.EMP_STATUS → exp_Initial.EMP_STATUS → SQ_PSEUDOSSN_FROM_SDA_TBL.EMP_STATUS → PSEUDOSSN_FROM_SDA_TBL.EMP_STATUS | PSEUDOSSN_FROM_SDA_TBL.EMP_STATUS |
| PSEUDOSSN_TBL | MANAGER_STATUS | fil_Inserts.MANAGER_STATUS → exp_Determine_Inserts.MANAGER_STATUS → exp_Initial.MANAGER_STATUS → SQ_PSEUDOSSN_FROM_SDA_TBL.MANAGER_STATUS → PSEUDOSSN_FROM_SDA_TBL.MANAGER_STATUS | PSEUDOSSN_FROM_SDA_TBL.MANAGER_STATUS |
| PSEUDOSSN_TBL | POSITION_SENSITIVITY_CD | fil_Inserts.POSITION_SENSITIVITY_CD → exp_Determine_Inserts.POSITION_SENSITIVITY_CD → exp_Initial.POSITION_SENSITIVITY_CD → SQ_PSEUDOSSN_FROM_SDA_TBL.POSITION_SENSITIVITY_CD → PSEUDOSSN_FROM_SDA_TBL.POSITION_SENSITIVITY_CD | PSEUDOSSN_FROM_SDA_TBL.POSITION_SENSITIVITY_CD |
| PSEUDOSSN_TBL | CAREER_START_DATE | fil_Inserts.CAREER_START_DATE → exp_Determine_Inserts.CAREER_START_DATE → exp_Initial.CAREER_START_DATE → SQ_PSEUDOSSN_FROM_SDA_TBL.CAREER_START_DATE → PSEUDOSSN_FROM_SDA_TBL.CAREER_START_DATE | PSEUDOSSN_FROM_SDA_TBL.CAREER_START_DATE |
| PSEUDOSSN_TBL | CAREER_CONV_DATE | fil_Inserts.CAREER_CONV_DATE → exp_Determine_Inserts.CAREER_CONV_DATE → exp_Initial.CAREER_CONV_DATE → SQ_PSEUDOSSN_FROM_SDA_TBL.CAREER_CONV_DATE → PSEUDOSSN_FROM_SDA_TBL.CAREER_CONV_DATE | PSEUDOSSN_FROM_SDA_TBL.CAREER_CONV_DATE |
| PSEUDOSSN_TBL | PROBATION_DATE | fil_Inserts.PROBATION_DATE → exp_Determine_Inserts.PROBATION_DATE → exp_Initial.PROBATION_DATE → SQ_PSEUDOSSN_FROM_SDA_TBL.PROBATION_DATE → PSEUDOSSN_FROM_SDA_TBL.PROBATION_DATE | PSEUDOSSN_FROM_SDA_TBL.PROBATION_DATE |
| PSEUDOSSN_TBL | ABNORMAL_RATE_CD | fil_Inserts.ABNORMAL_RATE_CD → exp_Determine_Inserts.ABNORMAL_RATE_CD → exp_Initial.ABNORMAL_RATE_CD → SQ_PSEUDOSSN_FROM_SDA_TBL.ABNORMAL_RATE_CD → PSEUDOSSN_FROM_SDA_TBL.ABNORMAL_RATE_CD | PSEUDOSSN_FROM_SDA_TBL.ABNORMAL_RATE_CD |
| PSEUDOSSN_TBL | APPT_LIMIT_HRS | fil_Inserts.APPT_LIMIT_HRS → exp_Determine_Inserts.APPT_LIMIT_HRS → exp_Initial.APPT_LIMIT_HRS → SQ_PSEUDOSSN_FROM_SDA_TBL.APPT_LIMIT_HRS → PSEUDOSSN_FROM_SDA_TBL.APPT_LIMIT_HRS | PSEUDOSSN_FROM_SDA_TBL.APPT_LIMIT_HRS |
| PSEUDOSSN_TBL | APPT_LIMIT_PAY | fil_Inserts.APPT_LIMIT_PAY → exp_Determine_Inserts.APPT_LIMIT_PAY → exp_Initial.APPT_LIMIT_PAY → SQ_PSEUDOSSN_FROM_SDA_TBL.APPT_LIMIT_PAY → PSEUDOSSN_FROM_SDA_TBL.APPT_LIMIT_PAY | PSEUDOSSN_FROM_SDA_TBL.APPT_LIMIT_PAY |
| PSEUDOSSN_TBL | LAST_PAY_CHANGE | fil_Inserts.LAST_PAY_CHANGE → exp_Determine_Inserts.LAST_PAY_CHANGE → exp_Initial.LAST_PAY_CHANGE → SQ_PSEUDOSSN_FROM_SDA_TBL.LAST_PAY_CHANGE → PSEUDOSSN_FROM_SDA_TBL.LAST_PAY_CHANGE | PSEUDOSSN_FROM_SDA_TBL.LAST_PAY_CHANGE |
| PSEUDOSSN_TBL | CHARITY_AREA_CD | fil_Inserts.CHARITY_AREA_CD → exp_Determine_Inserts.CHARITY_AREA_CD → exp_Initial.CHARITY_AREA_CD → SQ_PSEUDOSSN_FROM_SDA_TBL.CHARITY_AREA_CD → PSEUDOSSN_FROM_SDA_TBL.CHARITY_AREA_CD | PSEUDOSSN_FROM_SDA_TBL.CHARITY_AREA_CD |
| PSEUDOSSN_TBL | CHARITY_EFF_DATE | fil_Inserts.CHARITY_EFF_DATE → exp_Determine_Inserts.CHARITY_EFF_DATE → exp_Initial.CHARITY_EFF_DATE → SQ_PSEUDOSSN_FROM_SDA_TBL.CHARITY_EFF_DATE → PSEUDOSSN_FROM_SDA_TBL.CHARITY_EFF_DATE | PSEUDOSSN_FROM_SDA_TBL.CHARITY_EFF_DATE |
| PSEUDOSSN_TBL | CHARITY_DED_AMT | fil_Inserts.CHARITY_DED_AMT → exp_Determine_Inserts.CHARITY_DED_AMT → exp_Initial.CHARITY_DED_AMT → SQ_PSEUDOSSN_FROM_SDA_TBL.CHARITY_DED_AMT → PSEUDOSSN_FROM_SDA_TBL.CHARITY_DED_AMT | PSEUDOSSN_FROM_SDA_TBL.CHARITY_DED_AMT |
| PSEUDOSSN_TBL | LAST_NOA_CD | fil_Inserts.LAST_NOA_CD → exp_Determine_Inserts.LAST_NOA_CD → exp_Initial.LAST_NOA_CD → SQ_PSEUDOSSN_FROM_SDA_TBL.LAST_NOA_CD → PSEUDOSSN_FROM_SDA_TBL.LAST_NOA_CD | PSEUDOSSN_FROM_SDA_TBL.LAST_NOA_CD |
| PSEUDOSSN_TBL | QUARTERS_DED_AMT | fil_Inserts.QUARTERS_DED_AMT → exp_Determine_Inserts.QUARTERS_DED_AMT → exp_Initial.QUARTERS_DED_AMT → SQ_PSEUDOSSN_FROM_SDA_TBL.QUARTERS_DED_AMT → PSEUDOSSN_FROM_SDA_TBL.QUARTERS_DED_AMT | PSEUDOSSN_FROM_SDA_TBL.QUARTERS_DED_AMT |
| PSEUDOSSN_TBL | SUBSIST_DED_AMT | fil_Inserts.SUBSIST_DED_AMT → exp_Determine_Inserts.SUBSIST_DED_AMT → exp_Initial.SUBSIST_DED_AMT → SQ_PSEUDOSSN_FROM_SDA_TBL.SUBSIST_DED_AMT → PSEUDOSSN_FROM_SDA_TBL.SUBSIST_DED_AMT | PSEUDOSSN_FROM_SDA_TBL.SUBSIST_DED_AMT |
| PSEUDOSSN_TBL | PAY_BASIS_CD | fil_Inserts.PAY_BASIS_CD → exp_Determine_Inserts.PAY_BASIS_CD → exp_Initial.PAY_BASIS_CD → SQ_PSEUDOSSN_FROM_SDA_TBL.PAY_BASIS_CD → PSEUDOSSN_FROM_SDA_TBL.PAY_BASIS_CD | PSEUDOSSN_FROM_SDA_TBL.PAY_BASIS_CD |
| PSEUDOSSN_TBL | WORK_SCHEDULE_CD | fil_Inserts.WORK_SCHEDULE_CD → exp_Determine_Inserts.WORK_SCHEDULE_CD → exp_Initial.WORK_SCHEDULE_CD → SQ_PSEUDOSSN_FROM_SDA_TBL.WORK_SCHEDULE_CD → PSEUDOSSN_FROM_SDA_TBL.WORK_SCHEDULE_CD | PSEUDOSSN_FROM_SDA_TBL.WORK_SCHEDULE_CD |
| PSEUDOSSN_TBL | OCCUPATION_CD | fil_Inserts.OCCUPATION_CD → exp_Determine_Inserts.OCCUPATION_CD → exp_Initial.OCCUPATION_CD → SQ_PSEUDOSSN_FROM_SDA_TBL.OCCUPATION_CD → PSEUDOSSN_FROM_SDA_TBL.OCCUPATION_CD | PSEUDOSSN_FROM_SDA_TBL.OCCUPATION_CD |
| PSEUDOSSN_TBL | DUTY_STATION | fil_Inserts.DUTY_STATION → exp_Determine_Inserts.DUTY_STATION → exp_Initial.DUTY_STATION → SQ_PSEUDOSSN_FROM_SDA_TBL.DUTY_STATION → PSEUDOSSN_FROM_SDA_TBL.DUTY_STATION | PSEUDOSSN_FROM_SDA_TBL.DUTY_STATION |
| PSEUDOSSN_TBL | JOB_IND | fil_Inserts.JOB_IND → exp_Determine_Inserts.JOB_IND → exp_Initial.JOB_IND → SQ_PSEUDOSSN_FROM_SDA_TBL.JOB_IND → PSEUDOSSN_FROM_SDA_TBL.JOB_IND | PSEUDOSSN_FROM_SDA_TBL.JOB_IND |
| PSEUDOSSN_TBL | REG_TEMP_CD | fil_Inserts.REG_TEMP_CD → exp_Determine_Inserts.REG_TEMP_CD → exp_Initial.REG_TEMP_CD → SQ_PSEUDOSSN_FROM_SDA_TBL.REG_TEMP_CD → PSEUDOSSN_FROM_SDA_TBL.REG_TEMP_CD | PSEUDOSSN_FROM_SDA_TBL.REG_TEMP_CD |
| PSEUDOSSN_TBL | SEPERATION_DATE | fil_Inserts.SEPERATION_DATE → exp_Determine_Inserts.SEPERATION_DATE → exp_Initial.SEPERATION_DATE → SQ_PSEUDOSSN_FROM_SDA_TBL.SEPERATION_DATE → PSEUDOSSN_FROM_SDA_TBL.SEPERATION_DATE | PSEUDOSSN_FROM_SDA_TBL.SEPERATION_DATE |
| PSEUDOSSN_TBL | PCA_CONTR_EFF_START_DATE | fil_Inserts.PCA_CONTR_EFF_START_DATE → exp_Determine_Inserts.PCA_CONTR_EFF_START_DATE → exp_Initial.PCA_CONTR_EFF_START_DATE → SQ_PSEUDOSSN_FROM_SDA_TBL.PCA_CONTR_EFF_START_DATE → PSEUDOSSN_FROM_SDA_TBL.PCA_CONTR_EFF_START_DATE | PSEUDOSSN_FROM_SDA_TBL.PCA_CONTR_EFF_START_DATE |
| PSEUDOSSN_TBL | PCA_CONTR_EFF_END_DATE | fil_Inserts.PCA_CONTR_EFF_END_DATE → exp_Determine_Inserts.PCA_CONTR_EFF_END_DATE → exp_Initial.PCA_CONTR_EFF_END_DATE → SQ_PSEUDOSSN_FROM_SDA_TBL.PCA_CONTR_EFF_END_DATE → PSEUDOSSN_FROM_SDA_TBL.PCA_CONTR_EFF_END_DATE | PSEUDOSSN_FROM_SDA_TBL.PCA_CONTR_EFF_END_DATE |
| PSEUDOSSN_TBL | MAX_ANNUAL_PAY | fil_Inserts.MAX_ANNUAL_PAY → exp_Determine_Inserts.MAX_ANNUAL_PAY → exp_Initial.MAX_ANNUAL_PAY → SQ_PSEUDOSSN_FROM_SDA_TBL.MAX_ANNUAL_PAY → PSEUDOSSN_FROM_SDA_TBL.MAX_ANNUAL_PAY | PSEUDOSSN_FROM_SDA_TBL.MAX_ANNUAL_PAY |
| PSEUDOSSN_TBL | PCA_BIWEEKLY_AMT | fil_Inserts.PCA_BIWEEKLY_AMT → exp_Determine_Inserts.PCA_BIWEEKLY_AMT → exp_Initial.PCA_BIWEEKLY_AMT → SQ_PSEUDOSSN_FROM_SDA_TBL.PCA_BIWEEKLY_AMT → PSEUDOSSN_FROM_SDA_TBL.PCA_BIWEEKLY_AMT | PSEUDOSSN_FROM_SDA_TBL.PCA_BIWEEKLY_AMT |
| PSEUDOSSN_TBL | PAY_PLAN_CD | fil_Inserts.PAY_PLAN_CD → exp_Determine_Inserts.PAY_PLAN_CD → exp_Initial.PAY_PLAN_CD → SQ_PSEUDOSSN_FROM_SDA_TBL.PAY_PLAN_CD → PSEUDOSSN_FROM_SDA_TBL.PAY_PLAN_CD | PSEUDOSSN_FROM_SDA_TBL.PAY_PLAN_CD |
| PSEUDOSSN_TBL | APPT_NTE_DTE | fil_Inserts.APPT_NTE_DTE → exp_Determine_Inserts.APPT_NTE_DTE → exp_Initial.APPT_NTE_DTE → SQ_PSEUDOSSN_FROM_SDA_TBL.APPT_NTE_DTE → PSEUDOSSN_FROM_SDA_TBL.APPT_NTE_DTE | PSEUDOSSN_FROM_SDA_TBL.APPT_NTE_DTE |
| PSEUDOSSN_TBL | SPECIAL_PROGRAM_CD | fil_Inserts.SPECIAL_PROGRAM_CD → exp_Determine_Inserts.SPECIAL_PROGRAM_CD → exp_Initial.SPECIAL_PROGRAM_CD → SQ_PSEUDOSSN_FROM_SDA_TBL.SPECIAL_PROGRAM_CD → PSEUDOSSN_FROM_SDA_TBL.SPECIAL_PROGRAM_CD | PSEUDOSSN_FROM_SDA_TBL.SPECIAL_PROGRAM_CD |
| PSEUDOSSN_TBL | TERM_ID | fil_Inserts.TERM_ID → exp_Determine_Inserts.TERM_ID → exp_Initial.TERM_ID → SQ_PSEUDOSSN_FROM_SDA_TBL.TERM_ID → PSEUDOSSN_FROM_SDA_TBL.TERM_ID | PSEUDOSSN_FROM_SDA_TBL.TERM_ID |
| PSEUDOSSN_TBL | EFFECTIVE_DATE | fil_Inserts.EFFECTIVE_DATE → exp_Determine_Inserts.EFFECTIVE_DATE → exp_Initial.EFFECTIVE_DATE → SQ_PSEUDOSSN_FROM_SDA_TBL.EFFECTIVE_DATE → PSEUDOSSN_FROM_SDA_TBL.EFFECTIVE_DATE | PSEUDOSSN_FROM_SDA_TBL.EFFECTIVE_DATE |
| PSEUDOSSN_TBL | EFFECTIVE_SEQ | fil_Inserts.EFFECTIVE_SEQ → exp_Determine_Inserts.EFFECTIVE_SEQ → exp_Initial.EFFECTIVE_SEQ → SQ_PSEUDOSSN_FROM_SDA_TBL.EFFECTIVE_SEQ → PSEUDOSSN_FROM_SDA_TBL.EFFECTIVE_SEQ | PSEUDOSSN_FROM_SDA_TBL.EFFECTIVE_SEQ |
| PSEUDOSSN_TBL | PAY_TABL_NO | fil_Inserts.PAY_TABL_NO → exp_Determine_Inserts.PAY_TABL_NO → exp_Initial.PAY_TABL_NO → SQ_PSEUDOSSN_FROM_SDA_TBL.PAY_TABL_NO → PSEUDOSSN_FROM_SDA_TBL.PAY_TABL_NO | PSEUDOSSN_FROM_SDA_TBL.PAY_TABL_NO |
| PSEUDOSSN_TBL | BUSINESS_UNIT | fil_Inserts.BUSINESS_UNIT → exp_Determine_Inserts.BUSINESS_UNIT → exp_Initial.BUSINESS_UNIT → SQ_PSEUDOSSN_FROM_SDA_TBL.BUSINESS_UNIT → PSEUDOSSN_FROM_SDA_TBL.BUSINESS_UNIT | PSEUDOSSN_FROM_SDA_TBL.BUSINESS_UNIT |
| PSEUDOSSN_TBL | DEPTID | fil_Inserts.DEPTID → exp_Determine_Inserts.DEPTID → exp_Initial.DEPTID → SQ_PSEUDOSSN_FROM_SDA_TBL.DEPTID → PSEUDOSSN_FROM_SDA_TBL.DEPTID | PSEUDOSSN_FROM_SDA_TBL.DEPTID |
| PSEUDOSSN_TBL | PCA_CONTR_LEN_YEAR | fil_Inserts.PCA_CONTR_LEN_YEAR → exp_Determine_Inserts.PCA_CONTR_LEN_YEAR → exp_Initial.PCA_CONTR_LEN_YEAR → SQ_PSEUDOSSN_FROM_SDA_TBL.PCA_CONTR_LEN_YEAR → PSEUDOSSN_FROM_SDA_TBL.PCA_CONTR_LEN_YEAR | PSEUDOSSN_FROM_SDA_TBL.PCA_CONTR_LEN_YEAR |
| PSEUDOSSN_TBL | TK_NUM | fil_Inserts.TK_NUM → exp_Determine_Inserts.TK_NUM → exp_Initial.TK_NUM → SQ_PSEUDOSSN_FROM_SDA_TBL.TK_NUM → PSEUDOSSN_FROM_SDA_TBL.TK_NUM | PSEUDOSSN_FROM_SDA_TBL.TK_NUM |
| PSEUDOSSN_TBL | PP_NUM | fil_Inserts.PP_NUM → exp_Determine_Inserts.PP_NUM → exp_Initial.PP_NUM → SQ_PSEUDOSSN_FROM_SDA_TBL.PP_NUM → PSEUDOSSN_FROM_SDA_TBL.PP_NUM | PSEUDOSSN_FROM_SDA_TBL.PP_NUM |
| PSEUDOSSN_TBL | PP_END_YEAR | fil_Inserts.PP_END_YEAR → exp_Determine_Inserts.PP_END_YEAR → exp_Initial.PP_END_YEAR → SQ_PSEUDOSSN_FROM_SDA_TBL.PP_END_YEAR → PSEUDOSSN_FROM_SDA_TBL.PP_END_YEAR | PSEUDOSSN_FROM_SDA_TBL.PP_END_YEAR |

## Mapping `m_Pseudossn_Counters`

- Sessions: `s_Pseudossn_Counters` (#10)
- Sources: `PSEUDOSSN_FILE`
- Target instances: `COUNTER_TBL`, `PSEUDOSSN_MESSAGE_FILE`

### Transformation `SQ_PSEUDOSSN_FILE` (Source Qualifier)

- **Number Of Sorted Ports**: `0`

### Transformation `agg_ALL_RECORDS` (Aggregator)

- **Sorted Input**: `NO`

### Transformation `fil_Detail` (Filter)

- **Filter Condition**: `RECORD_TYPE_FLAG = 'D' --RECORD_TYPE_FLAG = 'H' OR`

### Transformation `lkp_Count_PSEUDOSSN_Duplicates_ERROR_TABLE` (Lookup Procedure)

- **Lookup Sql Override**: `SELECT COUNT(*) as COUNT_CURRENT FROM ERROR_TBL a, (SELECT MAX(b1.ERROR_DATE) as ERROR_DATE FROM ERROR_TBL b1 WHERE b1.ERROR_DATE >= TRUNC(SYSDATE) AND b1.PROCESS_NAME = 'm_Pseudossn_Load_Pseudossn_Tbl' AND SUBSTR(b1.ERROR_MESSAGE, 3, 9) = 'duplicate' ) b WHERE a.ERROR_DATE = b.ERROR_DATE AND a.PROCESS_NAME = 'm_Pseudossn_Load_Pseudossn_Tbl'`
- **Lookup table name**: `ERROR_TBL`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `COUNT_CURRENT >= in_CONSTANT`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `lkp_Count_PSEUDOSSN_TBL` (Lookup Procedure)

- **Lookup Sql Override**: `SELECT COUNT(*) as COUNT_CURRENT FROM PSEUDOSSN_TBL`
- **Lookup table name**: `PSEUDOSSN_TBL`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `COUNT_CURRENT >= in_CONSTANT`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `lkp_PSEUDOSSN_TBL_Pay_Period` (Lookup Procedure)

- **Lookup Sql Override**: `SELECT MIN(PSEUDOSSN_TBL.PP_NUM) as PP_NUM, MIN(PSEUDOSSN_TBL.PP_END_YEAR) as PP_END_YEAR FROM PSEUDOSSN_TBL`
- **Lookup table name**: `PSEUDOSSN_TBL`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `PP_END_YEAR >= in_CONSTANT`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `nrm_Counters` (Normalizer)

- **Reset**: `NO`
- **Restart**: `NO`

- Normalizer `nrm_Counters` (vsam=False) occurs: COUNTER_DESCRIPTION×3, COUNTER_VALUE×3; generated: GK_COUNTER_DESCRIPTION, GCID_COUNTER_DESCRIPTION, GCID_COUNTER_VALUE
- Lookup `lkp_Count_PSEUDOSSN_Duplicates_ERROR_TABLE`: table `ERROR_TBL` (exists in export: **True**), condition `COUNT_CURRENT >= in_CONSTANT`, multiple-match policy `Use Any Value`.
- Lookup `lkp_Count_PSEUDOSSN_TBL`: table `PSEUDOSSN_TBL` (exists in export: **True**), condition `COUNT_CURRENT >= in_CONSTANT`, multiple-match policy `Use Any Value`.
- Lookup `lkp_PSEUDOSSN_TBL_Pay_Period`: table `PSEUDOSSN_TBL` (exists in export: **True**), condition `PP_END_YEAR >= in_CONSTANT`, multiple-match policy `Use Any Value`.

### Target instance `COUNTER_TBL` (table `COUNTER_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| COUNTER_TBL | RUN_DATE | exp_Final.o_RUN_DATE = SESSSTARTTIME | literal/expression: SESSSTARTTIME |
| COUNTER_TBL | PROCESS_NAME | exp_Final.o_PROCESS_NAME = $PMMappingName | literal/expression: $PMMappingName |
| COUNTER_TBL | COUNTER_DESCRIPTION | exp_Final.COUNTER_DESCRIPTION → nrm_Counters.COUNTER_DESCRIPTION [normalizer: one row per occurrence of COUNTER_DESCRIPTION_in1, COUNTER_DESCRIPTION_in2, COUNTER_DESCRIPTION_in3] → exp_Counters.o_COUNTER_DESCRIPTION_1 = 'Number of detail records from the PSEUDOSSN file.' → exp_Counters.o_COUNTER_DESCRIPTION_2 = 'Number of detail records loaded to the PSEUDOSSN table.' → exp_Counters.o_COUNTER_DESCRIPTION_3 = 'Number of duplicate records found.' | literal/expression: 'Number of detail records from the PSEUDOSSN file.'; literal/expression: 'Number of detail records loaded to the PSEUDOSSN table.'; literal/expression: 'Number of duplicate records found.' |
| COUNTER_TBL | COUNTER_VALUE | exp_Final.COUNTER_VALUE → nrm_Counters.COUNTER_VALUE [normalizer: one row per occurrence of COUNTER_VALUE_in1, COUNTER_VALUE_in2, COUNTER_VALUE_in3] → exp_Counters.DETAIL_RECORD_COUNT → exp_Detail_Count.DETAIL_RECORD_COUNT → agg_ALL_RECORDS.o_DETAIL_RECORD_COUNT = COUNT(SSN) → fil_Detail.SSN → exp_Determine_Detail.SSN → SQ_PSEUDOSSN_FILE.SSN → PSEUDOSSN_FILE.SSN → exp_Counters.lkp_COUNT_RECORDS_LOADED → lkp_Count_PSEUDOSSN_TBL.COUNT_CURRENT [lookup PSEUDOSSN_TBL.COUNT_CURRENT ON COUNT_CURRENT >= in_CONSTANT] → exp_Counters.lkp_COUNT_DUPLICATES → lkp_Count_PSEUDOSSN_Duplicates_ERROR_TABLE.COUNT_CURRENT [lookup ERROR_TBL.COUNT_CURRENT ON COUNT_CURRENT >= in_CONSTANT] | ERROR_TBL.COUNT_CURRENT (lookup); PSEUDOSSN_FILE.SSN; PSEUDOSSN_TBL.COUNT_CURRENT (lookup); literal/expression: 1 (lookup key) |
| COUNTER_TBL | PP_END_YEAR | (not connected — NULL) | — |
| COUNTER_TBL | PP_NUM | (not connected — NULL) | — |
| COUNTER_TBL | CYCLE_ID | (not connected — NULL) | — |

### Target instance `PSEUDOSSN_MESSAGE_FILE` (table `PSEUDOSSN_MESSAGE_FILE`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| PSEUDOSSN_MESSAGE_FILE | SUBJECT | exp_Final_Message.SUBJECT → exp_Build_Message.o_SUBJECT = SETVARIABLE($$MAP_SUBJECT, v_SUBJECT) → exp_Build_Message.v_SUBJECT = v_ENVIRONMENT \|\| 'Pseudo SSN loaded successfully for Pay Period: ' \|\| TO_CHAR(PP_END_YEAR) \|\| '-' \|\| v_PP_NUM → exp_Build_Message.v_ENVIRONMENT = DECODE(SUBSTR($PMRepositoryServiceName, 1, 4), 'Dev_', 'Dev: ', 'Test', 'Test: ', 'Prod', 'Prod: ') → exp_Counters.lkp_PP_END_YEAR → lkp_PSEUDOSSN_TBL_Pay_Period.PP_END_YEAR [lookup PSEUDOSSN_TBL.PP_END_YEAR ON PP_END_YEAR >= in_CONSTANT] → exp_Build_Message.v_PP_NUM = IIF(PP_NUM < 10, LPAD(TO_CHAR(PP_NUM), 2, '0'), TO_CHAR(PP_NUM) ) → exp_Counters.lkp_PP_NUM → lkp_PSEUDOSSN_TBL_Pay_Period.PP_NUM [lookup PSEUDOSSN_TBL.PP_NUM ON PP_END_YEAR >= in_CONSTANT] | PSEUDOSSN_TBL.PP_END_YEAR (lookup); PSEUDOSSN_TBL.PP_NUM (lookup); literal/expression: 1 (lookup key); literal/expression: DECODE(SUBSTR($PMRepositoryServiceName, 1, 4), 'Dev_', 'Dev: ', 'Test', 'Test: ', 'Prod', 'Prod: ') |
| PSEUDOSSN_MESSAGE_FILE | MESSAGE | exp_Final_Message.MESSAGE → exp_Build_Message.o_MESSAGE = SETVARIABLE($$MAP_MESSAGE, v_MESSAGE) → exp_Build_Message.v_MESSAGE = 'Number of Detail Records from PseudoSSN file = ' \|\| TO_CHAR(COUNTER_1) \|\| CHR(10) \|\| 'Number of Records loaded = ' \|\| TO_CHAR(COUNTER_2) \|\| CHR(10) \|\| 'Number of Duplicate Records = ' \|\| TO_CHAR(COUNTER_3) → exp_Counters.DETAIL_RECORD_COUNT → exp_Detail_Count.DETAIL_RECORD_COUNT → agg_ALL_RECORDS.o_DETAIL_RECORD_COUNT = COUNT(SSN) → fil_Detail.SSN → exp_Determine_Detail.SSN → SQ_PSEUDOSSN_FILE.SSN → PSEUDOSSN_FILE.SSN → exp_Counters.lkp_COUNT_RECORDS_LOADED → lkp_Count_PSEUDOSSN_TBL.COUNT_CURRENT [lookup PSEUDOSSN_TBL.COUNT_CURRENT ON COUNT_CURRENT >= in_CONSTANT] → exp_Counters.lkp_COUNT_DUPLICATES → lkp_Count_PSEUDOSSN_Duplicates_ERROR_TABLE.COUNT_CURRENT [lookup ERROR_TBL.COUNT_CURRENT ON COUNT_CURRENT >= in_CONSTANT] | ERROR_TBL.COUNT_CURRENT (lookup); PSEUDOSSN_FILE.SSN; PSEUDOSSN_TBL.COUNT_CURRENT (lookup); literal/expression: 1 (lookup key) |

