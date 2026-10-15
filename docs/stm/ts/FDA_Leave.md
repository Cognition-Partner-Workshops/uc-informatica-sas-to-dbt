# PowerCenter STM: `CPM`

Derived deterministically from `legacy/informatica_ts/FDA_Leave` by `tools/ts_lineage.py`. Personal identifiers are redacted as `<owner>`, `<path>`, `<email>`.

| Mappings | Sessions | Sources | Targets | Transformations | Mapplets |
|---|---|---|---|---|---|
| 10 | 10 | 7 | 9 | 84 | 0 |

Transformations by type: Aggregator 3, Expression 33, Filter 7, Joiner 1, Lookup Procedure 23, Normalizer 3, Sorter 2, Source Qualifier 11, Update Strategy 1

## Workflow `wf_FDA_Leave`

Session order:

1. `s_0010_PM_FDA_Verify_File` → mapping `m_0010_PM_FDA_Verify_File`
2. `s_0020_PM_FDA_Set_CPM_Calendar` → mapping `m_0020_PM_FDA_Set_CPM_Calendar`
3. `s_0025_PM_FDA_Set_Pay_Calendar` → mapping `m_0025_PM_FDA_Set_Pay_Calendar`
4. `s_0050_PM_FDA_Update_CPM_CYCLE_TBL_FDA` → mapping `m_0050_PM_FDA_Update_CPM_CYCLE_TBL_FDA`
5. `s_0100_PM_FDA_Load_TATRAN_To_DB` → mapping `m_0100_PM_FDA_Load_TATRAN_To_DB`
6. `s_0150_PM_FDA_Error_Counter` → mapping `m_0150_PM_FDA_Error_Counter`
7. `s_0200_PM_FDA_Create_200_Rows` → mapping `m_0200_PM_FDA_Create_Insert_200_Rows`
8. `s_0300_PM_FDA_Create_Output_File` → mapping `m_0300_PM_FDA_Create_Output_File`
9. `s_0500_PM_FDA_IO_Counter` → mapping `m_0500_PM_FDA_IO_Counter`
10. `s_1100_PM_FDA_Send_Email` → mapping `m_1100_PM_FDA_Send_Email`

| From | To | Condition |
|---|---|---|
| s_0020_PM_FDA_Set_CPM_Calendar | s_0025_PM_FDA_Set_Pay_Calendar | $s_0020_PM_FDA_Set_CPM_Calendar.Status = Succeeded |
| s_0050_PM_FDA_Update_CPM_CYCLE_TBL_FDA | s_0100_PM_FDA_Load_TATRAN_To_DB | $s_0050_PM_FDA_Update_CPM_CYCLE_TBL_FDA.Status = Succeeded |
| Start | s_0010_PM_FDA_Verify_File | — |
| s_0025_PM_FDA_Set_Pay_Calendar | s_0050_PM_FDA_Update_CPM_CYCLE_TBL_FDA | $s_0025_PM_FDA_Set_Pay_Calendar.Status = Succeeded |
| s_0300_PM_FDA_Create_Output_File | s_0500_PM_FDA_IO_Counter | $s_0300_PM_FDA_Create_Output_File.Status = Succeeded |
| s_0150_PM_FDA_Error_Counter | s_0200_PM_FDA_Create_200_Rows | $s_0150_PM_FDA_Error_Counter.Status = Succeeded |
| s_0500_PM_FDA_IO_Counter | s_1100_PM_FDA_Send_Email | $s_0500_PM_FDA_IO_Counter.Status = Succeeded |
| s_0010_PM_FDA_Verify_File | s_0020_PM_FDA_Set_CPM_Calendar | $s_0010_PM_FDA_Verify_File.Status = Succeeded |
| s_0200_PM_FDA_Create_200_Rows | s_0300_PM_FDA_Create_Output_File | $s_0200_PM_FDA_Create_200_Rows.Status = Succeeded |
| s_0100_PM_FDA_Load_TATRAN_To_DB | s_0150_PM_FDA_Error_Counter | $s_0100_PM_FDA_Load_TATRAN_To_DB.Status = Succeeded |

Command tasks:

- `s_0025_PM_FDA_Set_Pay_Calendar` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_0050_PM_FDA_Update_CPM_CYCLE_TBL_FDA` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_CYCLE_ID` = `$$WF_CYCLE_ID`; `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_0050_PM_FDA_Update_CPM_CYCLE_TBL_FDA` / Post-session success variable assignment `postsession_success_variable_assignment`: `$$WF_CYCLE_ID` = `$$MAP_CYCLE_ID`
- `s_0500_PM_FDA_IO_Counter` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_SUBJECT` = `$$WF_SUBJECT`; `$$MAP_MESSAGE` = `$$WF_MESSAGE`; `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`; `$$MAP_CYCLE_ID` = `$$WF_CYCLE_ID`
- `s_0500_PM_FDA_IO_Counter` / Post-session success variable assignment `postsession_success_variable_assignment`: `$$WF_SUBJECT` = `$$MAP_SUBJECT`; `$$WF_MESSAGE` = `$$MAP_MESSAGE`
- `s_0200_PM_FDA_Create_200_Rows` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_1100_PM_FDA_Send_Email` / Post-session success command `post_session_success_command`: `Command1` = `cd $Param_Root_Directory/data/int/out/CPM; cp $Param_FDA_12200_out_file FDA.TATRAN.PP$$WF_PP_NUM.TXT`; `Command2` = `<path>/scripts/fda_transfer.sh FDA.TATRAN.PP$$WF_PP_NUM.TXT`; `Command3` = `cd $Param_Root_Directory/data/int/in/CPM; mv tatran* $Param_Root_Directory/data/archive/CPM/`
- `s_0020_PM_FDA_Set_CPM_Calendar` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_0020_PM_FDA_Set_CPM_Calendar` / Post-session success variable assignment `postsession_success_variable_assignment`: `$$WF_PP_END_YEAR` = `$$MAP_PP_END_YEAR`; `$$WF_PP_NUM` = `$$MAP_PP_NUM`
- `s_0150_PM_FDA_Error_Counter` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`; `$$MAP_CYCLE_ID` = `$$WF_CYCLE_ID`

