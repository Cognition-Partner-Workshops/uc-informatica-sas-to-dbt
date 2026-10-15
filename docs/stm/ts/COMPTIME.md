# PowerCenter STM: `COMP_TIME`

Derived deterministically from `legacy/informatica_ts/COMPTIME` by `tools/ts_lineage.py`. Personal identifiers are redacted as `<owner>`, `<path>`, `<email>`.

| Mappings | Sessions | Sources | Targets | Transformations | Mapplets |
|---|---|---|---|---|---|
| 3 | 3 | 2 | 4 | 19 | 0 |

Transformations by type: Aggregator 1, Expression 11, Filter 2, Lookup Procedure 2, Source Qualifier 3

## Workflow `wf_COMPTIME`

Session order:

1. `s_COMPTIME_Current_Pay_Period` → mapping `m_COMPTIME_Current_Pay_Period`
2. `s_COMPTIME_Load_COMP_TIME_DAILY_TBL` → mapping `m_COMPTIME_Load_COMP_TIME_DAILY_TBL`
3. `s_COMPTIME_Build_Message_Counters` → mapping `m_COMPTIME_Build_Message_Counters`

| From | To | Condition |
|---|---|---|
| Start | s_COMPTIME_Current_Pay_Period | — |
| s_COMPTIME_Load_COMP_TIME_DAILY_TBL | s_COMPTIME_Build_Message_Counters | $s_COMPTIME_Load_COMP_TIME_DAILY_TBL.Status = Succeeded |
| s_COMPTIME_Current_Pay_Period | s_COMPTIME_Load_COMP_TIME_DAILY_TBL | $s_COMPTIME_Current_Pay_Period.Status = Succeeded |
| s_COMPTIME_Build_Message_Counters | email_COMPTIME_Complete | $s_COMPTIME_Build_Message_Counters.Status = Succeeded |

Command tasks:

- `s_COMPTIME_Current_Pay_Period` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`; `$$MAP_PP_YEAR_NUM` = `$$WF_PP_YEAR_NUM`
- `s_COMPTIME_Current_Pay_Period` / Post-session success variable assignment `postsession_success_variable_assignment`: `$$WF_PP_END_YEAR` = `$$MAP_PP_END_YEAR`; `$$WF_PP_NUM` = `$$MAP_PP_NUM`; `$$WF_PP_YEAR_NUM` = `$$MAP_PP_YEAR_NUM`
- `s_COMPTIME_Build_Message_Counters` / Post-session success command `post_session_success_command`: `Command1` = `mv $Param_Root_Directory/data/int/in/COMPTIME/$Param_COMPTIME_filename $Param_Root_Directory/data/archive/COMPTIME/u0827d01_P$$WF_PP_YEAR_NUM.txt`
- `s_COMPTIME_Build_Message_Counters` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_SUBJECT` = `$$WF_SUBJECT`; `$$MAP_MESSAGE` = `$$WF_MESSAGE`
- `s_COMPTIME_Build_Message_Counters` / Post-session success variable assignment `postsession_success_variable_assignment`: `$$WF_SUBJECT` = `$$MAP_SUBJECT`; `$$WF_MESSAGE` = `$$MAP_MESSAGE`

- Session `s_COMPTIME_Current_Pay_Period`: WRITER `COMP_TIME_DATE_FILE` Append if Exists=`NO`, Output Type=`File`, Output file directory=`$PMTargetFileDir\`, Output filename=`comp_time_date_file.txt`
- Session `s_COMPTIME_Load_COMP_TIME_DAILY_TBL`: READER `U0287D01` Input Type=`File`, Source file directory=`$Param_Root_Directory/data/int/in/COMPTIME`, Source filename=`$Param_COMPTIME_filename`; WRITER `COMP_TIME_DAILY_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`
- Session `s_COMPTIME_Build_Message_Counters`: WRITER `COUNTER_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`; WRITER `COMPTIME_MESSAGE_FILE` Append if Exists=`NO`, Output Type=`File`, Output file directory=`$PMTargetFileDir\`, Output filename=`comptime_message_file.txt`; READER `U0287D01` Input Type=`File`, Source file directory=`$Param_Root_Directory/data/int/in/COMPTIME`, Source filename=`$Param_COMPTIME_filename`

## Source definitions

| Source | Database type | Fields |
|---|---|---|
| PAY_PERIOD | Oracle | 10 |
| U0287D01 | Flat File | 12 |

## Target definitions

| Target | Database type | Fields |
|---|---|---|
| COMPTIME_MESSAGE_FILE | Flat File | 2 |
| COMP_TIME_DAILY_TBL | Oracle | 15 |
| COMP_TIME_DATE_FILE | Flat File | 1 |
| COUNTER_TBL | Oracle | 7 |

## Mapping `m_COMPTIME_Current_Pay_Period`

- Sessions: `s_COMPTIME_Current_Pay_Period` (#1)
- Sources: `PAY_PERIOD`
- Target instances: `COMP_TIME_DATE_FILE`

### Transformation `SQ_PAY_PERIOD` (Source Qualifier)

- **Source Filter**: `CURR_PP_FLAG = 'Y'`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`


