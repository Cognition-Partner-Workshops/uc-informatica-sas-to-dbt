# PowerCenter STM: `CPM`

Derived deterministically from `legacy/informatica_ts/CPM_CDC` by `tools/ts_lineage.py`. Personal identifiers are redacted as `<owner>`, `<path>`, `<email>`.

| Mappings | Sessions | Sources | Targets | Transformations | Mapplets |
|---|---|---|---|---|---|
| 6 | 6 | 3 | 6 | 30 | 0 |

Transformations by type: Aggregator 1, Expression 17, Lookup Procedure 6, Source Qualifier 6

## Workflow `wf_CPM_CDC`

Session order:

1. `s_CPM_CDC_Set_CPM_Calendar` → mapping `m_CPM_CDC_Set_CPM_Calendar`
2. `s_CPM_CDC_Set_Pay_Calendar` → mapping `m_CPM_CDC_Set_Pay_Calendar`
3. `s_CPM_CDC_Load_CPM_CDC_Header_File` → mapping `m_CPM_CDC_Load_CPM_CDC_Header_File`
4. `s_CPM_CDC_Load_CPM_CDC_Data_File` → mapping `m_CPM_CDC_Load_CPM_CDC_Data_File`
5. `s_CPM_CDC_Concatenate_Files` → mapping `m_CPM_CDC_Concatenate_Files`
6. `s_CPM_CDC_Build_Message` → mapping `m_CPM_CDC_Build_Message`

| From | To | Condition |
|---|---|---|
| Start | s_CPM_CDC_Set_CPM_Calendar | — |
| s_CPM_CDC_Load_CPM_CDC_Header_File | s_CPM_CDC_Load_CPM_CDC_Data_File | $s_CPM_CDC_Load_CPM_CDC_Header_File.Status = Succeeded |
| s_CPM_CDC_Set_CPM_Calendar | s_CPM_CDC_Set_Pay_Calendar | $s_CPM_CDC_Set_CPM_Calendar.Status = Succeeded |
| s_CPM_CDC_Load_CPM_CDC_Data_File | s_CPM_CDC_Concatenate_Files | $s_CPM_CDC_Load_CPM_CDC_Data_File.Status = Succeeded |
| s_CPM_CDC_Build_Message | email_CPM_CDC | $s_CPM_CDC_Build_Message.Status = Succeeded |
| s_CPM_CDC_Set_Pay_Calendar | s_CPM_CDC_Load_CPM_CDC_Header_File | $s_CPM_CDC_Set_Pay_Calendar.Status = Succeeded |
| s_CPM_CDC_Concatenate_Files | s_CPM_CDC_Build_Message | $s_CPM_CDC_Concatenate_Files.Status = Succeeded |

Command tasks:

- `s_CPM_CDC_Set_CPM_Calendar` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`; `$$MAP_PP_YEAR_NUM` = `$$WF_PP_YEAR_NUM`
- `s_CPM_CDC_Set_CPM_Calendar` / Post-session success variable assignment `postsession_success_variable_assignment`: `$$WF_PP_END_YEAR` = `$$MAP_PP_END_YEAR`; `$$WF_PP_NUM` = `$$MAP_PP_NUM`; `$$WF_PP_YEAR_NUM` = `$$MAP_PP_YEAR_NUM`
- `s_CPM_CDC_Load_CPM_CDC_Data_File` / Pre-session command `pre_session_command`: `Command1` = `$Param_ControlDir/scripts/remove_file.sh $Param_Root_Directory/data/int/out/CPM $Param_CPM_CDC_DAT_filename`
- `s_CPM_CDC_Load_CPM_CDC_Data_File` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_CPM_CDC_Set_Pay_Calendar` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_CPM_CDC_Concatenate_Files` / Pre-session command `pre_session_command`: `Command1` = `$Param_ControlDir/scripts/remove_file.sh $Param_Root_Directory/data/int/out/CPM $Param_CPM_CDC_out_filename`
- `s_CPM_CDC_Concatenate_Files` / Post-session success command `post_session_success_command`: `Command1` = `cd $Param_Root_Directory/data/int/out/CPM; cat $Param_CPM_CDC_HDR_filename $Param_CPM_CDC_DAT_filename > $Param_CPM_CDC_out_filename`
- `s_CPM_CDC_Load_CPM_CDC_Header_File` / Pre-session command `pre_session_command`: `Command1` = `$Param_ControlDir/scripts/remove_file.sh $Param_Root_Directory/data/int/out/CPM $Param_CPM_CDC_HDR_filename`
- `s_CPM_CDC_Load_CPM_CDC_Header_File` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_CPM_CDC_Build_Message` / Post-session success command `post_session_success_command`: `Command1` = `cd $Param_Root_Directory/data/int/out/CPM; cp $Param_CPM_CDC_out_filename CDC.CPM.PP$$WF_PP_YEAR_NUM`; `Command2` = `<path>/scripts/cdc_transfer.sh CDC.CPM.PP$$WF_PP_YEAR_NUM`
- `s_CPM_CDC_Build_Message` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_SUBJECT` = `$$WF_SUBJECT`; `$$MAP_MESSAGE` = `$$WF_MESSAGE`; `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_CPM_CDC_Build_Message` / Post-session success variable assignment `postsession_success_variable_assignment`: `$$WF_SUBJECT` = `$$MAP_SUBJECT`; `$$WF_MESSAGE` = `$$MAP_MESSAGE`

- Session `s_CPM_CDC_Set_CPM_Calendar`: WRITER `CPM_CDC_CPM_PAY_PERIOD_FILE` Append if Exists=`NO`, Output Type=`File`, Output file directory=`$PMTargetFileDir\`, Output filename=`cpm_cdc_cpm_pay_period_file.txt`
- Session `s_CPM_CDC_Set_Pay_Calendar`: WRITER `CPM_CDC_PAY_PERIOD_FILE` Append if Exists=`NO`, Output Type=`File`, Output file directory=`$PMTargetFileDir\`, Output filename=`cpm_cdc_pay_period_file1.out`
- Session `s_CPM_CDC_Load_CPM_CDC_Header_File`: WRITER `cdchdr_WS_CDC_HDR` File Name Override=`$Param_Root_Directory/data/int/out/CPM/$Param_CPM_CDC_HDR_filename`
- Session `s_CPM_CDC_Load_CPM_CDC_Data_File`: WRITER `cdcskel_WS_PAY_OUT_REC` File Name Override=`$Param_Root_Directory/data/int/out/CPM/$Param_CPM_CDC_DAT_filename`
- Session `s_CPM_CDC_Concatenate_Files`: WRITER `GENERIC_TARGET_FILE` Append if Exists=`NO`, Output Type=`File`, Output file directory=`$PMTargetFileDir\`, Output filename=`generic_target_file.txt`
- Session `s_CPM_CDC_Build_Message`: WRITER `CPM_CDC_MESSAGE_FILE` Append if Exists=`NO`, Output Type=`File`, Output file directory=`$PMTargetFileDir\`, Output filename=`cpm_cdc_message_file.txt`

## Source definitions

| Source | Database type | Fields |
|---|---|---|
| CPM_NEWPAY_TBL | Oracle | 501 |
| HI_GENERIC_SRC_TBL | Oracle | 1 |
| PAY_PERIOD | Oracle | 10 |

## Target definitions

| Target | Database type | Fields |
|---|---|---|
| CPM_CDC_CPM_PAY_PERIOD_FILE | Flat File | 1 |
| CPM_CDC_MESSAGE_FILE | Flat File | 2 |
| CPM_CDC_PAY_PERIOD_FILE | Flat File | 1 |
| GENERIC_TARGET_FILE | Flat File | 1 |
| cdchdr_WS_CDC_HDR | PWX_SEQ_NRDB2 | 15 |
| cdcskel_WS_PAY_OUT_REC | PWX_SEQ_NRDB2 | 736 |

## Mapping `m_CPM_CDC_Set_CPM_Calendar`

- Sessions: `s_CPM_CDC_Set_CPM_Calendar` (#1)
- Sources: `PAY_PERIOD1`
- Target instances: `CPM_CDC_CPM_PAY_PERIOD_FILE`

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

### Target instance `CPM_CDC_CPM_PAY_PERIOD_FILE` (table `CPM_CDC_CPM_PAY_PERIOD_FILE`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| CPM_CDC_CPM_PAY_PERIOD_FILE | CPM_PAY_PERIOD | exp_Final.o_CPM_PAY_PERIOD = PARAM_PP_END_YEAR \|\| '-' \|\| LPAD(PARAM_PP_NUM, 2, '0') → exp_Validate_Parameters.PARAM_PP_END_YEAR → exp_Set_Parameters.o_PARAM_PP_END_YEAR = SETVARIABLE($$MAP_PP_END_YEAR, TO_CHAR(v_PP_END_YEAR)) → exp_Set_Parameters.v_PP_END_YEAR = DECODE(TRUE, v_DEFAULT_TO_CURR_PP_FLAG = TRUE, lkp_CURR_PP_END_YEAR, v_PAY_PERIOD_PARAM_EXISTS_FLAG = TRUE, PARAM_PP_END_YEAR ) --IIF(v_PAY_PERIOD_PARAM_EXISTS_FLAG = TRUE, -- TO_CHAR(PARAM_PP_END_YEAR), -- TO_CHAR(lkp_CURR_PP_END_YEAR)) → exp_Set_Parameters.v_DEFAULT_TO_CURR_PP_FLAG = DECODE(TRUE, (ISNULL(INIT_PARAM_PP_END_YEAR) OR IS_SPACES(INIT_PARAM_PP_END_YEAR) OR LENGTH(LTRIM(INIT_PARAM_PP_END_YEAR)) = 0) AND (ISNULL(INIT_PARAM_PP_NUM) OR IS_SPACES(INIT_PARAM_PP_NUM) OR LENGTH(LTRIM(INIT_PARAM_PP_NUM)) = 0), TRUE, FALSE) → exp_Initial.o_INIT_PARAM_PP_END_YEAR = $$MAP_PP_END_YEAR → exp_Initial.o_INIT_PARAM_PP_NUM = $$MAP_PP_NUM → lkp_Current_Pay_Period.PP_END_YEAR [lookup PAY_PERIOD.PP_END_YEAR ON CURR_PP_FLAG = in_CURR_PP_FLAG] → exp_Set_Parameters.v_PAY_PERIOD_PARAM_EXISTS_FLAG = IIF(NOT ISNULL(lkp_PP_NUM), TRUE, FALSE) → lkp_Existing_Pay_Period.PP_NUM [lookup PAY_PERIOD.PP_NUM ON PP_NUM = in_PARAM_PP_NUM AND PP_END_YEAR = in_PARAM_PP_END_YEAR] → exp_Initial.o_PARAM_PP_END_YEAR = v_PARAM_PP_END_YEAR → exp_Initial.v_PARAM_PP_END_YEAR = IIF(NOT IS_NUMBER($$MAP_PP_END_YEAR), 0, TO_DECIMAL($$MAP_PP_END_YEAR)) → exp_Validate_Parameters.PARAM_PP_NUM → exp_Set_Parameters.o_PARAM_PP_NUM = SETVARIABLE($$MAP_PP_NUM, TO_CHAR(v_PP_NUM)) → exp_Set_Parameters.v_PP_NUM = DECODE(TRUE, v_DEFAULT_TO_CURR_PP_FLAG = TRUE, lkp_CURR_PP_NUM, v_PAY_PERIOD_PARAM_EXISTS_FLAG = TRUE, PARAM_PP_NUM ) --IIF(v_PAY_PERIOD_PARAM_EXISTS_FLAG = TRUE, -- TO_CHAR(PARAM_PP_NUM), -- TO_CHAR(lkp_CURR_PP_NUM)) → lkp_Current_Pay_Period.PP_NUM [lookup PAY_PERIOD.PP_NUM ON CURR_PP_FLAG = in_CURR_PP_FLAG] → exp_Initial.o_PARAM_PP_NUM = v_PARAM_PP_NUM → exp_Initial.v_PARAM_PP_NUM = IIF(NOT IS_NUMBER($$MAP_PP_NUM), 0, TO_DECIMAL($$MAP_PP_NUM)) | PAY_PERIOD.PP_END_YEAR (lookup); PAY_PERIOD.PP_NUM (lookup); literal/expression: $$MAP_PP_END_YEAR; literal/expression: $$MAP_PP_NUM; literal/expression: 'Y' (lookup key); literal/expression: IIF(NOT IS_NUMBER($$MAP_PP_END_YEAR), 0, TO_DECIMAL($$MAP_PP_END_YEAR)); literal/expression: IIF(NOT IS_NUMBER($$MAP_PP_END_YEAR), 0, TO_DECIMAL($$MAP_PP_END_YEAR)) (lookup key); literal/expression: IIF(NOT IS_NUMBER($$MAP_PP_NUM), 0, TO_DECIMAL($$MAP_PP_NUM)); literal/expression: IIF(NOT IS_NUMBER($$MAP_PP_NUM), 0, TO_DECIMAL($$MAP_PP_NUM)) (lookup key) |

## Mapping `m_CPM_CDC_Set_Pay_Calendar`

- Sessions: `s_CPM_CDC_Set_Pay_Calendar` (#2)
- Sources: `PAY_PERIOD1`
- Target instances: `CPM_CDC_PAY_PERIOD_FILE`

### Transformation `SQ_PAY_PERIOD` (Source Qualifier)

- **Sql Query**: `SELECT MAX(PAY_PERIOD.PP_NUM) PP_NUM , MAX(PAY_PERIOD.PP_END_YEAR) PP_END_YEAR FROM PAY_PERIOD`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `lkp_CPM_NEWPAY_TBL` (Lookup Procedure)

- **Lookup table name**: `CPM_NEWPAY_TBL`
- **Lookup Source Filter**: `PP_END_YEAR = TO_NUMBER('$$MAP_PP_END_YEAR') AND PP_NUM = TO_NUMBER('$$MAP_PP_NUM') AND BUSINESS_UNIT = 'CDC00'`
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

### Target instance `CPM_CDC_PAY_PERIOD_FILE` (table `CPM_CDC_PAY_PERIOD_FILE`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| CPM_CDC_PAY_PERIOD_FILE | CPM_PAY_PERIOD | exp_Final.o_CPM_PAY_PERIOD = PARAM_PP_END_YEAR \|\| '-' \|\| LPAD(PARAM_PP_NUM, 2, '0') → exp_Validate_Parameters.PARAM_PP_END_YEAR → exp_Set_Parameters.o_PARAM_PP_END_YEAR = SETVARIABLE($$MAP_PP_END_YEAR, TO_CHAR(v_PP_END_YEAR)) → exp_Set_Parameters.v_PP_END_YEAR = DECODE(TRUE, v_DEFAULT_TO_CURR_PP_FLAG = TRUE, lkp_CURR_PP_END_YEAR, v_PAY_PERIOD_PARAM_EXISTS_FLAG = TRUE, PARAM_PP_END_YEAR ) --IIF(v_PAY_PERIOD_PARAM_EXISTS_FLAG = TRUE, -- TO_CHAR(PARAM_PP_END_YEAR), -- TO_CHAR(lkp_CURR_PP_END_YEAR)) → exp_Set_Parameters.v_DEFAULT_TO_CURR_PP_FLAG = DECODE(TRUE, (ISNULL(INIT_PARAM_PP_END_YEAR) OR IS_SPACES(INIT_PARAM_PP_END_YEAR) OR LENGTH(LTRIM(INIT_PARAM_PP_END_YEAR)) = 0) AND (ISNULL(INIT_PARAM_PP_NUM) OR IS_SPACES(INIT_PARAM_PP_NUM) OR LENGTH(LTRIM(INIT_PARAM_PP_NUM)) = 0), TRUE, FALSE) → exp_Initial.o_INIT_PARAM_PP_END_YEAR = $$MAP_PP_END_YEAR → exp_Initial.o_INIT_PARAM_PP_NUM = $$MAP_PP_NUM → lkp_Current_Pay_Period.PP_END_YEAR [lookup PAY_PERIOD.PP_END_YEAR ON CURR_PP_FLAG = in_CURR_PP_FLAG] → exp_Set_Parameters.v_PAY_PERIOD_PARAM_EXISTS_FLAG = IIF(NOT ISNULL(lkp_PP_NUM), TRUE, FALSE) → lkp_Existing_Pay_Period.PP_NUM [lookup PAY_PERIOD.PP_NUM ON PP_NUM = in_PARAM_PP_NUM AND PP_END_YEAR = in_PARAM_PP_END_YEAR] → exp_Initial.o_PARAM_PP_END_YEAR = v_PARAM_PP_END_YEAR → exp_Initial.v_PARAM_PP_END_YEAR = IIF(NOT IS_NUMBER($$MAP_PP_END_YEAR), 0, TO_DECIMAL($$MAP_PP_END_YEAR)) → exp_Validate_Parameters.PARAM_PP_NUM → exp_Set_Parameters.o_PARAM_PP_NUM = SETVARIABLE($$MAP_PP_NUM, TO_CHAR(v_PP_NUM)) → exp_Set_Parameters.v_PP_NUM = DECODE(TRUE, v_DEFAULT_TO_CURR_PP_FLAG = TRUE, lkp_CURR_PP_NUM, v_PAY_PERIOD_PARAM_EXISTS_FLAG = TRUE, PARAM_PP_NUM ) --IIF(v_PAY_PERIOD_PARAM_EXISTS_FLAG = TRUE, -- TO_CHAR(PARAM_PP_NUM), -- TO_CHAR(lkp_CURR_PP_NUM)) → lkp_Current_Pay_Period.PP_NUM [lookup PAY_PERIOD.PP_NUM ON CURR_PP_FLAG = in_CURR_PP_FLAG] → exp_Initial.o_PARAM_PP_NUM = v_PARAM_PP_NUM → exp_Initial.v_PARAM_PP_NUM = IIF(NOT IS_NUMBER($$MAP_PP_NUM), 0, TO_DECIMAL($$MAP_PP_NUM)) | PAY_PERIOD.PP_END_YEAR (lookup); PAY_PERIOD.PP_NUM (lookup); literal/expression: $$MAP_PP_END_YEAR; literal/expression: $$MAP_PP_NUM; literal/expression: 'Y' (lookup key); literal/expression: IIF(NOT IS_NUMBER($$MAP_PP_END_YEAR), 0, TO_DECIMAL($$MAP_PP_END_YEAR)); literal/expression: IIF(NOT IS_NUMBER($$MAP_PP_END_YEAR), 0, TO_DECIMAL($$MAP_PP_END_YEAR)) (lookup key); literal/expression: IIF(NOT IS_NUMBER($$MAP_PP_NUM), 0, TO_DECIMAL($$MAP_PP_NUM)); literal/expression: IIF(NOT IS_NUMBER($$MAP_PP_NUM), 0, TO_DECIMAL($$MAP_PP_NUM)) (lookup key) |

## Mapping `m_CPM_CDC_Load_CPM_CDC_Header_File`

- Sessions: `s_CPM_CDC_Load_CPM_CDC_Header_File` (#3)
- Sources: `PAY_PERIOD`
- Target instances: `cdchdr_WS_CDC_HDR`

### Transformation `SQ_PAY_PERIOD` (Source Qualifier)

- **Source Filter**: `PAY_PERIOD.PP_END_YEAR = TO_NUMBER('$$MAP_PP_END_YEAR') AND PAY_PERIOD.PP_NUM = TO_NUMBER('$$MAP_PP_NUM')`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`


### Target instance `cdchdr_WS_CDC_HDR` (table `cdchdr_WS_CDC_HDR`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| cdchdr_WS_CDC_HDR | HDR_FNAME | (not connected — NULL) | — |
| cdchdr_WS_CDC_HDR | HDR_LNAME | exp_Final.HDR_LNAME → exp_Initial.o_HDR_LNAME = 'REGULAR' | literal/expression: 'REGULAR' |
| cdchdr_WS_CDC_HDR | HDR_PP_NUMBER | exp_Final.HDR_PP_NUMBER → exp_Initial.o_HDR_PP_NUMBER = PP_NUM → SQ_PAY_PERIOD.PP_NUM → PAY_PERIOD.PP_NUM | PAY_PERIOD.PP_NUM |
| cdchdr_WS_CDC_HDR | HDR_LVII_NUMBER | exp_Final.HDR_LVII_NUMBER → exp_Initial.o_HDR_LVII_NUMBER = 14 | literal/expression: 14 |
| cdchdr_WS_CDC_HDR | LVIISITE_2 | exp_Final.LVIISITE_2 → exp_Initial.o_LVIISITE_2 = '21' | literal/expression: '21' |
| cdchdr_WS_CDC_HDR | LVIISITE_3 | exp_Final.LVIISITE_3 → exp_Initial.o_LVIISITE_3 = '24' | literal/expression: '24' |
| cdchdr_WS_CDC_HDR | LVIISITE_4 | exp_Final.LVIISITE_4 → exp_Initial.o_LVIISITE_4 = '25' | literal/expression: '25' |
| cdchdr_WS_CDC_HDR | LVIISITE_5 | exp_Final.LVIISITE_5 → exp_Initial.o_LVIISITE_5 = '26' | literal/expression: '26' |
| cdchdr_WS_CDC_HDR | LVIISITE_6 | exp_Final.LVIISITE_6 → exp_Initial.o_LVIISITE_6 = '44' | literal/expression: '44' |
| cdchdr_WS_CDC_HDR | LVIISITE_7 | exp_Final.LVIISITE_7 → exp_Initial.o_LVIISITE_7 = '49' | literal/expression: '49' |
| cdchdr_WS_CDC_HDR | LVIISITE_8 | exp_Final.LVIISITE_8 → exp_Initial.o_LVIISITE_8 = '92' | literal/expression: '92' |
| cdchdr_WS_CDC_HDR | LVIISITE_9 | exp_Final.LVIISITE_9 → exp_Initial.o_LVIISITE_9 = ' ' | literal/expression: ' ' |
| cdchdr_WS_CDC_HDR | LVIISITE_10 | exp_Final.LVIISITE_10 → exp_Initial.o_LVIISITE_10 = ' ' | literal/expression: ' ' |
| cdchdr_WS_CDC_HDR | TAPE_NUMBER | exp_Final.TAPE_NUMBER → exp_Initial.o_TAPE_NUMBER = '1' | literal/expression: '1' |
| cdchdr_WS_CDC_HDR | FILLER_1 | (not connected — NULL) | — |

## Mapping `m_CPM_CDC_Load_CPM_CDC_Data_File`