- Session `s_0010_PM_FDA_Verify_File`: WRITER `CPM_FDA_PAY_PERIOD_FILE` Append if Exists=`NO`, Output Type=`File`, Output file directory=`$PMTargetFileDir\`, Output filename=`cpm_fda_pay_period_file.txt`; READER `HI_PM_FDA_TATRAN_FLAT_FILE_NAME` Command=`cd $Param_Root_Directory/data/int/in/CPM; ls -1 tatran*`, Input Type=`Command`, Source file directory=`$Param_Root_Directory/data/int/in/CPM`, Source filename=`HI_PM_FDA_TATRAN_FLAT`
- Session `s_0020_PM_FDA_Set_CPM_Calendar`: WRITER `CPM_FDA_CPM_PAY_PERIOD_FILE` Append if Exists=`NO`, Output Type=`File`, Output file directory=`$PMTargetFileDir\`, Output filename=`cpm_fda_cpm_pay_period_file.txt`
- Session `s_0025_PM_FDA_Set_Pay_Calendar`: WRITER `CPM_FDA_PAY_PERIOD_FILE` Append if Exists=`NO`, Output Type=`File`, Output file directory=`$PMTargetFileDir\`, Output filename=`cpm_fda_pay_period_file.txt`
- Session `s_0050_PM_FDA_Update_CPM_CYCLE_TBL_FDA`: WRITER `CPM_CYCLE_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`
- Session `s_0100_PM_FDA_Load_TATRAN_To_DB`: WRITER `HI_PM_FDA_TATRAN_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`YES`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`; READER `HI_PM_FDA_TATRAN_FLAT` Command=`cd $Param_Root_Directory/data/int/in/CPM; ls -1 tatran*`, Input Type=`Command`, Source file directory=`$Param_Root_Directory/data/int/in/CPM`, Source filename=`$Param_FDA_12100_file`
- Session `s_0150_PM_FDA_Error_Counter`: WRITER `ERROR_TBL_PAD` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`; WRITER `ERROR_TBL_YTD` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`; WRITER `ERROR_TBL_CPM` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`; WRITER `ERROR_TBL_MER` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`
- Session `s_0200_PM_FDA_Create_200_Rows`: WRITER `HI_PM_FDA_TATRAN_TBL1` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`
- Session `s_0300_PM_FDA_Create_Output_File`: WRITER `HI_PM_FDA_TATRAN_FLAT` Append if Exists=`NO`, Output Type=`File`, Output file directory=`$Param_Root_Directory/data/int/out/CPM`, Output filename=`$Param_FDA_12200_out_file`
- Session `s_0500_PM_FDA_IO_Counter`: WRITER `FDA_EXTRACT_MESSAGE_FILE` Append if Exists=`NO`, Output Type=`File`, Output file directory=`$Param_Root_Directory/data/int/out/CPM`, Output filename=`fda_extract_message_file.txt`; WRITER `COUNTER_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Bulk`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`
- Session `s_1100_PM_FDA_Send_Email`: WRITER `GENERIC_TARGET_FILE` Append if Exists=`NO`, Output Type=`File`, Output file directory=`$PMTargetFileDir\`, Output filename=`generic_target_file1.out`

## Source definitions

| Source | Database type | Fields |
|---|---|---|
| CPM_CYCLE_TBL | Oracle | 5 |
| ERROR_TBL | Oracle | 8 |
| HI_GENERIC_SRC_TBL | Oracle | 1 |
| HI_PM_FDA_TATRAN_FLAT | Flat File | 6 |
| HI_PM_FDA_TATRAN_FLAT_FILE_NAME | Flat File | 7 |
| HI_PM_FDA_TATRAN_TBL | Oracle | 8 |
| PAY_PERIOD | Oracle | 10 |

## Target definitions

| Target | Database type | Fields |
|---|---|---|
| COUNTER_TBL | Oracle | 7 |
| CPM_CYCLE_TBL | Oracle | 5 |
| CPM_FDA_CPM_PAY_PERIOD_FILE | Flat File | 1 |
| CPM_FDA_PAY_PERIOD_FILE | Flat File | 1 |
| ERROR_TBL | Oracle | 8 |
| FDA_EXTRACT_MESSAGE_FILE | Flat File | 2 |
| GENERIC_TARGET_FILE | Flat File | 1 |
| HI_PM_FDA_TATRAN_FLAT | Flat File | 6 |
| HI_PM_FDA_TATRAN_TBL | Oracle | 8 |

## Mapping `m_0010_PM_FDA_Verify_File`

- Sessions: `s_0010_PM_FDA_Verify_File` (#1)
- Sources: `HI_PM_FDA_TATRAN_FLAT_FILE_NAME`
- Target instances: `CPM_FDA_PAY_PERIOD_FILE`

### Transformation `SQ_HI_PM_FDA_TATRAN_FLAT_FILE_NAME` (Source Qualifier)

- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `agg_Count_Number_of_Files` (Aggregator)

- **Sorted Input**: `YES`

### Transformation `lkp_CPM_NEWPAY_TBL` (Lookup Procedure)

- **Lookup Sql Override**: `SELECT CPM_NEWPAY_TBL.DFAS_PSEUDO_SSN as DFAS_PSEUDO_SSN, CPM_NEWPAY_TBL.PP_END_YEAR as PP_END_YEAR, CPM_NEWPAY_TBL.PP_NUM as PP_NUM, CPM_NEWPAY_TBL.MP_POOL_DES as MP_POOL_DES FROM CPM_NEWPAY_TBL`
- **Lookup table name**: `CPM_NEWPAY_TBL`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `PP_END_YEAR = in_PARAM_PP_END_YEAR AND PP_NUM = in_PARAM_PP_NUM AND MP_POOL_DES = in_MP_POOL_DES`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `lkp_Current_Pay_Period` (Lookup Procedure)

- **Lookup table name**: `PAY_PERIOD`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `CURR_PP_FLAG = in_CURR_PP_FLAG`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `lkp_Existing_Pay_Period` (Lookup Procedure)

- **Lookup table name**: `PAY_PERIOD`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `PP_NUM = in_PARAM_PP_NUM AND PP_END_YEAR = in_PARAM_PP_END_YEAR`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `srt_Distinct_File_Names` (Sorter)

- **Case Sensitive**: `YES`
- **Distinct**: `YES`
- **Null Treated Low**: `NO`

- Sorter `srt_Distinct_File_Names` keys: CurrentlyProcessedFileName ASCENDING; distinct=YES
- Lookup `lkp_CPM_NEWPAY_TBL`: table `CPM_NEWPAY_TBL` (exists in export: **False**), condition `PP_END_YEAR = in_PARAM_PP_END_YEAR AND PP_NUM = in_PARAM_PP_NUM AND MP_POOL_DES = in_MP_POOL_DES`, multiple-match policy `Use Any Value`.
- Lookup `lkp_Current_Pay_Period`: table `PAY_PERIOD` (exists in export: **True**), condition `CURR_PP_FLAG = in_CURR_PP_FLAG`, multiple-match policy `Use Any Value`.
- Lookup `lkp_Existing_Pay_Period`: table `PAY_PERIOD` (exists in export: **True**), condition `PP_NUM = in_PARAM_PP_NUM AND PP_END_YEAR = in_PARAM_PP_END_YEAR`, multiple-match policy `Use Any Value`.

### Target instance `CPM_FDA_PAY_PERIOD_FILE` (table `CPM_FDA_PAY_PERIOD_FILE`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| CPM_FDA_PAY_PERIOD_FILE | CPM_PAY_PERIOD | exp_Final.o_CPM_PAY_PERIOD = PARAM_PP_END_YEAR \|\| '-' \|\| LPAD(PARAM_PP_NUM, 2, '0') → exp_Validate_Parameters.PARAM_PP_END_YEAR → exp_Set_Parameters.o_PARAM_PP_END_YEAR = SETVARIABLE($$MAP_PP_END_YEAR, TO_CHAR(v_PP_END_YEAR)) → exp_Set_Parameters.v_PP_END_YEAR = DECODE(TRUE, v_DEFAULT_TO_CURR_PP_FLAG = TRUE, lkp_CURR_PP_END_YEAR, v_PAY_PERIOD_PARAM_EXISTS_FLAG = TRUE, PARAM_PP_END_YEAR ) --IIF(v_PAY_PERIOD_PARAM_EXISTS_FLAG = TRUE, -- TO_CHAR(PARAM_PP_END_YEAR), -- TO_CHAR(lkp_CURR_PP_END_YEAR)) → exp_Set_Parameters.v_DEFAULT_TO_CURR_PP_FLAG = DECODE(TRUE, (ISNULL(INIT_PARAM_PP_END_YEAR) OR IS_SPACES(INIT_PARAM_PP_END_YEAR) OR LENGTH(LTRIM(INIT_PARAM_PP_END_YEAR)) = 0) AND (ISNULL(INIT_PARAM_PP_NUM) OR IS_SPACES(INIT_PARAM_PP_NUM) OR LENGTH(LTRIM(INIT_PARAM_PP_NUM)) = 0), TRUE, FALSE) → exp_Set_Parameters.INIT_PARAM_PP_END_YEAR → exp_Set_Parameters.INIT_PARAM_PP_NUM → lkp_Current_Pay_Period.PP_END_YEAR [lookup PAY_PERIOD.PP_END_YEAR ON CURR_PP_FLAG = in_CURR_PP_FLAG] → exp_Set_Parameters.v_PAY_PERIOD_PARAM_EXISTS_FLAG = IIF(NOT ISNULL(lkp_PP_NUM), TRUE, FALSE) → exp_Set_Parameters.lkp_PP_NUM → exp_Set_Parameters.PARAM_PP_END_YEAR → exp_Validate_Parameters.PARAM_PP_NUM → exp_Set_Parameters.o_PARAM_PP_NUM = SETVARIABLE($$MAP_PP_NUM, TO_CHAR(v_PP_NUM)) → exp_Set_Parameters.v_PP_NUM = DECODE(TRUE, v_DEFAULT_TO_CURR_PP_FLAG = TRUE, lkp_CURR_PP_NUM, v_PAY_PERIOD_PARAM_EXISTS_FLAG = TRUE, PARAM_PP_NUM ) --IIF(v_PAY_PERIOD_PARAM_EXISTS_FLAG = TRUE, -- TO_CHAR(PARAM_PP_NUM), -- TO_CHAR(lkp_CURR_PP_NUM)) → lkp_Current_Pay_Period.PP_NUM [lookup PAY_PERIOD.PP_NUM ON CURR_PP_FLAG = in_CURR_PP_FLAG] → exp_Set_Parameters.PARAM_PP_NUM | PAY_PERIOD.PP_END_YEAR (lookup); PAY_PERIOD.PP_NUM (lookup); literal/expression: 'Y' (lookup key) |

## Mapping `m_0020_PM_FDA_Set_CPM_Calendar`

- Sessions: `s_0020_PM_FDA_Set_CPM_Calendar` (#2)
- Sources: `PAY_PERIOD1`
- Target instances: `CPM_FDA_CPM_PAY_PERIOD_FILE`

### Transformation `SQ_PAY_PERIOD` (Source Qualifier)

- **Sql Query**: `SELECT MAX(PAY_PERIOD.PP_NUM) PP_NUM , MAX(PAY_PERIOD.PP_END_YEAR) PP_END_YEAR FROM PAY_PERIOD`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `lkp_Current_Pay_Period` (Lookup Procedure)

- **Lookup table name**: `PAY_PERIOD`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `CURR_PP_FLAG = in_CURR_PP_FLAG`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `lkp_Existing_Pay_Period` (Lookup Procedure)

- **Lookup table name**: `PAY_PERIOD`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `PP_NUM = in_PARAM_PP_NUM AND PP_END_YEAR = in_PARAM_PP_END_YEAR`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

- Lookup `lkp_Current_Pay_Period`: table `PAY_PERIOD` (exists in export: **True**), condition `CURR_PP_FLAG = in_CURR_PP_FLAG`, multiple-match policy `Use Any Value`.
- Lookup `lkp_Existing_Pay_Period`: table `PAY_PERIOD` (exists in export: **True**), condition `PP_NUM = in_PARAM_PP_NUM AND PP_END_YEAR = in_PARAM_PP_END_YEAR`, multiple-match policy `Use Any Value`.
- SQL override `SQ_PAY_PERIOD` positional bindings: 1 → `PP_NUM` = `MAX(PAY_PERIOD.PP_NUM) PP_NUM`; 2 → `PP_END_YEAR` = `MAX(PAY_PERIOD.PP_END_YEAR) PP_END_YEAR`

### Target instance `CPM_FDA_CPM_PAY_PERIOD_FILE` (table `CPM_FDA_CPM_PAY_PERIOD_FILE`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| CPM_FDA_CPM_PAY_PERIOD_FILE | CPM_PAY_PERIOD | exp_Final.o_CPM_PAY_PERIOD = PARAM_PP_END_YEAR \|\| '-' \|\| LPAD(PARAM_PP_NUM, 2, '0') → exp_Validate_Parameters.PARAM_PP_END_YEAR → exp_Set_Parameters.o_PARAM_PP_END_YEAR = SETVARIABLE($$MAP_PP_END_YEAR, TO_CHAR(v_PP_END_YEAR)) → exp_Set_Parameters.v_PP_END_YEAR = DECODE(TRUE, v_DEFAULT_TO_CURR_PP_FLAG = TRUE, lkp_CURR_PP_END_YEAR, v_PAY_PERIOD_PARAM_EXISTS_FLAG = TRUE, PARAM_PP_END_YEAR ) --IIF(v_PAY_PERIOD_PARAM_EXISTS_FLAG = TRUE, -- TO_CHAR(PARAM_PP_END_YEAR), -- TO_CHAR(lkp_CURR_PP_END_YEAR)) → exp_Set_Parameters.v_DEFAULT_TO_CURR_PP_FLAG = DECODE(TRUE, (ISNULL(INIT_PARAM_PP_END_YEAR) OR IS_SPACES(INIT_PARAM_PP_END_YEAR) OR LENGTH(LTRIM(INIT_PARAM_PP_END_YEAR)) = 0) AND (ISNULL(INIT_PARAM_PP_NUM) OR IS_SPACES(INIT_PARAM_PP_NUM) OR LENGTH(LTRIM(INIT_PARAM_PP_NUM)) = 0), TRUE, FALSE) → exp_Initial.o_INIT_PARAM_PP_END_YEAR = $$MAP_PP_END_YEAR → exp_Initial.o_INIT_PARAM_PP_NUM = $$MAP_PP_NUM → lkp_Current_Pay_Period.PP_END_YEAR [lookup PAY_PERIOD.PP_END_YEAR ON CURR_PP_FLAG = in_CURR_PP_FLAG] → exp_Set_Parameters.v_PAY_PERIOD_PARAM_EXISTS_FLAG = IIF(NOT ISNULL(lkp_PP_NUM), TRUE, FALSE) → lkp_Existing_Pay_Period.PP_NUM [lookup PAY_PERIOD.PP_NUM ON PP_NUM = in_PARAM_PP_NUM AND PP_END_YEAR = in_PARAM_PP_END_YEAR] → exp_Initial.o_PARAM_PP_END_YEAR = v_PARAM_PP_END_YEAR → exp_Initial.v_PARAM_PP_END_YEAR = IIF(NOT IS_NUMBER($$MAP_PP_END_YEAR), 0, TO_DECIMAL($$MAP_PP_END_YEAR)) → exp_Validate_Parameters.PARAM_PP_NUM → exp_Set_Parameters.o_PARAM_PP_NUM = SETVARIABLE($$MAP_PP_NUM, LPAD(TO_CHAR(v_PP_NUM), 2, '0')) → exp_Set_Parameters.v_PP_NUM = DECODE(TRUE, v_DEFAULT_TO_CURR_PP_FLAG = TRUE, lkp_CURR_PP_NUM, v_PAY_PERIOD_PARAM_EXISTS_FLAG = TRUE, PARAM_PP_NUM ) --IIF(v_PAY_PERIOD_PARAM_EXISTS_FLAG = TRUE, -- TO_CHAR(PARAM_PP_NUM), -- TO_CHAR(lkp_CURR_PP_NUM)) → lkp_Current_Pay_Period.PP_NUM [lookup PAY_PERIOD.PP_NUM ON CURR_PP_FLAG = in_CURR_PP_FLAG] → exp_Initial.o_PARAM_PP_NUM = v_PARAM_PP_NUM → exp_Initial.v_PARAM_PP_NUM = IIF(NOT IS_NUMBER($$MAP_PP_NUM), 0, TO_DECIMAL($$MAP_PP_NUM)) | PAY_PERIOD.PP_END_YEAR (lookup); PAY_PERIOD.PP_NUM (lookup); literal/expression: $$MAP_PP_END_YEAR; literal/expression: $$MAP_PP_NUM; literal/expression: 'Y' (lookup key); literal/expression: IIF(NOT IS_NUMBER($$MAP_PP_END_YEAR), 0, TO_DECIMAL($$MAP_PP_END_YEAR)); literal/expression: IIF(NOT IS_NUMBER($$MAP_PP_END_YEAR), 0, TO_DECIMAL($$MAP_PP_END_YEAR)) (lookup key); literal/expression: IIF(NOT IS_NUMBER($$MAP_PP_NUM), 0, TO_DECIMAL($$MAP_PP_NUM)); literal/expression: IIF(NOT IS_NUMBER($$MAP_PP_NUM), 0, TO_DECIMAL($$MAP_PP_NUM)) (lookup key) |

## Mapping `m_0025_PM_FDA_Set_Pay_Calendar`

- Sessions: `s_0025_PM_FDA_Set_Pay_Calendar` (#3)
- Sources: `PAY_PERIOD1`
- Target instances: `CPM_FDA_PAY_PERIOD_FILE`

### Transformation `SQ_PAY_PERIOD` (Source Qualifier)

- **Sql Query**: `SELECT MAX(PAY_PERIOD.PP_NUM) PP_NUM , MAX(PAY_PERIOD.PP_END_YEAR) PP_END_YEAR FROM PAY_PERIOD`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `lkp_CPM_NEWPAY_TBL` (Lookup Procedure)

- **Lookup table name**: `CPM_NEWPAY_TBL`
- **Lookup Source Filter**: `PP_END_YEAR = TO_NUMBER('$$MAP_PP_END_YEAR') AND PP_NUM = TO_NUMBER('$$MAP_PP_NUM')`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `PP_END_YEAR = in_PARAM_PP_END_YEAR AND PP_NUM = in_PARAM_PP_NUM AND MP_POOL_DES = in_MP_POOL_DES`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `lkp_Current_Pay_Period` (Lookup Procedure)

- **Lookup table name**: `PAY_PERIOD`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `CURR_PP_FLAG = in_CURR_PP_FLAG`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `lkp_Existing_Pay_Period` (Lookup Procedure)

- **Lookup table name**: `PAY_PERIOD`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `PP_NUM = in_PARAM_PP_NUM AND PP_END_YEAR = in_PARAM_PP_END_YEAR`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

- Lookup `lkp_CPM_NEWPAY_TBL`: table `CPM_NEWPAY_TBL` (exists in export: **False**), condition `PP_END_YEAR = in_PARAM_PP_END_YEAR AND PP_NUM = in_PARAM_PP_NUM AND MP_POOL_DES = in_MP_POOL_DES`, multiple-match policy `Use Any Value`.
- Lookup `lkp_Current_Pay_Period`: table `PAY_PERIOD` (exists in export: **True**), condition `CURR_PP_FLAG = in_CURR_PP_FLAG`, multiple-match policy `Use Any Value`.
- Lookup `lkp_Existing_Pay_Period`: table `PAY_PERIOD` (exists in export: **True**), condition `PP_NUM = in_PARAM_PP_NUM AND PP_END_YEAR = in_PARAM_PP_END_YEAR`, multiple-match policy `Use Any Value`.
- SQL override `SQ_PAY_PERIOD` positional bindings: 1 → `PP_NUM` = `MAX(PAY_PERIOD.PP_NUM) PP_NUM`; 2 → `PP_END_YEAR` = `MAX(PAY_PERIOD.PP_END_YEAR) PP_END_YEAR`

### Target instance `CPM_FDA_PAY_PERIOD_FILE` (table `CPM_FDA_PAY_PERIOD_FILE`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| CPM_FDA_PAY_PERIOD_FILE | CPM_PAY_PERIOD | exp_Final.o_CPM_PAY_PERIOD = PARAM_PP_END_YEAR \|\| '-' \|\| LPAD(PARAM_PP_NUM, 2, '0') → exp_Validate_Parameters.PARAM_PP_END_YEAR → exp_Set_Parameters.o_PARAM_PP_END_YEAR = SETVARIABLE($$MAP_PP_END_YEAR, TO_CHAR(v_PP_END_YEAR)) → exp_Set_Parameters.v_PP_END_YEAR = DECODE(TRUE, v_DEFAULT_TO_CURR_PP_FLAG = TRUE, lkp_CURR_PP_END_YEAR, v_PAY_PERIOD_PARAM_EXISTS_FLAG = TRUE, PARAM_PP_END_YEAR ) --IIF(v_PAY_PERIOD_PARAM_EXISTS_FLAG = TRUE, -- TO_CHAR(PARAM_PP_END_YEAR), -- TO_CHAR(lkp_CURR_PP_END_YEAR)) → exp_Set_Parameters.v_DEFAULT_TO_CURR_PP_FLAG = DECODE(TRUE, (ISNULL(INIT_PARAM_PP_END_YEAR) OR IS_SPACES(INIT_PARAM_PP_END_YEAR) OR LENGTH(LTRIM(INIT_PARAM_PP_END_YEAR)) = 0) AND (ISNULL(INIT_PARAM_PP_NUM) OR IS_SPACES(INIT_PARAM_PP_NUM) OR LENGTH(LTRIM(INIT_PARAM_PP_NUM)) = 0), TRUE, FALSE) → exp_Initial.o_INIT_PARAM_PP_END_YEAR = $$MAP_PP_END_YEAR → exp_Initial.o_INIT_PARAM_PP_NUM = $$MAP_PP_NUM → lkp_Current_Pay_Period.PP_END_YEAR [lookup PAY_PERIOD.PP_END_YEAR ON CURR_PP_FLAG = in_CURR_PP_FLAG] → exp_Set_Parameters.v_PAY_PERIOD_PARAM_EXISTS_FLAG = IIF(NOT ISNULL(lkp_PP_NUM), TRUE, FALSE) → lkp_Existing_Pay_Period.PP_NUM [lookup PAY_PERIOD.PP_NUM ON PP_NUM = in_PARAM_PP_NUM AND PP_END_YEAR = in_PARAM_PP_END_YEAR] → exp_Initial.o_PARAM_PP_END_YEAR = v_PARAM_PP_END_YEAR → exp_Initial.v_PARAM_PP_END_YEAR = IIF(NOT IS_NUMBER($$MAP_PP_END_YEAR), 0, TO_DECIMAL($$MAP_PP_END_YEAR)) → exp_Validate_Parameters.PARAM_PP_NUM → exp_Set_Parameters.o_PARAM_PP_NUM = SETVARIABLE($$MAP_PP_NUM, LPAD(TO_CHAR(v_PP_NUM), 2, '0')) → exp_Set_Parameters.v_PP_NUM = DECODE(TRUE, v_DEFAULT_TO_CURR_PP_FLAG = TRUE, lkp_CURR_PP_NUM, v_PAY_PERIOD_PARAM_EXISTS_FLAG = TRUE, PARAM_PP_NUM ) --IIF(v_PAY_PERIOD_PARAM_EXISTS_FLAG = TRUE, -- TO_CHAR(PARAM_PP_NUM), -- TO_CHAR(lkp_CURR_PP_NUM)) → lkp_Current_Pay_Period.PP_NUM [lookup PAY_PERIOD.PP_NUM ON CURR_PP_FLAG = in_CURR_PP_FLAG] → exp_Initial.o_PARAM_PP_NUM = v_PARAM_PP_NUM → exp_Initial.v_PARAM_PP_NUM = IIF(NOT IS_NUMBER($$MAP_PP_NUM), 0, TO_DECIMAL($$MAP_PP_NUM)) | PAY_PERIOD.PP_END_YEAR (lookup); PAY_PERIOD.PP_NUM (lookup); literal/expression: $$MAP_PP_END_YEAR; literal/expression: $$MAP_PP_NUM; literal/expression: 'Y' (lookup key); literal/expression: IIF(NOT IS_NUMBER($$MAP_PP_END_YEAR), 0, TO_DECIMAL($$MAP_PP_END_YEAR)); literal/expression: IIF(NOT IS_NUMBER($$MAP_PP_END_YEAR), 0, TO_DECIMAL($$MAP_PP_END_YEAR)) (lookup key); literal/expression: IIF(NOT IS_NUMBER($$MAP_PP_NUM), 0, TO_DECIMAL($$MAP_PP_NUM)); literal/expression: IIF(NOT IS_NUMBER($$MAP_PP_NUM), 0, TO_DECIMAL($$MAP_PP_NUM)) (lookup key) |

## Mapping `m_0050_PM_FDA_Update_CPM_CYCLE_TBL_FDA`

- Sessions: `s_0050_PM_FDA_Update_CPM_CYCLE_TBL_FDA` (#4)
- Sources: `CPM_CYCLE_TBL1`
- Target instances: `CPM_CYCLE_TBL`

### Transformation `SQ_CPM_CYCLE_TBL` (Source Qualifier)

- **Source Filter**: `CPM_CYCLE_TBL.PROCESS_NAME = 'FDA'`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `lkp_PAY_PERIOD` (Lookup Procedure)

- **Lookup table name**: `PAY_PERIOD`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `PP_END_YEAR = in_PARAM_PP_END_YEAR AND PP_NUM = in_PARAM_PP_NUM`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `upd_DFAS_HEADER_TABLE` (Update Strategy)

- **Update Strategy Expression**: `DD_UPDATE`
- **Forward Rejected Rows**: `YES`

- Update Strategy `upd_DFAS_HEADER_TABLE`: `DD_UPDATE` → CPM_CYCLE_TBL
- Lookup `lkp_PAY_PERIOD`: table `PAY_PERIOD` (exists in export: **True**), condition `PP_END_YEAR = in_PARAM_PP_END_YEAR AND PP_NUM = in_PARAM_PP_NUM`, multiple-match policy `Use Any Value`.

### Target instance `CPM_CYCLE_TBL` (table `CPM_CYCLE_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| CPM_CYCLE_TBL | PROCESS_NAME | upd_DFAS_HEADER_TABLE.PROCESS_NAME → exp_Increment_Cycle_ID.PROCESS_NAME → exp_Format_Lookup_Current_PAY_PERIOD.PROCESS_NAME → SQ_CPM_CYCLE_TBL.PROCESS_NAME → CPM_CYCLE_TBL1.PROCESS_NAME | CPM_CYCLE_TBL1.PROCESS_NAME |
| CPM_CYCLE_TBL | PP_END_YEAR | upd_DFAS_HEADER_TABLE.PP_END_YEAR → exp_Increment_Cycle_ID.lkp_PP_END_YEAR → lkp_PAY_PERIOD.PP_END_YEAR [lookup PAY_PERIOD.PP_END_YEAR ON PP_END_YEAR = in_PARAM_PP_END_YEAR AND PP_NUM = in_PARAM_PP_NUM] | PAY_PERIOD.PP_END_YEAR (lookup); literal/expression: $$MAP_PP_END_YEAR (lookup key); literal/expression: $$MAP_PP_NUM (lookup key) |
| CPM_CYCLE_TBL | PP_NUM | upd_DFAS_HEADER_TABLE.PP_NUM → exp_Increment_Cycle_ID.lkp_PP_NUM → lkp_PAY_PERIOD.PP_NUM [lookup PAY_PERIOD.PP_NUM ON PP_END_YEAR = in_PARAM_PP_END_YEAR AND PP_NUM = in_PARAM_PP_NUM] | PAY_PERIOD.PP_NUM (lookup); literal/expression: $$MAP_PP_END_YEAR (lookup key); literal/expression: $$MAP_PP_NUM (lookup key) |
| CPM_CYCLE_TBL | PP_END_DTE | upd_DFAS_HEADER_TABLE.PP_END_DTE → exp_Increment_Cycle_ID.lkp_PP_END_DTE → lkp_PAY_PERIOD.PP_END_DTE [lookup PAY_PERIOD.PP_END_DTE ON PP_END_YEAR = in_PARAM_PP_END_YEAR AND PP_NUM = in_PARAM_PP_NUM] | PAY_PERIOD.PP_END_DTE (lookup); literal/expression: $$MAP_PP_END_YEAR (lookup key); literal/expression: $$MAP_PP_NUM (lookup key) |
| CPM_CYCLE_TBL | CYCLE_ID | upd_DFAS_HEADER_TABLE.CYCLE_ID → exp_Increment_Cycle_ID.o_CYCLE_ID = v_CYCLE_ID --IIF(v_NEW_PP_FLAG = TRUE, --then --0, --else --CYCLE_ID + 1) → exp_Increment_Cycle_ID.v_CYCLE_ID = IIF(v_NEW_PP_FLAG = TRUE, --then 0, --else CYCLE_ID + 1) → exp_Increment_Cycle_ID.v_NEW_PP_FLAG = IIF(PP_END_DTE ^= lkp_PP_END_DTE,TRUE,FALSE) → exp_Format_Lookup_Current_PAY_PERIOD.PP_END_DTE → SQ_CPM_CYCLE_TBL.PP_END_DTE → CPM_CYCLE_TBL1.PP_END_DTE → lkp_PAY_PERIOD.PP_END_DTE [lookup PAY_PERIOD.PP_END_DTE ON PP_END_YEAR = in_PARAM_PP_END_YEAR AND PP_NUM = in_PARAM_PP_NUM] → exp_Format_Lookup_Current_PAY_PERIOD.CYCLE_ID → SQ_CPM_CYCLE_TBL.CYCLE_ID → CPM_CYCLE_TBL1.CYCLE_ID | CPM_CYCLE_TBL1.CYCLE_ID; CPM_CYCLE_TBL1.PP_END_DTE; PAY_PERIOD.PP_END_DTE (lookup); literal/expression: $$MAP_PP_END_YEAR (lookup key); literal/expression: $$MAP_PP_NUM (lookup key) |

## Mapping `m_0100_PM_FDA_Load_TATRAN_To_DB`

