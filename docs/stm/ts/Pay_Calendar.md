# PowerCenter STM: `Pay_Calendar`

Derived deterministically from `legacy/informatica_ts/Pay_Calendar` by `tools/ts_lineage.py`. Personal identifiers are redacted as `<owner>`, `<path>`, `<email>`.

| Mappings | Sessions | Sources | Targets | Transformations | Mapplets |
|---|---|---|---|---|---|
| 4 | 4 | 1 | 3 | 21 | 0 |

Transformations by type: Expression 10, Lookup Procedure 3, Router 1, Source Qualifier 4, Update Strategy 3

## Workflow `wf_Pay_Calendar`

Session order:

1. `s_Pay_Calendar_Reset_Pay_Calendar` → mapping `m_Pay_Calendar_Reset_Pay_Calendar`
2. `s_Pay_Calendar_Set_Pay_Calendar` → mapping `m_Pay_Calendar_Set_Pay_Calendar`
3. `s_Pay_Calendar_Verify_Pay_Calendar` → mapping `m_Pay_Calendar_Verify_Pay_Calendar`
4. `s_Pay_Calendar_Build_Message` → mapping `m_Pay_Calendar_Build_Message`

| From | To | Condition |
|---|---|---|
| Start | s_Pay_Calendar_Reset_Pay_Calendar | — |
| s_Pay_Calendar_Build_Message | Email_Pay_Calendar | $s_Pay_Calendar_Build_Message.Status = Succeeded |
| s_Pay_Calendar_Verify_Pay_Calendar | s_Pay_Calendar_Build_Message | $s_Pay_Calendar_Verify_Pay_Calendar.Status = Succeeded |
| s_Pay_Calendar_Reset_Pay_Calendar | s_Pay_Calendar_Set_Pay_Calendar | $s_Pay_Calendar_Reset_Pay_Calendar.Status = Succeeded |
| s_Pay_Calendar_Set_Pay_Calendar | s_Pay_Calendar_Verify_Pay_Calendar | $s_Pay_Calendar_Set_Pay_Calendar.Status = Succeeded |

Command tasks:

- `s_Pay_Calendar_Build_Message` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_SUBJECT` = `$$WF_SUBJECT`; `$$MAP_MESSAGE` = `$$WF_MESSAGE`
- `s_Pay_Calendar_Build_Message` / Post-session success variable assignment `postsession_success_variable_assignment`: `$$WF_SUBJECT` = `$$MAP_SUBJECT`; `$$WF_MESSAGE` = `$$MAP_MESSAGE`
- `s_Pay_Calendar_Set_Pay_Calendar` / Pre-session variable assignment `presession_variable_assignment`: `$$PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$PP_NUM` = `$$WF_PP_NUM`
- `s_Pay_Calendar_Set_Pay_Calendar` / Post-session success variable assignment `postsession_success_variable_assignment`: `$$WF_PP_END_YEAR` = `$$PP_END_YEAR`; `$$WF_PP_NUM` = `$$PP_NUM`

- Session `s_Pay_Calendar_Reset_Pay_Calendar`: WRITER `RESET_PAY_PERIOD` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`
- Session `s_Pay_Calendar_Set_Pay_Calendar`: WRITER `PAY_PERIOD_PARAM` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`; WRITER `PAY_PERIOD` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`
- Session `s_Pay_Calendar_Verify_Pay_Calendar`: WRITER `PAY_PERIOD_VERIFY_FILE` Append if Exists=`NO`, Output Type=`File`, Output file directory=`$PMTargetFileDir\`, Output filename=`pay_period_verify_file.txt`
- Session `s_Pay_Calendar_Build_Message`: WRITER `PAY_PERIOD_MESSAGE_FILE` Append if Exists=`NO`, Output Type=`File`, Output file directory=`$PMTargetFileDir\`, Output filename=`pay_period_message_file.txt`

## Source definitions

| Source | Database type | Fields |
|---|---|---|
| PAY_PERIOD | Oracle | 10 |

## Target definitions

| Target | Database type | Fields |
|---|---|---|
| PAY_PERIOD | Oracle | 8 |
| PAY_PERIOD_MESSAGE_FILE | Flat File | 2 |
| PAY_PERIOD_VERIFY_FILE | Flat File | 1 |

## Mapping `m_Pay_Calendar_Reset_Pay_Calendar`

- Sessions: `s_Pay_Calendar_Reset_Pay_Calendar` (#1)
- Sources: `PAY_PERIOD1`
- Target instances: `RESET_PAY_PERIOD`

### Transformation `SQ_PAY_PERIOD_RESET` (Source Qualifier)

- **Source Filter**: `PAY_PERIOD.CURR_PP_FLAG = 'Y'`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `upd_Reset_Current_PP` (Update Strategy)

- **Update Strategy Expression**: `DD_UPDATE`
- **Forward Rejected Rows**: `YES`

- Update Strategy `upd_Reset_Current_PP`: `DD_UPDATE` → RESET_PAY_PERIOD

### Target instance `RESET_PAY_PERIOD` (table `PAY_PERIOD`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| RESET_PAY_PERIOD | PP_NUM | upd_Reset_Current_PP.PP_NUM → exp_Initial.PP_NUM → SQ_PAY_PERIOD_RESET.PP_NUM → PAY_PERIOD1.PP_NUM | PAY_PERIOD1.PP_NUM |
| RESET_PAY_PERIOD | PP_END_YEAR | upd_Reset_Current_PP.PP_END_YEAR → exp_Initial.PP_END_YEAR → SQ_PAY_PERIOD_RESET.PP_END_YEAR → PAY_PERIOD1.PP_END_YEAR | PAY_PERIOD1.PP_END_YEAR |
| RESET_PAY_PERIOD | PP_START_DTE | (not connected — NULL) | — |
| RESET_PAY_PERIOD | PP_END_DTE | (not connected — NULL) | — |
| RESET_PAY_PERIOD | LV_NUM | (not connected — NULL) | — |
| RESET_PAY_PERIOD | LV_YEAR | (not connected — NULL) | — |
| RESET_PAY_PERIOD | PAY_DTE | (not connected — NULL) | — |
| RESET_PAY_PERIOD | CURR_PP_FLAG | upd_Reset_Current_PP.CURR_PP_FLAG → exp_Initial.o_CURR_PP_FLAG = NULL | literal/expression: NULL |

## Mapping `m_Pay_Calendar_Set_Pay_Calendar`

- Sessions: `s_Pay_Calendar_Set_Pay_Calendar` (#2)
- Sources: `PAY_PERIOD1`
- Target instances: `PAY_PERIOD`, `PAY_PERIOD_PARAM`

### Transformation `SQ_PAY_PERIOD` (Source Qualifier)

- **Sql Query**: `SELECT MAX(PAY_PERIOD.PP_NUM) PP_NUM , MAX(PAY_PERIOD.PP_END_YEAR) PP_END_YEAR FROM PAY_PERIOD`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `lkp_Existing_Pay_Period` (Lookup Procedure)

- **Lookup table name**: `PAY_PERIOD`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `PP_NUM = in_PARAM_PP_NUM AND PP_END_YEAR = in_PARAM_PP_END_YEAR`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `lkp_New_Current_Pay_Period` (Lookup Procedure)

- **Lookup table name**: `PAY_PERIOD`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `PP_START_DTE <= in_CURRENT_DATE AND PP_END_DTE >= in_CURRENT_DATE`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `rtr_Parameter_Non_Parameter` (Router)

- Router group `PARAMETERS_EXIST`: `PARAM_EXISTS_FLAG = TRUE`
- Router group `DEFAULT1`: `(default group)`
- Router group `PARAMETERS_NOT_EXIST`: `PARAM_EXISTS_FLAG = FALSE`

### Transformation `upd_Set_Current_PP_Non_Param` (Update Strategy)

- **Update Strategy Expression**: `DD_UPDATE`
- **Forward Rejected Rows**: `YES`

### Transformation `upd_Set_Current_PP_Param` (Update Strategy)

- **Update Strategy Expression**: `DD_UPDATE`
- **Forward Rejected Rows**: `YES`

- Update Strategy `upd_Set_Current_PP_Non_Param`: `DD_UPDATE` → PAY_PERIOD
- Update Strategy `upd_Set_Current_PP_Param`: `DD_UPDATE` → PAY_PERIOD_PARAM
- Lookup `lkp_Existing_Pay_Period`: table `PAY_PERIOD` (exists in export: **True**), condition `PP_NUM = in_PARAM_PP_NUM AND PP_END_YEAR = in_PARAM_PP_END_YEAR`, multiple-match policy `Use Any Value`.
- Lookup `lkp_New_Current_Pay_Period`: table `PAY_PERIOD` (exists in export: **True**), condition `PP_START_DTE <= in_CURRENT_DATE AND PP_END_DTE >= in_CURRENT_DATE`, multiple-match policy `Use Any Value`.
- SQL override `SQ_PAY_PERIOD` positional bindings: 1 → `PP_NUM` = `MAX(PAY_PERIOD.PP_NUM) PP_NUM`; 2 → `PP_END_YEAR` = `MAX(PAY_PERIOD.PP_END_YEAR) PP_END_YEAR`

### Target instance `PAY_PERIOD` (table `PAY_PERIOD`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| PAY_PERIOD | PP_NUM | upd_Set_Current_PP_Non_Param.PP_NUM → exp_Set_Current_Pay_Period_Non_Param.lkp_PP_NUM → lkp_New_Current_Pay_Period.PP_NUM [lookup PAY_PERIOD.PP_NUM ON PP_START_DTE <= in_CURRENT_DATE AND PP_END_DTE >= in_CURRENT_DATE] | PAY_PERIOD.PP_NUM (lookup); literal/expression: TRUNC(SESSSTARTTIME) (lookup key) |
| PAY_PERIOD | PP_END_YEAR | upd_Set_Current_PP_Non_Param.PP_END_YEAR → exp_Set_Current_Pay_Period_Non_Param.lkp_PP_END_YEAR → lkp_New_Current_Pay_Period.PP_END_YEAR [lookup PAY_PERIOD.PP_END_YEAR ON PP_START_DTE <= in_CURRENT_DATE AND PP_END_DTE >= in_CURRENT_DATE] | PAY_PERIOD.PP_END_YEAR (lookup); literal/expression: TRUNC(SESSSTARTTIME) (lookup key) |
| PAY_PERIOD | PP_START_DTE | (not connected — NULL) | — |
| PAY_PERIOD | PP_END_DTE | (not connected — NULL) | — |
| PAY_PERIOD | LV_NUM | (not connected — NULL) | — |
| PAY_PERIOD | LV_YEAR | (not connected — NULL) | — |
| PAY_PERIOD | PAY_DTE | (not connected — NULL) | — |
| PAY_PERIOD | CURR_PP_FLAG | upd_Set_Current_PP_Non_Param.CURR_PP_FLAG → exp_Set_Current_Pay_Period_Non_Param.o_CURR_PP_FLAG = 'Y' | literal/expression: 'Y' |

### Target instance `PAY_PERIOD_PARAM` (table `PAY_PERIOD`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| PAY_PERIOD_PARAM | PP_NUM | upd_Set_Current_PP_Param.PP_NUM → exp_Set_Current_Pay_Period_Param.PP_NUM → rtr_Parameter_Non_Parameter.PARAM_PP_NUM1 [router group PARAMETERS_EXIST WHERE PARAM_EXISTS_FLAG = TRUE] → exp_Determine_Parameters_Exist.PARAM_PP_NUM → exp_Initial.o_PARAM_PP_NUM = v_PARAM_PP_NUM → exp_Initial.v_PARAM_PP_NUM = IIF(NOT IS_NUMBER($$PP_NUM), 0, TO_DECIMAL($$PP_NUM)) → SQ_PAY_PERIOD.PP_NUM → PAY_PERIOD1.PP_NUM | PAY_PERIOD1.PP_NUM |
| PAY_PERIOD_PARAM | PP_END_YEAR | upd_Set_Current_PP_Param.PP_END_YEAR → exp_Set_Current_Pay_Period_Param.PP_END_YEAR → rtr_Parameter_Non_Parameter.PARAM_PP_END_YEAR1 [router group PARAMETERS_EXIST WHERE PARAM_EXISTS_FLAG = TRUE] → exp_Determine_Parameters_Exist.PARAM_PP_END_YEAR → exp_Initial.o_PARAM_PP_END_YEAR = v_PARAM_PP_END_YEAR → exp_Initial.v_PARAM_PP_END_YEAR = IIF(NOT IS_NUMBER($$PP_END_YEAR), 0, TO_DECIMAL($$PP_END_YEAR)) → SQ_PAY_PERIOD.PP_END_YEAR → PAY_PERIOD1.PP_END_YEAR | PAY_PERIOD1.PP_END_YEAR |
| PAY_PERIOD_PARAM | PP_START_DTE | (not connected — NULL) | — |
| PAY_PERIOD_PARAM | PP_END_DTE | (not connected — NULL) | — |
| PAY_PERIOD_PARAM | LV_NUM | (not connected — NULL) | — |
| PAY_PERIOD_PARAM | LV_YEAR | (not connected — NULL) | — |
| PAY_PERIOD_PARAM | PAY_DTE | (not connected — NULL) | — |
| PAY_PERIOD_PARAM | CURR_PP_FLAG | upd_Set_Current_PP_Param.CURR_PP_FLAG → exp_Set_Current_Pay_Period_Param.o_CURR_PP_FLAG = 'Y' | literal/expression: 'Y' |

## Mapping `m_Pay_Calendar_Verify_Pay_Calendar`

- Sessions: `s_Pay_Calendar_Verify_Pay_Calendar` (#3)
- Sources: `PAY_PERIOD1`
- Target instances: `PAY_PERIOD_VERIFY_FILE`

### Transformation `SQ_PAY_PERIOD` (Source Qualifier)

- **Sql Query**: `SELECT MAX(PAY_PERIOD.PP_NUM) PP_NUM , MAX(PAY_PERIOD.PP_END_YEAR) PP_END_YEAR FROM PAY_PERIOD`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `lkp_Current_Pay_Period` (Lookup Procedure)

- **Lookup Sql Override**: `SELECT COUNT(*) as COUNT_CURRENT FROM PAY_PERIOD WHERE CURR_PP_FLAG = 'Y'`
- **Lookup table name**: `PAY_PERIOD`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `COUNT_CURRENT >= in_MIN_PP_NUM`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

- Lookup `lkp_Current_Pay_Period`: table `PAY_PERIOD` (exists in export: **True**), condition `COUNT_CURRENT >= in_MIN_PP_NUM`, multiple-match policy `Use Any Value`.
- SQL override `SQ_PAY_PERIOD` positional bindings: 1 → `PP_NUM` = `MAX(PAY_PERIOD.PP_NUM) PP_NUM`; 2 → `PP_END_YEAR` = `MAX(PAY_PERIOD.PP_END_YEAR) PP_END_YEAR`

### Target instance `PAY_PERIOD_VERIFY_FILE` (table `PAY_PERIOD_VERIFY_FILE`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| PAY_PERIOD_VERIFY_FILE | SUBJECT | exp_Check_Current_Flag.o_CURRENT_FLAG_SET = DECODE(TRUE, v_CURRENT_FLAG_SET = TRUE, '!!!! Current flag has been properly set', v_CURRENT_FLAG_SET = FALSE AND (ISNULL (lkp_COUNT_CURRENT) OR lkp_COUNT_CURRENT = 0), ABORT('!!!! There is no pay period set.'), v_CURRENT_FLAG_SET = FALSE AND lkp_COUNT_CURRENT > 1, ABORT('!!!! There are more than one pay periods set to current.') ) → exp_Check_Current_Flag.v_CURRENT_FLAG_SET = IIF(lkp_COUNT_CURRENT = 1, TRUE, FALSE) → lkp_Current_Pay_Period.COUNT_CURRENT [lookup PAY_PERIOD.COUNT_CURRENT ON COUNT_CURRENT >= in_MIN_PP_NUM] | PAY_PERIOD.COUNT_CURRENT (lookup); literal/expression: 1 (lookup key) |

## Mapping `m_Pay_Calendar_Build_Message`

- Sessions: `s_Pay_Calendar_Build_Message` (#4)
- Sources: `PAY_PERIOD1`
- Target instances: `PAY_PERIOD_MESSAGE_FILE`

### Transformation `SQ_PAY_PERIOD` (Source Qualifier)

- **Source Filter**: `PAY_PERIOD.CURR_PP_FLAG = 'Y'`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`