### Target instance `COMP_TIME_DATE_FILE` (table `COMP_TIME_DATE_FILE`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| COMP_TIME_DATE_FILE | PAY_PERIOD | exp_Final.PAY_PERIOD → exp_Build_Pay_Period.o_PAY_PERIOD = TO_CHAR(PP_END_YEAR) \|\| v_PP_NUM → SQ_PAY_PERIOD.PP_END_YEAR → PAY_PERIOD.PP_END_YEAR → exp_Build_Pay_Period.v_PP_NUM = IIF(PP_NUM < 10, LPAD(TO_CHAR(PP_NUM), 2, '0'), TO_CHAR(PP_NUM) ) → SQ_PAY_PERIOD.PP_NUM → PAY_PERIOD.PP_NUM | PAY_PERIOD.PP_END_YEAR; PAY_PERIOD.PP_NUM |

## Mapping `m_COMPTIME_Load_COMP_TIME_DAILY_TBL`

- Sessions: `s_COMPTIME_Load_COMP_TIME_DAILY_TBL` (#2)
- Sources: `U0287D01`
- Target instances: `COMP_TIME_DAILY_TBL`

### Transformation `SQ_U0287D01` (Source Qualifier)

- **Number Of Sorted Ports**: `0`

### Transformation `fil_Valid_Records` (Filter)

- **Filter Condition**: `VALID_RECORD_FLAG = TRUE`

### Transformation `lkp_PAY_PERIOD` (Lookup Procedure)

- **Lookup table name**: `PAY_PERIOD`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `CURR_PP_FLAG = in_CURR_PP_FLAG`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

- Lookup `lkp_PAY_PERIOD`: table `PAY_PERIOD` (exists in export: **True**), condition `CURR_PP_FLAG = in_CURR_PP_FLAG`, multiple-match policy `Use Any Value`.

### Target instance `COMP_TIME_DAILY_TBL` (table `COMP_TIME_DAILY_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| COMP_TIME_DAILY_TBL | PP_END_YEAR | exp_Final.PP_END_YEAR → exp_Convert.o_PP_END_YEAR = lkp_PP_END_YEAR → lkp_PAY_PERIOD.PP_END_YEAR [lookup PAY_PERIOD.PP_END_YEAR ON CURR_PP_FLAG = in_CURR_PP_FLAG] | PAY_PERIOD.PP_END_YEAR (lookup); literal/expression: 'Y' (lookup key) |
| COMP_TIME_DAILY_TBL | PP_NUM | exp_Final.PP_NUM → exp_Convert.o_PP_NUM = lkp_PP_NUM → lkp_PAY_PERIOD.PP_NUM [lookup PAY_PERIOD.PP_NUM ON CURR_PP_FLAG = in_CURR_PP_FLAG] | PAY_PERIOD.PP_NUM (lookup); literal/expression: 'Y' (lookup key) |
| COMP_TIME_DAILY_TBL | PP_YEAR_NUM | exp_Final.PP_YEAR_NUM → exp_Convert.o_PP_YEAR_NUM = TO_DECIMAL( TO_CHAR(lkp_PP_END_YEAR) \|\| LPAD(TO_CHAR(lkp_PP_NUM), 2, '0')) → lkp_PAY_PERIOD.PP_END_YEAR [lookup PAY_PERIOD.PP_END_YEAR ON CURR_PP_FLAG = in_CURR_PP_FLAG] → lkp_PAY_PERIOD.PP_NUM [lookup PAY_PERIOD.PP_NUM ON CURR_PP_FLAG = in_CURR_PP_FLAG] | PAY_PERIOD.PP_END_YEAR (lookup); PAY_PERIOD.PP_NUM (lookup); literal/expression: 'Y' (lookup key) |
| COMP_TIME_DAILY_TBL | SSN | exp_Final.SSN → exp_Convert.SSN → fil_Valid_Records.SSN → exp_Initial.SSN → SQ_U0287D01.SSN → U0287D01.SSN | U0287D01.SSN |
| COMP_TIME_DAILY_TBL | NAME | exp_Final.NAME → exp_Convert.NAME → fil_Valid_Records.NAME → exp_Initial.NAME → SQ_U0287D01.NAME → U0287D01.NAME | U0287D01.NAME |
| COMP_TIME_DAILY_TBL | CURRENT_ACCT | exp_Final.CURRENT_ACCT → exp_Convert.CURRENT_ACCT → fil_Valid_Records.CURRENT_ACCT → exp_Initial.CURRENT_ACCT → SQ_U0287D01.CURRENT_ACCT → U0287D01.CURRENT_ACCT | U0287D01.CURRENT_ACCT |
| COMP_TIME_DAILY_TBL | CURRENT_ORG | exp_Final.CURRENT_ORG → exp_Convert.CURRENT_ORG → fil_Valid_Records.CURRENT_ORG → exp_Initial.CURRENT_ORG → SQ_U0287D01.CURRENT_ORG → U0287D01.CURRENT_ORG | U0287D01.CURRENT_ORG |
| COMP_TIME_DAILY_TBL | FLSA_STATUS | exp_Final.FLSA_STATUS → exp_Convert.FLSA_STATUS → fil_Valid_Records.FLSA_STATUS → exp_Initial.FLSA_STATUS → SQ_U0287D01.FLSA_STATUS → U0287D01.FLSA_STATUS | U0287D01.FLSA_STATUS |
| COMP_TIME_DAILY_TBL | COMP_TIME_CUR_BAL | exp_Final.COMP_TIME_CUR_BAL → exp_Convert.COMP_TIME_CUR_BAL → fil_Valid_Records.COMP_TIME_CUR_BAL → exp_Initial.COMP_TIME_CUR_BAL → SQ_U0287D01.COMP_TIME_CUR_BAL → U0287D01.COMP_TIME_CUR_BAL | U0287D01.COMP_TIME_CUR_BAL |
| COMP_TIME_DAILY_TBL | COMP_TIME_YEAR_EARNED | exp_Final.COMP_TIME_YEAR_EARNED → exp_Convert.COMP_TIME_YEAR_EARNED → fil_Valid_Records.COMP_TIME_YEAR_EARNED → exp_Initial.COMP_TIME_YEAR_EARNED → SQ_U0287D01.COMP_TIME_YEAR_EARNED → U0287D01.COMP_TIME_YEAR_EARNED | U0287D01.COMP_TIME_YEAR_EARNED |
| COMP_TIME_DAILY_TBL | PP_END_DATE | exp_Final.PP_END_DATE → exp_Convert.o_PP_END_DATE = IIF(IS_DATE(PP_END_DATE, 'YYYYMMDD'), TO_DATE(PP_END_DATE, 'YYYYMMDD') ) → fil_Valid_Records.PP_END_DATE → exp_Initial.PP_END_DATE → SQ_U0287D01.PP_END_DATE → U0287D01.PP_END_DATE | U0287D01.PP_END_DATE |
| COMP_TIME_DAILY_TBL | DAILY_DATE_EARNED | exp_Final.DAILY_DATE_EARNED → exp_Convert.o_DAILY_DATE_EARNED = IIF(IS_DATE(DAILY_DATE_EARNED, 'YYYYMMDD'), TO_DATE(DAILY_DATE_EARNED, 'YYYYMMDD') ) → fil_Valid_Records.DAILY_DATE_EARNED → exp_Initial.DAILY_DATE_EARNED → SQ_U0287D01.DAILY_DATE_EARNED → U0287D01.DAILY_DATE_EARNED | U0287D01.DAILY_DATE_EARNED |
| COMP_TIME_DAILY_TBL | COMP_TIME_RATE | exp_Final.COMP_TIME_RATE → exp_Convert.COMP_TIME_RATE → fil_Valid_Records.COMP_TIME_RATE → exp_Initial.COMP_TIME_RATE → SQ_U0287D01.COMP_TIME_RATE → U0287D01.COMP_TIME_RATE | U0287D01.COMP_TIME_RATE |
| COMP_TIME_DAILY_TBL | COMP_TIME_HOURS | exp_Final.COMP_TIME_HOURS → exp_Convert.COMP_TIME_HOURS → fil_Valid_Records.COMP_TIME_HOURS → exp_Initial.COMP_TIME_HOURS → SQ_U0287D01.COMP_TIME_HOURS → U0287D01.COMP_TIME_HOURS | U0287D01.COMP_TIME_HOURS |
| COMP_TIME_DAILY_TBL | COMP_TIME_UNDEF | exp_Final.COMP_TIME_UNDEF → exp_Convert.COMP_TIME_UNDEF → fil_Valid_Records.COMP_TIME_UNDEF → exp_Initial.COMP_TIME_UNDEF → SQ_U0287D01.COMP_TIME_UNDEF → U0287D01.COMP_TIME_UNDEF | U0287D01.COMP_TIME_UNDEF |

## Mapping `m_COMPTIME_Build_Message_Counters`

- Sessions: `s_COMPTIME_Build_Message_Counters` (#3)
- Sources: `U0287D01`
- Target instances: `COMPTIME_MESSAGE_FILE`, `COUNTER_TBL`

### Transformation `SQ_U0287D01` (Source Qualifier)

- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `agg_ALL_RECORDS` (Aggregator)

- **Sorted Input**: `NO`

### Transformation `fil_Detail` (Filter)

- **Filter Condition**: `RECORD_TYPE_FLAG = 'D' --RECORD_TYPE_FLAG = 'H' OR`

### Transformation `lkp_PAY_PERIOD` (Lookup Procedure)

- **Lookup table name**: `PAY_PERIOD`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `CURR_PP_FLAG = in_CURR_PP_FLAG`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

- Lookup `lkp_PAY_PERIOD`: table `PAY_PERIOD` (exists in export: **True**), condition `CURR_PP_FLAG = in_CURR_PP_FLAG`, multiple-match policy `Use Any Value`.

### Target instance `COMPTIME_MESSAGE_FILE` (table `COMPTIME_MESSAGE_FILE`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| COMPTIME_MESSAGE_FILE | SUBJECT | exp_Final_Message.SUBJECT → exp_Build_Message.o_SUBJECT = SETVARIABLE($$MAP_SUBJECT, v_SUBJECT) → exp_Build_Message.v_SUBJECT = v_ENVIRONMENT \|\| 'Comp Time File loaded successfully for Pay Period: ' \|\| TO_CHAR(PP_END_YEAR) \|\| '-' \|\| v_PP_NUM → exp_Build_Message.v_ENVIRONMENT = DECODE(SUBSTR($PMRepositoryServiceName, 1, 4), 'Dev_', 'Dev: ', 'Test', 'Test: ', 'Prod', 'Prod: ') → exp_Counters.lkp_PP_END_YEAR → lkp_PAY_PERIOD.PP_END_YEAR [lookup PAY_PERIOD.PP_END_YEAR ON CURR_PP_FLAG = in_CURR_PP_FLAG] → exp_Build_Message.v_PP_NUM = IIF(PP_NUM < 10, LPAD(TO_CHAR(PP_NUM), 2, '0'), TO_CHAR(PP_NUM) ) → exp_Counters.lkp_PP_NUM → lkp_PAY_PERIOD.PP_NUM [lookup PAY_PERIOD.PP_NUM ON CURR_PP_FLAG = in_CURR_PP_FLAG] | PAY_PERIOD.PP_END_YEAR (lookup); PAY_PERIOD.PP_NUM (lookup); literal/expression: 'Y' (lookup key); literal/expression: DECODE(SUBSTR($PMRepositoryServiceName, 1, 4), 'Dev_', 'Dev: ', 'Test', 'Test: ', 'Prod', 'Prod: ') |
| COMPTIME_MESSAGE_FILE | MESSAGE | exp_Final_Message.MESSAGE → exp_Build_Message.o_MESSAGE = SETVARIABLE($$MAP_MESSAGE, v_MESSAGE) → exp_Build_Message.v_MESSAGE = 'Number of Detail Records from Comp Time file = ' \|\| TO_CHAR(COUNTER_1) → exp_Counters.DETAIL_RECORD_COUNT → exp_Detail_Count.DETAIL_RECORD_COUNT → agg_ALL_RECORDS.o_DETAIL_RECORD_COUNT = COUNT(SSN) → fil_Detail.SSN → exp_Initial.SSN → SQ_U0287D01.SSN → U0287D01.SSN | U0287D01.SSN |

### Target instance `COUNTER_TBL` (table `COUNTER_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| COUNTER_TBL | RUN_DATE | exp_Final.o_RUN_DATE = SESSSTARTTIME | literal/expression: SESSSTARTTIME |
| COUNTER_TBL | PROCESS_NAME | exp_Final.o_PROCESS_NAME = $PMMappingName | literal/expression: $PMMappingName |
| COUNTER_TBL | COUNTER_DESCRIPTION | exp_Final.COUNTER_DESCRIPTION → exp_Counters.o_COUNTER_DESCRIPTION_1 = 'Number of detail records from the COMP TIME file.' | literal/expression: 'Number of detail records from the COMP TIME file.' |
| COUNTER_TBL | COUNTER_VALUE | exp_Final.COUNTER_VALUE → exp_Counters.DETAIL_RECORD_COUNT → exp_Detail_Count.DETAIL_RECORD_COUNT → agg_ALL_RECORDS.o_DETAIL_RECORD_COUNT = COUNT(SSN) → fil_Detail.SSN → exp_Initial.SSN → SQ_U0287D01.SSN → U0287D01.SSN | U0287D01.SSN |
| COUNTER_TBL | PP_END_YEAR | (not connected — NULL) | — |
| COUNTER_TBL | PP_NUM | (not connected — NULL) | — |
| COUNTER_TBL | CYCLE_ID | (not connected — NULL) | — |