- Sessions: `s_CPM_CDC_Load_CPM_CDC_Data_File` (#4)
- Sources: `CPM_NEWPAY_TBL`
- Target instances: `cdcskel_WS_PAY_OUT_REC`

### Transformation `SQ_CPM_NEWPAY_TBL` (Source Qualifier)

- **Source Filter**: `PP_END_YEAR = TO_NUMBER('$$MAP_PP_END_YEAR') AND PP_NUM = TO_NUMBER('$$MAP_PP_NUM') AND MP_POOL_DES = ' ' AND ( BUSINESS_UNIT IN ('CDC00', 'ATSDR') OR trim(ORG_CDE) in ('ANC34', 'ANC341', 'ANC342', 'ANC343', 'ANC344', 'ANC345') )`
- **Number Of Sorted Ports**: `3`
- **Select Distinct**: `NO`


### Target instance `cdcskel_WS_PAY_OUT_REC` (table `cdcskel_WS_PAY_OUT_REC`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| cdcskel_WS_PAY_OUT_REC | FIR_NAME_1 | exp_Final.FIR_NAME_1 → exp_Convert.o_FIR_NAME_1 = FIR_NAME_1 → exp_Init.FIR_NAME_1 → SQ_CPM_NEWPAY_TBL.FIR_NAME_1 → CPM_NEWPAY_TBL.FIR_NAME_1 | CPM_NEWPAY_TBL.FIR_NAME_1 |
| cdcskel_WS_PAY_OUT_REC | CODE_CONSL | exp_Final.CODE_CONSL → exp_Convert.o_CODE_CONSL = CODE_CONSL → exp_Init.CODE_CONSL → SQ_CPM_NEWPAY_TBL.CODE_CONSL → CPM_NEWPAY_TBL.CODE_CONSL | CPM_NEWPAY_TBL.CODE_CONSL |
| cdcskel_WS_PAY_OUT_REC | FILLER_1 | exp_Final.FILLER_1 → exp_Convert.o_FILLER_1 = FIR_NAME_3_11 → exp_Init.FIR_NAME_3_11 → SQ_CPM_NEWPAY_TBL.FIR_NAME_3_11 → CPM_NEWPAY_TBL.FIR_NAME_3_11 | CPM_NEWPAY_TBL.FIR_NAME_3_11 |
| cdcskel_WS_PAY_OUT_REC | MID_INIT | exp_Final.MID_INIT → exp_Convert.o_MID_INIT = MID_INIT → exp_Init.MID_INIT → SQ_CPM_NEWPAY_TBL.MID_INIT → CPM_NEWPAY_TBL.MID_INIT | CPM_NEWPAY_TBL.MID_INIT |
| cdcskel_WS_PAY_OUT_REC | SURNAME_3 | exp_Final.SURNAME_3 → exp_Convert.o_SURNAME_3 = SURNAME_3 → exp_Init.SURNAME_3 → SQ_CPM_NEWPAY_TBL.SURNAME_3 → CPM_NEWPAY_TBL.SURNAME_3 | CPM_NEWPAY_TBL.SURNAME_3 |
| cdcskel_WS_PAY_OUT_REC | SURNAME_OTHER | exp_Final.SURNAME_OTHER → exp_Convert.o_SURNAME_OTHER = SURNAME_OTHER → exp_Init.SURNAME_OTHER → SQ_CPM_NEWPAY_TBL.SURNAME_OTHER → CPM_NEWPAY_TBL.SURNAME_OTHER | CPM_NEWPAY_TBL.SURNAME_OTHER |
| cdcskel_WS_PAY_OUT_REC | SOC_SEC_NO | exp_Final.SOC_SEC_NO → exp_Convert.o_SOC_SEC_NO = SOC_SEC_NO --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(SOC_SEC_NO, 0)), '.', NULL) ,11, '0') → exp_Init.SOC_SEC_NO → SQ_CPM_NEWPAY_TBL.SOC_SEC_NO → CPM_NEWPAY_TBL.SOC_SEC_NO | CPM_NEWPAY_TBL.SOC_SEC_NO |
| cdcskel_WS_PAY_OUT_REC | NOTHING | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | OCCUP_CDE | exp_Final.OCCUP_CDE → exp_Convert.o_OCCUP_CDE = OCCUP_CDE --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(OCCUP_CDE, 0)),'.', NULL) ,5, '0') → exp_Init.OCCUP_CDE → SQ_CPM_NEWPAY_TBL.OCCUP_CDE → CPM_NEWPAY_TBL.OCCUP_CDE | CPM_NEWPAY_TBL.OCCUP_CDE |
| cdcskel_WS_PAY_OUT_REC | JOB_LOC_CDE | exp_Final.JOB_LOC_CDE → exp_Convert.o_JOB_LOC_CDE = ST_CONT_LOC \|\| CITY_LOC \|\| CTY_CTRY_LOC → exp_Init.ST_CONT_LOC → SQ_CPM_NEWPAY_TBL.ST_CONT_LOC → CPM_NEWPAY_TBL.ST_CONT_LOC → exp_Init.CITY_LOC → SQ_CPM_NEWPAY_TBL.CITY_LOC → CPM_NEWPAY_TBL.CITY_LOC → exp_Init.CTY_CTRY_LOC → SQ_CPM_NEWPAY_TBL.CTY_CTRY_LOC → CPM_NEWPAY_TBL.CTY_CTRY_LOC | CPM_NEWPAY_TBL.CITY_LOC; CPM_NEWPAY_TBL.CTY_CTRY_LOC; CPM_NEWPAY_TBL.ST_CONT_LOC |
| cdcskel_WS_PAY_OUT_REC | TK_NO | exp_Final.TK_NO → exp_Convert.o_TK_NO = TK_NO --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(TK_NO, 0)),'.', NULL) ,5, '0') → exp_Init.TK_NO → SQ_CPM_NEWPAY_TBL.TK_NO → CPM_NEWPAY_TBL.TK_NO | CPM_NEWPAY_TBL.TK_NO |
| cdcskel_WS_PAY_OUT_REC | CAN | exp_Final.CAN → exp_Convert.o_CAN = CAN_FY \|\| CAN_AGCY \|\| CAN_AP \|\| CAN_AGCY_ACCT_CDE → exp_Init.CAN_FY → SQ_CPM_NEWPAY_TBL.CAN_FY → CPM_NEWPAY_TBL.CAN_FY → exp_Init.CAN_AGCY → SQ_CPM_NEWPAY_TBL.CAN_AGCY → CPM_NEWPAY_TBL.CAN_AGCY → exp_Init.CAN_AP → SQ_CPM_NEWPAY_TBL.CAN_AP → CPM_NEWPAY_TBL.CAN_AP → exp_Init.CAN_AGCY_ACCT_CDE → SQ_CPM_NEWPAY_TBL.CAN_AGCY_ACCT_CDE → CPM_NEWPAY_TBL.CAN_AGCY_ACCT_CDE | CPM_NEWPAY_TBL.CAN_AGCY; CPM_NEWPAY_TBL.CAN_AGCY_ACCT_CDE; CPM_NEWPAY_TBL.CAN_AP; CPM_NEWPAY_TBL.CAN_FY |
| cdcskel_WS_PAY_OUT_REC | ORG_CDE | exp_Final.ORG_CDE → exp_Convert.o_ORG_CDE = ORG_P01 \|\| ORG_P2 \|\| ORG_P3 \|\| ORG_P4 \|\| ORG_P5 \|\| ORG_P6 \|\| ORG_P7 \|\| ORG_P8 \|\| ORG_P9 \|\| ORG_PX \|\| ORG_P11 → exp_Init.ORG_P01 → SQ_CPM_NEWPAY_TBL.ORG_P01 → CPM_NEWPAY_TBL.ORG_P01 → exp_Init.ORG_P2 → SQ_CPM_NEWPAY_TBL.ORG_P2 → CPM_NEWPAY_TBL.ORG_P2 → exp_Init.ORG_P3 → SQ_CPM_NEWPAY_TBL.ORG_P3 → CPM_NEWPAY_TBL.ORG_P3 → exp_Init.ORG_P4 → SQ_CPM_NEWPAY_TBL.ORG_P4 → CPM_NEWPAY_TBL.ORG_P4 → exp_Init.ORG_P5 → SQ_CPM_NEWPAY_TBL.ORG_P5 → CPM_NEWPAY_TBL.ORG_P5 → exp_Init.ORG_P6 → SQ_CPM_NEWPAY_TBL.ORG_P6 → CPM_NEWPAY_TBL.ORG_P6 → exp_Init.ORG_P7 → SQ_CPM_NEWPAY_TBL.ORG_P7 → CPM_NEWPAY_TBL.ORG_P7 → exp_Init.ORG_P8 → SQ_CPM_NEWPAY_TBL.ORG_P8 → CPM_NEWPAY_TBL.ORG_P8 → exp_Init.ORG_P9 → SQ_CPM_NEWPAY_TBL.ORG_P9 → CPM_NEWPAY_TBL.ORG_P9 → exp_Init.ORG_PX → SQ_CPM_NEWPAY_TBL.ORG_PX → CPM_NEWPAY_TBL.ORG_PX → exp_Init.ORG_P11 → SQ_CPM_NEWPAY_TBL.ORG_P11 → CPM_NEWPAY_TBL.ORG_P11 | CPM_NEWPAY_TBL.ORG_P01; CPM_NEWPAY_TBL.ORG_P11; CPM_NEWPAY_TBL.ORG_P2; CPM_NEWPAY_TBL.ORG_P3; CPM_NEWPAY_TBL.ORG_P4; CPM_NEWPAY_TBL.ORG_P5; CPM_NEWPAY_TBL.ORG_P6; CPM_NEWPAY_TBL.ORG_P7; CPM_NEWPAY_TBL.ORG_P8; CPM_NEWPAY_TBL.ORG_P9; CPM_NEWPAY_TBL.ORG_PX |
| cdcskel_WS_PAY_OUT_REC | SPOC | exp_Final.SPOC → exp_Convert.o_SPOC = SPOC → exp_Init.SPOC → SQ_CPM_NEWPAY_TBL.SPOC → CPM_NEWPAY_TBL.SPOC | CPM_NEWPAY_TBL.SPOC |
| cdcskel_WS_PAY_OUT_REC | SEX_CDE | exp_Final.SEX_CDE → exp_Convert.o_SEX_CDE = SEX_CDE → exp_Init.SEX_CDE → SQ_CPM_NEWPAY_TBL.SEX_CDE → CPM_NEWPAY_TBL.SEX_CDE | CPM_NEWPAY_TBL.SEX_CDE |
| cdcskel_WS_PAY_OUT_REC | VET_PREF_CDE | exp_Final.VET_PREF_CDE → exp_Convert.o_VET_PREF_CDE = VET_PREF_CDE → exp_Init.VET_PREF_CDE → SQ_CPM_NEWPAY_TBL.VET_PREF_CDE → CPM_NEWPAY_TBL.VET_PREF_CDE | CPM_NEWPAY_TBL.VET_PREF_CDE |
| cdcskel_WS_PAY_OUT_REC | TENURE_CDE | exp_Final.TENURE_CDE → exp_Convert.o_TENURE_CDE = TENURE_CDE → exp_Init.TENURE_CDE → SQ_CPM_NEWPAY_TBL.TENURE_CDE → CPM_NEWPAY_TBL.TENURE_CDE | CPM_NEWPAY_TBL.TENURE_CDE |
| cdcskel_WS_PAY_OUT_REC | FIL_POS_CDE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | PERM_TEMP_POS_CDE | exp_Final.PERM_TEMP_POS_CDE → exp_Convert.o_PERM_TEMP_POS_CDE = PERM_TEMP_POS_CDE → exp_Init.PERM_TEMP_POS_CDE → SQ_CPM_NEWPAY_TBL.PERM_TEMP_POS_CDE → CPM_NEWPAY_TBL.PERM_TEMP_POS_CDE | CPM_NEWPAY_TBL.PERM_TEMP_POS_CDE |
| cdcskel_WS_PAY_OUT_REC | FT_PT_INTER_POS_CDE | exp_Final.FT_PT_INTER_POS_CDE → exp_Convert.o_FT_PT_INTER_POS_CDE = FT_PT_INTER_POS_CDE → exp_Init.FT_PT_INTER_POS_CDE → SQ_CPM_NEWPAY_TBL.FT_PT_INTER_POS_CDE → CPM_NEWPAY_TBL.FT_PT_INTER_POS_CDE | CPM_NEWPAY_TBL.FT_PT_INTER_POS_CDE |
| cdcskel_WS_PAY_OUT_REC | CITIZEN_CDE | exp_Final.CITIZEN_CDE → exp_Convert.o_CITIZEN_CDE = CITIZEN_CDE → exp_Init.CITIZEN_CDE → SQ_CPM_NEWPAY_TBL.CITIZEN_CDE → CPM_NEWPAY_TBL.CITIZEN_CDE | CPM_NEWPAY_TBL.CITIZEN_CDE |
| cdcskel_WS_PAY_OUT_REC | TYPE_APPT_CDE | exp_Final.TYPE_APPT_CDE → exp_Convert.o_TYPE_APPT_CDE = TYPE_APPT_CDE → exp_Init.TYPE_APPT_CDE → SQ_CPM_NEWPAY_TBL.TYPE_APPT_CDE → CPM_NEWPAY_TBL.TYPE_APPT_CDE | CPM_NEWPAY_TBL.TYPE_APPT_CDE |
| cdcskel_WS_PAY_OUT_REC | AGCY_CDE_PER | exp_Final.AGCY_CDE_PER → exp_Convert.o_AGCY_CDE_PER = AGCY_CDE_PER --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(AGCY_CDE_PER, 0)), '.', NULL) ,2, '0') → exp_Init.AGCY_CDE_PER → SQ_CPM_NEWPAY_TBL.AGCY_CDE_PER → CPM_NEWPAY_TBL.AGCY_CDE_PER | CPM_NEWPAY_TBL.AGCY_CDE_PER |
| cdcskel_WS_PAY_OUT_REC | DATE_BIRTH | exp_Final.DATE_BIRTH → exp_Convert.o_DATE_BIRTH = v_DATE_BIRTH --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(v_DATE_BIRTH, 0)), '.', NULL) ,6, '0') → exp_Convert.v_DATE_BIRTH = TO_DECIMAL( SUBSTR(v_DATE_BIRTH_CHAR_PAD, 1, 2) \|\| SUBSTR(v_DATE_BIRTH_CHAR_PAD, 3, 2) \|\| SUBSTR(v_DATE_BIRTH_CHAR_PAD, 7, 2) , 0) → exp_Convert.v_DATE_BIRTH_CHAR_PAD = LPAD(TO_CHAR(DATE_BIRTH), 8, '0') → exp_Init.DATE_BIRTH → SQ_CPM_NEWPAY_TBL.DATE_BIRTH → CPM_NEWPAY_TBL.DATE_BIRTH | CPM_NEWPAY_TBL.DATE_BIRTH |
| cdcskel_WS_PAY_OUT_REC | FS_DATE | exp_Final.FS_DATE → exp_Convert.o_FS_DATE = v_FS_DATE --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(v_FS_DATE, 0)),'.', NULL) ,6, '0') → exp_Convert.v_FS_DATE = TO_DECIMAL( SUBSTR(v_FS_DATE_CHAR_PAD, 1, 2) \|\| SUBSTR(v_FS_DATE_CHAR_PAD, 3, 2) \|\| SUBSTR(v_FS_DATE_CHAR_PAD, 7, 2) , 0) → exp_Convert.v_FS_DATE_CHAR_PAD = LPAD(TO_CHAR(FS_DATE), 8, '0') → exp_Init.FS_DATE → SQ_CPM_NEWPAY_TBL.FS_DATE → CPM_NEWPAY_TBL.FS_DATE | CPM_NEWPAY_TBL.FS_DATE |
| cdcskel_WS_PAY_OUT_REC | PERS_NOA | exp_Final.PERS_NOA → exp_Convert.o_PERS_NOA = PERS_NOA → exp_Init.PERS_NOA → SQ_CPM_NEWPAY_TBL.PERS_NOA → CPM_NEWPAY_TBL.PERS_NOA | CPM_NEWPAY_TBL.PERS_NOA |
| cdcskel_WS_PAY_OUT_REC | EOD_DATE | exp_Final.EOD_DATE → exp_Convert.o_EOD_DATE = v_EOD_DATE --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(v_EOD_DATE, 0)), '.', NULL) ,6, '0') → exp_Convert.v_EOD_DATE = TO_DECIMAL( SUBSTR(v_EOD_DATE_CHAR_PAD, 1, 2) \|\| SUBSTR(v_EOD_DATE_CHAR_PAD, 3, 2) \|\| SUBSTR(v_EOD_DATE_CHAR_PAD, 7, 2) , 0) → exp_Convert.v_EOD_DATE_CHAR_PAD = LPAD(TO_CHAR(EOD_DATE), 8, '0') → exp_Init.EOD_DATE → SQ_CPM_NEWPAY_TBL.EOD_DATE → CPM_NEWPAY_TBL.EOD_DATE | CPM_NEWPAY_TBL.EOD_DATE |
| cdcskel_WS_PAY_OUT_REC | N_ACT_CDE_SEP | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | SEP_DATE | exp_Final.SEP_DATE → exp_Convert.o_SEP_DATE = v_SEP_DATE --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(v_SEP_DATE_CHAR, 0)), '.', NULL) ,6, '0') → exp_Convert.v_SEP_DATE = TO_DECIMAL( SUBSTR(v_SEP_DATE_CHAR_PAD, 1, 2) \|\| SUBSTR(v_SEP_DATE_CHAR_PAD, 3, 2) \|\| SUBSTR(v_SEP_DATE_CHAR_PAD, 7, 2) , 0) → exp_Convert.v_SEP_DATE_CHAR_PAD = LPAD(TO_CHAR(SEP_DATE), 8, '0') → exp_Init.SEP_DATE → SQ_CPM_NEWPAY_TBL.SEP_DATE → CPM_NEWPAY_TBL.SEP_DATE | CPM_NEWPAY_TBL.SEP_DATE |
| cdcskel_WS_PAY_OUT_REC | N_ACT_CDE_EOD | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | PERS_EFF_DATE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | SEP_CDE | exp_Final.SEP_CDE → exp_Convert.o_SEP_CDE = SEP_CDE → exp_Init.SEP_CDE → SQ_CPM_NEWPAY_TBL.SEP_CDE → CPM_NEWPAY_TBL.SEP_CDE | CPM_NEWPAY_TBL.SEP_CDE |
| cdcskel_WS_PAY_OUT_REC | PSI_START_DATE | exp_Final.PSI_START_DATE → exp_Convert.o_PSI_START_DATE = v_PSI_START_DATE --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(v_PSI_START_DATE, 0)), '.', NULL) ,6, '0') → exp_Convert.v_PSI_START_DATE = TO_DECIMAL( SUBSTR(v_PSI_START_DATE_CHAR_PAD, 1, 2) \|\| SUBSTR(v_PSI_START_DATE_CHAR_PAD, 3, 2) \|\| SUBSTR(v_PSI_START_DATE_CHAR_PAD, 7, 2) , 0) → exp_Convert.v_PSI_START_DATE_CHAR_PAD = LPAD(TO_CHAR(PSI_START_DATE), 8, '0') → exp_Init.PSI_START_DATE → SQ_CPM_NEWPAY_TBL.PSI_START_DATE → CPM_NEWPAY_TBL.PSI_START_DATE | CPM_NEWPAY_TBL.PSI_START_DATE |
| cdcskel_WS_PAY_OUT_REC | DAY_90_CDE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | NINTY_DATE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | TITLEX | exp_Final.TITLEX → exp_Convert.o_TITLEX = ' ' | literal/expression: ' ' |
| cdcskel_WS_PAY_OUT_REC | PHY_HNDCP | exp_Final.PHY_HNDCP → exp_Convert.o_PHY_HNDCP = LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(PHY_HNDCP, 0)), '.', NULL), 2, '0') → exp_Init.PHY_HNDCP → SQ_CPM_NEWPAY_TBL.PHY_HNDCP → CPM_NEWPAY_TBL.PHY_HNDCP | CPM_NEWPAY_TBL.PHY_HNDCP |
| cdcskel_WS_PAY_OUT_REC | HLTH_BNFTS_CAR_CTL | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | UNIF_ALLOW_CDE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | ANN_UNIF_PYMT_DTE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | ANN_UNIF_ALLOW | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | ANN_UNIF_ALLOW_SIGN | exp_Final.ANN_UNIF_ALLOW_SIGN → exp_Convert.o_ANN_UNIF_ALLOW_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | OTHER_LIM_DATE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | OTHER_LIM_HOURS | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | DESIG_AGENT | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | PREMIUM_PAY | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | RSSDP | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | CEILING_EN_CDE | exp_Final.CEILING_EN_CDE → exp_Convert.o_CEILING_EN_CDE = CEILING_EN_CDE → exp_Init.CEILING_EN_CDE → SQ_CPM_NEWPAY_TBL.CEILING_EN_CDE → CPM_NEWPAY_TBL.CEILING_EN_CDE | CPM_NEWPAY_TBL.CEILING_EN_CDE |
| cdcskel_WS_PAY_OUT_REC | FUNC_CDE | exp_Final.FUNC_CDE → exp_Convert.o_FUNC_CDE = FUNC_CDE → exp_Init.FUNC_CDE → SQ_CPM_NEWPAY_TBL.FUNC_CDE → CPM_NEWPAY_TBL.FUNC_CDE | CPM_NEWPAY_TBL.FUNC_CDE |
| cdcskel_WS_PAY_OUT_REC | SUPV_CDE | exp_Final.SUPV_CDE → exp_Convert.o_SUPV_CDE = LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(SUPV_CDE, 0)), '.', NULL), 1, '0') → exp_Init.SUPV_CDE → SQ_CPM_NEWPAY_TBL.SUPV_CDE → CPM_NEWPAY_TBL.SUPV_CDE | CPM_NEWPAY_TBL.SUPV_CDE |
| cdcskel_WS_PAY_OUT_REC | PAY_BASIS | exp_Final.PAY_BASIS → exp_Convert.o_PAY_BASIS = PAY_BASIS → exp_Init.PAY_BASIS → SQ_CPM_NEWPAY_TBL.PAY_BASIS → CPM_NEWPAY_TBL.PAY_BASIS | CPM_NEWPAY_TBL.PAY_BASIS |
| cdcskel_WS_PAY_OUT_REC | POS_SEN_CDE | exp_Final.POS_SEN_CDE → exp_Convert.o_POS_SEN_CDE = POS_SEN_CDE --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(POS_SEN_CDE, 0)), '.', NULL), 1, '0') → exp_Init.POS_SEN_CDE → SQ_CPM_NEWPAY_TBL.POS_SEN_CDE → CPM_NEWPAY_TBL.POS_SEN_CDE | CPM_NEWPAY_TBL.POS_SEN_CDE |
| cdcskel_WS_PAY_OUT_REC | CAR_SERV_DTE | exp_Final.CAR_SERV_DTE → exp_Convert.o_CAR_SERV_DTE = v_CAR_SERV_DTE --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(v_CAR_SERV_DTE, 0)), '.', NULL) ,13, '0') → exp_Convert.v_CAR_SERV_DTE = TO_DECIMAL( SUBSTR(v_CAR_SERV_DTE_CHAR_PAD, 9, 2) \|\| SUBSTR(v_CAR_SERV_DTE_CHAR_PAD, 11, 2) \|\| SUBSTR(v_CAR_SERV_DTE_CHAR_PAD, 15, 2), 0) → exp_Convert.v_CAR_SERV_DTE_CHAR_PAD = LPAD(TO_CHAR(CAR_SERV_DTE), 16, '0') → exp_Init.CAR_SERV_DTE → SQ_CPM_NEWPAY_TBL.CAR_SERV_DTE → CPM_NEWPAY_TBL.CAR_SERV_DTE | CPM_NEWPAY_TBL.CAR_SERV_DTE |
| cdcskel_WS_PAY_OUT_REC | PROB_DTE | exp_Final.PROB_DTE → exp_Convert.o_PROB_DTE = v_PROB_DTE --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(v_PROB_DTE, 0)), '.', NULL) ,6, '0') → exp_Convert.v_PROB_DTE = TO_DECIMAL( SUBSTR(v_PROB_DTE_CHAR_PAD, 1, 2) \|\| SUBSTR(v_PROB_DTE_CHAR_PAD, 3, 2) \|\| SUBSTR(v_PROB_DTE_CHAR_PAD, 7, 2), 0) → exp_Convert.v_PROB_DTE_CHAR_PAD = LPAD(TO_CHAR(PROB_DTE), 8, '0') → exp_Init.PROB_DTE → SQ_CPM_NEWPAY_TBL.PROB_DTE → CPM_NEWPAY_TBL.PROB_DTE | CPM_NEWPAY_TBL.PROB_DTE |
| cdcskel_WS_PAY_OUT_REC | PERS_LEGAL_AUTH | exp_Final.PERS_LEGAL_AUTH → exp_Convert.o_PERS_LEGAL_AUTH = '00' | literal/expression: '00' |
| cdcskel_WS_PAY_OUT_REC | APPRTN_POS_CDE | exp_Final.APPRTN_POS_CDE → exp_Convert.o_APPRTN_POS_CDE = '0' | literal/expression: '0' |
| cdcskel_WS_PAY_OUT_REC | SPO_TERM_ID | exp_Final.SPO_TERM_ID → exp_Convert.o_SPO_TERM_ID = SPO_TERM_ID → exp_Init.SPO_TERM_ID → SQ_CPM_NEWPAY_TBL.SPO_TERM_ID → CPM_NEWPAY_TBL.SPO_TERM_ID | CPM_NEWPAY_TBL.SPO_TERM_ID |
| cdcskel_WS_PAY_OUT_REC | PAY_PLAN | exp_Final.PAY_PLAN → exp_Convert.o_PAY_PLAN = POSITION_1 \|\| POSITION_2 → exp_Init.POSITION_1 → SQ_CPM_NEWPAY_TBL.POSITION_1 → CPM_NEWPAY_TBL.POSITION_1 → exp_Init.POSITION_2 → SQ_CPM_NEWPAY_TBL.POSITION_2 → CPM_NEWPAY_TBL.POSITION_2 | CPM_NEWPAY_TBL.POSITION_1; CPM_NEWPAY_TBL.POSITION_2 |
| cdcskel_WS_PAY_OUT_REC | GRADE | exp_Final.GRADE → exp_Convert.o_GRADE = GRADE → exp_Init.GRADE → SQ_CPM_NEWPAY_TBL.GRADE → CPM_NEWPAY_TBL.GRADE | CPM_NEWPAY_TBL.GRADE |
| cdcskel_WS_PAY_OUT_REC | STEP | exp_Final.STEP → exp_Convert.o_STEP = STEP → exp_Init.STEP → SQ_CPM_NEWPAY_TBL.STEP → CPM_NEWPAY_TBL.STEP | CPM_NEWPAY_TBL.STEP |
| cdcskel_WS_PAY_OUT_REC | ABNOR_RATE_CDE | exp_Final.ABNOR_RATE_CDE → exp_Convert.o_ABNOR_RATE_CDE = ABNOR_RATE_CDE → exp_Init.ABNOR_RATE_CDE → SQ_CPM_NEWPAY_TBL.ABNOR_RATE_CDE → CPM_NEWPAY_TBL.ABNOR_RATE_CDE | CPM_NEWPAY_TBL.ABNOR_RATE_CDE |
| cdcskel_WS_PAY_OUT_REC | SAVED_RATE_DATE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | APPT_LIM_DATE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | APPT_LIM_HRS | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | APPT_LIM_HRS_SIGN | exp_Final.APPT_LIM_HRS_SIGN → exp_Convert.o_APPT_LIM_HRS_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | APPT_LIM_PAY | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | APPT_LIM_PAY_SIGN | exp_Final.APPT_LIM_PAY_SIGN → exp_Convert.o_APPT_LIM_PAY_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | DATE_LAST_PAY_CHG | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | BASE_HRS | exp_Final.BASE_HRS → exp_Convert.o_BASE_HRS = ABS(BASE_HRS) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(BASE_HRS, 0)), '.', NULL), 3, '0') → exp_Init.BASE_HRS → SQ_CPM_NEWPAY_TBL.BASE_HRS → CPM_NEWPAY_TBL.BASE_HRS | CPM_NEWPAY_TBL.BASE_HRS |
| cdcskel_WS_PAY_OUT_REC | ANNUAL_SAL | exp_Final.ANNUAL_SAL → exp_Convert.o_ANNUAL_SAL = ABS(ANNUAL_SAL) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ANNUAL_SAL, 0)), '.', NULL), 7, '0') → exp_Init.ANNUAL_SAL → SQ_CPM_NEWPAY_TBL.ANNUAL_SAL → CPM_NEWPAY_TBL.ANNUAL_SAL | CPM_NEWPAY_TBL.ANNUAL_SAL |
| cdcskel_WS_PAY_OUT_REC | ANNUAL_SAL_PAPER | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | HRLY_RATE | exp_Final.HRLY_RATE → exp_Convert.o_HRLY_RATE = ABS(HRLY_RATE) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(HRLY_RATE, 2)), '.', NULL), 5, '0') → exp_Init.HRLY_RATE → SQ_CPM_NEWPAY_TBL.HRLY_RATE → CPM_NEWPAY_TBL.HRLY_RATE | CPM_NEWPAY_TBL.HRLY_RATE |
| cdcskel_WS_PAY_OUT_REC | HRLY_RATE_PAPER | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | OT_RATE | exp_Final.OT_RATE → exp_Convert.o_OT_RATE = ABS(OT_RATE) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(OT_RATE, 2)), '.', NULL), 5, '0') → exp_Init.OT_RATE → SQ_CPM_NEWPAY_TBL.OT_RATE → CPM_NEWPAY_TBL.OT_RATE | CPM_NEWPAY_TBL.OT_RATE |
| cdcskel_WS_PAY_OUT_REC | WSB_NSD2_RATE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | WSB_NSD3_RATE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | PD_PCT | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | COLA_PCT | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | UNIF_ALLOW | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | OTHER_TAX_PAY_CDE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | OTHER_TAX_PAY_AMT | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | OTHER_TAX_PAY_AMT_SIGN | exp_Final.OTHER_TAX_PAY_AMT_SIGN → exp_Convert.o_OTHER_TAX_PAY_AMT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | OTHER_NON_TAX_PAY_CDE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | OTH_N_TAX_PAY_AMT | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | OTH_N_TAX_PAY_AMT_SIGN | exp_Final.OTH_N_TAX_PAY_AMT_SIGN → exp_Convert.o_OTH_N_TAX_PAY_AMT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | SEV_PAY_TOT | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | SEV_PAY_TOT_SIGN | exp_Final.SEV_PAY_TOT_SIGN → exp_Convert.o_SEV_PAY_TOT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | SEV_PAY_AMT | exp_Final.SEV_PAY_AMT → exp_Convert.o_SEV_PAY_AMT = ABS(SEV_PAY_AMT) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(SEV_PAY_AMT), 2)), '.', NULL), 7, '0') → exp_Init.SEV_PAY_AMT → SQ_CPM_NEWPAY_TBL.SEV_PAY_AMT → CPM_NEWPAY_TBL.SEV_PAY_AMT | CPM_NEWPAY_TBL.SEV_PAY_AMT |
| cdcskel_WS_PAY_OUT_REC | SEV_PAY_AMT_SIGN | exp_Final.SEV_PAY_AMT_SIGN → exp_Convert.o_SEV_PAY_AMT_SIGN = IIF(SIGN(SEV_PAY_AMT) = -1, '-', '+') → exp_Init.SEV_PAY_AMT → SQ_CPM_NEWPAY_TBL.SEV_PAY_AMT → CPM_NEWPAY_TBL.SEV_PAY_AMT | CPM_NEWPAY_TBL.SEV_PAY_AMT |
| cdcskel_WS_PAY_OUT_REC | SEV_EFF_DAT | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | SEV_EFF_DAT_SIGN | exp_Final.SEV_EFF_DAT_SIGN → exp_Convert.o_SEV_EFF_DAT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | LUMP_SUM_PAID_HOURS | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | FED_RETIRE_1 | exp_Final.FED_RETIRE_1 → exp_Convert.o_FED_RETIRE_1 = SUBSTR(FED_RETIRE_CDE, 1, 1) → exp_Init.FED_RETIRE_CDE → SQ_CPM_NEWPAY_TBL.FED_RETIRE_CDE → CPM_NEWPAY_TBL.FED_RETIRE_CDE | CPM_NEWPAY_TBL.FED_RETIRE_CDE |
| cdcskel_WS_PAY_OUT_REC | FED_RETIRE_2 | exp_Final.FED_RETIRE_2 → exp_Convert.o_FED_RETIRE_2 = SUBSTR(FED_RETIRE_CDE, 2, 1) → exp_Init.FED_RETIRE_CDE → SQ_CPM_NEWPAY_TBL.FED_RETIRE_CDE → CPM_NEWPAY_TBL.FED_RETIRE_CDE | CPM_NEWPAY_TBL.FED_RETIRE_CDE |
| cdcskel_WS_PAY_OUT_REC | EMPTY1 | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | MP_POOL_DES | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | MP_HRLY_RATE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | MP_HRLY_RATE_SIGN | exp_Final.MP_HRLY_RATE_SIGN → exp_Convert.o_MP_HRLY_RATE_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | LEVY_FLAG | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | MEDC_NONRES_CDE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | FED_RETIRE_CDE_OLD | exp_Final.FED_RETIRE_CDE_OLD → exp_Convert.o_FED_RETIRE_CDE_OLD = FED_RETIRE_CDE_OLD → exp_Init.FED_RETIRE_CDE_OLD → SQ_CPM_NEWPAY_TBL.FED_RETIRE_CDE_OLD → CPM_NEWPAY_TBL.FED_RETIRE_CDE_OLD | CPM_NEWPAY_TBL.FED_RETIRE_CDE_OLD |
| cdcskel_WS_PAY_OUT_REC | REFUND_CDE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | REFUND_AMT | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | REFUND_AMT_SIGN | exp_Final.REFUND_AMT_SIGN → exp_Convert.o_REFUND_AMT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | REFUND_TOTAL | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | REFUND_TOTAL_SIGN | exp_Final.REFUND_TOTAL_SIGN → exp_Convert.o_REFUND_TOTAL_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | REFUND_CURRENT_BAL | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | REFUND_CURRENT_BAL_SIGN | exp_Final.REFUND_CURRENT_BAL_SIGN → exp_Convert.o_REFUND_CURRENT_BAL_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | LEVY_TOT_AMT | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | LEVY_TOT_AMT_SIGN | exp_Final.LEVY_TOT_AMT_SIGN → exp_Convert.o_LEVY_TOT_AMT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | EFF_DATE_LEVY_DED | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | LEVY_PP_DED | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | LEVY_PP_DED_SIGN | exp_Final.LEVY_PP_DED_SIGN → exp_Convert.o_LEVY_PP_DED_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | TOT_FED_TAX_EXEMP | exp_Final.TOT_FED_TAX_EXEMP → exp_Convert.o_TOT_FED_TAX_EXEMP = LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(TOT_FED_TAX_EXEMP, 0)), '.', NULL), 2, '0') → exp_Init.TOT_FED_TAX_EXEMP → SQ_CPM_NEWPAY_TBL.TOT_FED_TAX_EXEMP → CPM_NEWPAY_TBL.TOT_FED_TAX_EXEMP | CPM_NEWPAY_TBL.TOT_FED_TAX_EXEMP |
| cdcskel_WS_PAY_OUT_REC | ADDL_FED_TAX_EXEM | exp_Final.ADDL_FED_TAX_EXEM → exp_Convert.o_ADDL_FED_TAX_EXEM = '00' | literal/expression: '00' |
| cdcskel_WS_PAY_OUT_REC | FED_TAX_MAR_STAT | exp_Final.FED_TAX_MAR_STAT → exp_Convert.o_FED_TAX_MAR_STAT = FED_TAX_MAR_STAT --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(FED_TAX_MAR_STAT, 0)), '.', NULL), 1, '0') → exp_Init.FED_TAX_MAR_STAT → SQ_CPM_NEWPAY_TBL.FED_TAX_MAR_STAT → CPM_NEWPAY_TBL.FED_TAX_MAR_STAT | CPM_NEWPAY_TBL.FED_TAX_MAR_STAT |
| cdcskel_WS_PAY_OUT_REC | FED_OPT_TAX_DED | exp_Final.FED_OPT_TAX_DED → exp_Convert.o_FED_OPT_TAX_DED = LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(FED_OPT_TAX_DED, 0)), '.', NULL), 3, '0') → exp_Init.FED_OPT_TAX_DED → SQ_CPM_NEWPAY_TBL.FED_OPT_TAX_DED → CPM_NEWPAY_TBL.FED_OPT_TAX_DED | CPM_NEWPAY_TBL.FED_OPT_TAX_DED |
| cdcskel_WS_PAY_OUT_REC | FED_W4A_CDE | exp_Final.FED_W4A_CDE → exp_Convert.o_FED_W4A_CDE = '0' | literal/expression: '0' |
| cdcskel_WS_PAY_OUT_REC | ST_NON_RES_CDE | exp_Final.ST_NON_RES_CDE → exp_Convert.o_ST_NON_RES_CDE = '1' | literal/expression: '1' |
| cdcskel_WS_PAY_OUT_REC | ST_TAX_MAR_STAT | exp_Final.ST_TAX_MAR_STAT → exp_Convert.o_ST_TAX_MAR_STAT = ST_TAX_MAR_STAT --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ST_TAX_MAR_STAT, 0)), '.', NULL), 1, '0') → exp_Init.ST_TAX_MAR_STAT → SQ_CPM_NEWPAY_TBL.ST_TAX_MAR_STAT → CPM_NEWPAY_TBL.ST_TAX_MAR_STAT | CPM_NEWPAY_TBL.ST_TAX_MAR_STAT |
| cdcskel_WS_PAY_OUT_REC | ST_TAX_EXEMP | exp_Final.ST_TAX_EXEMP → exp_Convert.o_ST_TAX_EXEMP = ABS(ST_TAX_EXEMP) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ST_TAX_EXEMP, 0)), '.', NULL), 5, '0') → exp_Init.ST_TAX_EXEMP → SQ_CPM_NEWPAY_TBL.ST_TAX_EXEMP → CPM_NEWPAY_TBL.ST_TAX_EXEMP | CPM_NEWPAY_TBL.ST_TAX_EXEMP |
| cdcskel_WS_PAY_OUT_REC | ST_TAX_OPT_DED | exp_Final.ST_TAX_OPT_DED → exp_Convert.o_ST_TAX_OPT_DED = ABS(ST_TAX_OPT_DED) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ST_TAX_OPT_DED, 0)), '.', NULL), 3, '0') → exp_Init.ST_TAX_OPT_DED → SQ_CPM_NEWPAY_TBL.ST_TAX_OPT_DED → CPM_NEWPAY_TBL.ST_TAX_OPT_DED | CPM_NEWPAY_TBL.ST_TAX_OPT_DED |
| cdcskel_WS_PAY_OUT_REC | ST_TAX_CDE | exp_Final.ST_TAX_CDE → exp_Convert.o_ST_TAX_CDE = ST_TAX_CDE → exp_Init.ST_TAX_CDE → SQ_CPM_NEWPAY_TBL.ST_TAX_CDE → CPM_NEWPAY_TBL.ST_TAX_CDE | CPM_NEWPAY_TBL.ST_TAX_CDE |
| cdcskel_WS_PAY_OUT_REC | CITY_TAX_CDE | exp_Final.CITY_TAX_CDE → exp_Convert.o_CITY_TAX_CDE = CITY_ST_CDE \|\| CITY_ID_CDE → exp_Init.CITY_ST_CDE → SQ_CPM_NEWPAY_TBL.CITY_ST_CDE → CPM_NEWPAY_TBL.CITY_ST_CDE → exp_Init.CITY_ID_CDE → SQ_CPM_NEWPAY_TBL.CITY_ID_CDE → CPM_NEWPAY_TBL.CITY_ID_CDE | CPM_NEWPAY_TBL.CITY_ID_CDE; CPM_NEWPAY_TBL.CITY_ST_CDE |
| cdcskel_WS_PAY_OUT_REC | CITY_TAX_PER | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | CITY_TAX_PER_SIGN | exp_Final.CITY_TAX_PER_SIGN → exp_Convert.o_CITY_TAX_PER_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | CITY_MAR_STAT | exp_Final.CITY_MAR_STAT → exp_Convert.o_CITY_MAR_STAT = CITY_MAR_STAT --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(CITY_MAR_STAT, 0)), '.', NULL), 1, '0') → exp_Init.CITY_MAR_STAT → SQ_CPM_NEWPAY_TBL.CITY_MAR_STAT → CPM_NEWPAY_TBL.CITY_MAR_STAT | CPM_NEWPAY_TBL.CITY_MAR_STAT |
| cdcskel_WS_PAY_OUT_REC | CITY_EXEMP | exp_Final.CITY_EXEMP → exp_Convert.o_CITY_EXEMP = LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(CITY_EXEMP, 0)), '.', NULL), 2, '0') → exp_Init.CITY_EXEMP → SQ_CPM_NEWPAY_TBL.CITY_EXEMP → CPM_NEWPAY_TBL.CITY_EXEMP | CPM_NEWPAY_TBL.CITY_EXEMP |
| cdcskel_WS_PAY_OUT_REC | CITY_RES_CDE | exp_Final.CITY_RES_CDE → exp_Convert.o_CITY_RES_CDE = '0' | literal/expression: '0' |
| cdcskel_WS_PAY_OUT_REC | OCC_PRIV_TAX_CDE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | OCC_PRIV_TAX_AMT | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | OCC_PRIV_TAX_AMT_SIGN | exp_Final.OCC_PRIV_TAX_AMT_SIGN → exp_Convert.o_OCC_PRIV_TAX_AMT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | HLTH_ENROL_CDE | exp_Final.HLTH_ENROL_CDE → exp_Convert.o_HLTH_ENROL_CDE = HLTH_ENROL_CDE_1_2 \|\| HLTH_ENROL_CDE_3 → exp_Init.HLTH_ENROL_CDE_1_2 → SQ_CPM_NEWPAY_TBL.HLTH_ENROL_CDE_1_2 → CPM_NEWPAY_TBL.HLTH_ENROL_CDE_1_2 → exp_Init.HLTH_ENROL_CDE_3 → SQ_CPM_NEWPAY_TBL.HLTH_ENROL_CDE_3 → CPM_NEWPAY_TBL.HLTH_ENROL_CDE_3 | CPM_NEWPAY_TBL.HLTH_ENROL_CDE_1_2; CPM_NEWPAY_TBL.HLTH_ENROL_CDE_3 |
| cdcskel_WS_PAY_OUT_REC | EFF_DATE_HLTH_NACT | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | HLTH_DED | exp_Final.HLTH_DED → exp_Convert.o_HLTH_DED = ABS(HLTH_DED) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(HLTH_DED), 2)), '.', NULL), 5, '0') → exp_Init.HLTH_DED → SQ_CPM_NEWPAY_TBL.HLTH_DED → CPM_NEWPAY_TBL.HLTH_DED | CPM_NEWPAY_TBL.HLTH_DED |
| cdcskel_WS_PAY_OUT_REC | HLTH_DED_SIGN | exp_Final.HLTH_DED_SIGN → exp_Convert.o_HLTH_DED_SIGN = IIF(SIGN(HLTH_DED) = -1, '-', '+') → exp_Init.HLTH_DED → SQ_CPM_NEWPAY_TBL.HLTH_DED → CPM_NEWPAY_TBL.HLTH_DED | CPM_NEWPAY_TBL.HLTH_DED |
| cdcskel_WS_PAY_OUT_REC | HLTH_GOVT_SHARE | exp_Final.HLTH_GOVT_SHARE → exp_Convert.o_HLTH_GOVT_SHARE = ABS(HLTH_GOVT_SHARE) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(HLTH_GOVT_SHARE), 2)), '.', NULL), 5, '0') → exp_Init.HLTH_GOVT_SHARE → SQ_CPM_NEWPAY_TBL.HLTH_GOVT_SHARE → CPM_NEWPAY_TBL.HLTH_GOVT_SHARE | CPM_NEWPAY_TBL.HLTH_GOVT_SHARE |
| cdcskel_WS_PAY_OUT_REC | HLTH_GOVT_SHARE_SIGN | exp_Final.HLTH_GOVT_SHARE_SIGN → exp_Convert.o_HLTH_GOVT_SHARE_SIGN = IIF(SIGN(HLTH_GOVT_SHARE) = -1, '-', '+') → exp_Init.HLTH_GOVT_SHARE → SQ_CPM_NEWPAY_TBL.HLTH_GOVT_SHARE → CPM_NEWPAY_TBL.HLTH_GOVT_SHARE | CPM_NEWPAY_TBL.HLTH_GOVT_SHARE |
| cdcskel_WS_PAY_OUT_REC | FEGLI_CDE | exp_Final.FEGLI_CDE → exp_Convert.o_FEGLI_CDE = FEGLI_CDE → exp_Init.FEGLI_CDE → SQ_CPM_NEWPAY_TBL.FEGLI_CDE → CPM_NEWPAY_TBL.FEGLI_CDE | CPM_NEWPAY_TBL.FEGLI_CDE |
| cdcskel_WS_PAY_OUT_REC | EFF_DATE_FEGLI_REG | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | EFF_DATE_FEGLI_OPT | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | CHAR_AREA_CDE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | EFF_DATE_CHAR | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | CHAR_DED | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | CHAR_DED_SIGN | exp_Final.CHAR_DED_SIGN → exp_Convert.o_CHAR_DED_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | UNION_IDENT_CDE | exp_Final.UNION_IDENT_CDE → exp_Convert.o_UNION_IDENT_CDE = UNION_IDENT_CDE → exp_Init.UNION_IDENT_CDE → SQ_CPM_NEWPAY_TBL.UNION_IDENT_CDE → CPM_NEWPAY_TBL.UNION_IDENT_CDE | CPM_NEWPAY_TBL.UNION_IDENT_CDE |
| cdcskel_WS_PAY_OUT_REC | EFF_DATE_UN_N_ACT | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | UNION_DED | exp_Final.UNION_DED → exp_Convert.o_UNION_DED = ABS(UNION_DED) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(UNION_DED), 2)), '.', NULL), 5, '0') → exp_Init.UNION_DED → SQ_CPM_NEWPAY_TBL.UNION_DED → CPM_NEWPAY_TBL.UNION_DED | CPM_NEWPAY_TBL.UNION_DED |
| cdcskel_WS_PAY_OUT_REC | UNION_DED_SIGN | exp_Final.UNION_DED_SIGN → exp_Convert.o_UNION_DED_SIGN = IIF(SIGN(UNION_DED) = -1, '-', '+') → exp_Init.UNION_DED → SQ_CPM_NEWPAY_TBL.UNION_DED → CPM_NEWPAY_TBL.UNION_DED | CPM_NEWPAY_TBL.UNION_DED |
| cdcskel_WS_PAY_OUT_REC | QUARTERS_DED | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | QUARTERS_DED_SIGN | exp_Final.QUARTERS_DED_SIGN → exp_Convert.o_QUARTERS_DED_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | SUBSIST_DED | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | SUBSIST_DED_SIGN | exp_Final.SUBSIST_DED_SIGN → exp_Convert.o_SUBSIST_DED_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | LAUNDRY_DED | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | LAUNDRY_DED_SIGN | exp_Final.LAUNDRY_DED_SIGN → exp_Convert.o_LAUNDRY_DED_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | FERS_CONV_DTE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | FERS_FROZEN_SICK_LV | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | FERS_BAL_FWD | exp_Final.FERS_BAL_FWD → exp_Convert.o_FERS_BAL_FWD = ABS(FERS_BAL_FWD) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(FERS_BAL_FWD), 2)), '.', NULL), 9, '0') → exp_Init.FERS_BAL_FWD → SQ_CPM_NEWPAY_TBL.FERS_BAL_FWD → CPM_NEWPAY_TBL.FERS_BAL_FWD | CPM_NEWPAY_TBL.FERS_BAL_FWD |
| cdcskel_WS_PAY_OUT_REC | FERS_BAL_FWD_SIGN | exp_Final.FERS_BAL_FWD_SIGN → exp_Convert.o_FERS_BAL_FWD_SIGN = IIF(SIGN(FERS_BAL_FWD) = -1, '-', '+') → exp_Init.FERS_BAL_FWD → SQ_CPM_NEWPAY_TBL.FERS_BAL_FWD → CPM_NEWPAY_TBL.FERS_BAL_FWD | CPM_NEWPAY_TBL.FERS_BAL_FWD |
| cdcskel_WS_PAY_OUT_REC | TSPA_STATUS_CODE | exp_Final.TSPA_STATUS_CODE → exp_Convert.o_TSPA_STATUS_CODE = TSPA_STATUS_CODE → exp_Init.TSPA_STATUS_CODE → SQ_CPM_NEWPAY_TBL.TSPA_STATUS_CODE → CPM_NEWPAY_TBL.TSPA_STATUS_CODE | CPM_NEWPAY_TBL.TSPA_STATUS_CODE |
| cdcskel_WS_PAY_OUT_REC | TSPA_STATUS_CODE_DTE | exp_Final.TSPA_STATUS_CODE_DTE → exp_Convert.o_TSPA_STATUS_CODE_DTE = v_TSPA_STATUS_DTE --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(v_TSPA_STATUS_DTE, 0)), '.', NULL) ,6, '0') → exp_Convert.v_TSPA_STATUS_DTE = TO_DECIMAL( SUBSTR(v_TSPA_STATUS_DTE_CHAR_PAD, 1, 2) \|\| SUBSTR(v_TSPA_STATUS_DTE_CHAR_PAD, 3, 2) \|\| SUBSTR(v_TSPA_STATUS_DTE_CHAR_PAD, 7, 2) , 0) → exp_Convert.v_TSPA_STATUS_DTE_CHAR_PAD = LPAD(TO_CHAR(TSPA_STATUS_CODE_DTE), 8, '0') → exp_Init.TSPA_STATUS_CODE_DTE → SQ_CPM_NEWPAY_TBL.TSPA_STATUS_CODE_DTE → CPM_NEWPAY_TBL.TSPA_STATUS_CODE_DTE | CPM_NEWPAY_TBL.TSPA_STATUS_CODE_DTE |
| cdcskel_WS_PAY_OUT_REC | TSPA_SCD | exp_Final.TSPA_SCD → exp_Convert.o_TSPA_SCD = v_TSPA_SCD --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(TSPA_SCD, 0)), '.', NULL), 8, '0') → exp_Convert.v_TSPA_SCD = TO_DECIMAL( SUBSTR(v_TSPA_SCD_CHAR_PAD, 1, 2) \|\| SUBSTR(v_TSPA_SCD_CHAR_PAD, 3, 2) \|\| SUBSTR(v_TSPA_SCD_CHAR_PAD, 7, 2) , 0) --TO_DECIMAL(SUBSTR(v_TSPA_SCD_CHAR_PAD, 3, 5) , 0) → exp_Convert.v_TSPA_SCD_CHAR_PAD = LPAD(TO_CHAR(TO_DECIMAL(TSPA_SCD, 0)), 8, '0') → exp_Init.TSPA_SCD → SQ_CPM_NEWPAY_TBL.TSPA_SCD → CPM_NEWPAY_TBL.TSPA_SCD | CPM_NEWPAY_TBL.TSPA_SCD |
| cdcskel_WS_PAY_OUT_REC | TSPA_VEST_PERIOD | exp_Final.TSPA_VEST_PERIOD → exp_Convert.o_TSPA_VEST_PERIOD = LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(TSPA_VEST_PERIOD, 0)), '.', NULL), 1, '0') → exp_Init.TSPA_VEST_PERIOD → SQ_CPM_NEWPAY_TBL.TSPA_VEST_PERIOD → CPM_NEWPAY_TBL.TSPA_VEST_PERIOD | CPM_NEWPAY_TBL.TSPA_VEST_PERIOD |
| cdcskel_WS_PAY_OUT_REC | FILLER00 | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | TSPA_EAMT_DED | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | TSPA_EAMT_DED_SIGN | exp_Final.TSPA_EAMT_DED_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | TSPA_PRBAL | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | TSPA_PRBAL_SIGN | exp_Final.TSPA_PRBAL_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | TSPA_PRAMT_DED | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | TSPA_PRAMT_DED_SIGN | exp_Final.TSPA_PRAMT_DED_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | TSPG_ERDIST | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | TSPG_ERDIST_SIGN | exp_Final.TSPG_ERDIST_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | TSPG_PRDIST | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | TSPG_PRDIST_SIGN | exp_Final.TSPG_PRDIST_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | TSPG_GRDIST | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | TSPG_GRDIST_SIGN | exp_Final.TSPG_GRDIST_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | TSPG_INIT_1_PCT | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | TSPG_INIT_1_PCT_SIGN | exp_Final.TSPG_INIT_1_PCT_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | TSPG_1_PCT_ADJ | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | TSPG_1_PCT_ADJ_SIGN | exp_Final.TSPG_1_PCT_ADJ_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | TSPG_1_PCT_ADJ_CUM | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | TSPG_1_PCT_ADJ_CUM_SIGN | exp_Final.TSPG_1_PCT_ADJ_CUM_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | TSPF_ERDIST | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | TSPF_ERDIST_SIGN | exp_Final.TSPF_ERDIST_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | TSPF_PRDIST | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | TSPF_PRDIST_SIGN | exp_Final.TSPF_PRDIST_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | TSPF_GRDIST | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | TSPF_GRDIST_SIGN | exp_Final.TSPF_GRDIST_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | TSPC_ERDIST | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | TSPC_ERDIST_SIGN | exp_Final.TSPC_ERDIST_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | TSPC_PRDIST | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | TSPC_PRDIST_SIGN | exp_Final.TSPC_PRDIST_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | TSPC_GRDIST | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | TSPC_GRDIST_SIGN | exp_Final.TSPC_GRDIST_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | ALT_1_INST_AC_NO | exp_Final.ALT_1_INST_AC_NO → exp_Convert.o_ALT_1_INST_AC_NO = LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ALT_1_ROUTE_ID, 0)), '.', NULL), 8, '0') \|\| LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ALT_1_ROUTE_DIGIT, 0)), '.', NULL), 1, '0') → exp_Init.ALT_1_ROUTE_ID → SQ_CPM_NEWPAY_TBL.ALT_1_ROUTE_ID → CPM_NEWPAY_TBL.ALT_1_ROUTE_ID → exp_Init.ALT_1_ROUTE_DIGIT → SQ_CPM_NEWPAY_TBL.ALT_1_ROUTE_DIGIT → CPM_NEWPAY_TBL.ALT_1_ROUTE_DIGIT | CPM_NEWPAY_TBL.ALT_1_ROUTE_DIGIT; CPM_NEWPAY_TBL.ALT_1_ROUTE_ID |
| cdcskel_WS_PAY_OUT_REC | ALT_1_EE_ACCT_NO | exp_Final.ALT_1_EE_ACCT_NO → exp_Convert.o_ALT_1_EE_ACCT_NO = ALT_1_EE_ACCT_NO → exp_Init.ALT_1_EE_ACCT_NO → SQ_CPM_NEWPAY_TBL.ALT_1_EE_ACCT_NO → CPM_NEWPAY_TBL.ALT_1_EE_ACCT_NO | CPM_NEWPAY_TBL.ALT_1_EE_ACCT_NO |
| cdcskel_WS_PAY_OUT_REC | ALT_1_CODE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | ALT_1_ACCT_TYPE | exp_Final.ALT_1_ACCT_TYPE → exp_Convert.o_ALT_1_ACCT_TYPE = ALT_1_ACCT_TYPE → exp_Init.ALT_1_ACCT_TYPE → SQ_CPM_NEWPAY_TBL.ALT_1_ACCT_TYPE → CPM_NEWPAY_TBL.ALT_1_ACCT_TYPE | CPM_NEWPAY_TBL.ALT_1_ACCT_TYPE |
| cdcskel_WS_PAY_OUT_REC | EFF_DATE_ALT_1_N_ACT | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | ALT_1_DED | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | ALT_1_DED_SIGN | exp_Final.ALT_1_DED_SIGN → exp_Convert.o_ALT_1_DED_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | ALT_2_INST_ACCT_NO | exp_Final.ALT_2_INST_ACCT_NO → exp_Convert.o_ALT_2_INST_ACCT_NO = LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ALT_2_ROUTE_ID, 0)), '.', NULL), 8, '0') \|\| LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ALT_2_ROUTE_DIGIT, 0)), '.', NULL), 1, '0') → exp_Init.ALT_2_ROUTE_ID → SQ_CPM_NEWPAY_TBL.ALT_2_ROUTE_ID → CPM_NEWPAY_TBL.ALT_2_ROUTE_ID → exp_Init.ALT_2_ROUTE_DIGIT → SQ_CPM_NEWPAY_TBL.ALT_2_ROUTE_DIGIT → CPM_NEWPAY_TBL.ALT_2_ROUTE_DIGIT | CPM_NEWPAY_TBL.ALT_2_ROUTE_DIGIT; CPM_NEWPAY_TBL.ALT_2_ROUTE_ID |
| cdcskel_WS_PAY_OUT_REC | ALT_2_EE_ACCT_NO | exp_Final.ALT_2_EE_ACCT_NO → exp_Convert.o_ALT_2_EE_ACCT_NO = ALT_2_EE_ACCT_NO → exp_Init.ALT_2_EE_ACCT_NO → SQ_CPM_NEWPAY_TBL.ALT_2_EE_ACCT_NO → CPM_NEWPAY_TBL.ALT_2_EE_ACCT_NO | CPM_NEWPAY_TBL.ALT_2_EE_ACCT_NO |
| cdcskel_WS_PAY_OUT_REC | ALT_2_CODE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | ALT_2_ACCT_TYPE | exp_Final.ALT_2_ACCT_TYPE → exp_Convert.o_ALT_2_ACCT_TYPE = ALT_2_ACCT_TYPE → exp_Init.ALT_2_ACCT_TYPE → SQ_CPM_NEWPAY_TBL.ALT_2_ACCT_TYPE → CPM_NEWPAY_TBL.ALT_2_ACCT_TYPE | CPM_NEWPAY_TBL.ALT_2_ACCT_TYPE |
| cdcskel_WS_PAY_OUT_REC | EFF_DATE_ALT_2_N_ACT | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | ALT_2_DED | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | ALT_2_DED_SIGN | exp_Final.ALT_2_DED_SIGN → exp_Convert.o_ALT_2_DED_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | EFT_CODE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | EMPTY2 | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | EFT_EMPL_ACCT_NUMBER | exp_Final.EFT_EMPL_ACCT_NUMBER → exp_Convert.o_EFT_EMPL_ACCT_NUMBER = EFT_EMPL_ACCT_NUMBER → exp_Init.EFT_EMPL_ACCT_NUMBER → SQ_CPM_NEWPAY_TBL.EFT_EMPL_ACCT_NUMBER → CPM_NEWPAY_TBL.EFT_EMPL_ACCT_NUMBER | CPM_NEWPAY_TBL.EFT_EMPL_ACCT_NUMBER |
| cdcskel_WS_PAY_OUT_REC | EFT_EMPL_ACCT_TYPE | exp_Final.EFT_EMPL_ACCT_TYPE → exp_Convert.o_EFT_EMPL_ACCT_TYPE = EFT_EMPL_ACCT_TYPE → exp_Init.EFT_EMPL_ACCT_TYPE → SQ_CPM_NEWPAY_TBL.EFT_EMPL_ACCT_TYPE → CPM_NEWPAY_TBL.EFT_EMPL_ACCT_TYPE | CPM_NEWPAY_TBL.EFT_EMPL_ACCT_TYPE |
| cdcskel_WS_PAY_OUT_REC | EFT_EFF_DATE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | CSA_CDE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | CSA_PERCENT_DED | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | CSA_PERCENT_DED_SIGN | exp_Final.CSA_PERCENT_DED_SIGN → exp_Convert.o_CSA_PERCENT_DED_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | CSA_STD_AMOUNT_DED | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | CSA_STD_AMOUNT_DED_SIGN | exp_Final.CSA_STD_AMOUNT_DED_SIGN → exp_Convert.o_CSA_STD_AMOUNT_DED_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | CSA_EFF_DATE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | CSA_RECIPIENT_NAME | exp_Final.CSA_RECIPIENT_NAME → exp_Convert.o_CSA_RECIPIENT_NAME = CSA_RECIPIENT_NAME → exp_Init.CSA_RECIPIENT_NAME → SQ_CPM_NEWPAY_TBL.CSA_RECIPIENT_NAME → CPM_NEWPAY_TBL.CSA_RECIPIENT_NAME | CPM_NEWPAY_TBL.CSA_RECIPIENT_NAME |
| cdcskel_WS_PAY_OUT_REC | CSA_RECIPIENT_ACCT_NO | exp_Final.CSA_RECIPIENT_ACCT_NO → exp_Convert.o_CSA_RECIPIENT_ACCT_NO1 = CSA_RECIPIENT_ACCT_NO → exp_Init.CSA_RECIPIENT_ACCT_NO → SQ_CPM_NEWPAY_TBL.CSA_RECIPIENT_ACCT_NO → CPM_NEWPAY_TBL.CSA_RECIPIENT_ACCT_NO | CPM_NEWPAY_TBL.CSA_RECIPIENT_ACCT_NO |
| cdcskel_WS_PAY_OUT_REC | CSA_RECIPIENT_INST_NO | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | CSA_BACK_LIMIT | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | CSA_BACK_LIMIT_SIGN | exp_Final.CSA_BACK_LIMIT_SIGN → exp_Convert.o_CSA_BACK_LIMIT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | CSA_BACK_BIWEEK_DED | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | CSA_BACK_BIWEEK_DED_SIGN | exp_Final.CSA_BACK_BIWEEK_DED_SIGN → exp_Convert.o_CSA_BACK_BIWEEK_DED_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | PCA_CONTRACT_LGTH | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | PCA_EFF_DATE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | PCA_NTE_DATE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | PCA_MAX_PAY | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | PCA_MAX_PAY_SIGN | exp_Final.PCA_MAX_PAY_SIGN → exp_Convert.o_PCA_MAX_PAY_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | PCA_BIWEEK_AMT | exp_Final.PCA_BIWEEK_AMT → exp_Convert.o_PCA_BIWEEK_AMT = ABS(PCA_BIWEEK_AMT) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(PCA_BIWEEK_AMT), 2)), '.', NULL), 7, '0') → exp_Init.PCA_BIWEEK_AMT → SQ_CPM_NEWPAY_TBL.PCA_BIWEEK_AMT → CPM_NEWPAY_TBL.PCA_BIWEEK_AMT | CPM_NEWPAY_TBL.PCA_BIWEEK_AMT |
| cdcskel_WS_PAY_OUT_REC | PCA_BIWEEK_AMT_SIGN | exp_Final.PCA_BIWEEK_AMT_SIGN → exp_Convert.o_PCA_BIWEEK_AMT_SIGN = IIF(SIGN(PCA_BIWEEK_AMT) = -1, '-', '+') → exp_Init.PCA_BIWEEK_AMT → SQ_CPM_NEWPAY_TBL.PCA_BIWEEK_AMT → CPM_NEWPAY_TBL.PCA_BIWEEK_AMT | CPM_NEWPAY_TBL.PCA_BIWEEK_AMT |
| cdcskel_WS_PAY_OUT_REC | PCA_CONTR_TO_DATE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | PCA_CONTR_TO_DATE_SIGN | exp_Final.PCA_CONTR_TO_DATE_SIGN → exp_Convert.o_PCA_CONTR_TO_DATE_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | REEMP_ANN_CDE | exp_Final.REEMP_ANN_CDE → exp_Convert.o_REEMP_ANN_CDE = REEMP_ANN_CDE → exp_Init.REEMP_ANN_CDE → SQ_CPM_NEWPAY_TBL.REEMP_ANN_CDE → CPM_NEWPAY_TBL.REEMP_ANN_CDE | CPM_NEWPAY_TBL.REEMP_ANN_CDE |
| cdcskel_WS_PAY_OUT_REC | REEMP_ANU_HR_RTE | exp_Final.REEMP_ANU_HR_RTE → exp_Convert.o_REEMP_ANU_HR_RTE = ABS(REEMP_ANU_HR_RTE) --0 --'00000' → exp_Init.REEMP_ANU_HR_RTE → SQ_CPM_NEWPAY_TBL.REEMP_ANU_HR_RTE → CPM_NEWPAY_TBL.REEMP_ANU_HR_RTE | CPM_NEWPAY_TBL.REEMP_ANU_HR_RTE |
| cdcskel_WS_PAY_OUT_REC | REEMP_ANU_HR_RTE_SIGN | exp_Final.REEMP_ANU_HR_RTE_SIGN → exp_Convert.o_REEMP_ANU_HR_RTE_SIGN = IIF(SIGN(REEMP_ANU_HR_RTE) = -1, '-', '+') → exp_Init.REEMP_ANU_HR_RTE → SQ_CPM_NEWPAY_TBL.REEMP_ANU_HR_RTE → CPM_NEWPAY_TBL.REEMP_ANU_HR_RTE | CPM_NEWPAY_TBL.REEMP_ANU_HR_RTE |
| cdcskel_WS_PAY_OUT_REC | EIC_STATUS_CODE | exp_Final.EIC_STATUS_CODE → exp_Convert.o_EIC_STATUS_CODE = '0' | literal/expression: '0' |
| cdcskel_WS_PAY_OUT_REC | ERR_FLAG | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | FLSA_CDE | exp_Final.FLSA_CDE → exp_Convert.o_FLSA_CDE = FLSA_CDE → exp_Init.FLSA_CDE → SQ_CPM_NEWPAY_TBL.FLSA_CDE → CPM_NEWPAY_TBL.FLSA_CDE | CPM_NEWPAY_TBL.FLSA_CDE |
| cdcskel_WS_PAY_OUT_REC | RPT_CDE | exp_Final.RPT_CDE → exp_Convert.o_RPT_CDE = LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(RPT_CDE), 0)), '.', NULL), 1, '0') → exp_Init.RPT_CDE → SQ_CPM_NEWPAY_TBL.RPT_CDE → CPM_NEWPAY_TBL.RPT_CDE | CPM_NEWPAY_TBL.RPT_CDE |
| cdcskel_WS_PAY_OUT_REC | RET_BAL_FWD_OLD | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | RET_BAL_FWD_OLD_SIGN | exp_Final.RET_BAL_FWD_OLD_SIGN → exp_Convert.o_RET_BAL_FWD_OLD_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | CPP_NO | exp_Final.CPP_NO → exp_Convert.o_CPP_NO = LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(CPP_NO, 0)), '.', NULL), 2, '0') → exp_Init.CPP_NO → SQ_CPM_NEWPAY_TBL.CPP_NO → CPM_NEWPAY_TBL.CPP_NO | CPM_NEWPAY_TBL.CPP_NO |
| cdcskel_WS_PAY_OUT_REC | CPP_BASE_PAY | exp_Final.CPP_BASE_PAY → exp_Convert.o_CPP_BASE_PAY = ABS(CPP_BASE_PAY) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(CPP_BASE_PAY), 2)), '.', NULL), 9, '0') → exp_Init.CPP_BASE_PAY → SQ_CPM_NEWPAY_TBL.CPP_BASE_PAY → CPM_NEWPAY_TBL.CPP_BASE_PAY | CPM_NEWPAY_TBL.CPP_BASE_PAY |
| cdcskel_WS_PAY_OUT_REC | CPP_BASE_PAY_SIGN | exp_Final.CPP_BASE_PAY_SIGN → exp_Convert.o_CPP_BASE_PAY_SIGN = IIF(SIGN(CPP_BASE_PAY) = -1, '-', '+') → exp_Init.CPP_BASE_PAY → SQ_CPM_NEWPAY_TBL.CPP_BASE_PAY → CPM_NEWPAY_TBL.CPP_BASE_PAY | CPM_NEWPAY_TBL.CPP_BASE_PAY |
| cdcskel_WS_PAY_OUT_REC | CPP_OT_PAY | exp_Final.CPP_OT_PAY → exp_Convert.o_CPP_OT_PAY = ABS(CPP_OT_PAY) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(CPP_OT_PAY), 2)), '.', NULL), 7, '0') → exp_Init.CPP_OT_PAY → SQ_CPM_NEWPAY_TBL.CPP_OT_PAY → CPM_NEWPAY_TBL.CPP_OT_PAY | CPM_NEWPAY_TBL.CPP_OT_PAY |
| cdcskel_WS_PAY_OUT_REC | CPP_OT_PAY_SIGN | exp_Final.CPP_OT_PAY_SIGN → exp_Convert.o_CPP_OT_PAY_SIGN = IIF(SIGN(CPP_OT_PAY) = -1, '-', '+') → exp_Init.CPP_OT_PAY → SQ_CPM_NEWPAY_TBL.CPP_OT_PAY → CPM_NEWPAY_TBL.CPP_OT_PAY | CPM_NEWPAY_TBL.CPP_OT_PAY |
| cdcskel_WS_PAY_OUT_REC | CPP_ND_PAY | exp_Final.CPP_ND_PAY → exp_Convert.o_CPP_ND_PAY = ABS(CPP_ND_PAY) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(CPP_ND_PAY), 2)), '.', NULL), 7, '0') → exp_Init.CPP_ND_PAY → SQ_CPM_NEWPAY_TBL.CPP_ND_PAY → CPM_NEWPAY_TBL.CPP_ND_PAY | CPM_NEWPAY_TBL.CPP_ND_PAY |
| cdcskel_WS_PAY_OUT_REC | CPP_ND_PAY_SIGN | exp_Final.CPP_ND_PAY_SIGN → exp_Convert.o_CPP_ND_PAY_SIGN = IIF(SIGN(CPP_ND_PAY) = -1, '-', '+') → exp_Init.CPP_ND_PAY → SQ_CPM_NEWPAY_TBL.CPP_ND_PAY → CPM_NEWPAY_TBL.CPP_ND_PAY | CPM_NEWPAY_TBL.CPP_ND_PAY |
| cdcskel_WS_PAY_OUT_REC | CPP_SD_PAY | exp_Final.CPP_SD_PAY → exp_Convert.o_CPP_SD_PAY = ABS(CPP_SD_PAY) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(CPP_SD_PAY), 2)), '.', NULL), 7, '0') → exp_Init.CPP_SD_PAY → SQ_CPM_NEWPAY_TBL.CPP_SD_PAY → CPM_NEWPAY_TBL.CPP_SD_PAY | CPM_NEWPAY_TBL.CPP_SD_PAY |
| cdcskel_WS_PAY_OUT_REC | CPP_SD_PAY_SIGN | exp_Final.CPP_SD_PAY_SIGN → exp_Convert.o_CPP_SD_PAY_SIGN = IIF(SIGN(CPP_SD_PAY) = -1, '-', '+') → exp_Init.CPP_SD_PAY → SQ_CPM_NEWPAY_TBL.CPP_SD_PAY → CPM_NEWPAY_TBL.CPP_SD_PAY | CPM_NEWPAY_TBL.CPP_SD_PAY |
| cdcskel_WS_PAY_OUT_REC | CPP_HOL_PAY | exp_Final.CPP_HOL_PAY → exp_Convert.o_CPP_HOL_PAY = ABS(CPP_HOL_PAY) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(CPP_HOL_PAY), 2)), '.', NULL), 7, '0') → exp_Init.CPP_HOL_PAY → SQ_CPM_NEWPAY_TBL.CPP_HOL_PAY → CPM_NEWPAY_TBL.CPP_HOL_PAY | CPM_NEWPAY_TBL.CPP_HOL_PAY |
| cdcskel_WS_PAY_OUT_REC | CPP_HOL_PAY_SIGN | exp_Final.CPP_HOL_PAY_SIGN → exp_Convert.o_CPP_HOL_PAY_SIGN = IIF(SIGN(CPP_HOL_PAY) = -1, '-', '+') → exp_Init.CPP_HOL_PAY → SQ_CPM_NEWPAY_TBL.CPP_HOL_PAY → CPM_NEWPAY_TBL.CPP_HOL_PAY | CPM_NEWPAY_TBL.CPP_HOL_PAY |
| cdcskel_WS_PAY_OUT_REC | CPP_PD_PAY | exp_Final.CPP_PD_PAY → exp_Convert.o_CPP_PD_PAY = ABS(CPP_PD_PAY) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(CPP_PD_PAY), 2)), '.', NULL), 7, '0') → exp_Init.CPP_PD_PAY → SQ_CPM_NEWPAY_TBL.CPP_PD_PAY → CPM_NEWPAY_TBL.CPP_PD_PAY | CPM_NEWPAY_TBL.CPP_PD_PAY |
| cdcskel_WS_PAY_OUT_REC | CPP_PD_PAY_SIGN | exp_Final.CPP_PD_PAY_SIGN → exp_Convert.o_CPP_PD_PAY_SIGN = IIF(SIGN(CPP_PD_PAY) = -1, '-', '+') → exp_Init.CPP_PD_PAY → SQ_CPM_NEWPAY_TBL.CPP_PD_PAY → CPM_NEWPAY_TBL.CPP_PD_PAY | CPM_NEWPAY_TBL.CPP_PD_PAY |
| cdcskel_WS_PAY_OUT_REC | CPP_COLA_PAY | exp_Final.CPP_COLA_PAY → exp_Convert.o_CPP_COLA_PAY = ABS(CPP_COLA_PAY) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(CPP_COLA_PAY), 2)), '.', NULL), 7, '0') → exp_Init.CPP_COLA_PAY → SQ_CPM_NEWPAY_TBL.CPP_COLA_PAY → CPM_NEWPAY_TBL.CPP_COLA_PAY | CPM_NEWPAY_TBL.CPP_COLA_PAY |
| cdcskel_WS_PAY_OUT_REC | CPP_COLA_PAY_SIGN | exp_Final.CPP_COLA_PAY_SIGN → exp_Convert.o_CPP_COLA_PAY_SIGN = IIF(SIGN(CPP_COLA_PAY) = -1, '-', '+') → exp_Init.CPP_COLA_PAY → SQ_CPM_NEWPAY_TBL.CPP_COLA_PAY → CPM_NEWPAY_TBL.CPP_COLA_PAY | CPM_NEWPAY_TBL.CPP_COLA_PAY |
| cdcskel_WS_PAY_OUT_REC | CPP_UNIF_ALLOW | exp_Final.CPP_UNIF_ALLOW → exp_Convert.o_CPP_UNIF_ALLOW = ABS(CPP_UNIF_ALLOW) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(CPP_UNIF_ALLOW), 2)), '.', NULL), 7, '0') → exp_Init.CPP_UNIF_ALLOW → SQ_CPM_NEWPAY_TBL.CPP_UNIF_ALLOW → CPM_NEWPAY_TBL.CPP_UNIF_ALLOW | CPM_NEWPAY_TBL.CPP_UNIF_ALLOW |
| cdcskel_WS_PAY_OUT_REC | CPP_UNIF_ALLOW_SIGN | exp_Final.CPP_UNIF_ALLOW_SIGN → exp_Convert.o_CPP_UNIF_ALLOW_SIGN = IIF(SIGN(CPP_UNIF_ALLOW) = -1, '-', '+') → exp_Init.CPP_UNIF_ALLOW → SQ_CPM_NEWPAY_TBL.CPP_UNIF_ALLOW → CPM_NEWPAY_TBL.CPP_UNIF_ALLOW | CPM_NEWPAY_TBL.CPP_UNIF_ALLOW |
| cdcskel_WS_PAY_OUT_REC | CPP_SEV_PAY | exp_Final.CPP_SEV_PAY → exp_Convert.o_CPP_SEV_PAY = ABS(CPP_SEV_PAY) → exp_Init.CPP_SEV_PAY → SQ_CPM_NEWPAY_TBL.CPP_SEV_PAY → CPM_NEWPAY_TBL.CPP_SEV_PAY | CPM_NEWPAY_TBL.CPP_SEV_PAY |
| cdcskel_WS_PAY_OUT_REC | CPP_SEV_PAY_SIGN | exp_Final.CPP_SEV_PAY_SIGN → exp_Convert.o_CPP_SEV_PAY_SIGN = IIF(SIGN(CPP_SEV_PAY) = -1, '-', '+') → exp_Init.CPP_SEV_PAY → SQ_CPM_NEWPAY_TBL.CPP_SEV_PAY → CPM_NEWPAY_TBL.CPP_SEV_PAY | CPM_NEWPAY_TBL.CPP_SEV_PAY |
| cdcskel_WS_PAY_OUT_REC | CPP_CASH_AWARD | exp_Final.CPP_CASH_AWARD → exp_Convert.o_CPP_CASH_AWARD = ABS(CPP_CASH_AWARD) → exp_Init.CPP_CASH_AWARD → SQ_CPM_NEWPAY_TBL.CPP_CASH_AWARD → CPM_NEWPAY_TBL.CPP_CASH_AWARD | CPM_NEWPAY_TBL.CPP_CASH_AWARD |
| cdcskel_WS_PAY_OUT_REC | CPP_CASH_AWARD_SIGN | exp_Final.CPP_CASH_AWARD_SIGN → exp_Convert.o_CPP_CASH_AWARD_SIGN = IIF(SIGN(CPP_CASH_AWARD) = -1, '-', '+') → exp_Init.CPP_CASH_AWARD → SQ_CPM_NEWPAY_TBL.CPP_CASH_AWARD → CPM_NEWPAY_TBL.CPP_CASH_AWARD | CPM_NEWPAY_TBL.CPP_CASH_AWARD |
| cdcskel_WS_PAY_OUT_REC | CPP_MP_CASH_AWARD | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | CPP_MP_CASH_AWARD_SIGN | exp_Final.CPP_MP_CASH_AWARD_SIGN → exp_Convert.o_CPP_MP_CASH_AWARD_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | CPP_LUMPSUM_LVPY | exp_Final.CPP_LUMPSUM_LVPY → exp_Convert.o_CPP_LUMPSUM_LVPY = IIF(NOT ISNULL(CPP_LUMPSUM_LVPY), IIF(v_CPP_LUMPSUM_LVPY_EXCEEDS_LIMIT_FLAG = TRUE, TO_DECIMAL( v_CPP_LUMPSUM_LVPY_BEFORE_DEC \|\| '.' \|\| v_CPP_LUMPSUM_LVPY_AFTER_DEC, 2), ABS(CPP_LUMPSUM_LVPY)), 0) → exp_Init.CPP_LUMPSUM_LVPY → SQ_CPM_NEWPAY_TBL.CPP_LUMPSUM_LVPY → CPM_NEWPAY_TBL.CPP_LUMPSUM_LVPY → exp_Convert.v_CPP_LUMPSUM_LVPY_EXCEEDS_LIMIT_FLAG = IIF( ABS(CPP_LUMPSUM_LVPY) > 99999.99, TRUE, FALSE) → exp_Convert.v_CPP_LUMPSUM_LVPY_BEFORE_DEC = SUBSTR(v_CPP_LUMPSUM_LVPY_CHAR, v_CPP_LUMPSUM_LVPY_POS_DEC -5, 5) → exp_Convert.v_CPP_LUMPSUM_LVPY_CHAR = TO_CHAR(TO_DECIMAL(CPP_LUMPSUM_LVPY, 2)) → exp_Convert.v_CPP_LUMPSUM_LVPY_POS_DEC = INSTR(v_CPP_LUMPSUM_LVPY_CHAR, '.') → exp_Convert.v_CPP_LUMPSUM_LVPY_AFTER_DEC = SUBSTR(v_CPP_LUMPSUM_LVPY_CHAR, v_CPP_LUMPSUM_LVPY_POS_DEC + 1, 2) | CPM_NEWPAY_TBL.CPP_LUMPSUM_LVPY |
| cdcskel_WS_PAY_OUT_REC | CPP_LUMPSUM_LVPY_SIGN | exp_Final.CPP_LUMPSUM_LVPY_SIGN → exp_Convert.o_CPP_LUMPSUM_LVPY_SIGN = IIF(SIGN(CPP_LUMPSUM_LVPY) = -1, '-', '+') → exp_Init.CPP_LUMPSUM_LVPY → SQ_CPM_NEWPAY_TBL.CPP_LUMPSUM_LVPY → CPM_NEWPAY_TBL.CPP_LUMPSUM_LVPY | CPM_NEWPAY_TBL.CPP_LUMPSUM_LVPY |
| cdcskel_WS_PAY_OUT_REC | CPP_OTHER_PAY | exp_Final.CPP_OTHER_PAY → exp_Convert.o_CPP_OTHER_PAY = ABS(CPP_OTHER_PAY) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(CPP_OTHER_PAY), 2)), '.', NULL), 9, '0') → exp_Init.CPP_OTHER_PAY → SQ_CPM_NEWPAY_TBL.CPP_OTHER_PAY → CPM_NEWPAY_TBL.CPP_OTHER_PAY | CPM_NEWPAY_TBL.CPP_OTHER_PAY |
| cdcskel_WS_PAY_OUT_REC | CPP_OTHER_PAY_SIGN | exp_Final.CPP_OTHER_PAY_SIGN → exp_Convert.o_CPP_OTHER_PAY_SIGN = IIF(SIGN(CPP_OTHER_PAY) = -1, '-', '+') → exp_Init.CPP_OTHER_PAY → SQ_CPM_NEWPAY_TBL.CPP_OTHER_PAY → CPM_NEWPAY_TBL.CPP_OTHER_PAY | CPM_NEWPAY_TBL.CPP_OTHER_PAY |
| cdcskel_WS_PAY_OUT_REC | CPP_GROSS_PAY | exp_Final.CPP_GROSS_PAY → exp_Convert.o_CPP_GROSS_PAY = ABS(CPP_GROSS_PAY) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(CPP_GROSS_PAY), 2)), '.', NULL), 9, '0') → exp_Init.CPP_GROSS_PAY → SQ_CPM_NEWPAY_TBL.CPP_GROSS_PAY → CPM_NEWPAY_TBL.CPP_GROSS_PAY | CPM_NEWPAY_TBL.CPP_GROSS_PAY |
| cdcskel_WS_PAY_OUT_REC | CPP_GROSS_PAY_SIGN | exp_Final.CPP_GROSS_PAY_SIGN → exp_Convert.o_CPP_GROSS_PAY_SIGN = IIF(SIGN(CPP_GROSS_PAY) = -1, '-', '+') → exp_Init.CPP_GROSS_PAY → SQ_CPM_NEWPAY_TBL.CPP_GROSS_PAY → CPM_NEWPAY_TBL.CPP_GROSS_PAY | CPM_NEWPAY_TBL.CPP_GROSS_PAY |
| cdcskel_WS_PAY_OUT_REC | CPP_PAY_NS_FWIT | exp_Final.CPP_PAY_NS_FWIT → exp_Convert.o_CPP_PAY_NS_FWIT = ABS(CPP_PAY_NS_FWIT) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(CPP_PAY_NS_FWIT), 2)), '.', NULL), 9, '0') → exp_Init.CPP_PAY_NS_FWIT → SQ_CPM_NEWPAY_TBL.CPP_PAY_NS_FWIT → CPM_NEWPAY_TBL.CPP_PAY_NS_FWIT | CPM_NEWPAY_TBL.CPP_PAY_NS_FWIT |
| cdcskel_WS_PAY_OUT_REC | CPP_PAY_NS_FWIT_SIGN | exp_Final.CPP_PAY_NS_FWIT_SIGN → exp_Convert.o_CPP_PAY_NS_FWIT_SIGN = IIF(SIGN(CPP_PAY_NS_FWIT) = -1, '-', '+') → exp_Init.CPP_PAY_NS_FWIT → SQ_CPM_NEWPAY_TBL.CPP_PAY_NS_FWIT → CPM_NEWPAY_TBL.CPP_PAY_NS_FWIT | CPM_NEWPAY_TBL.CPP_PAY_NS_FWIT |
| cdcskel_WS_PAY_OUT_REC | CPP_FED_WITH_DED | exp_Final.CPP_FED_WITH_DED → exp_Convert.o_CPP_FED_WITH_DED = ABS(CPP_FED_WITH_DED) → exp_Init.CPP_FED_WITH_DED → SQ_CPM_NEWPAY_TBL.CPP_FED_WITH_DED → CPM_NEWPAY_TBL.CPP_FED_WITH_DED | CPM_NEWPAY_TBL.CPP_FED_WITH_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_FED_WITH_DED_SIGN | exp_Final.CPP_FED_WITH_DED_SIGN → exp_Convert.o_CPP_FED_WITH_DED_SIGN = IIF(SIGN(CPP_FED_WITH_DED) = -1, '-', '+') → exp_Init.CPP_FED_WITH_DED → SQ_CPM_NEWPAY_TBL.CPP_FED_WITH_DED → CPM_NEWPAY_TBL.CPP_FED_WITH_DED | CPM_NEWPAY_TBL.CPP_FED_WITH_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_PAY_S_FEDTX | exp_Final.CPP_PAY_S_FEDTX → exp_Convert.o_CPP_PAY_S_FEDTX = ABS(CPP_PAY_S_FEDTX) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(CPP_PAY_S_FEDTX), 2)), '.', NULL), 9, '0') → exp_Init.CPP_PAY_S_FEDTX → SQ_CPM_NEWPAY_TBL.CPP_PAY_S_FEDTX → CPM_NEWPAY_TBL.CPP_PAY_S_FEDTX | CPM_NEWPAY_TBL.CPP_PAY_S_FEDTX |
| cdcskel_WS_PAY_OUT_REC | CPP_PAY_S_FEDTX_SIGN | exp_Final.CPP_PAY_S_FEDTX_SIGN → exp_Convert.o_CPP_PAY_S_FEDTX_SIGN = IIF(SIGN(CPP_PAY_S_FEDTX) = -1, '-', '+') → exp_Init.CPP_PAY_S_FEDTX → SQ_CPM_NEWPAY_TBL.CPP_PAY_S_FEDTX → CPM_NEWPAY_TBL.CPP_PAY_S_FEDTX | CPM_NEWPAY_TBL.CPP_PAY_S_FEDTX |
| cdcskel_WS_PAY_OUT_REC | CPP_CSR_DED | exp_Final.CPP_CSR_DED → exp_Convert.o_CPP_CSR_DED = ABS(CPP_CSR_DED) → exp_Init.CPP_CSR_DED → SQ_CPM_NEWPAY_TBL.CPP_CSR_DED → CPM_NEWPAY_TBL.CPP_CSR_DED | CPM_NEWPAY_TBL.CPP_CSR_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_CSR_DED_SIGN | exp_Final.CPP_CSR_DED_SIGN → exp_Convert.o_CPP_CSR_DED_SIGN = IIF(SIGN(CPP_CSR_DED) = -1, '-', '+') → exp_Init.CPP_CSR_DED → SQ_CPM_NEWPAY_TBL.CPP_CSR_DED → CPM_NEWPAY_TBL.CPP_CSR_DED | CPM_NEWPAY_TBL.CPP_CSR_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_CSR_EMPLR | exp_Final.CPP_CSR_EMPLR → exp_Convert.o_CPP_CSR_EMPLR = ABS(CPP_CSR_EMPLR) → exp_Init.CPP_CSR_EMPLR → SQ_CPM_NEWPAY_TBL.CPP_CSR_EMPLR → CPM_NEWPAY_TBL.CPP_CSR_EMPLR | CPM_NEWPAY_TBL.CPP_CSR_EMPLR |
| cdcskel_WS_PAY_OUT_REC | CPP_CSR_EMPLR_SIGN | exp_Final.CPP_CSR_EMPLR_SIGN → exp_Convert.o_CPP_CSR_EMPLR_SIGN = IIF(SIGN(CPP_CSR_EMPLR) = -1, '-', '+') → exp_Init.CPP_CSR_EMPLR → SQ_CPM_NEWPAY_TBL.CPP_CSR_EMPLR → CPM_NEWPAY_TBL.CPP_CSR_EMPLR | CPM_NEWPAY_TBL.CPP_CSR_EMPLR |
| cdcskel_WS_PAY_OUT_REC | CPP_PAY_S_CSR | exp_Final.CPP_PAY_S_CSR → exp_Convert.o_CPP_PAY_S_CSR = ABS(CPP_PAY_S_CSR) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(CPP_PAY_S_CSR), 2)), '.', NULL), 9, '0') → exp_Init.CPP_PAY_S_CSR → SQ_CPM_NEWPAY_TBL.CPP_PAY_S_CSR → CPM_NEWPAY_TBL.CPP_PAY_S_CSR | CPM_NEWPAY_TBL.CPP_PAY_S_CSR |
| cdcskel_WS_PAY_OUT_REC | CPP_PAY_S_CSR_SIGN | exp_Final.CPP_PAY_S_CSR_SIGN → exp_Convert.o_CPP_PAY_S_CSR_SIGN = IIF(SIGN(CPP_PAY_S_CSR) = -1, '-', '+') → exp_Init.CPP_PAY_S_CSR → SQ_CPM_NEWPAY_TBL.CPP_PAY_S_CSR → CPM_NEWPAY_TBL.CPP_PAY_S_CSR | CPM_NEWPAY_TBL.CPP_PAY_S_CSR |
| cdcskel_WS_PAY_OUT_REC | CPP_FICA_DED | exp_Final.CPP_FICA_DED → exp_Convert.o_CPP_FICA_DED = ABS(CPP_FICA_DED) → exp_Init.CPP_FICA_DED → SQ_CPM_NEWPAY_TBL.CPP_FICA_DED → CPM_NEWPAY_TBL.CPP_FICA_DED | CPM_NEWPAY_TBL.CPP_FICA_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_FICA_DED_SIGN | exp_Final.CPP_FICA_DED_SIGN → exp_Convert.o_CPP_FICA_DED_SIGN = IIF(SIGN(CPP_FICA_DED) = -1, '-', '+') → exp_Init.CPP_FICA_DED → SQ_CPM_NEWPAY_TBL.CPP_FICA_DED → CPM_NEWPAY_TBL.CPP_FICA_DED | CPM_NEWPAY_TBL.CPP_FICA_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_FICA_EMPLR | exp_Final.CPP_FICA_EMPLR → exp_Convert.o_CPP_FICA_EMPLR = ABS(CPP_FICA_EMPLR) → exp_Init.CPP_FICA_EMPLR → SQ_CPM_NEWPAY_TBL.CPP_FICA_EMPLR → CPM_NEWPAY_TBL.CPP_FICA_EMPLR | CPM_NEWPAY_TBL.CPP_FICA_EMPLR |
| cdcskel_WS_PAY_OUT_REC | CPP_FICA_EMPLR_SIGN | exp_Final.CPP_FICA_EMPLR_SIGN → exp_Convert.o_CPP_FICA_EMPLR_SIGN = IIF(SIGN(CPP_FICA_EMPLR) = -1, '-', '+') → exp_Init.CPP_FICA_EMPLR → SQ_CPM_NEWPAY_TBL.CPP_FICA_EMPLR → CPM_NEWPAY_TBL.CPP_FICA_EMPLR | CPM_NEWPAY_TBL.CPP_FICA_EMPLR |
| cdcskel_WS_PAY_OUT_REC | CPP_PAY_S_FICA | exp_Final.CPP_PAY_S_FICA → exp_Convert.o_CPP_PAY_S_FICA = ABS(CPP_PAY_S_FICA) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(CPP_PAY_S_FICA), 2)), '.', NULL), 9, '0') → exp_Init.CPP_PAY_S_FICA → SQ_CPM_NEWPAY_TBL.CPP_PAY_S_FICA → CPM_NEWPAY_TBL.CPP_PAY_S_FICA | CPM_NEWPAY_TBL.CPP_PAY_S_FICA |
| cdcskel_WS_PAY_OUT_REC | CPP_PAY_S_FICA_SIGN | exp_Final.CPP_PAY_S_FICA_SIGN → exp_Convert.o_CPP_PAY_S_FICA_SIGN = IIF(SIGN(CPP_PAY_S_FICA) = -1, '-', '+') → exp_Init.CPP_PAY_S_FICA → SQ_CPM_NEWPAY_TBL.CPP_PAY_S_FICA → CPM_NEWPAY_TBL.CPP_PAY_S_FICA | CPM_NEWPAY_TBL.CPP_PAY_S_FICA |
| cdcskel_WS_PAY_OUT_REC | CPP_MEDC_DED | exp_Final.CPP_MEDC_DED → exp_Convert.o_CPP_MEDC_DED = ABS(CPP_MEDC_DED) → exp_Init.CPP_MEDC_DED → SQ_CPM_NEWPAY_TBL.CPP_MEDC_DED → CPM_NEWPAY_TBL.CPP_MEDC_DED | CPM_NEWPAY_TBL.CPP_MEDC_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_MEDC_DED_SIGN | exp_Final.CPP_MEDC_DED_SIGN → exp_Convert.o_CPP_MEDC_DED_SIGN = IIF(SIGN(CPP_MEDC_DED) = -1, '-', '+') → exp_Init.CPP_MEDC_DED → SQ_CPM_NEWPAY_TBL.CPP_MEDC_DED → CPM_NEWPAY_TBL.CPP_MEDC_DED | CPM_NEWPAY_TBL.CPP_MEDC_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_MEDC_EMPLR | exp_Final.CPP_MEDC_EMPLR → exp_Convert.o_CPP_MEDC_EMPLR = ABS(CPP_MEDC_EMPLR) → exp_Init.CPP_MEDC_EMPLR → SQ_CPM_NEWPAY_TBL.CPP_MEDC_EMPLR → CPM_NEWPAY_TBL.CPP_MEDC_EMPLR | CPM_NEWPAY_TBL.CPP_MEDC_EMPLR |
| cdcskel_WS_PAY_OUT_REC | CPP_MEDC_EMPLR_SIGN | exp_Final.CPP_MEDC_EMPLR_SIGN → exp_Convert.o_CPP_MEDC_EMPLR_SIGN = IIF(SIGN(CPP_MEDC_EMPLR) = -1, '-', '+') → exp_Init.CPP_MEDC_EMPLR → SQ_CPM_NEWPAY_TBL.CPP_MEDC_EMPLR → CPM_NEWPAY_TBL.CPP_MEDC_EMPLR | CPM_NEWPAY_TBL.CPP_MEDC_EMPLR |
| cdcskel_WS_PAY_OUT_REC | CPP_PAY_S_MEDC | exp_Final.CPP_PAY_S_MEDC → exp_Convert.o_CPP_PAY_S_MEDC = ABS(CPP_PAY_S_MEDC) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(CPP_PAY_S_MEDC), 2)), '.', NULL), 9, '0') → exp_Init.CPP_PAY_S_MEDC → SQ_CPM_NEWPAY_TBL.CPP_PAY_S_MEDC → CPM_NEWPAY_TBL.CPP_PAY_S_MEDC | CPM_NEWPAY_TBL.CPP_PAY_S_MEDC |
| cdcskel_WS_PAY_OUT_REC | CPP_PAY_S_MEDC_SIGN | exp_Final.CPP_PAY_S_MEDC_SIGN → exp_Convert.o_CPP_PAY_S_MEDC_SIGN = IIF(SIGN(CPP_PAY_S_MEDC) = -1, '-', '+') → exp_Init.CPP_PAY_S_MEDC → SQ_CPM_NEWPAY_TBL.CPP_PAY_S_MEDC → CPM_NEWPAY_TBL.CPP_PAY_S_MEDC | CPM_NEWPAY_TBL.CPP_PAY_S_MEDC |
| cdcskel_WS_PAY_OUT_REC | CPP_FERS_EMP_DED | exp_Final.CPP_FERS_EMP_DED → exp_Convert.o_CPP_FERS_EMP_DED = ABS(CPP_FERS_EMP_DED) → exp_Init.CPP_FERS_EMP_DED → SQ_CPM_NEWPAY_TBL.CPP_FERS_EMP_DED → CPM_NEWPAY_TBL.CPP_FERS_EMP_DED | CPM_NEWPAY_TBL.CPP_FERS_EMP_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_FERS_EMP_DED_SIGN | exp_Final.CPP_FERS_EMP_DED_SIGN → exp_Convert.o_CPP_FERS_EMP_DED_SIGN = IIF(SIGN(CPP_FERS_EMP_DED) = -1, '-', '+') → exp_Init.CPP_FERS_EMP_DED → SQ_CPM_NEWPAY_TBL.CPP_FERS_EMP_DED → CPM_NEWPAY_TBL.CPP_FERS_EMP_DED | CPM_NEWPAY_TBL.CPP_FERS_EMP_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_FERS_AGY_DED | exp_Final.CPP_FERS_AGY_DED → exp_Convert.o_CPP_FERS_AGY_DED = ABS(CPP_FERS_AGY_DED) → exp_Init.CPP_FERS_AGY_DED → SQ_CPM_NEWPAY_TBL.CPP_FERS_AGY_DED → CPM_NEWPAY_TBL.CPP_FERS_AGY_DED | CPM_NEWPAY_TBL.CPP_FERS_AGY_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_FERS_AGY_DED_SIGN | exp_Final.CPP_FERS_AGY_DED_SIGN → exp_Convert.o_CPP_FERS_AGY_DED_SIGN = IIF(SIGN(CPP_FERS_AGY_DED) = -1, '-', '+') → exp_Init.CPP_FERS_AGY_DED → SQ_CPM_NEWPAY_TBL.CPP_FERS_AGY_DED → CPM_NEWPAY_TBL.CPP_FERS_AGY_DED | CPM_NEWPAY_TBL.CPP_FERS_AGY_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_FERS_PAY_SUB | exp_Final.CPP_FERS_PAY_SUB → exp_Convert.o_CPP_FERS_PAY_SUB = ABS(CPP_FERS_PAY_SUB) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(CPP_FERS_PAY_SUB), 2)), '.', NULL), 9, '0') → exp_Init.CPP_FERS_PAY_SUB → SQ_CPM_NEWPAY_TBL.CPP_FERS_PAY_SUB → CPM_NEWPAY_TBL.CPP_FERS_PAY_SUB | CPM_NEWPAY_TBL.CPP_FERS_PAY_SUB |
| cdcskel_WS_PAY_OUT_REC | CPP_FERS_PAY_SUB_SIGN | exp_Final.CPP_FERS_PAY_SUB_SIGN → exp_Convert.o_CPP_FERS_PAY_SUB_SIGN = IIF(SIGN(CPP_FERS_PAY_SUB) = -1, '-', '+') → exp_Init.CPP_FERS_PAY_SUB → SQ_CPM_NEWPAY_TBL.CPP_FERS_PAY_SUB → CPM_NEWPAY_TBL.CPP_FERS_PAY_SUB | CPM_NEWPAY_TBL.CPP_FERS_PAY_SUB |
| cdcskel_WS_PAY_OUT_REC | CPP_LEVY_DED | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | CPP_LEVY_DED_SIGN | exp_Final.CPP_LEVY_DED_SIGN → exp_Convert.o_CPP_LEVY_DED_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | CPP_ST_TAX_DED | exp_Final.CPP_ST_TAX_DED → exp_Convert.o_CPP_ST_TAX_DED = ABS(CPP_ST_TAX_DED) → exp_Init.CPP_ST_TAX_DED → SQ_CPM_NEWPAY_TBL.CPP_ST_TAX_DED → CPM_NEWPAY_TBL.CPP_ST_TAX_DED | CPM_NEWPAY_TBL.CPP_ST_TAX_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_ST_TAX_DED_SIGN | exp_Final.CPP_ST_TAX_DED_SIGN → exp_Convert.o_CPP_ST_TAX_DED_SIGN = IIF(SIGN(CPP_ST_TAX_DED) = -1, '-', '+') → exp_Init.CPP_ST_TAX_DED → SQ_CPM_NEWPAY_TBL.CPP_ST_TAX_DED → CPM_NEWPAY_TBL.CPP_ST_TAX_DED | CPM_NEWPAY_TBL.CPP_ST_TAX_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_CITY_DED | exp_Final.CPP_CITY_DED → exp_Convert.o_CPP_CITY_DED = ABS(CPP_CITY_DED) → exp_Init.CPP_CITY_DED → SQ_CPM_NEWPAY_TBL.CPP_CITY_DED → CPM_NEWPAY_TBL.CPP_CITY_DED | CPM_NEWPAY_TBL.CPP_CITY_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_CITY_DED_SIGN | exp_Final.CPP_CITY_DED_SIGN → exp_Convert.o_CPP_CITY_DED_SIGN = IIF(SIGN(CPP_CITY_DED) = -1, '-', '+') → exp_Init.CPP_CITY_DED → SQ_CPM_NEWPAY_TBL.CPP_CITY_DED → CPM_NEWPAY_TBL.CPP_CITY_DED | CPM_NEWPAY_TBL.CPP_CITY_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_HLTH_DED | exp_Final.CPP_HLTH_DED → exp_Convert.o_CPP_HLTH_DED = ABS(CPP_HLTH_DED) → exp_Init.CPP_HLTH_DED → SQ_CPM_NEWPAY_TBL.CPP_HLTH_DED → CPM_NEWPAY_TBL.CPP_HLTH_DED | CPM_NEWPAY_TBL.CPP_HLTH_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_HLTH_DED_SIGN | exp_Final.CPP_HLTH_DED_SIGN → exp_Convert.o_CPP_HLTH_DED_SIGN = IIF(SIGN(CPP_HLTH_DED) = -1, '-', '+') → exp_Init.CPP_HLTH_DED → SQ_CPM_NEWPAY_TBL.CPP_HLTH_DED → CPM_NEWPAY_TBL.CPP_HLTH_DED | CPM_NEWPAY_TBL.CPP_HLTH_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_HLTH_EMPLR | exp_Final.CPP_HLTH_EMPLR → exp_Convert.o_CPP_HLTH_EMPLR = ABS(CPP_HLTH_EMPLR) → exp_Init.CPP_HLTH_EMPLR → SQ_CPM_NEWPAY_TBL.CPP_HLTH_EMPLR → CPM_NEWPAY_TBL.CPP_HLTH_EMPLR | CPM_NEWPAY_TBL.CPP_HLTH_EMPLR |
| cdcskel_WS_PAY_OUT_REC | CPP_HLTH_EMPLR_SIGN | exp_Final.CPP_HLTH_EMPLR_SIGN → exp_Convert.o_CPP_HLTH_EMPLR_SIGN = IIF(SIGN(CPP_HLTH_EMPLR) = -1, '-', '+') → exp_Init.CPP_HLTH_EMPLR → SQ_CPM_NEWPAY_TBL.CPP_HLTH_EMPLR → CPM_NEWPAY_TBL.CPP_HLTH_EMPLR | CPM_NEWPAY_TBL.CPP_HLTH_EMPLR |
| cdcskel_WS_PAY_OUT_REC | CPP_BOND_DED | exp_Final.CPP_BOND_DED → exp_Convert.o_CPP_BOND_DED = ABS(CPP_BOND_DED) → exp_Init.CPP_BOND_DED → SQ_CPM_NEWPAY_TBL.CPP_BOND_DED → CPM_NEWPAY_TBL.CPP_BOND_DED | CPM_NEWPAY_TBL.CPP_BOND_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_BOND_DED_SIGN | exp_Final.CPP_BOND_DED_SIGN → exp_Convert.o_CPP_BOND_DED_SIGN = IIF(SIGN(CPP_BOND_DED) = -1, '-', '+') → exp_Init.CPP_BOND_DED → SQ_CPM_NEWPAY_TBL.CPP_BOND_DED → CPM_NEWPAY_TBL.CPP_BOND_DED | CPM_NEWPAY_TBL.CPP_BOND_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_LI_REG_DED | exp_Final.CPP_LI_REG_DED → exp_Convert.o_CPP_LI_REG_DED = ABS(CPP_LI_REG_DED) → exp_Init.CPP_LI_REG_DED → SQ_CPM_NEWPAY_TBL.CPP_LI_REG_DED → CPM_NEWPAY_TBL.CPP_LI_REG_DED | CPM_NEWPAY_TBL.CPP_LI_REG_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_LI_REG_DED_SIGN | exp_Final.CPP_LI_REG_DED_SIGN → exp_Convert.o_CPP_LI_REG_DED_SIGN = IIF(SIGN(CPP_LI_REG_DED) = -1, '-', '+') → exp_Init.CPP_LI_REG_DED → SQ_CPM_NEWPAY_TBL.CPP_LI_REG_DED → CPM_NEWPAY_TBL.CPP_LI_REG_DED | CPM_NEWPAY_TBL.CPP_LI_REG_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_LI_EMPLR | exp_Final.CPP_LI_EMPLR → exp_Convert.o_CPP_LI_EMPLR = ABS(CPP_LI_EMPLR) → exp_Init.CPP_LI_EMPLR → SQ_CPM_NEWPAY_TBL.CPP_LI_EMPLR → CPM_NEWPAY_TBL.CPP_LI_EMPLR | CPM_NEWPAY_TBL.CPP_LI_EMPLR |
| cdcskel_WS_PAY_OUT_REC | CPP_LI_EMPLR_SIGN | exp_Final.CPP_LI_EMPLR_SIGN → exp_Convert.o_CPP_LI_EMPLR_SIGN = IIF(SIGN(CPP_LI_EMPLR) = -1, '-', '+') → exp_Init.CPP_LI_EMPLR → SQ_CPM_NEWPAY_TBL.CPP_LI_EMPLR → CPM_NEWPAY_TBL.CPP_LI_EMPLR | CPM_NEWPAY_TBL.CPP_LI_EMPLR |
| cdcskel_WS_PAY_OUT_REC | CPP_LI_OPT_DED | exp_Final.CPP_LI_OPT_DED → exp_Convert.o_CPP_LI_OPT_DED = ABS(CPP_LI_OPT_DED) → exp_Init.CPP_LI_OPT_DED → SQ_CPM_NEWPAY_TBL.CPP_LI_OPT_DED → CPM_NEWPAY_TBL.CPP_LI_OPT_DED | CPM_NEWPAY_TBL.CPP_LI_OPT_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_LI_OPT_DED_SIGN | exp_Final.CPP_LI_OPT_DED_SIGN → exp_Convert.o_CPP_LI_OPT_DED_SIGN = IIF(SIGN(CPP_LI_OPT_DED) = -1, '-', '+') → exp_Init.CPP_LI_OPT_DED → SQ_CPM_NEWPAY_TBL.CPP_LI_OPT_DED → CPM_NEWPAY_TBL.CPP_LI_OPT_DED | CPM_NEWPAY_TBL.CPP_LI_OPT_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_FEGLI_OPTB | exp_Final.CPP_FEGLI_OPTB → exp_Convert.o_CPP_FEGLI_OPTB = ABS(CPP_FEGLI_OPTB) → exp_Init.CPP_FEGLI_OPTB → SQ_CPM_NEWPAY_TBL.CPP_FEGLI_OPTB → CPM_NEWPAY_TBL.CPP_FEGLI_OPTB | CPM_NEWPAY_TBL.CPP_FEGLI_OPTB |
| cdcskel_WS_PAY_OUT_REC | CPP_FEGLI_OPTB_SIGN | exp_Final.CPP_FEGLI_OPTB_SIGN → exp_Convert.o_CPP_FEGLI_OPTB_SIGN = IIF(SIGN(CPP_FEGLI_OPTB) = -1, '-', '+') → exp_Init.CPP_FEGLI_OPTB → SQ_CPM_NEWPAY_TBL.CPP_FEGLI_OPTB → CPM_NEWPAY_TBL.CPP_FEGLI_OPTB | CPM_NEWPAY_TBL.CPP_FEGLI_OPTB |
| cdcskel_WS_PAY_OUT_REC | CPP_FEGLI_OPTC | exp_Final.CPP_FEGLI_OPTC → exp_Convert.o_CPP_FEGLI_OPTC = ABS(CPP_FEGLI_OPTC) → exp_Init.CPP_FEGLI_OPTC → SQ_CPM_NEWPAY_TBL.CPP_FEGLI_OPTC → CPM_NEWPAY_TBL.CPP_FEGLI_OPTC | CPM_NEWPAY_TBL.CPP_FEGLI_OPTC |
| cdcskel_WS_PAY_OUT_REC | CPP_FEGLI_OPTC_SIGN | exp_Final.CPP_FEGLI_OPTC_SIGN → exp_Convert.o_CPP_FEGLI_OPTC_SIGN = IIF(SIGN(CPP_FEGLI_OPTC) = -1, '-', '+') → exp_Init.CPP_FEGLI_OPTC → SQ_CPM_NEWPAY_TBL.CPP_FEGLI_OPTC → CPM_NEWPAY_TBL.CPP_FEGLI_OPTC | CPM_NEWPAY_TBL.CPP_FEGLI_OPTC |
| cdcskel_WS_PAY_OUT_REC | CPP_CHAR_DED | exp_Final.CPP_CHAR_DED → exp_Convert.o_CPP_CHAR_DED = ABS(CPP_CHAR_DED) → exp_Init.CPP_CHAR_DED → SQ_CPM_NEWPAY_TBL.CPP_CHAR_DED → CPM_NEWPAY_TBL.CPP_CHAR_DED | CPM_NEWPAY_TBL.CPP_CHAR_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_CHAR_DED_SIGN | exp_Final.CPP_CHAR_DED_SIGN → exp_Convert.o_CPP_CHAR_DED_SIGN = IIF(SIGN(CPP_CHAR_DED) = -1, '-', '+') → exp_Init.CPP_CHAR_DED → SQ_CPM_NEWPAY_TBL.CPP_CHAR_DED → CPM_NEWPAY_TBL.CPP_CHAR_DED | CPM_NEWPAY_TBL.CPP_CHAR_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_UNION_1_DED | exp_Final.CPP_UNION_1_DED → exp_Convert.o_CPP_UNION_1_DED = ABS(CPP_UNION_1_DED) → exp_Init.CPP_UNION_1_DED → SQ_CPM_NEWPAY_TBL.CPP_UNION_1_DED → CPM_NEWPAY_TBL.CPP_UNION_1_DED | CPM_NEWPAY_TBL.CPP_UNION_1_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_UNION_1_DED_SIGN | exp_Final.CPP_UNION_1_DED_SIGN → exp_Convert.o_CPP_UNION_1_DED_SIGN = IIF(SIGN(CPP_UNION_1_DED) = -1, '-', '+') → exp_Init.CPP_UNION_1_DED → SQ_CPM_NEWPAY_TBL.CPP_UNION_1_DED → CPM_NEWPAY_TBL.CPP_UNION_1_DED | CPM_NEWPAY_TBL.CPP_UNION_1_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_ALT_1_DED | exp_Final.CPP_ALT_1_DED → exp_Convert.o_CPP_ALT_1_DED = ABS(CPP_ALT_1_DED) → exp_Init.CPP_ALT_1_DED → SQ_CPM_NEWPAY_TBL.CPP_ALT_1_DED → CPM_NEWPAY_TBL.CPP_ALT_1_DED | CPM_NEWPAY_TBL.CPP_ALT_1_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_ALT_1_DED_SIGN | exp_Final.CPP_ALT_1_DED_SIGN → exp_Convert.o_CPP_ALT_1_DED_SIGN = IIF(SIGN(CPP_ALT_1_DED) = -1, '-', '+') --'+' → exp_Init.CPP_ALT_1_DED → SQ_CPM_NEWPAY_TBL.CPP_ALT_1_DED → CPM_NEWPAY_TBL.CPP_ALT_1_DED | CPM_NEWPAY_TBL.CPP_ALT_1_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_ALT_2_DED | exp_Final.CPP_ALT_2_DED → exp_Convert.o_CPP_ALT_2_DED = ABS(CPP_ALT_2_DED) → exp_Init.CPP_ALT_2_DED → SQ_CPM_NEWPAY_TBL.CPP_ALT_2_DED → CPM_NEWPAY_TBL.CPP_ALT_2_DED | CPM_NEWPAY_TBL.CPP_ALT_2_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_ALT_2_DED_SIGN | exp_Final.CPP_ALT_2_DED_SIGN → exp_Convert.o_CPP_ALT_2_DED_SIGN = IIF(SIGN(CPP_ALT_2_DED) = -1, '-', '+') --'+' → exp_Init.CPP_ALT_2_DED → SQ_CPM_NEWPAY_TBL.CPP_ALT_2_DED → CPM_NEWPAY_TBL.CPP_ALT_2_DED | CPM_NEWPAY_TBL.CPP_ALT_2_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_NET_ALT_DED | exp_Final.CPP_NET_ALT_DED → exp_Convert.o_CPP_NET_ALT_DED = ABS(CPP_NET_ALT_DED) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(CPP_NET_ALT_DED), 2)), '.', NULL), 9, '0') → exp_Init.CPP_NET_ALT_DED → SQ_CPM_NEWPAY_TBL.CPP_NET_ALT_DED → CPM_NEWPAY_TBL.CPP_NET_ALT_DED | CPM_NEWPAY_TBL.CPP_NET_ALT_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_NET_ALT_DED_SIGN | exp_Final.CPP_NET_ALT_DED_SIGN → exp_Convert.o_CPP_NET_ALT_DED_SIGN = IIF(SIGN(CPP_NET_ALT_DED) = -1, '-', '+') → exp_Init.CPP_NET_ALT_DED → SQ_CPM_NEWPAY_TBL.CPP_NET_ALT_DED → CPM_NEWPAY_TBL.CPP_NET_ALT_DED | CPM_NEWPAY_TBL.CPP_NET_ALT_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_REF_DED_CDE | exp_Final.CPP_REF_DED_CDE → exp_Convert.o_CPP_REF_DED_CDE = CPP_REF_DED_CDE → exp_Init.CPP_REF_DED_CDE → SQ_CPM_NEWPAY_TBL.CPP_REF_DED_CDE → CPM_NEWPAY_TBL.CPP_REF_DED_CDE | CPM_NEWPAY_TBL.CPP_REF_DED_CDE |
| cdcskel_WS_PAY_OUT_REC | CPP_REF_DED_AMT | exp_Final.CPP_REF_DED_AMT → exp_Convert.o_CPP_REF_DED_AMT = ABS(CPP_REF_DED_AMT) → exp_Init.CPP_REF_DED_AMT → SQ_CPM_NEWPAY_TBL.CPP_REF_DED_AMT → CPM_NEWPAY_TBL.CPP_REF_DED_AMT | CPM_NEWPAY_TBL.CPP_REF_DED_AMT |
| cdcskel_WS_PAY_OUT_REC | CPP_REF_DED_AMT_SIGN | exp_Final.CPP_REF_DED_AMT_SIGN → exp_Convert.o_CPP_REF_DED_AMT_SIGN = IIF(SIGN(CPP_REF_DED_AMT) = -1, '-', '+') → exp_Init.CPP_REF_DED_AMT → SQ_CPM_NEWPAY_TBL.CPP_REF_DED_AMT → CPM_NEWPAY_TBL.CPP_REF_DED_AMT | CPM_NEWPAY_TBL.CPP_REF_DED_AMT |
| cdcskel_WS_PAY_OUT_REC | CPP_QUARTERS_DED | exp_Final.CPP_QUARTERS_DED → exp_Convert.o_CPP_QUARTERS_DED = ABS(CPP_QUARTERS_DED) → exp_Init.CPP_QUARTERS_DED → SQ_CPM_NEWPAY_TBL.CPP_QUARTERS_DED → CPM_NEWPAY_TBL.CPP_QUARTERS_DED | CPM_NEWPAY_TBL.CPP_QUARTERS_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_QUARTERS_DED_SIGN | exp_Final.CPP_QUARTERS_DED_SIGN → exp_Convert.o_CPP_QUARTERS_DED_SIGN = IIF(SIGN(CPP_QUARTERS_DED) = -1, '-', '+') → exp_Init.CPP_QUARTERS_DED → SQ_CPM_NEWPAY_TBL.CPP_QUARTERS_DED → CPM_NEWPAY_TBL.CPP_QUARTERS_DED | CPM_NEWPAY_TBL.CPP_QUARTERS_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_SUBSIST_DED | exp_Final.CPP_SUBSIST_DED → exp_Convert.o_CPP_SUBSIST_DED = ABS(CPP_SUBSIST_DED) → exp_Init.CPP_SUBSIST_DED → SQ_CPM_NEWPAY_TBL.CPP_SUBSIST_DED → CPM_NEWPAY_TBL.CPP_SUBSIST_DED | CPM_NEWPAY_TBL.CPP_SUBSIST_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_SUBSIST_DED_SIGN | exp_Final.CPP_SUBSIST_DED_SIGN → exp_Convert.o_CPP_SUBSIST_DED_SIGN = IIF(SIGN(CPP_SUBSIST_DED) = -1, '-', '+') → exp_Init.CPP_SUBSIST_DED → SQ_CPM_NEWPAY_TBL.CPP_SUBSIST_DED → CPM_NEWPAY_TBL.CPP_SUBSIST_DED | CPM_NEWPAY_TBL.CPP_SUBSIST_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_LAUNDRY_DED | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | CPP_LAUNDRY_DED_SIGN | exp_Final.CPP_LAUNDRY_DED_SIGN → exp_Convert.o_CPP_LAUNDRY_DED_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | CPP_NET_PAY | exp_Final.CPP_NET_PAY → exp_Convert.o_CPP_NET_PAY = ABS(CPP_NET_PAY) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(CPP_NET_PAY), 2)), '.', NULL), 9, '0') → exp_Init.CPP_NET_PAY → SQ_CPM_NEWPAY_TBL.CPP_NET_PAY → CPM_NEWPAY_TBL.CPP_NET_PAY | CPM_NEWPAY_TBL.CPP_NET_PAY |
| cdcskel_WS_PAY_OUT_REC | CPP_NET_PAY_SIGN | exp_Final.CPP_NET_PAY_SIGN → exp_Convert.o_CPP_NET_PAY_SIGN = IIF(SIGN(CPP_NET_PAY) = -1, '-', '+') → exp_Init.CPP_NET_PAY → SQ_CPM_NEWPAY_TBL.CPP_NET_PAY → CPM_NEWPAY_TBL.CPP_NET_PAY | CPM_NEWPAY_TBL.CPP_NET_PAY |
| cdcskel_WS_PAY_OUT_REC | CPP_CSA_DED | exp_Final.CPP_CSA_DED → exp_Convert.o_CPP_CSA_DED = ABS(CPP_CSA_DED) → exp_Init.CPP_CSA_DED → SQ_CPM_NEWPAY_TBL.CPP_CSA_DED → CPM_NEWPAY_TBL.CPP_CSA_DED | CPM_NEWPAY_TBL.CPP_CSA_DED |
| cdcskel_WS_PAY_OUT_REC | CPP_CSA_DED_SIGN | exp_Final.CPP_CSA_DED_SIGN → exp_Convert.o_CPP_CSA_DED_SIGN = IIF(SIGN(CPP_CSA_DED) = -1, '-', '+') → exp_Init.CPP_CSA_DED → SQ_CPM_NEWPAY_TBL.CPP_CSA_DED → CPM_NEWPAY_TBL.CPP_CSA_DED | CPM_NEWPAY_TBL.CPP_CSA_DED |
| cdcskel_WS_PAY_OUT_REC | EIC_CPP_PAY | exp_Final.EIC_CPP_PAY → exp_Convert.o_EIC_CPP_PAY = ABS(EIC_CPP_PAY) → exp_Init.EIC_CPP_PAY → SQ_CPM_NEWPAY_TBL.EIC_CPP_PAY → CPM_NEWPAY_TBL.EIC_CPP_PAY | CPM_NEWPAY_TBL.EIC_CPP_PAY |
| cdcskel_WS_PAY_OUT_REC | EIC_CPP_PAY_SIGN | exp_Final.EIC_CPP_PAY_SIGN → exp_Convert.o_EIC_CPP_PAY_SIGN = IIF(SIGN(EIC_CPP_PAY) = -1, '-', '+') → exp_Init.EIC_CPP_PAY → SQ_CPM_NEWPAY_TBL.EIC_CPP_PAY → CPM_NEWPAY_TBL.EIC_CPP_PAY | CPM_NEWPAY_TBL.EIC_CPP_PAY |
| cdcskel_WS_PAY_OUT_REC | PCA_CPP_PAY | exp_Final.PCA_CPP_PAY → exp_Convert.o_PCA_CPP_PAY = ABS(PCA_CPP_PAY) → exp_Init.PCA_CPP_PAY → SQ_CPM_NEWPAY_TBL.PCA_CPP_PAY → CPM_NEWPAY_TBL.PCA_CPP_PAY | CPM_NEWPAY_TBL.PCA_CPP_PAY |
| cdcskel_WS_PAY_OUT_REC | PCA_CPP_PAY_SIGN | exp_Final.PCA_CPP_PAY_SIGN → exp_Convert.o_PCA_CPP_PAY_SIGN = IIF(SIGN(PCA_CPP_PAY) = -1, '-', '+') → exp_Init.PCA_CPP_PAY → SQ_CPM_NEWPAY_TBL.PCA_CPP_PAY → CPM_NEWPAY_TBL.PCA_CPP_PAY | CPM_NEWPAY_TBL.PCA_CPP_PAY |
| cdcskel_WS_PAY_OUT_REC | CPP_TSPA_PAY_SUB | exp_Final.CPP_TSPA_PAY_SUB → exp_Convert.o_CPP_TSPA_PAY_SUB = ABS(CPP_TSPA_PAY_SUB) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(CPP_TSPA_PAY_SUB), 2)), '.', NULL), 9, '0') → exp_Init.CPP_TSPA_PAY_SUB → SQ_CPM_NEWPAY_TBL.CPP_TSPA_PAY_SUB → CPM_NEWPAY_TBL.CPP_TSPA_PAY_SUB | CPM_NEWPAY_TBL.CPP_TSPA_PAY_SUB |
| cdcskel_WS_PAY_OUT_REC | CPP_TSPA_PAY_SUB_SIGN | exp_Final.CPP_TSPA_PAY_SUB_SIGN → exp_Convert.o_CPP_TSPA_PAY_SUB_SIGN = IIF(SIGN(CPP_TSPA_PAY_SUB) = -1, '-', '+') → exp_Init.CPP_TSPA_PAY_SUB → SQ_CPM_NEWPAY_TBL.CPP_TSPA_PAY_SUB → CPM_NEWPAY_TBL.CPP_TSPA_PAY_SUB | CPM_NEWPAY_TBL.CPP_TSPA_PAY_SUB |
| cdcskel_WS_PAY_OUT_REC | CPP_TSPG_GBADIST | exp_Final.CPP_TSPG_GBADIST → exp_Convert.o_CPP_TSPG_GBADIST = ABS(CPP_TSPG_GBADIST) → exp_Init.CPP_TSPG_GBADIST → SQ_CPM_NEWPAY_TBL.CPP_TSPG_GBADIST → CPM_NEWPAY_TBL.CPP_TSPG_GBADIST | CPM_NEWPAY_TBL.CPP_TSPG_GBADIST |
| cdcskel_WS_PAY_OUT_REC | CPP_TSPG_GBADIST_SIGN | exp_Final.CPP_TSPG_GBADIST_SIGN → exp_Convert.o_CPP_TSPG_GBADIST_SIGN = IIF(SIGN(CPP_TSPG_GBADIST) = -1, '-', '+') → exp_Init.CPP_TSPG_GBADIST → SQ_CPM_NEWPAY_TBL.CPP_TSPG_GBADIST → CPM_NEWPAY_TBL.CPP_TSPG_GBADIST | CPM_NEWPAY_TBL.CPP_TSPG_GBADIST |
| cdcskel_WS_PAY_OUT_REC | CPP_TSPG_EADIST | exp_Final.CPP_TSPG_EADIST → exp_Convert.o_CPP_TSPG_EADIST = ABS(CPP_TSPG_EADIST) → exp_Init.CPP_TSPG_EADIST → SQ_CPM_NEWPAY_TBL.CPP_TSPG_EADIST → CPM_NEWPAY_TBL.CPP_TSPG_EADIST | CPM_NEWPAY_TBL.CPP_TSPG_EADIST |
| cdcskel_WS_PAY_OUT_REC | CPP_TSPG_EADIST_SIGN | exp_Final.CPP_TSPG_EADIST_SIGN → exp_Convert.o_CPP_TSPG_EADIST_SIGN = IIF(SIGN(CPP_TSPG_EADIST) = -1, '-', '+') → exp_Init.CPP_TSPG_EADIST → SQ_CPM_NEWPAY_TBL.CPP_TSPG_EADIST → CPM_NEWPAY_TBL.CPP_TSPG_EADIST | CPM_NEWPAY_TBL.CPP_TSPG_EADIST |
| cdcskel_WS_PAY_OUT_REC | CPP_TSPG_GMADIST | exp_Final.CPP_TSPG_GMADIST → exp_Convert.o_CPP_TSPG_GMADIST = ABS(CPP_TSPG_GMADIST) → exp_Init.CPP_TSPG_GMADIST → SQ_CPM_NEWPAY_TBL.CPP_TSPG_GMADIST → CPM_NEWPAY_TBL.CPP_TSPG_GMADIST | CPM_NEWPAY_TBL.CPP_TSPG_GMADIST |
| cdcskel_WS_PAY_OUT_REC | CPP_TSPG_GMADIST_SIGN | exp_Final.CPP_TSPG_GMADIST_SIGN → exp_Convert.o_CPP_TSPG_GMADIST_SIGN = IIF(SIGN(CPP_TSPG_GMADIST) = -1, '-', '+') → exp_Init.CPP_TSPG_GMADIST → SQ_CPM_NEWPAY_TBL.CPP_TSPG_GMADIST → CPM_NEWPAY_TBL.CPP_TSPG_GMADIST | CPM_NEWPAY_TBL.CPP_TSPG_GMADIST |
| cdcskel_WS_PAY_OUT_REC | CPP_TSPG_PRADIST | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | CPP_TSPG_PRADIST_SIGN | exp_Final.CPP_TSPG_PRADIST_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | CPP_TSPF_GBADIST | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | CPP_TSPF_GBADIST_SIGN | exp_Final.CPP_TSPF_GBADIST_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | CPP_TSPF_EADIST | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | CPP_TSPF_EADIST_SIGN | exp_Final.CPP_TSPF_EADIST_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | CPP_TSPF_GMADIST | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | CPP_TSPF_GMADIST_SIGN | exp_Final.CPP_TSPF_GMADIST_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | CPP_TSPF_PRADIST | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | CPP_TSPF_PRADIST_SIGN | exp_Final.CPP_TSPF_PRADIST_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | CPP_TSPC_GBADIST | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | CPP_TSPC_GBADIST_SIGN | exp_Final.CPP_TSPC_GBADIST_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | CPP_TSPC_EADIST | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | CPP_TSPC_EADIST_SIGN | exp_Final.CPP_TSPC_EADIST_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | CPP_TSPC_GMADIST | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | CPP_TSPC_GMADIST_SIGN | exp_Final.CPP_TSPC_GMADIST_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | CPP_TSPC_PRADIST | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | CPP_TSPC_PRADIST_SIGN | exp_Final.CPP_TSPC_PRADIST_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | YTD_BASE_PAY | exp_Final.YTD_BASE_PAY → exp_Convert.o_YTD_BASE_PAY = ABS(YTD_BASE_PAY) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(YTD_BASE_PAY), 2)), '.', NULL), 9, '0') → exp_Init.YTD_BASE_PAY → SQ_CPM_NEWPAY_TBL.YTD_BASE_PAY → CPM_NEWPAY_TBL.YTD_BASE_PAY | CPM_NEWPAY_TBL.YTD_BASE_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_BASE_PAY_SIGN | exp_Final.YTD_BASE_PAY_SIGN → exp_Convert.o_YTD_BASE_PAY_SIGN = IIF(SIGN(YTD_BASE_PAY) = -1, '-', '+') → exp_Init.YTD_BASE_PAY → SQ_CPM_NEWPAY_TBL.YTD_BASE_PAY → CPM_NEWPAY_TBL.YTD_BASE_PAY | CPM_NEWPAY_TBL.YTD_BASE_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_OT_PAY | exp_Final.YTD_OT_PAY → exp_Convert.o_YTD_OT_PAY = ABS(YTD_OT_PAY) → exp_Init.YTD_OT_PAY → SQ_CPM_NEWPAY_TBL.YTD_OT_PAY → CPM_NEWPAY_TBL.YTD_OT_PAY | CPM_NEWPAY_TBL.YTD_OT_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_OT_PAY_SIGN | exp_Final.YTD_OT_PAY_SIGN → exp_Convert.o_YTD_OT_PAY_SIGN = IIF(SIGN(YTD_OT_PAY) = -1, '-', '+') → exp_Init.YTD_OT_PAY → SQ_CPM_NEWPAY_TBL.YTD_OT_PAY → CPM_NEWPAY_TBL.YTD_OT_PAY | CPM_NEWPAY_TBL.YTD_OT_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_ND_PAY | exp_Final.YTD_ND_PAY → exp_Convert.o_YTD_ND_PAY = ABS(YTD_ND_PAY) → exp_Init.YTD_ND_PAY → SQ_CPM_NEWPAY_TBL.YTD_ND_PAY → CPM_NEWPAY_TBL.YTD_ND_PAY | CPM_NEWPAY_TBL.YTD_ND_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_ND_PAY_SIGN | exp_Final.YTD_ND_PAY_SIGN → exp_Convert.o_YTD_ND_PAY_SIGN = IIF(SIGN(YTD_ND_PAY) = -1, '-', '+') → exp_Init.YTD_ND_PAY → SQ_CPM_NEWPAY_TBL.YTD_ND_PAY → CPM_NEWPAY_TBL.YTD_ND_PAY | CPM_NEWPAY_TBL.YTD_ND_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_SD_PAY | exp_Final.YTD_SD_PAY → exp_Convert.o_YTD_SD_PAY = ABS(YTD_SD_PAY) → exp_Init.YTD_SD_PAY → SQ_CPM_NEWPAY_TBL.YTD_SD_PAY → CPM_NEWPAY_TBL.YTD_SD_PAY | CPM_NEWPAY_TBL.YTD_SD_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_SD_PAY_SIGN | exp_Final.YTD_SD_PAY_SIGN → exp_Convert.o_YTD_SD_PAY_SIGN = IIF(SIGN(YTD_SD_PAY) = -1, '-', '+') → exp_Init.YTD_SD_PAY → SQ_CPM_NEWPAY_TBL.YTD_SD_PAY → CPM_NEWPAY_TBL.YTD_SD_PAY | CPM_NEWPAY_TBL.YTD_SD_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_HOL_PAY | exp_Final.YTD_HOL_PAY → exp_Convert.o_YTD_HOL_PAY = ABS(YTD_HOL_PAY) → exp_Init.YTD_HOL_PAY → SQ_CPM_NEWPAY_TBL.YTD_HOL_PAY → CPM_NEWPAY_TBL.YTD_HOL_PAY | CPM_NEWPAY_TBL.YTD_HOL_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_HOL_PAY_SIGN | exp_Final.YTD_HOL_PAY_SIGN → exp_Convert.o_YTD_HOL_PAY_SIGN = IIF(SIGN(YTD_HOL_PAY) = -1, '-', '+') → exp_Init.YTD_HOL_PAY → SQ_CPM_NEWPAY_TBL.YTD_HOL_PAY → CPM_NEWPAY_TBL.YTD_HOL_PAY | CPM_NEWPAY_TBL.YTD_HOL_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_PD_PAY | exp_Final.YTD_PD_PAY → exp_Convert.o_YTD_PD_PAY = ABS(YTD_PD_PAY) → exp_Init.YTD_PD_PAY → SQ_CPM_NEWPAY_TBL.YTD_PD_PAY → CPM_NEWPAY_TBL.YTD_PD_PAY | CPM_NEWPAY_TBL.YTD_PD_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_PD_PAY_SIGN | exp_Final.YTD_PD_PAY_SIGN → exp_Convert.o_YTD_PD_PAY_SIGN = IIF(SIGN(YTD_PD_PAY) = -1, '-', '+') → exp_Init.YTD_PD_PAY → SQ_CPM_NEWPAY_TBL.YTD_PD_PAY → CPM_NEWPAY_TBL.YTD_PD_PAY | CPM_NEWPAY_TBL.YTD_PD_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_COLA_PAY | exp_Final.YTD_COLA_PAY → exp_Convert.o_YTD_COLA_PAY = ABS(YTD_COLA_PAY) → exp_Init.YTD_COLA_PAY → SQ_CPM_NEWPAY_TBL.YTD_COLA_PAY → CPM_NEWPAY_TBL.YTD_COLA_PAY | CPM_NEWPAY_TBL.YTD_COLA_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_COLA_PAY_SIGN | exp_Final.YTD_COLA_PAY_SIGN → exp_Convert.o_YTD_COLA_PAY_SIGN = IIF(SIGN(YTD_COLA_PAY) = -1, '-', '+') → exp_Init.YTD_COLA_PAY → SQ_CPM_NEWPAY_TBL.YTD_COLA_PAY → CPM_NEWPAY_TBL.YTD_COLA_PAY | CPM_NEWPAY_TBL.YTD_COLA_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_UNIF_ALLOW | exp_Final.YTD_UNIF_ALLOW → exp_Convert.o_YTD_UNIF_ALLOW = ABS(YTD_UNIF_ALLOW) → exp_Init.YTD_UNIF_ALLOW → SQ_CPM_NEWPAY_TBL.YTD_UNIF_ALLOW → CPM_NEWPAY_TBL.YTD_UNIF_ALLOW | CPM_NEWPAY_TBL.YTD_UNIF_ALLOW |
| cdcskel_WS_PAY_OUT_REC | YTD_UNIF_ALLOW_SIGN | exp_Final.YTD_UNIF_ALLOW_SIGN → exp_Convert.o_YTD_UNIF_ALLOW_SIGN = IIF(SIGN(YTD_UNIF_ALLOW) = -1, '-', '+') → exp_Init.YTD_UNIF_ALLOW → SQ_CPM_NEWPAY_TBL.YTD_UNIF_ALLOW → CPM_NEWPAY_TBL.YTD_UNIF_ALLOW | CPM_NEWPAY_TBL.YTD_UNIF_ALLOW |
| cdcskel_WS_PAY_OUT_REC | YTD_SEV_PAY | exp_Final.YTD_SEV_PAY → exp_Convert.o_YTD_SEV_PAY = ABS(YTD_SEV_PAY) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(YTD_SEV_PAY), 2)), '.', NULL), 9, '0') → exp_Init.YTD_SEV_PAY → SQ_CPM_NEWPAY_TBL.YTD_SEV_PAY → CPM_NEWPAY_TBL.YTD_SEV_PAY | CPM_NEWPAY_TBL.YTD_SEV_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_SEV_PAY_SIGN | exp_Final.YTD_SEV_PAY_SIGN → exp_Convert.o_YTD_SEV_PAY_SIGN = IIF(SIGN(YTD_SEV_PAY) = -1, '-', '+') → exp_Init.YTD_SEV_PAY → SQ_CPM_NEWPAY_TBL.YTD_SEV_PAY → CPM_NEWPAY_TBL.YTD_SEV_PAY | CPM_NEWPAY_TBL.YTD_SEV_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_CASH_AWARDS | exp_Final.YTD_CASH_AWARDS → exp_Convert.o_YTD_CASH_AWARDS = ABS(YTD_CASH_AWARDS) → exp_Init.YTD_CASH_AWARDS → SQ_CPM_NEWPAY_TBL.YTD_CASH_AWARDS → CPM_NEWPAY_TBL.YTD_CASH_AWARDS | CPM_NEWPAY_TBL.YTD_CASH_AWARDS |
| cdcskel_WS_PAY_OUT_REC | YTD_CASH_AWARDS_SIGN | exp_Final.YTD_CASH_AWARDS_SIGN → exp_Convert.o_YTD_CASH_AWARDS_SIGN = IIF(SIGN(YTD_CASH_AWARDS) = -1, '-', '+') → exp_Init.YTD_CASH_AWARDS → SQ_CPM_NEWPAY_TBL.YTD_CASH_AWARDS → CPM_NEWPAY_TBL.YTD_CASH_AWARDS | CPM_NEWPAY_TBL.YTD_CASH_AWARDS |
| cdcskel_WS_PAY_OUT_REC | YTD_MP_CASH_AWARD | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | YTD_MP_CASH_AWARD_SIGN | exp_Final.YTD_MP_CASH_AWARD_SIGN → exp_Convert.o_YTD_MP_CASH_AWARD_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | YTD_LSL_PAY | exp_Final.YTD_LSL_PAY → exp_Convert.o_YTD_LSL_PAY = IIF(NOT ISNULL(YTD_LSL_PAY), IIF(v_YTD_LSL_PAY_EXCEEDS_LIMIT_FLAG = TRUE, v_YTD_LSL_LV_PAY_SIGN * TO_DECIMAL( v_YTD_LSL_LV_PAY_BEFORE_DEC \|\| '.' \|\| v_YTD_LSL_LV_PAY_AFTER_DEC ,2), ABS(YTD_LSL_PAY)), 0) → exp_Init.YTD_LSL_PAY → SQ_CPM_NEWPAY_TBL.YTD_LSL_PAY → CPM_NEWPAY_TBL.YTD_LSL_PAY → exp_Convert.v_YTD_LSL_PAY_EXCEEDS_LIMIT_FLAG = IIF( ABS(YTD_LSL_PAY) > 99999.99, TRUE, FALSE) → exp_Convert.v_YTD_LSL_LV_PAY_SIGN = SIGN(YTD_LSL_PAY) → exp_Convert.v_YTD_LSL_LV_PAY_BEFORE_DEC = SUBSTR(v_YTD_LSL_LV_PAY_CHAR, v_YTD_LSL_LV_PAY_POS_DEC -5, 5) → exp_Convert.v_YTD_LSL_LV_PAY_CHAR = TO_CHAR(TO_DECIMAL(YTD_LSL_PAY, 2)) → exp_Convert.v_YTD_LSL_LV_PAY_POS_DEC = INSTR(v_YTD_LSL_LV_PAY_CHAR, '.') → exp_Convert.v_YTD_LSL_LV_PAY_AFTER_DEC = SUBSTR(v_YTD_LSL_LV_PAY_CHAR, v_YTD_LSL_LV_PAY_POS_DEC + 1, 2) | CPM_NEWPAY_TBL.YTD_LSL_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_LSL_PAY_SIGN | exp_Final.YTD_LSL_PAY_SIGN → exp_Convert.o_YTD_LSL_PAY_SIGN = IIF(SIGN(YTD_LSL_PAY) = -1, '-', '+') → exp_Init.YTD_LSL_PAY → SQ_CPM_NEWPAY_TBL.YTD_LSL_PAY → CPM_NEWPAY_TBL.YTD_LSL_PAY | CPM_NEWPAY_TBL.YTD_LSL_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_MISC_OTH_PAY | exp_Final.YTD_MISC_OTH_PAY → exp_Convert.o_YTD_MISC_OTH_PAY = ABS(YTD_MISC_OTH_PAY) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(YTD_MISC_OTH_PAY), 2)), '.', NULL), 9, '0') → exp_Init.YTD_MISC_OTH_PAY → SQ_CPM_NEWPAY_TBL.YTD_MISC_OTH_PAY → CPM_NEWPAY_TBL.YTD_MISC_OTH_PAY | CPM_NEWPAY_TBL.YTD_MISC_OTH_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_MISC_OTH_PAY_SIGN | exp_Final.YTD_MISC_OTH_PAY_SIGN → exp_Convert.o_YTD_MISC_OTH_PAY_SIGN = IIF(SIGN(YTD_MISC_OTH_PAY) = -1, '-', '+') → exp_Init.YTD_MISC_OTH_PAY → SQ_CPM_NEWPAY_TBL.YTD_MISC_OTH_PAY → CPM_NEWPAY_TBL.YTD_MISC_OTH_PAY | CPM_NEWPAY_TBL.YTD_MISC_OTH_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_GROSS_PAY | exp_Final.YTD_GROSS_PAY → exp_Convert.o_YTD_GROSS_PAY = ABS(YTD_GROSS_PAY) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(YTD_GROSS_PAY), 2)), '.', NULL), 9, '0') → exp_Init.YTD_GROSS_PAY → SQ_CPM_NEWPAY_TBL.YTD_GROSS_PAY → CPM_NEWPAY_TBL.YTD_GROSS_PAY | CPM_NEWPAY_TBL.YTD_GROSS_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_GROSS_PAY_SIGN | exp_Final.YTD_GROSS_PAY_SIGN → exp_Convert.o_YTD_GROSS_PAY_SIGN = IIF(SIGN(YTD_GROSS_PAY) = -1, '-', '+') → exp_Init.YTD_GROSS_PAY → SQ_CPM_NEWPAY_TBL.YTD_GROSS_PAY → CPM_NEWPAY_TBL.YTD_GROSS_PAY | CPM_NEWPAY_TBL.YTD_GROSS_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_NON_TAX_PAY | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | YTD_NON_TAX_PAY_SIGN | exp_Final.YTD_NON_TAX_PAY_SIGN → exp_Convert.o_YTD_NON_TAX_PAY_SIGN = '+' --IIF(SIGN(YTD_NON_TAX_PAY) = -1, -- '-', -- '+') → exp_Init.YTD_NON_TAX_PAY → SQ_CPM_NEWPAY_TBL.YTD_NON_TAX_PAY → CPM_NEWPAY_TBL.YTD_NON_TAX_PAY | CPM_NEWPAY_TBL.YTD_NON_TAX_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_FED_TAX_DED | exp_Final.YTD_FED_TAX_DED → exp_Convert.o_YTD_FED_TAX_DED = ABS(YTD_FED_TAX_DED) → exp_Init.YTD_FED_TAX_DED → SQ_CPM_NEWPAY_TBL.YTD_FED_TAX_DED → CPM_NEWPAY_TBL.YTD_FED_TAX_DED | CPM_NEWPAY_TBL.YTD_FED_TAX_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_FED_TAX_DED_SIGN | exp_Final.YTD_FED_TAX_DED_SIGN → exp_Convert.o_YTD_FED_TAX_DED_SIGN = IIF(SIGN(YTD_FED_TAX_DED) = -1, '-', '+') → exp_Init.YTD_FED_TAX_DED → SQ_CPM_NEWPAY_TBL.YTD_FED_TAX_DED → CPM_NEWPAY_TBL.YTD_FED_TAX_DED | CPM_NEWPAY_TBL.YTD_FED_TAX_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_TAXABLE_PAY | exp_Final.YTD_TAXABLE_PAY → exp_Convert.o_YTD_TAXABLE_PAY = ABS(YTD_TAXABLE_PAY) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(YTD_TAXABLE_PAY), 2)), '.', NULL), 9, '0') → exp_Init.YTD_TAXABLE_PAY → SQ_CPM_NEWPAY_TBL.YTD_TAXABLE_PAY → CPM_NEWPAY_TBL.YTD_TAXABLE_PAY | CPM_NEWPAY_TBL.YTD_TAXABLE_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_TAXABLE_PAY_SIGN | exp_Final.YTD_TAXABLE_PAY_SIGN → exp_Convert.o_YTD_TAXABLE_PAY_SIGN = IIF(SIGN(YTD_TAXABLE_PAY) = -1, '-', '+') → exp_Init.YTD_TAXABLE_PAY → SQ_CPM_NEWPAY_TBL.YTD_TAXABLE_PAY → CPM_NEWPAY_TBL.YTD_TAXABLE_PAY | CPM_NEWPAY_TBL.YTD_TAXABLE_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_CSR_DED | exp_Final.YTD_CSR_DED → exp_Convert.o_YTD_CSR_DED = ABS(YTD_CSR_DED) → exp_Init.YTD_CSR_DED → SQ_CPM_NEWPAY_TBL.YTD_CSR_DED → CPM_NEWPAY_TBL.YTD_CSR_DED | CPM_NEWPAY_TBL.YTD_CSR_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_CSR_DED_SIGN | exp_Final.YTD_CSR_DED_SIGN → exp_Convert.o_YTD_CSR_DED_SIGN = IIF(SIGN(YTD_CSR_DED) = -1, '-', '+') → exp_Init.YTD_CSR_DED → SQ_CPM_NEWPAY_TBL.YTD_CSR_DED → CPM_NEWPAY_TBL.YTD_CSR_DED | CPM_NEWPAY_TBL.YTD_CSR_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_CSR_EMPLR | exp_Final.YTD_CSR_EMPLR → exp_Convert.o_YTD_CSR_EMPLR = ABS(YTD_CSR_EMPLR) → exp_Init.YTD_CSR_EMPLR → SQ_CPM_NEWPAY_TBL.YTD_CSR_EMPLR → CPM_NEWPAY_TBL.YTD_CSR_EMPLR | CPM_NEWPAY_TBL.YTD_CSR_EMPLR |
| cdcskel_WS_PAY_OUT_REC | YTD_CSR_EMPLR_SIGN | exp_Final.YTD_CSR_EMPLR_SIGN → exp_Convert.o_YTD_CSR_EMPLR_SIGN = IIF(SIGN(YTD_CSR_EMPLR) = -1, '-', '+') → exp_Init.YTD_CSR_EMPLR → SQ_CPM_NEWPAY_TBL.YTD_CSR_EMPLR → CPM_NEWPAY_TBL.YTD_CSR_EMPLR | CPM_NEWPAY_TBL.YTD_CSR_EMPLR |
| cdcskel_WS_PAY_OUT_REC | YTD_CSR_PAY | exp_Final.YTD_CSR_PAY → exp_Convert.o_YTD_CSR_PAY = ABS(YTD_CSR_PAY) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(YTD_CSR_PAY), 2)), '.', NULL), 9, '0') → exp_Init.YTD_CSR_PAY → SQ_CPM_NEWPAY_TBL.YTD_CSR_PAY → CPM_NEWPAY_TBL.YTD_CSR_PAY | CPM_NEWPAY_TBL.YTD_CSR_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_CSR_PAY_SIGN | exp_Final.YTD_CSR_PAY_SIGN → exp_Convert.o_YTD_CSR_PAY_SIGN = IIF(SIGN(YTD_CSR_PAY) = -1, '-', '+') → exp_Init.YTD_CSR_PAY → SQ_CPM_NEWPAY_TBL.YTD_CSR_PAY → CPM_NEWPAY_TBL.YTD_CSR_PAY | CPM_NEWPAY_TBL.YTD_CSR_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_FICA_DED | exp_Final.YTD_FICA_DED → exp_Convert.o_YTD_FICA_DED = ABS(YTD_FICA_DED) → exp_Init.YTD_FICA_DED → SQ_CPM_NEWPAY_TBL.YTD_FICA_DED → CPM_NEWPAY_TBL.YTD_FICA_DED | CPM_NEWPAY_TBL.YTD_FICA_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_FICA_DED_SIGN | exp_Final.YTD_FICA_DED_SIGN → exp_Convert.o_YTD_FICA_DED_SIGN = IIF(SIGN(YTD_FICA_DED) = -1, '-', '+') → exp_Init.YTD_FICA_DED → SQ_CPM_NEWPAY_TBL.YTD_FICA_DED → CPM_NEWPAY_TBL.YTD_FICA_DED | CPM_NEWPAY_TBL.YTD_FICA_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_FICA_EMPLR | exp_Final.YTD_FICA_EMPLR → exp_Convert.o_YTD_FICA_EMPLR = ABS(YTD_FICA_EMPLR) → exp_Init.YTD_FICA_EMPLR → SQ_CPM_NEWPAY_TBL.YTD_FICA_EMPLR → CPM_NEWPAY_TBL.YTD_FICA_EMPLR | CPM_NEWPAY_TBL.YTD_FICA_EMPLR |
| cdcskel_WS_PAY_OUT_REC | YTD_FICA_EMPLR_SIGN | exp_Final.YTD_FICA_EMPLR_SIGN → exp_Convert.o_YTD_FICA_EMPLR_SIGN = IIF(SIGN(YTD_FICA_EMPLR) = -1, '-', '+') → exp_Init.YTD_FICA_EMPLR → SQ_CPM_NEWPAY_TBL.YTD_FICA_EMPLR → CPM_NEWPAY_TBL.YTD_FICA_EMPLR | CPM_NEWPAY_TBL.YTD_FICA_EMPLR |
| cdcskel_WS_PAY_OUT_REC | YTD_FICA_PAY | exp_Final.YTD_FICA_PAY → exp_Convert.o_YTD_FICA_PAY = ABS(YTD_FICA_PAY) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(YTD_FICA_PAY), 2)), '.', NULL), 9, '0') → exp_Init.YTD_FICA_PAY → SQ_CPM_NEWPAY_TBL.YTD_FICA_PAY → CPM_NEWPAY_TBL.YTD_FICA_PAY | CPM_NEWPAY_TBL.YTD_FICA_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_FICA_PAY_SIGN | exp_Final.YTD_FICA_PAY_SIGN → exp_Convert.o_YTD_FICA_PAY_SIGN = IIF(SIGN(YTD_FICA_PAY) = -1, '-', '+') → exp_Init.YTD_FICA_PAY → SQ_CPM_NEWPAY_TBL.YTD_FICA_PAY → CPM_NEWPAY_TBL.YTD_FICA_PAY | CPM_NEWPAY_TBL.YTD_FICA_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_MEDC_DED | exp_Final.YTD_MEDC_DED → exp_Convert.o_YTD_MEDC_DED = ABS(YTD_MEDC_DED) → exp_Init.YTD_MEDC_DED → SQ_CPM_NEWPAY_TBL.YTD_MEDC_DED → CPM_NEWPAY_TBL.YTD_MEDC_DED | CPM_NEWPAY_TBL.YTD_MEDC_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_MEDC_DED_SIGN | exp_Final.YTD_MEDC_DED_SIGN → exp_Convert.o_YTD_MEDC_DED_SIGN = IIF(SIGN(YTD_MEDC_DED) = -1, '-', '+') → exp_Init.YTD_MEDC_DED → SQ_CPM_NEWPAY_TBL.YTD_MEDC_DED → CPM_NEWPAY_TBL.YTD_MEDC_DED | CPM_NEWPAY_TBL.YTD_MEDC_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_MEDC_EMPLR | exp_Final.YTD_MEDC_EMPLR → exp_Convert.o_YTD_MEDC_EMPLR = ABS(YTD_MEDC_EMPLR) → exp_Init.YTD_MEDC_EMPLR → SQ_CPM_NEWPAY_TBL.YTD_MEDC_EMPLR → CPM_NEWPAY_TBL.YTD_MEDC_EMPLR | CPM_NEWPAY_TBL.YTD_MEDC_EMPLR |
| cdcskel_WS_PAY_OUT_REC | YTD_MEDC_EMPLR_SIGN | exp_Final.YTD_MEDC_EMPLR_SIGN → exp_Convert.o_YTD_MEDC_EMPLR_SIGN = IIF(SIGN(YTD_MEDC_EMPLR) = -1, '-', '+') → exp_Init.YTD_MEDC_EMPLR → SQ_CPM_NEWPAY_TBL.YTD_MEDC_EMPLR → CPM_NEWPAY_TBL.YTD_MEDC_EMPLR | CPM_NEWPAY_TBL.YTD_MEDC_EMPLR |
| cdcskel_WS_PAY_OUT_REC | YTD_PAY_S_MEDC | exp_Final.YTD_PAY_S_MEDC → exp_Convert.o_YTD_PAY_S_MEDC = ABS(YTD_PAY_S_MEDC) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(YTD_PAY_S_MEDC), 2)), '.', NULL), 9, '0') → exp_Init.YTD_PAY_S_MEDC → SQ_CPM_NEWPAY_TBL.YTD_PAY_S_MEDC → CPM_NEWPAY_TBL.YTD_PAY_S_MEDC | CPM_NEWPAY_TBL.YTD_PAY_S_MEDC |
| cdcskel_WS_PAY_OUT_REC | YTD_PAY_S_MEDC_SIGN | exp_Final.YTD_PAY_S_MEDC_SIGN → exp_Convert.o_YTD_PAY_S_MEDC_SIGN = IIF(SIGN(YTD_PAY_S_MEDC) = -1, '-', '+') → exp_Init.YTD_PAY_S_MEDC → SQ_CPM_NEWPAY_TBL.YTD_PAY_S_MEDC → CPM_NEWPAY_TBL.YTD_PAY_S_MEDC | CPM_NEWPAY_TBL.YTD_PAY_S_MEDC |
| cdcskel_WS_PAY_OUT_REC | YTD_FERS_EMP_DED | exp_Final.YTD_FERS_EMP_DED → exp_Convert.o_YTD_FERS_EMP_DED = ABS(YTD_FERS_EMP_DED) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(YTD_FERS_EMP_DED), 2)), '.', NULL), 15, '0') → exp_Init.YTD_FERS_EMP_DED → SQ_CPM_NEWPAY_TBL.YTD_FERS_EMP_DED → CPM_NEWPAY_TBL.YTD_FERS_EMP_DED | CPM_NEWPAY_TBL.YTD_FERS_EMP_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_FERS_EMP_DED_SIGN | exp_Final.YTD_FERS_EMP_DED_SIGN → exp_Convert.o_YTD_FERS_EMP_DED_SIGN = IIF(SIGN(YTD_FERS_EMP_DED) = -1, '-', '+') → exp_Init.YTD_FERS_EMP_DED → SQ_CPM_NEWPAY_TBL.YTD_FERS_EMP_DED → CPM_NEWPAY_TBL.YTD_FERS_EMP_DED | CPM_NEWPAY_TBL.YTD_FERS_EMP_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_FERS_AGY_DED | exp_Final.YTD_FERS_AGY_DED → exp_Convert.o_YTD_FERS_AGY_DED = ABS(YTD_FERS_AGY_DED) → exp_Init.YTD_FERS_AGY_DED → SQ_CPM_NEWPAY_TBL.YTD_FERS_AGY_DED → CPM_NEWPAY_TBL.YTD_FERS_AGY_DED | CPM_NEWPAY_TBL.YTD_FERS_AGY_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_FERS_AGY_DED_SIGN | exp_Final.YTD_FERS_AGY_DED_SIGN → exp_Convert.o_YTD_FERS_AGY_DED_SIGN = IIF(SIGN(YTD_FERS_AGY_DED) = -1, '-', '+') → exp_Init.YTD_FERS_AGY_DED → SQ_CPM_NEWPAY_TBL.YTD_FERS_AGY_DED → CPM_NEWPAY_TBL.YTD_FERS_AGY_DED | CPM_NEWPAY_TBL.YTD_FERS_AGY_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_FERS_PAY_SUB | exp_Final.YTD_FERS_PAY_SUB → exp_Convert.o_YTD_FERS_PAY_SUB = ABS(YTD_FERS_PAY_SUB) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(YTD_FERS_PAY_SUB), 2)), '.', NULL), 9, '0') → exp_Init.YTD_FERS_PAY_SUB → SQ_CPM_NEWPAY_TBL.YTD_FERS_PAY_SUB → CPM_NEWPAY_TBL.YTD_FERS_PAY_SUB | CPM_NEWPAY_TBL.YTD_FERS_PAY_SUB |
| cdcskel_WS_PAY_OUT_REC | YTD_FERS_PAY_SUB_SIGN | exp_Final.YTD_FERS_PAY_SUB_SIGN → exp_Convert.o_YTD_FERS_PAY_SUB_SIGN = IIF(SIGN(YTD_FERS_PAY_SUB) = -1, '-', '+') → exp_Init.YTD_FERS_PAY_SUB → SQ_CPM_NEWPAY_TBL.YTD_FERS_PAY_SUB → CPM_NEWPAY_TBL.YTD_FERS_PAY_SUB | CPM_NEWPAY_TBL.YTD_FERS_PAY_SUB |
| cdcskel_WS_PAY_OUT_REC | YTD_LEVY_DED | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | YTD_LEVY_DED_SIGN | exp_Final.YTD_LEVY_DED_SIGN → exp_Convert.o_YTD_LEVY_DED_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | YTD_ST_TX_1_CDE | exp_Final.YTD_ST_TX_1_CDE → exp_Convert.o_YTD_ST_TX_1_CDE = LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(YTD_ST_TX_1_CDE), 0)), '.', NULL), 2, '0') → exp_Init.YTD_ST_TX_1_CDE → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_1_CDE → CPM_NEWPAY_TBL.YTD_ST_TX_1_CDE | CPM_NEWPAY_TBL.YTD_ST_TX_1_CDE |
| cdcskel_WS_PAY_OUT_REC | YTD_ST_TX_1_DED | exp_Final.YTD_ST_TX_1_DED → exp_Convert.o_YTD_ST_TX_1_DED = ABS(YTD_ST_TX_1_DED) → exp_Init.YTD_ST_TX_1_DED → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_1_DED → CPM_NEWPAY_TBL.YTD_ST_TX_1_DED | CPM_NEWPAY_TBL.YTD_ST_TX_1_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_ST_TX_1_DED_SIGN | exp_Final.YTD_ST_TX_1_DED_SIGN → exp_Convert.o_YTD_ST_TX_1_DED_SIGN = IIF(SIGN(YTD_ST_TX_1_DED) = -1, '-', '+') → exp_Init.YTD_ST_TX_1_DED → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_1_DED → CPM_NEWPAY_TBL.YTD_ST_TX_1_DED | CPM_NEWPAY_TBL.YTD_ST_TX_1_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_ST_TX_1_GRS | exp_Final.YTD_ST_TX_1_GRS → exp_Convert.o_YTD_ST_TX_1_GRS = ABS(YTD_ST_TX_1_GRS) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(YTD_ST_TX_1_GRS), 2)), '.', NULL), 9, '0') → exp_Init.YTD_ST_TX_1_GRS → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_1_GRS → CPM_NEWPAY_TBL.YTD_ST_TX_1_GRS | CPM_NEWPAY_TBL.YTD_ST_TX_1_GRS |
| cdcskel_WS_PAY_OUT_REC | YTD_ST_TX_1_GRS_SIGN | exp_Final.YTD_ST_TX_1_GRS_SIGN → exp_Convert.o_YTD_ST_TX_1_GRS_SIGN = IIF(SIGN(YTD_ST_TX_1_GRS) = -1, '-', '+') → exp_Init.YTD_ST_TX_1_GRS → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_1_GRS → CPM_NEWPAY_TBL.YTD_ST_TX_1_GRS | CPM_NEWPAY_TBL.YTD_ST_TX_1_GRS |
| cdcskel_WS_PAY_OUT_REC | YTD_ST_TX_2_CDE | exp_Final.YTD_ST_TX_2_CDE → exp_Convert.o_YTD_ST_TX_2_CDE = LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(YTD_ST_TX_2_CDE), 0)), '.', NULL), 2, '0') → exp_Init.YTD_ST_TX_2_CDE → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_2_CDE → CPM_NEWPAY_TBL.YTD_ST_TX_2_CDE | CPM_NEWPAY_TBL.YTD_ST_TX_2_CDE |
| cdcskel_WS_PAY_OUT_REC | YTD_ST_TX_2_DED | exp_Final.YTD_ST_TX_2_DED → exp_Convert.o_YTD_ST_TX_2_DED = ABS(YTD_ST_TX_2_DED) → exp_Init.YTD_ST_TX_2_DED → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_2_DED → CPM_NEWPAY_TBL.YTD_ST_TX_2_DED | CPM_NEWPAY_TBL.YTD_ST_TX_2_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_ST_TX_2_DED_SIGN | exp_Final.YTD_ST_TX_2_DED_SIGN → exp_Convert.o_YTD_ST_TX_2_DED_SIGN = IIF(SIGN(YTD_ST_TX_2_DED) = -1, '-', '+') → exp_Init.YTD_ST_TX_2_DED → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_2_DED → CPM_NEWPAY_TBL.YTD_ST_TX_2_DED | CPM_NEWPAY_TBL.YTD_ST_TX_2_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_ST_TX_2_GRS | exp_Final.YTD_ST_TX_2_GRS → exp_Convert.o_YTD_ST_TX_2_GRS = ABS(YTD_ST_TX_2_GRS) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(YTD_ST_TX_2_GRS), 2)), '.', NULL), 9, '0') → exp_Init.YTD_ST_TX_2_GRS → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_2_GRS → CPM_NEWPAY_TBL.YTD_ST_TX_2_GRS | CPM_NEWPAY_TBL.YTD_ST_TX_2_GRS |
| cdcskel_WS_PAY_OUT_REC | YTD_ST_TX_2_GRS_SIGN | exp_Final.YTD_ST_TX_2_GRS_SIGN → exp_Convert.o_YTD_ST_TX_2_GRS_SIGN = IIF(SIGN(YTD_ST_TX_2_GRS) = -1, '-', '+') → exp_Init.YTD_ST_TX_2_GRS → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_2_GRS → CPM_NEWPAY_TBL.YTD_ST_TX_2_GRS | CPM_NEWPAY_TBL.YTD_ST_TX_2_GRS |
| cdcskel_WS_PAY_OUT_REC | YTD_ST_TX_3_CDE | exp_Final.YTD_ST_TX_3_CDE → exp_Convert.o_YTD_ST_TX_3_CDE = LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(YTD_ST_TX_3_CDE), 0)), '.', NULL), 2, '0') → exp_Init.YTD_ST_TX_3_CDE → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_3_CDE → CPM_NEWPAY_TBL.YTD_ST_TX_3_CDE | CPM_NEWPAY_TBL.YTD_ST_TX_3_CDE |
| cdcskel_WS_PAY_OUT_REC | YTD_ST_TX_3_DED | exp_Final.YTD_ST_TX_3_DED → exp_Convert.o_YTD_ST_TX_3_DED = ABS(YTD_ST_TX_3_DED) → exp_Init.YTD_ST_TX_3_DED → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_3_DED → CPM_NEWPAY_TBL.YTD_ST_TX_3_DED | CPM_NEWPAY_TBL.YTD_ST_TX_3_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_ST_TX_3_DED_SIGN | exp_Final.YTD_ST_TX_3_DED_SIGN → exp_Convert.o_YTD_ST_TX_3_DED_SIGN = IIF(SIGN(YTD_ST_TX_3_DED) = -1, '-', '+') → exp_Init.YTD_ST_TX_3_DED → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_3_DED → CPM_NEWPAY_TBL.YTD_ST_TX_3_DED | CPM_NEWPAY_TBL.YTD_ST_TX_3_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_ST_TX_3_GRS | exp_Final.YTD_ST_TX_3_GRS → exp_Convert.o_YTD_ST_TX_3_GRS = ABS(YTD_ST_TX_3_GRS) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(YTD_ST_TX_3_GRS), 2)), '.', NULL), 9, '0') → exp_Init.YTD_ST_TX_3_GRS → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_3_GRS → CPM_NEWPAY_TBL.YTD_ST_TX_3_GRS | CPM_NEWPAY_TBL.YTD_ST_TX_3_GRS |
| cdcskel_WS_PAY_OUT_REC | YTD_ST_TX_3_GRS_SIGN | exp_Final.YTD_ST_TX_3_GRS_SIGN → exp_Convert.o_YTD_ST_TX_3_GRS_SIGN = IIF(SIGN(YTD_ST_TX_3_GRS) = -1, '-', '+') → exp_Init.YTD_ST_TX_3_GRS → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_3_GRS → CPM_NEWPAY_TBL.YTD_ST_TX_3_GRS | CPM_NEWPAY_TBL.YTD_ST_TX_3_GRS |
| cdcskel_WS_PAY_OUT_REC | YTD_ST_TX_4_CDE | exp_Final.YTD_ST_TX_4_CDE → exp_Convert.o_YTD_ST_TX_4_CDE = LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(YTD_ST_TX_4_CDE), 0)), '.', NULL), 2, '0') → exp_Init.YTD_ST_TX_4_CDE → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_4_CDE → CPM_NEWPAY_TBL.YTD_ST_TX_4_CDE | CPM_NEWPAY_TBL.YTD_ST_TX_4_CDE |
| cdcskel_WS_PAY_OUT_REC | YTD_ST_TX_4_DED | exp_Final.YTD_ST_TX_4_DED → exp_Convert.o_YTD_ST_TX_4_DED = ABS(YTD_ST_TX_4_DED) → exp_Init.YTD_ST_TX_4_DED → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_4_DED → CPM_NEWPAY_TBL.YTD_ST_TX_4_DED | CPM_NEWPAY_TBL.YTD_ST_TX_4_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_ST_TX_4_DED_SIGN | exp_Final.YTD_ST_TX_4_DED_SIGN → exp_Convert.o_YTD_ST_TX_4_DED_SIGN = IIF(SIGN(YTD_ST_TX_4_DED) = -1, '-', '+') → exp_Init.YTD_ST_TX_4_DED → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_4_DED → CPM_NEWPAY_TBL.YTD_ST_TX_4_DED | CPM_NEWPAY_TBL.YTD_ST_TX_4_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_ST_TX_4_GRS | exp_Final.YTD_ST_TX_4_GRS → exp_Convert.o_YTD_ST_TX_4_GRS = ABS(YTD_ST_TX_4_GRS) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(YTD_ST_TX_4_GRS), 2)), '.', NULL), 9, '0') → exp_Init.YTD_ST_TX_4_GRS → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_4_GRS → CPM_NEWPAY_TBL.YTD_ST_TX_4_GRS | CPM_NEWPAY_TBL.YTD_ST_TX_4_GRS |
| cdcskel_WS_PAY_OUT_REC | YTD_ST_TX_4_GRS_SIGN | exp_Final.YTD_ST_TX_4_GRS_SIGN → exp_Convert.o_YTD_ST_TX_4_GRS_SIGN = IIF(SIGN(YTD_ST_TX_4_GRS) = -1, '-', '+') → exp_Init.YTD_ST_TX_4_GRS → SQ_CPM_NEWPAY_TBL.YTD_ST_TX_4_GRS → CPM_NEWPAY_TBL.YTD_ST_TX_4_GRS | CPM_NEWPAY_TBL.YTD_ST_TX_4_GRS |
| cdcskel_WS_PAY_OUT_REC | YTD_ST_TX_SUM | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | YTD_ST_TX_SUM_SIGN | exp_Final.YTD_ST_TX_SUM_SIGN → exp_Convert.o_YTD_ST_TX_SUM_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | YTD_CITY_DED | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | YTD_CITY_DED_SIGN | exp_Final.YTD_CITY_DED_SIGN → exp_Convert.o_YTD_CITY_DED_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | YTD_CITY_TAX1_GROSS | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | YTD_CITY_TAX1_GROSS_SIGN | exp_Final.YTD_CITY_TAX1_GROSS_SIGN → exp_Convert.o_YTD_CITY_TAX1_GROSS_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | YTD_CITY_TAX2_GROSS | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | YTD_CITY_TAX2_GROSS_SIGN | exp_Final.YTD_CITY_TAX2_GROSS_SIGN → exp_Convert.o_YTD_CITY_TAX2_GROSS_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | YTD_CITY_TX_2_CDE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | YTD_CITY_TX_2_DED | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | YTD_CITY_TX_2_DED_SIGN | exp_Final.YTD_CITY_TX_2_DED_SIGN → exp_Convert.o_YTD_CITY_TX_2_DED_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | YTD_SUM_CITY | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | YTD_SUM_CITY_SIGN | exp_Final.YTD_SUM_CITY_SIGN → exp_Convert.o_YTD_SUM_CITY_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | YTD_HLTH_DED | exp_Final.YTD_HLTH_DED → exp_Convert.o_YTD_HLTH_DED = ABS(YTD_HLTH_DED) → exp_Init.YTD_HLTH_DED → SQ_CPM_NEWPAY_TBL.YTD_HLTH_DED → CPM_NEWPAY_TBL.YTD_HLTH_DED | CPM_NEWPAY_TBL.YTD_HLTH_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_HLTH_DED_SIGN | exp_Final.YTD_HLTH_DED_SIGN → exp_Convert.o_YTD_HLTH_DED_SIGN = IIF(SIGN(YTD_HLTH_DED) = -1, '-', '+') → exp_Init.YTD_HLTH_DED → SQ_CPM_NEWPAY_TBL.YTD_HLTH_DED → CPM_NEWPAY_TBL.YTD_HLTH_DED | CPM_NEWPAY_TBL.YTD_HLTH_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_HLTH_EMPLR | exp_Final.YTD_HLTH_EMPLR → exp_Convert.o_YTD_HLTH_EMPLR = ABS(YTD_HLTH_EMPLR) → exp_Init.YTD_HLTH_EMPLR → SQ_CPM_NEWPAY_TBL.YTD_HLTH_EMPLR → CPM_NEWPAY_TBL.YTD_HLTH_EMPLR | CPM_NEWPAY_TBL.YTD_HLTH_EMPLR |
| cdcskel_WS_PAY_OUT_REC | YTD_HLTH_EMPLR_SIGN | exp_Final.YTD_HLTH_EMPLR_SIGN → exp_Convert.o_YTD_HLTH_EMPLR_SIGN = IIF(SIGN(YTD_HLTH_EMPLR) = -1, '-', '+') → exp_Init.YTD_HLTH_EMPLR → SQ_CPM_NEWPAY_TBL.YTD_HLTH_EMPLR → CPM_NEWPAY_TBL.YTD_HLTH_EMPLR | CPM_NEWPAY_TBL.YTD_HLTH_EMPLR |
| cdcskel_WS_PAY_OUT_REC | YTD_BOND_DED | exp_Final.YTD_BOND_DED → exp_Convert.o_YTD_BOND_DED = ABS(YTD_BOND_DED) → exp_Init.YTD_BOND_DED → SQ_CPM_NEWPAY_TBL.YTD_BOND_DED → CPM_NEWPAY_TBL.YTD_BOND_DED | CPM_NEWPAY_TBL.YTD_BOND_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_BOND_DED_SIGN | exp_Final.YTD_BOND_DED_SIGN → exp_Convert.o_YTD_BOND_DED_SIGN = IIF(SIGN(YTD_BOND_DED) = -1, '-', '+') → exp_Init.YTD_BOND_DED → SQ_CPM_NEWPAY_TBL.YTD_BOND_DED → CPM_NEWPAY_TBL.YTD_BOND_DED | CPM_NEWPAY_TBL.YTD_BOND_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_LI_REG_DED | exp_Final.YTD_LI_REG_DED → exp_Convert.o_YTD_LI_REG_DED = ABS(YTD_LI_REG_DED) → exp_Init.YTD_LI_REG_DED → SQ_CPM_NEWPAY_TBL.YTD_LI_REG_DED → CPM_NEWPAY_TBL.YTD_LI_REG_DED | CPM_NEWPAY_TBL.YTD_LI_REG_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_LI_REG_DED_SIGN | exp_Final.YTD_LI_REG_DED_SIGN → exp_Convert.o_YTD_LI_REG_DED_SIGN = IIF(SIGN(YTD_LI_REG_DED) = -1, '-', '+') → exp_Init.YTD_LI_REG_DED → SQ_CPM_NEWPAY_TBL.YTD_LI_REG_DED → CPM_NEWPAY_TBL.YTD_LI_REG_DED | CPM_NEWPAY_TBL.YTD_LI_REG_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_LI_REG_EMPLR | exp_Final.YTD_LI_REG_EMPLR → exp_Convert.o_YTD_LI_REG_EMPLR = ABS(YTD_LI_REG_EMPLR) → exp_Init.YTD_LI_REG_EMPLR → SQ_CPM_NEWPAY_TBL.YTD_LI_REG_EMPLR → CPM_NEWPAY_TBL.YTD_LI_REG_EMPLR | CPM_NEWPAY_TBL.YTD_LI_REG_EMPLR |
| cdcskel_WS_PAY_OUT_REC | YTD_LI_REG_EMPLR_SIGN | exp_Final.YTD_LI_REG_EMPLR_SIGN → exp_Convert.o_YTD_LI_REG_EMPLR_SIGN = IIF(SIGN(YTD_LI_REG_EMPLR) = -1, '-', '+') → exp_Init.YTD_LI_REG_EMPLR → SQ_CPM_NEWPAY_TBL.YTD_LI_REG_EMPLR → CPM_NEWPAY_TBL.YTD_LI_REG_EMPLR | CPM_NEWPAY_TBL.YTD_LI_REG_EMPLR |
| cdcskel_WS_PAY_OUT_REC | YTD_LI_OPT_DED | exp_Final.YTD_LI_OPT_DED → exp_Convert.o_YTD_LI_OPT_DED = ABS(YTD_LI_OPT_DED) → exp_Init.YTD_LI_OPT_DED → SQ_CPM_NEWPAY_TBL.YTD_LI_OPT_DED → CPM_NEWPAY_TBL.YTD_LI_OPT_DED | CPM_NEWPAY_TBL.YTD_LI_OPT_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_LI_OPT_DED_SIGN | exp_Final.YTD_LI_OPT_DED_SIGN → exp_Convert.o_YTD_LI_OPT_DED_SIGN = IIF(SIGN(YTD_LI_OPT_DED) = -1, '-', '+') → exp_Init.YTD_LI_OPT_DED → SQ_CPM_NEWPAY_TBL.YTD_LI_OPT_DED → CPM_NEWPAY_TBL.YTD_LI_OPT_DED | CPM_NEWPAY_TBL.YTD_LI_OPT_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_FEGLI_OPTB | exp_Final.YTD_FEGLI_OPTB → exp_Convert.o_YTD_FEGLI_OPTB = ABS(YTD_FEGLI_OPTB) → exp_Init.YTD_FEGLI_OPTB → SQ_CPM_NEWPAY_TBL.YTD_FEGLI_OPTB → CPM_NEWPAY_TBL.YTD_FEGLI_OPTB | CPM_NEWPAY_TBL.YTD_FEGLI_OPTB |
| cdcskel_WS_PAY_OUT_REC | YTD_FEGLI_OPTB_SIGN | exp_Final.YTD_FEGLI_OPTB_SIGN → exp_Convert.o_YTD_FEGLI_OPTB_SIGN = IIF(SIGN(YTD_FEGLI_OPTB) = -1, '-', '+') → exp_Init.YTD_FEGLI_OPTB → SQ_CPM_NEWPAY_TBL.YTD_FEGLI_OPTB → CPM_NEWPAY_TBL.YTD_FEGLI_OPTB | CPM_NEWPAY_TBL.YTD_FEGLI_OPTB |
| cdcskel_WS_PAY_OUT_REC | YTD_FEGLI_OPTC | exp_Final.YTD_FEGLI_OPTC → exp_Convert.o_YTD_FEGLI_OPTC = ABS(YTD_FEGLI_OPTC) → exp_Init.YTD_FEGLI_OPTC → SQ_CPM_NEWPAY_TBL.YTD_FEGLI_OPTC → CPM_NEWPAY_TBL.YTD_FEGLI_OPTC | CPM_NEWPAY_TBL.YTD_FEGLI_OPTC |
| cdcskel_WS_PAY_OUT_REC | YTD_FEGLI_OPTC_SIGN | exp_Final.YTD_FEGLI_OPTC_SIGN → exp_Convert.o_YTD_FEGLI_OPTC_SIGN = IIF(SIGN(YTD_FEGLI_OPTC) = -1, '-', '+') → exp_Init.YTD_FEGLI_OPTC → SQ_CPM_NEWPAY_TBL.YTD_FEGLI_OPTC → CPM_NEWPAY_TBL.YTD_FEGLI_OPTC | CPM_NEWPAY_TBL.YTD_FEGLI_OPTC |
| cdcskel_WS_PAY_OUT_REC | YTD_CHAR_DED | exp_Final.YTD_CHAR_DED → exp_Convert.o_YTD_CHAR_DED = ABS(YTD_CHAR_DED) → exp_Init.YTD_CHAR_DED → SQ_CPM_NEWPAY_TBL.YTD_CHAR_DED → CPM_NEWPAY_TBL.YTD_CHAR_DED | CPM_NEWPAY_TBL.YTD_CHAR_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_CHAR_DED_SIGN | exp_Final.YTD_CHAR_DED_SIGN → exp_Convert.o_YTD_CHAR_DED_SIGN = IIF(SIGN(YTD_CHAR_DED) = -1, '-', '+') → exp_Init.YTD_CHAR_DED → SQ_CPM_NEWPAY_TBL.YTD_CHAR_DED → CPM_NEWPAY_TBL.YTD_CHAR_DED | CPM_NEWPAY_TBL.YTD_CHAR_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_UNION_1_DED | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | YTD_UNION_1_DED_SIGN | exp_Final.YTD_UNION_1_DED_SIGN → exp_Convert.o_YTD_UNION_1_DED_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | YTD_ALT_1_DED | exp_Final.YTD_ALT_1_DED → exp_Convert.o_YTD_ALT_1_DED = ABS(YTD_ALT_1_DED) → exp_Init.YTD_ALT_1_DED → SQ_CPM_NEWPAY_TBL.YTD_ALT_1_DED → CPM_NEWPAY_TBL.YTD_ALT_1_DED | CPM_NEWPAY_TBL.YTD_ALT_1_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_ALT_1_DED_SIGN | exp_Final.YTD_ALT_1_DED_SIGN → exp_Convert.o_YTD_ALT_1_DED_SIGN = IIF(SIGN(YTD_ALT_1_DED) = -1, '-', '+') → exp_Init.YTD_ALT_1_DED → SQ_CPM_NEWPAY_TBL.YTD_ALT_1_DED → CPM_NEWPAY_TBL.YTD_ALT_1_DED | CPM_NEWPAY_TBL.YTD_ALT_1_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_ALT_2_DED | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | YTD_ALT_2_DED_SIGN | exp_Final.YTD_ALT_2_DED_SIGN → exp_Convert.o_YTD_ALT_2_DED_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | YTD_ALT_3_DED | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | YTD_ALT_3_DED_SIGN | exp_Final.YTD_ALT_3_DED_SIGN → exp_Convert.o_YTD_ALT_3_DED_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | YTD_REF_1_CDE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | YTD_REF_1_AMT | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | YTD_REF_1_AMT_SIGN | exp_Final.YTD_REF_1_AMT_SIGN → exp_Convert.o_YTD_REF_1_AMT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | YTD_REF_2_CDE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | YTD_REF_2_AMT | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | YTD_REF_2_AMT_SIGN | exp_Final.YTD_REF_2_AMT_SIGN → exp_Convert.o_YTD_REF_2_AMT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | YTD_QUARTERS_DED | exp_Final.YTD_QUARTERS_DED → exp_Convert.o_YTD_QUARTERS_DED = ABS(YTD_QUARTERS_DED) → exp_Init.YTD_QUARTERS_DED → SQ_CPM_NEWPAY_TBL.YTD_QUARTERS_DED → CPM_NEWPAY_TBL.YTD_QUARTERS_DED | CPM_NEWPAY_TBL.YTD_QUARTERS_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_QUARTERS_DED_SIGN | exp_Final.YTD_QUARTERS_DED_SIGN → exp_Convert.o_YTD_QUARTERS_DED_SIGN = IIF(SIGN(YTD_QUARTERS_DED) = -1, '-', '+') → exp_Init.YTD_QUARTERS_DED → SQ_CPM_NEWPAY_TBL.YTD_QUARTERS_DED → CPM_NEWPAY_TBL.YTD_QUARTERS_DED | CPM_NEWPAY_TBL.YTD_QUARTERS_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_SUBSIST_DED | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | YTD_SUBSIST_DED_SIGN | exp_Final.YTD_SUBSIST_DED_SIGN → exp_Convert.o_YTD_SUBSIST_DED_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | YTD_LAUNDRY_DED | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | YTD_LAUNDRY_DED_SIGN | exp_Final.YTD_LAUNDRY_DED_SIGN → exp_Convert.o_YTD_LAUNDRY_DED_SIGN = IIF(SIGN(YTD_LAUNDRY_DED) = -1, '-', '+') → exp_Init.YTD_LAUNDRY_DED → SQ_CPM_NEWPAY_TBL.YTD_LAUNDRY_DED → CPM_NEWPAY_TBL.YTD_LAUNDRY_DED | CPM_NEWPAY_TBL.YTD_LAUNDRY_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_NET_PAY | exp_Final.YTD_NET_PAY → exp_Convert.o_YTD_NET_PAY = ABS(YTD_NET_PAY) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(YTD_NET_PAY), 2)), '.', NULL), 9, '0') → exp_Init.YTD_NET_PAY → SQ_CPM_NEWPAY_TBL.YTD_NET_PAY → CPM_NEWPAY_TBL.YTD_NET_PAY | CPM_NEWPAY_TBL.YTD_NET_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_NET_PAY_SIGN | exp_Final.YTD_NET_PAY_SIGN → exp_Convert.o_YTD_NET_PAY_SIGN = IIF(SIGN(YTD_NET_PAY) = -1, '-', '+') → exp_Init.YTD_NET_PAY → SQ_CPM_NEWPAY_TBL.YTD_NET_PAY → CPM_NEWPAY_TBL.YTD_NET_PAY | CPM_NEWPAY_TBL.YTD_NET_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_CSA_DED | exp_Final.YTD_CSA_DED → exp_Convert.o_YTD_CSA_DED = ABS(YTD_CSA_DED) → exp_Init.YTD_CSA_DED → SQ_CPM_NEWPAY_TBL.YTD_CSA_DED → CPM_NEWPAY_TBL.YTD_CSA_DED | CPM_NEWPAY_TBL.YTD_CSA_DED |
| cdcskel_WS_PAY_OUT_REC | YTD_CSA_DED_SIGN | exp_Final.YTD_CSA_DED_SIGN → exp_Convert.o_YTD_CSA_DED_SIGN = IIF(SIGN(YTD_CSA_DED) = -1, '-', '+') → exp_Init.YTD_CSA_DED → SQ_CPM_NEWPAY_TBL.YTD_CSA_DED → CPM_NEWPAY_TBL.YTD_CSA_DED | CPM_NEWPAY_TBL.YTD_CSA_DED |
| cdcskel_WS_PAY_OUT_REC | EIC_YTD_PAY | exp_Final.EIC_YTD_PAY → exp_Convert.o_EIC_YTD_PAY = ABS(EIC_YTD_PAY) → exp_Init.EIC_YTD_PAY → SQ_CPM_NEWPAY_TBL.EIC_YTD_PAY → CPM_NEWPAY_TBL.EIC_YTD_PAY | CPM_NEWPAY_TBL.EIC_YTD_PAY |
| cdcskel_WS_PAY_OUT_REC | EIC_YTD_PAY_SIGN | exp_Final.EIC_YTD_PAY_SIGN → exp_Convert.o_EIC_YTD_PAY_SIGN = IIF(SIGN(EIC_YTD_PAY) = -1, '-', '+') → exp_Init.EIC_YTD_PAY → SQ_CPM_NEWPAY_TBL.EIC_YTD_PAY → CPM_NEWPAY_TBL.EIC_YTD_PAY | CPM_NEWPAY_TBL.EIC_YTD_PAY |
| cdcskel_WS_PAY_OUT_REC | PCA_YTD_PAY | exp_Final.PCA_YTD_PAY → exp_Convert.o_PCA_YTD_PAY = ABS(PCA_YTD_PAY) → exp_Init.PCA_YTD_PAY → SQ_CPM_NEWPAY_TBL.PCA_YTD_PAY → CPM_NEWPAY_TBL.PCA_YTD_PAY | CPM_NEWPAY_TBL.PCA_YTD_PAY |
| cdcskel_WS_PAY_OUT_REC | PCA_YTD_PAY_SIGN | exp_Final.PCA_YTD_PAY_SIGN → exp_Convert.o_PCA_YTD_PAY_SIGN = IIF(SIGN(PCA_YTD_PAY) = -1, '-', '+') → exp_Init.PCA_YTD_PAY → SQ_CPM_NEWPAY_TBL.PCA_YTD_PAY → CPM_NEWPAY_TBL.PCA_YTD_PAY | CPM_NEWPAY_TBL.PCA_YTD_PAY |
| cdcskel_WS_PAY_OUT_REC | YTD_TSPA_PAY_SUB | exp_Final.YTD_TSPA_PAY_SUB → exp_Convert.o_YTD_TSPA_PAY_SUB = ABS(YTD_TSPA_PAY_SUB) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(YTD_TSPA_PAY_SUB), 2)), '.', NULL), 9, '0') → exp_Init.YTD_TSPA_PAY_SUB → SQ_CPM_NEWPAY_TBL.YTD_TSPA_PAY_SUB → CPM_NEWPAY_TBL.YTD_TSPA_PAY_SUB | CPM_NEWPAY_TBL.YTD_TSPA_PAY_SUB |
| cdcskel_WS_PAY_OUT_REC | YTD_TSPA_PAY_SUB_SIGN | exp_Final.YTD_TSPA_PAY_SUB_SIGN → exp_Convert.o_YTD_TSPA_PAY_SUB_SIGN = IIF(SIGN(YTD_TSPA_PAY_SUB) = -1, '-', '+') → exp_Init.YTD_TSPA_PAY_SUB → SQ_CPM_NEWPAY_TBL.YTD_TSPA_PAY_SUB → CPM_NEWPAY_TBL.YTD_TSPA_PAY_SUB | CPM_NEWPAY_TBL.YTD_TSPA_PAY_SUB |
| cdcskel_WS_PAY_OUT_REC | YTD_TSPG_GBADIST | exp_Final.YTD_TSPG_GBADIST → exp_Convert.o_YTD_TSPG_GBADIST = ABS(YTD_TSPG_GBADIST) → exp_Init.YTD_TSPG_GBADIST → SQ_CPM_NEWPAY_TBL.YTD_TSPG_GBADIST → CPM_NEWPAY_TBL.YTD_TSPG_GBADIST | CPM_NEWPAY_TBL.YTD_TSPG_GBADIST |
| cdcskel_WS_PAY_OUT_REC | YTD_TSPG_GBADIST_SIGN | exp_Final.YTD_TSPG_GBADIST_SIGN → exp_Convert.o_YTD_TSPG_GBADIST_SIGN = IIF(SIGN(YTD_TSPG_GBADIST) = -1, '-', '+') → exp_Init.YTD_TSPG_GBADIST → SQ_CPM_NEWPAY_TBL.YTD_TSPG_GBADIST → CPM_NEWPAY_TBL.YTD_TSPG_GBADIST | CPM_NEWPAY_TBL.YTD_TSPG_GBADIST |
| cdcskel_WS_PAY_OUT_REC | YTD_TSPG_EADIST | exp_Final.YTD_TSPG_EADIST → exp_Convert.o_YTD_TSPG_EADIST = ABS(YTD_TSPG_EADIST) → exp_Init.YTD_TSPG_EADIST → SQ_CPM_NEWPAY_TBL.YTD_TSPG_EADIST → CPM_NEWPAY_TBL.YTD_TSPG_EADIST | CPM_NEWPAY_TBL.YTD_TSPG_EADIST |
| cdcskel_WS_PAY_OUT_REC | YTD_TSPG_EADIST_SIGN | exp_Final.YTD_TSPG_EADIST_SIGN → exp_Convert.o_YTD_TSPG_EADIST_SIGN = IIF(SIGN(YTD_TSPG_EADIST) = -1, '-', '+') → exp_Init.YTD_TSPG_EADIST → SQ_CPM_NEWPAY_TBL.YTD_TSPG_EADIST → CPM_NEWPAY_TBL.YTD_TSPG_EADIST | CPM_NEWPAY_TBL.YTD_TSPG_EADIST |
| cdcskel_WS_PAY_OUT_REC | YTD_TSPG_GMADIST | exp_Final.YTD_TSPG_GMADIST → exp_Convert.o_YTD_TSPG_GMADIST = ABS(YTD_TSPG_GMADIST) → exp_Init.YTD_TSPG_GMADIST → SQ_CPM_NEWPAY_TBL.YTD_TSPG_GMADIST → CPM_NEWPAY_TBL.YTD_TSPG_GMADIST | CPM_NEWPAY_TBL.YTD_TSPG_GMADIST |
| cdcskel_WS_PAY_OUT_REC | YTD_TSPG_GMADIST_SIGN | exp_Final.YTD_TSPG_GMADIST_SIGN → exp_Convert.o_YTD_TSPG_GMADIST_SIGN = IIF(SIGN(YTD_TSPG_GMADIST) = -1, '-', '+') → exp_Init.YTD_TSPG_GMADIST → SQ_CPM_NEWPAY_TBL.YTD_TSPG_GMADIST → CPM_NEWPAY_TBL.YTD_TSPG_GMADIST | CPM_NEWPAY_TBL.YTD_TSPG_GMADIST |
| cdcskel_WS_PAY_OUT_REC | YTD_TSPG_PRADIST | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | YTD_TSPG_PRADIST_SIGN | exp_Final.YTD_TSPG_PRADIST_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | YTD_TSPF_GBADIST | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | YTD_TSPF_GBADIST_SIGN | exp_Final.YTD_TSPF_GBADIST_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | YTD_TSPF_EADIST | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | YTD_TSPF_EADIST_SIGN | exp_Final.YTD_TSPF_EADIST_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | YTD_TSPF_GMADIST | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | YTD_TSPF_GMADIST_SIGN | exp_Final.YTD_TSPF_GMADIST_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | YTD_TSPF_PRADIST | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | YTD_TSPF_PRADIST_SIGN | exp_Final.YTD_TSPF_PRADIST_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | YTD_TSPC_GBADIST | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | YTD_TSPC_GBADIST_SIGN | exp_Final.YTD_TSPC_GBADIST_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | YTD_TSPC_EADIST | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | YTD_TSPC_EADIST_SIGN | exp_Final.YTD_TSPC_EADIST_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | YTD_TSPC_GMADIST | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | YTD_TSPC_GMADIST_SIGN | exp_Final.YTD_TSPC_GMADIST_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | YTD_TSPC_PRADIST | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | YTD_TSPC_PRADIST_SIGN | exp_Final.YTD_TSPC_PRADIST_SIGN → exp_Set_Defaults.o_DEFAULT_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | ADJ_NO | exp_Final.ADJ_NO → exp_Convert.o_ADJ_NO = LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(ADJ_NO), 0)), '.', NULL), 2, '0') → exp_Init.ADJ_NO → SQ_CPM_NEWPAY_TBL.ADJ_NO → CPM_NEWPAY_TBL.ADJ_NO | CPM_NEWPAY_TBL.ADJ_NO |
| cdcskel_WS_PAY_OUT_REC | UNCOM_TOUR_AN_LV_FACT | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | UNCOM_TOUR_SICK_LVFACT | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | AN_LV_CR_RED | exp_Final.AN_LV_CR_RED → exp_Convert.o_AN_LV_CR_RED = ABS(AN_LV_CR_RED) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(AN_LV_CR_RED), 2)), '.', NULL), 5, '0') → exp_Init.AN_LV_CR_RED → SQ_CPM_NEWPAY_TBL.AN_LV_CR_RED → CPM_NEWPAY_TBL.AN_LV_CR_RED | CPM_NEWPAY_TBL.AN_LV_CR_RED |
| cdcskel_WS_PAY_OUT_REC | SICK_LV_CR_RED | exp_Final.SICK_LV_CR_RED → exp_Convert.o_SICK_LV_CR_RED = ABS(SICK_LV_CR_RED) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(SICK_LV_CR_RED), 2)), '.', NULL), 5, '0') → exp_Init.SICK_LV_CR_RED → SQ_CPM_NEWPAY_TBL.SICK_LV_CR_RED → CPM_NEWPAY_TBL.SICK_LV_CR_RED | CPM_NEWPAY_TBL.SICK_LV_CR_RED |
| cdcskel_WS_PAY_OUT_REC | LV_CAT_CDE | exp_Final.LV_CAT_CDE → exp_Convert.o_LV_CAT_CDE = LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(LV_CAT_CDE), 0)), '.', NULL), 1, '0') → exp_Init.LV_CAT_CDE → SQ_CPM_NEWPAY_TBL.LV_CAT_CDE → CPM_NEWPAY_TBL.LV_CAT_CDE | CPM_NEWPAY_TBL.LV_CAT_CDE |
| cdcskel_WS_PAY_OUT_REC | T_IN_SICK_HRS | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | T_IN_SICK_HRS_SIGN | exp_Final.T_IN_SICK_HRS_SIGN → exp_Convert.o_T_IN_SICK_HRS_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | T_IN_ANN_HRS | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | T_IN_ANN_HRS_SIGN | exp_Final.T_IN_ANN_HRS_SIGN → exp_Convert.o_T_IN_ANN_HRS_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | ANN_LV_VALUE_OLD | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | ANN_LV_VALUE_OLD_SIGN | exp_Final.ANN_LV_VALUE_OLD_SIGN → exp_Convert.o_ANN_LV_VALUE_OLD_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | SICK_LV_VALUE_OLD | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | SICK_LV_VALUE_OLD_SIGN | exp_Final.SICK_LV_VALUE_OLD_SIGN → exp_Convert.o_SICK_LV_VALUE_OLD_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | COMP_LV_VALUE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | COMP_LV_VALUE_SIGN | exp_Final.COMP_LV_VALUE_SIGN → exp_Convert.o_COMP_LV_VALUE_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | AN_LV_EARNED_CPP | exp_Final.AN_LV_EARNED_CPP → exp_Convert.o_AN_LV_EARNED_CPP = ABS(AN_LV_EARNED_CPP) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(AN_LV_EARNED_CPP), 0)), '.', NULL), 3, '0') → exp_Init.AN_LV_EARNED_CPP → SQ_CPM_NEWPAY_TBL.AN_LV_EARNED_CPP → CPM_NEWPAY_TBL.AN_LV_EARNED_CPP | CPM_NEWPAY_TBL.AN_LV_EARNED_CPP |
| cdcskel_WS_PAY_OUT_REC | AN_LV_EARNED_CPP_SIGN | exp_Final.AN_LV_EARNED_CPP_SIGN → exp_Convert.o_AN_LV_EARNED_CPP_SIGN = IIF(SIGN(AN_LV_EARNED_CPP) = -1, '-', '+') → exp_Init.AN_LV_EARNED_CPP → SQ_CPM_NEWPAY_TBL.AN_LV_EARNED_CPP → CPM_NEWPAY_TBL.AN_LV_EARNED_CPP | CPM_NEWPAY_TBL.AN_LV_EARNED_CPP |
| cdcskel_WS_PAY_OUT_REC | AN_LV_USED_CPP | exp_Final.AN_LV_USED_CPP → exp_Convert.o_AN_LV_USED_CPP = ABS(AN_LV_USED_CPP) → exp_Init.AN_LV_USED_CPP → SQ_CPM_NEWPAY_TBL.AN_LV_USED_CPP → CPM_NEWPAY_TBL.AN_LV_USED_CPP | CPM_NEWPAY_TBL.AN_LV_USED_CPP |
| cdcskel_WS_PAY_OUT_REC | AN_LV_USED_CPP_SIGN | exp_Final.AN_LV_USED_CPP_SIGN → exp_Convert.o_AN_LV_USED_CPP_SIGN = IIF(SIGN(AN_LV_USED_CPP) = -1, '-', '+') → exp_Init.AN_LV_USED_CPP → SQ_CPM_NEWPAY_TBL.AN_LV_USED_CPP → CPM_NEWPAY_TBL.AN_LV_USED_CPP | CPM_NEWPAY_TBL.AN_LV_USED_CPP |
| cdcskel_WS_PAY_OUT_REC | AN_LV_PRYR_BAL | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | AN_LV_PRYR_BAL_SIGN | exp_Final.AN_LV_PRYR_BAL_SIGN → exp_Convert.o_AN_LV_PRYR_BAL_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | AN_LV_ERND_YTD | exp_Final.AN_LV_ERND_YTD → exp_Convert.o_AN_LV_ERND_YTD = ABS(AN_LV_ERND_YTD) → exp_Init.AN_LV_ERND_YTD → SQ_CPM_NEWPAY_TBL.AN_LV_ERND_YTD → CPM_NEWPAY_TBL.AN_LV_ERND_YTD | CPM_NEWPAY_TBL.AN_LV_ERND_YTD |
| cdcskel_WS_PAY_OUT_REC | AN_LV_ERND_YTD_SIGN | exp_Final.AN_LV_ERND_YTD_SIGN → exp_Convert.o_AN_LV_ERND_YTD_SIGN = IIF(SIGN(AN_LV_ERND_YTD) = -1, '-', '+') → exp_Init.AN_LV_ERND_YTD → SQ_CPM_NEWPAY_TBL.AN_LV_ERND_YTD → CPM_NEWPAY_TBL.AN_LV_ERND_YTD | CPM_NEWPAY_TBL.AN_LV_ERND_YTD |
| cdcskel_WS_PAY_OUT_REC | AN_LV_ADV_CPP | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | AN_LV_ADV_CPP_SIGN | exp_Final.AN_LV_ADV_CPP_SIGN → exp_Convert.o_AN_LV_ADV_CPP_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | AN_LV_ADV_CBAL | exp_Final.AN_LV_ADV_CBAL → exp_Convert.o_AN_LV_ADV_CBAL = ABS(AN_LV_ADV_CBAL) → exp_Init.AN_LV_ADV_CBAL → SQ_CPM_NEWPAY_TBL.AN_LV_ADV_CBAL → CPM_NEWPAY_TBL.AN_LV_ADV_CBAL | CPM_NEWPAY_TBL.AN_LV_ADV_CBAL |
| cdcskel_WS_PAY_OUT_REC | AN_LV_ADV_CBAL_SIGN | exp_Final.AN_LV_ADV_CBAL_SIGN → exp_Convert.o_AN_LV_ADV_CBAL_SIGN = IIF(SIGN(AN_LV_ADV_CBAL) = -1, '-', '+') → exp_Init.AN_LV_ADV_CBAL → SQ_CPM_NEWPAY_TBL.AN_LV_ADV_CBAL → CPM_NEWPAY_TBL.AN_LV_ADV_CBAL | CPM_NEWPAY_TBL.AN_LV_ADV_CBAL |
| cdcskel_WS_PAY_OUT_REC | AN_LV_USED_YTD | exp_Final.AN_LV_USED_YTD → exp_Convert.o_AN_LV_USED_YTD = ABS(AN_LV_USED_YTD) → exp_Init.AN_LV_USED_YTD → SQ_CPM_NEWPAY_TBL.AN_LV_USED_YTD → CPM_NEWPAY_TBL.AN_LV_USED_YTD | CPM_NEWPAY_TBL.AN_LV_USED_YTD |
| cdcskel_WS_PAY_OUT_REC | AN_LV_USED_YTD_SIGN | exp_Final.AN_LV_USED_YTD_SIGN → exp_Convert.o_AN_LV_USED_YTD_SIGN = IIF(SIGN(AN_LV_USED_YTD) = -1, '-', '+') → exp_Init.AN_LV_USED_YTD → SQ_CPM_NEWPAY_TBL.AN_LV_USED_YTD → CPM_NEWPAY_TBL.AN_LV_USED_YTD | CPM_NEWPAY_TBL.AN_LV_USED_YTD |
| cdcskel_WS_PAY_OUT_REC | AN_LV_CUR_BAL | exp_Final.AN_LV_CUR_BAL → exp_Convert.o_AN_LV_CUR_BAL = ABS(AN_LV_CUR_BAL) → exp_Init.AN_LV_CUR_BAL → SQ_CPM_NEWPAY_TBL.AN_LV_CUR_BAL → CPM_NEWPAY_TBL.AN_LV_CUR_BAL | CPM_NEWPAY_TBL.AN_LV_CUR_BAL |
| cdcskel_WS_PAY_OUT_REC | AN_LV_CUR_BAL_SIGN | exp_Final.AN_LV_CUR_BAL_SIGN → exp_Convert.o_AN_LV_CUR_BAL_SIGN = IIF(SIGN(AN_LV_CUR_BAL) = -1, '-', '+') → exp_Init.AN_LV_CUR_BAL → SQ_CPM_NEWPAY_TBL.AN_LV_CUR_BAL → CPM_NEWPAY_TBL.AN_LV_CUR_BAL | CPM_NEWPAY_TBL.AN_LV_CUR_BAL |
| cdcskel_WS_PAY_OUT_REC | AN_LV_MAX_COVER | exp_Final.AN_LV_MAX_COVER → exp_Convert.o_AN_LV_MAX_COVER = ABS(AN_LV_MAX_COVER) → exp_Init.AN_LV_MAX_COVER → SQ_CPM_NEWPAY_TBL.AN_LV_MAX_COVER → CPM_NEWPAY_TBL.AN_LV_MAX_COVER | CPM_NEWPAY_TBL.AN_LV_MAX_COVER |
| cdcskel_WS_PAY_OUT_REC | AN_LV_MAX_COVER_SIGN | exp_Final.AN_LV_MAX_COVER_SIGN → exp_Convert.o_AN_LV_MAX_COVER_SIGN = IIF(SIGN(AN_LV_MAX_COVER) = -1, '-', '+') → exp_Init.AN_LV_MAX_COVER → SQ_CPM_NEWPAY_TBL.AN_LV_MAX_COVER → CPM_NEWPAY_TBL.AN_LV_MAX_COVER | CPM_NEWPAY_TBL.AN_LV_MAX_COVER |
| cdcskel_WS_PAY_OUT_REC | AN_LV_USE_LOSE | exp_Final.AN_LV_USE_LOSE → exp_Convert.o_AN_LV_USE_LOSE = ABS(AN_LV_USE_LOSE) → exp_Init.AN_LV_USE_LOSE → SQ_CPM_NEWPAY_TBL.AN_LV_USE_LOSE → CPM_NEWPAY_TBL.AN_LV_USE_LOSE | CPM_NEWPAY_TBL.AN_LV_USE_LOSE |
| cdcskel_WS_PAY_OUT_REC | AN_LV_USE_LOSE_SIGN | exp_Final.AN_LV_USE_LOSE_SIGN → exp_Convert.o_AN_LV_USE_LOSE_SIGN = IIF(SIGN(AN_LV_USE_LOSE) = -1, '-', '+') → exp_Init.AN_LV_USE_LOSE → SQ_CPM_NEWPAY_TBL.AN_LV_USE_LOSE → CPM_NEWPAY_TBL.AN_LV_USE_LOSE | CPM_NEWPAY_TBL.AN_LV_USE_LOSE |
| cdcskel_WS_PAY_OUT_REC | AN_LV_PTHRS_WK | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | AN_LV_PTHRS_WK_SIGN | exp_Final.AN_LV_PTHRS_WK_SIGN → exp_Convert.o_AN_LV_PTHRS_WK_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | SICK_LV_ERN_CPP | exp_Final.SICK_LV_ERN_CPP → exp_Convert.o_SICK_LV_ERN_CPP = ABS(SICK_LV_ERN_CPP) → exp_Init.SICK_LV_ERN_CPP → SQ_CPM_NEWPAY_TBL.SICK_LV_ERN_CPP → CPM_NEWPAY_TBL.SICK_LV_ERN_CPP | CPM_NEWPAY_TBL.SICK_LV_ERN_CPP |
| cdcskel_WS_PAY_OUT_REC | SICK_LV_ERN_CPP_SIGN | exp_Final.SICK_LV_ERN_CPP_SIGN → exp_Convert.o_SICK_LV_ERN_CPP_SIGN = IIF(SIGN(SICK_LV_ERN_CPP) = -1, '-', '+') → exp_Init.SICK_LV_ERN_CPP → SQ_CPM_NEWPAY_TBL.SICK_LV_ERN_CPP → CPM_NEWPAY_TBL.SICK_LV_ERN_CPP | CPM_NEWPAY_TBL.SICK_LV_ERN_CPP |
| cdcskel_WS_PAY_OUT_REC | SICK_LV_USD_CPP | exp_Final.SICK_LV_USD_CPP → exp_Convert.o_SICK_LV_USD_CPP = ABS(SICK_LV_USD_CPP) → exp_Init.SICK_LV_USD_CPP → SQ_CPM_NEWPAY_TBL.SICK_LV_USD_CPP → CPM_NEWPAY_TBL.SICK_LV_USD_CPP | CPM_NEWPAY_TBL.SICK_LV_USD_CPP |
| cdcskel_WS_PAY_OUT_REC | SICK_LV_USD_CPP_SIGN | exp_Final.SICK_LV_USD_CPP_SIGN → exp_Convert.o_SICK_LV_USD_CPP_SIGN = IIF(SIGN(SICK_LV_USD_CPP) = -1, '-', '+') → exp_Init.SICK_LV_USD_CPP → SQ_CPM_NEWPAY_TBL.SICK_LV_USD_CPP → CPM_NEWPAY_TBL.SICK_LV_USD_CPP | CPM_NEWPAY_TBL.SICK_LV_USD_CPP |
| cdcskel_WS_PAY_OUT_REC | SICK_LV_PRYR_BL | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | SICK_LV_PRYR_BL_SIGN | exp_Final.SICK_LV_PRYR_BL_SIGN → exp_Convert.o_SICK_LV_PRYR_BL_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | SICK_LV_ERN_YTD | exp_Final.SICK_LV_ERN_YTD → exp_Convert.o_SICK_LV_ERN_YTD = ABS(SICK_LV_ERN_YTD) → exp_Init.SICK_LV_ERN_YTD → SQ_CPM_NEWPAY_TBL.SICK_LV_ERN_YTD → CPM_NEWPAY_TBL.SICK_LV_ERN_YTD | CPM_NEWPAY_TBL.SICK_LV_ERN_YTD |
| cdcskel_WS_PAY_OUT_REC | SICK_LV_ERN_YTD_SIGN | exp_Final.SICK_LV_ERN_YTD_SIGN → exp_Convert.o_SICK_LV_ERN_YTD_SIGN = IIF(SIGN(SICK_LV_ERN_YTD) = -1, '-', '+') → exp_Init.SICK_LV_ERN_YTD → SQ_CPM_NEWPAY_TBL.SICK_LV_ERN_YTD → CPM_NEWPAY_TBL.SICK_LV_ERN_YTD | CPM_NEWPAY_TBL.SICK_LV_ERN_YTD |
| cdcskel_WS_PAY_OUT_REC | SICK_LV_ADV_CPP | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | SICK_LV_ADV_CPP_SIGN | exp_Final.SICK_LV_ADV_CPP_SIGN → exp_Convert.o_SICK_LV_ADV_CPP_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | SICK_LV_AD_CBAL | exp_Final.SICK_LV_AD_CBAL → exp_Convert.o_SICK_LV_AD_CBAL = ABS(SICK_LV_AD_CBAL) → exp_Init.SICK_LV_AD_CBAL → SQ_CPM_NEWPAY_TBL.SICK_LV_AD_CBAL → CPM_NEWPAY_TBL.SICK_LV_AD_CBAL | CPM_NEWPAY_TBL.SICK_LV_AD_CBAL |
| cdcskel_WS_PAY_OUT_REC | SICK_LV_AD_CBAL_SIGN | exp_Final.SICK_LV_AD_CBAL_SIGN → exp_Convert.o_SICK_LV_AD_CBAL_SIGN = IIF(SIGN(SICK_LV_AD_CBAL) = -1, '-', '+') → exp_Init.SICK_LV_AD_CBAL → SQ_CPM_NEWPAY_TBL.SICK_LV_AD_CBAL → CPM_NEWPAY_TBL.SICK_LV_AD_CBAL | CPM_NEWPAY_TBL.SICK_LV_AD_CBAL |
| cdcskel_WS_PAY_OUT_REC | SICK_LV_USD_YTD | exp_Final.SICK_LV_USD_YTD → exp_Convert.o_SICK_LV_USD_YTD = ABS(SICK_LV_USD_YTD) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(SICK_LV_USD_YTD), 2)), '.', NULL), 7, '0') → exp_Init.SICK_LV_USD_YTD → SQ_CPM_NEWPAY_TBL.SICK_LV_USD_YTD → CPM_NEWPAY_TBL.SICK_LV_USD_YTD | CPM_NEWPAY_TBL.SICK_LV_USD_YTD |
| cdcskel_WS_PAY_OUT_REC | SICK_LV_USD_YTD_SIGN | exp_Final.SICK_LV_USD_YTD_SIGN → exp_Convert.o_SICK_LV_USD_YTD_SIGN = IIF(SIGN(SICK_LV_USD_YTD) = -1, '-', '+') → exp_Init.SICK_LV_USD_YTD → SQ_CPM_NEWPAY_TBL.SICK_LV_USD_YTD → CPM_NEWPAY_TBL.SICK_LV_USD_YTD | CPM_NEWPAY_TBL.SICK_LV_USD_YTD |
| cdcskel_WS_PAY_OUT_REC | SICK_LV_CUR_BAL | exp_Final.SICK_LV_CUR_BAL → exp_Convert.o_SICK_LV_CUR_BAL = ABS(SICK_LV_CUR_BAL) → exp_Init.SICK_LV_CUR_BAL → SQ_CPM_NEWPAY_TBL.SICK_LV_CUR_BAL → CPM_NEWPAY_TBL.SICK_LV_CUR_BAL | CPM_NEWPAY_TBL.SICK_LV_CUR_BAL |
| cdcskel_WS_PAY_OUT_REC | SICK_LV_CUR_BAL_SIGN | exp_Final.SICK_LV_CUR_BAL_SIGN → exp_Convert.o_SICK_LV_CUR_BAL_SIGN = IIF(SIGN(SICK_LV_CUR_BAL) = -1, '-', '+') → exp_Init.SICK_LV_CUR_BAL → SQ_CPM_NEWPAY_TBL.SICK_LV_CUR_BAL → CPM_NEWPAY_TBL.SICK_LV_CUR_BAL | CPM_NEWPAY_TBL.SICK_LV_CUR_BAL |
| cdcskel_WS_PAY_OUT_REC | SICK_LV_PTHR_WK | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | SICK_LV_PTHR_WK_SIGN | exp_Final.SICK_LV_PTHR_WK_SIGN → exp_Convert.o_SICK_LV_PTHR_WK_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | COMP_LV_ERN_CPP | exp_Final.COMP_LV_ERN_CPP → exp_Convert.o_COMP_LV_ERN_CPP = ABS(COMP_LV_ERN_CPP) → exp_Init.COMP_LV_ERN_CPP → SQ_CPM_NEWPAY_TBL.COMP_LV_ERN_CPP → CPM_NEWPAY_TBL.COMP_LV_ERN_CPP | CPM_NEWPAY_TBL.COMP_LV_ERN_CPP |
| cdcskel_WS_PAY_OUT_REC | COMP_LV_ERN_CPP_SIGN | exp_Final.COMP_LV_ERN_CPP_SIGN → exp_Convert.o_COMP_LV_ERN_CPP_SIGN = IIF(SIGN(COMP_LV_ERN_CPP) = -1, '-', '+') → exp_Init.COMP_LV_ERN_CPP → SQ_CPM_NEWPAY_TBL.COMP_LV_ERN_CPP → CPM_NEWPAY_TBL.COMP_LV_ERN_CPP | CPM_NEWPAY_TBL.COMP_LV_ERN_CPP |
| cdcskel_WS_PAY_OUT_REC | COMP_LV_USD_CPP | exp_Final.COMP_LV_USD_CPP → exp_Convert.o_COMP_LV_USD_CPP = ABS(COMP_LV_USD_CPP) → exp_Init.COMP_LV_USD_CPP → SQ_CPM_NEWPAY_TBL.COMP_LV_USD_CPP → CPM_NEWPAY_TBL.COMP_LV_USD_CPP | CPM_NEWPAY_TBL.COMP_LV_USD_CPP |
| cdcskel_WS_PAY_OUT_REC | COMP_LV_USD_CPP_SIGN | exp_Final.COMP_LV_USD_CPP_SIGN → exp_Convert.o_COMP_LV_USD_CPP_SIGN = IIF(SIGN(COMP_LV_USD_CPP) = -1, '-', '+') → exp_Init.COMP_LV_USD_CPP → SQ_CPM_NEWPAY_TBL.COMP_LV_USD_CPP → CPM_NEWPAY_TBL.COMP_LV_USD_CPP | CPM_NEWPAY_TBL.COMP_LV_USD_CPP |
| cdcskel_WS_PAY_OUT_REC | COMP_LV_1 | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | COMP_LV_1_SIGN | exp_Final.COMP_LV_1_SIGN → exp_Convert.COMP_LV_1_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | COMP_LV_2 | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | COMP_LV_2_SIGN | exp_Final.COMP_LV_2_SIGN → exp_Convert.COMP_LV_2_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | COMP_LV_3 | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | COMP_LV_3_SIGN | exp_Final.COMP_LV_3_SIGN → exp_Convert.COMP_LV_3_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | COMP_LV_4 | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | COMP_LV_4_SIGN | exp_Final.COMP_LV_4_SIGN → exp_Convert.COMP_LV_4_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | COMP_LV_5 | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | COMP_LV_5_SIGN | exp_Final.COMP_LV_5_SIGN → exp_Convert.COMP_LV_5_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | COMP_LV_6 | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | COMP_LV_6_SIGN | exp_Final.COMP_LV_6_SIGN → exp_Convert.COMP_LV_6_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | COMP_LV_7 | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | COMP_LV_7_SIGN | exp_Final.COMP_LV_7_SIGN → exp_Convert.COMP_LV_7_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | COMP_LV_8 | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | COMP_LV_8_SIGN | exp_Final.COMP_LV_8_SIGN → exp_Convert.COMP_LV_8_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | COMP_LV_CUR_BAL | exp_Final.COMP_LV_CUR_BAL → exp_Convert.o_COMP_LV_CUR_BAL = ABS(COMP_LV_CUR_BAL) → exp_Init.COMP_LV_CUR_BAL → SQ_CPM_NEWPAY_TBL.COMP_LV_CUR_BAL → CPM_NEWPAY_TBL.COMP_LV_CUR_BAL | CPM_NEWPAY_TBL.COMP_LV_CUR_BAL |
| cdcskel_WS_PAY_OUT_REC | COMP_LV_CUR_BAL_SIGN | exp_Final.COMP_LV_CUR_BAL_SIGN → exp_Convert.o_COMP_LV_CUR_BAL_SIGN = IIF(SIGN(COMP_LV_CUR_BAL) = -1, '-', '+') → exp_Init.COMP_LV_CUR_BAL → SQ_CPM_NEWPAY_TBL.COMP_LV_CUR_BAL → CPM_NEWPAY_TBL.COMP_LV_CUR_BAL | CPM_NEWPAY_TBL.COMP_LV_CUR_BAL |
| cdcskel_WS_PAY_OUT_REC | ADMIN_LV_CPP | exp_Final.ADMIN_LV_CPP → exp_Convert.o_ADMIN_LV_CPP = ABS(ADMIN_LV_CPP) → exp_Init.ADMIN_LV_CPP → SQ_CPM_NEWPAY_TBL.ADMIN_LV_CPP → CPM_NEWPAY_TBL.ADMIN_LV_CPP | CPM_NEWPAY_TBL.ADMIN_LV_CPP |
| cdcskel_WS_PAY_OUT_REC | ADMIN_LV_CPP_SIGN | exp_Final.ADMIN_LV_CPP_SIGN → exp_Convert.o_ADMIN_LV_CPP_SIGN = IIF(SIGN(ADMIN_LV_CPP) = -1, '-', '+') --'+' → exp_Init.ADMIN_LV_CPP → SQ_CPM_NEWPAY_TBL.ADMIN_LV_CPP → CPM_NEWPAY_TBL.ADMIN_LV_CPP | CPM_NEWPAY_TBL.ADMIN_LV_CPP |
| cdcskel_WS_PAY_OUT_REC | ADMIN_LV_YTD | exp_Final.ADMIN_LV_YTD → exp_Convert.o_ADMIN_LV_YTD = ABS(ADMIN_LV_YTD) → exp_Init.ADMIN_LV_YTD → SQ_CPM_NEWPAY_TBL.ADMIN_LV_YTD → CPM_NEWPAY_TBL.ADMIN_LV_YTD | CPM_NEWPAY_TBL.ADMIN_LV_YTD |
| cdcskel_WS_PAY_OUT_REC | ADMIN_LV_YTD_SIGN | exp_Final.ADMIN_LV_YTD_SIGN → exp_Convert.o_ADMIN_LV_YTD_SIGN = IIF(SIGN(ADMIN_LV_YTD) = -1, '-', '+') → exp_Init.ADMIN_LV_YTD → SQ_CPM_NEWPAY_TBL.ADMIN_LV_YTD → CPM_NEWPAY_TBL.ADMIN_LV_YTD | CPM_NEWPAY_TBL.ADMIN_LV_YTD |
| cdcskel_WS_PAY_OUT_REC | MILITARY_LV_CPP | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | MILITARY_LV_CPP_SIGN | exp_Final.MILITARY_LV_CPP_SIGN → exp_Convert.o_MILITARY_LV_CPP_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | MILITARY_LV_YTD | exp_Final.MILITARY_LV_YTD → exp_Convert.o_MILITARY_LV_YTD = ABS(MILITARY_LV_YTD) → exp_Init.MILITARY_LV_YTD → SQ_CPM_NEWPAY_TBL.MILITARY_LV_YTD → CPM_NEWPAY_TBL.MILITARY_LV_YTD | CPM_NEWPAY_TBL.MILITARY_LV_YTD |
| cdcskel_WS_PAY_OUT_REC | MILITARY_LV_YTD_SIGN | exp_Final.MILITARY_LV_YTD_SIGN → exp_Convert.o_MILITARY_LV_YTD_SIGN = IIF(SIGN(MILITARY_LV_YTD) = -1, '-', '+') → exp_Init.MILITARY_LV_YTD → SQ_CPM_NEWPAY_TBL.MILITARY_LV_YTD → CPM_NEWPAY_TBL.MILITARY_LV_YTD | CPM_NEWPAY_TBL.MILITARY_LV_YTD |
| cdcskel_WS_PAY_OUT_REC | COURT_LV_CPP | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | COURT_LV_CPP_SIGN | exp_Final.COURT_LV_CPP_SIGN → exp_Convert.o_COURT_LV_CPP_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | COURT_LV_YTD | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | COURT_LV_YTD_SIGN | exp_Final.COURT_LV_YTD_SIGN → exp_Convert.o_COURT_LV_YTD_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | LWOP_CPP | exp_Final.LWOP_CPP → exp_Convert.o_LWOP_CPP = ABS(LWOP_CPP) → exp_Init.LWOP_CPP → SQ_CPM_NEWPAY_TBL.LWOP_CPP → CPM_NEWPAY_TBL.LWOP_CPP | CPM_NEWPAY_TBL.LWOP_CPP |
| cdcskel_WS_PAY_OUT_REC | LWOP_CPP_SIGN | exp_Final.LWOP_CPP_SIGN → exp_Convert.o_LWOP_CPP_SIGN = IIF(SIGN(LWOP_CPP) = -1, '-', '+') → exp_Init.LWOP_CPP → SQ_CPM_NEWPAY_TBL.LWOP_CPP → CPM_NEWPAY_TBL.LWOP_CPP | CPM_NEWPAY_TBL.LWOP_CPP |
| cdcskel_WS_PAY_OUT_REC | LWOP_YTD | exp_Final.LWOP_YTD → exp_Convert.o_LWOP_YTD = ABS(LWOP_YTD) --LPAD(REPLACECHR(0, TO_CHAR(TO_DECIMAL(ABS(LWOP_YTD), 2)), '.', NULL), 7, '0') → exp_Init.LWOP_YTD → SQ_CPM_NEWPAY_TBL.LWOP_YTD → CPM_NEWPAY_TBL.LWOP_YTD | CPM_NEWPAY_TBL.LWOP_YTD |
| cdcskel_WS_PAY_OUT_REC | LWOP_YTD_SIGN | exp_Final.LWOP_YTD_SIGN → exp_Convert.o_LWOP_YTD_SIGN = IIF(SIGN(LWOP_YTD) = -1, '-', '+') → exp_Init.LWOP_YTD → SQ_CPM_NEWPAY_TBL.LWOP_YTD → CPM_NEWPAY_TBL.LWOP_YTD | CPM_NEWPAY_TBL.LWOP_YTD |
| cdcskel_WS_PAY_OUT_REC | AWOL_CPP | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | AWOL_CPP_SIGN | exp_Final.AWOL_CPP_SIGN → exp_Convert.o_AWOL_CPP_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | AWOL_YTD | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | AWOL_YTD_SIGN | exp_Final.AWOL_YTD_SIGN → exp_Convert.o_AWOL_YTD_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | LWOP_LR | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | LWOP_LR_SIGN | exp_Final.LWOP_LR_SIGN → exp_Convert.o_LWOP_LR_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | OTHER_LV_CPP | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | OTHER_LV_CPP_SIGN | exp_Final.OTHER_LV_CPP_SIGN → exp_Convert.o_OTHER_LV_CPP_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | OTHER_LV_YTD | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | OTHER_LV_YTD_SIGN | exp_Final.OTHER_LV_YTD_SIGN → exp_Convert.o_OTHER_LV_YTD_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | LWOP_AWOP_LSPSI | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | LWOP_AWOP_LSPSI_SIGN | exp_Final.LWOP_AWOP_LSPSI_SIGN → exp_Convert.o_LWOP_AWOP_LSPSI_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | COMP_TIME_FOR_CPP | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | COMP_TIME_FOR_CPP_SIGN | exp_Final.COMP_TIME_FOR_CPP_SIGN → exp_Convert.o_COMP_TIME_FOR_CPP_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | TA_RECD_CDE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | REG_HRS_CPP | exp_Final.REG_HRS_CPP → exp_Convert.o_REG_HRS_CPP = ABS(REG_HRS_CPP) → exp_Init.REG_HRS_CPP → SQ_CPM_NEWPAY_TBL.REG_HRS_CPP → CPM_NEWPAY_TBL.REG_HRS_CPP | CPM_NEWPAY_TBL.REG_HRS_CPP |
| cdcskel_WS_PAY_OUT_REC | REG_HRS_CPP_SIGN | exp_Final.REG_HRS_CPP_SIGN → exp_Convert.o_REG_HRS_CPP_SIGN = IIF(SIGN(REG_HRS_CPP) = -1, '-', '+') → exp_Init.REG_HRS_CPP → SQ_CPM_NEWPAY_TBL.REG_HRS_CPP → CPM_NEWPAY_TBL.REG_HRS_CPP | CPM_NEWPAY_TBL.REG_HRS_CPP |
| cdcskel_WS_PAY_OUT_REC | REG_HRS_YTD | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | REG_HRS_YTD_SIGN | exp_Final.REG_HRS_YTD_SIGN → exp_Convert.o_REG_HRS_YTD_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | HRS_OT_1 | exp_Final.HRS_OT_1 → exp_Convert.o_HRS_OT_1 = ABS(HRS_OT_1) → exp_Init.HRS_OT_1 → SQ_CPM_NEWPAY_TBL.HRS_OT_1 → CPM_NEWPAY_TBL.HRS_OT_1 | CPM_NEWPAY_TBL.HRS_OT_1 |
| cdcskel_WS_PAY_OUT_REC | HRS_OT_1_SIGN | exp_Final.HRS_OT_1_SIGN → exp_Convert.o_HRS_OT_1_SIGN = IIF(SIGN(HRS_OT_1) = -1, '-', '+') → exp_Init.HRS_OT_1 → SQ_CPM_NEWPAY_TBL.HRS_OT_1 → CPM_NEWPAY_TBL.HRS_OT_1 | CPM_NEWPAY_TBL.HRS_OT_1 |
| cdcskel_WS_PAY_OUT_REC | HRS_OT_2 | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | HRS_OT_2_SIGN | exp_Final.HRS_OT_2_SIGN → exp_Convert.o_HRS_OT_2_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | HRS_OT_3 | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | HRS_OT_3_SIGN | exp_Final.HRS_OT_3_SIGN → exp_Convert.o_HRS_OT_3_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | HRS_OT_YTD | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | HRS_OT_YTD_SIGN | exp_Final.HRS_OT_YTD_SIGN → exp_Convert.o_HRS_OT_YTD_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | HRS_ND_1 | exp_Final.HRS_ND_1 → exp_Convert.o_HRS_ND_1 = ABS(HRS_ND_1) → exp_Init.HRS_ND_1 → SQ_CPM_NEWPAY_TBL.HRS_ND_1 → CPM_NEWPAY_TBL.HRS_ND_1 | CPM_NEWPAY_TBL.HRS_ND_1 |
| cdcskel_WS_PAY_OUT_REC | HRS_ND_1_SIGN | exp_Final.HRS_ND_1_SIGN → exp_Convert.o_HRS_ND_1_SIGN = IIF(SIGN(HRS_ND_1) = -1, '-', '+') → exp_Init.HRS_ND_1 → SQ_CPM_NEWPAY_TBL.HRS_ND_1 → CPM_NEWPAY_TBL.HRS_ND_1 | CPM_NEWPAY_TBL.HRS_ND_1 |
| cdcskel_WS_PAY_OUT_REC | HRS_ND_2 | exp_Final.HRS_ND_2 → exp_Convert.o_HRS_ND_2 = ABS(HRS_ND_2) → exp_Init.HRS_ND_2 → SQ_CPM_NEWPAY_TBL.HRS_ND_2 → CPM_NEWPAY_TBL.HRS_ND_2 | CPM_NEWPAY_TBL.HRS_ND_2 |
| cdcskel_WS_PAY_OUT_REC | HRS_ND_2_SIGN | exp_Final.HRS_ND_2_SIGN → exp_Convert.o_HRS_ND_2_SIGN = IIF(SIGN(HRS_ND_2) = -1, '-', '+') → exp_Init.HRS_ND_2 → SQ_CPM_NEWPAY_TBL.HRS_ND_2 → CPM_NEWPAY_TBL.HRS_ND_2 | CPM_NEWPAY_TBL.HRS_ND_2 |
| cdcskel_WS_PAY_OUT_REC | HRS_ND_3 | exp_Final.HRS_ND_3 → exp_Convert.o_HRS_ND_3 = ABS(HRS_ND_3) → exp_Init.HRS_ND_3 → SQ_CPM_NEWPAY_TBL.HRS_ND_3 → CPM_NEWPAY_TBL.HRS_ND_3 | CPM_NEWPAY_TBL.HRS_ND_3 |
| cdcskel_WS_PAY_OUT_REC | HRS_ND_3_SIGN | exp_Final.HRS_ND_3_SIGN → exp_Convert.o_HRS_ND_3_SIGN = IIF(SIGN(HRS_ND_3) = -1, '-', '+') → exp_Init.HRS_ND_3 → SQ_CPM_NEWPAY_TBL.HRS_ND_3 → CPM_NEWPAY_TBL.HRS_ND_3 | CPM_NEWPAY_TBL.HRS_ND_3 |
| cdcskel_WS_PAY_OUT_REC | HRS_ND_YTD | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | HRS_ND_YTD_SIGN | exp_Final.HRS_ND_YTD_SIGN → exp_Convert.o_HRS_ND_YTD_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | HRS_SD_1 | exp_Final.HRS_SD_1 → exp_Convert.o_HRS_SD_1 = ABS(HRS_SD_1) → exp_Init.HRS_SD_1 → SQ_CPM_NEWPAY_TBL.HRS_SD_1 → CPM_NEWPAY_TBL.HRS_SD_1 | CPM_NEWPAY_TBL.HRS_SD_1 |
| cdcskel_WS_PAY_OUT_REC | HRS_SD_1_SIGN | exp_Final.HRS_SD_1_SIGN → exp_Convert.o_HRS_SD_1_SIGN = IIF(SIGN(HRS_SD_1) = -1, '-', '+') → exp_Init.HRS_SD_1 → SQ_CPM_NEWPAY_TBL.HRS_SD_1 → CPM_NEWPAY_TBL.HRS_SD_1 | CPM_NEWPAY_TBL.HRS_SD_1 |
| cdcskel_WS_PAY_OUT_REC | HRS_SD_2 | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | HRS_SD_2_SIGN | exp_Final.HRS_SD_2_SIGN → exp_Convert.o_HRS_SD_2_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | HRS_SD_3 | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | HRS_SD_3_SIGN | exp_Final.HRS_SD_3_SIGN → exp_Convert.o_HRS_SD_3_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | HRS_SD_YTD | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | HRS_SD_YTD_SIGN | exp_Final.HRS_SD_YTD_SIGN → exp_Convert.o_HRS_SD_YTD_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | HRS_HOL_1 | exp_Final.HRS_HOL_1 → exp_Convert.o_HRS_HOL_1 = ABS(HRS_HOL_1) → exp_Init.HRS_HOL_1 → SQ_CPM_NEWPAY_TBL.HRS_HOL_1 → CPM_NEWPAY_TBL.HRS_HOL_1 | CPM_NEWPAY_TBL.HRS_HOL_1 |
| cdcskel_WS_PAY_OUT_REC | HRS_HOL_1_SIGN | exp_Final.HRS_HOL_1_SIGN → exp_Convert.o_HRS_HOL_1_SIGN = IIF(SIGN(HRS_HOL_1) = -1, '-', '+') → exp_Init.HRS_HOL_1 → SQ_CPM_NEWPAY_TBL.HRS_HOL_1 → CPM_NEWPAY_TBL.HRS_HOL_1 | CPM_NEWPAY_TBL.HRS_HOL_1 |
| cdcskel_WS_PAY_OUT_REC | HRS_HOL_2 | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | HRS_HOL_2_SIGN | exp_Final.HRS_HOL_2_SIGN → exp_Convert.o_HRS_HOL_2_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | HRS_HOL_3 | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | HRS_HOL_3_SIGN | exp_Final.HRS_HOL_3_SIGN → exp_Convert.o_HRS_HOL_3_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | HRS_HOL_YTD | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | HRS_HOL_YTD_SIGN | exp_Final.HRS_HOL_YTD_SIGN → exp_Convert.o_HRS_HOL_YTD_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | HRS_OTHER_CPP | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | HRS_OTHER_CPP_SIGN | exp_Final.HRS_OTHER_CPP_SIGN → exp_Convert.o_HRS_OTHER_CPP_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | HRS_OTHER_YTD | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | HRS_OTHER_YTD_SIGN | exp_Final.HRS_OTHER_YTD_SIGN → exp_Convert.o_HRS_OTHER_YTD_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | DAYS_INTER_CPP | exp_Final.DAYS_INTER_CPP → exp_Convert.o_DAYS_INTER_CPP = '00' | literal/expression: '00' |
| cdcskel_WS_PAY_OUT_REC | DAYS_INTER_YTD | exp_Final.DAYS_INTER_YTD → exp_Convert.o_DAYS_INTER_YTD = '000' | literal/expression: '000' |
| cdcskel_WS_PAY_OUT_REC | DAYS_INTER_CBAL | exp_Final.DAYS_INTER_CBAL → exp_Convert.o_DAYS_INTER_CBAL = '000' | literal/expression: '000' |
| cdcskel_WS_PAY_OUT_REC | SPEC_REG_HRS | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | SPEC_REG_HRS_SIGN | exp_Final.SPEC_REG_HRS_SIGN → exp_Convert.o_SPEC_REG_HRS_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | HRS_OT_PL | exp_Final.HRS_OT_PL → exp_Convert.o_HRS_OT_PL = ABS(HRS_OT_PL) → exp_Init.HRS_OT_PL → SQ_CPM_NEWPAY_TBL.HRS_OT_PL → CPM_NEWPAY_TBL.HRS_OT_PL | CPM_NEWPAY_TBL.HRS_OT_PL |
| cdcskel_WS_PAY_OUT_REC | HRS_OT_PL_SIGN | exp_Final.HRS_OT_PL_SIGN → exp_Convert.o_HRS_OT_PL_SIGN = IIF(SIGN(HRS_OT_PL) = -1, '-', '+') → exp_Init.HRS_OT_PL → SQ_CPM_NEWPAY_TBL.HRS_OT_PL → CPM_NEWPAY_TBL.HRS_OT_PL | CPM_NEWPAY_TBL.HRS_OT_PL |
| cdcskel_WS_PAY_OUT_REC | HRS_OT_SPEC | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | HRS_OT_SPEC_SIGN | exp_Final.HRS_OT_SPEC_SIGN → exp_Convert.o_HRS_OT_SPEC_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | BOND_NOTE_TOT_PUR_PR | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | BOND_NOTE_TOT_PUR_PR_SIGN | exp_Final.BOND_NOTE_TOT_PUR_PR_SIGN → exp_Convert.o_BOND_NOTE_TOT_PUR_PR_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | BOND_NOTE_TOT_DED | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | BOND_NOTE_TOT_DED_SIGN | exp_Final.BOND_NOTE_TOT_DED_SIGN → exp_Convert.o_BOND_NOTE_TOT_DED_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | BOND_NOTE_BAL | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | BOND_NOTE_BAL_SIGN | exp_Final.BOND_NOTE_BAL_SIGN → exp_Convert.o_BOND_NOTE_BAL_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | REL_COMP_ERND_CPP | exp_Final.REL_COMP_ERND_CPP → exp_Convert.o_REL_COMP_ERND_CPP = ABS(REL_COMP_ERND_CPP) → exp_Init.REL_COMP_ERND_CPP → SQ_CPM_NEWPAY_TBL.REL_COMP_ERND_CPP → CPM_NEWPAY_TBL.REL_COMP_ERND_CPP | CPM_NEWPAY_TBL.REL_COMP_ERND_CPP |
| cdcskel_WS_PAY_OUT_REC | REL_COMP_ERND_CPP_SIGN | exp_Final.REL_COMP_ERND_CPP_SIGN → exp_Convert.o_REL_COMP_ERND_CPP_SIGN = IIF(SIGN(REL_COMP_ERND_CPP) = -1, '-', '+') → exp_Init.REL_COMP_ERND_CPP → SQ_CPM_NEWPAY_TBL.REL_COMP_ERND_CPP → CPM_NEWPAY_TBL.REL_COMP_ERND_CPP | CPM_NEWPAY_TBL.REL_COMP_ERND_CPP |
| cdcskel_WS_PAY_OUT_REC | REL_COMP_USED_CPP | exp_Final.REL_COMP_USED_CPP → exp_Convert.o_REL_COMP_USED_CPP = ABS(REL_COMP_USED_CPP) → exp_Init.REL_COMP_USED_CPP → SQ_CPM_NEWPAY_TBL.REL_COMP_USED_CPP → CPM_NEWPAY_TBL.REL_COMP_USED_CPP | CPM_NEWPAY_TBL.REL_COMP_USED_CPP |
| cdcskel_WS_PAY_OUT_REC | REL_COMP_USED_CPP_SIGN | exp_Final.REL_COMP_USED_CPP_SIGN → exp_Convert.o_REL_COMP_USED_CPP_SIGN = IIF(SIGN(REL_COMP_USED_CPP) = -1, '-', '+') → exp_Init.REL_COMP_USED_CPP → SQ_CPM_NEWPAY_TBL.REL_COMP_USED_CPP → CPM_NEWPAY_TBL.REL_COMP_USED_CPP | CPM_NEWPAY_TBL.REL_COMP_USED_CPP |
| cdcskel_WS_PAY_OUT_REC | REL_COMP_CURR_BAL | exp_Final.REL_COMP_CURR_BAL → exp_Convert.o_REL_COMP_CURR_BAL = ABS(REL_COMP_CURR_BAL) → exp_Init.REL_COMP_CURR_BAL → SQ_CPM_NEWPAY_TBL.REL_COMP_CURR_BAL → CPM_NEWPAY_TBL.REL_COMP_CURR_BAL | CPM_NEWPAY_TBL.REL_COMP_CURR_BAL |
| cdcskel_WS_PAY_OUT_REC | REL_COMP_CURR_BAL_SIGN | exp_Final.REL_COMP_CURR_BAL_SIGN → exp_Convert.o_REL_COMP_CURR_BAL_SIGN = IIF(SIGN(REL_COMP_CURR_BAL) = -1, '-', '+') → exp_Init.REL_COMP_CURR_BAL → SQ_CPM_NEWPAY_TBL.REL_COMP_CURR_BAL → CPM_NEWPAY_TBL.REL_COMP_CURR_BAL | CPM_NEWPAY_TBL.REL_COMP_CURR_BAL |
| cdcskel_WS_PAY_OUT_REC | CR_HRS_ERND_CPP | exp_Final.CR_HRS_ERND_CPP → exp_Convert.o_CR_HRS_ERND_CPP = ABS(CR_HRS_ERND_CPP) → exp_Init.CR_HRS_ERND_CPP → SQ_CPM_NEWPAY_TBL.CR_HRS_ERND_CPP → CPM_NEWPAY_TBL.CR_HRS_ERND_CPP | CPM_NEWPAY_TBL.CR_HRS_ERND_CPP |
| cdcskel_WS_PAY_OUT_REC | CR_HRS_ERND_CPP_SIGN | exp_Final.CR_HRS_ERND_CPP_SIGN → exp_Convert.o_CR_HRS_ERND_CPP_SIGN = IIF(SIGN(CR_HRS_ERND_CPP) = -1, '-', '+') → exp_Init.CR_HRS_ERND_CPP → SQ_CPM_NEWPAY_TBL.CR_HRS_ERND_CPP → CPM_NEWPAY_TBL.CR_HRS_ERND_CPP | CPM_NEWPAY_TBL.CR_HRS_ERND_CPP |
| cdcskel_WS_PAY_OUT_REC | CR_HRS_USED_CPP | exp_Final.CR_HRS_USED_CPP → exp_Convert.o_CR_HRS_USED_CPP = ABS(CR_HRS_USED_CPP) → exp_Init.CR_HRS_USED_CPP → SQ_CPM_NEWPAY_TBL.CR_HRS_USED_CPP → CPM_NEWPAY_TBL.CR_HRS_USED_CPP | CPM_NEWPAY_TBL.CR_HRS_USED_CPP |
| cdcskel_WS_PAY_OUT_REC | CR_HRS_USED_CPP_SIGN | exp_Final.CR_HRS_USED_CPP_SIGN → exp_Convert.o_CR_HRS_USED_CPP_SIGN = IIF(SIGN(CR_HRS_USED_CPP) = -1, '-', '+') → exp_Init.CR_HRS_USED_CPP → SQ_CPM_NEWPAY_TBL.CR_HRS_USED_CPP → CPM_NEWPAY_TBL.CR_HRS_USED_CPP | CPM_NEWPAY_TBL.CR_HRS_USED_CPP |
| cdcskel_WS_PAY_OUT_REC | CR_HRS_CUR_BAL | exp_Final.CR_HRS_CUR_BAL → exp_Convert.o_CR_HRS_CUR_BAL = ABS(CR_HRS_CUR_BAL) → exp_Init.CR_HRS_CUR_BAL → SQ_CPM_NEWPAY_TBL.CR_HRS_CUR_BAL → CPM_NEWPAY_TBL.CR_HRS_CUR_BAL | CPM_NEWPAY_TBL.CR_HRS_CUR_BAL |
| cdcskel_WS_PAY_OUT_REC | CR_HRS_CUR_BAL_SIGN | exp_Final.CR_HRS_CUR_BAL_SIGN → exp_Convert.o_CR_HRS_CUR_BAL_SIGN = IIF(SIGN(CR_HRS_CUR_BAL) = -1, '-', '+') → exp_Init.CR_HRS_CUR_BAL → SQ_CPM_NEWPAY_TBL.CR_HRS_CUR_BAL → CPM_NEWPAY_TBL.CR_HRS_CUR_BAL | CPM_NEWPAY_TBL.CR_HRS_CUR_BAL |
| cdcskel_WS_PAY_OUT_REC | MIL_LV_ELIG_CDE | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | HOME_LV_CPP | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | HOME_LV_CPP_SIGN | exp_Final.HOME_LV_CPP_SIGN → exp_Convert.o_HOME_LV_CPP_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | HOME_LV_YTD | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | HOME_LV_YTD_SIGN | exp_Final.HOME_LV_YTD_SIGN → exp_Convert.o_HOME_LV_YTD_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | RESTOR_AL_USED_CPP | (not connected — NULL) | — |
| cdcskel_WS_PAY_OUT_REC | RESTOR_AL_USED_CPP_SIGN | exp_Final.RESTOR_AL_USED_CPP_SIGN → exp_Convert.o_RESTOR_AL_USED_CPP_SIGN = '+' | literal/expression: '+' |
| cdcskel_WS_PAY_OUT_REC | RESTOR_AL_USED_YTD | exp_Final.RESTOR_AL_USED_YTD → exp_Convert.o_RESTOR_AL_USED_YTD = ABS(RESTOR_AL_USED_YTD) → exp_Init.RESTOR_AL_USED_YTD → SQ_CPM_NEWPAY_TBL.RESTOR_AL_USED_YTD → CPM_NEWPAY_TBL.RESTOR_AL_USED_YTD | CPM_NEWPAY_TBL.RESTOR_AL_USED_YTD |
| cdcskel_WS_PAY_OUT_REC | RESTOR_AL_USED_YTD_SIGN | exp_Final.RESTOR_AL_USED_YTD_SIGN → exp_Convert.o_RESTOR_AL_USED_YTD_SIGN = IIF(SIGN(RESTOR_AL_USED_YTD) = -1, '-', '+') → exp_Init.RESTOR_AL_USED_YTD → SQ_CPM_NEWPAY_TBL.RESTOR_AL_USED_YTD → CPM_NEWPAY_TBL.RESTOR_AL_USED_YTD | CPM_NEWPAY_TBL.RESTOR_AL_USED_YTD |
| cdcskel_WS_PAY_OUT_REC | RESTOR_AL_BALANCE | exp_Final.RESTOR_AL_BALANCE → exp_Convert.o_RESTOR_AL_BALANCE = ABS(RESTOR_AL_BALANCE) → exp_Init.RESTOR_AL_BALANCE → SQ_CPM_NEWPAY_TBL.RESTOR_AL_BALANCE → CPM_NEWPAY_TBL.RESTOR_AL_BALANCE | CPM_NEWPAY_TBL.RESTOR_AL_BALANCE |
| cdcskel_WS_PAY_OUT_REC | RESTOR_AL_BALANCE_SIGN | exp_Final.RESTOR_AL_BALANCE_SIGN → exp_Convert.o_RESTOR_AL_BALANCE_SIGN = IIF(SIGN(RESTOR_AL_BALANCE) = -1, '-', '+') → exp_Init.RESTOR_AL_BALANCE → SQ_CPM_NEWPAY_TBL.RESTOR_AL_BALANCE → CPM_NEWPAY_TBL.RESTOR_AL_BALANCE | CPM_NEWPAY_TBL.RESTOR_AL_BALANCE |
| cdcskel_WS_PAY_OUT_REC | RESTOR_AL_BAL_1 | exp_Final.RESTOR_AL_BAL_1 → exp_Convert.o_RESTOR_AL_BAL_1 = ABS(RESTOR_AL_BAL_1) → exp_Init.RESTOR_AL_BAL_1 → SQ_CPM_NEWPAY_TBL.RESTOR_AL_BAL_1 → CPM_NEWPAY_TBL.RESTOR_AL_BAL_1 | CPM_NEWPAY_TBL.RESTOR_AL_BAL_1 |
| cdcskel_WS_PAY_OUT_REC | RESTOR_AL_BAL_1_SIGN | exp_Final.RESTOR_AL_BAL_1_SIGN → exp_Convert.o_RESTOR_AL_BAL_1_SIGN = IIF(SIGN(RESTOR_AL_BAL_1) = -1, '-', '+') → exp_Init.RESTOR_AL_BAL_1 → SQ_CPM_NEWPAY_TBL.RESTOR_AL_BAL_1 → CPM_NEWPAY_TBL.RESTOR_AL_BAL_1 | CPM_NEWPAY_TBL.RESTOR_AL_BAL_1 |
| cdcskel_WS_PAY_OUT_REC | RESTOR_AL_BAL_2 | exp_Final.RESTOR_AL_BAL_2 → exp_Convert.o_RESTOR_AL_BAL_2 = ABS(RESTOR_AL_BAL_2) → exp_Init.RESTOR_AL_BAL_2 → SQ_CPM_NEWPAY_TBL.RESTOR_AL_BAL_2 → CPM_NEWPAY_TBL.RESTOR_AL_BAL_2 | CPM_NEWPAY_TBL.RESTOR_AL_BAL_2 |
| cdcskel_WS_PAY_OUT_REC | RESTOR_AL_BAL_2_SIGN | exp_Final.RESTOR_AL_BAL_2_SIGN → exp_Convert.o_RESTOR_AL_BAL_2_SIGN = IIF(SIGN(RESTOR_AL_BAL_2) = -1, '-', '+') → exp_Init.RESTOR_AL_BAL_2 → SQ_CPM_NEWPAY_TBL.RESTOR_AL_BAL_2 → CPM_NEWPAY_TBL.RESTOR_AL_BAL_2 | CPM_NEWPAY_TBL.RESTOR_AL_BAL_2 |
| cdcskel_WS_PAY_OUT_REC | RESTOR_AL_BAL_3 | exp_Final.RESTOR_AL_BAL_3 → exp_Convert.o_RESTOR_AL_BAL_3 = ABS(RESTOR_AL_BAL_3) → exp_Init.RESTOR_AL_BAL_3 → SQ_CPM_NEWPAY_TBL.RESTOR_AL_BAL_3 → CPM_NEWPAY_TBL.RESTOR_AL_BAL_3 | CPM_NEWPAY_TBL.RESTOR_AL_BAL_3 |
| cdcskel_WS_PAY_OUT_REC | RESTOR_AL_BAL_3_SIGN | exp_Final.RESTOR_AL_BAL_3_SIGN → exp_Convert.o_RESTOR_AL_BAL_3_SIGN = IIF(SIGN(RESTOR_AL_BAL_3) = -1, '-', '+') → exp_Init.RESTOR_AL_BAL_3 → SQ_CPM_NEWPAY_TBL.RESTOR_AL_BAL_3 → CPM_NEWPAY_TBL.RESTOR_AL_BAL_3 | CPM_NEWPAY_TBL.RESTOR_AL_BAL_3 |