### Target instance `PAY_PERIOD_MESSAGE_FILE` (table `PAY_PERIOD_MESSAGE_FILE`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| PAY_PERIOD_MESSAGE_FILE | SUBJECT | exp_Final.SUBJECT → exp_Initial.o_SUBJECT = SETVARIABLE($$MAP_SUBJECT, v_SUBJECT) → exp_Initial.v_SUBJECT = v_ENVIRONMENT \|\| 'Pay Calendar Process Completed Successfully for: ' \|\| TO_CHAR(PP_END_YEAR) \|\| '-' \|\| v_PP_NUM → exp_Initial.v_ENVIRONMENT = DECODE(SUBSTR($PMRepositoryServiceName, 1, 4), 'Dev_', 'Dev: ', 'Test', 'Test: ', 'Prod', 'Prod: ') → SQ_PAY_PERIOD.PP_END_YEAR → PAY_PERIOD1.PP_END_YEAR → exp_Initial.v_PP_NUM = IIF(PP_NUM < 10, LPAD(TO_CHAR(PP_NUM), 2, '0'), TO_CHAR(PP_NUM) ) → SQ_PAY_PERIOD.PP_NUM → PAY_PERIOD1.PP_NUM | PAY_PERIOD1.PP_END_YEAR; PAY_PERIOD1.PP_NUM; literal/expression: DECODE(SUBSTR($PMRepositoryServiceName, 1, 4), 'Dev_', 'Dev: ', 'Test', 'Test: ', 'Prod', 'Prod: ') |
| PAY_PERIOD_MESSAGE_FILE | MESSAGE | exp_Final.MESSAGE → exp_Initial.o_MESSAGE = SETVARIABLE($$MAP_MESSAGE, v_MESSAGE) → exp_Initial.v_MESSAGE = 'Current Pay Period = ' \|\| v_PP_NUM \|\| CHR(10) \|\| 'Begin Date = ' \|\| TO_CHAR(PP_START_DTE, 'MM/DD/YYYY') \|\| CHR(10) \|\| 'End Date = ' \|\| TO_CHAR(PP_END_DTE, 'MM/DD/YYYY') → exp_Initial.v_PP_NUM = IIF(PP_NUM < 10, LPAD(TO_CHAR(PP_NUM), 2, '0'), TO_CHAR(PP_NUM) ) → SQ_PAY_PERIOD.PP_NUM → PAY_PERIOD1.PP_NUM → SQ_PAY_PERIOD.PP_START_DTE → PAY_PERIOD1.PP_START_DTE → SQ_PAY_PERIOD.PP_END_DTE → PAY_PERIOD1.PP_END_DTE | PAY_PERIOD1.PP_END_DTE; PAY_PERIOD1.PP_NUM; PAY_PERIOD1.PP_START_DTE |