- Sessions: `s_0100_PM_FDA_Load_TATRAN_To_DB` (#5)
- Sources: `HI_PM_FDA_TATRAN_FLAT`
- Target instances: `HI_PM_FDA_TATRAN_TBL`

### Transformation `SQ_HI_PM_FDA_TATRAN_FLAT` (Source Qualifier)

- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `fil_Filter_Out_01_99` (Filter)

- **Filter Condition**: `IIF(FDA_REC_TYPE ^= '01' AND FDA_REC_TYPE ^= '99' ,TRUE )`

### Transformation `srt_Sort_By_BATCH_SEQ` (Sorter)

- **Case Sensitive**: `YES`
- **Distinct**: `NO`
- **Null Treated Low**: `NO`

- Target instance `HI_PM_FDA_TATRAN_TBL`: Post SQL=`delete from HI_PM_FDA_TATRAN_TBL where fda_emp_id not in (select distinct(fda_emp_id) from HI_PM_FDA_TATRAN_TBL where fda_rec_type = '12')`
- Sorter `srt_Sort_By_BATCH_SEQ` keys: FDA_BATCH_ID ASCENDING, FDA_TK_NO ASCENDING, FDA_EMP_ID ASCENDING, FDA_PP_YEAR ASCENDING, FDA_PP_NUM ASCENDING, FDA_REC_TYPE ASCENDING, FDA_SEQ ASCENDING; distinct=NO

### Target instance `HI_PM_FDA_TATRAN_TBL` (table `HI_PM_FDA_TATRAN_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| HI_PM_FDA_TATRAN_TBL | FDA_BATCH_ID | srt_Sort_By_BATCH_SEQ.FDA_BATCH_ID → exp_Add_FDA_SEQ.FDA_BATCH_SEQ = v_FDA_BATCH_SEQ → exp_Add_FDA_SEQ.v_FDA_BATCH_SEQ = IIF(v_CURR_BATCH_KEY ^= v_PREV_BATCH_KEY, v_FDA_BATCH_SEQ +1, --- ELSE OLD KEY v_FDA_BATCH_SEQ) → exp_Add_FDA_SEQ.v_CURR_BATCH_KEY = FDA_TK_NO \|\|FDA_EMP_ID \|\|FDA_PP_YEAR \|\|FDA_PP_NUM → fil_Filter_Out_01_99.FDA_TK_NO → SQ_HI_PM_FDA_TATRAN_FLAT.FDA_TK_NO → HI_PM_FDA_TATRAN_FLAT.FDA_TK_NO → fil_Filter_Out_01_99.FDA_EMP_ID → SQ_HI_PM_FDA_TATRAN_FLAT.FDA_EMP_ID → HI_PM_FDA_TATRAN_FLAT.FDA_EMP_ID → fil_Filter_Out_01_99.FDA_PP_YEAR → SQ_HI_PM_FDA_TATRAN_FLAT.FDA_PP_YEAR → HI_PM_FDA_TATRAN_FLAT.FDA_PP_YEAR → fil_Filter_Out_01_99.FDA_PP_NUM → SQ_HI_PM_FDA_TATRAN_FLAT.FDA_PP_NUM → HI_PM_FDA_TATRAN_FLAT.FDA_PP_NUM → exp_Add_FDA_SEQ.v_PREV_BATCH_KEY = FDA_TK_NO \|\| FDA_EMP_ID \|\| FDA_PP_YEAR \|\| FDA_PP_NUM | HI_PM_FDA_TATRAN_FLAT.FDA_EMP_ID; HI_PM_FDA_TATRAN_FLAT.FDA_PP_NUM; HI_PM_FDA_TATRAN_FLAT.FDA_PP_YEAR; HI_PM_FDA_TATRAN_FLAT.FDA_TK_NO |
| HI_PM_FDA_TATRAN_TBL | FDA_TK_NO | srt_Sort_By_BATCH_SEQ.FDA_TK_NO → exp_Add_FDA_SEQ.FDA_TK_NO → fil_Filter_Out_01_99.FDA_TK_NO → SQ_HI_PM_FDA_TATRAN_FLAT.FDA_TK_NO → HI_PM_FDA_TATRAN_FLAT.FDA_TK_NO | HI_PM_FDA_TATRAN_FLAT.FDA_TK_NO |
| HI_PM_FDA_TATRAN_TBL | FDA_EMP_ID | srt_Sort_By_BATCH_SEQ.FDA_EMP_ID → exp_Add_FDA_SEQ.FDA_EMP_ID → fil_Filter_Out_01_99.FDA_EMP_ID → SQ_HI_PM_FDA_TATRAN_FLAT.FDA_EMP_ID → HI_PM_FDA_TATRAN_FLAT.FDA_EMP_ID | HI_PM_FDA_TATRAN_FLAT.FDA_EMP_ID |
| HI_PM_FDA_TATRAN_TBL | FDA_PP_YEAR | srt_Sort_By_BATCH_SEQ.FDA_PP_YEAR → exp_Add_FDA_SEQ.FDA_PP_YEAR → fil_Filter_Out_01_99.FDA_PP_YEAR → SQ_HI_PM_FDA_TATRAN_FLAT.FDA_PP_YEAR → HI_PM_FDA_TATRAN_FLAT.FDA_PP_YEAR | HI_PM_FDA_TATRAN_FLAT.FDA_PP_YEAR |
| HI_PM_FDA_TATRAN_TBL | FDA_PP_NUM | srt_Sort_By_BATCH_SEQ.FDA_PP_NUM → exp_Add_FDA_SEQ.FDA_PP_NUM → fil_Filter_Out_01_99.FDA_PP_NUM → SQ_HI_PM_FDA_TATRAN_FLAT.FDA_PP_NUM → HI_PM_FDA_TATRAN_FLAT.FDA_PP_NUM | HI_PM_FDA_TATRAN_FLAT.FDA_PP_NUM |
| HI_PM_FDA_TATRAN_TBL | FDA_REC_TYPE | srt_Sort_By_BATCH_SEQ.FDA_REC_TYPE → exp_Add_FDA_SEQ.FDA_REC_TYPE → fil_Filter_Out_01_99.FDA_REC_TYPE → SQ_HI_PM_FDA_TATRAN_FLAT.FDA_REC_TYPE → HI_PM_FDA_TATRAN_FLAT.FDA_REC_TYPE | HI_PM_FDA_TATRAN_FLAT.FDA_REC_TYPE |
| HI_PM_FDA_TATRAN_TBL | FDA_SEQ | srt_Sort_By_BATCH_SEQ.FDA_SEQ → exp_Add_FDA_SEQ.FDA_SEQ = v_FDA_SEQ → exp_Add_FDA_SEQ.v_FDA_SEQ = IIF(ISNULL(v_FDA_SEQ), 1, --ELSE v_FDA_SEQ +1) | literal/expression: IIF(ISNULL(v_FDA_SEQ), 1, --ELSE v_FDA_SEQ +1) |
| HI_PM_FDA_TATRAN_TBL | FDA_DATA | srt_Sort_By_BATCH_SEQ.FDA_DATA → exp_Add_FDA_SEQ.FDA_DATA → fil_Filter_Out_01_99.FDA_DATA → SQ_HI_PM_FDA_TATRAN_FLAT.FDA_DATA → HI_PM_FDA_TATRAN_FLAT.FDA_DATA | HI_PM_FDA_TATRAN_FLAT.FDA_DATA |

## Mapping `m_0150_PM_FDA_Error_Counter`

- Sessions: `s_0150_PM_FDA_Error_Counter` (#6)
- Sources: `HI_PM_FDA_TATRAN_TBL11`
- Target instances: `ERROR_TBL_CPM`, `ERROR_TBL_MER`, `ERROR_TBL_PAD`, `ERROR_TBL_YTD`

### Transformation `SQ_HI_PM_FDA_TATRAN_TBL11` (Source Qualifier)

- **Source Filter**: `HI_PM_FDA_TATRAN_TBL.FDA_REC_TYPE = '02'`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `fil_Errors_CPM` (Filter)

- **Filter Condition**: `IIF(ISNULL(SOC_SEC_NO) ,TRUE, FALSE)`

### Transformation `fil_Errors_MER` (Filter)

- **Filter Condition**: `IIF(ISNULL(MER_SSN) ,TRUE, FALSE)`

### Transformation `fil_Errors_PAD` (Filter)

- **Filter Condition**: `IIF(ISNULL(PAD_SOC_SEC_NO) ,TRUE, FALSE)`

### Transformation `fil_Errors_YTD` (Filter)

- **Filter Condition**: `IIF(ISNULL(DYD_SSN_1) ,TRUE, FALSE)`

### Transformation `lkp_CPM_MER_DETAIL_STG_TBL` (Lookup Procedure)

- **Lookup table name**: `CPM_MER_DETAIL_STG_TBL`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `MER_SSN = lkp_FDA_EMP_ID AND PP_END_YEAR = lkp_CURR_PP_END_YEAR AND PP_NUM = lkp_CURR_PP_NUM`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `lkp_CPM_NEWPAY_TBL` (Lookup Procedure)

- **Lookup table name**: `CPM_NEWPAY_TBL`
- **Lookup Source Filter**: `PP_END_YEAR = TO_NUMBER('$$MAP_PP_END_YEAR') AND PP_NUM = TO_NUMBER('$$MAP_PP_NUM')`
- **Lookup policy on multiple match**: `Use First Value`
- **Lookup condition**: `PP_END_YEAR = lkp_PP_END_YEAR AND PP_NUM = lkp_PP_NUM AND DFAS_PSEUDO_SSN = lkp_FDA_EMP_ID`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `lkp_CPM_PAD_DETAIL_STG_TBL` (Lookup Procedure)

- **Lookup table name**: `CPM_PAD_DETAIL_STG_TBL`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `PP_END_YEAR = lkp_PP_END_YEAR AND PP_NUM = lkp_PP_PP_NUM AND PAD_SOC_SEC_NO = lkp_FDA_EMP_ID`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `lkp_CPM_YTD_DETAIL_STG_TBL` (Lookup Procedure)

- **Lookup table name**: `CPM_YTD_DETAIL_STG_TBL`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `PP_END_YEAR = lkp_PP_END_YEAR AND PP_NUM = lkp_PP_NUM AND DYD_SSN_1 = lkp_FDA_EMP_ID`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `lkp_PAY_PERIOD11` (Lookup Procedure)

- **Lookup table name**: `PAY_PERIOD`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `CURR_PP_FLAG = lkp_CURR_PP_FLAG`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

- Lookup `lkp_CPM_MER_DETAIL_STG_TBL`: table `CPM_MER_DETAIL_STG_TBL` (exists in export: **False**), condition `MER_SSN = lkp_FDA_EMP_ID AND PP_END_YEAR = lkp_CURR_PP_END_YEAR AND PP_NUM = lkp_CURR_PP_NUM`, multiple-match policy `Use Any Value`.
- Lookup `lkp_CPM_NEWPAY_TBL`: table `CPM_NEWPAY_TBL` (exists in export: **False**), condition `PP_END_YEAR = lkp_PP_END_YEAR AND PP_NUM = lkp_PP_NUM AND DFAS_PSEUDO_SSN = lkp_FDA_EMP_ID`, multiple-match policy `Use First Value`.
- Lookup `lkp_CPM_PAD_DETAIL_STG_TBL`: table `CPM_PAD_DETAIL_STG_TBL` (exists in export: **False**), condition `PP_END_YEAR = lkp_PP_END_YEAR AND PP_NUM = lkp_PP_PP_NUM AND PAD_SOC_SEC_NO = lkp_FDA_EMP_ID`, multiple-match policy `Use Any Value`.
- Lookup `lkp_CPM_YTD_DETAIL_STG_TBL`: table `CPM_YTD_DETAIL_STG_TBL` (exists in export: **False**), condition `PP_END_YEAR = lkp_PP_END_YEAR AND PP_NUM = lkp_PP_NUM AND DYD_SSN_1 = lkp_FDA_EMP_ID`, multiple-match policy `Use Any Value`.
- Lookup `lkp_PAY_PERIOD11`: table `PAY_PERIOD` (exists in export: **True**), condition `CURR_PP_FLAG = lkp_CURR_PP_FLAG`, multiple-match policy `Use Any Value`.

### Target instance `ERROR_TBL_CPM` (table `ERROR_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| ERROR_TBL_CPM | PROCESS_NAME | exp_Format_CPM.PROCESS_NAME = $PMMappingName | literal/expression: $PMMappingName |
| ERROR_TBL_CPM | ERROR_MESSAGE | exp_Format_CPM.ERR_DESC = 'DOES NOT HAVE A PAYMASTER RECORD' | literal/expression: 'DOES NOT HAVE A PAYMASTER RECORD' |
| ERROR_TBL_CPM | SOURCE_KEY | exp_Format_CPM.ERR_EMPL_ID = lkp_FDA_EMP_ID → fil_Errors_CPM.lkp_FDA_EMP_ID → lkp_CPM_NEWPAY_TBL.lkp_FDA_EMP_ID → exp_Format_Get_Current_PP11.lkp_FDA_EMP_ID → SQ_HI_PM_FDA_TATRAN_TBL11.FDA_EMP_ID → HI_PM_FDA_TATRAN_TBL11.FDA_EMP_ID | HI_PM_FDA_TATRAN_TBL11.FDA_EMP_ID |
| ERROR_TBL_CPM | ERROR_DATE | exp_Format_CPM.ERR_TS = SESSSTARTTIME | literal/expression: SESSSTARTTIME |
| ERROR_TBL_CPM | PP_END_YEAR | exp_Format_CPM.ERR_PP_END_YEAR = lkp_CURR_PP_END_YEAR → fil_Errors_CPM.lkp_CURR_PP_END_YEAR → lkp_CPM_NEWPAY_TBL.lkp_PP_END_YEAR → exp_Format_Get_Current_PP11.o_PP_END_YEAR = TO_DECIMAL($$MAP_PP_END_YEAR, 0) | literal/expression: TO_DECIMAL($$MAP_PP_END_YEAR, 0) |
| ERROR_TBL_CPM | PP_NUM | exp_Format_CPM.ERR_PP_NUM = lkp_CURR_PP_NUM → fil_Errors_CPM.lkp_CURR_PP_NUM → lkp_CPM_NEWPAY_TBL.lkp_PP_NUM → exp_Format_Get_Current_PP11.o_PP_NUM = TO_DECIMAL($$MAP_PP_NUM, 0) | literal/expression: TO_DECIMAL($$MAP_PP_NUM, 0) |
| ERROR_TBL_CPM | CYCLE_ID | exp_Format_CPM.ERR_CYCLE_ID = lkp_CYCLE_ID → fil_Errors_CPM.lkp_CYCLE_ID → lkp_CPM_NEWPAY_TBL.lkp_CYCLE_ID → exp_Format_Get_Current_PP11.o_CYCLE_ID = $$MAP_CYCLE_ID | literal/expression: $$MAP_CYCLE_ID |
| ERROR_TBL_CPM | ERROR_CODE | (not connected — NULL) | — |

### Target instance `ERROR_TBL_MER` (table `ERROR_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| ERROR_TBL_MER | PROCESS_NAME | exp_Format_MER.PROCESS_NAME = $PMMappingName | literal/expression: $PMMappingName |
| ERROR_TBL_MER | ERROR_MESSAGE | exp_Format_MER.ERR_DESC = 'DOES NOT HAVE A MER RECORD (P6722D01)' | literal/expression: 'DOES NOT HAVE A MER RECORD (P6722D01)' |
| ERROR_TBL_MER | SOURCE_KEY | exp_Format_MER.ERR_EMPL_ID = lkp_FDA_EMP_ID → fil_Errors_MER.lkp_FDA_EMP_ID → lkp_CPM_MER_DETAIL_STG_TBL.lkp_FDA_EMP_ID → exp_Format_Get_Current_PP11.lkp_FDA_EMP_ID → SQ_HI_PM_FDA_TATRAN_TBL11.FDA_EMP_ID → HI_PM_FDA_TATRAN_TBL11.FDA_EMP_ID | HI_PM_FDA_TATRAN_TBL11.FDA_EMP_ID |
| ERROR_TBL_MER | ERROR_DATE | exp_Format_MER.ERR_TS = SESSSTARTTIME | literal/expression: SESSSTARTTIME |
| ERROR_TBL_MER | PP_END_YEAR | exp_Format_MER.ERR_PP_END_YEAR = lkp_CURR_PP_END_YEAR → fil_Errors_MER.lkp_CURR_PP_END_YEAR → lkp_CPM_MER_DETAIL_STG_TBL.lkp_CURR_PP_END_YEAR → exp_Format_Get_Current_PP11.o_PP_END_YEAR = TO_DECIMAL($$MAP_PP_END_YEAR, 0) | literal/expression: TO_DECIMAL($$MAP_PP_END_YEAR, 0) |
| ERROR_TBL_MER | PP_NUM | exp_Format_MER.ERR_PP_NUM = lkp_CURR_PP_NUM → fil_Errors_MER.lkp_CURR_PP_NUM → lkp_CPM_MER_DETAIL_STG_TBL.lkp_CURR_PP_NUM → exp_Format_Get_Current_PP11.o_PP_NUM = TO_DECIMAL($$MAP_PP_NUM, 0) | literal/expression: TO_DECIMAL($$MAP_PP_NUM, 0) |
| ERROR_TBL_MER | CYCLE_ID | exp_Format_MER.ERR_CYCLE_ID = lkp_CYCLE_ID → fil_Errors_MER.lkp_CYCLE_ID → lkp_CPM_MER_DETAIL_STG_TBL.lkp_CYCLE_ID → exp_Format_Get_Current_PP11.o_CYCLE_ID = $$MAP_CYCLE_ID | literal/expression: $$MAP_CYCLE_ID |
| ERROR_TBL_MER | ERROR_CODE | (not connected — NULL) | — |

### Target instance `ERROR_TBL_PAD` (table `ERROR_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| ERROR_TBL_PAD | PROCESS_NAME | exp_Format_PAD.PROCESS_NAME = $PMMappingName | literal/expression: $PMMappingName |
| ERROR_TBL_PAD | ERROR_MESSAGE | exp_Format_PAD.ERR_DESC = 'DOES NOT HAVE A PAD RECORD (P6331X01)' | literal/expression: 'DOES NOT HAVE A PAD RECORD (P6331X01)' |
| ERROR_TBL_PAD | SOURCE_KEY | exp_Format_PAD.ERR_EMPL_ID = lkp_FDA_EMP_ID → fil_Errors_PAD.lkp_FDA_EMP_ID → lkp_CPM_PAD_DETAIL_STG_TBL.lkp_FDA_EMP_ID → exp_Format_Get_Current_PP11.lkp_FDA_EMP_ID → SQ_HI_PM_FDA_TATRAN_TBL11.FDA_EMP_ID → HI_PM_FDA_TATRAN_TBL11.FDA_EMP_ID | HI_PM_FDA_TATRAN_TBL11.FDA_EMP_ID |
| ERROR_TBL_PAD | ERROR_DATE | exp_Format_PAD.ERR_TS = SESSSTARTTIME | literal/expression: SESSSTARTTIME |
| ERROR_TBL_PAD | PP_END_YEAR | exp_Format_PAD.ERR_PP_END_YEAR = lkp_CURR_PP_END_YEAR → fil_Errors_PAD.lkp_CURR_PP_END_YEAR → lkp_CPM_PAD_DETAIL_STG_TBL.lkp_PP_END_YEAR → exp_Format_Get_Current_PP11.o_PP_END_YEAR = TO_DECIMAL($$MAP_PP_END_YEAR, 0) | literal/expression: TO_DECIMAL($$MAP_PP_END_YEAR, 0) |
| ERROR_TBL_PAD | PP_NUM | exp_Format_PAD.ERR_PP_NUM = lkp_CURR_PP_NUM → fil_Errors_PAD.lkp_CURR_PP_NUM → lkp_CPM_PAD_DETAIL_STG_TBL.lkp_PP_PP_NUM → exp_Format_Get_Current_PP11.o_PP_NUM = TO_DECIMAL($$MAP_PP_NUM, 0) | literal/expression: TO_DECIMAL($$MAP_PP_NUM, 0) |
| ERROR_TBL_PAD | CYCLE_ID | exp_Format_PAD.ERR_CYCLE_ID = lkp_CYCLE_ID → fil_Errors_PAD.lkp_CYCLE_ID → lkp_CPM_PAD_DETAIL_STG_TBL.lkp_CYCLE_ID → exp_Format_Get_Current_PP11.o_CYCLE_ID = $$MAP_CYCLE_ID | literal/expression: $$MAP_CYCLE_ID |
| ERROR_TBL_PAD | ERROR_CODE | (not connected — NULL) | — |

### Target instance `ERROR_TBL_YTD` (table `ERROR_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| ERROR_TBL_YTD | PROCESS_NAME | exp_Format_YTD.PROCESS_NAME = $PMMappingName | literal/expression: $PMMappingName |
| ERROR_TBL_YTD | ERROR_MESSAGE | exp_Format_YTD.ERR_DESC = 'DOES NOT HAVE A YTD RECORD (P6791X01)' | literal/expression: 'DOES NOT HAVE A YTD RECORD (P6791X01)' |
| ERROR_TBL_YTD | SOURCE_KEY | exp_Format_YTD.ERR_EMPL_ID = lkp_FDA_EMP_ID → fil_Errors_YTD.lkp_FDA_EMP_ID → lkp_CPM_YTD_DETAIL_STG_TBL.lkp_FDA_EMP_ID → exp_Format_Get_Current_PP11.lkp_FDA_EMP_ID → SQ_HI_PM_FDA_TATRAN_TBL11.FDA_EMP_ID → HI_PM_FDA_TATRAN_TBL11.FDA_EMP_ID | HI_PM_FDA_TATRAN_TBL11.FDA_EMP_ID |
| ERROR_TBL_YTD | ERROR_DATE | exp_Format_YTD.ERR_TS = SESSSTARTTIME | literal/expression: SESSSTARTTIME |
| ERROR_TBL_YTD | PP_END_YEAR | exp_Format_YTD.ERR_PP_END_YEAR = lkp_CURR_PP_END_YEAR → fil_Errors_YTD.lkp_CURR_PP_END_YEAR → lkp_CPM_YTD_DETAIL_STG_TBL.lkp_PP_END_YEAR → exp_Format_Get_Current_PP11.o_PP_END_YEAR = TO_DECIMAL($$MAP_PP_END_YEAR, 0) | literal/expression: TO_DECIMAL($$MAP_PP_END_YEAR, 0) |
| ERROR_TBL_YTD | PP_NUM | exp_Format_YTD.ERR_PP_NUM = lkp_CURR_PP_NUM → fil_Errors_YTD.lkp_CURR_PP_NUM → lkp_CPM_YTD_DETAIL_STG_TBL.lkp_PP_NUM → exp_Format_Get_Current_PP11.o_PP_NUM = TO_DECIMAL($$MAP_PP_NUM, 0) | literal/expression: TO_DECIMAL($$MAP_PP_NUM, 0) |
| ERROR_TBL_YTD | CYCLE_ID | exp_Format_YTD.ERR_CYCLE_ID = lkp_CYCLE_ID → fil_Errors_YTD.lkp_CYCLE_ID → lkp_CPM_YTD_DETAIL_STG_TBL.lkp_CYCLE_ID → exp_Format_Get_Current_PP11.o_CYCLE_ID = $$MAP_CYCLE_ID | literal/expression: $$MAP_CYCLE_ID |
| ERROR_TBL_YTD | ERROR_CODE | (not connected — NULL) | — |

## Mapping `m_0200_PM_FDA_Create_Insert_200_Rows`

- Sessions: `s_0200_PM_FDA_Create_200_Rows` (#7)
- Sources: `HI_PM_FDA_TATRAN_TBL`
- Target instances: `HI_PM_FDA_TATRAN_TBL1`

### Transformation `SQ_HI_PM_FDA_TATRAN_TBL` (Source Qualifier)

- **Source Filter**: `HI_PM_FDA_TATRAN_TBL.FDA_REC_TYPE = '02'`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `fil_Filter_Out_NULL` (Filter)

- **Filter Condition**: `IIF( ISNULL(MER_SSN) AND ISNULL(PAD_SOC_SEC_NO) AND ISNULL(DYD_SSN_1) AND ISNULL(PYF_EYE_ID_1) ,FALSE,TRUE)`

### Transformation `lkp_CPM_MER_DETAIL_STG_TBL` (Lookup Procedure)

- **Lookup table name**: `CPM_MER_DETAIL_STG_TBL`
- **Lookup Source Filter**: `SUBSTR(MER_ORG,1,1) = 'D'`
- **Lookup policy on multiple match**: `Use First Value`
- **Lookup condition**: `PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `lkp_CPM_NEWPAY_TBL` (Lookup Procedure)

- **Lookup table name**: `CPM_NEWPAY_TBL`
- **Lookup Source Filter**: `PP_END_YEAR = TO_NUMBER('$$MAP_PP_END_YEAR') AND PP_NUM = TO_NUMBER('$$MAP_PP_NUM')`
- **Lookup policy on multiple match**: `Use First Value`
- **Lookup condition**: `PP_END_YEAR = lkp_PP_END_YEAR AND PP_NUM = lkp_PP_NUM AND DFAS_PSEUDO_SSN = lkp_FDA_EMP_ID`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `lkp_CPM_PAD_DETAIL_STG_TBL` (Lookup Procedure)

- **Lookup table name**: `CPM_PAD_DETAIL_STG_TBL`
- **Lookup Source Filter**: `SUBSTR(PAD_ORGANIZATION,1,1) = 'D'`
- **Lookup policy on multiple match**: `Use First Value`
- **Lookup condition**: `PP_END_YEAR = lkp_PP_END_YEAR AND PP_NUM = lkp_PP_NUM AND PAD_SOC_SEC_NO = lkp_FDA_EMP_ID`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `lkp_CPM_YTD_DETAIL_STG_TBL` (Lookup Procedure)

- **Lookup table name**: `CPM_YTD_DETAIL_STG_TBL`
- **Lookup Source Filter**: `SUBSTR(DYD_ACTIVITY,1,1) = 'D'`
- **Lookup policy on multiple match**: `Use First Value`
- **Lookup condition**: `PP_END_YEAR = lkp_PP_END_YEAR AND PP_NUM = lkp_PP_NUM AND DYD_SSN_1 = lkp_FDA_EMP_ID`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `lkp_PAY_PERIOD` (Lookup Procedure)

- **Lookup table name**: `PAY_PERIOD`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `CURR_PP_FLAG = lkp_CURR_PP_FLAG`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `lkp_PSEUDOSSN` (Lookup Procedure)

- **Lookup table name**: `PSEUDOSSN_TBL`
- **Lookup policy on multiple match**: `Use First Value`
- **Lookup condition**: `PSEUDOSSN = lkp_FDA_EMP_ID`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `nrm_Normalize_200_Records` (Normalizer)

- **Reset**: `NO`
- **Restart**: `NO`

- Normalizer `nrm_Normalize_200_Records` (vsam=False) occurs: FDA_DATA×14, FDA_SEQ×14; generated: GK_FDA_DATA, GCID_FDA_DATA, GCID_FDA_SEQ
- Lookup `lkp_CPM_MER_DETAIL_STG_TBL`: table `CPM_MER_DETAIL_STG_TBL` (exists in export: **False**), condition `PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID`, multiple-match policy `Use First Value`.
- Lookup `lkp_CPM_NEWPAY_TBL`: table `CPM_NEWPAY_TBL` (exists in export: **False**), condition `PP_END_YEAR = lkp_PP_END_YEAR AND PP_NUM = lkp_PP_NUM AND DFAS_PSEUDO_SSN = lkp_FDA_EMP_ID`, multiple-match policy `Use First Value`.
- Lookup `lkp_CPM_PAD_DETAIL_STG_TBL`: table `CPM_PAD_DETAIL_STG_TBL` (exists in export: **False**), condition `PP_END_YEAR = lkp_PP_END_YEAR AND PP_NUM = lkp_PP_NUM AND PAD_SOC_SEC_NO = lkp_FDA_EMP_ID`, multiple-match policy `Use First Value`.
- Lookup `lkp_CPM_YTD_DETAIL_STG_TBL`: table `CPM_YTD_DETAIL_STG_TBL` (exists in export: **False**), condition `PP_END_YEAR = lkp_PP_END_YEAR AND PP_NUM = lkp_PP_NUM AND DYD_SSN_1 = lkp_FDA_EMP_ID`, multiple-match policy `Use First Value`.
- Lookup `lkp_PAY_PERIOD`: table `PAY_PERIOD` (exists in export: **True**), condition `CURR_PP_FLAG = lkp_CURR_PP_FLAG`, multiple-match policy `Use Any Value`.
- Lookup `lkp_PSEUDOSSN`: table `PSEUDOSSN_TBL` (exists in export: **False**), condition `PSEUDOSSN = lkp_FDA_EMP_ID`, multiple-match policy `Use First Value`.

### Target instance `HI_PM_FDA_TATRAN_TBL1` (table `HI_PM_FDA_TATRAN_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| HI_PM_FDA_TATRAN_TBL1 | FDA_BATCH_ID | nrm_Normalize_200_Records.FDA_BATCH_ID [normalizer: one row per occurrence of FDA_BATCH_ID_in] → exp_Format_200_Records.FDA_BATCH_ID → fil_Filter_Out_NULL.FDA_BATCH_ID → SQ_HI_PM_FDA_TATRAN_TBL.FDA_BATCH_ID → HI_PM_FDA_TATRAN_TBL.FDA_BATCH_ID | HI_PM_FDA_TATRAN_TBL.FDA_BATCH_ID |
| HI_PM_FDA_TATRAN_TBL1 | FDA_TK_NO | nrm_Normalize_200_Records.FDA_TK_NO [normalizer: one row per occurrence of FDA_TK_NO_in] → exp_Format_200_Records.FDA_TK_NO → fil_Filter_Out_NULL.FDA_TK_NO → SQ_HI_PM_FDA_TATRAN_TBL.FDA_TK_NO → HI_PM_FDA_TATRAN_TBL.FDA_TK_NO | HI_PM_FDA_TATRAN_TBL.FDA_TK_NO |
| HI_PM_FDA_TATRAN_TBL1 | FDA_EMP_ID | nrm_Normalize_200_Records.FDA_EMP_ID [normalizer: one row per occurrence of FDA_EMP_ID_in] → lkp_PSEUDOSSN.SSN [lookup PSEUDOSSN_TBL.SSN ON PSEUDOSSN = lkp_FDA_EMP_ID] | HI_PM_FDA_TATRAN_TBL.FDA_EMP_ID (lookup key); PSEUDOSSN_TBL.SSN (lookup) |
| HI_PM_FDA_TATRAN_TBL1 | FDA_PP_YEAR | nrm_Normalize_200_Records.FDA_PP_YEAR [normalizer: one row per occurrence of FDA_PP_YEAR_in] → exp_Format_200_Records.FDA_PP_YEAR → fil_Filter_Out_NULL.FDA_PP_YEAR → SQ_HI_PM_FDA_TATRAN_TBL.FDA_PP_YEAR → HI_PM_FDA_TATRAN_TBL.FDA_PP_YEAR | HI_PM_FDA_TATRAN_TBL.FDA_PP_YEAR |
| HI_PM_FDA_TATRAN_TBL1 | FDA_PP_NUM | nrm_Normalize_200_Records.FDA_PP_NUM [normalizer: one row per occurrence of FDA_PP_NUM_in] → exp_Format_200_Records.FDA_PP_NUM → fil_Filter_Out_NULL.FDA_PP_NUM → SQ_HI_PM_FDA_TATRAN_TBL.FDA_PP_NUM → HI_PM_FDA_TATRAN_TBL.FDA_PP_NUM | HI_PM_FDA_TATRAN_TBL.FDA_PP_NUM |
| HI_PM_FDA_TATRAN_TBL1 | FDA_REC_TYPE | nrm_Normalize_200_Records.FDA_REC_TYPE [normalizer: one row per occurrence of FDA_REC_TYPE_in] → exp_Format_200_Records.FDA_REC_TYPE = '12' | literal/expression: '12' |
| HI_PM_FDA_TATRAN_TBL1 | FDA_SEQ | nrm_Normalize_200_Records.FDA_SEQ [normalizer: one row per occurrence of FDA_SEQ_in1, FDA_SEQ_in2, FDA_SEQ_in3, FDA_SEQ_in4, FDA_SEQ_in5, FDA_SEQ_in6, FDA_SEQ_in7, FDA_SEQ_in8, FDA_SEQ_in9, FDA_SEQ_in10, FDA_SEQ_in11, FDA_SEQ_in12, FDA_SEQ_in13, FDA_SEQ_in14] → exp_Format_200_Records.FDA_200_SEQ = 1001000 → exp_Format_200_Records.FDA_201_SEQ = 1001001 → exp_Format_200_Records.FDA_202_SEQ = 1001002 → exp_Format_200_Records.FDA_203_SEQ = 1001003 → exp_Format_200_Records.FDA_204_SEQ = 1001004 → exp_Format_200_Records.FDA_205_SEQ = 1001005 → exp_Format_200_Records.FDA_206_SEQ = 1001006 → exp_Format_200_Records.FDA_207_SEQ = 1001007 → exp_Format_200_Records.FDA_208_SEQ = 1001008 → exp_Format_200_Records.FDA_209_SEQ = 1001009 → exp_Format_200_Records.FDA_211_SEQ = 1001011 → exp_Format_200_Records.FDA_212_SEQ = 1001012 → exp_Format_200_Records.FDA_214_SEQ = 1001014 → exp_Format_200_Records.FDA_215_SEQ = 1001015 | literal/expression: 1001000; literal/expression: 1001001; literal/expression: 1001002; literal/expression: 1001003; literal/expression: 1001004; literal/expression: 1001005; literal/expression: 1001006; literal/expression: 1001007; literal/expression: 1001008; literal/expression: 1001009; literal/expression: 1001011; literal/expression: 1001012; literal/expression: 1001014; literal/expression: 1001015 |
| HI_PM_FDA_TATRAN_TBL1 | FDA_DATA | nrm_Normalize_200_Records.FDA_DATA [normalizer: one row per occurrence of FDA_DATA_in1, FDA_DATA_in2, FDA_DATA_in3, FDA_DATA_in4, FDA_DATA_in5, FDA_DATA_in6, FDA_DATA_in7, FDA_DATA_in8, FDA_DATA_in9, FDA_DATA_in10, FDA_DATA_in11, FDA_DATA_in12, FDA_DATA_in13, FDA_DATA_in14] → exp_Format_200_Records.FDA_200_DATA = '200\|'\|\| v_MER_ANN_LV_ACCRUAL_RT \|\| '\|' \|\| v_MER_ANN_LV_ACCRD_YTD \|\| '\|' \|\| v_MER_ANN_LV_ENDBAL \|\| '\|' \|\| v_MER_ANN_LV_USED_YTD \|\| '\|' \|\| v_MER_ANN_LV_BEGBAL \|\| '\|' \|\| v_MER_ANN_LV_CEILING \|\| '\|' \|\| v_MER_ANN_LV_USED_PAY_PD \|\| '\|' → exp_Format_200_Records.v_MER_ANN_LV_ACCRUAL_RT = DECODE(TRUE, ISNULL(MER_ANN_LV_ACCRUAL_RT),'+000.00', --ELSE MER_ANN_LV_ACCRUAL_RT < 0,'-' \|\| LPAD(TO_DECIMAL(MER_ANN_LV_ACCRUAL_RT * -1,2),6,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_ANN_LV_ACCRUAL_RT,2),6,'0') ) → fil_Filter_Out_NULL.MER_ANN_LV_ACCRUAL_RT → lkp_CPM_MER_DETAIL_STG_TBL.MER_ANN_LV_ACCRUAL_RT [lookup CPM_MER_DETAIL_STG_TBL.MER_ANN_LV_ACCRUAL_RT ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_ANN_LV_ACCRD_YTD = DECODE(TRUE, ISNULL(MER_ANN_LV_ACCRD_YTD),'+00000.00', --ELSE MER_ANN_LV_ACCRD_YTD < 0,'-' \|\| LPAD(TO_DECIMAL(MER_ANN_LV_ACCRD_YTD * -1,2),8,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_ANN_LV_ACCRD_YTD,2),8,'0') ) → fil_Filter_Out_NULL.MER_ANN_LV_ACCRD_YTD → lkp_CPM_MER_DETAIL_STG_TBL.MER_ANN_LV_ACCRD_YTD [lookup CPM_MER_DETAIL_STG_TBL.MER_ANN_LV_ACCRD_YTD ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_ANN_LV_ENDBAL = DECODE(TRUE, ISNULL(MER_ANN_LV_ENDBAL),'+00000.00', --ELSE MER_ANN_LV_ENDBAL < 0,'-' \|\| LPAD(TO_DECIMAL(MER_ANN_LV_ENDBAL * -1,2),8,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_ANN_LV_ENDBAL,2),8,'0') ) → fil_Filter_Out_NULL.MER_ANN_LV_ENDBAL → lkp_CPM_MER_DETAIL_STG_TBL.MER_ANN_LV_ENDBAL [lookup CPM_MER_DETAIL_STG_TBL.MER_ANN_LV_ENDBAL ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_ANN_LV_USED_YTD = DECODE(TRUE, ISNULL(MER_ANN_LV_USED_YTD),'+00000.00', --ELSE MER_ANN_LV_USED_YTD < 0,'-' \|\| LPAD(TO_DECIMAL(MER_ANN_LV_USED_YTD * -1,2),8,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_ANN_LV_USED_YTD,2),8,'0') ) → fil_Filter_Out_NULL.MER_ANN_LV_USED_YTD → lkp_CPM_MER_DETAIL_STG_TBL.MER_ANN_LV_USED_YTD [lookup CPM_MER_DETAIL_STG_TBL.MER_ANN_LV_USED_YTD ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_ANN_LV_BEGBAL = DECODE(TRUE, ISNULL(MER_ANN_LV_BEGBAL),'+00000.00', --ELSE MER_ANN_LV_BEGBAL < 0,'-' \|\| LPAD(TO_DECIMAL(MER_ANN_LV_BEGBAL * -1,2),8,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_ANN_LV_BEGBAL,2),8,'0') ) → fil_Filter_Out_NULL.MER_ANN_LV_BEGBAL → lkp_CPM_MER_DETAIL_STG_TBL.MER_ANN_LV_BEGBAL [lookup CPM_MER_DETAIL_STG_TBL.MER_ANN_LV_BEGBAL ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_ANN_LV_CEILING = DECODE(TRUE, ISNULL(MER_ANN_LV_CEILING),'+00000.00', --ELSE MER_ANN_LV_CEILING < 0,'-' \|\| LPAD(TO_DECIMAL(MER_ANN_LV_CEILING * -1,2),8,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_ANN_LV_CEILING,2),8,'0') ) → fil_Filter_Out_NULL.MER_ANN_LV_CEILING → lkp_CPM_MER_DETAIL_STG_TBL.MER_ANN_LV_CEILING [lookup CPM_MER_DETAIL_STG_TBL.MER_ANN_LV_CEILING ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_ANN_LV_USED_PAY_PD = DECODE(TRUE, ISNULL(MER_ANN_LV_USED_PAY_PD),'+000.00', --ELSE MER_ANN_LV_USED_PAY_PD < 0,'-' \|\| LPAD(TO_DECIMAL(MER_ANN_LV_USED_PAY_PD * -1,2),6,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_ANN_LV_USED_PAY_PD,2),6,'0') ) → fil_Filter_Out_NULL.MER_ANN_LV_USED_PAY_PD → lkp_CPM_MER_DETAIL_STG_TBL.MER_ANN_LV_USED_PAY_PD [lookup CPM_MER_DETAIL_STG_TBL.MER_ANN_LV_USED_PAY_PD ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.FDA_201_DATA = '201\|'\|\| v_MER_RSTRD_ANN_LV_ENDBAL_1 \|\| '\|' \|\| v_MER_RSTRD_ANN_LV_ENDBAL_2 \|\| '\|' \|\| v_MER_RSTRD_ANN_LV_ENDBAL_3 \|\| '\|' → exp_Format_200_Records.v_MER_RSTRD_ANN_LV_ENDBAL_1 = DECODE(TRUE, ISNULL(MER_RSTRD_ANN_LV_ENDBAL_1),'+000.00', --ELSE MER_RSTRD_ANN_LV_ENDBAL_1 < 0,'-' \|\| LPAD(TO_DECIMAL(MER_RSTRD_ANN_LV_ENDBAL_1 * -1,2),6,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_RSTRD_ANN_LV_ENDBAL_1,2),6,'0') ) → fil_Filter_Out_NULL.MER_RSTRD_ANN_LV_ENDBAL_1 → lkp_CPM_MER_DETAIL_STG_TBL.MER_RSTRD_ANN_LV_ENDBAL_1 [lookup CPM_MER_DETAIL_STG_TBL.MER_RSTRD_ANN_LV_ENDBAL_1 ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_RSTRD_ANN_LV_ENDBAL_2 = DECODE(TRUE, ISNULL(MER_RSTRD_ANN_LV_ENDBAL_2),'+000.00', --ELSE MER_RSTRD_ANN_LV_ENDBAL_2 < 0,'-' \|\| LPAD(TO_DECIMAL(MER_RSTRD_ANN_LV_ENDBAL_2 * -1,2),6,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_RSTRD_ANN_LV_ENDBAL_2,2),6,'0') ) → fil_Filter_Out_NULL.MER_RSTRD_ANN_LV_ENDBAL_2 → lkp_CPM_MER_DETAIL_STG_TBL.MER_RSTRD_ANN_LV_ENDBAL_2 [lookup CPM_MER_DETAIL_STG_TBL.MER_RSTRD_ANN_LV_ENDBAL_2 ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_RSTRD_ANN_LV_ENDBAL_3 = DECODE(TRUE, ISNULL(MER_RSTRD_ANN_LV_ENDBAL_3),'+000.00', --ELSE MER_RSTRD_ANN_LV_ENDBAL_3 < 0,'-' \|\| LPAD(TO_DECIMAL(MER_RSTRD_ANN_LV_ENDBAL_3 * -1,2),6,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_RSTRD_ANN_LV_ENDBAL_3,2),6,'0') ) → fil_Filter_Out_NULL.MER_RSTRD_ANN_LV_ENDBAL_3 → lkp_CPM_MER_DETAIL_STG_TBL.MER_RSTRD_ANN_LV_ENDBAL_3 [lookup CPM_MER_DETAIL_STG_TBL.MER_RSTRD_ANN_LV_ENDBAL_3 ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.FDA_202_DATA = '202\|' \|\| v_MER_SICK_LV_ACCRUAL_RT \|\| '\|' \|\| v_MER_SICK_LV_ACCRUED_YTD \|\| '\|' \|\| v_MER_ADVNCD_SICK_LV_BAL \|\| '\|' \|\| v_MER_SICK_LV_ENDBAL \|\| '\|' \|\| v_MER_SICK_LV_BEGBAL \|\| '\|' \|\| v_MER_SICK_LV_USED_YTD \|\| '\|' \|\| v_MER_SICK_LV_USED_PAY_PD \|\| '\|' → exp_Format_200_Records.v_MER_SICK_LV_ACCRUAL_RT = DECODE(TRUE, ISNULL(MER_SICK_LV_ACCRUAL_RT),'+000.00', --ELSE MER_SICK_LV_ACCRUAL_RT < 0,'-' \|\| LPAD(TO_DECIMAL(MER_SICK_LV_ACCRUAL_RT * -1,2),6,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_SICK_LV_ACCRUAL_RT,2),6,'0') ) → fil_Filter_Out_NULL.MER_SICK_LV_ACCRUAL_RT → lkp_CPM_MER_DETAIL_STG_TBL.MER_SICK_LV_ACCRUAL_RT [lookup CPM_MER_DETAIL_STG_TBL.MER_SICK_LV_ACCRUAL_RT ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_SICK_LV_ACCRUED_YTD = DECODE(TRUE, ISNULL(MER_SICK_LV_ACCRUED_YTD),'+00000.00', --ELSE MER_SICK_LV_ACCRUED_YTD < 0,'-' \|\| LPAD(TO_DECIMAL(MER_SICK_LV_ACCRUED_YTD * -1,2),8,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_SICK_LV_ACCRUED_YTD,2),8,'0') ) → fil_Filter_Out_NULL.MER_SICK_LV_ACCRUED_YTD → lkp_CPM_MER_DETAIL_STG_TBL.MER_SICK_LV_ACCRUED_YTD [lookup CPM_MER_DETAIL_STG_TBL.MER_SICK_LV_ACCRUED_YTD ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_ADVNCD_SICK_LV_BAL = DECODE(TRUE, ISNULL(MER_ADVNCD_SICK_LV_BAL),'+000.00', --ELSE MER_ADVNCD_SICK_LV_BAL < 0,'-' \|\| LPAD(TO_DECIMAL(MER_ADVNCD_SICK_LV_BAL * -1,2),6,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_ADVNCD_SICK_LV_BAL,2),6,'0') ) → fil_Filter_Out_NULL.MER_ADVNCD_SICK_LV_BAL → lkp_CPM_MER_DETAIL_STG_TBL.MER_ADVNCD_SICK_LV_BAL [lookup CPM_MER_DETAIL_STG_TBL.MER_ADVNCD_SICK_LV_BAL ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_SICK_LV_ENDBAL = DECODE(TRUE, ISNULL(MER_SICK_LV_ENDBAL),'+00000.00', --ELSE MER_SICK_LV_ENDBAL < 0,'-' \|\| LPAD(TO_DECIMAL(MER_SICK_LV_ENDBAL * -1,2),8,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_SICK_LV_ENDBAL,2),8,'0') ) → fil_Filter_Out_NULL.MER_SICK_LV_ENDBAL → lkp_CPM_MER_DETAIL_STG_TBL.MER_SICK_LV_ENDBAL [lookup CPM_MER_DETAIL_STG_TBL.MER_SICK_LV_ENDBAL ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_SICK_LV_BEGBAL = DECODE(TRUE, ISNULL(MER_SICK_LV_BEGBAL),'+00000.00', --ELSE MER_SICK_LV_BEGBAL < 0,'-' \|\| LPAD(TO_DECIMAL(MER_SICK_LV_BEGBAL * -1,2),8,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_SICK_LV_BEGBAL,2),8,'0') ) → fil_Filter_Out_NULL.MER_SICK_LV_BEGBAL → lkp_CPM_MER_DETAIL_STG_TBL.MER_SICK_LV_BEGBAL [lookup CPM_MER_DETAIL_STG_TBL.MER_SICK_LV_BEGBAL ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_SICK_LV_USED_YTD = DECODE(TRUE, ISNULL(MER_SICK_LV_USED_YTD),'+00000.00', --ELSE MER_SICK_LV_USED_YTD < 0,'-' \|\| LPAD(TO_DECIMAL(MER_SICK_LV_USED_YTD * -1,2),8,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_SICK_LV_USED_YTD,2),8,'0') ) → fil_Filter_Out_NULL.MER_SICK_LV_USED_YTD → lkp_CPM_MER_DETAIL_STG_TBL.MER_SICK_LV_USED_YTD [lookup CPM_MER_DETAIL_STG_TBL.MER_SICK_LV_USED_YTD ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_SICK_LV_USED_PAY_PD = DECODE(TRUE, ISNULL(MER_SICK_LV_USED_PAY_PD),'+000.00', --ELSE MER_SICK_LV_USED_PAY_PD < 0,'-' \|\| LPAD(TO_DECIMAL(MER_SICK_LV_USED_PAY_PD * -1,2),6,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_SICK_LV_USED_PAY_PD,2),6,'0') ) → fil_Filter_Out_NULL.MER_SICK_LV_USED_PAY_PD → lkp_CPM_MER_DETAIL_STG_TBL.MER_SICK_LV_USED_PAY_PD [lookup CPM_MER_DETAIL_STG_TBL.MER_SICK_LV_USED_PAY_PD ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.FDA_203_DATA = '203\|' \|\| v_MER_COMP_TIME_ENDBAL \|\| '\|' \|\| v_MER_COMP_TIME_BEGBAL \|\| '\|' \|\| v_MER_COMP_TIME_EARN_YTD \|\| '\|' \|\| v_MER_COMP_TIME_USED_YTD \|\| '\|' \|\| v_PAD_COMP_TIME_EARNED \|\| '\|' \|\| v_PAD_COMP_TIME_USED \|\| '\|' → exp_Format_200_Records.v_MER_COMP_TIME_ENDBAL = DECODE(TRUE, ISNULL(MER_COMP_TIME_ENDBAL),'+00000.00', --ELSE MER_COMP_TIME_ENDBAL < 0,'-' \|\| LPAD(TO_DECIMAL(MER_COMP_TIME_ENDBAL * -1,2),8,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_COMP_TIME_ENDBAL,2),8,'0') ) → fil_Filter_Out_NULL.MER_COMP_TIME_ENDBAL → lkp_CPM_MER_DETAIL_STG_TBL.MER_COMP_TIME_ENDBAL [lookup CPM_MER_DETAIL_STG_TBL.MER_COMP_TIME_ENDBAL ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_COMP_TIME_BEGBAL = DECODE(TRUE, ISNULL(MER_COMP_TIME_BEGBAL),'+00000.00', --ELSE MER_COMP_TIME_BEGBAL < 0,'-' \|\| LPAD(TO_DECIMAL(MER_COMP_TIME_BEGBAL * -1,2),8,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_COMP_TIME_BEGBAL,2),8,'0') ) → fil_Filter_Out_NULL.MER_COMP_TIME_BEGBAL → lkp_CPM_MER_DETAIL_STG_TBL.MER_COMP_TIME_BEGBAL [lookup CPM_MER_DETAIL_STG_TBL.MER_COMP_TIME_BEGBAL ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_COMP_TIME_EARN_YTD = DECODE(TRUE, ISNULL(MER_COMP_TIME_EARN_YTD),'+00000.00', --ELSE MER_COMP_TIME_EARN_YTD < 0,'-' \|\| LPAD(TO_DECIMAL(MER_COMP_TIME_EARN_YTD * -1,2),8,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_COMP_TIME_EARN_YTD,2),8,'0') ) → fil_Filter_Out_NULL.MER_COMP_TIME_EARN_YTD → lkp_CPM_MER_DETAIL_STG_TBL.MER_COMP_TIME_EARN_YTD [lookup CPM_MER_DETAIL_STG_TBL.MER_COMP_TIME_EARN_YTD ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_COMP_TIME_USED_YTD = DECODE(TRUE, ISNULL(MER_COMP_TIME_USED_YTD),'+00000.00', --ELSE MER_COMP_TIME_USED_YTD < 0,'-' \|\| LPAD(TO_DECIMAL(MER_COMP_TIME_USED_YTD * -1,2),8,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_COMP_TIME_USED_YTD,2),8,'0') ) → fil_Filter_Out_NULL.MER_COMP_TIME_USED_YTD → lkp_CPM_MER_DETAIL_STG_TBL.MER_COMP_TIME_USED_YTD [lookup CPM_MER_DETAIL_STG_TBL.MER_COMP_TIME_USED_YTD ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_PAD_COMP_TIME_EARNED = DECODE(TRUE, ISNULL(PAD_COMP_TIME_EARNED),'+000.00', --ELSE PAD_COMP_TIME_EARNED < 0,'-' \|\| LPAD(TO_DECIMAL(PAD_COMP_TIME_EARNED * -1,2),6,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(PAD_COMP_TIME_EARNED,2),6,'0') ) → fil_Filter_Out_NULL.PAD_COMP_TIME_EARNED → lkp_CPM_PAD_DETAIL_STG_TBL.PAD_COMP_TIME_EARNED [lookup CPM_PAD_DETAIL_STG_TBL.PAD_COMP_TIME_EARNED ON PP_END_YEAR = lkp_PP_END_YEAR AND PP_NUM = lkp_PP_NUM AND PAD_SOC_SEC_NO = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_PAD_COMP_TIME_USED = DECODE(TRUE, ISNULL(PAD_COMP_TIME_USED),'+000.00', --ELSE PAD_COMP_TIME_USED < 0,'-' \|\| LPAD(TO_DECIMAL(PAD_COMP_TIME_USED * -1,2),6,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(PAD_COMP_TIME_USED,2),6,'0') ) → fil_Filter_Out_NULL.PAD_COMP_TIME_USED → lkp_CPM_PAD_DETAIL_STG_TBL.PAD_COMP_TIME_USED [lookup CPM_PAD_DETAIL_STG_TBL.PAD_COMP_TIME_USED ON PP_END_YEAR = lkp_PP_END_YEAR AND PP_NUM = lkp_PP_NUM AND PAD_SOC_SEC_NO = lkp_FDA_EMP_ID] → exp_Format_200_Records.FDA_204_DATA = '204\|' \|\| v_MER_RELG_CMPTM_ENDBAL \|\| '\|' \|\| v_MER_RELG_CMPTM_BEGBAL \|\| '\|' \|\| v_MER_RELG_CMPTM_EARN_YTD \|\| '\|' \|\| v_MER_RELG_CMPTM_USED_YTD \|\| '\|' \|\| v_PAD_RELIG_COMP_EARNED \|\| '\|' \|\| v_PAD_RELIG_COMP_USED \|\| '\|' → exp_Format_200_Records.v_MER_RELG_CMPTM_ENDBAL = DECODE(TRUE, ISNULL(MER_RELG_CMPTM_ENDBAL),'+00000.00', --ELSE MER_RELG_CMPTM_ENDBAL < 0,'-' \|\| LPAD(TO_DECIMAL(MER_RELG_CMPTM_ENDBAL * -1,2),8,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_RELG_CMPTM_ENDBAL,2),8,'0') ) → fil_Filter_Out_NULL.MER_RELG_CMPTM_ENDBAL → lkp_CPM_MER_DETAIL_STG_TBL.MER_RELG_CMPTM_ENDBAL [lookup CPM_MER_DETAIL_STG_TBL.MER_RELG_CMPTM_ENDBAL ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_RELG_CMPTM_BEGBAL = DECODE(TRUE, ISNULL(MER_RELG_CMPTM_BEGBAL),'+00000.00', --ELSE MER_RELG_CMPTM_BEGBAL < 0,'-' \|\| LPAD(TO_DECIMAL(MER_RELG_CMPTM_BEGBAL * -1,2),8,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_RELG_CMPTM_BEGBAL,2),8,'0') ) → fil_Filter_Out_NULL.MER_RELG_CMPTM_BEGBAL → lkp_CPM_MER_DETAIL_STG_TBL.MER_RELG_CMPTM_BEGBAL [lookup CPM_MER_DETAIL_STG_TBL.MER_RELG_CMPTM_BEGBAL ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_RELG_CMPTM_EARN_YTD = DECODE(TRUE, ISNULL(MER_RELG_CMPTM_EARN_YTD),'+00000.00', --ELSE MER_RELG_CMPTM_EARN_YTD < 0,'-' \|\| LPAD(TO_DECIMAL(MER_RELG_CMPTM_EARN_YTD * -1,2),8,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_RELG_CMPTM_EARN_YTD,2),8,'0') ) → fil_Filter_Out_NULL.MER_RELG_CMPTM_EARN_YTD → lkp_CPM_MER_DETAIL_STG_TBL.MER_RELG_CMPTM_EARN_YTD [lookup CPM_MER_DETAIL_STG_TBL.MER_RELG_CMPTM_EARN_YTD ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_RELG_CMPTM_USED_YTD = DECODE(TRUE, ISNULL(MER_RELG_CMPTM_USED_YTD),'+00000.00', --ELSE MER_RELG_CMPTM_USED_YTD < 0,'-' \|\| LPAD(TO_DECIMAL(MER_RELG_CMPTM_USED_YTD * -1,2),8,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_RELG_CMPTM_USED_YTD,2),8,'0') ) → fil_Filter_Out_NULL.MER_RELG_CMPTM_USED_YTD → lkp_CPM_MER_DETAIL_STG_TBL.MER_RELG_CMPTM_USED_YTD [lookup CPM_MER_DETAIL_STG_TBL.MER_RELG_CMPTM_USED_YTD ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_PAD_RELIG_COMP_EARNED = DECODE(TRUE, ISNULL(PAD_RELIG_COMP_EARNED),'+000.00', --ELSE PAD_RELIG_COMP_EARNED < 0,'-' \|\| LPAD(TO_DECIMAL(PAD_RELIG_COMP_EARNED * -1,2),6,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(PAD_RELIG_COMP_EARNED,2),6,'0') ) → fil_Filter_Out_NULL.PAD_RELIG_COMP_EARNED → lkp_CPM_PAD_DETAIL_STG_TBL.PAD_RELIG_COMP_EARNED [lookup CPM_PAD_DETAIL_STG_TBL.PAD_RELIG_COMP_EARNED ON PP_END_YEAR = lkp_PP_END_YEAR AND PP_NUM = lkp_PP_NUM AND PAD_SOC_SEC_NO = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_PAD_RELIG_COMP_USED = DECODE(TRUE, ISNULL(PAD_RELIG_COMP_USED),'+000.00', --ELSE PAD_RELIG_COMP_USED < 0,'-' \|\| LPAD(TO_DECIMAL(PAD_RELIG_COMP_USED * -1,2),6,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(PAD_RELIG_COMP_USED,2),6,'0') ) → fil_Filter_Out_NULL.PAD_RELIG_COMP_USED → lkp_CPM_PAD_DETAIL_STG_TBL.PAD_RELIG_COMP_USED [lookup CPM_PAD_DETAIL_STG_TBL.PAD_RELIG_COMP_USED ON PP_END_YEAR = lkp_PP_END_YEAR AND PP_NUM = lkp_PP_NUM AND PAD_SOC_SEC_NO = lkp_FDA_EMP_ID] → exp_Format_200_Records.FDA_205_DATA = '205\|' \|\| v_MER_TVL_COMP_END_BAL \|\| '\|' \|\| v_MER_TVL_COMP_BEGIN_BAL \|\| '\|' \|\| v_MER_TVL_COMP_EARN_YTD \|\| '\|' \|\| v_MER_TVL_COMP_USED_YTD \|\| '\|' \|\| v_PAD_COMPTIME_TRAVEL_EARNED \|\| '\|' \|\| v_PAD_COMPTIME_TRAVEL_USED \|\| '\|' → exp_Format_200_Records.v_MER_TVL_COMP_END_BAL = DECODE(TRUE, ISNULL(MER_TVL_COMP_END_BAL),'+00000.00', --ELSE MER_TVL_COMP_END_BAL < 0,'-' \|\| LPAD(TO_DECIMAL(MER_TVL_COMP_END_BAL * -1,2),8,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_TVL_COMP_END_BAL,2),8,'0') ) → fil_Filter_Out_NULL.MER_TVL_COMP_END_BAL → lkp_CPM_MER_DETAIL_STG_TBL.MER_TVL_COMP_END_BAL [lookup CPM_MER_DETAIL_STG_TBL.MER_TVL_COMP_END_BAL ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_TVL_COMP_BEGIN_BAL = DECODE(TRUE, ISNULL(MER_TVL_COMP_BEGIN_BAL),'+00000.00', --ELSE MER_TVL_COMP_BEGIN_BAL < 0,'-' \|\| LPAD(TO_DECIMAL(MER_TVL_COMP_BEGIN_BAL * -1,2),8,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_TVL_COMP_BEGIN_BAL,2),8,'0') ) → fil_Filter_Out_NULL.MER_TVL_COMP_BEGIN_BAL → lkp_CPM_MER_DETAIL_STG_TBL.MER_TVL_COMP_BEGIN_BAL [lookup CPM_MER_DETAIL_STG_TBL.MER_TVL_COMP_BEGIN_BAL ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_TVL_COMP_EARN_YTD = DECODE(TRUE, ISNULL(MER_TVL_COMP_EARN_YTD),'+00000.00', --ELSE MER_TVL_COMP_EARN_YTD < 0,'-' \|\| LPAD(TO_DECIMAL(MER_TVL_COMP_EARN_YTD * -1,2),8,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_TVL_COMP_EARN_YTD,2),8,'0') ) → fil_Filter_Out_NULL.MER_TVL_COMP_EARN_YTD → lkp_CPM_MER_DETAIL_STG_TBL.MER_TVL_COMP_EARN_YTD [lookup CPM_MER_DETAIL_STG_TBL.MER_TVL_COMP_EARN_YTD ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_TVL_COMP_USED_YTD = DECODE(TRUE, ISNULL(MER_TVL_COMP_USED_YTD),'+00000.00', --ELSE MER_TVL_COMP_USED_YTD < 0,'-' \|\| LPAD(TO_DECIMAL(MER_TVL_COMP_USED_YTD * -1,2),8,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_TVL_COMP_USED_YTD,2),8,'0') ) → fil_Filter_Out_NULL.MER_TVL_COMP_USED_YTD → lkp_CPM_MER_DETAIL_STG_TBL.MER_TVL_COMP_USED_YTD [lookup CPM_MER_DETAIL_STG_TBL.MER_TVL_COMP_USED_YTD ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_PAD_COMPTIME_TRAVEL_EARNED = DECODE(TRUE, ISNULL(PAD_COMPTIME_TRAVEL_EARNED),'+000.00', --ELSE PAD_COMPTIME_TRAVEL_EARNED < 0,'-' \|\| LPAD(TO_DECIMAL(PAD_COMPTIME_TRAVEL_EARNED * -1,2),6,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(PAD_COMPTIME_TRAVEL_EARNED,2),6,'0') ) → fil_Filter_Out_NULL.PAD_COMPTIME_TRAVEL_EARNED → lkp_CPM_PAD_DETAIL_STG_TBL.PAD_COMPTIME_TRAVEL_EARNED [lookup CPM_PAD_DETAIL_STG_TBL.PAD_COMPTIME_TRAVEL_EARNED ON PP_END_YEAR = lkp_PP_END_YEAR AND PP_NUM = lkp_PP_NUM AND PAD_SOC_SEC_NO = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_PAD_COMPTIME_TRAVEL_USED = DECODE(TRUE, ISNULL(PAD_COMPTIME_TRAVEL_USED),'+000.00', --ELSE PAD_COMPTIME_TRAVEL_USED < 0,'-' \|\| LPAD(TO_DECIMAL(PAD_COMPTIME_TRAVEL_USED * -1,2),6,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(PAD_COMPTIME_TRAVEL_USED,2),6,'0') ) → fil_Filter_Out_NULL.PAD_COMPTIME_TRAVEL_USED → lkp_CPM_PAD_DETAIL_STG_TBL.PAD_COMPTIME_TRAVEL_USED [lookup CPM_PAD_DETAIL_STG_TBL.PAD_COMPTIME_TRAVEL_USED ON PP_END_YEAR = lkp_PP_END_YEAR AND PP_NUM = lkp_PP_NUM AND PAD_SOC_SEC_NO = lkp_FDA_EMP_ID] → exp_Format_200_Records.FDA_206_DATA = '206\|' \|\| v_PAD_ADMIN_LVE_HOURS \|\| '\|' \|\| v_DYD_ADMINISTRATIVE_LEAVE \|\| '\|' → exp_Format_200_Records.v_PAD_ADMIN_LVE_HOURS = DECODE(TRUE, ISNULL(PAD_ADMIN_LVE_HOURS),'+000.00', --ELSE PAD_ADMIN_LVE_HOURS < 0,'-' \|\| LPAD(TO_DECIMAL(PAD_ADMIN_LVE_HOURS * -1,2),6,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(PAD_ADMIN_LVE_HOURS,2),6,'0') ) → fil_Filter_Out_NULL.PAD_ADMIN_LVE_HOURS → lkp_CPM_PAD_DETAIL_STG_TBL.PAD_ADMIN_LVE_HOURS [lookup CPM_PAD_DETAIL_STG_TBL.PAD_ADMIN_LVE_HOURS ON PP_END_YEAR = lkp_PP_END_YEAR AND PP_NUM = lkp_PP_NUM AND PAD_SOC_SEC_NO = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_DYD_ADMINISTRATIVE_LEAVE = DECODE(TRUE, ISNULL(DYD_ADMINISTRATIVE_LEAVE),'+00000.00', --ELSE DYD_ADMINISTRATIVE_LEAVE < 0,'-' \|\| LPAD(TO_DECIMAL(DYD_ADMINISTRATIVE_LEAVE * -1,2),8,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(DYD_ADMINISTRATIVE_LEAVE,2),8,'0') ) → fil_Filter_Out_NULL.DYD_ADMINISTRATIVE_LEAVE → lkp_CPM_YTD_DETAIL_STG_TBL.DYD_ADMINISTRATIVE_LEAVE [lookup CPM_YTD_DETAIL_STG_TBL.DYD_ADMINISTRATIVE_LEAVE ON PP_END_YEAR = lkp_PP_END_YEAR AND PP_NUM = lkp_PP_NUM AND DYD_SSN_1 = lkp_FDA_EMP_ID] → exp_Format_200_Records.FDA_207_DATA = '207\|' \|\| v_MER_MIL_LV_ENDBAL \|\| '\|' \|\| v_MER_MIL_LV_BEGBAL \|\| '\|' \|\| v_MER_MIL_LV_USED_YTD \|\| '\|' \|\| v_PAD_MILITARY_LVE_EARNED_YTD \|\| '\|' → exp_Format_200_Records.v_MER_MIL_LV_ENDBAL = DECODE(TRUE, ISNULL(MER_MIL_LV_ENDBAL),'+000.00', --ELSE MER_MIL_LV_ENDBAL < 0,'-' \|\| LPAD(TO_DECIMAL(MER_MIL_LV_ENDBAL * -1,2),6,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_MIL_LV_ENDBAL,2),6,'0') ) → fil_Filter_Out_NULL.MER_MIL_LV_ENDBAL → lkp_CPM_MER_DETAIL_STG_TBL.MER_MIL_LV_ENDBAL [lookup CPM_MER_DETAIL_STG_TBL.MER_MIL_LV_ENDBAL ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_MIL_LV_BEGBAL = DECODE(TRUE, ISNULL(MER_MIL_LV_BEGBAL),'+000.00', --ELSE MER_MIL_LV_BEGBAL < 0,'-' \|\| LPAD(TO_DECIMAL(MER_MIL_LV_BEGBAL * -1,2),6,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_MIL_LV_BEGBAL,2),6,'0') ) → fil_Filter_Out_NULL.MER_MIL_LV_BEGBAL → lkp_CPM_MER_DETAIL_STG_TBL.MER_MIL_LV_BEGBAL [lookup CPM_MER_DETAIL_STG_TBL.MER_MIL_LV_BEGBAL ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_MIL_LV_USED_YTD = DECODE(TRUE, ISNULL(MER_MIL_LV_USED_YTD),'+000.00', --ELSE MER_MIL_LV_USED_YTD < 0,'-' \|\| LPAD(TO_DECIMAL(MER_MIL_LV_USED_YTD * -1,2),6,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_MIL_LV_USED_YTD,2),6,'0') ) → fil_Filter_Out_NULL.MER_MIL_LV_USED_YTD → lkp_CPM_MER_DETAIL_STG_TBL.MER_MIL_LV_USED_YTD [lookup CPM_MER_DETAIL_STG_TBL.MER_MIL_LV_USED_YTD ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_PAD_MILITARY_LVE_EARNED_YTD = DECODE(TRUE, ISNULL(PAD_MILITARY_LVE_EARNED_YTD),'+000.00', --ELSE PAD_MILITARY_LVE_EARNED_YTD < 0,'-' \|\| LPAD(TO_DECIMAL(PAD_MILITARY_LVE_EARNED_YTD * -1,2),6,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(PAD_MILITARY_LVE_EARNED_YTD,2),6,'0') ) → fil_Filter_Out_NULL.PAD_MILITARY_LVE_EARNED_YTD → lkp_CPM_PAD_DETAIL_STG_TBL.PAD_MILITARY_LVE_EARNED_YTD [lookup CPM_PAD_DETAIL_STG_TBL.PAD_MILITARY_LVE_EARNED_YTD ON PP_END_YEAR = lkp_PP_END_YEAR AND PP_NUM = lkp_PP_NUM AND PAD_SOC_SEC_NO = lkp_FDA_EMP_ID] → exp_Format_200_Records.FDA_208_DATA = '208\|' \|\| v_PAD_DONATED_LVE_BAL \|\| '\|' \|\| v_PAD_DONATED_LVE_USED \|\| '\|' → exp_Format_200_Records.v_PAD_DONATED_LVE_BAL = DECODE(TRUE, ISNULL(PAD_DONATED_LVE_BAL),'+00000.00', --ELSE PAD_DONATED_LVE_BAL < 0,'-' \|\| LPAD(TO_DECIMAL(PAD_DONATED_LVE_BAL * -1,2),8,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(PAD_DONATED_LVE_BAL,2),8,'0') ) → fil_Filter_Out_NULL.PAD_DONATED_LVE_BAL → lkp_CPM_PAD_DETAIL_STG_TBL.PAD_DONATED_LVE_BAL [lookup CPM_PAD_DETAIL_STG_TBL.PAD_DONATED_LVE_BAL ON PP_END_YEAR = lkp_PP_END_YEAR AND PP_NUM = lkp_PP_NUM AND PAD_SOC_SEC_NO = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_PAD_DONATED_LVE_USED = DECODE(TRUE, ISNULL(PAD_DONATED_LVE_USED),'+000.00', --ELSE PAD_DONATED_LVE_USED < 0,'-' \|\| LPAD(TO_DECIMAL(PAD_DONATED_LVE_USED * -1,2),6,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(PAD_DONATED_LVE_USED,2),6,'0') ) → fil_Filter_Out_NULL.PAD_DONATED_LVE_USED → lkp_CPM_PAD_DETAIL_STG_TBL.PAD_DONATED_LVE_USED [lookup CPM_PAD_DETAIL_STG_TBL.PAD_DONATED_LVE_USED ON PP_END_YEAR = lkp_PP_END_YEAR AND PP_NUM = lkp_PP_NUM AND PAD_SOC_SEC_NO = lkp_FDA_EMP_ID] → exp_Format_200_Records.FDA_209_DATA = '209\|' \|\| v_DYD_LWOP_AWOL \|\| '\|' → exp_Format_200_Records.v_DYD_LWOP_AWOL = DECODE(TRUE, ISNULL(DYD_LWOP_AWOL),'+00000.00', --ELSE DYD_LWOP_AWOL < 0,'-' \|\| LPAD(TO_DECIMAL(DYD_LWOP_AWOL * -1,2),8,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(DYD_LWOP_AWOL,2),8,'0') ) → fil_Filter_Out_NULL.DYD_LWOP_AWOL → lkp_CPM_YTD_DETAIL_STG_TBL.DYD_LWOP_AWOL [lookup CPM_YTD_DETAIL_STG_TBL.DYD_LWOP_AWOL ON PP_END_YEAR = lkp_PP_END_YEAR AND PP_NUM = lkp_PP_NUM AND DYD_SSN_1 = lkp_FDA_EMP_ID] → exp_Format_200_Records.FDA_211_DATA = '211\|' \|\| v_MER_CRED_HRS_ENDBAL \|\| '\|' \|\| v_MER_CRED_HRS_BEGBAL \|\| '\|' \|\| v_MER_CRED_HRS_EARN_YTD \|\| '\|' \|\| v_MER_CRED_HRS_USED_YTD \|\| '\|' \|\| v_PAD_CREDIT_HOURS_EARNED \|\| '\|' \|\| v_PAD_CREDIT_HOURS_USED \|\| '\|' → exp_Format_200_Records.v_MER_CRED_HRS_ENDBAL = DECODE(TRUE, ISNULL(MER_CRED_HRS_ENDBAL),'+00000.00', --ELSE MER_CRED_HRS_ENDBAL < 0,'-' \|\| LPAD(TO_DECIMAL(MER_CRED_HRS_ENDBAL * -1,2),8,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_CRED_HRS_ENDBAL,2),8,'0') ) → fil_Filter_Out_NULL.MER_CRED_HRS_ENDBAL → lkp_CPM_MER_DETAIL_STG_TBL.MER_CRED_HRS_ENDBAL [lookup CPM_MER_DETAIL_STG_TBL.MER_CRED_HRS_ENDBAL ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_CRED_HRS_BEGBAL = DECODE(TRUE, ISNULL(MER_CRED_HRS_BEGBAL),'+00000.00', --ELSE MER_CRED_HRS_BEGBAL < 0,'-' \|\| LPAD(TO_DECIMAL(MER_CRED_HRS_BEGBAL * -1,2),8,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_CRED_HRS_BEGBAL,2),8,'0') ) → fil_Filter_Out_NULL.MER_CRED_HRS_BEGBAL → lkp_CPM_MER_DETAIL_STG_TBL.MER_CRED_HRS_BEGBAL [lookup CPM_MER_DETAIL_STG_TBL.MER_CRED_HRS_BEGBAL ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_CRED_HRS_EARN_YTD = DECODE(TRUE, ISNULL(MER_CRED_HRS_EARN_YTD),'+00000.00', --ELSE MER_CRED_HRS_EARN_YTD < 0,'-' \|\| LPAD(TO_DECIMAL(MER_CRED_HRS_EARN_YTD * -1,2),8,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_CRED_HRS_EARN_YTD,2),8,'0') ) → fil_Filter_Out_NULL.MER_CRED_HRS_EARN_YTD → lkp_CPM_MER_DETAIL_STG_TBL.MER_CRED_HRS_EARN_YTD [lookup CPM_MER_DETAIL_STG_TBL.MER_CRED_HRS_EARN_YTD ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_CRED_HRS_USED_YTD = DECODE(TRUE, ISNULL(MER_CRED_HRS_USED_YTD),'+00000.00', --ELSE MER_CRED_HRS_USED_YTD < 0,'-' \|\| LPAD(TO_DECIMAL(MER_CRED_HRS_USED_YTD * -1,2),8,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_CRED_HRS_USED_YTD,2),8,'0') ) → fil_Filter_Out_NULL.MER_CRED_HRS_USED_YTD → lkp_CPM_MER_DETAIL_STG_TBL.MER_CRED_HRS_USED_YTD [lookup CPM_MER_DETAIL_STG_TBL.MER_CRED_HRS_USED_YTD ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_PAD_CREDIT_HOURS_EARNED = DECODE(TRUE, ISNULL(PAD_CREDIT_HOURS_EARNED),'+000.00', --ELSE PAD_CREDIT_HOURS_EARNED < 0,'-' \|\| LPAD(TO_DECIMAL(PAD_CREDIT_HOURS_EARNED * -1,2),6,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(PAD_CREDIT_HOURS_EARNED,2),6,'0') ) → fil_Filter_Out_NULL.PAD_CREDIT_HOURS_EARNED → lkp_CPM_PAD_DETAIL_STG_TBL.PAD_CREDIT_HOURS_EARNED [lookup CPM_PAD_DETAIL_STG_TBL.PAD_CREDIT_HOURS_EARNED ON PP_END_YEAR = lkp_PP_END_YEAR AND PP_NUM = lkp_PP_NUM AND PAD_SOC_SEC_NO = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_PAD_CREDIT_HOURS_USED = DECODE(TRUE, ISNULL(PAD_CREDIT_HOURS_USED),'+000.00', --ELSE PAD_CREDIT_HOURS_USED < 0,'-' \|\| LPAD(TO_DECIMAL( PAD_CREDIT_HOURS_USED * -1,2),6,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(PAD_CREDIT_HOURS_USED,2),6,'0') ) → fil_Filter_Out_NULL.PAD_CREDIT_HOURS_USED → lkp_CPM_PAD_DETAIL_STG_TBL.PAD_CREDIT_HOURS_USED [lookup CPM_PAD_DETAIL_STG_TBL.PAD_CREDIT_HOURS_USED ON PP_END_YEAR = lkp_PP_END_YEAR AND PP_NUM = lkp_PP_NUM AND PAD_SOC_SEC_NO = lkp_FDA_EMP_ID] → exp_Format_200_Records.FDA_212_DATA = '212\|' \|\| v_MER_TOFF_AWRD_BEG_YRGAL \|\| '\|' \|\| v_MER_TOFF_AWRD_AUTHHRS_YTD \|\| '\|' \|\| v_MER_TOFF_AWRD_USED_YTD \|\| '\|' \|\| v_MER_TOFF_AWRD_FORF_YTD \|\| '\|' \|\| v_MER_TOFF_AWRD_ENDBAL \|\| '\|+000\|+000\|' → exp_Format_200_Records.v_MER_TOFF_AWRD_BEG_YRGAL = DECODE(TRUE, ISNULL(MER_TOFF_AWRD_BEG_YRGAL),'+00000.00', --ELSE MER_TOFF_AWRD_BEG_YRGAL < 0,'-' \|\| LPAD(TO_DECIMAL(MER_TOFF_AWRD_BEG_YRGAL * -1,2),8,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_TOFF_AWRD_BEG_YRGAL,2),8,'0') ) → fil_Filter_Out_NULL.MER_TOFF_AWRD_BEG_YRGAL → lkp_CPM_MER_DETAIL_STG_TBL.MER_TOFF_AWRD_BEG_YRGAL [lookup CPM_MER_DETAIL_STG_TBL.MER_TOFF_AWRD_BEG_YRGAL ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_TOFF_AWRD_AUTHHRS_YTD = DECODE(TRUE, ISNULL(MER_TOFF_AWRD_AUTHHRS_YTD),'+00000.00', --ELSE MER_TOFF_AWRD_AUTHHRS_YTD < 0,'-' \|\| LPAD(TO_DECIMAL(MER_TOFF_AWRD_AUTHHRS_YTD * -1,2),6,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_TOFF_AWRD_AUTHHRS_YTD,2),6,'0') ) → fil_Filter_Out_NULL.MER_TOFF_AWRD_AUTHHRS_YTD → lkp_CPM_MER_DETAIL_STG_TBL.MER_TOFF_AWRD_AUTHHRS_YTD [lookup CPM_MER_DETAIL_STG_TBL.MER_TOFF_AWRD_AUTHHRS_YTD ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_TOFF_AWRD_USED_YTD = DECODE(TRUE, ISNULL(MER_TOFF_AWRD_USED_YTD),'+000.00', --ELSE MER_TOFF_AWRD_USED_YTD < 0,'-' \|\| LPAD(TO_DECIMAL(MER_TOFF_AWRD_USED_YTD * -1,2),6,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_TOFF_AWRD_USED_YTD,2),6,'0') ) → fil_Filter_Out_NULL.MER_TOFF_AWRD_USED_YTD → lkp_CPM_MER_DETAIL_STG_TBL.MER_TOFF_AWRD_USED_YTD [lookup CPM_MER_DETAIL_STG_TBL.MER_TOFF_AWRD_USED_YTD ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_TOFF_AWRD_FORF_YTD = DECODE(TRUE, ISNULL(MER_TOFF_AWRD_FORF_YTD),'+000.00', --ELSE MER_TOFF_AWRD_FORF_YTD < 0,'-' \|\| LPAD(TO_DECIMAL(MER_TOFF_AWRD_FORF_YTD * -1,2),6,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_TOFF_AWRD_FORF_YTD,2),6,'0') ) → fil_Filter_Out_NULL.MER_TOFF_AWRD_FORF_YTD → lkp_CPM_MER_DETAIL_STG_TBL.MER_TOFF_AWRD_FORF_YTD [lookup CPM_MER_DETAIL_STG_TBL.MER_TOFF_AWRD_FORF_YTD ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_MER_TOFF_AWRD_ENDBAL = DECODE(TRUE, ISNULL(MER_TOFF_AWRD_ENDBAL),'+000.00', --ELSE MER_TOFF_AWRD_ENDBAL < 0,'-' \|\| LPAD(TO_DECIMAL(MER_TOFF_AWRD_ENDBAL * -1,2),6,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(MER_TOFF_AWRD_ENDBAL,2),6,'0') ) → fil_Filter_Out_NULL.MER_TOFF_AWRD_ENDBAL → lkp_CPM_MER_DETAIL_STG_TBL.MER_TOFF_AWRD_ENDBAL [lookup CPM_MER_DETAIL_STG_TBL.MER_TOFF_AWRD_ENDBAL ON PP_END_YEAR = lkp_FDA_PP_YEAR AND PP_NUM = lkp_FDA_PP_NUM AND MER_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.FDA_214_DATA = '214\|' \|\| v_PAD_OVERTIME_HOURS \|\| '\|' → exp_Format_200_Records.v_PAD_OVERTIME_HOURS = DECODE(TRUE, ISNULL(PAD_OVERTIME_HOURS),'+00000.00', --ELSE PAD_OVERTIME_HOURS < 0,'-' \|\| LPAD(TO_DECIMAL(PAD_OVERTIME_HOURS * -1,2),8,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(PAD_OVERTIME_HOURS,2),8,'0') ) → fil_Filter_Out_NULL.PAD_OVERTIME_HOURS → lkp_CPM_PAD_DETAIL_STG_TBL.PAD_OVERTIME_HOURS [lookup CPM_PAD_DETAIL_STG_TBL.PAD_OVERTIME_HOURS ON PP_END_YEAR = lkp_PP_END_YEAR AND PP_NUM = lkp_PP_NUM AND PAD_SOC_SEC_NO = lkp_FDA_EMP_ID] → exp_Format_200_Records.FDA_215_DATA = '215\|' \|\| v_PYF_SRY_HR \|\| '\|' \|\| v_PYF_BSC_OT_RAT \|\| '\|' → exp_Format_200_Records.v_PYF_SRY_HR = DECODE(TRUE, ISNULL(PYF_SRY_HR),'+000.00', --ELSE PYF_SRY_HR < 0,'-' \|\| LPAD(TO_DECIMAL(PYF_SRY_HR * -1,2),6,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(PYF_SRY_HR,2),6,'0') ) → fil_Filter_Out_NULL.PYF_SRY_HR → lkp_CPM_NEWPAY_TBL.HRLY_RATE [lookup CPM_NEWPAY_TBL.HRLY_RATE ON PP_END_YEAR = lkp_PP_END_YEAR AND PP_NUM = lkp_PP_NUM AND DFAS_PSEUDO_SSN = lkp_FDA_EMP_ID] → exp_Format_200_Records.v_PYF_BSC_OT_RAT = DECODE(TRUE, ISNULL(PYF_BSC_OT_RAT),'+000.00', --ELSE PYF_BSC_OT_RAT < 0,'-' \|\| LPAD(TO_DECIMAL(PYF_BSC_OT_RAT * -1,2),6,'0'), --ELSE '+' \|\| LPAD(TO_DECIMAL(PYF_BSC_OT_RAT,2),6,'0') ) → fil_Filter_Out_NULL.PYF_BSC_OT_RAT → lkp_CPM_NEWPAY_TBL.OT_RATE [lookup CPM_NEWPAY_TBL.OT_RATE ON PP_END_YEAR = lkp_PP_END_YEAR AND PP_NUM = lkp_PP_NUM AND DFAS_PSEUDO_SSN = lkp_FDA_EMP_ID] | CPM_MER_DETAIL_STG_TBL.MER_ADVNCD_SICK_LV_BAL (lookup); CPM_MER_DETAIL_STG_TBL.MER_ANN_LV_ACCRD_YTD (lookup); CPM_MER_DETAIL_STG_TBL.MER_ANN_LV_ACCRUAL_RT (lookup); CPM_MER_DETAIL_STG_TBL.MER_ANN_LV_BEGBAL (lookup); CPM_MER_DETAIL_STG_TBL.MER_ANN_LV_CEILING (lookup); CPM_MER_DETAIL_STG_TBL.MER_ANN_LV_ENDBAL (lookup); CPM_MER_DETAIL_STG_TBL.MER_ANN_LV_USED_PAY_PD (lookup); CPM_MER_DETAIL_STG_TBL.MER_ANN_LV_USED_YTD (lookup); CPM_MER_DETAIL_STG_TBL.MER_COMP_TIME_BEGBAL (lookup); CPM_MER_DETAIL_STG_TBL.MER_COMP_TIME_EARN_YTD (lookup); CPM_MER_DETAIL_STG_TBL.MER_COMP_TIME_ENDBAL (lookup); CPM_MER_DETAIL_STG_TBL.MER_COMP_TIME_USED_YTD (lookup); CPM_MER_DETAIL_STG_TBL.MER_CRED_HRS_BEGBAL (lookup); CPM_MER_DETAIL_STG_TBL.MER_CRED_HRS_EARN_YTD (lookup); CPM_MER_DETAIL_STG_TBL.MER_CRED_HRS_ENDBAL (lookup); CPM_MER_DETAIL_STG_TBL.MER_CRED_HRS_USED_YTD (lookup); CPM_MER_DETAIL_STG_TBL.MER_MIL_LV_BEGBAL (lookup); CPM_MER_DETAIL_STG_TBL.MER_MIL_LV_ENDBAL (lookup); CPM_MER_DETAIL_STG_TBL.MER_MIL_LV_USED_YTD (lookup); CPM_MER_DETAIL_STG_TBL.MER_RELG_CMPTM_BEGBAL (lookup); CPM_MER_DETAIL_STG_TBL.MER_RELG_CMPTM_EARN_YTD (lookup); CPM_MER_DETAIL_STG_TBL.MER_RELG_CMPTM_ENDBAL (lookup); CPM_MER_DETAIL_STG_TBL.MER_RELG_CMPTM_USED_YTD (lookup); CPM_MER_DETAIL_STG_TBL.MER_RSTRD_ANN_LV_ENDBAL_1 (lookup); CPM_MER_DETAIL_STG_TBL.MER_RSTRD_ANN_LV_ENDBAL_2 (lookup); CPM_MER_DETAIL_STG_TBL.MER_RSTRD_ANN_LV_ENDBAL_3 (lookup); CPM_MER_DETAIL_STG_TBL.MER_SICK_LV_ACCRUAL_RT (lookup); CPM_MER_DETAIL_STG_TBL.MER_SICK_LV_ACCRUED_YTD (lookup); CPM_MER_DETAIL_STG_TBL.MER_SICK_LV_BEGBAL (lookup); CPM_MER_DETAIL_STG_TBL.MER_SICK_LV_ENDBAL (lookup); CPM_MER_DETAIL_STG_TBL.MER_SICK_LV_USED_PAY_PD (lookup); CPM_MER_DETAIL_STG_TBL.MER_SICK_LV_USED_YTD (lookup); CPM_MER_DETAIL_STG_TBL.MER_TOFF_AWRD_AUTHHRS_YTD (lookup); CPM_MER_DETAIL_STG_TBL.MER_TOFF_AWRD_BEG_YRGAL (lookup); CPM_MER_DETAIL_STG_TBL.MER_TOFF_AWRD_ENDBAL (lookup); CPM_MER_DETAIL_STG_TBL.MER_TOFF_AWRD_FORF_YTD (lookup); CPM_MER_DETAIL_STG_TBL.MER_TOFF_AWRD_USED_YTD (lookup); CPM_MER_DETAIL_STG_TBL.MER_TVL_COMP_BEGIN_BAL (lookup); CPM_MER_DETAIL_STG_TBL.MER_TVL_COMP_EARN_YTD (lookup); CPM_MER_DETAIL_STG_TBL.MER_TVL_COMP_END_BAL (lookup); CPM_MER_DETAIL_STG_TBL.MER_TVL_COMP_USED_YTD (lookup); CPM_NEWPAY_TBL.HRLY_RATE (lookup); CPM_NEWPAY_TBL.OT_RATE (lookup); CPM_PAD_DETAIL_STG_TBL.PAD_ADMIN_LVE_HOURS (lookup); CPM_PAD_DETAIL_STG_TBL.PAD_COMPTIME_TRAVEL_EARNED (lookup); CPM_PAD_DETAIL_STG_TBL.PAD_COMPTIME_TRAVEL_USED (lookup); CPM_PAD_DETAIL_STG_TBL.PAD_COMP_TIME_EARNED (lookup); CPM_PAD_DETAIL_STG_TBL.PAD_COMP_TIME_USED (lookup); CPM_PAD_DETAIL_STG_TBL.PAD_CREDIT_HOURS_EARNED (lookup); CPM_PAD_DETAIL_STG_TBL.PAD_CREDIT_HOURS_USED (lookup); CPM_PAD_DETAIL_STG_TBL.PAD_DONATED_LVE_BAL (lookup); CPM_PAD_DETAIL_STG_TBL.PAD_DONATED_LVE_USED (lookup); CPM_PAD_DETAIL_STG_TBL.PAD_MILITARY_LVE_EARNED_YTD (lookup); CPM_PAD_DETAIL_STG_TBL.PAD_OVERTIME_HOURS (lookup); CPM_PAD_DETAIL_STG_TBL.PAD_RELIG_COMP_EARNED (lookup); CPM_PAD_DETAIL_STG_TBL.PAD_RELIG_COMP_USED (lookup); CPM_YTD_DETAIL_STG_TBL.DYD_ADMINISTRATIVE_LEAVE (lookup); CPM_YTD_DETAIL_STG_TBL.DYD_LWOP_AWOL (lookup); HI_PM_FDA_TATRAN_TBL.FDA_EMP_ID (lookup key); literal/expression: 'D' (lookup key); literal/expression: 'E' (lookup key); literal/expression: TO_DECIMAL($$MAP_PP_END_YEAR, 0) (lookup key); literal/expression: TO_DECIMAL($$MAP_PP_NUM, 0) (lookup key) |

## Mapping `m_0300_PM_FDA_Create_Output_File`

- Sessions: `s_0300_PM_FDA_Create_Output_File` (#8)
- Sources: `HI_PM_FDA_TATRAN_TBL`
- Target instances: `HI_PM_FDA_TATRAN_FLAT`

### Transformation `SQ_HI_PM_FDA_TATRAN_TBL` (Source Qualifier)

- **Sql Query**: `SELECT HI_PM_FDA_TATRAN_TBL.FDA_TK_NO, HI_PM_FDA_TATRAN_TBL.FDA_EMP_ID, HI_PM_FDA_TATRAN_TBL.FDA_PP_YEAR, HI_PM_FDA_TATRAN_TBL.FDA_PP_NUM, HI_PM_FDA_TATRAN_TBL.FDA_REC_TYPE, HI_PM_FDA_TATRAN_TBL.FDA_DATA FROM HI_PM_FDA_TATRAN_TBL ORDER BY HI_PM_FDA_TATRAN_TBL.FDA_BATCH_ID, HI_PM_FDA_TATRAN_TBL.FDA_TK_NO, HI_PM_FDA_TATRAN_TBL.FDA_EMP_ID, HI_PM_FDA_TATRAN_TBL.FDA_PP_YEAR, HI_PM_FDA_TATRAN_TBL.FDA_PP_NUM, HI_PM_FDA_TATRAN_TBL.FDA_REC_TYPE, HI_PM_FDA_TATRAN_TBL.FDA_SEQ`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

- SQL override `SQ_HI_PM_FDA_TATRAN_TBL` positional bindings: 1 → `FDA_BATCH_ID` = `HI_PM_FDA_TATRAN_TBL.FDA_TK_NO`; 2 → `FDA_TK_NO` = `HI_PM_FDA_TATRAN_TBL.FDA_EMP_ID`; 3 → `FDA_EMP_ID` = `HI_PM_FDA_TATRAN_TBL.FDA_PP_YEAR`; 4 → `FDA_PP_YEAR` = `HI_PM_FDA_TATRAN_TBL.FDA_PP_NUM`; 5 → `FDA_PP_NUM` = `HI_PM_FDA_TATRAN_TBL.FDA_REC_TYPE`; 6 → `FDA_REC_TYPE` = `HI_PM_FDA_TATRAN_TBL.FDA_DATA`

### Target instance `HI_PM_FDA_TATRAN_FLAT` (table `HI_PM_FDA_TATRAN_FLAT`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| HI_PM_FDA_TATRAN_FLAT | FDA_TK_NO | exp_Convert_Minutes_REPLACESTR.FDA_TK_NO → SQ_HI_PM_FDA_TATRAN_TBL.FDA_TK_NO → HI_PM_FDA_TATRAN_TBL.FDA_TK_NO | HI_PM_FDA_TATRAN_TBL.FDA_TK_NO |
| HI_PM_FDA_TATRAN_FLAT | FDA_EMP_ID | exp_Convert_Minutes_REPLACESTR.FDA_EMP_ID → SQ_HI_PM_FDA_TATRAN_TBL.FDA_EMP_ID → HI_PM_FDA_TATRAN_TBL.FDA_EMP_ID | HI_PM_FDA_TATRAN_TBL.FDA_EMP_ID |
| HI_PM_FDA_TATRAN_FLAT | FDA_PP_YEAR | exp_Convert_Minutes_REPLACESTR.FDA_PP_YEAR → SQ_HI_PM_FDA_TATRAN_TBL.FDA_PP_YEAR → HI_PM_FDA_TATRAN_TBL.FDA_PP_YEAR | HI_PM_FDA_TATRAN_TBL.FDA_PP_YEAR |
| HI_PM_FDA_TATRAN_FLAT | FDA_PP_NUM | exp_Convert_Minutes_REPLACESTR.FDA_PP_NUM → SQ_HI_PM_FDA_TATRAN_TBL.FDA_PP_NUM → HI_PM_FDA_TATRAN_TBL.FDA_PP_NUM | HI_PM_FDA_TATRAN_TBL.FDA_PP_NUM |
| HI_PM_FDA_TATRAN_FLAT | FDA_REC_TYPE | exp_Convert_Minutes_REPLACESTR.FDA_REC_TYPE → SQ_HI_PM_FDA_TATRAN_TBL.FDA_REC_TYPE → HI_PM_FDA_TATRAN_TBL.FDA_REC_TYPE | HI_PM_FDA_TATRAN_TBL.FDA_REC_TYPE |
| HI_PM_FDA_TATRAN_FLAT | FDA_DATA | exp_Convert_Minutes_REPLACESTR.o_FDA_DATA = IIF(SUBSTR(i_FDA_DATA,1,3) ^= '215', REPLACESTR(0, REPLACESTR(0, REPLACESTR(0,i_FDA_DATA,'.25\|','.15\|') ,'.50\|','.30\|') ,'.75\|','.45\|'), i_FDA_DATA ) → SQ_HI_PM_FDA_TATRAN_TBL.FDA_DATA → HI_PM_FDA_TATRAN_TBL.FDA_DATA | HI_PM_FDA_TATRAN_TBL.FDA_DATA |

## Mapping `m_0500_PM_FDA_IO_Counter`

- Sessions: `s_0500_PM_FDA_IO_Counter` (#9)
- Sources: `ERROR_TBL`, `HI_PM_FDA_TATRAN_TBL`, `PAY_PERIOD`
- Target instances: `COUNTER_TBL`, `FDA_EXTRACT_MESSAGE_FILE`

### Transformation `SQ_ERROR_TBL` (Source Qualifier)

- **Sql Query**: `SELECT a.PROCESS_NAME, a.ERROR_MESSAGE, a.ERROR_DATE, a.PP_END_YEAR, a.PP_NUM, a.CYCLE_ID FROM ERROR_TBL a, (SELECT b1.PP_END_YEAR, b1.PP_NUM, MAX(b1.ERROR_DATE) as ERROR_DATE, MAX(b1.CYCLE_ID) as CYCLE_ID FROM ERROR_TBL b1 WHERE b1.ERROR_DATE >= TRUNC(SYSDATE) AND b1.PP_END_YEAR = TO_NUMBER('$$MAP_PP_END_YEAR') AND b1.PP_NUM = TO_NUMBER('$$MAP_PP_NUM') AND b1.CYCLE_ID = $$MAP_CYCLE_ID AND b1.PROCESS_NAME = 'm_0150_PM_FDA_Error_Counter' GROUP BY b1.PP_END_YEAR, b1.PP_NUM ) b WHERE a.PP_END_YEAR = b.PP_END_YEAR AND a.PP_NUM = b.PP_NUM AND a.ERROR_DATE = b.ERROR_DATE AND a.CYCLE_ID = b.CYCLE_ID AND a.PROCESS_NAME = 'm_0150_PM_FDA_Error_Counter'`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `SQ_HI_PM_FDA_TATRAN_TBL` (Source Qualifier)

- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `agg_All_Leave_Recs` (Aggregator)

- **Sorted Input**: `NO`

### Transformation `agg_Error_Records` (Aggregator)

- **Sorted Input**: `NO`

### Transformation `fil_Leave_Records` (Filter)

- **Filter Condition**: `FDA_REC_TYPE='02'`

### Transformation `jnr_All_Counts` (Joiner)

- **Join Condition**: `CONSTANT_ERROR = CONSTANT`
- **Join Type**: `Normal Join`
- **Null ordering in master**: `Null Is Highest Value`
- **Null ordering in detail**: `Null Is Highest Value`
- **Sorted Input**: `NO`

### Transformation `lkp_Count_HI_PM_FDA_TATRAN_TBL_ALL` (Lookup Procedure)

- **Lookup Sql Override**: `SELECT COUNT(*) as WRITTEN_REC_COUNT FROM HI_PM_FDA_TATRAN_TBL`
- **Lookup table name**: `HI_PM_FDA_TATRAN_TBL`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `WRITTEN_REC_COUNT >= in_CONSTANT`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `lkp_Count_HI_PM_FDA_TATRAN_TBL_READ` (Lookup Procedure)

- **Lookup Sql Override**: `SELECT COUNT(*) as COUNT_READ_IN FROM HI_PM_FDA_TATRAN_TBL WHERE FDA_SEQ < 1000000`
- **Lookup table name**: `HI_PM_FDA_TATRAN_TBL`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `COUNT_READ_IN >= in_CONSTANT`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `lkp_Curr_Pay_Period` (Lookup Procedure)

- **Lookup table name**: `PAY_PERIOD`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `CURR_PP_FLAG = in_CURR_PP_FLAG`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `nrm_Counters` (Normalizer)

- **Reset**: `NO`
- **Restart**: `NO`

### Transformation `nrm_Counters_Message` (Normalizer)

- **Reset**: `NO`
- **Restart**: `NO`

- Joiner `jnr_All_Counts`: Normal Join ON `CONSTANT_ERROR = CONSTANT`
- Normalizer `nrm_Counters` (vsam=False) occurs: COUNTER_DESCRIPTION×4, COUNTER_VALUE×4, SEQ_NUM×4; generated: GK_COUNTER_DESCRIPTION, GCID_COUNTER_DESCRIPTION, GCID_COUNTER_VALUE, GCID_SEQ_NUM
- Normalizer `nrm_Counters_Message` (vsam=False) occurs: COUNTER_DESCRIPTION×6, COUNTER_VALUE×6; generated: GK_COUNTER_DESCRIPTION, GCID_COUNTER_DESCRIPTION, GCID_COUNTER_VALUE
- Lookup `lkp_Count_HI_PM_FDA_TATRAN_TBL_ALL`: table `HI_PM_FDA_TATRAN_TBL` (exists in export: **True**), condition `WRITTEN_REC_COUNT >= in_CONSTANT`, multiple-match policy `Use Any Value`.
- Lookup `lkp_Count_HI_PM_FDA_TATRAN_TBL_READ`: table `HI_PM_FDA_TATRAN_TBL` (exists in export: **True**), condition `COUNT_READ_IN >= in_CONSTANT`, multiple-match policy `Use Any Value`.
- Lookup `lkp_Curr_Pay_Period`: table `PAY_PERIOD` (exists in export: **True**), condition `CURR_PP_FLAG = in_CURR_PP_FLAG`, multiple-match policy `Use Any Value`.
- SQL override `SQ_ERROR_TBL` positional bindings: 1 → `PROCESS_NAME` = `a.PROCESS_NAME`; 2 → `ERROR_MESSAGE` = `a.ERROR_MESSAGE`; 3 → `SOURCE_KEY` = `a.ERROR_DATE`; 4 → `ERROR_DATE` = `a.PP_END_YEAR`; 5 → `PP_END_YEAR` = `a.PP_NUM`; 6 → `PP_NUM` = `a.CYCLE_ID`

### Target instance `COUNTER_TBL` (table `COUNTER_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| COUNTER_TBL | RUN_DATE | exp_Final_Rec_Insert.o_CTR_TS = SESSSTARTTIME | literal/expression: SESSSTARTTIME |
| COUNTER_TBL | PROCESS_NAME | exp_Final_Rec_Insert.o_CTR_PROCESS = 'FDA EXTRACT' | literal/expression: 'FDA EXTRACT' |
| COUNTER_TBL | COUNTER_DESCRIPTION | exp_Final_Rec_Insert.COUNTER_DESCRIPTION → nrm_Counters.COUNTER_DESCRIPTION [normalizer: one row per occurrence of COUNTER_DESCRIPTION_in1, COUNTER_DESCRIPTION_in2, COUNTER_DESCRIPTION_in3, COUNTER_DESCRIPTION_in4] → exp_Counters.o_COUNTER_DESCR_1 = 'TATRAN Records Read' → exp_Counters.o_COUNTER_DESCR_2 = 'Leave Records Read' → exp_Counters.o_COUNTER_DESCR_3 = 'Error Records' → exp_Counters.o_COUNTER_DESCR_4 = 'New TATRAN Records Written' | literal/expression: 'Error Records'; literal/expression: 'Leave Records Read'; literal/expression: 'New TATRAN Records Written'; literal/expression: 'TATRAN Records Read' |
| COUNTER_TBL | COUNTER_VALUE | exp_Final_Rec_Insert.COUNTER_VALUE → nrm_Counters.COUNTER_VALUE [normalizer: one row per occurrence of COUNTER_VALUE_in1, COUNTER_VALUE_in2, COUNTER_VALUE_in3, COUNTER_VALUE_in4] → exp_Counters.COUNT_READ_IN → jnr_All_Counts.COUNT_READ_IN → exp_Counters1.COUNT_READ_IN → lkp_Count_HI_PM_FDA_TATRAN_TBL_READ.COUNT_READ_IN [lookup HI_PM_FDA_TATRAN_TBL.COUNT_READ_IN ON COUNT_READ_IN >= in_CONSTANT] → exp_Counters.LEAVE_REC_COUNT → jnr_All_Counts.LEAVE_REC_COUNT → exp_Counters1.LEAVE_REC_COUNT → exp_Leave_Rec_Count.LEAVE_REC_COUNT → agg_All_Leave_Recs.o_LEAVE_REC_COUNT = COUNT(*) → exp_Counters.ERROR_REC_COUNT → jnr_All_Counts.ERROR_REC_COUNT → exp_Error_Count.ERROR_REC_COUNT → agg_Error_Records.o_ERROR_REC_COUNT = COUNT(*) → exp_Counters.WRITTEN_REC_COUNT → jnr_All_Counts.WRITTEN_REC_COUNT → exp_Counters1.WRITTEN_REC_COUNT → lkp_Count_HI_PM_FDA_TATRAN_TBL_ALL.WRITTEN_REC_COUNT [lookup HI_PM_FDA_TATRAN_TBL.WRITTEN_REC_COUNT ON WRITTEN_REC_COUNT >= in_CONSTANT] | HI_PM_FDA_TATRAN_TBL.COUNT_READ_IN (lookup); HI_PM_FDA_TATRAN_TBL.WRITTEN_REC_COUNT (lookup); literal/expression: 1 (lookup key); literal/expression: COUNT(*) |
| COUNTER_TBL | PP_END_YEAR | exp_Final_Rec_Insert.o_PP_END_YEAR = TO_DECIMAL($$MAP_PP_END_YEAR, 0) | literal/expression: TO_DECIMAL($$MAP_PP_END_YEAR, 0) |
| COUNTER_TBL | PP_NUM | exp_Final_Rec_Insert.o_PP_NUM = TO_DECIMAL($$MAP_PP_NUM, 0) | literal/expression: TO_DECIMAL($$MAP_PP_NUM, 0) |
| COUNTER_TBL | CYCLE_ID | (not connected — NULL) | — |

### Target instance `FDA_EXTRACT_MESSAGE_FILE` (table `FDA_EXTRACT_MESSAGE_FILE`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| FDA_EXTRACT_MESSAGE_FILE | COUNT_DESC | exp_Final_Message.COUNT_DESC → nrm_Counters_Message.COUNTER_DESCRIPTION [normalizer: one row per occurrence of COUNTER_DESCRIPTION_in1, COUNTER_DESCRIPTION_in2, COUNTER_DESCRIPTION_in3, COUNTER_DESCRIPTION_in4, COUNTER_DESCRIPTION_in5, COUNTER_DESCRIPTION_in6] → exp_Build_Message.TITLE_DESCR_1 → exp_Counters.o_TITLE_DESCR_1 = 'FDA Leave Counts for Pay Period: ' \|\| TO_CHAR(PP_END_YEAR) \|\| '-' \|\| v_PP_NUM → jnr_All_Counts.PP_END_YEAR → exp_Counters1.o_PP_END_YEAR = TO_DECIMAL($$MAP_PP_END_YEAR, 0) → exp_Counters.v_PP_NUM = IIF(PP_NUM < 10, LPAD(TO_CHAR(PP_NUM), 2, '0'), TO_CHAR(PP_NUM) ) → jnr_All_Counts.PP_NUM → exp_Counters1.o_PP_NUM = TO_DECIMAL($$MAP_PP_NUM, 0) → exp_Build_Message.BLANK_DESCR_1 → exp_Counters.o_BLANK_DESCR_1 = ' ' → exp_Build_Message.COUNTER_DESCR_1 → exp_Counters.o_COUNTER_DESCR_1 = 'TATRAN Records Read' → exp_Build_Message.COUNTER_DESCR_2 → exp_Counters.o_COUNTER_DESCR_2 = 'Leave Records Read' → exp_Build_Message.COUNTER_DESCR_3 → exp_Counters.o_COUNTER_DESCR_3 = 'Error Records' → exp_Build_Message.COUNTER_DESCR_4 → exp_Counters.o_COUNTER_DESCR_4 = 'New TATRAN Records Written' | literal/expression: ' '; literal/expression: 'Error Records'; literal/expression: 'Leave Records Read'; literal/expression: 'New TATRAN Records Written'; literal/expression: 'TATRAN Records Read'; literal/expression: TO_DECIMAL($$MAP_PP_END_YEAR, 0); literal/expression: TO_DECIMAL($$MAP_PP_NUM, 0) |
| FDA_EXTRACT_MESSAGE_FILE | COUNT_VALUE | exp_Final_Message.COUNT_VALUE → nrm_Counters_Message.COUNTER_VALUE [normalizer: one row per occurrence of COUNTER_VALUE_in1, COUNTER_VALUE_in2, COUNTER_VALUE_in3, COUNTER_VALUE_in4, COUNTER_VALUE_in5, COUNTER_VALUE_in6] → exp_Build_Message.TITLE_COUNTER_VALUE_1 → exp_Counters.o_TITLE_COUNTER_VALUE_1 → exp_Build_Message.BLANK_COUNTER_VALUE_1 → exp_Counters.o_BLANK_COUNTER_VALUE_1 → exp_Build_Message.COUNT_READ_IN → exp_Counters.COUNT_READ_IN → jnr_All_Counts.COUNT_READ_IN → exp_Counters1.COUNT_READ_IN → lkp_Count_HI_PM_FDA_TATRAN_TBL_READ.COUNT_READ_IN [lookup HI_PM_FDA_TATRAN_TBL.COUNT_READ_IN ON COUNT_READ_IN >= in_CONSTANT] → exp_Build_Message.LEAVE_REC_COUNT → exp_Counters.LEAVE_REC_COUNT → jnr_All_Counts.LEAVE_REC_COUNT → exp_Counters1.LEAVE_REC_COUNT → exp_Leave_Rec_Count.LEAVE_REC_COUNT → agg_All_Leave_Recs.o_LEAVE_REC_COUNT = COUNT(*) → exp_Build_Message.ERROR_REC_COUNT → exp_Counters.ERROR_REC_COUNT → jnr_All_Counts.ERROR_REC_COUNT → exp_Error_Count.ERROR_REC_COUNT → agg_Error_Records.o_ERROR_REC_COUNT = COUNT(*) → exp_Build_Message.WRITTEN_REC_COUNT → exp_Counters.WRITTEN_REC_COUNT → jnr_All_Counts.WRITTEN_REC_COUNT → exp_Counters1.WRITTEN_REC_COUNT → lkp_Count_HI_PM_FDA_TATRAN_TBL_ALL.WRITTEN_REC_COUNT [lookup HI_PM_FDA_TATRAN_TBL.WRITTEN_REC_COUNT ON WRITTEN_REC_COUNT >= in_CONSTANT] | HI_PM_FDA_TATRAN_TBL.COUNT_READ_IN (lookup); HI_PM_FDA_TATRAN_TBL.WRITTEN_REC_COUNT (lookup); literal/expression: 1 (lookup key); literal/expression: COUNT(*) |

## Mapping `m_1100_PM_FDA_Send_Email`

- Sessions: `s_1100_PM_FDA_Send_Email` (#10)
- Sources: `HI_GENERIC_SRC_TBL`
- Target instances: `GENERIC_TARGET_FILE`

### Transformation `SQ_HI_GENERIC_SRC_TBL` (Source Qualifier)

- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`


### Target instance `GENERIC_TARGET_FILE` (table `GENERIC_TARGET_FILE`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| GENERIC_TARGET_FILE | ID | SQ_HI_GENERIC_SRC_TBL.ID → HI_GENERIC_SRC_TBL.ID | HI_GENERIC_SRC_TBL.ID |