## Mapping `m_CPM_CDC_Concatenate_Files`

- Sessions: `s_CPM_CDC_Concatenate_Files` (#5)
- Sources: `HI_GENERIC_SRC_TBL`
- Target instances: `GENERIC_TARGET_FILE`

### Transformation `SQ_HI_GENERIC_SRC_TBL` (Source Qualifier)

- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`


### Target instance `GENERIC_TARGET_FILE` (table `GENERIC_TARGET_FILE`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| GENERIC_TARGET_FILE | ID | SQ_HI_GENERIC_SRC_TBL.ID → HI_GENERIC_SRC_TBL.ID | HI_GENERIC_SRC_TBL.ID |

## Mapping `m_CPM_CDC_Build_Message`

- Sessions: `s_CPM_CDC_Build_Message` (#6)
- Sources: `CPM_NEWPAY_TBL`
- Target instances: `CPM_CDC_MESSAGE_FILE`

### Transformation `SQ_CPM_NEWPAY_TBL` (Source Qualifier)

- **Source Filter**: `PP_END_YEAR = TO_NUMBER('$$MAP_PP_END_YEAR') AND PP_NUM = TO_NUMBER('$$MAP_PP_NUM') AND MP_POOL_DES = ' ' AND ( BUSINESS_UNIT IN ('CDC00', 'ATSDR') OR trim(ORG_CDE) in ('ANC34', 'ANC341', 'ANC342', 'ANC343', 'ANC344', 'ANC345') )`
- **Number Of Sorted Ports**: `3`
- **Select Distinct**: `NO`

### Transformation `agg_Count_CPM_CDC` (Aggregator)

- **Sorted Input**: `NO`

### Transformation `lkp_Pay_Period_Total` (Lookup Procedure)

- **Lookup Sql Override**: `SELECT COUNT(*) as COUNT_TOTAL FROM PAY_PERIOD WHERE PP_END_YEAR = TO_NUMBER('$$MAP_PP_END_YEAR') AND PP_NUM = TO_NUMBER('$$MAP_PP_NUM')`
- **Lookup table name**: `PAY_PERIOD`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `COUNT_TOTAL >= in_CONSTANT`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

- Lookup `lkp_Pay_Period_Total`: table `PAY_PERIOD` (exists in export: **True**), condition `COUNT_TOTAL >= in_CONSTANT`, multiple-match policy `Use Any Value`.

### Target instance `CPM_CDC_MESSAGE_FILE` (table `CPM_CDC_MESSAGE_FILE`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| CPM_CDC_MESSAGE_FILE | SUBJECT | exp_Final.SUBJECT → exp_Build_Message.o_SUBJECT = SETVARIABLE($$MAP_SUBJECT, v_SUBJECT) → exp_Build_Message.v_SUBJECT = v_ENVIRONMENT \|\| 'CPM CDC Process Completed Successfully for: ' \|\| TO_CHAR(PP_END_YEAR) \|\| '-' \|\| v_PP_NUM → exp_Build_Message.v_ENVIRONMENT = DECODE(SUBSTR($PMRepositoryServiceName, 1, 4), 'Dev_', 'Dev: ', 'Test', 'Test: ', 'Prod', 'Prod: ') → agg_Count_CPM_CDC.PP_END_YEAR → exp_Initial.PP_END_YEAR → SQ_CPM_NEWPAY_TBL.PP_END_YEAR → CPM_NEWPAY_TBL.PP_END_YEAR → exp_Build_Message.v_PP_NUM = IIF(PP_NUM < 10, LPAD(TO_CHAR(PP_NUM), 2, '0'), TO_CHAR(PP_NUM) ) → agg_Count_CPM_CDC.PP_NUM → exp_Initial.PP_NUM → SQ_CPM_NEWPAY_TBL.PP_NUM → CPM_NEWPAY_TBL.PP_NUM | CPM_NEWPAY_TBL.PP_END_YEAR; CPM_NEWPAY_TBL.PP_NUM; literal/expression: DECODE(SUBSTR($PMRepositoryServiceName, 1, 4), 'Dev_', 'Dev: ', 'Test', 'Test: ', 'Prod', 'Prod: ') |
| CPM_CDC_MESSAGE_FILE | MESSAGE | exp_Final.MESSAGE → exp_Build_Message.o_MESSAGE = SETVARIABLE($$MAP_MESSAGE, v_MESSAGE) → exp_Build_Message.v_MESSAGE = 'Total number of CPM CDC records loaded is: ' \|\| TO_CHAR(v_TOTAL_RECORDS) → exp_Build_Message.v_TOTAL_RECORDS = IIF(ISNULL(lkp_COUNT_HDR_TOTAL), CPM_CDC_TOTAL, CPM_CDC_TOTAL + lkp_COUNT_HDR_TOTAL) → lkp_Pay_Period_Total.COUNT_TOTAL [lookup PAY_PERIOD.COUNT_TOTAL ON COUNT_TOTAL >= in_CONSTANT] → agg_Count_CPM_CDC.o_CPM_CDC_TOTAL = COUNT(*) | PAY_PERIOD.COUNT_TOTAL (lookup); literal/expression: 1 (lookup key); literal/expression: COUNT(*) |

