# PowerCenter STM: `CPM`

Derived deterministically from `legacy/informatica_ts/CPM_NIH` by `tools/ts_lineage.py`. Personal identifiers are redacted as `<owner>`, `<path>`, `<email>`.

| Mappings | Sessions | Sources | Targets | Transformations | Mapplets |
|---|---|---|---|---|---|
| 6 | 6 | 3 | 6 | 30 | 0 |

Transformations by type: Aggregator 1, Expression 17, Lookup Procedure 6, Source Qualifier 6

## Workflow `wf_CPM_NIH`

Session order:

1. `s_CPM_NIH_Set_CPM_Calendar` → mapping `m_CPM_NIH_Set_CPM_Calendar`
2. `s_CPM_NIH_Set_Pay_Calendar` → mapping `m_CPM_NIH_Set_Pay_Calendar`
3. `s_CPM_NIH_Load_CPM_NIH_Header_File` → mapping `m_CPM_NIH_Load_CPM_NIH_Header_File`
4. `s_CPM_NIH_Load_CPM_NIH_Data_File` → mapping `m_CPM_NIH_Load_CPM_NIH_Data_File`
5. `s_CPM_NIH_Concatenate_Files` → mapping `m_CPM_NIH_Concatenate_Files`
6. `s_CPM_NIH_Build_Message` → mapping `m_CPM_NIH_Build_Message`

| From | To | Condition |
|---|---|---|
| s_CPM_NIH_Set_CPM_Calendar | s_CPM_NIH_Set_Pay_Calendar | $s_CPM_NIH_Set_CPM_Calendar.Status = Succeeded |
| s_CPM_NIH_Build_Message | email_CPM_NIH | $s_CPM_NIH_Build_Message.Status = Succeeded |
| s_CPM_NIH_Load_CPM_NIH_Data_File | s_CPM_NIH_Concatenate_Files | $s_CPM_NIH_Load_CPM_NIH_Data_File.Status = Succeeded |
| Start | s_CPM_NIH_Set_CPM_Calendar | — |
| s_CPM_NIH_Load_CPM_NIH_Header_File | s_CPM_NIH_Load_CPM_NIH_Data_File | $s_CPM_NIH_Load_CPM_NIH_Header_File.Status = Succeeded |
| s_CPM_NIH_Set_Pay_Calendar | s_CPM_NIH_Load_CPM_NIH_Header_File | $s_CPM_NIH_Set_Pay_Calendar.Status = Succeeded |
| s_CPM_NIH_Concatenate_Files | s_CPM_NIH_Build_Message | $s_CPM_NIH_Concatenate_Files.Status = Succeeded |

Command tasks:

- `s_CPM_NIH_Set_Pay_Calendar` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_CPM_NIH_Concatenate_Files` / Pre-session command `pre_session_command`: `Command1` = `$Param_ControlDir/scripts/remove_file.sh $Param_Root_Directory/data/int/out/CPM $Param_CPM_NIH_out_filename`
- `s_CPM_NIH_Concatenate_Files` / Post-session success command `post_session_success_command`: `Command1` = `cd $Param_Root_Directory/data/int/out/CPM; cat $Param_CPM_NIH_HDR_filename $Param_CPM_NIH_DAT_filename > $Param_CPM_NIH_out_filename`
- `s_CPM_NIH_Set_CPM_Calendar` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`; `$$MAP_PP_YEAR_NUM` = `$$WF_PP_YEAR_NUM`
- `s_CPM_NIH_Set_CPM_Calendar` / Post-session success variable assignment `postsession_success_variable_assignment`: `$$WF_PP_END_YEAR` = `$$MAP_PP_END_YEAR`; `$$WF_PP_NUM` = `$$MAP_PP_NUM`; `$$WF_PP_YEAR_NUM` = `$$MAP_PP_YEAR_NUM`
- `s_CPM_NIH_Load_CPM_NIH_Data_File` / Pre-session command `pre_session_command`: `Command1` = `$Param_ControlDir/scripts/remove_file.sh $Param_Root_Directory/data/int/out/CPM $Param_CPM_NIH_DAT_filename`
- `s_CPM_NIH_Load_CPM_NIH_Data_File` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_CPM_NIH_Load_CPM_NIH_Header_File` / Pre-session command `pre_session_command`: `Command1` = `$Param_ControlDir/scripts/remove_file.sh $Param_Root_Directory/data/int/out/CPM $Param_CPM_NIH_HDR_filename`
- `s_CPM_NIH_Load_CPM_NIH_Header_File` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_CPM_NIH_Build_Message` / Post-session success command `post_session_success_command`: `Command1` = `cd $Param_Root_Directory/data/int/out/CPM; cp $Param_CPM_NIH_out_filename NIHPAYMASTER.PP$$WF_PP_YEAR_NUM`; `Command2` = `<path>/scripts/nih_cpm_transfer.sh NIHPAYMASTER.PP$$WF_PP_YEAR_NUM`
- `s_CPM_NIH_Build_Message` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_SUBJECT` = `$$WF_SUBJECT`; `$$MAP_MESSAGE` = `$$WF_MESSAGE`; `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_CPM_NIH_Build_Message` / Post-session success variable assignment `postsession_success_variable_assignment`: `$$WF_SUBJECT` = `$$MAP_SUBJECT`; `$$WF_MESSAGE` = `$$MAP_MESSAGE`

- Session `s_CPM_NIH_Set_CPM_Calendar`: WRITER `CPM_NIH_CPM_PAY_PERIOD_FILE` Append if Exists=`NO`, Output Type=`File`, Output file directory=`$PMTargetFileDir\`, Output filename=`cpm_nih_cpm_pay_period_file.txt`
- Session `s_CPM_NIH_Set_Pay_Calendar`: WRITER `CPM_NIH_PAY_PERIOD_FILE` Append if Exists=`NO`, Output Type=`File`, Output file directory=`$PMTargetFileDir\`, Output filename=`cpm_nih_pay_period_file.txt`
- Session `s_CPM_NIH_Load_CPM_NIH_Header_File`: WRITER `nihhdr_WS_NIH_HDR` File Name Override=`$Param_Root_Directory/data/int/out/CPM/$Param_CPM_NIH_HDR_filename`
- Session `s_CPM_NIH_Load_CPM_NIH_Data_File`: WRITER `nihtest_NIH_PAYROLL_MASTER` File Name Override=`$Param_Root_Directory/data/int/out/CPM/$Param_CPM_NIH_DAT_filename`
- Session `s_CPM_NIH_Concatenate_Files`: WRITER `GENERIC_TARGET_FILE` Append if Exists=`NO`, Output Type=`File`, Output file directory=`$PMTargetFileDir\`, Output filename=`generic_target_file.txt`
- Session `s_CPM_NIH_Build_Message`: WRITER `CPM_NIH_MESSAGE_FILE` Append if Exists=`NO`, Output Type=`File`, Output file directory=`$PMTargetFileDir\`, Output filename=`cpm_nih_message_file.txt`

## Source definitions

| Source | Database type | Fields |
|---|---|---|
| CPM_NEWPAY_TBL | Oracle | 501 |
| HI_GENERIC_SRC_TBL | Oracle | 1 |
| PAY_PERIOD | Oracle | 10 |

## Target definitions

| Target | Database type | Fields |
|---|---|---|
| CPM_NIH_CPM_PAY_PERIOD_FILE | Flat File | 1 |
| CPM_NIH_MESSAGE_FILE | Flat File | 2 |
| CPM_NIH_PAY_PERIOD_FILE | Flat File | 1 |
| GENERIC_TARGET_FILE | Flat File | 1 |
| nihhdr_WS_NIH_HDR | PWX_SEQ_NRDB2 | 18 |
| nihtest_NIH_PAYROLL_MASTER | PWX_SEQ_NRDB2 | 534 |

## Mapping `m_CPM_NIH_Set_CPM_Calendar`

- Sessions: `s_CPM_NIH_Set_CPM_Calendar` (#1)
- Sources: `PAY_PERIOD1`
- Target instances: `CPM_NIH_CPM_PAY_PERIOD_FILE`

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

### Target instance `CPM_NIH_CPM_PAY_PERIOD_FILE` (table `CPM_NIH_CPM_PAY_PERIOD_FILE`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| CPM_NIH_CPM_PAY_PERIOD_FILE | CPM_PAY_PERIOD | exp_Final.o_CPM_PAY_PERIOD = PARAM_PP_END_YEAR \|\| '-' \|\| LPAD(PARAM_PP_NUM, 2, '0') → exp_Validate_Parameters.PARAM_PP_END_YEAR → exp_Set_Parameters.o_PARAM_PP_END_YEAR = SETVARIABLE($$MAP_PP_END_YEAR, TO_CHAR(v_PP_END_YEAR)) → exp_Set_Parameters.v_PP_END_YEAR = DECODE(TRUE, v_DEFAULT_TO_CURR_PP_FLAG = TRUE, lkp_CURR_PP_END_YEAR, v_PAY_PERIOD_PARAM_EXISTS_FLAG = TRUE, PARAM_PP_END_YEAR ) --IIF(v_PAY_PERIOD_PARAM_EXISTS_FLAG = TRUE, -- TO_CHAR(PARAM_PP_END_YEAR), -- TO_CHAR(lkp_CURR_PP_END_YEAR)) → exp_Set_Parameters.v_DEFAULT_TO_CURR_PP_FLAG = DECODE(TRUE, (ISNULL(INIT_PARAM_PP_END_YEAR) OR IS_SPACES(INIT_PARAM_PP_END_YEAR) OR LENGTH(LTRIM(INIT_PARAM_PP_END_YEAR)) = 0) AND (ISNULL(INIT_PARAM_PP_NUM) OR IS_SPACES(INIT_PARAM_PP_NUM) OR LENGTH(LTRIM(INIT_PARAM_PP_NUM)) = 0), TRUE, FALSE) → exp_Initial.o_INIT_PARAM_PP_END_YEAR = $$MAP_PP_END_YEAR → exp_Initial.o_INIT_PARAM_PP_NUM = $$MAP_PP_NUM → lkp_Current_Pay_Period.PP_END_YEAR [lookup PAY_PERIOD.PP_END_YEAR ON CURR_PP_FLAG = in_CURR_PP_FLAG] → exp_Set_Parameters.v_PAY_PERIOD_PARAM_EXISTS_FLAG = IIF(NOT ISNULL(lkp_PP_NUM), TRUE, FALSE) → lkp_Existing_Pay_Period.PP_NUM [lookup PAY_PERIOD.PP_NUM ON PP_NUM = in_PARAM_PP_NUM AND PP_END_YEAR = in_PARAM_PP_END_YEAR] → exp_Initial.o_PARAM_PP_END_YEAR = v_PARAM_PP_END_YEAR → exp_Initial.v_PARAM_PP_END_YEAR = IIF(NOT IS_NUMBER($$MAP_PP_END_YEAR), 0, TO_DECIMAL($$MAP_PP_END_YEAR)) → exp_Validate_Parameters.PARAM_PP_NUM → exp_Set_Parameters.o_PARAM_PP_NUM = SETVARIABLE($$MAP_PP_NUM, TO_CHAR(v_PP_NUM)) → exp_Set_Parameters.v_PP_NUM = DECODE(TRUE, v_DEFAULT_TO_CURR_PP_FLAG = TRUE, lkp_CURR_PP_NUM, v_PAY_PERIOD_PARAM_EXISTS_FLAG = TRUE, PARAM_PP_NUM ) --IIF(v_PAY_PERIOD_PARAM_EXISTS_FLAG = TRUE, -- TO_CHAR(PARAM_PP_NUM), -- TO_CHAR(lkp_CURR_PP_NUM)) → lkp_Current_Pay_Period.PP_NUM [lookup PAY_PERIOD.PP_NUM ON CURR_PP_FLAG = in_CURR_PP_FLAG] → exp_Initial.o_PARAM_PP_NUM = v_PARAM_PP_NUM → exp_Initial.v_PARAM_PP_NUM = IIF(NOT IS_NUMBER($$MAP_PP_NUM), 0, TO_DECIMAL($$MAP_PP_NUM)) | PAY_PERIOD.PP_END_YEAR (lookup); PAY_PERIOD.PP_NUM (lookup); literal/expression: $$MAP_PP_END_YEAR; literal/expression: $$MAP_PP_NUM; literal/expression: 'Y' (lookup key); literal/expression: IIF(NOT IS_NUMBER($$MAP_PP_END_YEAR), 0, TO_DECIMAL($$MAP_PP_END_YEAR)); literal/expression: IIF(NOT IS_NUMBER($$MAP_PP_END_YEAR), 0, TO_DECIMAL($$MAP_PP_END_YEAR)) (lookup key); literal/expression: IIF(NOT IS_NUMBER($$MAP_PP_NUM), 0, TO_DECIMAL($$MAP_PP_NUM)); literal/expression: IIF(NOT IS_NUMBER($$MAP_PP_NUM), 0, TO_DECIMAL($$MAP_PP_NUM)) (lookup key) |

## Mapping `m_CPM_NIH_Set_Pay_Calendar`

- Sessions: `s_CPM_NIH_Set_Pay_Calendar` (#2)
- Sources: `PAY_PERIOD1`
- Target instances: `CPM_NIH_PAY_PERIOD_FILE`

### Transformation `SQ_PAY_PERIOD` (Source Qualifier)

- **Sql Query**: `SELECT MAX(PAY_PERIOD.PP_NUM) PP_NUM , MAX(PAY_PERIOD.PP_END_YEAR) PP_END_YEAR FROM PAY_PERIOD`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `lkp_CPM_NEWPAY_TBL` (Lookup Procedure)

- **Lookup table name**: `CPM_NEWPAY_TBL`
- **Lookup Source Filter**: `PP_END_YEAR = TO_NUMBER('$$MAP_PP_END_YEAR') AND PP_NUM = TO_NUMBER('$$MAP_PP_NUM') AND BUSINESS_UNIT = 'NIH00'`
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

- Lookup `lkp_CPM_NEWPAY_TBL`: table `CPM_NEWPAY_TBL` (exists in export: **True**), condition `PP_END_YEAR = in_PARAM_PP_END_YEAR AND PP_NUM = in_PARAM_PP_NUM AND MP_POOL_DES = in_MP_POOL_DES`, multiple-match policy `Use Any Value`.
- Lookup `lkp_Current_Pay_Period`: table `PAY_PERIOD` (exists in export: **True**), condition `CURR_PP_FLAG = in_CURR_PP_FLAG`, multiple-match policy `Use Any Value`.
- Lookup `lkp_Existing_Pay_Period`: table `PAY_PERIOD` (exists in export: **True**), condition `PP_NUM = in_PARAM_PP_NUM AND PP_END_YEAR = in_PARAM_PP_END_YEAR`, multiple-match policy `Use Any Value`.
- SQL override `SQ_PAY_PERIOD` positional bindings: 1 → `PP_NUM` = `MAX(PAY_PERIOD.PP_NUM) PP_NUM`; 2 → `PP_END_YEAR` = `MAX(PAY_PERIOD.PP_END_YEAR) PP_END_YEAR`

### Target instance `CPM_NIH_PAY_PERIOD_FILE` (table `CPM_NIH_PAY_PERIOD_FILE`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| CPM_NIH_PAY_PERIOD_FILE | CPM_PAY_PERIOD | exp_Final.o_CPM_PAY_PERIOD = PARAM_PP_END_YEAR \|\| '-' \|\| LPAD(PARAM_PP_NUM, 2, '0') → exp_Validate_Parameters.PARAM_PP_END_YEAR → exp_Set_Parameters.o_PARAM_PP_END_YEAR = SETVARIABLE($$MAP_PP_END_YEAR, TO_CHAR(v_PP_END_YEAR)) → exp_Set_Parameters.v_PP_END_YEAR = DECODE(TRUE, v_DEFAULT_TO_CURR_PP_FLAG = TRUE, lkp_CURR_PP_END_YEAR, v_PAY_PERIOD_PARAM_EXISTS_FLAG = TRUE, PARAM_PP_END_YEAR ) --IIF(v_PAY_PERIOD_PARAM_EXISTS_FLAG = TRUE, -- TO_CHAR(PARAM_PP_END_YEAR), -- TO_CHAR(lkp_CURR_PP_END_YEAR)) → exp_Set_Parameters.v_DEFAULT_TO_CURR_PP_FLAG = DECODE(TRUE, (ISNULL(INIT_PARAM_PP_END_YEAR) OR IS_SPACES(INIT_PARAM_PP_END_YEAR) OR LENGTH(LTRIM(INIT_PARAM_PP_END_YEAR)) = 0) AND (ISNULL(INIT_PARAM_PP_NUM) OR IS_SPACES(INIT_PARAM_PP_NUM) OR LENGTH(LTRIM(INIT_PARAM_PP_NUM)) = 0), TRUE, FALSE) → exp_Initial.o_INIT_PARAM_PP_END_YEAR = $$MAP_PP_END_YEAR → exp_Initial.o_INIT_PARAM_PP_NUM = $$MAP_PP_NUM → lkp_Current_Pay_Period.PP_END_YEAR [lookup PAY_PERIOD.PP_END_YEAR ON CURR_PP_FLAG = in_CURR_PP_FLAG] → exp_Set_Parameters.v_PAY_PERIOD_PARAM_EXISTS_FLAG = IIF(NOT ISNULL(lkp_PP_NUM), TRUE, FALSE) → lkp_Existing_Pay_Period.PP_NUM [lookup PAY_PERIOD.PP_NUM ON PP_NUM = in_PARAM_PP_NUM AND PP_END_YEAR = in_PARAM_PP_END_YEAR] → exp_Initial.o_PARAM_PP_END_YEAR = v_PARAM_PP_END_YEAR → exp_Initial.v_PARAM_PP_END_YEAR = IIF(NOT IS_NUMBER($$MAP_PP_END_YEAR), 0, TO_DECIMAL($$MAP_PP_END_YEAR)) → exp_Validate_Parameters.PARAM_PP_NUM → exp_Set_Parameters.o_PARAM_PP_NUM = SETVARIABLE($$MAP_PP_NUM, TO_CHAR(v_PP_NUM)) → exp_Set_Parameters.v_PP_NUM = DECODE(TRUE, v_DEFAULT_TO_CURR_PP_FLAG = TRUE, lkp_CURR_PP_NUM, v_PAY_PERIOD_PARAM_EXISTS_FLAG = TRUE, PARAM_PP_NUM ) --IIF(v_PAY_PERIOD_PARAM_EXISTS_FLAG = TRUE, -- TO_CHAR(PARAM_PP_NUM), -- TO_CHAR(lkp_CURR_PP_NUM)) → lkp_Current_Pay_Period.PP_NUM [lookup PAY_PERIOD.PP_NUM ON CURR_PP_FLAG = in_CURR_PP_FLAG] → exp_Initial.o_PARAM_PP_NUM = v_PARAM_PP_NUM → exp_Initial.v_PARAM_PP_NUM = IIF(NOT IS_NUMBER($$MAP_PP_NUM), 0, TO_DECIMAL($$MAP_PP_NUM)) | PAY_PERIOD.PP_END_YEAR (lookup); PAY_PERIOD.PP_NUM (lookup); literal/expression: $$MAP_PP_END_YEAR; literal/expression: $$MAP_PP_NUM; literal/expression: 'Y' (lookup key); literal/expression: IIF(NOT IS_NUMBER($$MAP_PP_END_YEAR), 0, TO_DECIMAL($$MAP_PP_END_YEAR)); literal/expression: IIF(NOT IS_NUMBER($$MAP_PP_END_YEAR), 0, TO_DECIMAL($$MAP_PP_END_YEAR)) (lookup key); literal/expression: IIF(NOT IS_NUMBER($$MAP_PP_NUM), 0, TO_DECIMAL($$MAP_PP_NUM)); literal/expression: IIF(NOT IS_NUMBER($$MAP_PP_NUM), 0, TO_DECIMAL($$MAP_PP_NUM)) (lookup key) |

## Mapping `m_CPM_NIH_Load_CPM_NIH_Header_File`

- Sessions: `s_CPM_NIH_Load_CPM_NIH_Header_File` (#3)
- Sources: `PAY_PERIOD`
- Target instances: `nihhdr_WS_NIH_HDR`

### Transformation `SQ_PAY_PERIOD` (Source Qualifier)

- **Source Filter**: `PAY_PERIOD.PP_END_YEAR = TO_NUMBER('$$MAP_PP_END_YEAR') AND PAY_PERIOD.PP_NUM = TO_NUMBER('$$MAP_PP_NUM')`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`


### Target instance `nihhdr_WS_NIH_HDR` (table `nihhdr_WS_NIH_HDR`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| nihhdr_WS_NIH_HDR | HDR_SOC_SEC | exp_Final.HDR_SOC_SEC → exp_Initial.o_HDR_SOC_SEC = 0 | literal/expression: 0 |
| nihhdr_WS_NIH_HDR | HDR_FNAME | (not connected — NULL) | — |
| nihhdr_WS_NIH_HDR | HDR_INITIAL | (not connected — NULL) | — |
| nihhdr_WS_NIH_HDR | HDR_LNAME | exp_Final.HDR_LNAME → exp_Initial.o_HDR_LNAME = 'REGULAR' | literal/expression: 'REGULAR' |
| nihhdr_WS_NIH_HDR | HDR_PP_NUMBER | exp_Final.HDR_PP_NUMBER → exp_Initial.o_HDR_PP_NUMBER = LPAD(TO_CHAR(TO_INTEGER(PP_NUM)), 2, '0') → SQ_PAY_PERIOD.PP_NUM → PAY_PERIOD.PP_NUM | PAY_PERIOD.PP_NUM |
| nihhdr_WS_NIH_HDR | HDR_LVII_NUMBER | exp_Final.HDR_LVII_NUMBER → exp_Initial.o_HDR_LVII_NUMBER = '15' | literal/expression: '15' |
| nihhdr_WS_NIH_HDR | LVIISITE_1 | exp_Final.LVIISITE_1 → exp_Initial.o_LVIISITE_1 = '08' | literal/expression: '08' |
| nihhdr_WS_NIH_HDR | LVIISITE_2 | exp_Final.LVIISITE_2 → exp_Initial.o_LVIISITE_2 = '10' | literal/expression: '10' |
| nihhdr_WS_NIH_HDR | LVIISITE_3 | exp_Final.LVIISITE_3 → exp_Initial.o_LVIISITE_3 = '17' | literal/expression: '17' |
| nihhdr_WS_NIH_HDR | LVIISITE_4 | exp_Final.LVIISITE_4 → exp_Initial.o_LVIISITE_4 = '39' | literal/expression: '39' |
| nihhdr_WS_NIH_HDR | LVIISITE_5 | exp_Final.LVIISITE_5 → exp_Initial.o_LVIISITE_5 = '41' | literal/expression: '41' |
| nihhdr_WS_NIH_HDR | LVIISITE_6 | exp_Final.LVIISITE_6 → exp_Initial.o_LVIISITE_6 = '46' | literal/expression: '46' |
| nihhdr_WS_NIH_HDR | LVIISITE_7 | exp_Final.LVIISITE_7 → exp_Initial.o_LVIISITE_7 = '50' | literal/expression: '50' |
| nihhdr_WS_NIH_HDR | LVIISITE_8 | exp_Final.LVIISITE_8 → exp_Initial.o_LVIISITE_8 = '51' | literal/expression: '51' |
| nihhdr_WS_NIH_HDR | LVIISITE_9 | exp_Final.LVIISITE_9 → exp_Initial.o_LVIISITE_9 = '90' | literal/expression: '90' |
| nihhdr_WS_NIH_HDR | LVIISITE_10 | exp_Final.LVIISITE_10 → exp_Initial.o_LVIISITE_10 = '93' | literal/expression: '93' |
| nihhdr_WS_NIH_HDR | TAPE_NUMBER | exp_Final.TAPE_NUMBER → exp_Initial.o_TAPE_NUMBER = 1 | literal/expression: 1 |
| nihhdr_WS_NIH_HDR | FILLER_1 | (not connected — NULL) | — |

## Mapping `m_CPM_NIH_Load_CPM_NIH_Data_File`

- Sessions: `s_CPM_NIH_Load_CPM_NIH_Data_File` (#4)
- Sources: `CPM_NEWPAY_TBL`
- Target instances: `nihtest_NIH_PAYROLL_MASTER`

### Transformation `SQ_CPM_NEWPAY_TBL` (Source Qualifier)

- **User Defined Join**: `CPM_NEWPAY_TBL.PP_END_YEAR = TO_NUMBER('$$MAP_PP_END_YEAR') AND CPM_NEWPAY_TBL.PP_NUM = TO_NUMBER('$$MAP_PP_NUM') AND CPM_NEWPAY_TBL.MP_POOL_DES = ' ' AND CPM_NEWPAY_TBL.BUSINESS_UNIT = 'NIH00'`
- **Number Of Sorted Ports**: `3`
- **Select Distinct**: `NO`


### Target instance `nihtest_NIH_PAYROLL_MASTER` (table `nihtest_NIH_PAYROLL_MASTER`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| nihtest_NIH_PAYROLL_MASTER | SOC_SEC_NO | exp_Final.SOC_SEC_NO → exp_Init.SOC_SEC_NO → SQ_CPM_NEWPAY_TBL.SOC_SEC_NO → CPM_NEWPAY_TBL.SOC_SEC_NO | CPM_NEWPAY_TBL.SOC_SEC_NO |
| nihtest_NIH_PAYROLL_MASTER | FIR_NAME_1 | exp_Final.FIR_NAME_1 → exp_Init.FIR_NAME_1 → SQ_CPM_NEWPAY_TBL.FIR_NAME_1 → CPM_NEWPAY_TBL.FIR_NAME_1 | CPM_NEWPAY_TBL.FIR_NAME_1 |
| nihtest_NIH_PAYROLL_MASTER | CODE_CONSL | exp_Final.CODE_CONSL → exp_Init.CODE_CONSL → SQ_CPM_NEWPAY_TBL.CODE_CONSL → CPM_NEWPAY_TBL.CODE_CONSL | CPM_NEWPAY_TBL.CODE_CONSL |
| nihtest_NIH_PAYROLL_MASTER | FILLER_1 | exp_Final.FILLER_1 → exp_Init.FIR_NAME_3_11 → SQ_CPM_NEWPAY_TBL.FIR_NAME_3_11 → CPM_NEWPAY_TBL.FIR_NAME_3_11 | CPM_NEWPAY_TBL.FIR_NAME_3_11 |
| nihtest_NIH_PAYROLL_MASTER | MID_INIT | exp_Final.MID_INIT → exp_Init.MID_INIT → SQ_CPM_NEWPAY_TBL.MID_INIT → CPM_NEWPAY_TBL.MID_INIT | CPM_NEWPAY_TBL.MID_INIT |
| nihtest_NIH_PAYROLL_MASTER | SURNAME_3 | exp_Final.SURNAME_3 → exp_Init.SURNAME_3 → SQ_CPM_NEWPAY_TBL.SURNAME_3 → CPM_NEWPAY_TBL.SURNAME_3 | CPM_NEWPAY_TBL.SURNAME_3 |
| nihtest_NIH_PAYROLL_MASTER | SURNAME_OTHER | exp_Final.SURNAME_OTHER → exp_Init.SURNAME_OTHER → SQ_CPM_NEWPAY_TBL.SURNAME_OTHER → CPM_NEWPAY_TBL.SURNAME_OTHER | CPM_NEWPAY_TBL.SURNAME_OTHER |
| nihtest_NIH_PAYROLL_MASTER | ST_CONT_LOC | exp_Final.ST_CONT_LOC → exp_Init.ST_CONT_LOC → SQ_CPM_NEWPAY_TBL.ST_CONT_LOC → CPM_NEWPAY_TBL.ST_CONT_LOC | CPM_NEWPAY_TBL.ST_CONT_LOC |
| nihtest_NIH_PAYROLL_MASTER | CITY_LOC | exp_Final.CITY_LOC → exp_Init.CITY_LOC → SQ_CPM_NEWPAY_TBL.CITY_LOC → CPM_NEWPAY_TBL.CITY_LOC | CPM_NEWPAY_TBL.CITY_LOC |
| nihtest_NIH_PAYROLL_MASTER | CTY_CTRY_LOC | exp_Final.CTY_CTRY_LOC → exp_Init.CTY_CTRY_LOC → SQ_CPM_NEWPAY_TBL.CTY_CTRY_LOC → CPM_NEWPAY_TBL.CTY_CTRY_LOC | CPM_NEWPAY_TBL.CTY_CTRY_LOC |
| nihtest_NIH_PAYROLL_MASTER | CAN_FY | exp_Final.CAN_FY → exp_Init.CAN_FY → SQ_CPM_NEWPAY_TBL.CAN_FY → CPM_NEWPAY_TBL.CAN_FY | CPM_NEWPAY_TBL.CAN_FY |
| nihtest_NIH_PAYROLL_MASTER | CAN_AGCY | exp_Final.CAN_AGCY → exp_Init.CAN_AGCY → SQ_CPM_NEWPAY_TBL.CAN_AGCY → CPM_NEWPAY_TBL.CAN_AGCY | CPM_NEWPAY_TBL.CAN_AGCY |
| nihtest_NIH_PAYROLL_MASTER | CAN_AP | exp_Final.CAN_AP → exp_Init.CAN_AP → SQ_CPM_NEWPAY_TBL.CAN_AP → CPM_NEWPAY_TBL.CAN_AP | CPM_NEWPAY_TBL.CAN_AP |
| nihtest_NIH_PAYROLL_MASTER | CAN_AGCY_ACCT_CDE | exp_Final.CAN_AGCY_ACCT_CDE → exp_Init.CAN_AGCY_ACCT_CDE → SQ_CPM_NEWPAY_TBL.CAN_AGCY_ACCT_CDE → CPM_NEWPAY_TBL.CAN_AGCY_ACCT_CDE | CPM_NEWPAY_TBL.CAN_AGCY_ACCT_CDE |
| nihtest_NIH_PAYROLL_MASTER | ORG_CDE | exp_Final.ORG_CDE → exp_Init.ORG_CDE → SQ_CPM_NEWPAY_TBL.ORG_CDE → CPM_NEWPAY_TBL.ORG_CDE | CPM_NEWPAY_TBL.ORG_CDE |
| nihtest_NIH_PAYROLL_MASTER | SEX_CDE | exp_Final.SEX_CDE → exp_Init.SEX_CDE → SQ_CPM_NEWPAY_TBL.SEX_CDE → CPM_NEWPAY_TBL.SEX_CDE | CPM_NEWPAY_TBL.SEX_CDE |
| nihtest_NIH_PAYROLL_MASTER | VET_PREF_CDE | exp_Final.VET_PREF_CDE → exp_Init.VET_PREF_CDE → SQ_CPM_NEWPAY_TBL.VET_PREF_CDE → CPM_NEWPAY_TBL.VET_PREF_CDE | CPM_NEWPAY_TBL.VET_PREF_CDE |
| nihtest_NIH_PAYROLL_MASTER | TENURE_CDE | exp_Final.TENURE_CDE → exp_Init.TENURE_CDE → SQ_CPM_NEWPAY_TBL.TENURE_CDE → CPM_NEWPAY_TBL.TENURE_CDE | CPM_NEWPAY_TBL.TENURE_CDE |
| nihtest_NIH_PAYROLL_MASTER | PERM_TEMP_POS_CDE | exp_Final.PERM_TEMP_POS_CDE → exp_Init.PERM_TEMP_POS_CDE → SQ_CPM_NEWPAY_TBL.PERM_TEMP_POS_CDE → CPM_NEWPAY_TBL.PERM_TEMP_POS_CDE | CPM_NEWPAY_TBL.PERM_TEMP_POS_CDE |
| nihtest_NIH_PAYROLL_MASTER | FT_PT_INTER_POS_CDE | exp_Final.FT_PT_INTER_POS_CDE → exp_Init.FT_PT_INTER_POS_CDE → SQ_CPM_NEWPAY_TBL.FT_PT_INTER_POS_CDE → CPM_NEWPAY_TBL.FT_PT_INTER_POS_CDE | CPM_NEWPAY_TBL.FT_PT_INTER_POS_CDE |
| nihtest_NIH_PAYROLL_MASTER | CITIZEN_CDE | exp_Final.CITIZEN_CDE → exp_Init.CITIZEN_CDE → SQ_CPM_NEWPAY_TBL.CITIZEN_CDE → CPM_NEWPAY_TBL.CITIZEN_CDE | CPM_NEWPAY_TBL.CITIZEN_CDE |
| nihtest_NIH_PAYROLL_MASTER | TYPE_APPT_CDE | exp_Final.TYPE_APPT_CDE → exp_Init.TYPE_APPT_CDE → SQ_CPM_NEWPAY_TBL.TYPE_APPT_CDE → CPM_NEWPAY_TBL.TYPE_APPT_CDE | CPM_NEWPAY_TBL.TYPE_APPT_CDE |
| nihtest_NIH_PAYROLL_MASTER | PERS_NOA | exp_Final.PERS_NOA → exp_Init.PERS_NOA → SQ_CPM_NEWPAY_TBL.PERS_NOA → CPM_NEWPAY_TBL.PERS_NOA | CPM_NEWPAY_TBL.PERS_NOA |
| nihtest_NIH_PAYROLL_MASTER | SEP_CDE | exp_Final.SEP_CDE → exp_Init.SEP_CDE → SQ_CPM_NEWPAY_TBL.SEP_CDE → CPM_NEWPAY_TBL.SEP_CDE | CPM_NEWPAY_TBL.SEP_CDE |
| nihtest_NIH_PAYROLL_MASTER | CEILING_EN_CDE | exp_Final.CEILING_EN_CDE → exp_Init.CEILING_EN_CDE → SQ_CPM_NEWPAY_TBL.CEILING_EN_CDE → CPM_NEWPAY_TBL.CEILING_EN_CDE | CPM_NEWPAY_TBL.CEILING_EN_CDE |
| nihtest_NIH_PAYROLL_MASTER | FUNC_CDE | exp_Final.FUNC_CDE → exp_Init.FUNC_CDE → SQ_CPM_NEWPAY_TBL.FUNC_CDE → CPM_NEWPAY_TBL.FUNC_CDE | CPM_NEWPAY_TBL.FUNC_CDE |
| nihtest_NIH_PAYROLL_MASTER | PAY_BASIS | exp_Final.PAY_BASIS → exp_Init.PAY_BASIS → SQ_CPM_NEWPAY_TBL.PAY_BASIS → CPM_NEWPAY_TBL.PAY_BASIS | CPM_NEWPAY_TBL.PAY_BASIS |
| nihtest_NIH_PAYROLL_MASTER | SPO_TERM_ID | exp_Final.SPO_TERM_ID → exp_Init.SPO_TERM_ID → SQ_CPM_NEWPAY_TBL.SPO_TERM_ID → CPM_NEWPAY_TBL.SPO_TERM_ID | CPM_NEWPAY_TBL.SPO_TERM_ID |
| nihtest_NIH_PAYROLL_MASTER | POSITION_1 | exp_Final.POSITION_1 → exp_Init.POSITION_1 → SQ_CPM_NEWPAY_TBL.POSITION_1 → CPM_NEWPAY_TBL.POSITION_1 | CPM_NEWPAY_TBL.POSITION_1 |
| nihtest_NIH_PAYROLL_MASTER | POSITION_2 | exp_Final.POSITION_2 → exp_Init.POSITION_2 → SQ_CPM_NEWPAY_TBL.POSITION_2 → CPM_NEWPAY_TBL.POSITION_2 | CPM_NEWPAY_TBL.POSITION_2 |
| nihtest_NIH_PAYROLL_MASTER | GRADE | exp_Final.GRADE → exp_Init.GRADE → SQ_CPM_NEWPAY_TBL.GRADE → CPM_NEWPAY_TBL.GRADE | CPM_NEWPAY_TBL.GRADE |
| nihtest_NIH_PAYROLL_MASTER | STEP | exp_Final.STEP → exp_Init.STEP → SQ_CPM_NEWPAY_TBL.STEP → CPM_NEWPAY_TBL.STEP | CPM_NEWPAY_TBL.STEP |
| nihtest_NIH_PAYROLL_MASTER | ABNOR_RATE_CDE | exp_Final.ABNOR_RATE_CDE → exp_Init.ABNOR_RATE_CDE → SQ_CPM_NEWPAY_TBL.ABNOR_RATE_CDE → CPM_NEWPAY_TBL.ABNOR_RATE_CDE | CPM_NEWPAY_TBL.ABNOR_RATE_CDE |
| nihtest_NIH_PAYROLL_MASTER | FED_RETIRE_CDE_OLD | exp_Final.FED_RETIRE_CDE_OLD → exp_Init.FED_RETIRE_CDE_OLD → SQ_CPM_NEWPAY_TBL.FED_RETIRE_CDE_OLD → CPM_NEWPAY_TBL.FED_RETIRE_CDE_OLD | CPM_NEWPAY_TBL.FED_RETIRE_CDE_OLD |
| nihtest_NIH_PAYROLL_MASTER | ST_TAX_CDE | exp_Final.ST_TAX_CDE → exp_Init.ST_TAX_CDE → SQ_CPM_NEWPAY_TBL.ST_TAX_CDE → CPM_NEWPAY_TBL.ST_TAX_CDE | CPM_NEWPAY_TBL.ST_TAX_CDE |
| nihtest_NIH_PAYROLL_MASTER | CITY_ST_CDE | exp_Final.CITY_ST_CDE → exp_Init.CITY_ST_CDE → SQ_CPM_NEWPAY_TBL.CITY_ST_CDE → CPM_NEWPAY_TBL.CITY_ST_CDE | CPM_NEWPAY_TBL.CITY_ST_CDE |
| nihtest_NIH_PAYROLL_MASTER | CITY_ID_CDE | exp_Final.CITY_ID_CDE → exp_Init.CITY_ID_CDE → SQ_CPM_NEWPAY_TBL.CITY_ID_CDE → CPM_NEWPAY_TBL.CITY_ID_CDE | CPM_NEWPAY_TBL.CITY_ID_CDE |
| nihtest_NIH_PAYROLL_MASTER | HLTH_ENROL_CDE | exp_Final.HLTH_ENROL_CDE → exp_Convert.o_HLTH_ENROL_CDE = HLTH_ENROL_CDE_1_2 \|\| HLTH_ENROL_CDE_3 → exp_Init.HLTH_ENROL_CDE_1_2 → SQ_CPM_NEWPAY_TBL.HLTH_ENROL_CDE_1_2 → CPM_NEWPAY_TBL.HLTH_ENROL_CDE_1_2 → exp_Init.HLTH_ENROL_CDE_3 → SQ_CPM_NEWPAY_TBL.HLTH_ENROL_CDE_3 → CPM_NEWPAY_TBL.HLTH_ENROL_CDE_3 | CPM_NEWPAY_TBL.HLTH_ENROL_CDE_1_2; CPM_NEWPAY_TBL.HLTH_ENROL_CDE_3 |
| nihtest_NIH_PAYROLL_MASTER | UNION_IDENT_CDE | exp_Final.UNION_IDENT_CDE → exp_Init.UNION_IDENT_CDE → SQ_CPM_NEWPAY_TBL.UNION_IDENT_CDE → CPM_NEWPAY_TBL.UNION_IDENT_CDE | CPM_NEWPAY_TBL.UNION_IDENT_CDE |
| nihtest_NIH_PAYROLL_MASTER | TSPA_STATUS_CODE | exp_Final.TSPA_STATUS_CODE → exp_Init.TSPA_STATUS_CODE → SQ_CPM_NEWPAY_TBL.TSPA_STATUS_CODE → CPM_NEWPAY_TBL.TSPA_STATUS_CODE | CPM_NEWPAY_TBL.TSPA_STATUS_CODE |
| nihtest_NIH_PAYROLL_MASTER | ALT_1_EE_ACCT_NO | exp_Final.ALT_1_EE_ACCT_NO → exp_Init.ALT_1_EE_ACCT_NO → SQ_CPM_NEWPAY_TBL.ALT_1_EE_ACCT_NO → CPM_NEWPAY_TBL.ALT_1_EE_ACCT_NO | CPM_NEWPAY_TBL.ALT_1_EE_ACCT_NO |
| nihtest_NIH_PAYROLL_MASTER | ALT_1_ACCT_TYPE | exp_Final.ALT_1_ACCT_TYPE → exp_Init.ALT_1_ACCT_TYPE → SQ_CPM_NEWPAY_TBL.ALT_1_ACCT_TYPE → CPM_NEWPAY_TBL.ALT_1_ACCT_TYPE | CPM_NEWPAY_TBL.ALT_1_ACCT_TYPE |
| nihtest_NIH_PAYROLL_MASTER | ALT_2_EE_ACCT_NO | exp_Final.ALT_2_EE_ACCT_NO → exp_Init.ALT_2_EE_ACCT_NO → SQ_CPM_NEWPAY_TBL.ALT_2_EE_ACCT_NO → CPM_NEWPAY_TBL.ALT_2_EE_ACCT_NO | CPM_NEWPAY_TBL.ALT_2_EE_ACCT_NO |
| nihtest_NIH_PAYROLL_MASTER | ALT_2_ACCT_TYPE | exp_Final.ALT_2_ACCT_TYPE → exp_Init.ALT_2_ACCT_TYPE → SQ_CPM_NEWPAY_TBL.ALT_2_ACCT_TYPE → CPM_NEWPAY_TBL.ALT_2_ACCT_TYPE | CPM_NEWPAY_TBL.ALT_2_ACCT_TYPE |
| nihtest_NIH_PAYROLL_MASTER | EFT_CODE | (not connected — NULL) | — |
| nihtest_NIH_PAYROLL_MASTER | EFT_EMPL_ACCT_NUMBER | exp_Final.EFT_EMPL_ACCT_NUMBER → exp_Init.EFT_EMPL_ACCT_NUMBER → SQ_CPM_NEWPAY_TBL.EFT_EMPL_ACCT_NUMBER → CPM_NEWPAY_TBL.EFT_EMPL_ACCT_NUMBER | CPM_NEWPAY_TBL.EFT_EMPL_ACCT_NUMBER |
| nihtest_NIH_PAYROLL_MASTER | EFT_EMPL_ACCT_TYPE | exp_Final.EFT_EMPL_ACCT_TYPE → exp_Init.EFT_EMPL_ACCT_TYPE → SQ_CPM_NEWPAY_TBL.EFT_EMPL_ACCT_TYPE → CPM_NEWPAY_TBL.EFT_EMPL_ACCT_TYPE | CPM_NEWPAY_TBL.EFT_EMPL_ACCT_TYPE |
| nihtest_NIH_PAYROLL_MASTER | CSA_RECIPIENT_NAME | exp_Final.CSA_RECIPIENT_NAME → exp_Init.CSA_RECIPIENT_NAME → SQ_CPM_NEWPAY_TBL.CSA_RECIPIENT_NAME → CPM_NEWPAY_TBL.CSA_RECIPIENT_NAME | CPM_NEWPAY_TBL.CSA_RECIPIENT_NAME |
| nihtest_NIH_PAYROLL_MASTER | CSA_RECIPIENT_ACCT_NO | exp_Final.CSA_RECIPIENT_ACCT_NO → exp_Init.CSA_RECIPIENT_ACCT_NO → SQ_CPM_NEWPAY_TBL.CSA_RECIPIENT_ACCT_NO → CPM_NEWPAY_TBL.CSA_RECIPIENT_ACCT_NO | CPM_NEWPAY_TBL.CSA_RECIPIENT_ACCT_NO |
| nihtest_NIH_PAYROLL_MASTER | REEMP_ANN_CDE | exp_Final.REEMP_ANN_CDE → exp_Init.REEMP_ANN_CDE → SQ_CPM_NEWPAY_TBL.REEMP_ANN_CDE → CPM_NEWPAY_TBL.REEMP_ANN_CDE | CPM_NEWPAY_TBL.REEMP_ANN_CDE |
| nihtest_NIH_PAYROLL_MASTER | FLSA_CDE | exp_Final.FLSA_CDE → exp_Init.FLSA_CDE → SQ_CPM_NEWPAY_TBL.FLSA_CDE → CPM_NEWPAY_TBL.FLSA_CDE | CPM_NEWPAY_TBL.FLSA_CDE |
| nihtest_NIH_PAYROLL_MASTER | CPP_REF_DED_CDE | exp_Final.CPP_REF_DED_CDE → exp_Init.CPP_REF_DED_CDE → SQ_CPM_NEWPAY_TBL.CPP_REF_DED_CDE → CPM_NEWPAY_TBL.CPP_REF_DED_CDE | CPM_NEWPAY_TBL.CPP_REF_DED_CDE |
| nihtest_NIH_PAYROLL_MASTER | ADJ_REFUND_CDE | exp_Final.ADJ_REFUND_CDE → exp_Init.ADJ_REFUND_CDE → SQ_CPM_NEWPAY_TBL.ADJ_REFUND_CDE → CPM_NEWPAY_TBL.ADJ_REFUND_CDE | CPM_NEWPAY_TBL.ADJ_REFUND_CDE |
| nihtest_NIH_PAYROLL_MASTER | ALT_4_EE_ACCT_NO | exp_Final.ALT_4_EE_ACCT_NO → exp_Init.ALT_4_EE_ACCT_NO → SQ_CPM_NEWPAY_TBL.ALT_4_EE_ACCT_NO → CPM_NEWPAY_TBL.ALT_4_EE_ACCT_NO | CPM_NEWPAY_TBL.ALT_4_EE_ACCT_NO |
| nihtest_NIH_PAYROLL_MASTER | ALT_4_ACCT_TYPE | exp_Final.ALT_4_ACCT_TYPE → exp_Init.ALT_4_ACCT_TYPE → SQ_CPM_NEWPAY_TBL.ALT_4_ACCT_TYPE → CPM_NEWPAY_TBL.ALT_4_ACCT_TYPE | CPM_NEWPAY_TBL.ALT_4_ACCT_TYPE |
| nihtest_NIH_PAYROLL_MASTER | ST_CNTY_TAX_CODE | (not connected — NULL) | — |
| nihtest_NIH_PAYROLL_MASTER | PSP_CONTRACT_LGTH | (not connected — NULL) | — |
| nihtest_NIH_PAYROLL_MASTER | FEGLI_CDE | exp_Final.FEGLI_CDE → exp_Init.FEGLI_CDE → SQ_CPM_NEWPAY_TBL.FEGLI_CDE → CPM_NEWPAY_TBL.FEGLI_CDE | CPM_NEWPAY_TBL.FEGLI_CDE |
| nihtest_NIH_PAYROLL_MASTER | FEGLI_CDE_2 | exp_Final.FEGLI_CDE_2 → exp_Init.FEGLI_CDE_2 → SQ_CPM_NEWPAY_TBL.FEGLI_CDE_2 → CPM_NEWPAY_TBL.FEGLI_CDE_2 | CPM_NEWPAY_TBL.FEGLI_CDE_2 |
| nihtest_NIH_PAYROLL_MASTER | FEHB_PC_PRE_TAX_IND | (not connected — NULL) | — |
| nihtest_NIH_PAYROLL_MASTER | ALT_5_ACCT_TYPE | exp_Final.ALT_5_ACCT_TYPE → exp_Init.ALT_5_ACCT_TYPE → SQ_CPM_NEWPAY_TBL.ALT_5_ACCT_TYPE → CPM_NEWPAY_TBL.ALT_5_ACCT_TYPE | CPM_NEWPAY_TBL.ALT_5_ACCT_TYPE |
| nihtest_NIH_PAYROLL_MASTER | ALT_6_ACCT_TYPE | exp_Final.ALT_6_ACCT_TYPE → exp_Init.ALT_6_ACCT_TYPE → SQ_CPM_NEWPAY_TBL.ALT_6_ACCT_TYPE → CPM_NEWPAY_TBL.ALT_6_ACCT_TYPE | CPM_NEWPAY_TBL.ALT_6_ACCT_TYPE |
| nihtest_NIH_PAYROLL_MASTER | ALT_7_ACCT_TYPE | exp_Final.ALT_7_ACCT_TYPE → exp_Init.ALT_7_ACCT_TYPE → SQ_CPM_NEWPAY_TBL.ALT_7_ACCT_TYPE → CPM_NEWPAY_TBL.ALT_7_ACCT_TYPE | CPM_NEWPAY_TBL.ALT_7_ACCT_TYPE |
| nihtest_NIH_PAYROLL_MASTER | ALT_8_ACCT_TYPE | exp_Final.ALT_8_ACCT_TYPE → exp_Init.ALT_8_ACCT_TYPE → SQ_CPM_NEWPAY_TBL.ALT_8_ACCT_TYPE → CPM_NEWPAY_TBL.ALT_8_ACCT_TYPE | CPM_NEWPAY_TBL.ALT_8_ACCT_TYPE |
| nihtest_NIH_PAYROLL_MASTER | ALT_5_EE_ACCT_NO | exp_Final.ALT_5_EE_ACCT_NO → exp_Init.ALT_5_EE_ACCT_NO → SQ_CPM_NEWPAY_TBL.ALT_5_EE_ACCT_NO → CPM_NEWPAY_TBL.ALT_5_EE_ACCT_NO | CPM_NEWPAY_TBL.ALT_5_EE_ACCT_NO |
| nihtest_NIH_PAYROLL_MASTER | ALT_6_EE_ACCT_NO | exp_Final.ALT_6_EE_ACCT_NO → exp_Init.ALT_6_EE_ACCT_NO → SQ_CPM_NEWPAY_TBL.ALT_6_EE_ACCT_NO → CPM_NEWPAY_TBL.ALT_6_EE_ACCT_NO | CPM_NEWPAY_TBL.ALT_6_EE_ACCT_NO |
| nihtest_NIH_PAYROLL_MASTER | ALT_7_EE_ACCT_NO | exp_Final.ALT_7_EE_ACCT_NO → exp_Init.ALT_7_EE_ACCT_NO → SQ_CPM_NEWPAY_TBL.ALT_7_EE_ACCT_NO → CPM_NEWPAY_TBL.ALT_7_EE_ACCT_NO | CPM_NEWPAY_TBL.ALT_7_EE_ACCT_NO |
| nihtest_NIH_PAYROLL_MASTER | ALT_8_EE_ACCT_NO | exp_Final.ALT_8_EE_ACCT_NO → exp_Init.ALT_8_EE_ACCT_NO → SQ_CPM_NEWPAY_TBL.ALT_8_EE_ACCT_NO → CPM_NEWPAY_TBL.ALT_8_EE_ACCT_NO | CPM_NEWPAY_TBL.ALT_8_EE_ACCT_NO |
| nihtest_NIH_PAYROLL_MASTER | VIS_DENTAL_1_CDE | exp_Final.VIS_DENTAL_1_CDE → exp_Init.VIS_DENT_1_CDE → SQ_CPM_NEWPAY_TBL.VIS_DENT_1_CDE → CPM_NEWPAY_TBL.VIS_DENT_1_CDE | CPM_NEWPAY_TBL.VIS_DENT_1_CDE |
| nihtest_NIH_PAYROLL_MASTER | VIS_DENTAL_2_CDE | exp_Final.VIS_DENTAL_2_CDE → exp_Init.VIS_DENT_2_CDE → SQ_CPM_NEWPAY_TBL.VIS_DENT_2_CDE → CPM_NEWPAY_TBL.VIS_DENT_2_CDE | CPM_NEWPAY_TBL.VIS_DENT_2_CDE |
| nihtest_NIH_PAYROLL_MASTER | VIS_DENTAL_3_CDE | exp_Final.VIS_DENTAL_3_CDE → exp_Init.VIS_DENT_3_CDE → SQ_CPM_NEWPAY_TBL.VIS_DENT_3_CDE → CPM_NEWPAY_TBL.VIS_DENT_3_CDE | CPM_NEWPAY_TBL.VIS_DENT_3_CDE |
| nihtest_NIH_PAYROLL_MASTER | AGCY_CDE_PER | exp_Final.AGCY_CDE_PER → exp_Init.AGCY_CDE_PER → SQ_CPM_NEWPAY_TBL.AGCY_CDE_PER → CPM_NEWPAY_TBL.AGCY_CDE_PER | CPM_NEWPAY_TBL.AGCY_CDE_PER |
| nihtest_NIH_PAYROLL_MASTER | PHY_HNDCP | exp_Final.PHY_HNDCP → exp_Init.PHY_HNDCP → SQ_CPM_NEWPAY_TBL.PHY_HNDCP → CPM_NEWPAY_TBL.PHY_HNDCP | CPM_NEWPAY_TBL.PHY_HNDCP |
| nihtest_NIH_PAYROLL_MASTER | SUPV_CDE | exp_Final.SUPV_CDE → exp_Init.SUPV_CDE → SQ_CPM_NEWPAY_TBL.SUPV_CDE → CPM_NEWPAY_TBL.SUPV_CDE | CPM_NEWPAY_TBL.SUPV_CDE |
| nihtest_NIH_PAYROLL_MASTER | POS_SEN_CDE | exp_Final.POS_SEN_CDE → exp_Init.POS_SEN_CDE → SQ_CPM_NEWPAY_TBL.POS_SEN_CDE → CPM_NEWPAY_TBL.POS_SEN_CDE | CPM_NEWPAY_TBL.POS_SEN_CDE |
| nihtest_NIH_PAYROLL_MASTER | TOT_FED_TAX_EXEMP | exp_Final.TOT_FED_TAX_EXEMP → exp_Init.TOT_FED_TAX_EXEMP → SQ_CPM_NEWPAY_TBL.TOT_FED_TAX_EXEMP → CPM_NEWPAY_TBL.TOT_FED_TAX_EXEMP | CPM_NEWPAY_TBL.TOT_FED_TAX_EXEMP |
| nihtest_NIH_PAYROLL_MASTER | ADDL_FED_TAX_EXEM | exp_Final.ADDL_FED_TAX_EXEM → exp_Set_Defaults.o_DEFAULT_NUM_1 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | FED_TAX_MAR_STAT | exp_Final.FED_TAX_MAR_STAT → exp_Convert.o_FED_TAX_MAR_STAT = DECODE(FED_TAX_MAR_STAT, 'F', '6', 'M', '4', 'S', '2', '0') → exp_Init.FED_TAX_MAR_STAT → SQ_CPM_NEWPAY_TBL.FED_TAX_MAR_STAT → CPM_NEWPAY_TBL.FED_TAX_MAR_STAT | CPM_NEWPAY_TBL.FED_TAX_MAR_STAT |
| nihtest_NIH_PAYROLL_MASTER | ST_TAX_MAR_STAT | exp_Final.ST_TAX_MAR_STAT → exp_Convert.o_ST_TAX_MAR_STAT = DECODE(ST_TAX_MAR_STAT, 'D', '4', 'E', '5', 'F', '6', 'H', '8', 'M', '4', 'N', '5', 'O', '6', 'S', '2', 'T', '3', 'W', '6', 'X', '7', 'Y', '8', 'Z', '9', '0') → exp_Init.ST_TAX_MAR_STAT → SQ_CPM_NEWPAY_TBL.ST_TAX_MAR_STAT → CPM_NEWPAY_TBL.ST_TAX_MAR_STAT | CPM_NEWPAY_TBL.ST_TAX_MAR_STAT |
| nihtest_NIH_PAYROLL_MASTER | CITY_MAR_STAT | exp_Final.CITY_MAR_STAT → exp_Init.CITY_MAR_STAT → SQ_CPM_NEWPAY_TBL.CITY_MAR_STAT → CPM_NEWPAY_TBL.CITY_MAR_STAT | CPM_NEWPAY_TBL.CITY_MAR_STAT |
| nihtest_NIH_PAYROLL_MASTER | CITY_EXEMP | exp_Final.CITY_EXEMP → exp_Init.CITY_EXEMP → SQ_CPM_NEWPAY_TBL.CITY_EXEMP → CPM_NEWPAY_TBL.CITY_EXEMP | CPM_NEWPAY_TBL.CITY_EXEMP |
| nihtest_NIH_PAYROLL_MASTER | TSPA_VEST_PERIOD | exp_Final.TSPA_VEST_PERIOD → exp_Init.TSPA_VEST_PERIOD → SQ_CPM_NEWPAY_TBL.TSPA_VEST_PERIOD → CPM_NEWPAY_TBL.TSPA_VEST_PERIOD | CPM_NEWPAY_TBL.TSPA_VEST_PERIOD |
| nihtest_NIH_PAYROLL_MASTER | ALT_1_ROUTE_ID | exp_Final.ALT_1_ROUTE_ID → exp_Init.ALT_1_ROUTE_ID → SQ_CPM_NEWPAY_TBL.ALT_1_ROUTE_ID → CPM_NEWPAY_TBL.ALT_1_ROUTE_ID | CPM_NEWPAY_TBL.ALT_1_ROUTE_ID |
| nihtest_NIH_PAYROLL_MASTER | ALT_1_ROUTE_DIGIT | exp_Final.ALT_1_ROUTE_DIGIT → exp_Init.ALT_1_ROUTE_DIGIT → SQ_CPM_NEWPAY_TBL.ALT_1_ROUTE_DIGIT → CPM_NEWPAY_TBL.ALT_1_ROUTE_DIGIT | CPM_NEWPAY_TBL.ALT_1_ROUTE_DIGIT |
| nihtest_NIH_PAYROLL_MASTER | ALT_2_ROUTE_ID | exp_Final.ALT_2_ROUTE_ID → exp_Init.ALT_2_ROUTE_ID → SQ_CPM_NEWPAY_TBL.ALT_2_ROUTE_ID → CPM_NEWPAY_TBL.ALT_2_ROUTE_ID | CPM_NEWPAY_TBL.ALT_2_ROUTE_ID |
| nihtest_NIH_PAYROLL_MASTER | ALT_2_ROUTE_DIGIT | exp_Final.ALT_2_ROUTE_DIGIT → exp_Init.ALT_2_ROUTE_DIGIT → SQ_CPM_NEWPAY_TBL.ALT_2_ROUTE_DIGIT → CPM_NEWPAY_TBL.ALT_2_ROUTE_DIGIT | CPM_NEWPAY_TBL.ALT_2_ROUTE_DIGIT |
| nihtest_NIH_PAYROLL_MASTER | EFT_ROUTE_ID | exp_Final.EFT_ROUTE_ID → exp_Init.EFT_ROUTE_ID → SQ_CPM_NEWPAY_TBL.EFT_ROUTE_ID → CPM_NEWPAY_TBL.EFT_ROUTE_ID | CPM_NEWPAY_TBL.EFT_ROUTE_ID |
| nihtest_NIH_PAYROLL_MASTER | EFT_CK_DIGIT | exp_Final.EFT_CK_DIGIT → exp_Init.EFT_CK_DIGIT → SQ_CPM_NEWPAY_TBL.EFT_CK_DIGIT → CPM_NEWPAY_TBL.EFT_CK_DIGIT | CPM_NEWPAY_TBL.EFT_CK_DIGIT |
| nihtest_NIH_PAYROLL_MASTER | EIC_STATUS_CODE | exp_Final.EIC_STATUS_CODE → exp_Set_Defaults.o_DEFAULT_NUM_1 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | RPT_CDE | exp_Final.RPT_CDE → exp_Init.RPT_CDE → SQ_CPM_NEWPAY_TBL.RPT_CDE → CPM_NEWPAY_TBL.RPT_CDE | CPM_NEWPAY_TBL.RPT_CDE |
| nihtest_NIH_PAYROLL_MASTER | CPP_NO | exp_Final.CPP_NO → exp_Init.CPP_NO → SQ_CPM_NEWPAY_TBL.CPP_NO → CPM_NEWPAY_TBL.CPP_NO | CPM_NEWPAY_TBL.CPP_NO |
| nihtest_NIH_PAYROLL_MASTER | YTD_ST_TX_1_CDE | exp_Final.YTD_ST_TX_1_CDE → exp_Init.YTD_ST_TX_1_CDE → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_1_CDE → CPM_NEWPAY_TBL.YTD_ST_TX_1_CDE | CPM_NEWPAY_TBL.YTD_ST_TX_1_CDE |
| nihtest_NIH_PAYROLL_MASTER | YTD_ST_TX_2_CDE | exp_Final.YTD_ST_TX_2_CDE → exp_Init.YTD_ST_TX_2_CDE → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_2_CDE → CPM_NEWPAY_TBL.YTD_ST_TX_2_CDE | CPM_NEWPAY_TBL.YTD_ST_TX_2_CDE |
| nihtest_NIH_PAYROLL_MASTER | YTD_ST_TX_3_CDE | exp_Final.YTD_ST_TX_3_CDE → exp_Init.YTD_ST_TX_3_CDE → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_3_CDE → CPM_NEWPAY_TBL.YTD_ST_TX_3_CDE | CPM_NEWPAY_TBL.YTD_ST_TX_3_CDE |
| nihtest_NIH_PAYROLL_MASTER | YTD_ST_TX_4_CDE | exp_Final.YTD_ST_TX_4_CDE → exp_Init.YTD_ST_TX_4_CDE → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_4_CDE → CPM_NEWPAY_TBL.YTD_ST_TX_4_CDE | CPM_NEWPAY_TBL.YTD_ST_TX_4_CDE |
| nihtest_NIH_PAYROLL_MASTER | ADJ_NO | exp_Final.ADJ_NO → exp_Init.ADJ_NO → SQ_CPM_NEWPAY_TBL.ADJ_NO → CPM_NEWPAY_TBL.ADJ_NO | CPM_NEWPAY_TBL.ADJ_NO |
| nihtest_NIH_PAYROLL_MASTER | LV_CAT_CDE | exp_Final.LV_CAT_CDE → exp_Init.LV_CAT_CDE → SQ_CPM_NEWPAY_TBL.LV_CAT_CDE → CPM_NEWPAY_TBL.LV_CAT_CDE | CPM_NEWPAY_TBL.LV_CAT_CDE |
| nihtest_NIH_PAYROLL_MASTER | DAYS_INTER_CPP | exp_Final.DAYS_INTER_CPP → exp_Set_Defaults.o_DEFAULT_NUM_1 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | DAYS_INTER_YTD | exp_Final.DAYS_INTER_YTD → exp_Set_Defaults.o_DEFAULT_NUM_1 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | DAYS_INTER_CBAL | exp_Final.DAYS_INTER_CBAL → exp_Set_Defaults.o_DEFAULT_NUM_1 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | ALT_4_ROUTE_ID | exp_Final.ALT_4_ROUTE_ID → exp_Init.ALT_4_ROUTE_ID → SQ_CPM_NEWPAY_TBL.ALT_4_ROUTE_ID → CPM_NEWPAY_TBL.ALT_4_ROUTE_ID | CPM_NEWPAY_TBL.ALT_4_ROUTE_ID |
| nihtest_NIH_PAYROLL_MASTER | ALT_4_ROUTE_DIGIT | exp_Final.ALT_4_ROUTE_DIGIT → exp_Init.ALT_4_ROUTE_DIGIT → SQ_CPM_NEWPAY_TBL.ALT_4_ROUTE_DIGIT → CPM_NEWPAY_TBL.ALT_4_ROUTE_DIGIT | CPM_NEWPAY_TBL.ALT_4_ROUTE_DIGIT |
| nihtest_NIH_PAYROLL_MASTER | ALT_5_ROUTE_ID | exp_Final.ALT_5_ROUTE_ID → exp_Init.ALT_5_ROUTE_ID → SQ_CPM_NEWPAY_TBL.ALT_5_ROUTE_ID → CPM_NEWPAY_TBL.ALT_5_ROUTE_ID | CPM_NEWPAY_TBL.ALT_5_ROUTE_ID |
| nihtest_NIH_PAYROLL_MASTER | ALT_5_ROUTE_DIGIT | exp_Final.ALT_5_ROUTE_DIGIT → exp_Init.ALT_5_ROUTE_DIGIT → SQ_CPM_NEWPAY_TBL.ALT_5_ROUTE_DIGIT → CPM_NEWPAY_TBL.ALT_5_ROUTE_DIGIT | CPM_NEWPAY_TBL.ALT_5_ROUTE_DIGIT |
| nihtest_NIH_PAYROLL_MASTER | ALT_6_ROUTE_ID | exp_Final.ALT_6_ROUTE_ID → exp_Init.ALT_6_ROUTE_ID → SQ_CPM_NEWPAY_TBL.ALT_6_ROUTE_ID → CPM_NEWPAY_TBL.ALT_6_ROUTE_ID | CPM_NEWPAY_TBL.ALT_6_ROUTE_ID |
| nihtest_NIH_PAYROLL_MASTER | ALT_6_ROUTE_DIGIT | exp_Final.ALT_6_ROUTE_DIGIT → exp_Init.ALT_6_ROUTE_DIGIT → SQ_CPM_NEWPAY_TBL.ALT_6_ROUTE_DIGIT → CPM_NEWPAY_TBL.ALT_6_ROUTE_DIGIT | CPM_NEWPAY_TBL.ALT_6_ROUTE_DIGIT |
| nihtest_NIH_PAYROLL_MASTER | ALT_7_ROUTE_ID | exp_Final.ALT_7_ROUTE_ID → exp_Init.ALT_7_ROUTE_ID → SQ_CPM_NEWPAY_TBL.ALT_7_ROUTE_ID → CPM_NEWPAY_TBL.ALT_7_ROUTE_ID | CPM_NEWPAY_TBL.ALT_7_ROUTE_ID |
| nihtest_NIH_PAYROLL_MASTER | ALT_7_ROUTE_DIGIT | exp_Final.ALT_7_ROUTE_DIGIT → exp_Init.ALT_7_ROUTE_DIGIT → SQ_CPM_NEWPAY_TBL.ALT_7_ROUTE_DIGIT → CPM_NEWPAY_TBL.ALT_7_ROUTE_DIGIT | CPM_NEWPAY_TBL.ALT_7_ROUTE_DIGIT |
| nihtest_NIH_PAYROLL_MASTER | ALT_8_ROUTE_ID | exp_Final.ALT_8_ROUTE_ID → exp_Init.ALT_8_ROUTE_ID → SQ_CPM_NEWPAY_TBL.ALT_8_ROUTE_ID → CPM_NEWPAY_TBL.ALT_8_ROUTE_ID | CPM_NEWPAY_TBL.ALT_8_ROUTE_ID |
| nihtest_NIH_PAYROLL_MASTER | ALT_8_ROUTE_DIGIT | exp_Final.ALT_8_ROUTE_DIGIT → exp_Init.ALT_8_ROUTE_DIGIT → SQ_CPM_NEWPAY_TBL.ALT_8_ROUTE_DIGIT → CPM_NEWPAY_TBL.ALT_8_ROUTE_DIGIT | CPM_NEWPAY_TBL.ALT_8_ROUTE_DIGIT |
| nihtest_NIH_PAYROLL_MASTER | OCCUP_CDE | exp_Final.OCCUP_CDE → exp_Init.OCCUP_CDE → SQ_CPM_NEWPAY_TBL.OCCUP_CDE → CPM_NEWPAY_TBL.OCCUP_CDE | CPM_NEWPAY_TBL.OCCUP_CDE |
| nihtest_NIH_PAYROLL_MASTER | TK_NO | exp_Final.TK_NO → exp_Init.TK_NO → SQ_CPM_NEWPAY_TBL.TK_NO → CPM_NEWPAY_TBL.TK_NO | CPM_NEWPAY_TBL.TK_NO |
| nihtest_NIH_PAYROLL_MASTER | SPOC | exp_Final.SPOC → exp_Init.SPOC → SQ_CPM_NEWPAY_TBL.SPOC → CPM_NEWPAY_TBL.SPOC | CPM_NEWPAY_TBL.SPOC |
| nihtest_NIH_PAYROLL_MASTER | DATE_BIRTH | exp_Final.DATE_BIRTH → exp_Convert.o_DATE_BIRTH = v_DATE_BIRTH → exp_Convert.v_DATE_BIRTH = TO_DECIMAL( SUBSTR(v_DATE_BIRTH_CHAR_PAD, 1, 2) \|\| SUBSTR(v_DATE_BIRTH_CHAR_PAD, 3, 2) \|\| SUBSTR(v_DATE_BIRTH_CHAR_PAD, 7, 2) , 0) → exp_Convert.v_DATE_BIRTH_CHAR_PAD = LPAD(TO_CHAR(DATE_BIRTH), 8, '0') → exp_Init.DATE_BIRTH → SQ_CPM_NEWPAY_TBL.DATE_BIRTH → CPM_NEWPAY_TBL.DATE_BIRTH | CPM_NEWPAY_TBL.DATE_BIRTH |
| nihtest_NIH_PAYROLL_MASTER | FS_DATE | exp_Final.FS_DATE → exp_Convert.o_FS_DATE = v_FS_DATE → exp_Convert.v_FS_DATE = TO_DECIMAL( SUBSTR(v_FS_DATE_CHAR_PAD, 1, 2) \|\| SUBSTR(v_FS_DATE_CHAR_PAD, 3, 2) \|\| SUBSTR(v_FS_DATE_CHAR_PAD, 7, 2) , 0) → exp_Convert.v_FS_DATE_CHAR_PAD = LPAD(TO_CHAR(FS_DATE), 8, '0') → exp_Init.FS_DATE → SQ_CPM_NEWPAY_TBL.FS_DATE → CPM_NEWPAY_TBL.FS_DATE | CPM_NEWPAY_TBL.FS_DATE |
| nihtest_NIH_PAYROLL_MASTER | EOD_DATE | exp_Final.EOD_DATE → exp_Convert.o_EOD_DATE = v_EOD_DATE → exp_Convert.v_EOD_DATE = TO_DECIMAL( SUBSTR(v_EOD_DATE_CHAR_PAD, 1, 2) \|\| SUBSTR(v_EOD_DATE_CHAR_PAD, 3, 2) \|\| SUBSTR(v_EOD_DATE_CHAR_PAD, 7, 2) , 0) → exp_Convert.v_EOD_DATE_CHAR_PAD = LPAD(TO_CHAR(EOD_DATE), 8, '0') → exp_Init.EOD_DATE → SQ_CPM_NEWPAY_TBL.EOD_DATE → CPM_NEWPAY_TBL.EOD_DATE | CPM_NEWPAY_TBL.EOD_DATE |
| nihtest_NIH_PAYROLL_MASTER | SEP_DATE | exp_Final.SEP_DATE → exp_Convert.o_SEP_DATE = v_SEP_DATE → exp_Convert.v_SEP_DATE = TO_DECIMAL( SUBSTR(v_SEP_DATE_CHAR_PAD, 1, 2) \|\| SUBSTR(v_SEP_DATE_CHAR_PAD, 3, 2) \|\| SUBSTR(v_SEP_DATE_CHAR_PAD, 7, 2) , 0) → exp_Convert.v_SEP_DATE_CHAR_PAD = LPAD(TO_CHAR(SEP_DATE), 8, '0') → exp_Init.SEP_DATE → SQ_CPM_NEWPAY_TBL.SEP_DATE → CPM_NEWPAY_TBL.SEP_DATE | CPM_NEWPAY_TBL.SEP_DATE |
| nihtest_NIH_PAYROLL_MASTER | PSI_START_DATE | exp_Final.PSI_START_DATE → exp_Convert.o_PSI_START_DATE = v_PSI_START_DATE → exp_Convert.v_PSI_START_DATE = TO_DECIMAL( SUBSTR(v_PSI_START_DATE_CHAR_PAD, 1, 2) \|\| SUBSTR(v_PSI_START_DATE_CHAR_PAD, 3, 2) \|\| SUBSTR(v_PSI_START_DATE_CHAR_PAD, 7, 2) , 0) → exp_Convert.v_PSI_START_DATE_CHAR_PAD = LPAD(TO_CHAR(PSI_START_DATE), 8, '0') → exp_Init.PSI_START_DATE → SQ_CPM_NEWPAY_TBL.PSI_START_DATE → CPM_NEWPAY_TBL.PSI_START_DATE | CPM_NEWPAY_TBL.PSI_START_DATE |
| nihtest_NIH_PAYROLL_MASTER | PREMIUM_PAY | exp_Final.PREMIUM_PAY → exp_Set_Defaults.o_DEFAULT_NUM_1 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | CAR_SERV_DTE | exp_Final.CAR_SERV_DTE → exp_Convert.o_CAR_SERV_DTE = v_CAR_SERV_DTE → exp_Convert.v_CAR_SERV_DTE = TO_DECIMAL( SUBSTR(v_CAR_SERV_DTE_CHAR_PAD, 9, 2) \|\| SUBSTR(v_CAR_SERV_DTE_CHAR_PAD, 11, 2) \|\| SUBSTR(v_CAR_SERV_DTE_CHAR_PAD, 15, 2) , 0) → exp_Convert.v_CAR_SERV_DTE_CHAR_PAD = LPAD(TO_CHAR(CAR_SERV_DTE), 16, '0') → exp_Init.CAR_SERV_DTE → SQ_CPM_NEWPAY_TBL.CAR_SERV_DTE → CPM_NEWPAY_TBL.CAR_SERV_DTE | CPM_NEWPAY_TBL.CAR_SERV_DTE |
| nihtest_NIH_PAYROLL_MASTER | PROB_DTE | exp_Final.PROB_DTE → exp_Convert.o_PROB_DTE = v_PROB_DTE → exp_Convert.v_PROB_DTE = TO_DECIMAL( SUBSTR(v_PROB_DTE_CHAR_PAD, 1, 2) \|\| SUBSTR(v_PROB_DTE_CHAR_PAD, 3, 2) \|\| SUBSTR(v_PROB_DTE_CHAR_PAD, 7, 2), 0) → exp_Convert.v_PROB_DTE_CHAR_PAD = LPAD(TO_CHAR(PROB_DTE), 8, '0') → exp_Init.PROB_DTE → SQ_CPM_NEWPAY_TBL.PROB_DTE → CPM_NEWPAY_TBL.PROB_DTE | CPM_NEWPAY_TBL.PROB_DTE |
| nihtest_NIH_PAYROLL_MASTER | BASE_HRS | exp_Final.BASE_HRS → exp_Init.BASE_HRS → SQ_CPM_NEWPAY_TBL.BASE_HRS → CPM_NEWPAY_TBL.BASE_HRS | CPM_NEWPAY_TBL.BASE_HRS |
| nihtest_NIH_PAYROLL_MASTER | ANNUAL_SAL | exp_Final.ANNUAL_SAL → exp_Init.ANNUAL_SAL → SQ_CPM_NEWPAY_TBL.ANNUAL_SAL → CPM_NEWPAY_TBL.ANNUAL_SAL | CPM_NEWPAY_TBL.ANNUAL_SAL |
| nihtest_NIH_PAYROLL_MASTER | HRLY_RATE | exp_Final.HRLY_RATE → exp_Init.HRLY_RATE → SQ_CPM_NEWPAY_TBL.HRLY_RATE → CPM_NEWPAY_TBL.HRLY_RATE | CPM_NEWPAY_TBL.HRLY_RATE |
| nihtest_NIH_PAYROLL_MASTER | OT_RATE | exp_Final.OT_RATE → exp_Init.OT_RATE → SQ_CPM_NEWPAY_TBL.OT_RATE → CPM_NEWPAY_TBL.OT_RATE | CPM_NEWPAY_TBL.OT_RATE |
| nihtest_NIH_PAYROLL_MASTER | SEV_PAY_AMT | exp_Final.SEV_PAY_AMT → exp_Init.SEV_PAY_AMT → SQ_CPM_NEWPAY_TBL.SEV_PAY_AMT → CPM_NEWPAY_TBL.SEV_PAY_AMT | CPM_NEWPAY_TBL.SEV_PAY_AMT |
| nihtest_NIH_PAYROLL_MASTER | FED_OPT_TAX_DED | exp_Final.FED_OPT_TAX_DED → exp_Init.FED_OPT_TAX_DED → SQ_CPM_NEWPAY_TBL.FED_OPT_TAX_DED → CPM_NEWPAY_TBL.FED_OPT_TAX_DED | CPM_NEWPAY_TBL.FED_OPT_TAX_DED |
| nihtest_NIH_PAYROLL_MASTER | ST_TAX_EXEMP | exp_Final.ST_TAX_EXEMP → exp_Init.ST_TAX_EXEMP → SQ_CPM_NEWPAY_TBL.ST_TAX_EXEMP → CPM_NEWPAY_TBL.ST_TAX_EXEMP | CPM_NEWPAY_TBL.ST_TAX_EXEMP |
| nihtest_NIH_PAYROLL_MASTER | ST_TAX_OPT_DED | exp_Final.ST_TAX_OPT_DED → exp_Init.ST_TAX_OPT_DED → SQ_CPM_NEWPAY_TBL.ST_TAX_OPT_DED → CPM_NEWPAY_TBL.ST_TAX_OPT_DED | CPM_NEWPAY_TBL.ST_TAX_OPT_DED |
| nihtest_NIH_PAYROLL_MASTER | HLTH_DED | exp_Final.HLTH_DED → exp_Init.HLTH_DED → SQ_CPM_NEWPAY_TBL.HLTH_DED → CPM_NEWPAY_TBL.HLTH_DED | CPM_NEWPAY_TBL.HLTH_DED |
| nihtest_NIH_PAYROLL_MASTER | HLTH_GOVT_SHARE | exp_Final.HLTH_GOVT_SHARE → exp_Init.HLTH_GOVT_SHARE → SQ_CPM_NEWPAY_TBL.HLTH_GOVT_SHARE → CPM_NEWPAY_TBL.HLTH_GOVT_SHARE | CPM_NEWPAY_TBL.HLTH_GOVT_SHARE |
| nihtest_NIH_PAYROLL_MASTER | UNION_DED | exp_Final.UNION_DED → exp_Init.UNION_DED → SQ_CPM_NEWPAY_TBL.UNION_DED → CPM_NEWPAY_TBL.UNION_DED | CPM_NEWPAY_TBL.UNION_DED |
| nihtest_NIH_PAYROLL_MASTER | FERS_BAL_FWD | exp_Final.FERS_BAL_FWD → exp_Init.FERS_BAL_FWD → SQ_CPM_NEWPAY_TBL.FERS_BAL_FWD → CPM_NEWPAY_TBL.FERS_BAL_FWD | CPM_NEWPAY_TBL.FERS_BAL_FWD |
| nihtest_NIH_PAYROLL_MASTER | TSPA_STATUS_CODE_DTE | exp_Final.TSPA_STATUS_CODE_DTE → exp_Convert.o_TSPA_STATUS_CODE_DTE = v_TSPA_STATUS_CODE_DTE → exp_Convert.v_TSPA_STATUS_CODE_DTE = TO_DECIMAL( SUBSTR(v_TSPA_STATUS_CODE_DTE_CHAR_PAD, 1, 2) \|\| SUBSTR(v_TSPA_STATUS_CODE_DTE_CHAR_PAD, 3, 2) \|\| SUBSTR(v_TSPA_STATUS_CODE_DTE_CHAR_PAD, 7, 2) , 0) → exp_Convert.v_TSPA_STATUS_CODE_DTE_CHAR_PAD = LPAD(TO_CHAR(TSPA_STATUS_CODE_DTE), 8, '0') → exp_Init.TSPA_STATUS_CODE_DTE → SQ_CPM_NEWPAY_TBL.TSPA_STATUS_CODE_DTE → CPM_NEWPAY_TBL.TSPA_STATUS_CODE_DTE | CPM_NEWPAY_TBL.TSPA_STATUS_CODE_DTE |
| nihtest_NIH_PAYROLL_MASTER | TSPA_SCD | exp_Final.TSPA_SCD → exp_Convert.o_TSPA_SCD = v_TSPA_SCD → exp_Convert.v_TSPA_SCD = TO_DECIMAL( SUBSTR(v_TSPA_SCD_CHAR_PAD, 1, 2) \|\| SUBSTR(v_TSPA_SCD_CHAR_PAD, 3, 2) \|\| SUBSTR(v_TSPA_SCD_CHAR_PAD, 7, 2) , 0) → exp_Convert.v_TSPA_SCD_CHAR_PAD = LPAD(TO_CHAR(TO_DECIMAL(TSPA_SCD, 0)), 8, '0') → exp_Init.TSPA_SCD → SQ_CPM_NEWPAY_TBL.TSPA_SCD → CPM_NEWPAY_TBL.TSPA_SCD | CPM_NEWPAY_TBL.TSPA_SCD |
| nihtest_NIH_PAYROLL_MASTER | PCA_BIWEEK_AMT | exp_Final.PCA_BIWEEK_AMT → exp_Init.PCA_BIWEEK_AMT → SQ_CPM_NEWPAY_TBL.PCA_BIWEEK_AMT → CPM_NEWPAY_TBL.PCA_BIWEEK_AMT | CPM_NEWPAY_TBL.PCA_BIWEEK_AMT |
| nihtest_NIH_PAYROLL_MASTER | REEMP_ANU_HR_RTE | exp_Final.REEMP_ANU_HR_RTE → exp_Init.REEMP_ANU_HR_RTE → SQ_CPM_NEWPAY_TBL.REEMP_ANU_HR_RTE → CPM_NEWPAY_TBL.REEMP_ANU_HR_RTE | CPM_NEWPAY_TBL.REEMP_ANU_HR_RTE |
| nihtest_NIH_PAYROLL_MASTER | CPP_BASE_PAY | exp_Final.CPP_BASE_PAY → exp_Init.CPP_BASE_PAY → SQ_CPM_NEWPAY_TBL.CPP_BASE_PAY → CPM_NEWPAY_TBL.CPP_BASE_PAY | CPM_NEWPAY_TBL.CPP_BASE_PAY |
| nihtest_NIH_PAYROLL_MASTER | CPP_OT_PAY | exp_Final.CPP_OT_PAY → exp_Init.CPP_OT_PAY → SQ_CPM_NEWPAY_TBL.CPP_OT_PAY → CPM_NEWPAY_TBL.CPP_OT_PAY | CPM_NEWPAY_TBL.CPP_OT_PAY |
| nihtest_NIH_PAYROLL_MASTER | CPP_ND_PAY | exp_Final.CPP_ND_PAY → exp_Init.CPP_ND_PAY → SQ_CPM_NEWPAY_TBL.CPP_ND_PAY → CPM_NEWPAY_TBL.CPP_ND_PAY | CPM_NEWPAY_TBL.CPP_ND_PAY |
| nihtest_NIH_PAYROLL_MASTER | CPP_SD_PAY | exp_Final.CPP_SD_PAY → exp_Init.CPP_SD_PAY → SQ_CPM_NEWPAY_TBL.CPP_SD_PAY → CPM_NEWPAY_TBL.CPP_SD_PAY | CPM_NEWPAY_TBL.CPP_SD_PAY |
| nihtest_NIH_PAYROLL_MASTER | CPP_HOL_PAY | exp_Final.CPP_HOL_PAY → exp_Init.CPP_HOL_PAY → SQ_CPM_NEWPAY_TBL.CPP_HOL_PAY → CPM_NEWPAY_TBL.CPP_HOL_PAY | CPM_NEWPAY_TBL.CPP_HOL_PAY |
| nihtest_NIH_PAYROLL_MASTER | CPP_PD_PAY | exp_Final.CPP_PD_PAY → exp_Init.CPP_PD_PAY → SQ_CPM_NEWPAY_TBL.CPP_PD_PAY → CPM_NEWPAY_TBL.CPP_PD_PAY | CPM_NEWPAY_TBL.CPP_PD_PAY |
| nihtest_NIH_PAYROLL_MASTER | CPP_COLA_PAY | exp_Final.CPP_COLA_PAY → exp_Init.CPP_COLA_PAY → SQ_CPM_NEWPAY_TBL.CPP_COLA_PAY → CPM_NEWPAY_TBL.CPP_COLA_PAY | CPM_NEWPAY_TBL.CPP_COLA_PAY |
| nihtest_NIH_PAYROLL_MASTER | CPP_UNIF_ALLOW | exp_Final.CPP_UNIF_ALLOW → exp_Init.CPP_UNIF_ALLOW → SQ_CPM_NEWPAY_TBL.CPP_UNIF_ALLOW → CPM_NEWPAY_TBL.CPP_UNIF_ALLOW | CPM_NEWPAY_TBL.CPP_UNIF_ALLOW |
| nihtest_NIH_PAYROLL_MASTER | CPP_SEV_PAY | exp_Final.CPP_SEV_PAY → exp_Init.CPP_SEV_PAY → SQ_CPM_NEWPAY_TBL.CPP_SEV_PAY → CPM_NEWPAY_TBL.CPP_SEV_PAY | CPM_NEWPAY_TBL.CPP_SEV_PAY |
| nihtest_NIH_PAYROLL_MASTER | CPP_CASH_AWARD | exp_Final.CPP_CASH_AWARD → exp_Init.CPP_CASH_AWARD → SQ_CPM_NEWPAY_TBL.CPP_CASH_AWARD → CPM_NEWPAY_TBL.CPP_CASH_AWARD | CPM_NEWPAY_TBL.CPP_CASH_AWARD |
| nihtest_NIH_PAYROLL_MASTER | CPP_OTHER_PAY | exp_Final.CPP_OTHER_PAY → exp_Init.CPP_OTHER_PAY → SQ_CPM_NEWPAY_TBL.CPP_OTHER_PAY → CPM_NEWPAY_TBL.CPP_OTHER_PAY | CPM_NEWPAY_TBL.CPP_OTHER_PAY |
| nihtest_NIH_PAYROLL_MASTER | CPP_GROSS_PAY | exp_Final.CPP_GROSS_PAY → exp_Init.CPP_GROSS_PAY → SQ_CPM_NEWPAY_TBL.CPP_GROSS_PAY → CPM_NEWPAY_TBL.CPP_GROSS_PAY | CPM_NEWPAY_TBL.CPP_GROSS_PAY |
| nihtest_NIH_PAYROLL_MASTER | CPP_PAY_NS_FWIT | exp_Final.CPP_PAY_NS_FWIT → exp_Init.CPP_PAY_NS_FWIT → SQ_CPM_NEWPAY_TBL.CPP_PAY_NS_FWIT → CPM_NEWPAY_TBL.CPP_PAY_NS_FWIT | CPM_NEWPAY_TBL.CPP_PAY_NS_FWIT |
| nihtest_NIH_PAYROLL_MASTER | CPP_FED_WITH_DED | exp_Final.CPP_FED_WITH_DED → exp_Init.CPP_FED_WITH_DED → SQ_CPM_NEWPAY_TBL.CPP_FED_WITH_DED → CPM_NEWPAY_TBL.CPP_FED_WITH_DED | CPM_NEWPAY_TBL.CPP_FED_WITH_DED |
| nihtest_NIH_PAYROLL_MASTER | CPP_PAY_S_FEDTX | exp_Final.CPP_PAY_S_FEDTX → exp_Init.CPP_PAY_S_FEDTX → SQ_CPM_NEWPAY_TBL.CPP_PAY_S_FEDTX → CPM_NEWPAY_TBL.CPP_PAY_S_FEDTX | CPM_NEWPAY_TBL.CPP_PAY_S_FEDTX |
| nihtest_NIH_PAYROLL_MASTER | CPP_CSR_DED | exp_Final.CPP_CSR_DED → exp_Init.CPP_CSR_DED → SQ_CPM_NEWPAY_TBL.CPP_CSR_DED → CPM_NEWPAY_TBL.CPP_CSR_DED | CPM_NEWPAY_TBL.CPP_CSR_DED |
| nihtest_NIH_PAYROLL_MASTER | CPP_CSR_EMPLR | exp_Final.CPP_CSR_EMPLR → exp_Init.CPP_CSR_EMPLR → SQ_CPM_NEWPAY_TBL.CPP_CSR_EMPLR → CPM_NEWPAY_TBL.CPP_CSR_EMPLR | CPM_NEWPAY_TBL.CPP_CSR_EMPLR |
| nihtest_NIH_PAYROLL_MASTER | CPP_PAY_S_CSR | exp_Final.CPP_PAY_S_CSR → exp_Init.CPP_PAY_S_CSR → SQ_CPM_NEWPAY_TBL.CPP_PAY_S_CSR → CPM_NEWPAY_TBL.CPP_PAY_S_CSR | CPM_NEWPAY_TBL.CPP_PAY_S_CSR |
| nihtest_NIH_PAYROLL_MASTER | CPP_FICA_DED | exp_Final.CPP_FICA_DED → exp_Init.CPP_FICA_DED → SQ_CPM_NEWPAY_TBL.CPP_FICA_DED → CPM_NEWPAY_TBL.CPP_FICA_DED | CPM_NEWPAY_TBL.CPP_FICA_DED |
| nihtest_NIH_PAYROLL_MASTER | CPP_FICA_EMPLR | exp_Final.CPP_FICA_EMPLR → exp_Init.CPP_FICA_EMPLR → SQ_CPM_NEWPAY_TBL.CPP_FICA_EMPLR → CPM_NEWPAY_TBL.CPP_FICA_EMPLR | CPM_NEWPAY_TBL.CPP_FICA_EMPLR |
| nihtest_NIH_PAYROLL_MASTER | CPP_PAY_S_FICA | exp_Final.CPP_PAY_S_FICA → exp_Init.CPP_PAY_S_FICA → SQ_CPM_NEWPAY_TBL.CPP_PAY_S_FICA → CPM_NEWPAY_TBL.CPP_PAY_S_FICA | CPM_NEWPAY_TBL.CPP_PAY_S_FICA |
| nihtest_NIH_PAYROLL_MASTER | CPP_MEDC_DED | exp_Final.CPP_MEDC_DED → exp_Init.CPP_MEDC_DED → SQ_CPM_NEWPAY_TBL.CPP_MEDC_DED → CPM_NEWPAY_TBL.CPP_MEDC_DED | CPM_NEWPAY_TBL.CPP_MEDC_DED |
| nihtest_NIH_PAYROLL_MASTER | CPP_MEDC_EMPLR | exp_Final.CPP_MEDC_EMPLR → exp_Init.CPP_MEDC_EMPLR → SQ_CPM_NEWPAY_TBL.CPP_MEDC_EMPLR → CPM_NEWPAY_TBL.CPP_MEDC_EMPLR | CPM_NEWPAY_TBL.CPP_MEDC_EMPLR |
| nihtest_NIH_PAYROLL_MASTER | CPP_PAY_S_MEDC | exp_Final.CPP_PAY_S_MEDC → exp_Init.CPP_PAY_S_MEDC → SQ_CPM_NEWPAY_TBL.CPP_PAY_S_MEDC → CPM_NEWPAY_TBL.CPP_PAY_S_MEDC | CPM_NEWPAY_TBL.CPP_PAY_S_MEDC |
| nihtest_NIH_PAYROLL_MASTER | CPP_FERS_EMP_DED | exp_Final.CPP_FERS_EMP_DED → exp_Init.CPP_FERS_EMP_DED → SQ_CPM_NEWPAY_TBL.CPP_FERS_EMP_DED → CPM_NEWPAY_TBL.CPP_FERS_EMP_DED | CPM_NEWPAY_TBL.CPP_FERS_EMP_DED |
| nihtest_NIH_PAYROLL_MASTER | CPP_FERS_AGY_DED | exp_Final.CPP_FERS_AGY_DED → exp_Init.CPP_FERS_AGY_DED → SQ_CPM_NEWPAY_TBL.CPP_FERS_AGY_DED → CPM_NEWPAY_TBL.CPP_FERS_AGY_DED | CPM_NEWPAY_TBL.CPP_FERS_AGY_DED |
| nihtest_NIH_PAYROLL_MASTER | CPP_FERS_PAY_SUB | exp_Final.CPP_FERS_PAY_SUB → exp_Init.CPP_FERS_PAY_SUB → SQ_CPM_NEWPAY_TBL.CPP_FERS_PAY_SUB → CPM_NEWPAY_TBL.CPP_FERS_PAY_SUB | CPM_NEWPAY_TBL.CPP_FERS_PAY_SUB |
| nihtest_NIH_PAYROLL_MASTER | CPP_LEVY_DED | exp_Final.CPP_LEVY_DED → exp_Set_Defaults.o_DEFAULT_NUM_1 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | CPP_ST_TAX_DED | exp_Final.CPP_ST_TAX_DED → exp_Init.CPP_ST_TAX_DED → SQ_CPM_NEWPAY_TBL.CPP_ST_TAX_DED → CPM_NEWPAY_TBL.CPP_ST_TAX_DED | CPM_NEWPAY_TBL.CPP_ST_TAX_DED |
| nihtest_NIH_PAYROLL_MASTER | CPP_CITY_DED | exp_Final.CPP_CITY_DED → exp_Init.CPP_CITY_DED → SQ_CPM_NEWPAY_TBL.CPP_CITY_DED → CPM_NEWPAY_TBL.CPP_CITY_DED | CPM_NEWPAY_TBL.CPP_CITY_DED |
| nihtest_NIH_PAYROLL_MASTER | CPP_HLTH_DED | exp_Final.CPP_HLTH_DED → exp_Init.CPP_HLTH_DED → SQ_CPM_NEWPAY_TBL.CPP_HLTH_DED → CPM_NEWPAY_TBL.CPP_HLTH_DED | CPM_NEWPAY_TBL.CPP_HLTH_DED |
| nihtest_NIH_PAYROLL_MASTER | CPP_HLTH_EMPLR | exp_Final.CPP_HLTH_EMPLR → exp_Init.CPP_HLTH_EMPLR → SQ_CPM_NEWPAY_TBL.CPP_HLTH_EMPLR → CPM_NEWPAY_TBL.CPP_HLTH_EMPLR | CPM_NEWPAY_TBL.CPP_HLTH_EMPLR |
| nihtest_NIH_PAYROLL_MASTER | CPP_BOND_DED | exp_Final.CPP_BOND_DED → exp_Init.CPP_BOND_DED → SQ_CPM_NEWPAY_TBL.CPP_BOND_DED → CPM_NEWPAY_TBL.CPP_BOND_DED | CPM_NEWPAY_TBL.CPP_BOND_DED |
| nihtest_NIH_PAYROLL_MASTER | CPP_LI_REG_DED | exp_Final.CPP_LI_REG_DED → exp_Init.CPP_LI_REG_DED → SQ_CPM_NEWPAY_TBL.CPP_LI_REG_DED → CPM_NEWPAY_TBL.CPP_LI_REG_DED | CPM_NEWPAY_TBL.CPP_LI_REG_DED |
| nihtest_NIH_PAYROLL_MASTER | CPP_LI_EMPLR | exp_Final.CPP_LI_EMPLR → exp_Init.CPP_LI_EMPLR → SQ_CPM_NEWPAY_TBL.CPP_LI_EMPLR → CPM_NEWPAY_TBL.CPP_LI_EMPLR | CPM_NEWPAY_TBL.CPP_LI_EMPLR |
| nihtest_NIH_PAYROLL_MASTER | CPP_LI_OPT_DED | exp_Final.CPP_LI_OPT_DED → exp_Init.CPP_LI_OPT_DED → SQ_CPM_NEWPAY_TBL.CPP_LI_OPT_DED → CPM_NEWPAY_TBL.CPP_LI_OPT_DED | CPM_NEWPAY_TBL.CPP_LI_OPT_DED |
| nihtest_NIH_PAYROLL_MASTER | CPP_FEGLI_OPTB | exp_Final.CPP_FEGLI_OPTB → exp_Init.CPP_FEGLI_OPTB → SQ_CPM_NEWPAY_TBL.CPP_FEGLI_OPTB → CPM_NEWPAY_TBL.CPP_FEGLI_OPTB | CPM_NEWPAY_TBL.CPP_FEGLI_OPTB |
| nihtest_NIH_PAYROLL_MASTER | CPP_FEGLI_OPTC | exp_Final.CPP_FEGLI_OPTC → exp_Init.CPP_FEGLI_OPTC → SQ_CPM_NEWPAY_TBL.CPP_FEGLI_OPTC → CPM_NEWPAY_TBL.CPP_FEGLI_OPTC | CPM_NEWPAY_TBL.CPP_FEGLI_OPTC |
| nihtest_NIH_PAYROLL_MASTER | CPP_CHAR_DED | exp_Final.CPP_CHAR_DED → exp_Init.CPP_CHAR_DED → SQ_CPM_NEWPAY_TBL.CPP_CHAR_DED → CPM_NEWPAY_TBL.CPP_CHAR_DED | CPM_NEWPAY_TBL.CPP_CHAR_DED |
| nihtest_NIH_PAYROLL_MASTER | CPP_UNION_1_DED | exp_Final.CPP_UNION_1_DED → exp_Init.CPP_UNION_1_DED → SQ_CPM_NEWPAY_TBL.CPP_UNION_1_DED → CPM_NEWPAY_TBL.CPP_UNION_1_DED | CPM_NEWPAY_TBL.CPP_UNION_1_DED |
| nihtest_NIH_PAYROLL_MASTER | CPP_ALT_1_DED | exp_Final.CPP_ALT_1_DED → exp_Init.CPP_ALT_1_DED → SQ_CPM_NEWPAY_TBL.CPP_ALT_1_DED → CPM_NEWPAY_TBL.CPP_ALT_1_DED | CPM_NEWPAY_TBL.CPP_ALT_1_DED |
| nihtest_NIH_PAYROLL_MASTER | CPP_ALT_2_DED | exp_Final.CPP_ALT_2_DED → exp_Init.CPP_ALT_2_DED → SQ_CPM_NEWPAY_TBL.CPP_ALT_2_DED → CPM_NEWPAY_TBL.CPP_ALT_2_DED | CPM_NEWPAY_TBL.CPP_ALT_2_DED |
| nihtest_NIH_PAYROLL_MASTER | CPP_NET_ALT_DED | exp_Final.CPP_NET_ALT_DED → exp_Init.CPP_NET_ALT_DED → SQ_CPM_NEWPAY_TBL.CPP_NET_ALT_DED → CPM_NEWPAY_TBL.CPP_NET_ALT_DED | CPM_NEWPAY_TBL.CPP_NET_ALT_DED |
| nihtest_NIH_PAYROLL_MASTER | CPP_REF_DED_AMT | exp_Final.CPP_REF_DED_AMT → exp_Init.CPP_REF_DED_AMT → SQ_CPM_NEWPAY_TBL.CPP_REF_DED_AMT → CPM_NEWPAY_TBL.CPP_REF_DED_AMT | CPM_NEWPAY_TBL.CPP_REF_DED_AMT |
| nihtest_NIH_PAYROLL_MASTER | CPP_QUARTERS_DED | exp_Final.CPP_QUARTERS_DED → exp_Init.CPP_QUARTERS_DED → SQ_CPM_NEWPAY_TBL.CPP_QUARTERS_DED → CPM_NEWPAY_TBL.CPP_QUARTERS_DED | CPM_NEWPAY_TBL.CPP_QUARTERS_DED |
| nihtest_NIH_PAYROLL_MASTER | CPP_SUBSIST_DED | exp_Final.CPP_SUBSIST_DED → exp_Init.CPP_SUBSIST_DED → SQ_CPM_NEWPAY_TBL.CPP_SUBSIST_DED → CPM_NEWPAY_TBL.CPP_SUBSIST_DED | CPM_NEWPAY_TBL.CPP_SUBSIST_DED |
| nihtest_NIH_PAYROLL_MASTER | CPP_NET_PAY | exp_Final.CPP_NET_PAY → exp_Init.CPP_NET_PAY → SQ_CPM_NEWPAY_TBL.CPP_NET_PAY → CPM_NEWPAY_TBL.CPP_NET_PAY | CPM_NEWPAY_TBL.CPP_NET_PAY |
| nihtest_NIH_PAYROLL_MASTER | CPP_CSA_DED | exp_Final.CPP_CSA_DED → exp_Init.CPP_CSA_DED → SQ_CPM_NEWPAY_TBL.CPP_CSA_DED → CPM_NEWPAY_TBL.CPP_CSA_DED | CPM_NEWPAY_TBL.CPP_CSA_DED |
| nihtest_NIH_PAYROLL_MASTER | EIC_CPP_PAY | exp_Final.EIC_CPP_PAY → exp_Init.EIC_CPP_PAY → SQ_CPM_NEWPAY_TBL.EIC_CPP_PAY → CPM_NEWPAY_TBL.EIC_CPP_PAY | CPM_NEWPAY_TBL.EIC_CPP_PAY |
| nihtest_NIH_PAYROLL_MASTER | PCA_CPP_PAY | exp_Final.PCA_CPP_PAY → exp_Init.PCA_CPP_PAY → SQ_CPM_NEWPAY_TBL.PCA_CPP_PAY → CPM_NEWPAY_TBL.PCA_CPP_PAY | CPM_NEWPAY_TBL.PCA_CPP_PAY |
| nihtest_NIH_PAYROLL_MASTER | CPP_TSPA_PAY_SUB | exp_Final.CPP_TSPA_PAY_SUB → exp_Init.CPP_TSPA_PAY_SUB → SQ_CPM_NEWPAY_TBL.CPP_TSPA_PAY_SUB → CPM_NEWPAY_TBL.CPP_TSPA_PAY_SUB | CPM_NEWPAY_TBL.CPP_TSPA_PAY_SUB |
| nihtest_NIH_PAYROLL_MASTER | CPP_TSPG_GBADIST | exp_Final.CPP_TSPG_GBADIST → exp_Init.CPP_TSPG_GBADIST → SQ_CPM_NEWPAY_TBL.CPP_TSPG_GBADIST → CPM_NEWPAY_TBL.CPP_TSPG_GBADIST | CPM_NEWPAY_TBL.CPP_TSPG_GBADIST |
| nihtest_NIH_PAYROLL_MASTER | CPP_TSPG_EADIST | exp_Final.CPP_TSPG_EADIST → exp_Init.CPP_TSPG_EADIST → SQ_CPM_NEWPAY_TBL.CPP_TSPG_EADIST → CPM_NEWPAY_TBL.CPP_TSPG_EADIST | CPM_NEWPAY_TBL.CPP_TSPG_EADIST |
| nihtest_NIH_PAYROLL_MASTER | CPP_TSPG_GMADIST | exp_Final.CPP_TSPG_GMADIST → exp_Init.CPP_TSPG_GMADIST → SQ_CPM_NEWPAY_TBL.CPP_TSPG_GMADIST → CPM_NEWPAY_TBL.CPP_TSPG_GMADIST | CPM_NEWPAY_TBL.CPP_TSPG_GMADIST |
| nihtest_NIH_PAYROLL_MASTER | CPP_TSPF_GBADIST | exp_Final.CPP_TSPF_GBADIST → exp_Set_Defaults.o_DEFAULT_NUM_1 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | CPP_TSPF_EADIST | exp_Final.CPP_TSPF_EADIST → exp_Set_Defaults.o_DEFAULT_NUM_1 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | CPP_TSPF_GMADIST | exp_Final.CPP_TSPF_GMADIST → exp_Set_Defaults.o_DEFAULT_NUM_1 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | CPP_TSPC_GBADIST | exp_Final.CPP_TSPC_GBADIST → exp_Set_Defaults.o_DEFAULT_NUM_1 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | CPP_TSPC_EADIST | exp_Final.CPP_TSPC_EADIST → exp_Set_Defaults.o_DEFAULT_NUM_1 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | CPP_TSPC_GMADIST | exp_Final.CPP_TSPC_GMADIST → exp_Set_Defaults.o_DEFAULT_NUM_1 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | YTD_BASE_PAY | exp_Final.YTD_BASE_PAY → exp_Init.YTD_BASE_PAY → SQ_CPM_NEWPAY_TBL.YTD_BASE_PAY → CPM_NEWPAY_TBL.YTD_BASE_PAY | CPM_NEWPAY_TBL.YTD_BASE_PAY |
| nihtest_NIH_PAYROLL_MASTER | YTD_OT_PAY | exp_Final.YTD_OT_PAY → exp_Init.YTD_OT_PAY → SQ_CPM_NEWPAY_TBL.YTD_OT_PAY → CPM_NEWPAY_TBL.YTD_OT_PAY | CPM_NEWPAY_TBL.YTD_OT_PAY |
| nihtest_NIH_PAYROLL_MASTER | YTD_ND_PAY | exp_Final.YTD_ND_PAY → exp_Init.YTD_ND_PAY → SQ_CPM_NEWPAY_TBL.YTD_ND_PAY → CPM_NEWPAY_TBL.YTD_ND_PAY | CPM_NEWPAY_TBL.YTD_ND_PAY |
| nihtest_NIH_PAYROLL_MASTER | YTD_SD_PAY | exp_Final.YTD_SD_PAY → exp_Init.YTD_SD_PAY → SQ_CPM_NEWPAY_TBL.YTD_SD_PAY → CPM_NEWPAY_TBL.YTD_SD_PAY | CPM_NEWPAY_TBL.YTD_SD_PAY |
| nihtest_NIH_PAYROLL_MASTER | YTD_HOL_PAY | exp_Final.YTD_HOL_PAY → exp_Init.YTD_HOL_PAY → SQ_CPM_NEWPAY_TBL.YTD_HOL_PAY → CPM_NEWPAY_TBL.YTD_HOL_PAY | CPM_NEWPAY_TBL.YTD_HOL_PAY |
| nihtest_NIH_PAYROLL_MASTER | YTD_PD_PAY | exp_Final.YTD_PD_PAY → exp_Init.YTD_PD_PAY → SQ_CPM_NEWPAY_TBL.YTD_PD_PAY → CPM_NEWPAY_TBL.YTD_PD_PAY | CPM_NEWPAY_TBL.YTD_PD_PAY |
| nihtest_NIH_PAYROLL_MASTER | YTD_COLA_PAY | exp_Final.YTD_COLA_PAY → exp_Init.YTD_COLA_PAY → SQ_CPM_NEWPAY_TBL.YTD_COLA_PAY → CPM_NEWPAY_TBL.YTD_COLA_PAY | CPM_NEWPAY_TBL.YTD_COLA_PAY |
| nihtest_NIH_PAYROLL_MASTER | YTD_UNIF_ALLOW | exp_Final.YTD_UNIF_ALLOW → exp_Init.YTD_UNIF_ALLOW → SQ_CPM_NEWPAY_TBL.YTD_UNIF_ALLOW → CPM_NEWPAY_TBL.YTD_UNIF_ALLOW | CPM_NEWPAY_TBL.YTD_UNIF_ALLOW |
| nihtest_NIH_PAYROLL_MASTER | YTD_SEV_PAY | exp_Final.YTD_SEV_PAY → exp_Init.YTD_SEV_PAY → SQ_CPM_NEWPAY_TBL.YTD_SEV_PAY → CPM_NEWPAY_TBL.YTD_SEV_PAY | CPM_NEWPAY_TBL.YTD_SEV_PAY |
| nihtest_NIH_PAYROLL_MASTER | YTD_CASH_AWARDS | exp_Final.YTD_CASH_AWARDS → exp_Init.YTD_CASH_AWARDS → SQ_CPM_NEWPAY_TBL.YTD_CASH_AWARDS → CPM_NEWPAY_TBL.YTD_CASH_AWARDS | CPM_NEWPAY_TBL.YTD_CASH_AWARDS |
| nihtest_NIH_PAYROLL_MASTER | YTD_MISC_OTH_PAY | exp_Final.YTD_MISC_OTH_PAY → exp_Init.YTD_MISC_OTH_PAY → SQ_CPM_NEWPAY_TBL.YTD_MISC_OTH_PAY → CPM_NEWPAY_TBL.YTD_MISC_OTH_PAY | CPM_NEWPAY_TBL.YTD_MISC_OTH_PAY |
| nihtest_NIH_PAYROLL_MASTER | YTD_GROSS_PAY | exp_Final.YTD_GROSS_PAY → exp_Init.YTD_GROSS_PAY → SQ_CPM_NEWPAY_TBL.YTD_GROSS_PAY → CPM_NEWPAY_TBL.YTD_GROSS_PAY | CPM_NEWPAY_TBL.YTD_GROSS_PAY |
| nihtest_NIH_PAYROLL_MASTER | YTD_NON_TAX_PAY | exp_Final.YTD_NON_TAX_PAY → exp_Set_Defaults.o_DEFAULT_NUM_2 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | YTD_FED_TAX_DED | exp_Final.YTD_FED_TAX_DED → exp_Init.YTD_FED_TAX_DED → SQ_CPM_NEWPAY_TBL.YTD_FED_TAX_DED → CPM_NEWPAY_TBL.YTD_FED_TAX_DED | CPM_NEWPAY_TBL.YTD_FED_TAX_DED |
| nihtest_NIH_PAYROLL_MASTER | YTD_TAXABLE_PAY | exp_Final.YTD_TAXABLE_PAY → exp_Init.YTD_TAXABLE_PAY → SQ_CPM_NEWPAY_TBL.YTD_TAXABLE_PAY → CPM_NEWPAY_TBL.YTD_TAXABLE_PAY | CPM_NEWPAY_TBL.YTD_TAXABLE_PAY |
| nihtest_NIH_PAYROLL_MASTER | YTD_CSR_DED | exp_Final.YTD_CSR_DED → exp_Init.YTD_CSR_DED → SQ_CPM_NEWPAY_TBL.YTD_CSR_DED → CPM_NEWPAY_TBL.YTD_CSR_DED | CPM_NEWPAY_TBL.YTD_CSR_DED |
| nihtest_NIH_PAYROLL_MASTER | YTD_CSR_EMPLR | exp_Final.YTD_CSR_EMPLR → exp_Init.YTD_CSR_EMPLR → SQ_CPM_NEWPAY_TBL.YTD_CSR_EMPLR → CPM_NEWPAY_TBL.YTD_CSR_EMPLR | CPM_NEWPAY_TBL.YTD_CSR_EMPLR |
| nihtest_NIH_PAYROLL_MASTER | YTD_CSR_PAY | exp_Final.YTD_CSR_PAY → exp_Init.YTD_CSR_PAY → SQ_CPM_NEWPAY_TBL.YTD_CSR_PAY → CPM_NEWPAY_TBL.YTD_CSR_PAY | CPM_NEWPAY_TBL.YTD_CSR_PAY |
| nihtest_NIH_PAYROLL_MASTER | YTD_FICA_DED | exp_Final.YTD_FICA_DED → exp_Init.YTD_FICA_DED → SQ_CPM_NEWPAY_TBL.YTD_FICA_DED → CPM_NEWPAY_TBL.YTD_FICA_DED | CPM_NEWPAY_TBL.YTD_FICA_DED |
| nihtest_NIH_PAYROLL_MASTER | YTD_FICA_EMPLR | exp_Final.YTD_FICA_EMPLR → exp_Init.YTD_FICA_EMPLR → SQ_CPM_NEWPAY_TBL.YTD_FICA_EMPLR → CPM_NEWPAY_TBL.YTD_FICA_EMPLR | CPM_NEWPAY_TBL.YTD_FICA_EMPLR |
| nihtest_NIH_PAYROLL_MASTER | YTD_FICA_PAY | exp_Final.YTD_FICA_PAY → exp_Init.YTD_FICA_PAY → SQ_CPM_NEWPAY_TBL.YTD_FICA_PAY → CPM_NEWPAY_TBL.YTD_FICA_PAY | CPM_NEWPAY_TBL.YTD_FICA_PAY |
| nihtest_NIH_PAYROLL_MASTER | YTD_MEDC_DED | exp_Final.YTD_MEDC_DED → exp_Init.YTD_MEDC_DED → SQ_CPM_NEWPAY_TBL.YTD_MEDC_DED → CPM_NEWPAY_TBL.YTD_MEDC_DED | CPM_NEWPAY_TBL.YTD_MEDC_DED |
| nihtest_NIH_PAYROLL_MASTER | YTD_MEDC_EMPLR | exp_Final.YTD_MEDC_EMPLR → exp_Init.YTD_MEDC_EMPLR → SQ_CPM_NEWPAY_TBL.YTD_MEDC_EMPLR → CPM_NEWPAY_TBL.YTD_MEDC_EMPLR | CPM_NEWPAY_TBL.YTD_MEDC_EMPLR |
| nihtest_NIH_PAYROLL_MASTER | YTD_PAY_S_MEDC | exp_Final.YTD_PAY_S_MEDC → exp_Init.YTD_PAY_S_MEDC → SQ_CPM_NEWPAY_TBL.YTD_PAY_S_MEDC → CPM_NEWPAY_TBL.YTD_PAY_S_MEDC | CPM_NEWPAY_TBL.YTD_PAY_S_MEDC |
| nihtest_NIH_PAYROLL_MASTER | YTD_FERS_EMP_DED | exp_Final.YTD_FERS_EMP_DED → exp_Init.YTD_FERS_EMP_DED → SQ_CPM_NEWPAY_TBL.YTD_FERS_EMP_DED → CPM_NEWPAY_TBL.YTD_FERS_EMP_DED | CPM_NEWPAY_TBL.YTD_FERS_EMP_DED |
| nihtest_NIH_PAYROLL_MASTER | YTD_FERS_AGY_DED | exp_Final.YTD_FERS_AGY_DED → exp_Init.YTD_FERS_AGY_DED → SQ_CPM_NEWPAY_TBL.YTD_FERS_AGY_DED → CPM_NEWPAY_TBL.YTD_FERS_AGY_DED | CPM_NEWPAY_TBL.YTD_FERS_AGY_DED |
| nihtest_NIH_PAYROLL_MASTER | YTD_FERS_PAY_SUB | exp_Final.YTD_FERS_PAY_SUB → exp_Init.YTD_FERS_PAY_SUB → SQ_CPM_NEWPAY_TBL.YTD_FERS_PAY_SUB → CPM_NEWPAY_TBL.YTD_FERS_PAY_SUB | CPM_NEWPAY_TBL.YTD_FERS_PAY_SUB |
| nihtest_NIH_PAYROLL_MASTER | YTD_ST_TX_1_DED | exp_Final.YTD_ST_TX_1_DED → exp_Init.YTD_ST_TX_1_DED → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_1_DED → CPM_NEWPAY_TBL.YTD_ST_TX_1_DED | CPM_NEWPAY_TBL.YTD_ST_TX_1_DED |
| nihtest_NIH_PAYROLL_MASTER | YTD_ST_TX_1_GRS | exp_Final.YTD_ST_TX_1_GRS → exp_Init.YTD_ST_TX_1_GRS → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_1_GRS → CPM_NEWPAY_TBL.YTD_ST_TX_1_GRS | CPM_NEWPAY_TBL.YTD_ST_TX_1_GRS |
| nihtest_NIH_PAYROLL_MASTER | YTD_ST_TX_2_DED | exp_Final.YTD_ST_TX_2_DED → exp_Init.YTD_ST_TX_2_DED → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_2_DED → CPM_NEWPAY_TBL.YTD_ST_TX_2_DED | CPM_NEWPAY_TBL.YTD_ST_TX_2_DED |
| nihtest_NIH_PAYROLL_MASTER | YTD_ST_TX_2_GRS | exp_Final.YTD_ST_TX_2_GRS → exp_Init.YTD_ST_TX_2_GRS → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_2_GRS → CPM_NEWPAY_TBL.YTD_ST_TX_2_GRS | CPM_NEWPAY_TBL.YTD_ST_TX_2_GRS |
| nihtest_NIH_PAYROLL_MASTER | YTD_ST_TX_3_DED | exp_Final.YTD_ST_TX_3_DED → exp_Init.YTD_ST_TX_3_DED → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_3_DED → CPM_NEWPAY_TBL.YTD_ST_TX_3_DED | CPM_NEWPAY_TBL.YTD_ST_TX_3_DED |
| nihtest_NIH_PAYROLL_MASTER | YTD_ST_TX_3_GRS | exp_Final.YTD_ST_TX_3_GRS → exp_Init.YTD_ST_TX_3_GRS → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_3_GRS → CPM_NEWPAY_TBL.YTD_ST_TX_3_GRS | CPM_NEWPAY_TBL.YTD_ST_TX_3_GRS |
| nihtest_NIH_PAYROLL_MASTER | YTD_ST_TX_4_DED | exp_Final.YTD_ST_TX_4_DED → exp_Init.YTD_ST_TX_4_DED → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_4_DED → CPM_NEWPAY_TBL.YTD_ST_TX_4_DED | CPM_NEWPAY_TBL.YTD_ST_TX_4_DED |
| nihtest_NIH_PAYROLL_MASTER | YTD_ST_TX_4_GRS | exp_Final.YTD_ST_TX_4_GRS → exp_Init.YTD_ST_TX_4_GRS → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_4_GRS → CPM_NEWPAY_TBL.YTD_ST_TX_4_GRS | CPM_NEWPAY_TBL.YTD_ST_TX_4_GRS |
| nihtest_NIH_PAYROLL_MASTER | YTD_CITY_DED | exp_Final.YTD_CITY_DED → exp_Set_Defaults.o_DEFAULT_NUM_2 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | YTD_HLTH_DED | exp_Final.YTD_HLTH_DED → exp_Init.YTD_HLTH_DED → SQ_CPM_NEWPAY_TBL.YTD_HLTH_DED → CPM_NEWPAY_TBL.YTD_HLTH_DED | CPM_NEWPAY_TBL.YTD_HLTH_DED |
| nihtest_NIH_PAYROLL_MASTER | YTD_HLTH_EMPLR | exp_Final.YTD_HLTH_EMPLR → exp_Init.YTD_HLTH_EMPLR → SQ_CPM_NEWPAY_TBL.YTD_HLTH_EMPLR → CPM_NEWPAY_TBL.YTD_HLTH_EMPLR | CPM_NEWPAY_TBL.YTD_HLTH_EMPLR |
| nihtest_NIH_PAYROLL_MASTER | YTD_BOND_DED | exp_Final.YTD_BOND_DED → exp_Init.YTD_BOND_DED → SQ_CPM_NEWPAY_TBL.YTD_BOND_DED → CPM_NEWPAY_TBL.YTD_BOND_DED | CPM_NEWPAY_TBL.YTD_BOND_DED |
| nihtest_NIH_PAYROLL_MASTER | YTD_LI_REG_DED | exp_Final.YTD_LI_REG_DED → exp_Init.YTD_LI_REG_DED → SQ_CPM_NEWPAY_TBL.YTD_LI_REG_DED → CPM_NEWPAY_TBL.YTD_LI_REG_DED | CPM_NEWPAY_TBL.YTD_LI_REG_DED |
| nihtest_NIH_PAYROLL_MASTER | YTD_LI_REG_EMPLR | exp_Final.YTD_LI_REG_EMPLR → exp_Init.YTD_LI_REG_EMPLR → SQ_CPM_NEWPAY_TBL.YTD_LI_REG_EMPLR → CPM_NEWPAY_TBL.YTD_LI_REG_EMPLR | CPM_NEWPAY_TBL.YTD_LI_REG_EMPLR |
| nihtest_NIH_PAYROLL_MASTER | YTD_LI_OPT_DED | exp_Final.YTD_LI_OPT_DED → exp_Init.YTD_LI_OPT_DED → SQ_CPM_NEWPAY_TBL.YTD_LI_OPT_DED → CPM_NEWPAY_TBL.YTD_LI_OPT_DED | CPM_NEWPAY_TBL.YTD_LI_OPT_DED |
| nihtest_NIH_PAYROLL_MASTER | YTD_FEGLI_OPTB | exp_Final.YTD_FEGLI_OPTB → exp_Init.YTD_FEGLI_OPTB → SQ_CPM_NEWPAY_TBL.YTD_FEGLI_OPTB → CPM_NEWPAY_TBL.YTD_FEGLI_OPTB | CPM_NEWPAY_TBL.YTD_FEGLI_OPTB |
| nihtest_NIH_PAYROLL_MASTER | YTD_FEGLI_OPTC | exp_Final.YTD_FEGLI_OPTC → exp_Init.YTD_FEGLI_OPTC → SQ_CPM_NEWPAY_TBL.YTD_FEGLI_OPTC → CPM_NEWPAY_TBL.YTD_FEGLI_OPTC | CPM_NEWPAY_TBL.YTD_FEGLI_OPTC |
| nihtest_NIH_PAYROLL_MASTER | YTD_CHAR_DED | exp_Final.YTD_CHAR_DED → exp_Init.YTD_CHAR_DED → SQ_CPM_NEWPAY_TBL.YTD_CHAR_DED → CPM_NEWPAY_TBL.YTD_CHAR_DED | CPM_NEWPAY_TBL.YTD_CHAR_DED |
| nihtest_NIH_PAYROLL_MASTER | YTD_ALT_1_DED | exp_Final.YTD_ALT_1_DED → exp_Init.YTD_ALT_1_DED → SQ_CPM_NEWPAY_TBL.YTD_ALT_1_DED → CPM_NEWPAY_TBL.YTD_ALT_1_DED | CPM_NEWPAY_TBL.YTD_ALT_1_DED |
| nihtest_NIH_PAYROLL_MASTER | YTD_QUARTERS_DED | exp_Final.YTD_QUARTERS_DED → exp_Init.YTD_QUARTERS_DED → SQ_CPM_NEWPAY_TBL.YTD_QUARTERS_DED → CPM_NEWPAY_TBL.YTD_QUARTERS_DED | CPM_NEWPAY_TBL.YTD_QUARTERS_DED |
| nihtest_NIH_PAYROLL_MASTER | YTD_NET_PAY | exp_Final.YTD_NET_PAY → exp_Init.YTD_NET_PAY → SQ_CPM_NEWPAY_TBL.YTD_NET_PAY → CPM_NEWPAY_TBL.YTD_NET_PAY | CPM_NEWPAY_TBL.YTD_NET_PAY |
| nihtest_NIH_PAYROLL_MASTER | YTD_CSA_DED | exp_Final.YTD_CSA_DED → exp_Init.YTD_CSA_DED → SQ_CPM_NEWPAY_TBL.YTD_CSA_DED → CPM_NEWPAY_TBL.YTD_CSA_DED | CPM_NEWPAY_TBL.YTD_CSA_DED |
| nihtest_NIH_PAYROLL_MASTER | EIC_YTD_PAY | exp_Final.EIC_YTD_PAY → exp_Init.EIC_YTD_PAY → SQ_CPM_NEWPAY_TBL.EIC_YTD_PAY → CPM_NEWPAY_TBL.EIC_YTD_PAY | CPM_NEWPAY_TBL.EIC_YTD_PAY |
| nihtest_NIH_PAYROLL_MASTER | PCA_YTD_PAY | exp_Final.PCA_YTD_PAY → exp_Init.PCA_YTD_PAY → SQ_CPM_NEWPAY_TBL.PCA_YTD_PAY → CPM_NEWPAY_TBL.PCA_YTD_PAY | CPM_NEWPAY_TBL.PCA_YTD_PAY |
| nihtest_NIH_PAYROLL_MASTER | YTD_TSPA_PAY_SUB | exp_Final.YTD_TSPA_PAY_SUB → exp_Init.YTD_TSPA_PAY_SUB → SQ_CPM_NEWPAY_TBL.YTD_TSPA_PAY_SUB → CPM_NEWPAY_TBL.YTD_TSPA_PAY_SUB | CPM_NEWPAY_TBL.YTD_TSPA_PAY_SUB |
| nihtest_NIH_PAYROLL_MASTER | YTD_TSPG_GBADIST | exp_Final.YTD_TSPG_GBADIST → exp_Init.YTD_TSPG_GBADIST → SQ_CPM_NEWPAY_TBL.YTD_TSPG_GBADIST → CPM_NEWPAY_TBL.YTD_TSPG_GBADIST | CPM_NEWPAY_TBL.YTD_TSPG_GBADIST |
| nihtest_NIH_PAYROLL_MASTER | YTD_TSPG_EADIST | exp_Final.YTD_TSPG_EADIST → exp_Init.YTD_TSPG_EADIST → SQ_CPM_NEWPAY_TBL.YTD_TSPG_EADIST → CPM_NEWPAY_TBL.YTD_TSPG_EADIST | CPM_NEWPAY_TBL.YTD_TSPG_EADIST |
| nihtest_NIH_PAYROLL_MASTER | YTD_TSPG_GMADIST | exp_Final.YTD_TSPG_GMADIST → exp_Init.YTD_TSPG_GMADIST → SQ_CPM_NEWPAY_TBL.YTD_TSPG_GMADIST → CPM_NEWPAY_TBL.YTD_TSPG_GMADIST | CPM_NEWPAY_TBL.YTD_TSPG_GMADIST |
| nihtest_NIH_PAYROLL_MASTER | YTD_TSPF_GBADIST | exp_Final.YTD_TSPF_GBADIST → exp_Set_Defaults.o_DEFAULT_NUM_2 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | YTD_TSPF_EADIST | exp_Final.YTD_TSPF_EADIST → exp_Set_Defaults.o_DEFAULT_NUM_2 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | YTD_TSPF_GMADIST | exp_Final.YTD_TSPF_GMADIST → exp_Set_Defaults.o_DEFAULT_NUM_2 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | YTD_TSPC_GBADIST | exp_Final.YTD_TSPC_GBADIST → exp_Set_Defaults.o_DEFAULT_NUM_2 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | YTD_TSPC_EADIST | exp_Final.YTD_TSPC_EADIST → exp_Set_Defaults.o_DEFAULT_NUM_2 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | YTD_TSPC_GMADIST | exp_Final.YTD_TSPC_GMADIST → exp_Set_Defaults.o_DEFAULT_NUM_2 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | ADJ_BASE_PAY | exp_Final.ADJ_BASE_PAY → exp_Init.ADJ_BASE_PAY → SQ_CPM_NEWPAY_TBL.ADJ_BASE_PAY → CPM_NEWPAY_TBL.ADJ_BASE_PAY | CPM_NEWPAY_TBL.ADJ_BASE_PAY |
| nihtest_NIH_PAYROLL_MASTER | ADJ_OT_PAY | exp_Final.ADJ_OT_PAY → exp_Init.ADJ_OT_PAY → SQ_CPM_NEWPAY_TBL.ADJ_OT_PAY → CPM_NEWPAY_TBL.ADJ_OT_PAY | CPM_NEWPAY_TBL.ADJ_OT_PAY |
| nihtest_NIH_PAYROLL_MASTER | ADJ_ND_PAY | exp_Final.ADJ_ND_PAY → exp_Init.ADJ_ND_PAY → SQ_CPM_NEWPAY_TBL.ADJ_ND_PAY → CPM_NEWPAY_TBL.ADJ_ND_PAY | CPM_NEWPAY_TBL.ADJ_ND_PAY |
| nihtest_NIH_PAYROLL_MASTER | ADJ_SD_PAY | exp_Final.ADJ_SD_PAY → exp_Init.ADJ_SD_PAY → SQ_CPM_NEWPAY_TBL.ADJ_SD_PAY → CPM_NEWPAY_TBL.ADJ_SD_PAY | CPM_NEWPAY_TBL.ADJ_SD_PAY |
| nihtest_NIH_PAYROLL_MASTER | ADJ_HOL_PAY | exp_Final.ADJ_HOL_PAY → exp_Init.ADJ_HOL_PAY → SQ_CPM_NEWPAY_TBL.ADJ_HOL_PAY → CPM_NEWPAY_TBL.ADJ_HOL_PAY | CPM_NEWPAY_TBL.ADJ_HOL_PAY |
| nihtest_NIH_PAYROLL_MASTER | ADJ_PD_PAY | exp_Final.ADJ_PD_PAY → exp_Init.ADJ_PD_PAY → SQ_CPM_NEWPAY_TBL.ADJ_PD_PAY → CPM_NEWPAY_TBL.ADJ_PD_PAY | CPM_NEWPAY_TBL.ADJ_PD_PAY |
| nihtest_NIH_PAYROLL_MASTER | ADJ_COLA_PAY | exp_Final.ADJ_COLA_PAY → exp_Init.ADJ_COLA_PAY → SQ_CPM_NEWPAY_TBL.ADJ_COLA_PAY → CPM_NEWPAY_TBL.ADJ_COLA_PAY | CPM_NEWPAY_TBL.ADJ_COLA_PAY |
| nihtest_NIH_PAYROLL_MASTER | ADJ_UNIF_ALLOW | exp_Final.ADJ_UNIF_ALLOW → exp_Init.ADJ_UNIF_ALLOW → SQ_CPM_NEWPAY_TBL.ADJ_UNIF_ALLOW → CPM_NEWPAY_TBL.ADJ_UNIF_ALLOW | CPM_NEWPAY_TBL.ADJ_UNIF_ALLOW |
| nihtest_NIH_PAYROLL_MASTER | ADJ_SEV_PAY | exp_Final.ADJ_SEV_PAY → exp_Init.ADJ_SEV_PAY → SQ_CPM_NEWPAY_TBL.ADJ_SEV_PAY → CPM_NEWPAY_TBL.ADJ_SEV_PAY | CPM_NEWPAY_TBL.ADJ_SEV_PAY |
| nihtest_NIH_PAYROLL_MASTER | ADJ_CAS_AWARD | exp_Final.ADJ_CAS_AWARD → exp_Init.ADJ_CAS_AWARD → SQ_CPM_NEWPAY_TBL.ADJ_CAS_AWARD → CPM_NEWPAY_TBL.ADJ_CAS_AWARD | CPM_NEWPAY_TBL.ADJ_CAS_AWARD |
| nihtest_NIH_PAYROLL_MASTER | ADJ_OTHER_PAY | exp_Final.ADJ_OTHER_PAY → exp_Init.ADJ_OTHER_PAY → SQ_CPM_NEWPAY_TBL.ADJ_OTHER_PAY → CPM_NEWPAY_TBL.ADJ_OTHER_PAY | CPM_NEWPAY_TBL.ADJ_OTHER_PAY |
| nihtest_NIH_PAYROLL_MASTER | ADJ_GROSS_PAY | exp_Final.ADJ_GROSS_PAY → exp_Init.ADJ_GROSS_PAY → SQ_CPM_NEWPAY_TBL.ADJ_GROSS_PAY → CPM_NEWPAY_TBL.ADJ_GROSS_PAY | CPM_NEWPAY_TBL.ADJ_GROSS_PAY |
| nihtest_NIH_PAYROLL_MASTER | ADJ_PAY_NS_FWIT | exp_Final.ADJ_PAY_NS_FWIT → exp_Init.ADJ_PAY_NS_FWIT → SQ_CPM_NEWPAY_TBL.ADJ_PAY_NS_FWIT → CPM_NEWPAY_TBL.ADJ_PAY_NS_FWIT | CPM_NEWPAY_TBL.ADJ_PAY_NS_FWIT |
| nihtest_NIH_PAYROLL_MASTER | ADJ_FED_WITH_DED | exp_Final.ADJ_FED_WITH_DED → exp_Init.ADJ_FED_WITH_DED → SQ_CPM_NEWPAY_TBL.ADJ_FED_WITH_DED → CPM_NEWPAY_TBL.ADJ_FED_WITH_DED | CPM_NEWPAY_TBL.ADJ_FED_WITH_DED |
| nihtest_NIH_PAYROLL_MASTER | ADJ_CSR_DED | exp_Final.ADJ_CSR_DED → exp_Init.ADJ_CSR_DED → SQ_CPM_NEWPAY_TBL.ADJ_CSR_DED → CPM_NEWPAY_TBL.ADJ_CSR_DED | CPM_NEWPAY_TBL.ADJ_CSR_DED |
| nihtest_NIH_PAYROLL_MASTER | ADJ_CSR_WAGES | exp_Final.ADJ_CSR_WAGES → exp_Set_Defaults.o_DEFAULT_NUM_2 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | ADJ_CSR_EMPL_DED | exp_Final.ADJ_CSR_EMPL_DED → exp_Init.ADJ_CSR_EMPL_DED → SQ_CPM_NEWPAY_TBL.ADJ_CSR_EMPL_DED → CPM_NEWPAY_TBL.ADJ_CSR_EMPL_DED | CPM_NEWPAY_TBL.ADJ_CSR_EMPL_DED |
| nihtest_NIH_PAYROLL_MASTER | ADJ_FICA_DED | exp_Final.ADJ_FICA_DED → exp_Init.ADJ_FICA_DED → SQ_CPM_NEWPAY_TBL.ADJ_FICA_DED → CPM_NEWPAY_TBL.ADJ_FICA_DED | CPM_NEWPAY_TBL.ADJ_FICA_DED |
| nihtest_NIH_PAYROLL_MASTER | ADJ_FICA_WAGES | exp_Final.ADJ_FICA_WAGES → exp_Init.ADJ_FICA_WAGES → SQ_CPM_NEWPAY_TBL.ADJ_FICA_WAGES → CPM_NEWPAY_TBL.ADJ_FICA_WAGES | CPM_NEWPAY_TBL.ADJ_FICA_WAGES |
| nihtest_NIH_PAYROLL_MASTER | ADJ_FICA_EMPL_DED | exp_Final.ADJ_FICA_EMPL_DED → exp_Init.ADJ_FICA_EMPL_DED → SQ_CPM_NEWPAY_TBL.ADJ_FICA_EMPL_DED → CPM_NEWPAY_TBL.ADJ_FICA_EMPL_DED | CPM_NEWPAY_TBL.ADJ_FICA_EMPL_DED |
| nihtest_NIH_PAYROLL_MASTER | ADJ_MEDC_DED | exp_Final.ADJ_MEDC_DED → exp_Init.ADJ_MEDC_DED → SQ_CPM_NEWPAY_TBL.ADJ_MEDC_DED → CPM_NEWPAY_TBL.ADJ_MEDC_DED | CPM_NEWPAY_TBL.ADJ_MEDC_DED |
| nihtest_NIH_PAYROLL_MASTER | ADJ_MEDC_WAGES | exp_Final.ADJ_MEDC_WAGES → exp_Init.ADJ_MEDC_WAGES → SQ_CPM_NEWPAY_TBL.ADJ_MEDC_WAGES → CPM_NEWPAY_TBL.ADJ_MEDC_WAGES | CPM_NEWPAY_TBL.ADJ_MEDC_WAGES |
| nihtest_NIH_PAYROLL_MASTER | ADJ_MEDC_EMPL_DED | exp_Final.ADJ_MEDC_EMPL_DED → exp_Init.ADJ_MEDC_EMPL_DED → SQ_CPM_NEWPAY_TBL.ADJ_MEDC_EMPL_DED → CPM_NEWPAY_TBL.ADJ_MEDC_EMPL_DED | CPM_NEWPAY_TBL.ADJ_MEDC_EMPL_DED |
| nihtest_NIH_PAYROLL_MASTER | ADJ_FERS_EMP_DED | exp_Final.ADJ_FERS_EMP_DED → exp_Init.ADJ_FERS_EMP_DED → SQ_CPM_NEWPAY_TBL.ADJ_FERS_EMP_DED → CPM_NEWPAY_TBL.ADJ_FERS_EMP_DED | CPM_NEWPAY_TBL.ADJ_FERS_EMP_DED |
| nihtest_NIH_PAYROLL_MASTER | ADJ_FERS_AGY_DED | exp_Final.ADJ_FERS_AGY_DED → exp_Init.ADJ_FERS_AGY_DED → SQ_CPM_NEWPAY_TBL.ADJ_FERS_AGY_DED → CPM_NEWPAY_TBL.ADJ_FERS_AGY_DED | CPM_NEWPAY_TBL.ADJ_FERS_AGY_DED |
| nihtest_NIH_PAYROLL_MASTER | ADJ_FERS_WAGES | exp_Final.ADJ_FERS_WAGES → exp_Init.ADJ_FERS_WAGES → SQ_CPM_NEWPAY_TBL.ADJ_FERS_WAGES → CPM_NEWPAY_TBL.ADJ_FERS_WAGES | CPM_NEWPAY_TBL.ADJ_FERS_WAGES |
| nihtest_NIH_PAYROLL_MASTER | ADJ_ST_TAX_DED | exp_Final.ADJ_ST_TAX_DED → exp_Init.ADJ_ST_TAX_DED → SQ_CPM_NEWPAY_TBL.ADJ_ST_TAX_DED → CPM_NEWPAY_TBL.ADJ_ST_TAX_DED | CPM_NEWPAY_TBL.ADJ_ST_TAX_DED |
| nihtest_NIH_PAYROLL_MASTER | ADJ_ST_TAX_DD2 | exp_Final.ADJ_ST_TAX_DD2 → exp_Set_Defaults.o_DEFAULT_NUM_2 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | ADJ_CITY_DED | exp_Final.ADJ_CITY_DED → exp_Init.ADJ_CITY_DED → SQ_CPM_NEWPAY_TBL.ADJ_CITY_DED → CPM_NEWPAY_TBL.ADJ_CITY_DED | CPM_NEWPAY_TBL.ADJ_CITY_DED |
| nihtest_NIH_PAYROLL_MASTER | ADJ_HLTH_DED | exp_Final.ADJ_HLTH_DED → exp_Init.ADJ_HLTH_DED → SQ_CPM_NEWPAY_TBL.ADJ_HLTH_DED → CPM_NEWPAY_TBL.ADJ_HLTH_DED | CPM_NEWPAY_TBL.ADJ_HLTH_DED |
| nihtest_NIH_PAYROLL_MASTER | ADJ_HLTH_EMPLR | exp_Final.ADJ_HLTH_EMPLR → exp_Init.ADJ_HLTH_EMPLR → SQ_CPM_NEWPAY_TBL.ADJ_HLTH_EMPLR → CPM_NEWPAY_TBL.ADJ_HLTH_EMPLR | CPM_NEWPAY_TBL.ADJ_HLTH_EMPLR |
| nihtest_NIH_PAYROLL_MASTER | ADJ_BOND_DED | exp_Final.ADJ_BOND_DED → exp_Init.ADJ_BOND_DED → SQ_CPM_NEWPAY_TBL.ADJ_BOND_DED → CPM_NEWPAY_TBL.ADJ_BOND_DED | CPM_NEWPAY_TBL.ADJ_BOND_DED |
| nihtest_NIH_PAYROLL_MASTER | ADJ_LI_REG_DED | exp_Final.ADJ_LI_REG_DED → exp_Init.ADJ_LI_REG_DED → SQ_CPM_NEWPAY_TBL.ADJ_LI_REG_DED → CPM_NEWPAY_TBL.ADJ_LI_REG_DED | CPM_NEWPAY_TBL.ADJ_LI_REG_DED |
| nihtest_NIH_PAYROLL_MASTER | ADJ_LI_OPT_DED | exp_Final.ADJ_LI_OPT_DED → exp_Init.ADJ_LI_OPT_DED → SQ_CPM_NEWPAY_TBL.ADJ_LI_OPT_DED → CPM_NEWPAY_TBL.ADJ_LI_OPT_DED | CPM_NEWPAY_TBL.ADJ_LI_OPT_DED |
| nihtest_NIH_PAYROLL_MASTER | ADJ_FEGLI_OPTB | exp_Final.ADJ_FEGLI_OPTB → exp_Init.ADJ_FEGLI_OPTB → SQ_CPM_NEWPAY_TBL.ADJ_FEGLI_OPTB → CPM_NEWPAY_TBL.ADJ_FEGLI_OPTB | CPM_NEWPAY_TBL.ADJ_FEGLI_OPTB |
| nihtest_NIH_PAYROLL_MASTER | ADJ_FEGLI_OPTC | exp_Final.ADJ_FEGLI_OPTC → exp_Init.ADJ_FEGLI_OPTC → SQ_CPM_NEWPAY_TBL.ADJ_FEGLI_OPTC → CPM_NEWPAY_TBL.ADJ_FEGLI_OPTC | CPM_NEWPAY_TBL.ADJ_FEGLI_OPTC |
| nihtest_NIH_PAYROLL_MASTER | ADJ_CHAR_DED | exp_Final.ADJ_CHAR_DED → exp_Init.ADJ_CHAR_DED → SQ_CPM_NEWPAY_TBL.ADJ_CHAR_DED → CPM_NEWPAY_TBL.ADJ_CHAR_DED | CPM_NEWPAY_TBL.ADJ_CHAR_DED |
| nihtest_NIH_PAYROLL_MASTER | ADJ_UNION_DED | exp_Final.ADJ_UNION_DED → exp_Init.ADJ_UNION_DED → SQ_CPM_NEWPAY_TBL.ADJ_UNION_DED → CPM_NEWPAY_TBL.ADJ_UNION_DED | CPM_NEWPAY_TBL.ADJ_UNION_DED |
| nihtest_NIH_PAYROLL_MASTER | ADJ_REFUND_DED | exp_Final.ADJ_REFUND_DED → exp_Init.ADJ_REFUND_DED → SQ_CPM_NEWPAY_TBL.ADJ_REFUND_DED → CPM_NEWPAY_TBL.ADJ_REFUND_DED | CPM_NEWPAY_TBL.ADJ_REFUND_DED |
| nihtest_NIH_PAYROLL_MASTER | ADJ_QUARTERS_DED | exp_Final.ADJ_QUARTERS_DED → exp_Init.ADJ_QUARTERS_DED → SQ_CPM_NEWPAY_TBL.ADJ_QUARTERS_DED → CPM_NEWPAY_TBL.ADJ_QUARTERS_DED | CPM_NEWPAY_TBL.ADJ_QUARTERS_DED |
| nihtest_NIH_PAYROLL_MASTER | ADJ_SUBSIST_DED | exp_Final.ADJ_SUBSIST_DED → exp_Init.ADJ_SUBSIST_DED → SQ_CPM_NEWPAY_TBL.ADJ_SUBSIST_DED → CPM_NEWPAY_TBL.ADJ_SUBSIST_DED | CPM_NEWPAY_TBL.ADJ_SUBSIST_DED |
| nihtest_NIH_PAYROLL_MASTER | ADJ_LAUNDRY_DED | exp_Final.ADJ_LAUNDRY_DED → exp_Set_Defaults.o_DEFAULT_NUM_2 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | ADJ_NET_PAY | exp_Final.ADJ_NET_PAY → exp_Init.ADJ_NET_PAY → SQ_CPM_NEWPAY_TBL.ADJ_NET_PAY → CPM_NEWPAY_TBL.ADJ_NET_PAY | CPM_NEWPAY_TBL.ADJ_NET_PAY |
| nihtest_NIH_PAYROLL_MASTER | EIC_ADJ_PAY | exp_Final.EIC_ADJ_PAY → exp_Init.EIC_ADJ_PAY → SQ_CPM_NEWPAY_TBL.EIC_ADJ_PAY → CPM_NEWPAY_TBL.EIC_ADJ_PAY | CPM_NEWPAY_TBL.EIC_ADJ_PAY |
| nihtest_NIH_PAYROLL_MASTER | PCA_ADJ_PAY | exp_Final.PCA_ADJ_PAY → exp_Init.PCA_ADJ_PAY → SQ_CPM_NEWPAY_TBL.PCA_ADJ_PAY → CPM_NEWPAY_TBL.PCA_ADJ_PAY | CPM_NEWPAY_TBL.PCA_ADJ_PAY |
| nihtest_NIH_PAYROLL_MASTER | ADJ_TSPA_PAY_SUB | exp_Final.ADJ_TSPA_PAY_SUB → exp_Init.ADJ_TSPA_PAY_SUB → SQ_CPM_NEWPAY_TBL.ADJ_TSPA_PAY_SUB → CPM_NEWPAY_TBL.ADJ_TSPA_PAY_SUB | CPM_NEWPAY_TBL.ADJ_TSPA_PAY_SUB |
| nihtest_NIH_PAYROLL_MASTER | ADJ_TSPG_GBADIST | exp_Final.ADJ_TSPG_GBADIST → exp_Init.ADJ_TSPG_GBADIST → SQ_CPM_NEWPAY_TBL.ADJ_TSPG_GBADIST → CPM_NEWPAY_TBL.ADJ_TSPG_GBADIST | CPM_NEWPAY_TBL.ADJ_TSPG_GBADIST |
| nihtest_NIH_PAYROLL_MASTER | ADJ_TSPG_EADIST | exp_Final.ADJ_TSPG_EADIST → exp_Init.ADJ_TSPG_EADIST → SQ_CPM_NEWPAY_TBL.ADJ_TSPG_EADIST → CPM_NEWPAY_TBL.ADJ_TSPG_EADIST | CPM_NEWPAY_TBL.ADJ_TSPG_EADIST |
| nihtest_NIH_PAYROLL_MASTER | ADJ_TSPG_GMADIST | exp_Final.ADJ_TSPG_GMADIST → exp_Init.ADJ_TSPG_GMADIST → SQ_CPM_NEWPAY_TBL.ADJ_TSPG_GMADIST → CPM_NEWPAY_TBL.ADJ_TSPG_GMADIST | CPM_NEWPAY_TBL.ADJ_TSPG_GMADIST |
| nihtest_NIH_PAYROLL_MASTER | UNCOM_TOUR_AN_LV_FACT | exp_Final.UNCOM_TOUR_AN_LV_FACT → exp_Set_Defaults.o_DEFAULT_NUM_2 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | UNCOM_TOUR_SICK_LVFACT | exp_Final.UNCOM_TOUR_SICK_LVFACT → exp_Set_Defaults.o_DEFAULT_NUM_2 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | AN_LV_CR_RED | exp_Final.AN_LV_CR_RED → exp_Init.AN_LV_CR_RED → SQ_CPM_NEWPAY_TBL.AN_LV_CR_RED → CPM_NEWPAY_TBL.AN_LV_CR_RED | CPM_NEWPAY_TBL.AN_LV_CR_RED |
| nihtest_NIH_PAYROLL_MASTER | SICK_LV_CR_RED | exp_Final.SICK_LV_CR_RED → exp_Init.SICK_LV_CR_RED → SQ_CPM_NEWPAY_TBL.SICK_LV_CR_RED → CPM_NEWPAY_TBL.SICK_LV_CR_RED | CPM_NEWPAY_TBL.SICK_LV_CR_RED |
| nihtest_NIH_PAYROLL_MASTER | AN_LV_EARNED_CPP | exp_Final.AN_LV_EARNED_CPP → exp_Init.AN_LV_EARNED_CPP → SQ_CPM_NEWPAY_TBL.AN_LV_EARNED_CPP → CPM_NEWPAY_TBL.AN_LV_EARNED_CPP | CPM_NEWPAY_TBL.AN_LV_EARNED_CPP |
| nihtest_NIH_PAYROLL_MASTER | AN_LV_USED_CPP | exp_Final.AN_LV_USED_CPP → exp_Init.AN_LV_USED_CPP → SQ_CPM_NEWPAY_TBL.AN_LV_USED_CPP → CPM_NEWPAY_TBL.AN_LV_USED_CPP | CPM_NEWPAY_TBL.AN_LV_USED_CPP |
| nihtest_NIH_PAYROLL_MASTER | AN_LV_PRYR_BAL | exp_Final.AN_LV_PRYR_BAL → exp_Set_Defaults.o_DEFAULT_NUM_2 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | AN_LV_ERND_YTD | exp_Final.AN_LV_ERND_YTD → exp_Init.AN_LV_ERND_YTD → SQ_CPM_NEWPAY_TBL.AN_LV_ERND_YTD → CPM_NEWPAY_TBL.AN_LV_ERND_YTD | CPM_NEWPAY_TBL.AN_LV_ERND_YTD |
| nihtest_NIH_PAYROLL_MASTER | AN_LV_ADV_CPP | exp_Final.AN_LV_ADV_CPP → exp_Set_Defaults.o_DEFAULT_NUM_2 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | AN_LV_ADV_CBAL | exp_Final.AN_LV_ADV_CBAL → exp_Init.AN_LV_ADV_CBAL → SQ_CPM_NEWPAY_TBL.AN_LV_ADV_CBAL → CPM_NEWPAY_TBL.AN_LV_ADV_CBAL | CPM_NEWPAY_TBL.AN_LV_ADV_CBAL |
| nihtest_NIH_PAYROLL_MASTER | AN_LV_USED_YTD | exp_Final.AN_LV_USED_YTD → exp_Init.AN_LV_USED_YTD → SQ_CPM_NEWPAY_TBL.AN_LV_USED_YTD → CPM_NEWPAY_TBL.AN_LV_USED_YTD | CPM_NEWPAY_TBL.AN_LV_USED_YTD |
| nihtest_NIH_PAYROLL_MASTER | AN_LV_CUR_BAL | exp_Final.AN_LV_CUR_BAL → exp_Init.AN_LV_CUR_BAL → SQ_CPM_NEWPAY_TBL.AN_LV_CUR_BAL → CPM_NEWPAY_TBL.AN_LV_CUR_BAL | CPM_NEWPAY_TBL.AN_LV_CUR_BAL |
| nihtest_NIH_PAYROLL_MASTER | AN_LV_MAX_COVER | exp_Final.AN_LV_MAX_COVER → exp_Init.AN_LV_MAX_COVER → SQ_CPM_NEWPAY_TBL.AN_LV_MAX_COVER → CPM_NEWPAY_TBL.AN_LV_MAX_COVER | CPM_NEWPAY_TBL.AN_LV_MAX_COVER |
| nihtest_NIH_PAYROLL_MASTER | AN_LV_USE_LOSE | exp_Final.AN_LV_USE_LOSE → exp_Init.AN_LV_USE_LOSE → SQ_CPM_NEWPAY_TBL.AN_LV_USE_LOSE → CPM_NEWPAY_TBL.AN_LV_USE_LOSE | CPM_NEWPAY_TBL.AN_LV_USE_LOSE |
| nihtest_NIH_PAYROLL_MASTER | AN_LV_PTHRS_WK | exp_Final.AN_LV_PTHRS_WK → exp_Set_Defaults.o_DEFAULT_NUM_2 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | SICK_LV_ERN_CPP | exp_Final.SICK_LV_ERN_CPP → exp_Init.SICK_LV_ERN_CPP → SQ_CPM_NEWPAY_TBL.SICK_LV_ERN_CPP → CPM_NEWPAY_TBL.SICK_LV_ERN_CPP | CPM_NEWPAY_TBL.SICK_LV_ERN_CPP |
| nihtest_NIH_PAYROLL_MASTER | SICK_LV_USD_CPP | exp_Final.SICK_LV_USD_CPP → exp_Init.SICK_LV_USD_CPP → SQ_CPM_NEWPAY_TBL.SICK_LV_USD_CPP → CPM_NEWPAY_TBL.SICK_LV_USD_CPP | CPM_NEWPAY_TBL.SICK_LV_USD_CPP |
| nihtest_NIH_PAYROLL_MASTER | SICK_LV_PRYR_BL | exp_Final.SICK_LV_PRYR_BL → exp_Set_Defaults.o_DEFAULT_NUM_2 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | SICK_LV_ERN_YTD | exp_Final.SICK_LV_ERN_YTD → exp_Init.SICK_LV_ERN_YTD → SQ_CPM_NEWPAY_TBL.SICK_LV_ERN_YTD → CPM_NEWPAY_TBL.SICK_LV_ERN_YTD | CPM_NEWPAY_TBL.SICK_LV_ERN_YTD |
| nihtest_NIH_PAYROLL_MASTER | SICK_LV_ADV_CPP | exp_Final.SICK_LV_ADV_CPP → exp_Set_Defaults.o_DEFAULT_NUM_2 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | SICK_LV_AD_CBAL | exp_Final.SICK_LV_AD_CBAL → exp_Init.SICK_LV_AD_CBAL → SQ_CPM_NEWPAY_TBL.SICK_LV_AD_CBAL → CPM_NEWPAY_TBL.SICK_LV_AD_CBAL | CPM_NEWPAY_TBL.SICK_LV_AD_CBAL |
| nihtest_NIH_PAYROLL_MASTER | SICK_LV_USD_YTD | exp_Final.SICK_LV_USD_YTD → exp_Init.SICK_LV_USD_YTD → SQ_CPM_NEWPAY_TBL.SICK_LV_USD_YTD → CPM_NEWPAY_TBL.SICK_LV_USD_YTD | CPM_NEWPAY_TBL.SICK_LV_USD_YTD |
| nihtest_NIH_PAYROLL_MASTER | SICK_LV_CUR_BAL | exp_Final.SICK_LV_CUR_BAL → exp_Init.SICK_LV_CUR_BAL → SQ_CPM_NEWPAY_TBL.SICK_LV_CUR_BAL → CPM_NEWPAY_TBL.SICK_LV_CUR_BAL | CPM_NEWPAY_TBL.SICK_LV_CUR_BAL |
| nihtest_NIH_PAYROLL_MASTER | SICK_LV_PTHR_WK | exp_Final.SICK_LV_PTHR_WK → exp_Set_Defaults.o_DEFAULT_NUM_2 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | COMP_LV_ERN_CPP | exp_Final.COMP_LV_ERN_CPP → exp_Init.COMP_LV_ERN_CPP → SQ_CPM_NEWPAY_TBL.COMP_LV_ERN_CPP → CPM_NEWPAY_TBL.COMP_LV_ERN_CPP | CPM_NEWPAY_TBL.COMP_LV_ERN_CPP |
| nihtest_NIH_PAYROLL_MASTER | COMP_LV_USD_CPP | exp_Final.COMP_LV_USD_CPP → exp_Init.COMP_LV_USD_CPP → SQ_CPM_NEWPAY_TBL.COMP_LV_USD_CPP → CPM_NEWPAY_TBL.COMP_LV_USD_CPP | CPM_NEWPAY_TBL.COMP_LV_USD_CPP |
| nihtest_NIH_PAYROLL_MASTER | COMP_LV_CUR_BAL | exp_Final.COMP_LV_CUR_BAL → exp_Init.COMP_LV_CUR_BAL → SQ_CPM_NEWPAY_TBL.COMP_LV_CUR_BAL → CPM_NEWPAY_TBL.COMP_LV_CUR_BAL | CPM_NEWPAY_TBL.COMP_LV_CUR_BAL |
| nihtest_NIH_PAYROLL_MASTER | ADMIN_LV_CPP | exp_Final.ADMIN_LV_CPP → exp_Init.ADMIN_LV_CPP → SQ_CPM_NEWPAY_TBL.ADMIN_LV_CPP → CPM_NEWPAY_TBL.ADMIN_LV_CPP | CPM_NEWPAY_TBL.ADMIN_LV_CPP |
| nihtest_NIH_PAYROLL_MASTER | ADMIN_LV_YTD | exp_Final.ADMIN_LV_YTD → exp_Init.ADMIN_LV_YTD → SQ_CPM_NEWPAY_TBL.ADMIN_LV_YTD → CPM_NEWPAY_TBL.ADMIN_LV_YTD | CPM_NEWPAY_TBL.ADMIN_LV_YTD |
| nihtest_NIH_PAYROLL_MASTER | MILITARY_LV_YTD | exp_Final.MILITARY_LV_YTD → exp_Init.MILITARY_LV_YTD → SQ_CPM_NEWPAY_TBL.MILITARY_LV_YTD → CPM_NEWPAY_TBL.MILITARY_LV_YTD | CPM_NEWPAY_TBL.MILITARY_LV_YTD |
| nihtest_NIH_PAYROLL_MASTER | COURT_LV_CPP | exp_Final.COURT_LV_CPP → exp_Set_Defaults.o_DEFAULT_NUM_3 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | COURT_LV_YTD | exp_Final.COURT_LV_YTD → exp_Set_Defaults.o_DEFAULT_NUM_3 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | LWOP_CPP | exp_Final.LWOP_CPP → exp_Init.LWOP_CPP → SQ_CPM_NEWPAY_TBL.LWOP_CPP → CPM_NEWPAY_TBL.LWOP_CPP | CPM_NEWPAY_TBL.LWOP_CPP |
| nihtest_NIH_PAYROLL_MASTER | LWOP_YTD | exp_Final.LWOP_YTD → exp_Init.LWOP_YTD → SQ_CPM_NEWPAY_TBL.LWOP_YTD → CPM_NEWPAY_TBL.LWOP_YTD | CPM_NEWPAY_TBL.LWOP_YTD |
| nihtest_NIH_PAYROLL_MASTER | AWOL_CPP | exp_Final.AWOL_CPP → exp_Set_Defaults.o_DEFAULT_NUM_3 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | AWOL_YTD | exp_Final.AWOL_YTD → exp_Set_Defaults.o_DEFAULT_NUM_3 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | LWOP_AWOP_LSPSI | exp_Final.LWOP_AWOP_LSPSI → exp_Set_Defaults.o_DEFAULT_NUM_3 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | COMP_TIME_FOR_CPP | exp_Final.COMP_TIME_FOR_CPP → exp_Set_Defaults.o_DEFAULT_NUM_3 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | REG_HRS_CPP | exp_Final.REG_HRS_CPP → exp_Init.REG_HRS_CPP → SQ_CPM_NEWPAY_TBL.REG_HRS_CPP → CPM_NEWPAY_TBL.REG_HRS_CPP | CPM_NEWPAY_TBL.REG_HRS_CPP |
| nihtest_NIH_PAYROLL_MASTER | REG_HRS_YTD | exp_Final.REG_HRS_YTD → exp_Set_Defaults.o_DEFAULT_NUM_3 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | HRS_OT_1 | exp_Final.HRS_OT_1 → exp_Init.HRS_OT_1 → SQ_CPM_NEWPAY_TBL.HRS_OT_1 → CPM_NEWPAY_TBL.HRS_OT_1 | CPM_NEWPAY_TBL.HRS_OT_1 |
| nihtest_NIH_PAYROLL_MASTER | HRS_OT_YTD | exp_Final.HRS_OT_YTD → exp_Set_Defaults.o_DEFAULT_NUM_3 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | HRS_ND_1 | exp_Final.HRS_ND_1 → exp_Init.HRS_ND_1 → SQ_CPM_NEWPAY_TBL.HRS_ND_1 → CPM_NEWPAY_TBL.HRS_ND_1 | CPM_NEWPAY_TBL.HRS_ND_1 |
| nihtest_NIH_PAYROLL_MASTER | HRS_ND_2 | exp_Final.HRS_ND_2 → exp_Init.HRS_ND_2 → SQ_CPM_NEWPAY_TBL.HRS_ND_2 → CPM_NEWPAY_TBL.HRS_ND_2 | CPM_NEWPAY_TBL.HRS_ND_2 |
| nihtest_NIH_PAYROLL_MASTER | HRS_ND_3 | exp_Final.HRS_ND_3 → exp_Init.HRS_ND_3 → SQ_CPM_NEWPAY_TBL.HRS_ND_3 → CPM_NEWPAY_TBL.HRS_ND_3 | CPM_NEWPAY_TBL.HRS_ND_3 |
| nihtest_NIH_PAYROLL_MASTER | HRS_ND_YTD | exp_Final.HRS_ND_YTD → exp_Set_Defaults.o_DEFAULT_NUM_3 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | HRS_SD_1 | exp_Final.HRS_SD_1 → exp_Init.HRS_SD_1 → SQ_CPM_NEWPAY_TBL.HRS_SD_1 → CPM_NEWPAY_TBL.HRS_SD_1 | CPM_NEWPAY_TBL.HRS_SD_1 |
| nihtest_NIH_PAYROLL_MASTER | HRS_SD_YTD | exp_Final.HRS_SD_YTD → exp_Set_Defaults.o_DEFAULT_NUM_3 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | HRS_HOL_1 | exp_Final.HRS_HOL_1 → exp_Init.HRS_HOL_1 → SQ_CPM_NEWPAY_TBL.HRS_HOL_1 → CPM_NEWPAY_TBL.HRS_HOL_1 | CPM_NEWPAY_TBL.HRS_HOL_1 |
| nihtest_NIH_PAYROLL_MASTER | HRS_HOL_YTD | exp_Final.HRS_HOL_YTD → exp_Set_Defaults.o_DEFAULT_NUM_3 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | HRS_OTHER_CPP | exp_Final.HRS_OTHER_CPP → exp_Set_Defaults.o_DEFAULT_NUM_3 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | HRS_OTHER_YTD | exp_Final.HRS_OTHER_YTD → exp_Set_Defaults.o_DEFAULT_NUM_3 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | HRS_OT_PL | exp_Final.HRS_OT_PL → exp_Init.HRS_OT_PL → SQ_CPM_NEWPAY_TBL.HRS_OT_PL → CPM_NEWPAY_TBL.HRS_OT_PL | CPM_NEWPAY_TBL.HRS_OT_PL |
| nihtest_NIH_PAYROLL_MASTER | STAFFING_BIW_AMT | exp_Final.STAFFING_BIW_AMT → exp_Init.STAFFING_BIW_AMT → SQ_CPM_NEWPAY_TBL.STAFFING_BIW_AMT → CPM_NEWPAY_TBL.STAFFING_BIW_AMT | CPM_NEWPAY_TBL.STAFFING_BIW_AMT |
| nihtest_NIH_PAYROLL_MASTER | CPP_STAFFING | exp_Final.CPP_STAFFING → exp_Init.CPP_STAFFING → SQ_CPM_NEWPAY_TBL.CPP_STAFFING → CPM_NEWPAY_TBL.CPP_STAFFING | CPM_NEWPAY_TBL.CPP_STAFFING |
| nihtest_NIH_PAYROLL_MASTER | YTD_STAFFING | exp_Final.YTD_STAFFING → exp_Init.YTD_STAFFING → SQ_CPM_NEWPAY_TBL.YTD_STAFFING → CPM_NEWPAY_TBL.YTD_STAFFING | CPM_NEWPAY_TBL.YTD_STAFFING |
| nihtest_NIH_PAYROLL_MASTER | TRANSFER_IN_FICA_PAY | exp_Final.TRANSFER_IN_FICA_PAY → exp_Init.TRANSFER_IN_FICA_PAY → SQ_CPM_NEWPAY_TBL.TRANSFER_IN_FICA_PAY → CPM_NEWPAY_TBL.TRANSFER_IN_FICA_PAY | CPM_NEWPAY_TBL.TRANSFER_IN_FICA_PAY |
| nihtest_NIH_PAYROLL_MASTER | COMP_HRS_PAID | exp_Final.COMP_HRS_PAID → exp_Init.COMP_HRS_PAID → SQ_CPM_NEWPAY_TBL.COMP_HRS_PAID → CPM_NEWPAY_TBL.COMP_HRS_PAID | CPM_NEWPAY_TBL.COMP_HRS_PAID |
| nihtest_NIH_PAYROLL_MASTER | COMP_TIME_HRLY_RATE | exp_Final.COMP_TIME_HRLY_RATE → exp_Init.COMP_TIME_HRLY_RATE → SQ_CPM_NEWPAY_TBL.COMP_TIME_HRLY_RATE → CPM_NEWPAY_TBL.COMP_TIME_HRLY_RATE | CPM_NEWPAY_TBL.COMP_TIME_HRLY_RATE |
| nihtest_NIH_PAYROLL_MASTER | CPP_ALT_4_DED | exp_Final.CPP_ALT_4_DED → exp_Init.CPP_ALT_4_DED → SQ_CPM_NEWPAY_TBL.CPP_ALT_4_DED → CPM_NEWPAY_TBL.CPP_ALT_4_DED | CPM_NEWPAY_TBL.CPP_ALT_4_DED |
| nihtest_NIH_PAYROLL_MASTER | CPP_LOAN_1_DED | exp_Final.CPP_LOAN_1_DED → exp_Init.CPP_LOAN_1_DED → SQ_CPM_NEWPAY_TBL.CPP_LOAN_1_DED → CPM_NEWPAY_TBL.CPP_LOAN_1_DED | CPM_NEWPAY_TBL.CPP_LOAN_1_DED |
| nihtest_NIH_PAYROLL_MASTER | YTD_LOAN_1_DED | exp_Final.YTD_LOAN_1_DED → exp_Init.YTD_LOAN_1_DED → SQ_CPM_NEWPAY_TBL.YTD_LOAN_1_DED → CPM_NEWPAY_TBL.YTD_LOAN_1_DED | CPM_NEWPAY_TBL.YTD_LOAN_1_DED |
| nihtest_NIH_PAYROLL_MASTER | ADJ_LOAN_1_DED | exp_Final.ADJ_LOAN_1_DED → exp_Init.ADJ_LOAN_1_DED → SQ_CPM_NEWPAY_TBL.ADJ_LOAN_1_DED → CPM_NEWPAY_TBL.ADJ_LOAN_1_DED | CPM_NEWPAY_TBL.ADJ_LOAN_1_DED |
| nihtest_NIH_PAYROLL_MASTER | CPP_COUNTY_TAX_GROSS | exp_Final.CPP_COUNTY_TAX_GROSS → exp_Init.CPP_COUNTY_TAX_GROSS → SQ_CPM_NEWPAY_TBL.CPP_COUNTY_TAX_GROSS → CPM_NEWPAY_TBL.CPP_COUNTY_TAX_GROSS | CPM_NEWPAY_TBL.CPP_COUNTY_TAX_GROSS |
| nihtest_NIH_PAYROLL_MASTER | CPP_ST_TAX_GROSS | exp_Final.CPP_ST_TAX_GROSS → exp_Convert.o_CPP_ST_TAX_GROSS = DECODE(TRUE, ISNULL(CPP_ST_TAX_GROSS), 0, NOT ISNULL(CPP_ST_TAX_GROSS) AND v_CPP_ST_TAX_GROSS_EXCEEDS_LIMIT_FLAG = TRUE, v_CPP_ST_TAX_GROSS_SIGN * TO_DECIMAL( v_CPP_ST_TAX_GROSS_BEFORE_DEC \|\| '.' \|\| v_CPP_ST_TAX_GROSS_AFTER_DEC , 2), NOT ISNULL(CPP_ST_TAX_GROSS), CPP_ST_TAX_GROSS, 0) → exp_Init.CPP_ST_TAX_GROSS → SQ_CPM_NEWPAY_TBL.CPP_ST_TAX_GROSS → CPM_NEWPAY_TBL.CPP_ST_TAX_GROSS → exp_Convert.v_CPP_ST_TAX_GROSS_EXCEEDS_LIMIT_FLAG = IIF( ABS(CPP_ST_TAX_GROSS) > 99999.99, TRUE, FALSE) → exp_Convert.v_CPP_ST_TAX_GROSS_SIGN = SIGN(CPP_ST_TAX_GROSS) → exp_Convert.v_CPP_ST_TAX_GROSS_BEFORE_DEC = SUBSTR(v_CPP_ST_TAX_GROSS_CHAR, v_CPP_ST_TAX_GROSS_POS_DEC - 5, 5) → exp_Convert.v_CPP_ST_TAX_GROSS_CHAR = TO_CHAR(ABS(TO_DECIMAL(CPP_ST_TAX_GROSS, 2))) → exp_Convert.v_CPP_ST_TAX_GROSS_POS_DEC = INSTR(v_CPP_ST_TAX_GROSS_CHAR, '.') → exp_Convert.v_CPP_ST_TAX_GROSS_AFTER_DEC = SUBSTR(v_CPP_ST_TAX_GROSS_CHAR, v_CPP_ST_TAX_GROSS_POS_DEC + 1, 2) | CPM_NEWPAY_TBL.CPP_ST_TAX_GROSS |
| nihtest_NIH_PAYROLL_MASTER | TRANSFER_IN_FICA_DED | exp_Final.TRANSFER_IN_FICA_DED → exp_Init.TRANSFER_IN_FICA_DED → SQ_CPM_NEWPAY_TBL.TRANSFER_IN_FICA_DED → CPM_NEWPAY_TBL.TRANSFER_IN_FICA_DED | CPM_NEWPAY_TBL.TRANSFER_IN_FICA_DED |
| nihtest_NIH_PAYROLL_MASTER | CPP_INST_AGY_PAID | exp_Final.CPP_INST_AGY_PAID → exp_Init.CPP_INST_AGY_PAID → SQ_CPM_NEWPAY_TBL.CPP_INST_AGY_PAID → CPM_NEWPAY_TBL.CPP_INST_AGY_PAID | CPM_NEWPAY_TBL.CPP_INST_AGY_PAID |
| nihtest_NIH_PAYROLL_MASTER | CPP_ON_CALL_PAY | exp_Final.CPP_ON_CALL_PAY → exp_Init.CPP_ON_CALL_PAY → SQ_CPM_NEWPAY_TBL.CPP_ON_CALL_PAY → CPM_NEWPAY_TBL.CPP_ON_CALL_PAY | CPM_NEWPAY_TBL.CPP_ON_CALL_PAY |
| nihtest_NIH_PAYROLL_MASTER | YTD_ON_CALL_PAY | exp_Final.YTD_ON_CALL_PAY → exp_Init.YTD_ON_CALL_PAY → SQ_CPM_NEWPAY_TBL.YTD_ON_CALL_PAY → CPM_NEWPAY_TBL.YTD_ON_CALL_PAY | CPM_NEWPAY_TBL.YTD_ON_CALL_PAY |
| nihtest_NIH_PAYROLL_MASTER | ADJ_ON_CALL_PAY | exp_Final.ADJ_ON_CALL_PAY → exp_Init.ADJ_ON_CALL_PAY → SQ_CPM_NEWPAY_TBL.ADJ_ON_CALL_PAY → CPM_NEWPAY_TBL.ADJ_ON_CALL_PAY | CPM_NEWPAY_TBL.ADJ_ON_CALL_PAY |
| nihtest_NIH_PAYROLL_MASTER | CPP_ON_CALL_HRS | exp_Final.CPP_ON_CALL_HRS → exp_Init.CPP_ON_CALL_HRS → SQ_CPM_NEWPAY_TBL.CPP_ON_CALL_HRS → CPM_NEWPAY_TBL.CPP_ON_CALL_HRS | CPM_NEWPAY_TBL.CPP_ON_CALL_HRS |
| nihtest_NIH_PAYROLL_MASTER | YTD_ON_CALL_HRS | exp_Final.YTD_ON_CALL_HRS → exp_Set_Defaults.o_DEFAULT_NUM_4 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | CPP_LOCAL_DIFF | exp_Final.CPP_LOCAL_DIFF → exp_Init.CPP_LOCAL_DIFF → SQ_CPM_NEWPAY_TBL.CPP_LOCAL_DIFF → CPM_NEWPAY_TBL.CPP_LOCAL_DIFF | CPM_NEWPAY_TBL.CPP_LOCAL_DIFF |
| nihtest_NIH_PAYROLL_MASTER | INCENT_TIME_EARNED | exp_Final.INCENT_TIME_EARNED → exp_Set_Defaults.o_DEFAULT_NUM_4 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | INCENT_TIME_USED | exp_Final.INCENT_TIME_USED → exp_Set_Defaults.o_DEFAULT_NUM_4 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | INCENT_TIME_CUR_BAL | exp_Final.INCENT_TIME_CUR_BAL → exp_Init.INCENT_TIME_CUR_BAL → SQ_CPM_NEWPAY_TBL.INCENT_TIME_CUR_BAL → CPM_NEWPAY_TBL.INCENT_TIME_CUR_BAL | CPM_NEWPAY_TBL.INCENT_TIME_CUR_BAL |
| nihtest_NIH_PAYROLL_MASTER | BAYLR_REG_HRS_CPP | exp_Final.BAYLR_REG_HRS_CPP → exp_Set_Defaults.o_DEFAULT_NUM_4 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | BAYLR_REG_HRS_YTD | exp_Final.BAYLR_REG_HRS_YTD → exp_Set_Defaults.o_DEFAULT_NUM_4 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | CPP_BAYLR_BP | exp_Final.CPP_BAYLR_BP → exp_Set_Defaults.o_DEFAULT_NUM_4 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | YTD_BAYLR_BP | exp_Final.YTD_BAYLR_BP → exp_Set_Defaults.o_DEFAULT_NUM_4 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | NON_BAYLR_REG_HRS_CPP | exp_Final.NON_BAYLR_REG_HRS_CPP → exp_Set_Defaults.o_DEFAULT_NUM_4 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | NON_BAYLR_REG_HRS_YTD | exp_Final.NON_BAYLR_REG_HRS_YTD → exp_Set_Defaults.o_DEFAULT_NUM_4 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | CPP_NON_BAYLR_BP | exp_Final.CPP_NON_BAYLR_BP → exp_Set_Defaults.o_DEFAULT_NUM_4 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | YTD_NON_BAYLR_BP | exp_Final.YTD_NON_BAYLR_BP → exp_Set_Defaults.o_DEFAULT_NUM_4 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | T38_OT_HRS_CPP | exp_Final.T38_OT_HRS_CPP → exp_Init.T38_OT_HRS_CPP → SQ_CPM_NEWPAY_TBL.T38_OT_HRS_CPP → CPM_NEWPAY_TBL.T38_OT_HRS_CPP | CPM_NEWPAY_TBL.T38_OT_HRS_CPP |
| nihtest_NIH_PAYROLL_MASTER | T38_HOL_OT_HRS_CPP | exp_Final.T38_HOL_OT_HRS_CPP → exp_Init.T38_HOL_OT_HRS_CPP → SQ_CPM_NEWPAY_TBL.T38_HOL_OT_HRS_CPP → CPM_NEWPAY_TBL.T38_HOL_OT_HRS_CPP | CPM_NEWPAY_TBL.T38_HOL_OT_HRS_CPP |
| nihtest_NIH_PAYROLL_MASTER | T38_ND_HRS_CPP | exp_Final.T38_ND_HRS_CPP → exp_Init.T38_ND_HRS_CPP → SQ_CPM_NEWPAY_TBL.T38_ND_HRS_CPP → CPM_NEWPAY_TBL.T38_ND_HRS_CPP | CPM_NEWPAY_TBL.T38_ND_HRS_CPP |
| nihtest_NIH_PAYROLL_MASTER | T38_ONCALL_HRS_CPP | exp_Final.T38_ONCALL_HRS_CPP → exp_Init.T38_ONCALL_HRS_CPP → SQ_CPM_NEWPAY_TBL.T38_ONCALL_HRS_CPP → CPM_NEWPAY_TBL.T38_ONCALL_HRS_CPP | CPM_NEWPAY_TBL.T38_ONCALL_HRS_CPP |
| nihtest_NIH_PAYROLL_MASTER | T38_SAT_DIF_HRS_CPP | exp_Final.T38_SAT_DIF_HRS_CPP → exp_Init.T38_SAT_DIF_HRS_CPP → SQ_CPM_NEWPAY_TBL.T38_SAT_DIF_HRS_CPP → CPM_NEWPAY_TBL.T38_SAT_DIF_HRS_CPP | CPM_NEWPAY_TBL.T38_SAT_DIF_HRS_CPP |
| nihtest_NIH_PAYROLL_MASTER | T38_SUN_DIF_HRS_CPP | exp_Final.T38_SUN_DIF_HRS_CPP → exp_Init.T38_SUN_DIF_HRS_CPP → SQ_CPM_NEWPAY_TBL.T38_SUN_DIF_HRS_CPP → CPM_NEWPAY_TBL.T38_SUN_DIF_HRS_CPP | CPM_NEWPAY_TBL.T38_SUN_DIF_HRS_CPP |
| nihtest_NIH_PAYROLL_MASTER | T38_OT_HRS_YTD | exp_Final.T38_OT_HRS_YTD → exp_Set_Defaults.o_DEFAULT_NUM_5 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | T38_HOL_OT_HRS_YTD | exp_Final.T38_HOL_OT_HRS_YTD → exp_Set_Defaults.o_DEFAULT_NUM_5 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | T38_ND_HRS_YTD | exp_Final.T38_ND_HRS_YTD → exp_Set_Defaults.o_DEFAULT_NUM_5 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | T38_ONCALL_HRS_YTD | exp_Final.T38_ONCALL_HRS_YTD → exp_Set_Defaults.o_DEFAULT_NUM_5 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | T38_SAT_DIF_HRS_YTD | exp_Final.T38_SAT_DIF_HRS_YTD → exp_Set_Defaults.o_DEFAULT_NUM_5 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | T38_SUN_DIF_HRS_YTD | exp_Final.T38_SUN_DIF_HRS_YTD → exp_Set_Defaults.o_DEFAULT_NUM_5 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | CPP_T38_OT_PAY | exp_Final.CPP_T38_OT_PAY → exp_Set_Defaults.o_DEFAULT_NUM_5 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | CPP_T38_HOL_OT_PAY | exp_Final.CPP_T38_HOL_OT_PAY → exp_Set_Defaults.o_DEFAULT_NUM_5 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | CPP_T38_ND_PAY | exp_Final.CPP_T38_ND_PAY → exp_Set_Defaults.o_DEFAULT_NUM_5 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | CPP_T38_ONCALL_PAY | exp_Final.CPP_T38_ONCALL_PAY → exp_Init.CPP_T38_ONCALL_PAY → SQ_CPM_NEWPAY_TBL.CPP_T38_ONCALL_PAY → CPM_NEWPAY_TBL.CPP_T38_ONCALL_PAY | CPM_NEWPAY_TBL.CPP_T38_ONCALL_PAY |
| nihtest_NIH_PAYROLL_MASTER | CPP_T38_SAT_DIF_PAY | exp_Final.CPP_T38_SAT_DIF_PAY → exp_Set_Defaults.o_DEFAULT_NUM_5 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | CPP_T38_SUN_DIF_PAY | exp_Final.CPP_T38_SUN_DIF_PAY → exp_Set_Defaults.o_DEFAULT_NUM_5 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | T38_OT_PAY_YTD | exp_Final.T38_OT_PAY_YTD → exp_Init.T38_OT_PAY_YTD → SQ_CPM_NEWPAY_TBL.T38_OT_PAY_YTD → CPM_NEWPAY_TBL.T38_OT_PAY_YTD | CPM_NEWPAY_TBL.T38_OT_PAY_YTD |
| nihtest_NIH_PAYROLL_MASTER | T38_HOL_OT_PAY_YTD | exp_Final.T38_HOL_OT_PAY_YTD → exp_Init.T38_HOL_OT_PAY_YTD → SQ_CPM_NEWPAY_TBL.T38_HOL_OT_PAY_YTD → CPM_NEWPAY_TBL.T38_HOL_OT_PAY_YTD | CPM_NEWPAY_TBL.T38_HOL_OT_PAY_YTD |
| nihtest_NIH_PAYROLL_MASTER | T38_ND_PAY_YTD | exp_Final.T38_ND_PAY_YTD → exp_Init.T38_ND_PAY_YTD → SQ_CPM_NEWPAY_TBL.T38_ND_PAY_YTD → CPM_NEWPAY_TBL.T38_ND_PAY_YTD | CPM_NEWPAY_TBL.T38_ND_PAY_YTD |
| nihtest_NIH_PAYROLL_MASTER | T38_ONCALL_PAY_YTD | exp_Final.T38_ONCALL_PAY_YTD → exp_Init.T38_ONCALL_PAY_YTD → SQ_CPM_NEWPAY_TBL.T38_ONCALL_PAY_YTD → CPM_NEWPAY_TBL.T38_ONCALL_PAY_YTD | CPM_NEWPAY_TBL.T38_ONCALL_PAY_YTD |
| nihtest_NIH_PAYROLL_MASTER | T38_SAT_DIF_PAY_YTD | exp_Final.T38_SAT_DIF_PAY_YTD → exp_Init.T38_SAT_DIF_PAY_YTD → SQ_CPM_NEWPAY_TBL.T38_SAT_DIF_PAY_YTD → CPM_NEWPAY_TBL.T38_SAT_DIF_PAY_YTD | CPM_NEWPAY_TBL.T38_SAT_DIF_PAY_YTD |
| nihtest_NIH_PAYROLL_MASTER | T38_SUN_DIF_PAY_YTD | exp_Final.T38_SUN_DIF_PAY_YTD → exp_Init.T38_SUN_DIF_PAY_YTD → SQ_CPM_NEWPAY_TBL.T38_SUN_DIF_PAY_YTD → CPM_NEWPAY_TBL.T38_SUN_DIF_PAY_YTD | CPM_NEWPAY_TBL.T38_SUN_DIF_PAY_YTD |
| nihtest_NIH_PAYROLL_MASTER | DCS_NBR_DEBTS | exp_Final.DCS_NBR_DEBTS → exp_Init.DCS_NBR_DEBTS → SQ_CPM_NEWPAY_TBL.DCS_NBR_DEBTS → CPM_NEWPAY_TBL.DCS_NBR_DEBTS | CPM_NEWPAY_TBL.DCS_NBR_DEBTS |
| nihtest_NIH_PAYROLL_MASTER | CPP_DCS_DEBT_AMT | exp_Final.CPP_DCS_DEBT_AMT → exp_Init.CPP_DCS_DEBT_AMT → SQ_CPM_NEWPAY_TBL.CPP_DCS_DEBT_AMT → CPM_NEWPAY_TBL.CPP_DCS_DEBT_AMT | CPM_NEWPAY_TBL.CPP_DCS_DEBT_AMT |
| nihtest_NIH_PAYROLL_MASTER | YTD_DCS_DEBT_AMT | exp_Final.YTD_DCS_DEBT_AMT → exp_Init.YTD_DCS_DEBT_AMT → SQ_CPM_NEWPAY_TBL.YTD_DCS_DEBT_AMT → CPM_NEWPAY_TBL.YTD_DCS_DEBT_AMT | CPM_NEWPAY_TBL.YTD_DCS_DEBT_AMT |
| nihtest_NIH_PAYROLL_MASTER | ADJ_DCS_DEBT_AMT | exp_Final.ADJ_DCS_DEBT_AMT → exp_Init.ADJ_DCS_DEBT_AMT → SQ_CPM_NEWPAY_TBL.ADJ_DCS_DEBT_AMT → CPM_NEWPAY_TBL.ADJ_DCS_DEBT_AMT | CPM_NEWPAY_TBL.ADJ_DCS_DEBT_AMT |
| nihtest_NIH_PAYROLL_MASTER | HRS_HAZARD_CPP | exp_Final.HRS_HAZARD_CPP → exp_Init.HRS_HAZARD_CPP → SQ_CPM_NEWPAY_TBL.HRS_HAZARD_CPP → CPM_NEWPAY_TBL.HRS_HAZARD_CPP | CPM_NEWPAY_TBL.HRS_HAZARD_CPP |
| nihtest_NIH_PAYROLL_MASTER | RET_BAL_FWD | exp_Final.RET_BAL_FWD → exp_Init.RET_BAL_FWD → SQ_CPM_NEWPAY_TBL.RET_BAL_FWD → CPM_NEWPAY_TBL.RET_BAL_FWD | CPM_NEWPAY_TBL.RET_BAL_FWD |
| nihtest_NIH_PAYROLL_MASTER | ANN_LV_VALUE | exp_Final.ANN_LV_VALUE → exp_Set_Defaults.o_DEFAULT_NUM_6 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | SICK_LV_VALUE | exp_Final.SICK_LV_VALUE → exp_Set_Defaults.o_DEFAULT_NUM_6 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | T38_REG_HRS_CPP | exp_Final.T38_REG_HRS_CPP → exp_Set_Defaults.o_DEFAULT_NUM_6 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | T38_REG_HRS_YTD | exp_Final.T38_REG_HRS_YTD → exp_Set_Defaults.o_DEFAULT_NUM_6 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | T38_BP_CPP | exp_Final.T38_BP_CPP → exp_Set_Defaults.o_DEFAULT_NUM_6 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | T38_BP_YTD | exp_Final.T38_BP_YTD → exp_Set_Defaults.o_DEFAULT_NUM_6 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | LOCAL_PCENT_RATE | exp_Final.LOCAL_PCENT_RATE → exp_Init.LOCAL_PCENT_RATE → SQ_CPM_NEWPAY_TBL.LOCAL_PCENT_RATE → CPM_NEWPAY_TBL.LOCAL_PCENT_RATE | CPM_NEWPAY_TBL.LOCAL_PCENT_RATE |
| nihtest_NIH_PAYROLL_MASTER | CPP_SEP_INCENT | exp_Final.CPP_SEP_INCENT → exp_Init.CPP_SEP_INCENT → SQ_CPM_NEWPAY_TBL.CPP_SEP_INCENT → CPM_NEWPAY_TBL.CPP_SEP_INCENT | CPM_NEWPAY_TBL.CPP_SEP_INCENT |
| nihtest_NIH_PAYROLL_MASTER | YTD_SEP_INCENT | exp_Final.YTD_SEP_INCENT → exp_Init.YTD_SEP_INCENT → SQ_CPM_NEWPAY_TBL.YTD_SEP_INCENT → CPM_NEWPAY_TBL.YTD_SEP_INCENT | CPM_NEWPAY_TBL.YTD_SEP_INCENT |
| nihtest_NIH_PAYROLL_MASTER | PSP_START_DATE | exp_Final.PSP_START_DATE → exp_Set_Defaults.o_DEFAULT_NUM_6 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | PSP_NTE_DATE | exp_Final.PSP_NTE_DATE → exp_Set_Defaults.o_DEFAULT_NUM_6 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | PSP_YRLY_PAY | exp_Final.PSP_YRLY_PAY → exp_Set_Defaults.o_DEFAULT_NUM_6 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | PSP_NTE_CONTRACT_AMT | exp_Final.PSP_NTE_CONTRACT_AMT → exp_Set_Defaults.o_DEFAULT_NUM_6 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | PSP_CONTR_TO_DATE | exp_Final.PSP_CONTR_TO_DATE → exp_Set_Defaults.o_DEFAULT_NUM_6 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | PSP_CONTR_YTD | exp_Final.PSP_CONTR_YTD → exp_Set_Defaults.o_DEFAULT_NUM_6 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | PSP_LGTH_SVC_INC_AMT | exp_Final.PSP_LGTH_SVC_INC_AMT → exp_Set_Defaults.o_DEFAULT_NUM_6 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | PSP_LGNTH_SVC_CHNG_DATE | exp_Final.PSP_LGNTH_SVC_CHNG_DATE → exp_Set_Defaults.o_DEFAULT_NUM_6 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | PSP_BIWKLY_AMT | exp_Final.PSP_BIWKLY_AMT → exp_Init.PSP_BIWKLY_AMT → SQ_CPM_NEWPAY_TBL.PSP_BIWKLY_AMT → CPM_NEWPAY_TBL.PSP_BIWKLY_AMT | CPM_NEWPAY_TBL.PSP_BIWKLY_AMT |
| nihtest_NIH_PAYROLL_MASTER | CPP_PSP_PAY | exp_Final.CPP_PSP_PAY → exp_Init.CPP_PSP_PAY → SQ_CPM_NEWPAY_TBL.CPP_PSP_PAY → CPM_NEWPAY_TBL.CPP_PSP_PAY | CPM_NEWPAY_TBL.CPP_PSP_PAY |
| nihtest_NIH_PAYROLL_MASTER | YTD_PSP_PAY | exp_Final.YTD_PSP_PAY → exp_Init.YTD_PSP_PAY → SQ_CPM_NEWPAY_TBL.YTD_PSP_PAY → CPM_NEWPAY_TBL.YTD_PSP_PAY | CPM_NEWPAY_TBL.YTD_PSP_PAY |
| nihtest_NIH_PAYROLL_MASTER | ADJ_PSP_PAY | exp_Final.ADJ_PSP_PAY → exp_Init.ADJ_PSP_PAY → SQ_CPM_NEWPAY_TBL.ADJ_PSP_PAY → CPM_NEWPAY_TBL.ADJ_PSP_PAY | CPM_NEWPAY_TBL.ADJ_PSP_PAY |
| nihtest_NIH_PAYROLL_MASTER | CPP_PSP_CSRS_DED | exp_Final.CPP_PSP_CSRS_DED → exp_Set_Defaults.o_DEFAULT_NUM_7 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | YTD_PSP_CSRS_DED | exp_Final.YTD_PSP_CSRS_DED → exp_Set_Defaults.o_DEFAULT_NUM_7 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | ADJ_PSP_CSRS_DED | exp_Final.ADJ_PSP_CSRS_DED → exp_Set_Defaults.o_DEFAULT_NUM_7 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | CPP_PSP_CSRS_GOVT | exp_Final.CPP_PSP_CSRS_GOVT → exp_Set_Defaults.o_DEFAULT_NUM_7 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | YTD_PSP_CSRS_GOVT | exp_Final.YTD_PSP_CSRS_GOVT → exp_Set_Defaults.o_DEFAULT_NUM_7 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | ADJ_PSP_CSRS_GOVT | exp_Final.ADJ_PSP_CSRS_GOVT → exp_Set_Defaults.o_DEFAULT_NUM_7 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | CPP_PSP_CSRS_PAY | exp_Final.CPP_PSP_CSRS_PAY → exp_Set_Defaults.o_DEFAULT_NUM_7 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | YTD_PSP_CSRS_PAY | exp_Final.YTD_PSP_CSRS_PAY → exp_Set_Defaults.o_DEFAULT_NUM_7 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | ADJ_PSP_CSRS_PAY | exp_Final.ADJ_PSP_CSRS_PAY → exp_Set_Defaults.o_DEFAULT_NUM_7 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | PSP_CSRS_BAL_FWRD | exp_Final.PSP_CSRS_BAL_FWRD → exp_Set_Defaults.o_DEFAULT_NUM_7 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | CPP_PSP_FERS_DED | exp_Final.CPP_PSP_FERS_DED → exp_Set_Defaults.o_DEFAULT_NUM_7 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | YTD_PSP_FERS_DED | exp_Final.YTD_PSP_FERS_DED → exp_Set_Defaults.o_DEFAULT_NUM_7 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | ADJ_PSP_FERS_DED | exp_Final.ADJ_PSP_FERS_DED → exp_Set_Defaults.o_DEFAULT_NUM_7 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | CPP_PSP_FERS_GOVT | exp_Final.CPP_PSP_FERS_GOVT → exp_Set_Defaults.o_DEFAULT_NUM_7 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | YTD_PSP_FERS_GOVT | exp_Final.YTD_PSP_FERS_GOVT → exp_Set_Defaults.o_DEFAULT_NUM_7 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | ADJ_PSP_FERS_GOVT | exp_Final.ADJ_PSP_FERS_GOVT → exp_Set_Defaults.o_DEFAULT_NUM_7 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | CPP_PSP_FERS_PAY | exp_Final.CPP_PSP_FERS_PAY → exp_Set_Defaults.o_DEFAULT_NUM_7 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | YTD_PSP_FERS_PAY | exp_Final.YTD_PSP_FERS_PAY → exp_Set_Defaults.o_DEFAULT_NUM_7 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | ADJ_PSP_FERS_PAY | exp_Final.ADJ_PSP_FERS_PAY → exp_Set_Defaults.o_DEFAULT_NUM_7 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | RESTOR_AL_USED_CPP | exp_Final.RESTOR_AL_USED_CPP → exp_Set_Defaults.o_DEFAULT_NUM_7 = 0 | literal/expression: 0 |
| nihtest_NIH_PAYROLL_MASTER | RESTOR_AL_USED_YTD | exp_Final.RESTOR_AL_USED_YTD → exp_Init.RESTOR_AL_USED_YTD → SQ_CPM_NEWPAY_TBL.RESTOR_AL_USED_YTD → CPM_NEWPAY_TBL.RESTOR_AL_USED_YTD | CPM_NEWPAY_TBL.RESTOR_AL_USED_YTD |
| nihtest_NIH_PAYROLL_MASTER | RESTOR_AL_BALANCE | exp_Final.RESTOR_AL_BALANCE → exp_Init.RESTOR_AL_BALANCE → SQ_CPM_NEWPAY_TBL.RESTOR_AL_BALANCE → CPM_NEWPAY_TBL.RESTOR_AL_BALANCE | CPM_NEWPAY_TBL.RESTOR_AL_BALANCE |
| nihtest_NIH_PAYROLL_MASTER | RESTOR_AL_BAL_1 | exp_Final.RESTOR_AL_BAL_1 → exp_Init.RESTOR_AL_BAL_1 → SQ_CPM_NEWPAY_TBL.RESTOR_AL_BAL_1 → CPM_NEWPAY_TBL.RESTOR_AL_BAL_1 | CPM_NEWPAY_TBL.RESTOR_AL_BAL_1 |
| nihtest_NIH_PAYROLL_MASTER | RESTOR_AL_BAL_2 | exp_Final.RESTOR_AL_BAL_2 → exp_Init.RESTOR_AL_BAL_2 → SQ_CPM_NEWPAY_TBL.RESTOR_AL_BAL_2 → CPM_NEWPAY_TBL.RESTOR_AL_BAL_2 | CPM_NEWPAY_TBL.RESTOR_AL_BAL_2 |
| nihtest_NIH_PAYROLL_MASTER | RESTOR_AL_BAL_3 | exp_Final.RESTOR_AL_BAL_3 → exp_Init.RESTOR_AL_BAL_3 → SQ_CPM_NEWPAY_TBL.RESTOR_AL_BAL_3 → CPM_NEWPAY_TBL.RESTOR_AL_BAL_3 | CPM_NEWPAY_TBL.RESTOR_AL_BAL_3 |
| nihtest_NIH_PAYROLL_MASTER | RESTOR_AL_PAID_CPP | exp_Final.RESTOR_AL_PAID_CPP → exp_Init.RESTOR_AL_PAID_CPP → SQ_CPM_NEWPAY_TBL.RESTOR_AL_PAID_CPP → CPM_NEWPAY_TBL.RESTOR_AL_PAID_CPP | CPM_NEWPAY_TBL.RESTOR_AL_PAID_CPP |
| nihtest_NIH_PAYROLL_MASTER | RESTOR_AL_PAID_ADJ | exp_Final.RESTOR_AL_PAID_ADJ → exp_Init.RESTOR_AL_PAID_ADJ → SQ_CPM_NEWPAY_TBL.RESTOR_AL_PAID_ADJ → CPM_NEWPAY_TBL.RESTOR_AL_PAID_ADJ | CPM_NEWPAY_TBL.RESTOR_AL_PAID_ADJ |
| nihtest_NIH_PAYROLL_MASTER | CPP_LUMPSUM_LVPY | exp_Final.CPP_LUMPSUM_LVPY → exp_Init.CPP_LUMPSUM_LVPY → SQ_CPM_NEWPAY_TBL.CPP_LUMPSUM_LVPY → CPM_NEWPAY_TBL.CPP_LUMPSUM_LVPY | CPM_NEWPAY_TBL.CPP_LUMPSUM_LVPY |
| nihtest_NIH_PAYROLL_MASTER | YTD_LSL_PAY | exp_Final.YTD_LSL_PAY → exp_Init.YTD_LSL_PAY → SQ_CPM_NEWPAY_TBL.YTD_LSL_PAY → CPM_NEWPAY_TBL.YTD_LSL_PAY | CPM_NEWPAY_TBL.YTD_LSL_PAY |
| nihtest_NIH_PAYROLL_MASTER | ADJ_LUMP_SUM | exp_Final.ADJ_LUMP_SUM → exp_Init.ADJ_LUMP_SUM → SQ_CPM_NEWPAY_TBL.ADJ_LUMP_SUM → CPM_NEWPAY_TBL.ADJ_LUMP_SUM | CPM_NEWPAY_TBL.ADJ_LUMP_SUM |
| nihtest_NIH_PAYROLL_MASTER | CPP_RECRUIT | exp_Final.CPP_RECRUIT → exp_Init.CPP_RECRUIT → SQ_CPM_NEWPAY_TBL.CPP_RECRUIT → CPM_NEWPAY_TBL.CPP_RECRUIT | CPM_NEWPAY_TBL.CPP_RECRUIT |
| nihtest_NIH_PAYROLL_MASTER | YTD_RECRUIT | exp_Final.YTD_RECRUIT → exp_Init.YTD_RECRUIT → SQ_CPM_NEWPAY_TBL.YTD_RECRUIT → CPM_NEWPAY_TBL.YTD_RECRUIT | CPM_NEWPAY_TBL.YTD_RECRUIT |
| nihtest_NIH_PAYROLL_MASTER | ADJ_RECRUIT | exp_Final.ADJ_RECRUIT → exp_Init.ADJ_RECRUIT → SQ_CPM_NEWPAY_TBL.ADJ_RECRUIT → CPM_NEWPAY_TBL.ADJ_RECRUIT | CPM_NEWPAY_TBL.ADJ_RECRUIT |
| nihtest_NIH_PAYROLL_MASTER | CPP_RELOC | exp_Final.CPP_RELOC → exp_Init.CPP_RELOC → SQ_CPM_NEWPAY_TBL.CPP_RELOC → CPM_NEWPAY_TBL.CPP_RELOC | CPM_NEWPAY_TBL.CPP_RELOC |
| nihtest_NIH_PAYROLL_MASTER | YTD_RELOC | exp_Final.YTD_RELOC → exp_Init.YTD_RELOC → SQ_CPM_NEWPAY_TBL.YTD_RELOC → CPM_NEWPAY_TBL.YTD_RELOC | CPM_NEWPAY_TBL.YTD_RELOC |
| nihtest_NIH_PAYROLL_MASTER | ADJ_RELOC | exp_Final.ADJ_RELOC → exp_Init.ADJ_RELOC → SQ_CPM_NEWPAY_TBL.ADJ_RELOC → CPM_NEWPAY_TBL.ADJ_RELOC | CPM_NEWPAY_TBL.ADJ_RELOC |
| nihtest_NIH_PAYROLL_MASTER | CPP_RETENT | exp_Final.CPP_RETENT → exp_Init.CPP_RETENT → SQ_CPM_NEWPAY_TBL.CPP_RETENT → CPM_NEWPAY_TBL.CPP_RETENT | CPM_NEWPAY_TBL.CPP_RETENT |
| nihtest_NIH_PAYROLL_MASTER | YTD_RETENT | exp_Final.YTD_RETENT → exp_Init.YTD_RETENT → SQ_CPM_NEWPAY_TBL.YTD_RETENT → CPM_NEWPAY_TBL.YTD_RETENT | CPM_NEWPAY_TBL.YTD_RETENT |
| nihtest_NIH_PAYROLL_MASTER | ADJ_RETENT | exp_Final.ADJ_RETENT → exp_Init.ADJ_RETENT → SQ_CPM_NEWPAY_TBL.ADJ_RETENT → CPM_NEWPAY_TBL.ADJ_RETENT | CPM_NEWPAY_TBL.ADJ_RETENT |
| nihtest_NIH_PAYROLL_MASTER | CPP_TEA_EMP_DED | exp_Final.CPP_TEA_EMP_DED → exp_Init.CPP_TEA_EMP_DED → SQ_CPM_NEWPAY_TBL.CPP_TEA_EMP_DED → CPM_NEWPAY_TBL.CPP_TEA_EMP_DED | CPM_NEWPAY_TBL.CPP_TEA_EMP_DED |
| nihtest_NIH_PAYROLL_MASTER | YTD_TEA_EMP_DED | exp_Final.YTD_TEA_EMP_DED → exp_Init.YTD_TEA_EMP_DED → SQ_CPM_NEWPAY_TBL.YTD_TEA_EMP_DED → CPM_NEWPAY_TBL.YTD_TEA_EMP_DED | CPM_NEWPAY_TBL.YTD_TEA_EMP_DED |
| nihtest_NIH_PAYROLL_MASTER | ADJ_TEA_EMP_DED | exp_Final.ADJ_TEA_EMP_DED → exp_Init.ADJ_TEA_EMP_DED → SQ_CPM_NEWPAY_TBL.ADJ_TEA_EMP_DED → CPM_NEWPAY_TBL.ADJ_TEA_EMP_DED | CPM_NEWPAY_TBL.ADJ_TEA_EMP_DED |
| nihtest_NIH_PAYROLL_MASTER | CPP_TEA_GVT_TV_CONT | exp_Final.CPP_TEA_GVT_TV_CONT → exp_Init.CPP_TEA_GVT_TV_CONT → SQ_CPM_NEWPAY_TBL.CPP_TEA_GVT_TV_CONT → CPM_NEWPAY_TBL.CPP_TEA_GVT_TV_CONT | CPM_NEWPAY_TBL.CPP_TEA_GVT_TV_CONT |
| nihtest_NIH_PAYROLL_MASTER | ADJ_TEA_GVT_TV_CONT | exp_Final.ADJ_TEA_GVT_TV_CONT → exp_Init.ADJ_TEA_GVT_TV_CONT → SQ_CPM_NEWPAY_TBL.ADJ_TEA_GVT_TV_CONT → CPM_NEWPAY_TBL.ADJ_TEA_GVT_TV_CONT | CPM_NEWPAY_TBL.ADJ_TEA_GVT_TV_CONT |
| nihtest_NIH_PAYROLL_MASTER | CPP_TEA_GVT_PK_CONT | exp_Final.CPP_TEA_GVT_PK_CONT → exp_Init.CPP_TEA_GVT_PK_CONT → SQ_CPM_NEWPAY_TBL.CPP_TEA_GVT_PK_CONT → CPM_NEWPAY_TBL.CPP_TEA_GVT_PK_CONT | CPM_NEWPAY_TBL.CPP_TEA_GVT_PK_CONT |
| nihtest_NIH_PAYROLL_MASTER | FEHB_PC_PRE_TAX_YTD | exp_Final.FEHB_PC_PRE_TAX_YTD → exp_Init.FEHB_PC_PRE_TAX_YTD → SQ_CPM_NEWPAY_TBL.FEHB_PC_PRE_TAX_YTD → CPM_NEWPAY_TBL.FEHB_PC_PRE_TAX_YTD | CPM_NEWPAY_TBL.FEHB_PC_PRE_TAX_YTD |
| nihtest_NIH_PAYROLL_MASTER | YTD_CHILD_SUB | exp_Final.YTD_CHILD_SUB → exp_Init.YTD_CHILD_SUB → SQ_CPM_NEWPAY_TBL.YTD_CHILD_SUB → CPM_NEWPAY_TBL.YTD_CHILD_SUB | CPM_NEWPAY_TBL.YTD_CHILD_SUB |
| nihtest_NIH_PAYROLL_MASTER | SUSP_HRS_CPP | exp_Final.SUSP_HRS_CPP → exp_Init.SUSP_HRS_CPP → SQ_CPM_NEWPAY_TBL.SUSP_HRS_CPP → CPM_NEWPAY_TBL.SUSP_HRS_CPP | CPM_NEWPAY_TBL.SUSP_HRS_CPP |
| nihtest_NIH_PAYROLL_MASTER | FURLO_HRS_CPP | exp_Final.FURLO_HRS_CPP → exp_Init.FURLO_HRS_CPP → SQ_CPM_NEWPAY_TBL.FURLO_HRS_CPP → CPM_NEWPAY_TBL.FURLO_HRS_CPP | CPM_NEWPAY_TBL.FURLO_HRS_CPP |
| nihtest_NIH_PAYROLL_MASTER | REL_COMP_ERND_CPP | exp_Final.REL_COMP_ERND_CPP → exp_Init.REL_COMP_ERND_CPP → SQ_CPM_NEWPAY_TBL.REL_COMP_ERND_CPP → CPM_NEWPAY_TBL.REL_COMP_ERND_CPP | CPM_NEWPAY_TBL.REL_COMP_ERND_CPP |
| nihtest_NIH_PAYROLL_MASTER | REL_COMP_USED_CPP | exp_Final.REL_COMP_USED_CPP → exp_Init.REL_COMP_USED_CPP → SQ_CPM_NEWPAY_TBL.REL_COMP_USED_CPP → CPM_NEWPAY_TBL.REL_COMP_USED_CPP | CPM_NEWPAY_TBL.REL_COMP_USED_CPP |
| nihtest_NIH_PAYROLL_MASTER | REL_COMP_CURR_BAL | exp_Final.REL_COMP_CURR_BAL → exp_Init.REL_COMP_CURR_BAL → SQ_CPM_NEWPAY_TBL.REL_COMP_CURR_BAL → CPM_NEWPAY_TBL.REL_COMP_CURR_BAL | CPM_NEWPAY_TBL.REL_COMP_CURR_BAL |
| nihtest_NIH_PAYROLL_MASTER | REL_COMP_LS_PAY_CPP | exp_Final.REL_COMP_LS_PAY_CPP → exp_Init.REL_COMP_LS_PAY_CPP → SQ_CPM_NEWPAY_TBL.REL_COMP_LS_PAY_CPP → CPM_NEWPAY_TBL.REL_COMP_LS_PAY_CPP | CPM_NEWPAY_TBL.REL_COMP_LS_PAY_CPP |
| nihtest_NIH_PAYROLL_MASTER | REL_COMP_LS_PAY_YTD | exp_Final.REL_COMP_LS_PAY_YTD → exp_Init.REL_COMP_LS_PAY_YTD → SQ_CPM_NEWPAY_TBL.REL_COMP_LS_PAY_YTD → CPM_NEWPAY_TBL.REL_COMP_LS_PAY_YTD | CPM_NEWPAY_TBL.REL_COMP_LS_PAY_YTD |
| nihtest_NIH_PAYROLL_MASTER | REL_COMP_LS_PAY_ADJ | exp_Final.REL_COMP_LS_PAY_ADJ → exp_Init.REL_COMP_LS_PAY_ADJ → SQ_CPM_NEWPAY_TBL.REL_COMP_LS_PAY_ADJ → CPM_NEWPAY_TBL.REL_COMP_LS_PAY_ADJ | CPM_NEWPAY_TBL.REL_COMP_LS_PAY_ADJ |
| nihtest_NIH_PAYROLL_MASTER | REL_COMP_LS_HRS | exp_Final.REL_COMP_LS_HRS → exp_Init.REL_COMP_LS_HRS → SQ_CPM_NEWPAY_TBL.REL_COMP_LS_HRS → CPM_NEWPAY_TBL.REL_COMP_LS_HRS | CPM_NEWPAY_TBL.REL_COMP_LS_HRS |
| nihtest_NIH_PAYROLL_MASTER | CR_HRS_ERND_CPP | exp_Final.CR_HRS_ERND_CPP → exp_Init.CR_HRS_ERND_CPP → SQ_CPM_NEWPAY_TBL.CR_HRS_ERND_CPP → CPM_NEWPAY_TBL.CR_HRS_ERND_CPP | CPM_NEWPAY_TBL.CR_HRS_ERND_CPP |
| nihtest_NIH_PAYROLL_MASTER | CR_HRS_USED_CPP | exp_Final.CR_HRS_USED_CPP → exp_Init.CR_HRS_USED_CPP → SQ_CPM_NEWPAY_TBL.CR_HRS_USED_CPP → CPM_NEWPAY_TBL.CR_HRS_USED_CPP | CPM_NEWPAY_TBL.CR_HRS_USED_CPP |
| nihtest_NIH_PAYROLL_MASTER | CR_HRS_CUR_BAL | exp_Final.CR_HRS_CUR_BAL → exp_Init.CR_HRS_CUR_BAL → SQ_CPM_NEWPAY_TBL.CR_HRS_CUR_BAL → CPM_NEWPAY_TBL.CR_HRS_CUR_BAL | CPM_NEWPAY_TBL.CR_HRS_CUR_BAL |
| nihtest_NIH_PAYROLL_MASTER | CR_HRS_LS_PAY_CPP | exp_Final.CR_HRS_LS_PAY_CPP → exp_Init.CR_HRS_LS_PAY_CPP → SQ_CPM_NEWPAY_TBL.CR_HRS_LS_PAY_CPP → CPM_NEWPAY_TBL.CR_HRS_LS_PAY_CPP | CPM_NEWPAY_TBL.CR_HRS_LS_PAY_CPP |
| nihtest_NIH_PAYROLL_MASTER | CR_HRS_LS_PAY_YTD | exp_Final.CR_HRS_LS_PAY_YTD → exp_Init.CR_HRS_LS_PAY_YTD → SQ_CPM_NEWPAY_TBL.CR_HRS_LS_PAY_YTD → CPM_NEWPAY_TBL.CR_HRS_LS_PAY_YTD | CPM_NEWPAY_TBL.CR_HRS_LS_PAY_YTD |
| nihtest_NIH_PAYROLL_MASTER | CR_HRS_LS_PAY_ADJ | exp_Final.CR_HRS_LS_PAY_ADJ → exp_Init.CR_HRS_LS_PAY_ADJ → SQ_CPM_NEWPAY_TBL.CR_HRS_LS_PAY_ADJ → CPM_NEWPAY_TBL.CR_HRS_LS_PAY_ADJ | CPM_NEWPAY_TBL.CR_HRS_LS_PAY_ADJ |
| nihtest_NIH_PAYROLL_MASTER | CR_HRS_LS_HRS | exp_Final.CR_HRS_LS_HRS → exp_Init.CR_HRS_LS_HRS → SQ_CPM_NEWPAY_TBL.CR_HRS_LS_HRS → CPM_NEWPAY_TBL.CR_HRS_LS_HRS | CPM_NEWPAY_TBL.CR_HRS_LS_HRS |
| nihtest_NIH_PAYROLL_MASTER | YTD_PREPD_HB | exp_Final.YTD_PREPD_HB → exp_Init.YTD_PREPD_HB → SQ_CPM_NEWPAY_TBL.YTD_PREPD_HB → CPM_NEWPAY_TBL.YTD_PREPD_HB | CPM_NEWPAY_TBL.YTD_PREPD_HB |
| nihtest_NIH_PAYROLL_MASTER | CPP_LTC_DED | exp_Final.CPP_LTC_DED → exp_Init.CPP_LTC_DED → SQ_CPM_NEWPAY_TBL.CPP_LTC_DED → CPM_NEWPAY_TBL.CPP_LTC_DED | CPM_NEWPAY_TBL.CPP_LTC_DED |
| nihtest_NIH_PAYROLL_MASTER | YTD_LTC_DED | exp_Final.YTD_LTC_DED → exp_Init.YTD_LTC_DED → SQ_CPM_NEWPAY_TBL.YTD_LTC_DED → CPM_NEWPAY_TBL.YTD_LTC_DED | CPM_NEWPAY_TBL.YTD_LTC_DED |
| nihtest_NIH_PAYROLL_MASTER | ADJ_LTC_DED | exp_Final.ADJ_LTC_DED → exp_Init.ADJ_LTC_DED → SQ_CPM_NEWPAY_TBL.ADJ_LTC_DED → CPM_NEWPAY_TBL.ADJ_LTC_DED | CPM_NEWPAY_TBL.ADJ_LTC_DED |
| nihtest_NIH_PAYROLL_MASTER | CPP_FSAHC_DED | exp_Final.CPP_FSAHC_DED → exp_Init.CPP_FSAHC_DED → SQ_CPM_NEWPAY_TBL.CPP_FSAHC_DED → CPM_NEWPAY_TBL.CPP_FSAHC_DED | CPM_NEWPAY_TBL.CPP_FSAHC_DED |
| nihtest_NIH_PAYROLL_MASTER | YTD_FSAHC_DED | exp_Final.YTD_FSAHC_DED → exp_Init.YTD_FSAHC_DED → SQ_CPM_NEWPAY_TBL.YTD_FSAHC_DED → CPM_NEWPAY_TBL.YTD_FSAHC_DED | CPM_NEWPAY_TBL.YTD_FSAHC_DED |
| nihtest_NIH_PAYROLL_MASTER | ADJ_FSAHC_DED | exp_Final.ADJ_FSAHC_DED → exp_Init.ADJ_FSAHC_DED → SQ_CPM_NEWPAY_TBL.ADJ_FSAHC_DED → CPM_NEWPAY_TBL.ADJ_FSAHC_DED | CPM_NEWPAY_TBL.ADJ_FSAHC_DED |
| nihtest_NIH_PAYROLL_MASTER | CPP_FSADC_DED | exp_Final.CPP_FSADC_DED → exp_Init.CPP_FSADC_DED → SQ_CPM_NEWPAY_TBL.CPP_FSADC_DED → CPM_NEWPAY_TBL.CPP_FSADC_DED | CPM_NEWPAY_TBL.CPP_FSADC_DED |
| nihtest_NIH_PAYROLL_MASTER | YTD_FSADC_DED | exp_Final.YTD_FSADC_DED → exp_Init.YTD_FSADC_DED → SQ_CPM_NEWPAY_TBL.YTD_FSADC_DED → CPM_NEWPAY_TBL.YTD_FSADC_DED | CPM_NEWPAY_TBL.YTD_FSADC_DED |
| nihtest_NIH_PAYROLL_MASTER | ADJ_FSADC_DED | exp_Final.ADJ_FSADC_DED → exp_Init.ADJ_FSADC_DED → SQ_CPM_NEWPAY_TBL.ADJ_FSADC_DED → CPM_NEWPAY_TBL.ADJ_FSADC_DED | CPM_NEWPAY_TBL.ADJ_FSADC_DED |
| nihtest_NIH_PAYROLL_MASTER | CPP_TSP_OVER50 | exp_Final.CPP_TSP_OVER50 → exp_Init.CPP_TSP_OVER50 → SQ_CPM_NEWPAY_TBL.CPP_TSP_OVER50 → CPM_NEWPAY_TBL.CPP_TSP_OVER50 | CPM_NEWPAY_TBL.CPP_TSP_OVER50 |
| nihtest_NIH_PAYROLL_MASTER | ADJ_TSP_OVER50 | exp_Final.ADJ_TSP_OVER50 → exp_Init.ADJ_TSP_OVER50 → SQ_CPM_NEWPAY_TBL.ADJ_TSP_OVER50 → CPM_NEWPAY_TBL.ADJ_TSP_OVER50 | CPM_NEWPAY_TBL.ADJ_TSP_OVER50 |
| nihtest_NIH_PAYROLL_MASTER | YTD_TSP_OVER50 | exp_Final.YTD_TSP_OVER50 → exp_Init.YTD_TSP_OVER50 → SQ_CPM_NEWPAY_TBL.YTD_TSP_OVER50 → CPM_NEWPAY_TBL.YTD_TSP_OVER50 | CPM_NEWPAY_TBL.YTD_TSP_OVER50 |
| nihtest_NIH_PAYROLL_MASTER | CPP_ALT_5_DED | exp_Final.CPP_ALT_5_DED → exp_Init.CPP_ALT_5_DED → SQ_CPM_NEWPAY_TBL.CPP_ALT_5_DED → CPM_NEWPAY_TBL.CPP_ALT_5_DED | CPM_NEWPAY_TBL.CPP_ALT_5_DED |
| nihtest_NIH_PAYROLL_MASTER | CPP_ALT_6_DED | exp_Final.CPP_ALT_6_DED → exp_Init.CPP_ALT_6_DED → SQ_CPM_NEWPAY_TBL.CPP_ALT_6_DED → CPM_NEWPAY_TBL.CPP_ALT_6_DED | CPM_NEWPAY_TBL.CPP_ALT_6_DED |
| nihtest_NIH_PAYROLL_MASTER | CPP_ALT_7_DED | exp_Final.CPP_ALT_7_DED → exp_Init.CPP_ALT_7_DED → SQ_CPM_NEWPAY_TBL.CPP_ALT_7_DED → CPM_NEWPAY_TBL.CPP_ALT_7_DED | CPM_NEWPAY_TBL.CPP_ALT_7_DED |
| nihtest_NIH_PAYROLL_MASTER | CPP_ALT_8_DED | exp_Final.CPP_ALT_8_DED → exp_Init.CPP_ALT_8_DED → SQ_CPM_NEWPAY_TBL.CPP_ALT_8_DED → CPM_NEWPAY_TBL.CPP_ALT_8_DED | CPM_NEWPAY_TBL.CPP_ALT_8_DED |
| nihtest_NIH_PAYROLL_MASTER | TVL_COMP_BEGIN_BAL | exp_Final.TVL_COMP_BEGIN_BAL → exp_Init.TVL_COMP_BEGIN_BAL → SQ_CPM_NEWPAY_TBL.TVL_COMP_BEGIN_BAL → CPM_NEWPAY_TBL.TVL_COMP_BEGIN_BAL | CPM_NEWPAY_TBL.TVL_COMP_BEGIN_BAL |
| nihtest_NIH_PAYROLL_MASTER | TVL_COMP_END_BAL | exp_Final.TVL_COMP_END_BAL → exp_Init.TVL_COMP_END_BAL → SQ_CPM_NEWPAY_TBL.TVL_COMP_END_BAL → CPM_NEWPAY_TBL.TVL_COMP_END_BAL | CPM_NEWPAY_TBL.TVL_COMP_END_BAL |
| nihtest_NIH_PAYROLL_MASTER | TVL_COMP_USED_YTD | exp_Final.TVL_COMP_USED_YTD → exp_Init.TVL_COMP_USED_YTD → SQ_CPM_NEWPAY_TBL.TVL_COMP_USED_YTD → CPM_NEWPAY_TBL.TVL_COMP_USED_YTD | CPM_NEWPAY_TBL.TVL_COMP_USED_YTD |
| nihtest_NIH_PAYROLL_MASTER | TVL_COMP_FORFEITED | exp_Final.TVL_COMP_FORFEITED → exp_Init.TVL_COMP_FORFEITED → SQ_CPM_NEWPAY_TBL.TVL_COMP_FORFEITED → CPM_NEWPAY_TBL.TVL_COMP_FORFEITED | CPM_NEWPAY_TBL.TVL_COMP_FORFEITED |
| nihtest_NIH_PAYROLL_MASTER | VIS_DENT_1_CPP | exp_Final.VIS_DENT_1_CPP → exp_Init.VIS_DENT_1_CPP → SQ_CPM_NEWPAY_TBL.VIS_DENT_1_CPP → CPM_NEWPAY_TBL.VIS_DENT_1_CPP | CPM_NEWPAY_TBL.VIS_DENT_1_CPP |
| nihtest_NIH_PAYROLL_MASTER | VIS_DENT_1_YTD | exp_Final.VIS_DENT_1_YTD → exp_Init.VIS_DENT_1_YTD → SQ_CPM_NEWPAY_TBL.VIS_DENT_1_YTD → CPM_NEWPAY_TBL.VIS_DENT_1_YTD | CPM_NEWPAY_TBL.VIS_DENT_1_YTD |
| nihtest_NIH_PAYROLL_MASTER | VIS_DENT_2_CPP | exp_Final.VIS_DENT_2_CPP → exp_Init.VIS_DENT_2_CPP → SQ_CPM_NEWPAY_TBL.VIS_DENT_2_CPP → CPM_NEWPAY_TBL.VIS_DENT_2_CPP | CPM_NEWPAY_TBL.VIS_DENT_2_CPP |
| nihtest_NIH_PAYROLL_MASTER | VIS_DENT_2_YTD | exp_Final.VIS_DENT_2_YTD → exp_Init.VIS_DENT_2_YTD → SQ_CPM_NEWPAY_TBL.VIS_DENT_2_YTD → CPM_NEWPAY_TBL.VIS_DENT_2_YTD | CPM_NEWPAY_TBL.VIS_DENT_2_YTD |
| nihtest_NIH_PAYROLL_MASTER | VIS_DENT_3_CPP | exp_Final.VIS_DENT_3_CPP → exp_Init.VIS_DENT_3_CPP → SQ_CPM_NEWPAY_TBL.VIS_DENT_3_CPP → CPM_NEWPAY_TBL.VIS_DENT_3_CPP | CPM_NEWPAY_TBL.VIS_DENT_3_CPP |
| nihtest_NIH_PAYROLL_MASTER | VIS_DENT_3_YTD | exp_Final.VIS_DENT_3_YTD → exp_Init.VIS_DENT_3_YTD → SQ_CPM_NEWPAY_TBL.VIS_DENT_3_YTD → CPM_NEWPAY_TBL.VIS_DENT_3_YTD | CPM_NEWPAY_TBL.VIS_DENT_3_YTD |
| nihtest_NIH_PAYROLL_MASTER | FED_RETIRE_1 | exp_Final.FED_RETIRE_1 → exp_Convert.o_FED_RETIRE_1 = SUBSTR(FED_RETIRE_CDE, 1, 1) → exp_Init.FED_RETIRE_CDE → SQ_CPM_NEWPAY_TBL.FED_RETIRE_CDE → CPM_NEWPAY_TBL.FED_RETIRE_CDE | CPM_NEWPAY_TBL.FED_RETIRE_CDE |
| nihtest_NIH_PAYROLL_MASTER | FED_RETIRE_2 | exp_Final.FED_RETIRE_2 → exp_Convert.o_FED_RETIRE_2 = SUBSTR(FED_RETIRE_CDE, 2, 1) → exp_Init.FED_RETIRE_CDE → SQ_CPM_NEWPAY_TBL.FED_RETIRE_CDE → CPM_NEWPAY_TBL.FED_RETIRE_CDE | CPM_NEWPAY_TBL.FED_RETIRE_CDE |

## Mapping `m_CPM_NIH_Concatenate_Files`

- Sessions: `s_CPM_NIH_Concatenate_Files` (#5)
- Sources: `HI_GENERIC_SRC_TBL`
- Target instances: `GENERIC_TARGET_FILE`

### Transformation `SQ_HI_GENERIC_SRC_TBL` (Source Qualifier)

- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`


### Target instance `GENERIC_TARGET_FILE` (table `GENERIC_TARGET_FILE`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| GENERIC_TARGET_FILE | ID | SQ_HI_GENERIC_SRC_TBL.ID → HI_GENERIC_SRC_TBL.ID | HI_GENERIC_SRC_TBL.ID |

## Mapping `m_CPM_NIH_Build_Message`

- Sessions: `s_CPM_NIH_Build_Message` (#6)
- Sources: `CPM_NEWPAY_TBL`
- Target instances: `CPM_NIH_MESSAGE_FILE`

### Transformation `SQ_CPM_NEWPAY_TBL` (Source Qualifier)

- **Source Filter**: `CPM_NEWPAY_TBL.PP_END_YEAR = TO_NUMBER('$$MAP_PP_END_YEAR') AND CPM_NEWPAY_TBL.PP_NUM = TO_NUMBER('$$MAP_PP_NUM') AND CPM_NEWPAY_TBL.MP_POOL_DES = ' ' AND CPM_NEWPAY_TBL.BUSINESS_UNIT = 'NIH00'`
- **Number Of Sorted Ports**: `3`
- **Select Distinct**: `NO`

### Transformation `agg_Count_CPM_NIH` (Aggregator)

- **Sorted Input**: `NO`

### Transformation `lkp_Pay_Period_Total` (Lookup Procedure)

- **Lookup Sql Override**: `SELECT COUNT(*) as COUNT_TOTAL FROM PAY_PERIOD WHERE PP_END_YEAR = TO_NUMBER('$$MAP_PP_END_YEAR') AND PP_NUM = TO_NUMBER('$$MAP_PP_NUM')`
- **Lookup table name**: `PAY_PERIOD`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `COUNT_TOTAL >= in_CONSTANT`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

- Lookup `lkp_Pay_Period_Total`: table `PAY_PERIOD` (exists in export: **True**), condition `COUNT_TOTAL >= in_CONSTANT`, multiple-match policy `Use Any Value`.

### Target instance `CPM_NIH_MESSAGE_FILE` (table `CPM_NIH_MESSAGE_FILE`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| CPM_NIH_MESSAGE_FILE | SUBJECT | exp_Final.SUBJECT → exp_Build_Message.o_SUBJECT = SETVARIABLE($$MAP_SUBJECT, v_SUBJECT) → exp_Build_Message.v_SUBJECT = v_ENVIRONMENT \|\| 'CPM NIH Process Completed Successfully for: ' \|\| TO_CHAR(PP_END_YEAR) \|\| '-' \|\| v_PP_NUM → exp_Build_Message.v_ENVIRONMENT = DECODE(SUBSTR($PMRepositoryServiceName, 1, 4), 'Dev_', 'Dev: ', 'Test', 'Test: ', 'Prod', 'Prod: ') → agg_Count_CPM_NIH.PP_END_YEAR → exp_Initial.PP_END_YEAR → SQ_CPM_NEWPAY_TBL.PP_END_YEAR → CPM_NEWPAY_TBL.PP_END_YEAR → exp_Build_Message.v_PP_NUM = IIF(PP_NUM < 10, LPAD(TO_CHAR(PP_NUM), 2, '0'), TO_CHAR(PP_NUM) ) → agg_Count_CPM_NIH.PP_NUM → exp_Initial.PP_NUM → SQ_CPM_NEWPAY_TBL.PP_NUM → CPM_NEWPAY_TBL.PP_NUM | CPM_NEWPAY_TBL.PP_END_YEAR; CPM_NEWPAY_TBL.PP_NUM; literal/expression: DECODE(SUBSTR($PMRepositoryServiceName, 1, 4), 'Dev_', 'Dev: ', 'Test', 'Test: ', 'Prod', 'Prod: ') |
| CPM_NIH_MESSAGE_FILE | MESSAGE | exp_Final.MESSAGE → exp_Build_Message.o_MESSAGE = SETVARIABLE($$MAP_MESSAGE, v_MESSAGE) → exp_Build_Message.v_MESSAGE = 'Total number of CPM NIH records loaded is: ' \|\| TO_CHAR(v_TOTAL_RECORDS) → exp_Build_Message.v_TOTAL_RECORDS = IIF(ISNULL(lkp_COUNT_HDR_TOTAL), CPM_NIH_TOTAL, CPM_NIH_TOTAL + lkp_COUNT_HDR_TOTAL) → lkp_Pay_Period_Total.COUNT_TOTAL [lookup PAY_PERIOD.COUNT_TOTAL ON COUNT_TOTAL >= in_CONSTANT] → agg_Count_CPM_NIH.o_CPM_NIH_TOTAL = COUNT(*) | PAY_PERIOD.COUNT_TOTAL (lookup); literal/expression: 1 (lookup key); literal/expression: COUNT(*) |

