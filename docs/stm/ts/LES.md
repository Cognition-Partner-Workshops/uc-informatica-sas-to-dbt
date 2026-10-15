# PowerCenter STM: `LES`

Derived deterministically from `legacy/informatica_ts/LES` by `tools/ts_lineage.py`. Personal identifiers are redacted as `<owner>`, `<path>`, `<email>`.

| Mappings | Sessions | Sources | Targets | Transformations | Mapplets |
|---|---|---|---|---|---|
| 32 | 32 | 36 | 35 | 224 | 0 |

Transformations by type: Aggregator 4, Expression 90, Filter 38, Joiner 17, Lookup Procedure 17, Normalizer 21, Router 1, Sequence 5, Source Qualifier 31

## Workflow `wf_LES`

Session order:

1. `s_LES_Current_Pay_Period` → mapping `m_LES_Current_Pay_Period`
2. `s_LES_Verify_Header` → mapping `m_LES_Verify_Header`
3. `s_LES_Verify_Record_Count` → mapping `m_LES_Verify_Record_Count`
4. `s_LES_Load_LES_HEADER_TBL` → mapping `m_LES_Load_LES_HEADER_TBL`
5. `s_LES_Load_LES_EMP_DETAIL_TBL` → mapping `m_LES_Load_LES_EMP_DETAIL_TBL`
6. `s_LES_Load_LES_EMP_DETAIL_RECTYPE_1_TBL` → mapping `m_LES_Load_LES_EMP_DETAIL_RECTYPE_1_TBL`
7. `s_LES_Load_LES_EMP_DETAIL_RECTYPE_2_TBL` → mapping `m_LES_Load_LES_EMP_DETAIL_RECTYPE_2_TBL`
8. `s_LES_Load_LES_EMP_DETAIL_RECTYPE_3_TBL` → mapping `m_LES_Load_LES_EMP_DETAIL_RECTYPE_3_TBL`
9. `s_LES_Load_LES_EMP_DETAIL_RECTYPE_4_TBL` → mapping `m_LES_Load_LES_EMP_DETAIL_RECTYPE_4_TBL`
10. `s_LES_Load_LES_EMP_DETAIL_RECTYPE_5_TBL` → mapping `m_LES_Load_LES_EMP_DETAIL_RECTYPE_5_TBL`
11. `s_LES_Load_LES_EMP_DETAIL_RECTYPE_6_TBL` → mapping `m_LES_Load_LES_EMP_DETAIL_RECTYPE_6_TBL`
12. `s_LES_Load_LES_EMP_DETAIL_RECTYPE_C_TBL` → mapping `m_LES_Load_LES_EMP_DETAIL_RECTYPE_C_TBL`
13. `s_LES_Load_LES_EMP_DETAIL_RECTYPE_R_TBL` → mapping `m_LES_Load_LES_EMP_DETAIL_RECTYPE_R_TBL`
14. `s_LES_Load_LES_EMP_DETAIL_RECTYPE_D_TBL` → mapping `m_LES_Load_LES_EMP_DETAIL_RECTYPE_D_TBL`
15. `s_LES_Load_LES_EMP_DETAIL_RECTYPE_L_TBL` → mapping `m_LES_Load_LES_EMP_DETAIL_RECTYPE_L_TBL`
16. `s_LES_Load_LES_EMP_DETAIL_RECTYPE_U_TBL` → mapping `m_LES_Load_LES_EMP_DETAIL_RECTYPE_U_TBL`
17. `s_LES_Load_LES_EMP_DETAIL_RECTYPE_M_TBL` → mapping `m_LES_Load_LES_EMP_DETAIL_RECTYPE_M_TBL`
18. `s_LES_Load_LES_EMP_DETAIL_RECTYPE_T_TBL` → mapping `m_LES_Load_LES_EMP_DETAIL_RECTYPE_T_TBL`
19. `s_LES_Load_LES_PRIMARY_DATA_TBL` → mapping `m_LES_Load_LES_PRIMARY_DATA_TBL`
20. `s_LES_Load_LES_EMP_DETAIL_CURR_EARN_TBL` → mapping `m_LES_Load_LES_EMP_DETAIL_CURR_EARN_TBL`
21. `s_LES_Load_LES_EMP_DETAIL_RETRO_EARN_TBL` → mapping `m_LES_Load_LES_EMP_DETAIL_RETRO_EARN_TBL`
22. `s_LES_Load_LES_EMP_DETAIL_LEAVE_TBL` → mapping `m_LES_Load_LES_EMP_DETAIL_LEAVE_TBL`
23. `s_LESRPT_Load_LESC` → mapping `m_LESRPT_Load_LESC`
24. `s_LESRPT_Load_LESD` → mapping `m_LESRPT_Load_LESD`
25. `s_LESRPT_Load_LESL` → mapping `m_LESRPT_Load_LESL`
26. `s_LESRPT_Load_LESM` → mapping `m_LESRPT_Load_LESM`
27. `s_LESRPT_Load_LESR` → mapping `m_LESRPT_Load_LESR`
28. `s_LESRPT_Load_LESS` → mapping `m_LESRPT_Load_LESS`
29. `s_LESRPT_Load_LEST` → mapping `m_LESRPT_Load_LEST`
30. `s_LESRPT_Load_LESU` → mapping `m_LESRPT_Load_LESU`
31. `s_LES_NIH_FILE` → mapping `m_LES_NIH_FILE`
32. `s_LES_Build_Message_Counters` → mapping `m_LES_Build_Message_Counters`

| From | To | Condition |
|---|---|---|
| s_LES_Load_LES_EMP_DETAIL_RECTYPE_6_TBL | s_LES_Load_LES_EMP_DETAIL_RECTYPE_C_TBL | $s_LES_Load_LES_EMP_DETAIL_RECTYPE_6_TBL.Status = Succeeded |
| s_LES_Load_LES_EMP_DETAIL_RECTYPE_U_TBL | s_LES_Load_LES_EMP_DETAIL_RECTYPE_M_TBL | $s_LES_Load_LES_EMP_DETAIL_RECTYPE_U_TBL.Status = Succeeded |
| s_LES_Load_LES_EMP_DETAIL_RECTYPE_5_TBL | s_LES_Load_LES_EMP_DETAIL_RECTYPE_6_TBL | $s_LES_Load_LES_EMP_DETAIL_RECTYPE_5_TBL.Status = Succeeded |
| s_LES_Load_LES_EMP_DETAIL_RECTYPE_D_TBL | s_LES_Load_LES_EMP_DETAIL_RECTYPE_L_TBL | $s_LES_Load_LES_EMP_DETAIL_RECTYPE_D_TBL.Status = Succeeded |
| s_LES_Load_LES_EMP_DETAIL_RECTYPE_L_TBL | s_LES_Load_LES_EMP_DETAIL_RECTYPE_U_TBL | $s_LES_Load_LES_EMP_DETAIL_RECTYPE_L_TBL.Status = Succeeded |
| s_LES_Load_LES_EMP_DETAIL_RECTYPE_C_TBL | s_LES_Load_LES_EMP_DETAIL_RECTYPE_R_TBL | $s_LES_Load_LES_EMP_DETAIL_RECTYPE_C_TBL.Status = Succeeded |
| s_LES_Load_LES_HEADER_TBL | s_LES_Load_LES_EMP_DETAIL_TBL | $s_LES_Load_LES_HEADER_TBL.Status = Succeeded |
| s_LES_Load_LES_EMP_DETAIL_RECTYPE_3_TBL | s_LES_Load_LES_EMP_DETAIL_RECTYPE_4_TBL | $s_LES_Load_LES_EMP_DETAIL_RECTYPE_3_TBL.Status = Succeeded |
| s_LES_Load_LES_EMP_DETAIL_TBL | s_LES_Load_LES_EMP_DETAIL_RECTYPE_1_TBL | $s_LES_Load_LES_EMP_DETAIL_TBL.Status = Succeeded |
| s_LES_Load_LES_EMP_DETAIL_RECTYPE_4_TBL | s_LES_Load_LES_EMP_DETAIL_RECTYPE_5_TBL | $s_LES_Load_LES_EMP_DETAIL_RECTYPE_4_TBL.Status = Succeeded |
| s_LES_Verify_Record_Count | s_LES_Load_LES_HEADER_TBL | $s_LES_Verify_Record_Count.Status = Succeeded |
| s_LES_Load_LES_EMP_DETAIL_RECTYPE_2_TBL | s_LES_Load_LES_EMP_DETAIL_RECTYPE_3_TBL | $s_LES_Load_LES_EMP_DETAIL_RECTYPE_2_TBL.Status = Succeeded |
| s_LES_Load_LES_EMP_DETAIL_RECTYPE_T_TBL | s_LES_Load_LES_PRIMARY_DATA_TBL | $s_LES_Load_LES_EMP_DETAIL_RECTYPE_T_TBL.Status = Succeeded |
| s_LES_Load_LES_EMP_DETAIL_RECTYPE_M_TBL | s_LES_Load_LES_EMP_DETAIL_RECTYPE_T_TBL | $s_LES_Load_LES_EMP_DETAIL_RECTYPE_M_TBL.Status = Succeeded |
| s_LES_Build_Message_Counters | email_LES_Complete | $s_LES_Build_Message_Counters.Status = Succeeded |
| s_LES_Load_LES_EMP_DETAIL_RECTYPE_1_TBL | s_LES_Load_LES_EMP_DETAIL_RECTYPE_2_TBL | $s_LES_Load_LES_EMP_DETAIL_RECTYPE_1_TBL.Status = Succeeded |
| Start | s_LES_Current_Pay_Period | — |
| s_LES_Load_LES_EMP_DETAIL_RECTYPE_R_TBL | s_LES_Load_LES_EMP_DETAIL_RECTYPE_D_TBL | $s_LES_Load_LES_EMP_DETAIL_RECTYPE_R_TBL.Status = Succeeded |
| s_LES_NIH_FILE | s_LES_Build_Message_Counters | $s_LES_NIH_FILE.Status = Succeeded |
| s_LES_Load_LES_PRIMARY_DATA_TBL | s_LES_Load_LES_EMP_DETAIL_CURR_EARN_TBL | $s_LES_Load_LES_PRIMARY_DATA_TBL.Status = Succeeded |
| s_LESRPT_Load_LESU | s_LES_NIH_FILE | $s_LESRPT_Load_LESU.Status = Succeeded |
| s_LES_Load_LES_EMP_DETAIL_CURR_EARN_TBL | s_LES_Load_LES_EMP_DETAIL_RETRO_EARN_TBL | $s_LES_Load_LES_EMP_DETAIL_CURR_EARN_TBL.Status = Succeeded |
| s_LES_Load_LES_EMP_DETAIL_RETRO_EARN_TBL | s_LES_Load_LES_EMP_DETAIL_LEAVE_TBL | $s_LES_Load_LES_EMP_DETAIL_RETRO_EARN_TBL.Status = Succeeded |
| s_LES_Verify_Header | s_LES_Verify_Record_Count | $s_LES_Verify_Header.Status = Succeeded |
| s_LES_Current_Pay_Period | s_LES_Verify_Header | $s_LES_Current_Pay_Period.Status = Succeeded |
| s_LESRPT_Load_LESM | s_LESRPT_Load_LESR | $s_LESRPT_Load_LESM.Status = Succeeded |
| s_LES_Load_LES_EMP_DETAIL_LEAVE_TBL | s_LESRPT_Load_LESC | $s_LES_Load_LES_EMP_DETAIL_LEAVE_TBL.Status = Succeeded |
| s_LESRPT_Load_LEST | s_LESRPT_Load_LESU | $s_LESRPT_Load_LEST.Status = Succeeded |
| s_LESRPT_Load_LESR | s_LESRPT_Load_LESS | $s_LESRPT_Load_LESR.Status = Succeeded |
| s_LESRPT_Load_LESC | s_LESRPT_Load_LESD | $s_LESRPT_Load_LESC.Status = Succeeded |
| s_LESRPT_Load_LESL | s_LESRPT_Load_LESM | $s_LESRPT_Load_LESL.Status = Succeeded |
| s_LESRPT_Load_LESS | s_LESRPT_Load_LEST | $s_LESRPT_Load_LESS.Status = Succeeded |
| s_LESRPT_Load_LESD | s_LESRPT_Load_LESL | $s_LESRPT_Load_LESD.Status = Succeeded |

Command tasks:

- `s_LES_Load_LES_EMP_DETAIL_RECTYPE_C_TBL` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_LES_Load_LES_EMP_DETAIL_RECTYPE_M_TBL` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_LES_Load_LES_EMP_DETAIL_RECTYPE_6_TBL` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_LES_Load_LES_EMP_DETAIL_RECTYPE_L_TBL` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_LES_Load_LES_EMP_DETAIL_RECTYPE_U_TBL` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_LES_Load_LES_EMP_DETAIL_RECTYPE_R_TBL` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_LES_Load_LES_EMP_DETAIL_TBL` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_LES_Load_LES_EMP_DETAIL_RECTYPE_4_TBL` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_LES_Load_LES_EMP_DETAIL_RECTYPE_1_TBL` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_LES_Load_LES_EMP_DETAIL_RECTYPE_5_TBL` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_LES_Load_LES_HEADER_TBL` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_LES_Load_LES_HEADER_TBL` / Post-session success variable assignment `postsession_success_variable_assignment`: `$$WF_PP_END_YEAR` = `$$MAP_PP_END_YEAR`; `$$WF_PP_NUM` = `$$MAP_PP_NUM`
- `s_LES_Load_LES_EMP_DETAIL_RECTYPE_3_TBL` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_LES_Load_LES_PRIMARY_DATA_TBL` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_LES_Load_LES_EMP_DETAIL_RECTYPE_T_TBL` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_LES_Load_LES_EMP_DETAIL_RECTYPE_2_TBL` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_LES_Current_Pay_Period` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`; `$$MAP_PP_YEAR_NUM` = `$$WF_PP_YEAR_NUM`
- `s_LES_Current_Pay_Period` / Post-session success variable assignment `postsession_success_variable_assignment`: `$$WF_PP_END_YEAR` = `$$MAP_PP_END_YEAR`; `$$WF_PP_NUM` = `$$MAP_PP_NUM`; `$$WF_PP_YEAR_NUM` = `$$MAP_PP_YEAR_NUM`
- `s_LES_Load_LES_EMP_DETAIL_RECTYPE_D_TBL` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_LES_Build_Message_Counters` / Post-session success command `post_session_success_command`: `Command1` = `cd $Param_Root_Directory/data/int/out/LES; cp $Param_LES_NIH_emp_detail NIHLES.P$$WF_PP_YEAR_NUM`; `Command2` = `<path>/scripts/nih_les_transfer.sh NIHLES.P$$WF_PP_YEAR_NUM`; `Command3` = `$Param_ControlDir/scripts/archive_files.sh $Param_Root_Directory/data/int/in/LES $Param_Root_Directory/data/archive/LES $$WF_PP_YEAR_NUM`
- `s_LES_Build_Message_Counters` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_SUBJECT` = `$$WF_SUBJECT`; `$$MAP_MESSAGE` = `$$WF_MESSAGE`; `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_LES_Build_Message_Counters` / Post-session success variable assignment `postsession_success_variable_assignment`: `$$WF_SUBJECT` = `$$MAP_SUBJECT`; `$$WF_MESSAGE` = `$$MAP_MESSAGE`
- `s_LES_Load_LES_EMP_DETAIL_CURR_EARN_TBL` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_LES_Load_LES_EMP_DETAIL_RETRO_EARN_TBL` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_LES_Load_LES_EMP_DETAIL_LEAVE_TBL` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_LESRPT_Load_LESR` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_LESRPT_Load_LESC` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_LESRPT_Load_LESU` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_LESRPT_Load_LESS` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_LESRPT_Load_LESD` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_LESRPT_Load_LESM` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_LESRPT_Load_LEST` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`
- `s_LESRPT_Load_LESL` / Pre-session variable assignment `presession_variable_assignment`: `$$MAP_PP_END_YEAR` = `$$WF_PP_END_YEAR`; `$$MAP_PP_NUM` = `$$WF_PP_NUM`

- Session `s_LES_Current_Pay_Period`: WRITER `LES_PAY_PERIOD_DATE_FILE` Append if Exists=`NO`, Output Type=`File`, Output file directory=`$PMTargetFileDir\`, Output filename=`les_pay_period.txt`
- Session `s_LES_Verify_Header`: WRITER `LES_HEADER_FILE` Append if Exists=`NO`, Output Type=`File`, Output file directory=`$PMTargetFileDir\`, Output filename=`les_header_file.txt`; READER `EMP_REC_TYPE_0` Command=`cd $Param_Root_Directory\data\int\in\LES; ls -1\|sort`, Input Type=`Command`, Source file directory=`$Param_Root_Directory\data\int\in\LES`, Source filename=`cd $$WF_LES_INPUT_DIR; ls -1\|sort`
- Session `s_LES_Verify_Record_Count`: WRITER `LES_TOTALS_FILE` Append if Exists=`NO`, Output Type=`File`, Output file directory=`$PMTargetFileDir\`, Output filename=`les_totals_file.txt`; READER `EMP_REC_TYPE_E` Command=`cd $Param_Root_Directory\data\int\in\LES; ls -1\|sort`, Input Type=`Command`, Source file directory=`$Param_Root_Directory\data\int\in\LES`, Source filename=`EMP_REC_TYPE_E.txt`
- Session `s_LES_Load_LES_HEADER_TBL`: WRITER `LES_HEADER_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`; READER `EMP_REC_TYPE_0` Command=`cd $Param_Root_Directory\data\int\in\LES; ls -1\|sort`, Input Type=`Command`, Source file directory=`$Param_Root_Directory\data\int\in\LES`, Source filename=`lesext01.txt`
- Session `s_LES_Load_LES_EMP_DETAIL_TBL`: WRITER `LES_EMP_DETAIL_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`YES`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`; READER `EMP_REC_TYPE_E` Command=`cd $Param_Root_Directory\data\int\in\LES; ls -1\|sort`, Input Type=`Command`, Source file directory=`$Param_Root_Directory\data\int\in\LES`, Source filename=`lesext01.txt`; WRITER `ERROR_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Bulk`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`
- Session `s_LES_Load_LES_EMP_DETAIL_RECTYPE_1_TBL`: WRITER `LES_EMP_DETAIL_RECTYPE_1_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`; READER `EMP_REC_TYPE_1` Command=`cd $Param_Root_Directory\data\int\in\LES; ls -1\|sort`, Input Type=`Command`, Source file directory=`$Param_Root_Directory\data\int\in\LES`, Source filename=`EMP_REC_TYPE_1.txt`
- Session `s_LES_Load_LES_EMP_DETAIL_RECTYPE_2_TBL`: WRITER `LES_EMP_DETAIL_RECTYPE_2_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`; READER `EMP_REC_TYPE_2` Command=`cd $Param_Root_Directory\data\int\in\LES; ls -1\|sort`, Input Type=`Command`, Source file directory=`$Param_Root_Directory\data\int\in\LES`, Source filename=`EMP_REC_TYPE_2.txt`
- Session `s_LES_Load_LES_EMP_DETAIL_RECTYPE_3_TBL`: WRITER `LES_EMP_DETAIL_RECTYPE_3_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`; READER `EMP_REC_TYPE_3` Command=`cd $Param_Root_Directory\data\int\in\LES; ls -1\|sort`, Input Type=`Command`, Source file directory=`$Param_Root_Directory\data\int\in\LES`, Source filename=`EMP_REC_TYPE_3.txt`
- Session `s_LES_Load_LES_EMP_DETAIL_RECTYPE_4_TBL`: WRITER `LES_EMP_DETAIL_RECTYPE_4_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`; READER `EMP_REC_TYPE_4` Command=`cd $Param_Root_Directory\data\int\in\LES; ls -1\|sort`, Input Type=`Command`, Source file directory=`$Param_Root_Directory\data\int\in\LES`, Source filename=`EMP_REC_TYPE_4.txt`
- Session `s_LES_Load_LES_EMP_DETAIL_RECTYPE_5_TBL`: WRITER `LES_EMP_DETAIL_RECTYPE_5_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`; READER `EMP_REC_TYPE_5` Command=`cd $Param_Root_Directory\data\int\in\LES; ls -1\|sort`, Input Type=`Command`, Source file directory=`$Param_Root_Directory\data\int\in\LES`, Source filename=`EMP_REC_TYPE_5.txt`
- Session `s_LES_Load_LES_EMP_DETAIL_RECTYPE_6_TBL`: WRITER `LES_EMP_DETAIL_RECTYPE_6_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`; READER `EMP_REC_TYPE_6` Command=`cd $Param_Root_Directory\data\int\in\LES; ls -1\|sort`, Input Type=`Command`, Source file directory=`$Param_Root_Directory\data\int\in\LES`, Source filename=`EMP_REC_TYPE_6.txt`
- Session `s_LES_Load_LES_EMP_DETAIL_RECTYPE_C_TBL`: WRITER `LES_EMP_DETAIL_RECTYPE_C_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`; READER `EMP_REC_TYPE_C` Command=`cd $Param_Root_Directory\data\int\in\LES; ls -1\|sort`, Input Type=`Command`, Source file directory=`$Param_Root_Directory\data\int\in\LES`, Source filename=`EMP_REC_TYPE_C.txt`
- Session `s_LES_Load_LES_EMP_DETAIL_RECTYPE_R_TBL`: WRITER `LES_EMP_DETAIL_RECTYPE_R_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`; READER `EMP_REC_TYPE_R` Command=`cd $Param_Root_Directory\data\int\in\LES; ls -1\|sort`, Input Type=`Command`, Source file directory=`$Param_Root_Directory\data\int\in\LES`, Source filename=`EMP_REC_TYPE_R.txt`
- Session `s_LES_Load_LES_EMP_DETAIL_RECTYPE_D_TBL`: WRITER `LES_EMP_DETAIL_RECTYPE_D_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`; READER `EMP_REC_TYPE_D` Command=`cd $Param_Root_Directory\data\int\in\LES; ls -1\|sort`, Input Type=`Command`, Source file directory=`$Param_Root_Directory\data\int\in\LES`, Source filename=`EMP_REC_TYPE_D.txt`
- Session `s_LES_Load_LES_EMP_DETAIL_RECTYPE_L_TBL`: WRITER `LES_EMP_DETAIL_RECTYPE_L_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`; READER `EMP_REC_TYPE_L` Command=`cd $Param_Root_Directory\data\int\in\LES; ls -1\|sort`, Input Type=`Command`, Source file directory=`$Param_Root_Directory\data\int\in\LES`, Source filename=`EMP_R`
- Session `s_LES_Load_LES_EMP_DETAIL_RECTYPE_U_TBL`: WRITER `LES_EMP_DETAIL_RECTYPE_U_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`; READER `EMP_REC_TYPE_U` Command=`cd $Param_Root_Directory\data\int\in\LES; ls -1\|sort`, Input Type=`Command`, Source file directory=`$Param_Root_Directory\data\int\in\LES`, Source filename=`cd <path>/LES201; ls -1`
- Session `s_LES_Load_LES_EMP_DETAIL_RECTYPE_M_TBL`: WRITER `LES_EMP_DETAIL_RECTYPE_M_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`; READER `EMP_REC_TYPE_M` Command=`cd $Param_Root_Directory\data\int\in\LES; ls -1\|sort`, Input Type=`Command`, Source file directory=`$Param_Root_Directory\data\int\in\LES`, Source filename=`cd <path>/LES201; ls -1`
- Session `s_LES_Load_LES_EMP_DETAIL_RECTYPE_T_TBL`: WRITER `LES_EMP_DETAIL_RECTYPE_T_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`; READER `EMP_REC_TYPE_T` Command=`cd $Param_Root_Directory\data\int\in\LES; ls -1\|sort`, Input Type=`Command`, Source file directory=`$Param_Root_Directory\data\int\in\LES`, Source filename=`cd <path>/LES201; ls -1`
- Session `s_LES_Load_LES_PRIMARY_DATA_TBL`: WRITER `LES_PRIMARY_DATA_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`
- Session `s_LES_Load_LES_EMP_DETAIL_CURR_EARN_TBL`: WRITER `LES_EMP_DETAIL_CURR_EARN_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`
- Session `s_LES_Load_LES_EMP_DETAIL_RETRO_EARN_TBL`: WRITER `LES_EMP_DETAIL_RETRO_EARN_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`
- Session `s_LES_Load_LES_EMP_DETAIL_LEAVE_TBL`: WRITER `LES_EMP_DETAIL_LEAVE_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`
- Session `s_LESRPT_Load_LESC`: WRITER `LESC` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`
- Session `s_LESRPT_Load_LESD`: WRITER `LESD` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`
- Session `s_LESRPT_Load_LESL`: WRITER `LESL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`
- Session `s_LESRPT_Load_LESM`: WRITER `LESM` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`
- Session `s_LESRPT_Load_LESR`: WRITER `LESR` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`
- Session `s_LESRPT_Load_LESS`: WRITER `LESS` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`
- Session `s_LESRPT_Load_LEST`: WRITER `LEST` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`
- Session `s_LESRPT_Load_LESU`: WRITER `LESU` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`
- Session `s_LES_NIH_FILE`: WRITER `LES_NIH_EMPLOYEE_DETAIL` Append if Exists=`NO`, Output Type=`File`, Output file directory=`$Param_Root_Directory/data/int/out/LES`, Output filename=`$Param_LES_NIH_emp_detail`; READER `LES_EMPLOYEE_DETAIL` Command=`cd $Param_Root_Directory\data\int\in\LES; ls -1\|sort`, Input Type=`Command`, Source file directory=`$Param_Root_Directory\data\int\in\LES`, Source filename=`LES_EMPLOYEE_DETAIL`; WRITER `LES_NIH_EMPLOYEE_SUMMARY_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Normal`, Truncate target table option=`YES`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`
- Session `s_LES_Build_Message_Counters`: WRITER `LES_MESSAGE_FILE` Append if Exists=`NO`, Output Type=`File`, Output file directory=`$PMTargetFileDir\`, Output filename=`les_message_file.txt`; WRITER `COUNTER_TBL` Delete=`YES`, Insert=`YES`, Target load type=`Bulk`, Truncate target table option=`NO`, Update as Insert=`NO`, Update as Update=`YES`, Update else Insert=`NO`; READER `EMP_REC_TYPE_E` Command=`cd $Param_Root_Directory\data\int\in\LES; ls -1\|sort`, Input Type=`Command`, Source file directory=`$Param_Root_Directory\data\int\in\LES`, Source filename=`EMP_REC_TYPE_E.txt`

## Source definitions

| Source | Database type | Fields |
|---|---|---|
| EMP_REC_TYPE_0 | VSAM | 11 |
| EMP_REC_TYPE_1 | VSAM | 20 |
| EMP_REC_TYPE_2 | VSAM | 16 |
| EMP_REC_TYPE_3 | VSAM | 20 |
| EMP_REC_TYPE_4 | VSAM | 17 |
| EMP_REC_TYPE_5 | VSAM | 18 |
| EMP_REC_TYPE_6 | VSAM | 7 |
| EMP_REC_TYPE_C | VSAM | 13 |
| EMP_REC_TYPE_D | VSAM | 11 |
| EMP_REC_TYPE_E | VSAM | 9 |
| EMP_REC_TYPE_L | VSAM | 13 |
| EMP_REC_TYPE_M | VSAM | 4 |
| EMP_REC_TYPE_R | VSAM | 13 |
| EMP_REC_TYPE_T | VSAM | 6 |
| EMP_REC_TYPE_U | VSAM | 10 |
| ERROR_TBL | Oracle | 7 |
| LES_EMPLOYEE_DETAIL | Flat File | 5 |
| LES_EMP_DETAIL_LEAVE_TBL | Oracle | 15 |
| LES_EMP_DETAIL_RECTYPE_1_TBL | Oracle | 21 |
| LES_EMP_DETAIL_RECTYPE_2_TBL | Oracle | 17 |
| LES_EMP_DETAIL_RECTYPE_3_TBL | Oracle | 21 |
| LES_EMP_DETAIL_RECTYPE_4_TBL | Oracle | 17 |
| LES_EMP_DETAIL_RECTYPE_5_TBL | Oracle | 18 |
| LES_EMP_DETAIL_RECTYPE_6_TBL | Oracle | 8 |
| LES_EMP_DETAIL_RECTYPE_C_TBL | Oracle | 14 |
| LES_EMP_DETAIL_RECTYPE_D_TBL | Oracle | 13 |
| LES_EMP_DETAIL_RECTYPE_L_TBL | Oracle | 15 |
| LES_EMP_DETAIL_RECTYPE_M_TBL | Oracle | 6 |
| LES_EMP_DETAIL_RECTYPE_R_TBL | Oracle | 14 |
| LES_EMP_DETAIL_RECTYPE_T_TBL | Oracle | 8 |
| LES_EMP_DETAIL_RECTYPE_U_TBL | Oracle | 11 |
| LES_EMP_DETAIL_TBL | Oracle | 5 |
| LES_HEADER_TBL | Oracle | 7 |
| LES_NIH_EMPLOYEE_SUMMARY_TBL | Oracle | 4 |
| LES_PRIMARY_DATA_TBL | Oracle | 90 |
| PAY_PERIOD | Oracle | 10 |

## Target definitions

| Target | Database type | Fields |
|---|---|---|
| COUNTER_TBL | Oracle | 7 |
| ERROR_TBL | Oracle | 7 |
| LESC | Oracle | 22 |
| LESD | Oracle | 21 |
| LESL | Oracle | 22 |
| LESM | Oracle | 14 |
| LESR | Oracle | 22 |
| LESS | Oracle | 91 |
| LEST | Oracle | 16 |
| LESU | Oracle | 19 |
| LES_EMP_DETAIL_CURR_EARN_TBL | Oracle | 8 |
| LES_EMP_DETAIL_LEAVE_TBL | Oracle | 15 |
| LES_EMP_DETAIL_RECTYPE_1_TBL | Oracle | 21 |
| LES_EMP_DETAIL_RECTYPE_2_TBL | Oracle | 17 |
| LES_EMP_DETAIL_RECTYPE_3_TBL | Oracle | 21 |
| LES_EMP_DETAIL_RECTYPE_4_TBL | Oracle | 17 |
| LES_EMP_DETAIL_RECTYPE_5_TBL | Oracle | 18 |
| LES_EMP_DETAIL_RECTYPE_6_TBL | Oracle | 8 |
| LES_EMP_DETAIL_RECTYPE_C_TBL | Oracle | 14 |
| LES_EMP_DETAIL_RECTYPE_D_TBL | Oracle | 13 |
| LES_EMP_DETAIL_RECTYPE_L_TBL | Oracle | 15 |
| LES_EMP_DETAIL_RECTYPE_M_TBL | Oracle | 6 |
| LES_EMP_DETAIL_RECTYPE_R_TBL | Oracle | 14 |
| LES_EMP_DETAIL_RECTYPE_T_TBL | Oracle | 8 |
| LES_EMP_DETAIL_RECTYPE_U_TBL | Oracle | 11 |
| LES_EMP_DETAIL_RETRO_EARN_TBL | Oracle | 8 |
| LES_EMP_DETAIL_TBL | Oracle | 5 |
| LES_HEADER_FILE | Flat File | 3 |
| LES_HEADER_TBL | Oracle | 7 |
| LES_MESSAGE_FILE | Flat File | 2 |
| LES_NIH_EMPLOYEE_DETAIL | Flat File | 5 |
| LES_NIH_EMPLOYEE_SUMMARY_TBL | Oracle | 4 |
| LES_PAY_PERIOD_DATE_FILE | Flat File | 1 |
| LES_PRIMARY_DATA_TBL | Oracle | 90 |
| LES_TOTALS_FILE | Flat File | 2 |

## Mapping `m_LES_Current_Pay_Period`

- Sessions: `s_LES_Current_Pay_Period` (#1)
- Sources: `PAY_PERIOD`
- Target instances: `LES_PAY_PERIOD_DATE_FILE`

### Transformation `SQ_PAY_PERIOD` (Source Qualifier)

- **Source Filter**: `PAY_PERIOD.CURR_PP_FLAG = 'Y'`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`


### Target instance `LES_PAY_PERIOD_DATE_FILE` (table `LES_PAY_PERIOD_DATE_FILE`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LES_PAY_PERIOD_DATE_FILE | PAY_PERIOD_TXT | exp_Final.PAY_PERIOD → exp_Build_Pay_Period.o_PAY_PERIOD = TO_CHAR(PP_END_YEAR) \|\| v_PP_NUM → SQ_PAY_PERIOD.PP_END_YEAR → PAY_PERIOD.PP_END_YEAR → exp_Build_Pay_Period.v_PP_NUM = IIF(PP_NUM < 10, LPAD(TO_CHAR(PP_NUM), 2, '0'), TO_CHAR(PP_NUM) ) → SQ_PAY_PERIOD.PP_NUM → PAY_PERIOD.PP_NUM | PAY_PERIOD.PP_END_YEAR; PAY_PERIOD.PP_NUM |

## Mapping `m_LES_Verify_Header`

- Sessions: `s_LES_Verify_Header` (#2)
- Sources: `EMP_REC_TYPE_0`
- Target instances: `LES_HEADER_FILE`

### Transformation `Norm_EMP_REC_TYPE_0` (Normalizer)

- **Reset**: `NO`
- **Restart**: `NO`

### Transformation `fil_LES_HEADER` (Filter)

- **Filter Condition**: `RECORD_TYPE = '0'`

### Transformation `lkp_Current_Pay_Period` (Lookup Procedure)

- **Lookup table name**: `PAY_PERIOD`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `CURR_PP_FLAG = in_CURR_PP_FLAG`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `lkp_Pay_Period_Record_Date` (Lookup Procedure)

- **Lookup table name**: `PAY_PERIOD`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `PP_START_DTE <= in_HEADER_DATE AND PP_END_DTE >= in_HEADER_DATE`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

- Normalizer `Norm_EMP_REC_TYPE_0` (vsam=True, source EMP_REC_TYPE_0) occurs: —; generated: —
- Lookup `lkp_Current_Pay_Period`: table `PAY_PERIOD` (exists in export: **True**), condition `CURR_PP_FLAG = in_CURR_PP_FLAG`, multiple-match policy `Use Any Value`.
- Lookup `lkp_Pay_Period_Record_Date`: table `PAY_PERIOD` (exists in export: **True**), condition `PP_START_DTE <= in_HEADER_DATE AND PP_END_DTE >= in_HEADER_DATE`, multiple-match policy `Use Any Value`.

### Target instance `LES_HEADER_FILE` (table `LES_HEADER_FILE`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LES_HEADER_FILE | PP_YEAR_NUM | exp_Final.PP_YEAR_NUM → exp_Stage.o_PP_YEAR_NUM = TO_CHAR(CURRENT_PP_END_YEAR) \|\| v_PP_NUM → exp_Verify_Header_Date.lkp_CURRENT_PP_END_YEAR → lkp_Current_Pay_Period.PP_END_YEAR [lookup PAY_PERIOD.PP_END_YEAR ON CURR_PP_FLAG = in_CURR_PP_FLAG] → exp_Stage.v_PP_NUM = IIF(CURRENT_PP_NUM < 10, LPAD(TO_CHAR(CURRENT_PP_NUM), 2, '0'), TO_CHAR(CURRENT_PP_NUM) ) → exp_Verify_Header_Date.lkp_CURRENT_PP_NUM → lkp_Current_Pay_Period.PP_NUM [lookup PAY_PERIOD.PP_NUM ON CURR_PP_FLAG = in_CURR_PP_FLAG] | PAY_PERIOD.PP_END_YEAR (lookup); PAY_PERIOD.PP_NUM (lookup); literal/expression: 'Y' (lookup key) |
| LES_HEADER_FILE | INPUT_FILE_NUMBER | exp_Final.INPUT_FILE_NUMBER → exp_Stage.FILE_COUNTER → exp_Verify_Header_Date.o_FILE_COUNTER = v_FILE_COUNTER → exp_Verify_Header_Date.v_FILE_COUNTER = v_FILE_COUNTER + 1 | literal/expression: v_FILE_COUNTER + 1 |
| LES_HEADER_FILE | INPUT_PP_END_DATE | exp_Final.INPUT_PP_END_DATE → exp_Stage.PP_END_DTE_SOURCE_STRING → exp_Verify_Header_Date.PP_END_DTE_SOURCE_STRING → exp_Convert.PP_END_DTE_SOURCE_STRING → fil_LES_HEADER.PPD_END_DATE → Norm_EMP_REC_TYPE_0.PPD_END_DATE → EMP_REC_TYPE_0.PPD_END_DATE | EMP_REC_TYPE_0.PPD_END_DATE |

## Mapping `m_LES_Verify_Record_Count`

- Sessions: `s_LES_Verify_Record_Count` (#3)
- Sources: `EMP_REC_TYPE_E`
- Target instances: `LES_TOTALS_FILE`

### Transformation `Norm_EMP_REC_TYPE_E` (Normalizer)

- **Reset**: `NO`
- **Restart**: `NO`

### Transformation `fil_LES_Records` (Filter)

- **Filter Condition**: `SUBSTR(WS_EMP_REC_TYPE, 1, 1) = '0' OR WS_EMP_REC_TYPE = '*E' OR SUBSTR(WS_EMP_REC_TYPE, 1, 1) = '2'`

### Transformation `fil_Trailer_Records` (Filter)

- **Filter Condition**: `SUBSTR(WS_EMP_REC_TYPE, 1, 1) = '2'`

- Normalizer `Norm_EMP_REC_TYPE_E` (vsam=True, source EMP_REC_TYPE_E) occurs: —; generated: —

### Target instance `LES_TOTALS_FILE` (table `LES_TOTALS_FILE`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LES_TOTALS_FILE | INPUT_FILE_NUMBER | exp_Final.INPUT_FILE_NUMBER → exp_Stage.FILE_COUNTER → fil_Trailer_Records.FILE_COUNTER → exp_Verify_Header_Date.o_FILE_COUNTER = v_FILE_COUNTER → exp_Verify_Header_Date.v_FILE_COUNTER = IIF(SUBSTR(WS_EMP_REC_TYPE, 1, 1) = '0', v_FILE_COUNTER + 1, v_FILE_COUNTER ) → exp_Convert.WS_EMP_REC_TYPE → fil_LES_Records.WS_EMP_REC_TYPE → Norm_EMP_REC_TYPE_E.WS_EMP_REC_TYPE → EMP_REC_TYPE_E.WS_EMP_REC_TYPE | EMP_REC_TYPE_E.WS_EMP_REC_TYPE |
| LES_TOTALS_FILE | INPUT_FILE_TOTAL | exp_Final.INPUT_FILE_TOTAL → exp_Stage.LES_COUNT → fil_Trailer_Records.LES_COUNT → exp_Verify_Header_Date.LES_COUNT → exp_Convert.o_LES_COUNT = IIF(SUBSTR(WS_EMP_REC_TYPE, 1, 1) = '2', v_LES_COUNT ) → fil_LES_Records.WS_EMP_REC_TYPE → Norm_EMP_REC_TYPE_E.WS_EMP_REC_TYPE → EMP_REC_TYPE_E.WS_EMP_REC_TYPE → exp_Convert.v_LES_COUNT = IIF(SUBSTR(WS_EMP_REC_TYPE, 1, 1) = '2' AND IS_NUMBER(v_LES_COUNT_STRING), TO_INTEGER(v_LES_COUNT_STRING), NULL) → exp_Convert.v_LES_COUNT_STRING = IIF(SUBSTR(WS_EMP_REC_TYPE, 1, 1) = '2', SUBSTR(WS_EMP_REC_TYPE, 2, 1) \|\| WS_SSN3 \|\| WS_SSN2 \|\| SUBSTR(WS_SSN4, 1, 1), NULL) → fil_LES_Records.WS_SSN3 → Norm_EMP_REC_TYPE_E.WS_SSN3 → EMP_REC_TYPE_E.WS_SSN3 → fil_LES_Records.WS_SSN2 → Norm_EMP_REC_TYPE_E.WS_SSN2 → EMP_REC_TYPE_E.WS_SSN2 → fil_LES_Records.WS_SSN4 → Norm_EMP_REC_TYPE_E.WS_SSN4 → EMP_REC_TYPE_E.WS_SSN4 | EMP_REC_TYPE_E.WS_EMP_REC_TYPE; EMP_REC_TYPE_E.WS_SSN2; EMP_REC_TYPE_E.WS_SSN3; EMP_REC_TYPE_E.WS_SSN4 |

## Mapping `m_LES_Load_LES_HEADER_TBL`

- Sessions: `s_LES_Load_LES_HEADER_TBL` (#4)
- Sources: `EMP_REC_TYPE_0`
- Target instances: `LES_HEADER_TBL`

### Transformation `Norm_EMP_REC_TYPE_0` (Normalizer)

- **Reset**: `NO`
- **Restart**: `NO`

### Transformation `fil_First_Header_Record` (Filter)

- **Filter Condition**: `HEADER_COUNTER =1`

### Transformation `fil_LES_HEADER` (Filter)

- **Filter Condition**: `RECORD_TYPE = '0'`

### Transformation `lkp_Pay_Period_Record_Date` (Lookup Procedure)

- **Lookup table name**: `PAY_PERIOD`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `PP_START_DTE <= in_PP_DATE AND PP_END_DTE >= in_PP_DATE`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

- Normalizer `Norm_EMP_REC_TYPE_0` (vsam=True, source EMP_REC_TYPE_0) occurs: —; generated: —
- Lookup `lkp_Pay_Period_Record_Date`: table `PAY_PERIOD` (exists in export: **True**), condition `PP_START_DTE <= in_PP_DATE AND PP_END_DTE >= in_PP_DATE`, multiple-match policy `Use Any Value`.

### Target instance `LES_HEADER_TBL` (table `LES_HEADER_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LES_HEADER_TBL | PP_END_YEAR | exp_Final.PP_END_YEAR → exp_Stage.PP_END_YEAR → lkp_Pay_Period_Record_Date.PP_END_YEAR [lookup PAY_PERIOD.PP_END_YEAR ON PP_START_DTE <= in_PP_DATE AND PP_END_DTE >= in_PP_DATE] | EMP_REC_TYPE_0.PPD_END_DATE (lookup key); PAY_PERIOD.PP_END_YEAR (lookup) |
| LES_HEADER_TBL | PP_NUM | exp_Final.PP_NUM → exp_Stage.PP_NUM → lkp_Pay_Period_Record_Date.PP_NUM [lookup PAY_PERIOD.PP_NUM ON PP_START_DTE <= in_PP_DATE AND PP_END_DTE >= in_PP_DATE] | EMP_REC_TYPE_0.PPD_END_DATE (lookup key); PAY_PERIOD.PP_NUM (lookup) |
| LES_HEADER_TBL | PP_END_DTE | exp_Final.PP_END_DTE → exp_Stage.PP_END_DTE → fil_First_Header_Record.PP_END_DTE → exp_Convert.o_PP_END_DTE = IIF(IS_DATE(v_PP_END_DTE, 'MM/DD/YYYY'), TO_DATE(v_PP_END_DTE, 'MM/DD/YYYY') ) → exp_Convert.v_PP_END_DTE = SUBSTR(PP_END_DTE, 5, 2) \|\| '/' \|\| SUBSTR(PP_END_DTE, 7, 2) \|\| '/' \|\| SUBSTR(PP_END_DTE, 1, 4) --Convert end date into MM/DD/YYYY format. --Incoming format is YYYYMMDD → fil_LES_HEADER.PPD_END_DATE → Norm_EMP_REC_TYPE_0.PPD_END_DATE → EMP_REC_TYPE_0.PPD_END_DATE | EMP_REC_TYPE_0.PPD_END_DATE |
| LES_HEADER_TBL | HDR_LOC_ID | exp_Final.HDR_LOC_ID → exp_Stage.HDR_LOC_ID → fil_First_Header_Record.HDR_LOC_ID → exp_Convert.HDR_LOC_ID → fil_LES_HEADER.HEADER_LOC_ID → Norm_EMP_REC_TYPE_0.HEADER_LOC_ID → EMP_REC_TYPE_0.HEADER_LOC_ID | EMP_REC_TYPE_0.HEADER_LOC_ID |
| LES_HEADER_TBL | HDR_LOC_NAME | exp_Final.HDR_LOC_NAME → exp_Stage.HDR_LOC_NAME → fil_First_Header_Record.HDR_LOC_NAME → exp_Convert.HDR_LOC_NAME → fil_LES_HEADER.HEADER_LOC_NAME → Norm_EMP_REC_TYPE_0.HEADER_LOC_NAME → EMP_REC_TYPE_0.HEADER_LOC_NAME | EMP_REC_TYPE_0.HEADER_LOC_NAME |
| LES_HEADER_TBL | SYSTEM_ID | exp_Final.SYSTEM_ID → exp_Stage.SYSTEM_ID → fil_First_Header_Record.SYSTEM_ID → exp_Convert.SYSTEM_ID → fil_LES_HEADER.SYSTEM_ID → Norm_EMP_REC_TYPE_0.SYSTEM_ID → EMP_REC_TYPE_0.SYSTEM_ID | EMP_REC_TYPE_0.SYSTEM_ID |
| LES_HEADER_TBL | TRANSMISSION_DTE | exp_Final.TRANSMISSION_DTE → exp_Stage.TRANSMISSION_DTE → fil_First_Header_Record.TRANSMISSION_DTE → exp_Convert.TRANSMISSION_DTE = IIF(IS_DATE(v_TRANSMISSION_DTE, 'MM/DD/YYYY'), TO_DATE(v_TRANSMISSION_DTE, 'MM/DD/YYYY') ) → exp_Convert.v_TRANSMISSION_DTE = TRANSMISSION_MONTH \|\| '/' \|\| TRANSMISSION_DAY \|\| '/' \|\| TRANSMISSION_CENTURY \|\| TRANSMISSION_YEAR → fil_LES_HEADER.TRANSMISSION_MONTH → Norm_EMP_REC_TYPE_0.TRANSMISSION_MONTH → EMP_REC_TYPE_0.TRANSMISSION_MONTH → fil_LES_HEADER.TRANSMISSION_DAY → Norm_EMP_REC_TYPE_0.TRANSMISSION_DAY → EMP_REC_TYPE_0.TRANSMISSION_DAY → fil_LES_HEADER.TRANSMISSION_CENTURY → Norm_EMP_REC_TYPE_0.TRANSMISSION_CENTURY → EMP_REC_TYPE_0.TRANSMISSION_CENTURY → fil_LES_HEADER.TRANSMISSION_YEAR → Norm_EMP_REC_TYPE_0.TRANSMISSION_YEAR → EMP_REC_TYPE_0.TRANSMISSION_YEAR | EMP_REC_TYPE_0.TRANSMISSION_CENTURY; EMP_REC_TYPE_0.TRANSMISSION_DAY; EMP_REC_TYPE_0.TRANSMISSION_MONTH; EMP_REC_TYPE_0.TRANSMISSION_YEAR |

## Mapping `m_LES_Load_LES_EMP_DETAIL_TBL`

- Sessions: `s_LES_Load_LES_EMP_DETAIL_TBL` (#5)
- Sources: `EMP_REC_TYPE_E`, `LES_HEADER_TBL`
- Target instances: `ERROR_TBL`, `LES_EMP_DETAIL_TBL`

### Transformation `Norm_EMP_REC_TYPE_E` (Normalizer)

- **Reset**: `NO`
- **Restart**: `NO`

### Transformation `SQ_LES_HEADER_TBL` (Source Qualifier)

- **Source Filter**: `LES_HEADER_TBL.PP_END_YEAR = $$MAP_PP_END_YEAR AND LES_HEADER_TBL.PP_NUM = $$MAP_PP_NUM`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `fil_EMPLOYEE_DETAIL` (Filter)

- **Filter Condition**: `WS_EMP_REC_TYPE = '*E'`

### Transformation `jnr_HEADER_EMP_DETAILS` (Joiner)

- **Join Condition**: `CONSTANT_EMPLOYEE_DETAIL = CONSTANT_HEADER`
- **Join Type**: `Normal Join`
- **Null ordering in master**: `Null Is Highest Value`
- **Null ordering in detail**: `Null Is Highest Value`
- **Sorted Input**: `NO`

### Transformation `lkp_PSEUDSSN_TBL` (Lookup Procedure)

- **Lookup table name**: `PSEUDOSSN_TBL`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `PSEUDOSSN = in_DFAS_PSEUDOSSN`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `rtr_GOOD_BAD_RECORDS` (Router)

- Router group `GOOD_RECORDS`: `TRUE --Loads all records to the target table`
- Router group `DEFAULT1`: `(default group)`
- Router group `BAD_RECORDS`: `ERROR_FLAG = TRUE`

- Joiner `jnr_HEADER_EMP_DETAILS`: Normal Join ON `CONSTANT_EMPLOYEE_DETAIL = CONSTANT_HEADER`
- Normalizer `Norm_EMP_REC_TYPE_E` (vsam=True, source EMP_REC_TYPE_E) occurs: —; generated: —
- Lookup `lkp_PSEUDSSN_TBL`: table `PSEUDOSSN_TBL` (exists in export: **False**), condition `PSEUDOSSN = in_DFAS_PSEUDOSSN`, multiple-match policy `Use Any Value`.

### Target instance `ERROR_TBL` (table `ERROR_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| ERROR_TBL | PROCESS_NAME | exp_FINAL_ERRORS.MAPPING_NAME → rtr_GOOD_BAD_RECORDS.MAPPING_NAME3 [router group BAD_RECORDS WHERE ERROR_FLAG = TRUE] → exp_CHECK_ERRORS.o_MAPPING_NAME = $PMMappingName | literal/expression: $PMMappingName |
| ERROR_TBL | ERROR_MESSAGE | exp_FINAL_ERRORS.ERROR_MESSAGE → rtr_GOOD_BAD_RECORDS.ERROR_MESSAGE_13 [router group BAD_RECORDS WHERE ERROR_FLAG = TRUE] → exp_CHECK_ERRORS.o_ERROR_MESSAGE_1 = IIF(v_ERROR_FLAG_1 = TRUE, 'The PSEUDOSSN: ' \|\| SSN \|\| ' is not found for this LES Number: ' \|\| WS_EMP_LES_NUM) → exp_CHECK_ERRORS.v_ERROR_FLAG_1 = IIF(ISNULL(lkp_PSEUDOSSN), --THEN TRUE, --ELSE FALSE) → lkp_PSEUDSSN_TBL.PSEUDOSSN [lookup PSEUDOSSN_TBL.PSEUDOSSN ON PSEUDOSSN = in_DFAS_PSEUDOSSN] → exp_STAGE.SSN → jnr_HEADER_EMP_DETAILS.SSN → exp_Convert.o_SSN = WS_SSN3 \|\| WS_SSN2 \|\| WS_SSN4 → fil_EMPLOYEE_DETAIL.WS_SSN3 → Norm_EMP_REC_TYPE_E.WS_SSN3 → EMP_REC_TYPE_E.WS_SSN3 → fil_EMPLOYEE_DETAIL.WS_SSN2 → Norm_EMP_REC_TYPE_E.WS_SSN2 → EMP_REC_TYPE_E.WS_SSN2 → fil_EMPLOYEE_DETAIL.WS_SSN4 → Norm_EMP_REC_TYPE_E.WS_SSN4 → EMP_REC_TYPE_E.WS_SSN4 → exp_STAGE.WS_EMP_LES_NUM → jnr_HEADER_EMP_DETAILS.WS_EMP_LES_NUM → exp_Convert.WS_EMP_LES_NUM → fil_EMPLOYEE_DETAIL.WS_EMP_LES_NUM → Norm_EMP_REC_TYPE_E.WS_EMP_LES_NUM → EMP_REC_TYPE_E.WS_EMP_LES_NUM | EMP_REC_TYPE_E.WS_EMP_LES_NUM; EMP_REC_TYPE_E.WS_SSN2; EMP_REC_TYPE_E.WS_SSN2 (lookup key); EMP_REC_TYPE_E.WS_SSN3; EMP_REC_TYPE_E.WS_SSN3 (lookup key); EMP_REC_TYPE_E.WS_SSN4; EMP_REC_TYPE_E.WS_SSN4 (lookup key); PSEUDOSSN_TBL.PSEUDOSSN (lookup) |
| ERROR_TBL | SOURCE_KEY | exp_FINAL_ERRORS.SRC_KEY → rtr_GOOD_BAD_RECORDS.SRC_KEY3 [router group BAD_RECORDS WHERE ERROR_FLAG = TRUE] → exp_CHECK_ERRORS.o_SRC_KEY = TO_CHAR(PP_END_YEAR) \|\| ' \|\| ' \|\| LPAD(TO_CHAR(PP_NUM), 2, '0') \|\| ' \|\| ' \|\| WS_EMP_LES_NUM \|\| ' \|\| ' \|\| SSN \|\| ' \|\| ' → exp_STAGE.PP_END_YEAR → jnr_HEADER_EMP_DETAILS.PP_END_YEAR → exp_HEADER.PP_END_YEAR → SQ_LES_HEADER_TBL.PP_END_YEAR → LES_HEADER_TBL.PP_END_YEAR → exp_STAGE.PP_NUM → jnr_HEADER_EMP_DETAILS.PP_NUM → exp_HEADER.PP_NUM → SQ_LES_HEADER_TBL.PP_NUM → LES_HEADER_TBL.PP_NUM → exp_STAGE.WS_EMP_LES_NUM → jnr_HEADER_EMP_DETAILS.WS_EMP_LES_NUM → exp_Convert.WS_EMP_LES_NUM → fil_EMPLOYEE_DETAIL.WS_EMP_LES_NUM → Norm_EMP_REC_TYPE_E.WS_EMP_LES_NUM → EMP_REC_TYPE_E.WS_EMP_LES_NUM → exp_STAGE.SSN → jnr_HEADER_EMP_DETAILS.SSN → exp_Convert.o_SSN = WS_SSN3 \|\| WS_SSN2 \|\| WS_SSN4 → fil_EMPLOYEE_DETAIL.WS_SSN3 → Norm_EMP_REC_TYPE_E.WS_SSN3 → EMP_REC_TYPE_E.WS_SSN3 → fil_EMPLOYEE_DETAIL.WS_SSN2 → Norm_EMP_REC_TYPE_E.WS_SSN2 → EMP_REC_TYPE_E.WS_SSN2 → fil_EMPLOYEE_DETAIL.WS_SSN4 → Norm_EMP_REC_TYPE_E.WS_SSN4 → EMP_REC_TYPE_E.WS_SSN4 | EMP_REC_TYPE_E.WS_EMP_LES_NUM; EMP_REC_TYPE_E.WS_SSN2; EMP_REC_TYPE_E.WS_SSN3; EMP_REC_TYPE_E.WS_SSN4; LES_HEADER_TBL.PP_END_YEAR; LES_HEADER_TBL.PP_NUM |
| ERROR_TBL | ERROR_DATE | exp_FINAL_ERRORS.o_ERROR_DATE = SESSSTARTTIME | literal/expression: SESSSTARTTIME |
| ERROR_TBL | PP_END_YEAR | exp_FINAL_ERRORS.PP_END_YEAR → rtr_GOOD_BAD_RECORDS.PP_END_YEAR3 [router group BAD_RECORDS WHERE ERROR_FLAG = TRUE] → exp_CHECK_ERRORS.PP_END_YEAR → exp_STAGE.PP_END_YEAR → jnr_HEADER_EMP_DETAILS.PP_END_YEAR → exp_HEADER.PP_END_YEAR → SQ_LES_HEADER_TBL.PP_END_YEAR → LES_HEADER_TBL.PP_END_YEAR | LES_HEADER_TBL.PP_END_YEAR |
| ERROR_TBL | PP_NUM | exp_FINAL_ERRORS.PP_NUM → rtr_GOOD_BAD_RECORDS.PP_NUM3 [router group BAD_RECORDS WHERE ERROR_FLAG = TRUE] → exp_CHECK_ERRORS.PP_NUM → exp_STAGE.PP_NUM → jnr_HEADER_EMP_DETAILS.PP_NUM → exp_HEADER.PP_NUM → SQ_LES_HEADER_TBL.PP_NUM → LES_HEADER_TBL.PP_NUM | LES_HEADER_TBL.PP_NUM |
| ERROR_TBL | CYCLE_ID | (not connected — NULL) | — |

### Target instance `LES_EMP_DETAIL_TBL` (table `LES_EMP_DETAIL_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LES_EMP_DETAIL_TBL | PP_END_YEAR | exp_FINAL.PP_END_YEAR → rtr_GOOD_BAD_RECORDS.PP_END_YEAR1 [router group GOOD_RECORDS WHERE TRUE --Loads all records to the target table] → exp_CHECK_ERRORS.PP_END_YEAR → exp_STAGE.PP_END_YEAR → jnr_HEADER_EMP_DETAILS.PP_END_YEAR → exp_HEADER.PP_END_YEAR → SQ_LES_HEADER_TBL.PP_END_YEAR → LES_HEADER_TBL.PP_END_YEAR | LES_HEADER_TBL.PP_END_YEAR |
| LES_EMP_DETAIL_TBL | PP_NUM | exp_FINAL.PP_NUM → rtr_GOOD_BAD_RECORDS.PP_NUM1 [router group GOOD_RECORDS WHERE TRUE --Loads all records to the target table] → exp_CHECK_ERRORS.PP_NUM → exp_STAGE.PP_NUM → jnr_HEADER_EMP_DETAILS.PP_NUM → exp_HEADER.PP_NUM → SQ_LES_HEADER_TBL.PP_NUM → LES_HEADER_TBL.PP_NUM | LES_HEADER_TBL.PP_NUM |
| LES_EMP_DETAIL_TBL | PSEUDOSSN | exp_FINAL.SOCIAL_SECURITY_NUMBER → rtr_GOOD_BAD_RECORDS.PSEUDOSSN1 [router group GOOD_RECORDS WHERE TRUE --Loads all records to the target table] → exp_CHECK_ERRORS.SSN → exp_STAGE.SSN → jnr_HEADER_EMP_DETAILS.SSN → exp_Convert.o_SSN = WS_SSN3 \|\| WS_SSN2 \|\| WS_SSN4 → fil_EMPLOYEE_DETAIL.WS_SSN3 → Norm_EMP_REC_TYPE_E.WS_SSN3 → EMP_REC_TYPE_E.WS_SSN3 → fil_EMPLOYEE_DETAIL.WS_SSN2 → Norm_EMP_REC_TYPE_E.WS_SSN2 → EMP_REC_TYPE_E.WS_SSN2 → fil_EMPLOYEE_DETAIL.WS_SSN4 → Norm_EMP_REC_TYPE_E.WS_SSN4 → EMP_REC_TYPE_E.WS_SSN4 | EMP_REC_TYPE_E.WS_SSN2; EMP_REC_TYPE_E.WS_SSN3; EMP_REC_TYPE_E.WS_SSN4 |
| LES_EMP_DETAIL_TBL | LES_NUMBER | exp_FINAL.o_LES_NUMBER = TO_INTEGER( LES_NUMBER) → rtr_GOOD_BAD_RECORDS.LES_NUMBER1 [router group GOOD_RECORDS WHERE TRUE --Loads all records to the target table] → exp_CHECK_ERRORS.WS_EMP_LES_NUM → exp_STAGE.WS_EMP_LES_NUM → jnr_HEADER_EMP_DETAILS.WS_EMP_LES_NUM → exp_Convert.WS_EMP_LES_NUM → fil_EMPLOYEE_DETAIL.WS_EMP_LES_NUM → Norm_EMP_REC_TYPE_E.WS_EMP_LES_NUM → EMP_REC_TYPE_E.WS_EMP_LES_NUM | EMP_REC_TYPE_E.WS_EMP_LES_NUM |
| LES_EMP_DETAIL_TBL | LES_DELIVERY_IND | exp_FINAL.LES_DELIVERY_INDICATOR → rtr_GOOD_BAD_RECORDS.LES_DELIVERY_IDC1 [router group GOOD_RECORDS WHERE TRUE --Loads all records to the target table] → exp_CHECK_ERRORS.WS_EMP_LES_DELIVERY_IDC → exp_STAGE.WS_EMP_LES_DELIVERY_IDC → jnr_HEADER_EMP_DETAILS.WS_EMP_LES_DELIVERY_IDC → exp_Convert.WS_EMP_LES_DELIVERY_IDC → fil_EMPLOYEE_DETAIL.WS_EMP_LES_DELIVERY_IDC → Norm_EMP_REC_TYPE_E.WS_EMP_LES_DELIVERY_IDC → EMP_REC_TYPE_E.WS_EMP_LES_DELIVERY_IDC | EMP_REC_TYPE_E.WS_EMP_LES_DELIVERY_IDC |

## Mapping `m_LES_Load_LES_EMP_DETAIL_RECTYPE_1_TBL`

- Sessions: `s_LES_Load_LES_EMP_DETAIL_RECTYPE_1_TBL` (#6)
- Sources: `EMP_REC_TYPE_1`, `LES_EMP_DETAIL_TBL`
- Target instances: `LES_EMP_DETAIL_RECTYPE_1_TBL`

### Transformation `Norm_EMP_REC_TYPE_1` (Normalizer)

- **Reset**: `NO`
- **Restart**: `NO`

### Transformation `SQ_LES_EMP_DETAIL_TBL` (Source Qualifier)

- **Source Filter**: `LES_EMP_DETAIL_TBL.PP_END_YEAR = $$MAP_PP_END_YEAR AND LES_EMP_DETAIL_TBL.PP_NUM = $$MAP_PP_NUM`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `fil_EMP_REC_TYPE_1` (Filter)

- **Filter Condition**: `WS_LES_REC_TYPE1 = '*1'`

### Transformation `fil_EMP_REC_TYPE_1_EMP_DETAIL` (Filter)

- **Filter Condition**: `WS_LES_REC_TYPE1 = '*1' OR WS_LES_REC_TYPE1 = '*E'`

### Transformation `jnr_LES_NUMBER` (Joiner)

- **Join Condition**: `EMP_LES_NUMBER = LES_NUMBER`
- **Join Type**: `Normal Join`
- **Null ordering in master**: `Null Is Highest Value`
- **Null ordering in detail**: `Null Is Highest Value`
- **Sorted Input**: `NO`

- Joiner `jnr_LES_NUMBER`: Normal Join ON `EMP_LES_NUMBER = LES_NUMBER`
- Normalizer `Norm_EMP_REC_TYPE_1` (vsam=True, source EMP_REC_TYPE_1) occurs: —; generated: —

### Target instance `LES_EMP_DETAIL_RECTYPE_1_TBL` (table `LES_EMP_DETAIL_RECTYPE_1_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LES_EMP_DETAIL_RECTYPE_1_TBL | PP_END_YEAR | exp_Final.PP_END_YEAR → jnr_LES_NUMBER.PP_END_YEAR → SQ_LES_EMP_DETAIL_TBL.PP_END_YEAR → LES_EMP_DETAIL_TBL.PP_END_YEAR | LES_EMP_DETAIL_TBL.PP_END_YEAR |
| LES_EMP_DETAIL_RECTYPE_1_TBL | PP_NUM | exp_Final.PP_NUM → jnr_LES_NUMBER.PP_NUM → SQ_LES_EMP_DETAIL_TBL.PP_NUM → LES_EMP_DETAIL_TBL.PP_NUM | LES_EMP_DETAIL_TBL.PP_NUM |
| LES_EMP_DETAIL_RECTYPE_1_TBL | LES_NUMBER | exp_Final.LES_NUMBER → jnr_LES_NUMBER.LES_NUMBER → fil_EMP_REC_TYPE_1.LES_NUMBER → exp_Convert.o_LES_NUMBER = IIF(IS_NUMBER(v_LES_NUMBER), TO_INTEGER(v_LES_NUMBER) ) → exp_Convert.v_LES_NUMBER = IIF(WS_LES_REC_TYPE1 = '*E', SUBSTR(PAY_DTE, 4, 3) \|\| SUBSTR(EMPLOYEE_NAME, 1, 4), v_LES_NUMBER ) → fil_EMP_REC_TYPE_1_EMP_DETAIL.WS_LES_REC_TYPE1 → Norm_EMP_REC_TYPE_1.WS_LES_REC_TYPE1 → EMP_REC_TYPE_1.WS_LES_REC_TYPE1 → fil_EMP_REC_TYPE_1_EMP_DETAIL.WS_LES_PAY_DT → Norm_EMP_REC_TYPE_1.WS_LES_PAY_DT → EMP_REC_TYPE_1.WS_LES_PAY_DT → fil_EMP_REC_TYPE_1_EMP_DETAIL.WS_LES_EYE_NME → Norm_EMP_REC_TYPE_1.WS_LES_EYE_NME → EMP_REC_TYPE_1.WS_LES_EYE_NME | EMP_REC_TYPE_1.WS_LES_EYE_NME; EMP_REC_TYPE_1.WS_LES_PAY_DT; EMP_REC_TYPE_1.WS_LES_REC_TYPE1 |
| LES_EMP_DETAIL_RECTYPE_1_TBL | PSEUDOSSN | exp_Final.PSEUDOSSN → jnr_LES_NUMBER.PSEUDOSSN → SQ_LES_EMP_DETAIL_TBL.PSEUDOSSN → LES_EMP_DETAIL_TBL.PSEUDOSSN | LES_EMP_DETAIL_TBL.PSEUDOSSN |
| LES_EMP_DETAIL_RECTYPE_1_TBL | PP_END_DTE | exp_Final.PP_END_DTE → jnr_LES_NUMBER.PP_END_DTE → fil_EMP_REC_TYPE_1.PP_END_DTE → exp_Convert.o_PP_END_DTE = IIF(IS_DATE(v_EMP_DET_PP_END_DTE, 'MM/DD/RR'), TO_DATE(v_EMP_DET_PP_END_DTE, 'MM/DD/RR') ) → exp_Convert.v_EMP_DET_PP_END_DTE = SUBSTR(PP_END_DTE, 1, 2) \|\| '/' \|\| SUBSTR(PP_END_DTE, 3, 2) \|\| '/' \|\| SUBSTR(PP_END_DTE, 5, 2) --Convert PP END DTE to MM/DD/RR format → fil_EMP_REC_TYPE_1_EMP_DETAIL.WS_LES_PPD_END_DT → Norm_EMP_REC_TYPE_1.WS_LES_PPD_END_DT → EMP_REC_TYPE_1.WS_LES_PPD_END_DT | EMP_REC_TYPE_1.WS_LES_PPD_END_DT |
| LES_EMP_DETAIL_RECTYPE_1_TBL | PAY_DTE | exp_Final.PAY_DTE → jnr_LES_NUMBER.PAY_DTE → fil_EMP_REC_TYPE_1.PAY_DTE → exp_Convert.o_PAY_DTE = IIF(IS_DATE(v_PAY_DTE, 'MM/DD/RR'), TO_DATE(v_PAY_DTE, 'MM/DD/RR') ) → exp_Convert.v_PAY_DTE = SUBSTR(PAY_DTE, 1, 2) \|\| '/' \|\| SUBSTR(PAY_DTE, 3, 2) \|\| '/' \|\| SUBSTR(PAY_DTE, 5, 2) --Convert PAY DTE to MM/DD/RR format → fil_EMP_REC_TYPE_1_EMP_DETAIL.WS_LES_PAY_DT → Norm_EMP_REC_TYPE_1.WS_LES_PAY_DT → EMP_REC_TYPE_1.WS_LES_PAY_DT | EMP_REC_TYPE_1.WS_LES_PAY_DT |
| LES_EMP_DETAIL_RECTYPE_1_TBL | EMPLOYEE_NAME | exp_Final.EMPLOYEE_NAME → jnr_LES_NUMBER.EMPLOYEE_NAME → fil_EMP_REC_TYPE_1.EMPLOYEE_NAME → exp_Convert.EMPLOYEE_NAME → fil_EMP_REC_TYPE_1_EMP_DETAIL.WS_LES_EYE_NME → Norm_EMP_REC_TYPE_1.WS_LES_EYE_NME → EMP_REC_TYPE_1.WS_LES_EYE_NME | EMP_REC_TYPE_1.WS_LES_EYE_NME |
| LES_EMP_DETAIL_RECTYPE_1_TBL | PAY_PLAN_CD | exp_Final.PAY_PLAN_CD → jnr_LES_NUMBER.PAY_PLAN_CD → fil_EMP_REC_TYPE_1.PAY_PLAN_CD → exp_Convert.PAY_PLAN_CD → fil_EMP_REC_TYPE_1_EMP_DETAIL.WS_LES_PAY_PLAN → Norm_EMP_REC_TYPE_1.WS_LES_PAY_PLAN → EMP_REC_TYPE_1.WS_LES_PAY_PLAN | EMP_REC_TYPE_1.WS_LES_PAY_PLAN |
| LES_EMP_DETAIL_RECTYPE_1_TBL | GRADE | exp_Final.GRADE → jnr_LES_NUMBER.GRADE → fil_EMP_REC_TYPE_1.GRADE → exp_Convert.GRADE → fil_EMP_REC_TYPE_1_EMP_DETAIL.WS_LES_PAY_GRADE → Norm_EMP_REC_TYPE_1.WS_LES_PAY_GRADE → EMP_REC_TYPE_1.WS_LES_PAY_GRADE | EMP_REC_TYPE_1.WS_LES_PAY_GRADE |
| LES_EMP_DETAIL_RECTYPE_1_TBL | STEP | exp_Final.STEP → jnr_LES_NUMBER.STEP → fil_EMP_REC_TYPE_1.STEP → exp_Convert.STEP → fil_EMP_REC_TYPE_1_EMP_DETAIL.WS_LES_PAY_STEP → Norm_EMP_REC_TYPE_1.WS_LES_PAY_STEP → EMP_REC_TYPE_1.WS_LES_PAY_STEP | EMP_REC_TYPE_1.WS_LES_PAY_STEP |
| LES_EMP_DETAIL_RECTYPE_1_TBL | HRLY_RATE | exp_Final.HRLY_RATE → jnr_LES_NUMBER.HRLY_RATE → fil_EMP_REC_TYPE_1.HRLY_RATE → exp_Convert.HRLY_RATE → fil_EMP_REC_TYPE_1_EMP_DETAIL.WS_LES_HRLY_RATE → Norm_EMP_REC_TYPE_1.WS_LES_HRLY_RATE → EMP_REC_TYPE_1.WS_LES_HRLY_RATE | EMP_REC_TYPE_1.WS_LES_HRLY_RATE |
| LES_EMP_DETAIL_RECTYPE_1_TBL | BASE_OT_RATE | exp_Final.BASE_OT_RATE → jnr_LES_NUMBER.BASE_OT_RATE → fil_EMP_REC_TYPE_1.BASE_OT_RATE → exp_Convert.BASE_OT_RATE → fil_EMP_REC_TYPE_1_EMP_DETAIL.WS_LES_BASIC_OT_RATE → Norm_EMP_REC_TYPE_1.WS_LES_BASIC_OT_RATE → EMP_REC_TYPE_1.WS_LES_BASIC_OT_RATE | EMP_REC_TYPE_1.WS_LES_BASIC_OT_RATE |
| LES_EMP_DETAIL_RECTYPE_1_TBL | BASE_PAY | exp_Final.BASE_PAY → jnr_LES_NUMBER.BASE_PAY → fil_EMP_REC_TYPE_1.BASE_PAY → exp_Convert.BASE_PAY → fil_EMP_REC_TYPE_1_EMP_DETAIL.WS_LES_BASIC_PAY → Norm_EMP_REC_TYPE_1.WS_LES_BASIC_PAY → EMP_REC_TYPE_1.WS_LES_BASIC_PAY | EMP_REC_TYPE_1.WS_LES_BASIC_PAY |
| LES_EMP_DETAIL_RECTYPE_1_TBL | LOCALITY_ADJ | exp_Final.LOCALITY_ADJ → jnr_LES_NUMBER.LOCALITY_ADJ → fil_EMP_REC_TYPE_1.LOCALITY_ADJ → exp_Convert.LOCALITY_ADJ → fil_EMP_REC_TYPE_1_EMP_DETAIL.WS_LES_LOCAL_ADJ → Norm_EMP_REC_TYPE_1.WS_LES_LOCAL_ADJ → EMP_REC_TYPE_1.WS_LES_LOCAL_ADJ | EMP_REC_TYPE_1.WS_LES_LOCAL_ADJ |
| LES_EMP_DETAIL_RECTYPE_1_TBL | ADJ_BASE_PAY | exp_Final.ADJ_BASE_PAY → jnr_LES_NUMBER.ADJ_BASE_PAY → fil_EMP_REC_TYPE_1.ADJ_BASE_PAY → exp_Convert.ADJ_BASE_PAY → fil_EMP_REC_TYPE_1_EMP_DETAIL.WS_LES_ADJ_BASIC_PAY → Norm_EMP_REC_TYPE_1.WS_LES_ADJ_BASIC_PAY → EMP_REC_TYPE_1.WS_LES_ADJ_BASIC_PAY | EMP_REC_TYPE_1.WS_LES_ADJ_BASIC_PAY |
| LES_EMP_DETAIL_RECTYPE_1_TBL | LOCALITY_PERCENTAGE | exp_Final.LOCALITY_PERCENTAGE → jnr_LES_NUMBER.LOCALITY_PERCENTAGE → fil_EMP_REC_TYPE_1.LOCALITY_PERCENTAGE → exp_Convert.LOCALITY_PERCENTAGE → fil_EMP_REC_TYPE_1_EMP_DETAIL.WS_LES_LOCAL_PCT → Norm_EMP_REC_TYPE_1.WS_LES_LOCAL_PCT → EMP_REC_TYPE_1.WS_LES_LOCAL_PCT | EMP_REC_TYPE_1.WS_LES_LOCAL_PCT |
| LES_EMP_DETAIL_RECTYPE_1_TBL | FLSA_STATUS | exp_Final.FLSA_STATUS → jnr_LES_NUMBER.FLSA_STATUS → fil_EMP_REC_TYPE_1.FLSA_STATUS → exp_Convert.FLSA_STATUS → fil_EMP_REC_TYPE_1_EMP_DETAIL.WS_LES_FLSA → Norm_EMP_REC_TYPE_1.WS_LES_FLSA → EMP_REC_TYPE_1.WS_LES_FLSA | EMP_REC_TYPE_1.WS_LES_FLSA |
| LES_EMP_DETAIL_RECTYPE_1_TBL | LV_SCD_DTE | exp_Final.LV_SCD_DTE → jnr_LES_NUMBER.LV_SCD_DTE → fil_EMP_REC_TYPE_1.LV_SCD_DTE → exp_Convert.o_LV_SCD_DTE = IIF(IS_DATE(v_LV_SCD_DTE, 'MM/DD/RR'), TO_DATE(v_LV_SCD_DTE, 'MM/DD/RR') ) → exp_Convert.v_LV_SCD_DTE = SUBSTR(LV_SCD_DTE, 1, 2) \|\| '/' \|\| SUBSTR(LV_SCD_DTE, 3, 2) \|\| '/' \|\| SUBSTR(LV_SCD_DTE, 5, 2) --Convert LV SCD DTE to MM/DD/RR format → fil_EMP_REC_TYPE_1_EMP_DETAIL.WS_LES_SCD_LEAVE_DT → Norm_EMP_REC_TYPE_1.WS_LES_SCD_LEAVE_DT → EMP_REC_TYPE_1.WS_LES_SCD_LEAVE_DT | EMP_REC_TYPE_1.WS_LES_SCD_LEAVE_DT |
| LES_EMP_DETAIL_RECTYPE_1_TBL | MIL_LV_CARRY | exp_Final.MIL_LV_CARRY → jnr_LES_NUMBER.MIL_LV_CARRY → fil_EMP_REC_TYPE_1.MIL_LV_CARRY → exp_Convert.MIL_LV_CARRY → fil_EMP_REC_TYPE_1_EMP_DETAIL.WS_LES_MAX_LV_CRY → Norm_EMP_REC_TYPE_1.WS_LES_MAX_LV_CRY → EMP_REC_TYPE_1.WS_LES_MAX_LV_CRY | EMP_REC_TYPE_1.WS_LES_MAX_LV_CRY |
| LES_EMP_DETAIL_RECTYPE_1_TBL | LV_YR_END_DTE | exp_Final.LV_YR_END_DTE → jnr_LES_NUMBER.LV_YR_END_DTE → fil_EMP_REC_TYPE_1.LV_YR_END_DTE → exp_Convert.o_LV_YR_END_DTE = IIF(IS_DATE(v_LV_YR_END_DTE, 'MM/DD/RR'), TO_DATE(v_LV_YR_END_DTE, 'MM/DD/RR') ) → exp_Convert.v_LV_YR_END_DTE = SUBSTR(LV_YR_END_DTE, 1, 2) \|\| '/' \|\| SUBSTR(LV_YR_END_DTE, 3, 2) \|\| '/' \|\| SUBSTR(LV_YR_END_DTE, 5, 2) --Convert LV YR END DTE to MM/DD/RR format → fil_EMP_REC_TYPE_1_EMP_DETAIL.WS_LES_LV_YR_END_DT → Norm_EMP_REC_TYPE_1.WS_LES_LV_YR_END_DT → EMP_REC_TYPE_1.WS_LES_LV_YR_END_DT | EMP_REC_TYPE_1.WS_LES_LV_YR_END_DT |
| LES_EMP_DETAIL_RECTYPE_1_TBL | LAST_INCREASE_DTE | exp_Final.LAST_INCREASE_DTE → jnr_LES_NUMBER.LAST_INCREASE_DTE → fil_EMP_REC_TYPE_1.LAST_INCREASE_DTE → exp_Convert.o_LAST_INCREASE_DTE = IIF(IS_DATE(v_LAST_INCREASE_DTE, 'MM/DD/RR'), TO_DATE(v_LAST_INCREASE_DTE, 'MM/DD/RR') ) → exp_Convert.v_LAST_INCREASE_DTE = SUBSTR(LAST_INCREASE_DTE, 1, 2) \|\| '/' \|\| SUBSTR(LAST_INCREASE_DTE, 3, 2) \|\| '/' \|\| SUBSTR(LAST_INCREASE_DTE, 5, 2) --Convert LAST INCREASE DTE to MM/DD/RR format → fil_EMP_REC_TYPE_1_EMP_DETAIL.WS_LES_DATE_LST_INC → Norm_EMP_REC_TYPE_1.WS_LES_DATE_LST_INC → EMP_REC_TYPE_1.WS_LES_DATE_LST_INC | EMP_REC_TYPE_1.WS_LES_DATE_LST_INC |

## Mapping `m_LES_Load_LES_EMP_DETAIL_RECTYPE_2_TBL`

- Sessions: `s_LES_Load_LES_EMP_DETAIL_RECTYPE_2_TBL` (#7)
- Sources: `EMP_REC_TYPE_2`, `LES_EMP_DETAIL_TBL`
- Target instances: `LES_EMP_DETAIL_RECTYPE_2_TBL`

### Transformation `Norm_EMP_REC_TYPE_2` (Normalizer)

- **Reset**: `NO`
- **Restart**: `NO`

### Transformation `SQ_LES_EMP_DETAIL_TBL` (Source Qualifier)

- **Source Filter**: `LES_EMP_DETAIL_TBL.PP_END_YEAR = $$MAP_PP_END_YEAR AND LES_EMP_DETAIL_TBL.PP_NUM = $$MAP_PP_NUM --LES_EMP_DETAILS_TBL.PP_END_DTE = '$$MAP_PP_END_DTE'`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `fil_EMP_REC_TYPE_2` (Filter)

- **Filter Condition**: `WS_LES_REC_TYPE2 = '*2'`

### Transformation `fil_EMP_REC_TYPE_2_EMP_DETAIL` (Filter)

- **Filter Condition**: `WS_LES_REC_TYPE2 = '*2' OR WS_LES_REC_TYPE2 = '*E'`

### Transformation `jnr_LES_NUMBER` (Joiner)

- **Join Condition**: `LES_NUMBER = EMP2_LES_NUMBER`
- **Join Type**: `Normal Join`
- **Null ordering in master**: `Null Is Highest Value`
- **Null ordering in detail**: `Null Is Highest Value`
- **Sorted Input**: `NO`

- Joiner `jnr_LES_NUMBER`: Normal Join ON `LES_NUMBER = EMP2_LES_NUMBER`
- Normalizer `Norm_EMP_REC_TYPE_2` (vsam=True, source EMP_REC_TYPE_2) occurs: —; generated: —

### Target instance `LES_EMP_DETAIL_RECTYPE_2_TBL` (table `LES_EMP_DETAIL_RECTYPE_2_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LES_EMP_DETAIL_RECTYPE_2_TBL | PP_END_YEAR | exp_Final.PP_END_YEAR → jnr_LES_NUMBER.PP_END_YEAR → SQ_LES_EMP_DETAIL_TBL.PP_END_YEAR → LES_EMP_DETAIL_TBL.PP_END_YEAR | LES_EMP_DETAIL_TBL.PP_END_YEAR |
| LES_EMP_DETAIL_RECTYPE_2_TBL | PP_NUM | exp_Final.PP_NUM → jnr_LES_NUMBER.PP_NUM → SQ_LES_EMP_DETAIL_TBL.PP_NUM → LES_EMP_DETAIL_TBL.PP_NUM | LES_EMP_DETAIL_TBL.PP_NUM |
| LES_EMP_DETAIL_RECTYPE_2_TBL | LES_NUMBER | exp_Final.LES_NUMBER → jnr_LES_NUMBER.EMP2_LES_NUMBER → fil_EMP_REC_TYPE_2.EMP2_LES_NUMBER → exp_Convert.o_LES_NUMBER = IIF(IS_NUMBER(v_LES_NUMBER), TO_INTEGER(v_LES_NUMBER) ) → exp_Convert.v_LES_NUMBER = IIF(WS_LES_REC_TYPE2 = '*E', SUBSTR(WS_LES_NETPAY_FINORG,10,7), v_LES_NUMBER ) → fil_EMP_REC_TYPE_2_EMP_DETAIL.WS_LES_REC_TYPE2 → Norm_EMP_REC_TYPE_2.WS_LES_REC_TYPE2 → EMP_REC_TYPE_2.WS_LES_REC_TYPE2 → fil_EMP_REC_TYPE_2_EMP_DETAIL.WS_LES_NETPAY_FINORG → Norm_EMP_REC_TYPE_2.WS_LES_NETPAY_FINORG → EMP_REC_TYPE_2.WS_LES_NETPAY_FINORG | EMP_REC_TYPE_2.WS_LES_NETPAY_FINORG; EMP_REC_TYPE_2.WS_LES_REC_TYPE2 |
| LES_EMP_DETAIL_RECTYPE_2_TBL | PSEUDOSSN | exp_Final.PSEUDOSSN → jnr_LES_NUMBER.PSEUDOSSN → SQ_LES_EMP_DETAIL_TBL.PSEUDOSSN → LES_EMP_DETAIL_TBL.PSEUDOSSN | LES_EMP_DETAIL_TBL.PSEUDOSSN |
| LES_EMP_DETAIL_RECTYPE_2_TBL | NET_PAY_FINANCIAL_ORG | exp_Final.NET_PAY_FINANCIAL_ORG → jnr_LES_NUMBER.WS_LES_NETPAY_FINORG → fil_EMP_REC_TYPE_2.WS_LES_NETPAY_FINORG → exp_Convert.WS_LES_NETPAY_FINORG → fil_EMP_REC_TYPE_2_EMP_DETAIL.WS_LES_NETPAY_FINORG → Norm_EMP_REC_TYPE_2.WS_LES_NETPAY_FINORG → EMP_REC_TYPE_2.WS_LES_NETPAY_FINORG | EMP_REC_TYPE_2.WS_LES_NETPAY_FINORG |
| LES_EMP_DETAIL_RECTYPE_2_TBL | ALLOT1_FINANCIAL_ORG | exp_Final.ALLOT1_FINANCIAL_ORG → jnr_LES_NUMBER.WS_LES_ALLT1_FINORG → fil_EMP_REC_TYPE_2.WS_LES_ALLT1_FINORG → exp_Convert.WS_LES_ALLT1_FINORG → fil_EMP_REC_TYPE_2_EMP_DETAIL.WS_LES_ALLT1_FINORG → Norm_EMP_REC_TYPE_2.WS_LES_ALLT1_FINORG → EMP_REC_TYPE_2.WS_LES_ALLT1_FINORG | EMP_REC_TYPE_2.WS_LES_ALLT1_FINORG |
| LES_EMP_DETAIL_RECTYPE_2_TBL | ALLOT2_FINANCIAL_ORG | exp_Final.ALLOT2_FINANCIAL_ORG → jnr_LES_NUMBER.WS_LES_ALLT2_FINORG → fil_EMP_REC_TYPE_2.WS_LES_ALLT2_FINORG → exp_Convert.WS_LES_ALLT2_FINORG → fil_EMP_REC_TYPE_2_EMP_DETAIL.WS_LES_ALLT2_FINORG → Norm_EMP_REC_TYPE_2.WS_LES_ALLT2_FINORG → EMP_REC_TYPE_2.WS_LES_ALLT2_FINORG | EMP_REC_TYPE_2.WS_LES_ALLT2_FINORG |
| LES_EMP_DETAIL_RECTYPE_2_TBL | FEDERAL_TAX | exp_Final.FEDERAL_TAX → jnr_LES_NUMBER.WS_LES_FED_TIT → fil_EMP_REC_TYPE_2.WS_LES_FED_TIT → exp_Convert.WS_LES_FED_TIT → fil_EMP_REC_TYPE_2_EMP_DETAIL.WS_LES_FED_TIT → Norm_EMP_REC_TYPE_2.WS_LES_FED_TIT → EMP_REC_TYPE_2.WS_LES_FED_TIT | EMP_REC_TYPE_2.WS_LES_FED_TIT |
| LES_EMP_DETAIL_RECTYPE_2_TBL | FED_MARITAL_STATUS | exp_Final.FED_MARITAL_STATUS → jnr_LES_NUMBER.WS_LES_FED_MS → fil_EMP_REC_TYPE_2.WS_LES_FED_MS → exp_Convert.WS_LES_FED_MS → fil_EMP_REC_TYPE_2_EMP_DETAIL.WS_LES_FED_MS → Norm_EMP_REC_TYPE_2.WS_LES_FED_MS → EMP_REC_TYPE_2.WS_LES_FED_MS | EMP_REC_TYPE_2.WS_LES_FED_MS |
| LES_EMP_DETAIL_RECTYPE_2_TBL | FED_EXCEPTIONS | exp_Final.FED_EXCEPTIONS → jnr_LES_NUMBER.WS_LES_FED_ITW_XMP → fil_EMP_REC_TYPE_2.WS_LES_FED_ITW_XMP → exp_Convert.WS_LES_FED_ITW_XMP → fil_EMP_REC_TYPE_2_EMP_DETAIL.WS_LES_FED_ITW_XMP → Norm_EMP_REC_TYPE_2.WS_LES_FED_ITW_XMP → EMP_REC_TYPE_2.WS_LES_FED_ITW_XMP | EMP_REC_TYPE_2.WS_LES_FED_ITW_XMP |
| LES_EMP_DETAIL_RECTYPE_2_TBL | FED_ADDNL_WITHHOLDING | exp_Final.FED_ADDNL_WITHHOLDING → jnr_LES_NUMBER.WS_LES_FED_ADDTL → fil_EMP_REC_TYPE_2.WS_LES_FED_ADDTL → exp_Convert.WS_LES_FED_ADDTL → fil_EMP_REC_TYPE_2_EMP_DETAIL.WS_LES_FED_ADDTL → Norm_EMP_REC_TYPE_2.WS_LES_FED_ADDTL → EMP_REC_TYPE_2.WS_LES_FED_ADDTL | EMP_REC_TYPE_2.WS_LES_FED_ADDTL |
| LES_EMP_DETAIL_RECTYPE_2_TBL | STATE1_TAX | exp_Final.STATE1_TAX → jnr_LES_NUMBER.WS_LES_ST_TX1_TIT → fil_EMP_REC_TYPE_2.WS_LES_ST_TX1_TIT → exp_Convert.WS_LES_ST_TX1_TIT → fil_EMP_REC_TYPE_2_EMP_DETAIL.WS_LES_ST_TX1_TIT → Norm_EMP_REC_TYPE_2.WS_LES_ST_TX1_TIT → EMP_REC_TYPE_2.WS_LES_ST_TX1_TIT | EMP_REC_TYPE_2.WS_LES_ST_TX1_TIT |
| LES_EMP_DETAIL_RECTYPE_2_TBL | STATE1_MARITAL_STATUS | exp_Final.STATE1_MARITAL_STATUS → jnr_LES_NUMBER.WS_LES_ST_TX1_MS → fil_EMP_REC_TYPE_2.WS_LES_ST_TX1_MS → exp_Convert.WS_LES_ST_TX1_MS → fil_EMP_REC_TYPE_2_EMP_DETAIL.WS_LES_ST_TX1_MS → Norm_EMP_REC_TYPE_2.WS_LES_ST_TX1_MS → EMP_REC_TYPE_2.WS_LES_ST_TX1_MS | EMP_REC_TYPE_2.WS_LES_ST_TX1_MS |
| LES_EMP_DETAIL_RECTYPE_2_TBL | STATE1_EXCEPTIONS | exp_Final.STATE1_EXCEPTIONS → jnr_LES_NUMBER.WS_LES_ST_TX1_XMP → fil_EMP_REC_TYPE_2.WS_LES_ST_TX1_XMP → exp_Convert.WS_LES_ST_TX1_XMP → fil_EMP_REC_TYPE_2_EMP_DETAIL.WS_LES_ST_TX1_XMP → Norm_EMP_REC_TYPE_2.WS_LES_ST_TX1_XMP → EMP_REC_TYPE_2.WS_LES_ST_TX1_XMP | EMP_REC_TYPE_2.WS_LES_ST_TX1_XMP |
| LES_EMP_DETAIL_RECTYPE_2_TBL | STATE1_ADDNL_AMOUNT | exp_Final.STATE1_ADDNL_AMOUNT → jnr_LES_NUMBER.WS_LES_ST_TX1_ADDTL → fil_EMP_REC_TYPE_2.WS_LES_ST_TX1_ADDTL → exp_Convert.WS_LES_ST_TX1_ADDTL → fil_EMP_REC_TYPE_2_EMP_DETAIL.WS_LES_ST_TX1_ADDTL → Norm_EMP_REC_TYPE_2.WS_LES_ST_TX1_ADDTL → EMP_REC_TYPE_2.WS_LES_ST_TX1_ADDTL | EMP_REC_TYPE_2.WS_LES_ST_TX1_ADDTL |
| LES_EMP_DETAIL_RECTYPE_2_TBL | STATE2_TAX | exp_Final.STATE2_TAX → jnr_LES_NUMBER.WS_LES_ST_TX2_TIT → fil_EMP_REC_TYPE_2.WS_LES_ST_TX2_TIT → exp_Convert.WS_LES_ST_TX2_TIT → fil_EMP_REC_TYPE_2_EMP_DETAIL.WS_LES_ST_TX2_TIT → Norm_EMP_REC_TYPE_2.WS_LES_ST_TX2_TIT → EMP_REC_TYPE_2.WS_LES_ST_TX2_TIT | EMP_REC_TYPE_2.WS_LES_ST_TX2_TIT |
| LES_EMP_DETAIL_RECTYPE_2_TBL | STATE2_MARITAL_STATUS | exp_Final.STATE2_MARITAL_STATUS → jnr_LES_NUMBER.WS_LES_ST_TX2_MS → fil_EMP_REC_TYPE_2.WS_LES_ST_TX2_MS → exp_Convert.WS_LES_ST_TX2_MS → fil_EMP_REC_TYPE_2_EMP_DETAIL.WS_LES_ST_TX2_MS → Norm_EMP_REC_TYPE_2.WS_LES_ST_TX2_MS → EMP_REC_TYPE_2.WS_LES_ST_TX2_MS | EMP_REC_TYPE_2.WS_LES_ST_TX2_MS |

## Mapping `m_LES_Load_LES_EMP_DETAIL_RECTYPE_3_TBL`

- Sessions: `s_LES_Load_LES_EMP_DETAIL_RECTYPE_3_TBL` (#8)
- Sources: `EMP_REC_TYPE_3`, `LES_EMP_DETAIL_TBL`
- Target instances: `LES_EMP_DETAIL_RECTYPE_3_TBL`

### Transformation `Norm_EMP_REC_TYPE_3` (Normalizer)

- **Reset**: `NO`
- **Restart**: `NO`

### Transformation `SQ_LES_EMP_DETAIL_TBL` (Source Qualifier)

- **Source Filter**: `LES_EMP_DETAIL_TBL.PP_END_YEAR = $$MAP_PP_END_YEAR AND LES_EMP_DETAIL_TBL.PP_NUM = $$MAP_PP_NUM --LES_EMP_DETAILS_TBL.PP_END_DTE = '$$MAP_PP_END_DTE'`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `fil_EMP_REC_TYPE_3` (Filter)

- **Filter Condition**: `WS_LES_REC_TYPE3 = '*3'`

### Transformation `fil_EMP_REC_TYPE_3_EMP_DETAIL` (Filter)

- **Filter Condition**: `WS_LES_REC_TYPE3 = '*3' OR WS_LES_REC_TYPE3 = '*E'`

### Transformation `jnr_LES_NUMBER` (Joiner)

- **Join Condition**: `LES_NUMBER = EMP3_LES_NUMBER`
- **Join Type**: `Normal Join`
- **Null ordering in master**: `Null Is Highest Value`
- **Null ordering in detail**: `Null Is Highest Value`
- **Sorted Input**: `NO`

- Joiner `jnr_LES_NUMBER`: Normal Join ON `LES_NUMBER = EMP3_LES_NUMBER`
- Normalizer `Norm_EMP_REC_TYPE_3` (vsam=True, source EMP_REC_TYPE_3) occurs: —; generated: —

### Target instance `LES_EMP_DETAIL_RECTYPE_3_TBL` (table `LES_EMP_DETAIL_RECTYPE_3_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LES_EMP_DETAIL_RECTYPE_3_TBL | PP_END_YEAR | exp_Final.PP_END_YEAR → jnr_LES_NUMBER.PP_END_YEAR → SQ_LES_EMP_DETAIL_TBL.PP_END_YEAR → LES_EMP_DETAIL_TBL.PP_END_YEAR | LES_EMP_DETAIL_TBL.PP_END_YEAR |
| LES_EMP_DETAIL_RECTYPE_3_TBL | PP_NUM | exp_Final.PP_NUM → jnr_LES_NUMBER.PP_NUM → SQ_LES_EMP_DETAIL_TBL.PP_NUM → LES_EMP_DETAIL_TBL.PP_NUM | LES_EMP_DETAIL_TBL.PP_NUM |
| LES_EMP_DETAIL_RECTYPE_3_TBL | LES_NUMBER | exp_Final.LES_NUMBER → jnr_LES_NUMBER.EMP3_LES_NUMBER → fil_EMP_REC_TYPE_3.EMP3_LES_NUMBER → exp_Convert.EMP3_LES_NUMBER = IIF(IS_NUMBER(v_LES_NUMBER), TO_INTEGER(v_LES_NUMBER) ) → exp_Convert.v_LES_NUMBER = IIF(WS_LES_REC_TYPE3 = '*E', v_LES_ST_TX2_ADDL_CHAR \|\| WS_LES_LC_TX1_TIT, v_LES_NUMBER ) → fil_EMP_REC_TYPE_3_EMP_DETAIL.WS_LES_REC_TYPE3 → Norm_EMP_REC_TYPE_3.WS_LES_REC_TYPE3 → EMP_REC_TYPE_3.WS_LES_REC_TYPE3 → exp_Convert.v_LES_ST_TX2_ADDL_CHAR = SUBSTR(TO_CHAR(WS_LES_ST_TX2_ADDTL), 4,1) → fil_EMP_REC_TYPE_3_EMP_DETAIL.WS_LES_ST_TX2_ADDTL → Norm_EMP_REC_TYPE_3.WS_LES_ST_TX2_ADDTL → EMP_REC_TYPE_3.WS_LES_ST_TX2_ADDTL → fil_EMP_REC_TYPE_3_EMP_DETAIL.WS_LES_LC_TX1_TIT → Norm_EMP_REC_TYPE_3.WS_LES_LC_TX1_TIT → EMP_REC_TYPE_3.WS_LES_LC_TX1_TIT | EMP_REC_TYPE_3.WS_LES_LC_TX1_TIT; EMP_REC_TYPE_3.WS_LES_REC_TYPE3; EMP_REC_TYPE_3.WS_LES_ST_TX2_ADDTL |
| LES_EMP_DETAIL_RECTYPE_3_TBL | PSEUDOSSN | exp_Final.PSEUDOSSN → jnr_LES_NUMBER.PSEUDOSSN → SQ_LES_EMP_DETAIL_TBL.PSEUDOSSN → LES_EMP_DETAIL_TBL.PSEUDOSSN | LES_EMP_DETAIL_TBL.PSEUDOSSN |
| LES_EMP_DETAIL_RECTYPE_3_TBL | STATE2_EXCEPTIONS | exp_Final.STATE2_EXCEPTIONS → jnr_LES_NUMBER.WS_LES_ST_TX2_XMP → fil_EMP_REC_TYPE_3.WS_LES_ST_TX2_XMP → exp_Convert.WS_LES_ST_TX2_XMP → fil_EMP_REC_TYPE_3_EMP_DETAIL.WS_LES_ST_TX2_XMP → Norm_EMP_REC_TYPE_3.WS_LES_ST_TX2_XMP → EMP_REC_TYPE_3.WS_LES_ST_TX2_XMP | EMP_REC_TYPE_3.WS_LES_ST_TX2_XMP |
| LES_EMP_DETAIL_RECTYPE_3_TBL | STATE2_ADDNL_AMOUNT | exp_Final.STATE2_ADDNL_AMOUNT → jnr_LES_NUMBER.WS_LES_ST_TX2_ADDTL → fil_EMP_REC_TYPE_3.WS_LES_ST_TX2_ADDTL → exp_Convert.WS_LES_ST_TX2_ADDTL → fil_EMP_REC_TYPE_3_EMP_DETAIL.WS_LES_ST_TX2_ADDTL → Norm_EMP_REC_TYPE_3.WS_LES_ST_TX2_ADDTL → EMP_REC_TYPE_3.WS_LES_ST_TX2_ADDTL | EMP_REC_TYPE_3.WS_LES_ST_TX2_ADDTL |
| LES_EMP_DETAIL_RECTYPE_3_TBL | LOCAL1_TAX | exp_Final.LOCAL1_TAX → jnr_LES_NUMBER.WS_LES_LC_TX1_TIT → fil_EMP_REC_TYPE_3.WS_LES_LC_TX1_TIT → exp_Convert.WS_LES_LC_TX1_TIT → fil_EMP_REC_TYPE_3_EMP_DETAIL.WS_LES_LC_TX1_TIT → Norm_EMP_REC_TYPE_3.WS_LES_LC_TX1_TIT → EMP_REC_TYPE_3.WS_LES_LC_TX1_TIT | EMP_REC_TYPE_3.WS_LES_LC_TX1_TIT |
| LES_EMP_DETAIL_RECTYPE_3_TBL | LOCAL1_MARITAL_STATUS | exp_Final.LOCAL1_MARITAL_STATUS → jnr_LES_NUMBER.WS_LES_LC_TX1_MS → fil_EMP_REC_TYPE_3.WS_LES_LC_TX1_MS → exp_Convert.WS_LES_LC_TX1_MS → fil_EMP_REC_TYPE_3_EMP_DETAIL.WS_LES_LC_TX1_MS → Norm_EMP_REC_TYPE_3.WS_LES_LC_TX1_MS → EMP_REC_TYPE_3.WS_LES_LC_TX1_MS | EMP_REC_TYPE_3.WS_LES_LC_TX1_MS |
| LES_EMP_DETAIL_RECTYPE_3_TBL | LOCAL1_EXCEPTIONS | exp_Final.LOCAL1_EXCEPTIONS → jnr_LES_NUMBER.WS_LES_LC_TX1_XMP → fil_EMP_REC_TYPE_3.WS_LES_LC_TX1_XMP → exp_Convert.WS_LES_LC_TX1_XMP → fil_EMP_REC_TYPE_3_EMP_DETAIL.WS_LES_LC_TX1_XMP → Norm_EMP_REC_TYPE_3.WS_LES_LC_TX1_XMP → EMP_REC_TYPE_3.WS_LES_LC_TX1_XMP | EMP_REC_TYPE_3.WS_LES_LC_TX1_XMP |
| LES_EMP_DETAIL_RECTYPE_3_TBL | LOCAL1_ADDNL_AMOUNT | exp_Final.LOCAL1_ADDNL_AMOUNT → jnr_LES_NUMBER.WS_LES_LC_TX1_ADDTL → fil_EMP_REC_TYPE_3.WS_LES_LC_TX1_ADDTL → exp_Convert.WS_LES_LC_TX1_ADDTL → fil_EMP_REC_TYPE_3_EMP_DETAIL.WS_LES_LC_TX1_ADDTL → Norm_EMP_REC_TYPE_3.WS_LES_LC_TX1_ADDTL → EMP_REC_TYPE_3.WS_LES_LC_TX1_ADDTL | EMP_REC_TYPE_3.WS_LES_LC_TX1_ADDTL |
| LES_EMP_DETAIL_RECTYPE_3_TBL | LOCAL1_TAX_NAME | exp_Final.LOCAL1_TAX_NAME → jnr_LES_NUMBER.WS_LES_LC_TX1_NME → fil_EMP_REC_TYPE_3.WS_LES_LC_TX1_NME → exp_Convert.WS_LES_LC_TX1_NME → fil_EMP_REC_TYPE_3_EMP_DETAIL.WS_LES_LC_TX1_NME → Norm_EMP_REC_TYPE_3.WS_LES_LC_TX1_NME → EMP_REC_TYPE_3.WS_LES_LC_TX1_NME | EMP_REC_TYPE_3.WS_LES_LC_TX1_NME |
| LES_EMP_DETAIL_RECTYPE_3_TBL | LOCAL2_TAX | exp_Final.LOCAL2_TAX → jnr_LES_NUMBER.WS_LES_LC_TX2_TIT → fil_EMP_REC_TYPE_3.WS_LES_LC_TX2_TIT → exp_Convert.WS_LES_LC_TX2_TIT → fil_EMP_REC_TYPE_3_EMP_DETAIL.WS_LES_LC_TX2_TIT → Norm_EMP_REC_TYPE_3.WS_LES_LC_TX2_TIT → EMP_REC_TYPE_3.WS_LES_LC_TX2_TIT | EMP_REC_TYPE_3.WS_LES_LC_TX2_TIT |
| LES_EMP_DETAIL_RECTYPE_3_TBL | LOCAL2_MARITAL_STATUS | exp_Final.LOCAL2_MARITAL_STATUS → jnr_LES_NUMBER.WS_LES_LC_TX2_MS → fil_EMP_REC_TYPE_3.WS_LES_LC_TX2_MS → exp_Convert.WS_LES_LC_TX2_MS → fil_EMP_REC_TYPE_3_EMP_DETAIL.WS_LES_LC_TX2_MS → Norm_EMP_REC_TYPE_3.WS_LES_LC_TX2_MS → EMP_REC_TYPE_3.WS_LES_LC_TX2_MS | EMP_REC_TYPE_3.WS_LES_LC_TX2_MS |
| LES_EMP_DETAIL_RECTYPE_3_TBL | LOCAL2_EXCEPTIONS | exp_Final.LOCAL2_EXCEPTIONS → jnr_LES_NUMBER.WS_LES_LC_TX2_XMP → fil_EMP_REC_TYPE_3.WS_LES_LC_TX2_XMP → exp_Convert.WS_LES_LC_TX2_XMP → fil_EMP_REC_TYPE_3_EMP_DETAIL.WS_LES_LC_TX2_XMP → Norm_EMP_REC_TYPE_3.WS_LES_LC_TX2_XMP → EMP_REC_TYPE_3.WS_LES_LC_TX2_XMP | EMP_REC_TYPE_3.WS_LES_LC_TX2_XMP |
| LES_EMP_DETAIL_RECTYPE_3_TBL | LOCAL2_ADDNL_AMOUNT | exp_Final.LOCAL2_ADDNL_AMOUNT → jnr_LES_NUMBER.WS_LES_LC_TX2_ADDTL → fil_EMP_REC_TYPE_3.WS_LES_LC_TX2_ADDTL → exp_Convert.WS_LES_LC_TX2_ADDTL → fil_EMP_REC_TYPE_3_EMP_DETAIL.WS_LES_LC_TX2_ADDTL → Norm_EMP_REC_TYPE_3.WS_LES_LC_TX2_ADDTL → EMP_REC_TYPE_3.WS_LES_LC_TX2_ADDTL | EMP_REC_TYPE_3.WS_LES_LC_TX2_ADDTL |
| LES_EMP_DETAIL_RECTYPE_3_TBL | LOCAL2_TAX_NAME | exp_Final.LOCAL2_TAX_NAME → jnr_LES_NUMBER.WS_LES_LC_TX2_NME → fil_EMP_REC_TYPE_3.WS_LES_LC_TX2_NME → exp_Convert.WS_LES_LC_TX2_NME → fil_EMP_REC_TYPE_3_EMP_DETAIL.WS_LES_LC_TX2_NME → Norm_EMP_REC_TYPE_3.WS_LES_LC_TX2_NME → EMP_REC_TYPE_3.WS_LES_LC_TX2_NME | EMP_REC_TYPE_3.WS_LES_LC_TX2_NME |
| LES_EMP_DETAIL_RECTYPE_3_TBL | CSRS | exp_Final.CSRS → jnr_LES_NUMBER.WS_LES_CSRS_TIT → fil_EMP_REC_TYPE_3.WS_LES_CSRS_TIT → exp_Convert.WS_LES_CSRS_TIT → fil_EMP_REC_TYPE_3_EMP_DETAIL.WS_LES_CSRS_TIT → Norm_EMP_REC_TYPE_3.WS_LES_CSRS_TIT → EMP_REC_TYPE_3.WS_LES_CSRS_TIT | EMP_REC_TYPE_3.WS_LES_CSRS_TIT |
| LES_EMP_DETAIL_RECTYPE_3_TBL | CSRS_CUM_AMT | exp_Final.CSRS_CUM_AMT → jnr_LES_NUMBER.WS_LES_CSRS_CUMM_AMT → fil_EMP_REC_TYPE_3.WS_LES_CSRS_CUMM_AMT → exp_Convert.WS_LES_CSRS_CUMM_AMT → fil_EMP_REC_TYPE_3_EMP_DETAIL.WS_LES_CSRS_CUMM_AMT → Norm_EMP_REC_TYPE_3.WS_LES_CSRS_CUMM_AMT → EMP_REC_TYPE_3.WS_LES_CSRS_CUMM_AMT | EMP_REC_TYPE_3.WS_LES_CSRS_CUMM_AMT |
| LES_EMP_DETAIL_RECTYPE_3_TBL | BIWEEKLY_AMT | exp_Final.BIWEEKLY_AMT → jnr_LES_NUMBER.WS_LES_BIWK_TIT → fil_EMP_REC_TYPE_3.WS_LES_BIWK_TIT → exp_Convert.WS_LES_BIWK_TIT → fil_EMP_REC_TYPE_3_EMP_DETAIL.WS_LES_BIWK_TIT → Norm_EMP_REC_TYPE_3.WS_LES_BIWK_TIT → EMP_REC_TYPE_3.WS_LES_BIWK_TIT | EMP_REC_TYPE_3.WS_LES_BIWK_TIT |
| LES_EMP_DETAIL_RECTYPE_3_TBL | BIWEEKLY_ANNUITY | exp_Final.BIWEEKLY_ANNUITY → jnr_LES_NUMBER.WS_LES_BIWK_ANNTY → fil_EMP_REC_TYPE_3.WS_LES_BIWK_ANNTY → exp_Convert.WS_LES_BIWK_ANNTY → fil_EMP_REC_TYPE_3_EMP_DETAIL.WS_LES_BIWK_ANNTY → Norm_EMP_REC_TYPE_3.WS_LES_BIWK_ANNTY → EMP_REC_TYPE_3.WS_LES_BIWK_ANNTY | EMP_REC_TYPE_3.WS_LES_BIWK_ANNTY |
| LES_EMP_DETAIL_RECTYPE_3_TBL | MILITARY_DEPOSIT | exp_Final.MILITARY_DEPOSIT → jnr_LES_NUMBER.WS_LES_MILDPS_TIT → fil_EMP_REC_TYPE_3.WS_LES_MILDPS_TIT → exp_Convert.WS_LES_MILDPS_TIT → fil_EMP_REC_TYPE_3_EMP_DETAIL.WS_LES_MILDPS_TIT → Norm_EMP_REC_TYPE_3.WS_LES_MILDPS_TIT → EMP_REC_TYPE_3.WS_LES_MILDPS_TIT | EMP_REC_TYPE_3.WS_LES_MILDPS_TIT |

## Mapping `m_LES_Load_LES_EMP_DETAIL_RECTYPE_4_TBL`

- Sessions: `s_LES_Load_LES_EMP_DETAIL_RECTYPE_4_TBL` (#9)
- Sources: `EMP_REC_TYPE_4`, `LES_EMP_DETAIL_TBL`
- Target instances: `LES_EMP_DETAIL_RECTYPE_4_TBL`

### Transformation `Norm_EMP_REC_TYPE_4` (Normalizer)

- **Reset**: `NO`
- **Restart**: `NO`

### Transformation `SQ_LES_EMP_DETAIL_TBL` (Source Qualifier)

- **Source Filter**: `LES_EMP_DETAIL_TBL.PP_END_YEAR = $$MAP_PP_END_YEAR AND LES_EMP_DETAIL_TBL.PP_NUM = $$MAP_PP_NUM`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `fil_EMP_REC_TYPE_4` (Filter)

- **Filter Condition**: `WS_LES_REC_TYPE4 = '*4'`

### Transformation `fil_EMP_REC_TYPE_4_EMP_DETAIL` (Filter)

- **Filter Condition**: `WS_LES_REC_TYPE4 = '*4' OR WS_LES_REC_TYPE4 = '*E'`

### Transformation `jnr_LES_NUMBER` (Joiner)

- **Join Condition**: `LES_NUMBER = EMP4_LES_NUMBER`
- **Join Type**: `Normal Join`
- **Null ordering in master**: `Null Is Highest Value`
- **Null ordering in detail**: `Null Is Highest Value`
- **Sorted Input**: `NO`

- Joiner `jnr_LES_NUMBER`: Normal Join ON `LES_NUMBER = EMP4_LES_NUMBER`
- Normalizer `Norm_EMP_REC_TYPE_4` (vsam=True, source EMP_REC_TYPE_4) occurs: —; generated: GK_EMP_REC_TYPE_4

### Target instance `LES_EMP_DETAIL_RECTYPE_4_TBL` (table `LES_EMP_DETAIL_RECTYPE_4_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LES_EMP_DETAIL_RECTYPE_4_TBL | PP_END_YEAR | exp_Final.PP_END_YEAR → jnr_LES_NUMBER.PP_END_YEAR → SQ_LES_EMP_DETAIL_TBL.PP_END_YEAR → LES_EMP_DETAIL_TBL.PP_END_YEAR | LES_EMP_DETAIL_TBL.PP_END_YEAR |
| LES_EMP_DETAIL_RECTYPE_4_TBL | PP_NUM | exp_Final.PP_NUM → jnr_LES_NUMBER.PP_NUM → SQ_LES_EMP_DETAIL_TBL.PP_NUM → LES_EMP_DETAIL_TBL.PP_NUM | LES_EMP_DETAIL_TBL.PP_NUM |
| LES_EMP_DETAIL_RECTYPE_4_TBL | LES_NUMBER | exp_Final.LES_NUMBER → jnr_LES_NUMBER.EMP4_LES_NUMBER → fil_EMP_REC_TYPE_4.EMP4_LES_NUMBER → exp_Convert.o_EMP4_LES_NUMBER = IIF(IS_NUMBER(v_LES_NUMBER), TO_INTEGER(v_LES_NUMBER) ) → exp_Convert.v_LES_NUMBER = IIF(WS_LES_REC_TYPE4 = '*E', SUBSTR(WS_LES_MILDPS_TIT2, 2, 4) \|\| SUBSTR(WS_LES_MILDPS_OWED_RDF, 1, 3), v_LES_NUMBER) → fil_EMP_REC_TYPE_4_EMP_DETAIL.WS_LES_REC_TYPE4 → Norm_EMP_REC_TYPE_4.WS_LES_REC_TYPE4 → EMP_REC_TYPE_4.WS_LES_REC_TYPE4 → fil_EMP_REC_TYPE_4_EMP_DETAIL.WS_LES_MILDPS_TIT2 → Norm_EMP_REC_TYPE_4.WS_LES_MILDPS_TIT2 → EMP_REC_TYPE_4.WS_LES_MILDPS_TIT2 → fil_EMP_REC_TYPE_4_EMP_DETAIL.WS_LES_MILDPS_OWED_RDF → Norm_EMP_REC_TYPE_4.WS_LES_MILDPS_OWED_RDF → EMP_REC_TYPE_4.WS_LES_MILDPS_OWED_RDF | EMP_REC_TYPE_4.WS_LES_MILDPS_OWED_RDF; EMP_REC_TYPE_4.WS_LES_MILDPS_TIT2; EMP_REC_TYPE_4.WS_LES_REC_TYPE4 |
| LES_EMP_DETAIL_RECTYPE_4_TBL | PSEUDOSSN | exp_Final.PSEUDOSSN → jnr_LES_NUMBER.PSEUDOSSN → SQ_LES_EMP_DETAIL_TBL.PSEUDOSSN → LES_EMP_DETAIL_TBL.PSEUDOSSN | LES_EMP_DETAIL_TBL.PSEUDOSSN |
| LES_EMP_DETAIL_RECTYPE_4_TBL | MIL_DEPOSIT_PAID | exp_Final.MIL_DEPOSIT_PAID → jnr_LES_NUMBER.WS_LES_MILDPS_PD → fil_EMP_REC_TYPE_4.WS_LES_MILDPS_PD → exp_Convert.WS_LES_MILDPS_PD → fil_EMP_REC_TYPE_4_EMP_DETAIL.WS_LES_MILDPS_PD → Norm_EMP_REC_TYPE_4.WS_LES_MILDPS_PD → EMP_REC_TYPE_4.WS_LES_MILDPS_PD | EMP_REC_TYPE_4.WS_LES_MILDPS_PD |
| LES_EMP_DETAIL_RECTYPE_4_TBL | MIL_DEPOSIT_2 | exp_Final.MIL_DEPOSIT_2 → jnr_LES_NUMBER.WS_LES_MILDPS_TIT2 → fil_EMP_REC_TYPE_4.WS_LES_MILDPS_TIT2 → exp_Convert.WS_LES_MILDPS_TIT2 → fil_EMP_REC_TYPE_4_EMP_DETAIL.WS_LES_MILDPS_TIT2 → Norm_EMP_REC_TYPE_4.WS_LES_MILDPS_TIT2 → EMP_REC_TYPE_4.WS_LES_MILDPS_TIT2 | EMP_REC_TYPE_4.WS_LES_MILDPS_TIT2 |
| LES_EMP_DETAIL_RECTYPE_4_TBL | MIL_DEPOSIT_BAL | exp_Final.MIL_DEPOSIT_BAL → jnr_LES_NUMBER.WS_LES_MILDPS_OWED → fil_EMP_REC_TYPE_4.WS_LES_MILDPS_OWED → exp_Convert.WS_LES_MILDPS_OWED → fil_EMP_REC_TYPE_4_EMP_DETAIL.WS_LES_MILDPS_OWED → Norm_EMP_REC_TYPE_4.WS_LES_MILDPS_OWED → EMP_REC_TYPE_4.WS_LES_MILDPS_OWED | EMP_REC_TYPE_4.WS_LES_MILDPS_OWED |
| LES_EMP_DETAIL_RECTYPE_4_TBL | GROSS_PAY_AMT | exp_Final.GROSS_PAY_AMT → jnr_LES_NUMBER.WS_LES_GRS_PAY_AMT → fil_EMP_REC_TYPE_4.WS_LES_GRS_PAY_AMT → exp_Convert.WS_LES_GRS_PAY_AMT → fil_EMP_REC_TYPE_4_EMP_DETAIL.WS_LES_GRS_PAY_AMT → Norm_EMP_REC_TYPE_4.WS_LES_GRS_PAY_AMT → EMP_REC_TYPE_4.WS_LES_GRS_PAY_AMT | EMP_REC_TYPE_4.WS_LES_GRS_PAY_AMT |
| LES_EMP_DETAIL_RECTYPE_4_TBL | GROSS_PAY_AMT_YTD | exp_Final.GROSS_PAY_AMT_YTD → jnr_LES_NUMBER.WS_LES_GRS_PAY_YTD → fil_EMP_REC_TYPE_4.WS_LES_GRS_PAY_YTD → exp_Convert.WS_LES_GRS_PAY_YTD → fil_EMP_REC_TYPE_4_EMP_DETAIL.WS_LES_GRS_PAY_YTD → Norm_EMP_REC_TYPE_4.WS_LES_GRS_PAY_YTD → EMP_REC_TYPE_4.WS_LES_GRS_PAY_YTD | EMP_REC_TYPE_4.WS_LES_GRS_PAY_YTD |
| LES_EMP_DETAIL_RECTYPE_4_TBL | TAXABLE_WAGE_AMT | exp_Final.TAXABLE_WAGE_AMT → jnr_LES_NUMBER.WS_LES_TAX_WGE_AMT → fil_EMP_REC_TYPE_4.WS_LES_TAX_WGE_AMT → exp_Convert.WS_LES_TAX_WGE_AMT → fil_EMP_REC_TYPE_4_EMP_DETAIL.WS_LES_TAX_WGE_AMT → Norm_EMP_REC_TYPE_4.WS_LES_TAX_WGE_AMT → EMP_REC_TYPE_4.WS_LES_TAX_WGE_AMT | EMP_REC_TYPE_4.WS_LES_TAX_WGE_AMT |
| LES_EMP_DETAIL_RECTYPE_4_TBL | TAXABLE_WAGE_AMT_YTD | exp_Final.TAXABLE_WAGE_AMT_YTD → jnr_LES_NUMBER.WS_LES_TAX_WGE_YTD → fil_EMP_REC_TYPE_4.WS_LES_TAX_WGE_YTD → exp_Convert.WS_LES_TAX_WGE_YTD → fil_EMP_REC_TYPE_4_EMP_DETAIL.WS_LES_TAX_WGE_YTD → Norm_EMP_REC_TYPE_4.WS_LES_TAX_WGE_YTD → EMP_REC_TYPE_4.WS_LES_TAX_WGE_YTD | EMP_REC_TYPE_4.WS_LES_TAX_WGE_YTD |
| LES_EMP_DETAIL_RECTYPE_4_TBL | NONTAXABLE_WAGE_AMT | exp_Final.NONTAXABLE_WAGE_AMT → jnr_LES_NUMBER.WS_LES_NTAX_WGE_AMT → fil_EMP_REC_TYPE_4.WS_LES_NTAX_WGE_AMT → exp_Convert.WS_LES_NTAX_WGE_AMT → fil_EMP_REC_TYPE_4_EMP_DETAIL.WS_LES_NTAX_WGE_AMT → Norm_EMP_REC_TYPE_4.WS_LES_NTAX_WGE_AMT → EMP_REC_TYPE_4.WS_LES_NTAX_WGE_AMT | EMP_REC_TYPE_4.WS_LES_NTAX_WGE_AMT |
| LES_EMP_DETAIL_RECTYPE_4_TBL | NONTAXABLE_WAGE_AMT_YTD | exp_Final.NONTAXABLE_WAGE_AMT_YTD → jnr_LES_NUMBER.WS_LES_NTAX_WGE_YTD → fil_EMP_REC_TYPE_4.WS_LES_NTAX_WGE_YTD → exp_Convert.WS_LES_NTAX_WGE_YTD → fil_EMP_REC_TYPE_4_EMP_DETAIL.WS_LES_NTAX_WGE_YTD → Norm_EMP_REC_TYPE_4.WS_LES_NTAX_WGE_YTD → EMP_REC_TYPE_4.WS_LES_NTAX_WGE_YTD | EMP_REC_TYPE_4.WS_LES_NTAX_WGE_YTD |
| LES_EMP_DETAIL_RECTYPE_4_TBL | TAX_DEFERRED_AMT | exp_Final.TAX_DEFERRED_AMT → jnr_LES_NUMBER.WS_LES_DEF_TAX_AMT → fil_EMP_REC_TYPE_4.WS_LES_DEF_TAX_AMT → exp_Convert.WS_LES_DEF_TAX_AMT → fil_EMP_REC_TYPE_4_EMP_DETAIL.WS_LES_DEF_TAX_AMT → Norm_EMP_REC_TYPE_4.WS_LES_DEF_TAX_AMT → EMP_REC_TYPE_4.WS_LES_DEF_TAX_AMT | EMP_REC_TYPE_4.WS_LES_DEF_TAX_AMT |
| LES_EMP_DETAIL_RECTYPE_4_TBL | TAX_DEFERRED_AMT_YTD | exp_Final.TAX_DEFERRED_AMT_YTD → jnr_LES_NUMBER.WS_LES_DEF_TAX_YTD → fil_EMP_REC_TYPE_4.WS_LES_DEF_TAX_YTD → exp_Convert.WS_LES_DEF_TAX_YTD → fil_EMP_REC_TYPE_4_EMP_DETAIL.WS_LES_DEF_TAX_YTD → Norm_EMP_REC_TYPE_4.WS_LES_DEF_TAX_YTD → EMP_REC_TYPE_4.WS_LES_DEF_TAX_YTD | EMP_REC_TYPE_4.WS_LES_DEF_TAX_YTD |
| LES_EMP_DETAIL_RECTYPE_4_TBL | DEDUCTION_AMT | exp_Final.DEDUCTION_AMT → jnr_LES_NUMBER.WS_LES_DED_TAX_AMT → fil_EMP_REC_TYPE_4.WS_LES_DED_TAX_AMT → exp_Convert.WS_LES_DED_TAX_AMT → fil_EMP_REC_TYPE_4_EMP_DETAIL.WS_LES_DED_TAX_AMT → Norm_EMP_REC_TYPE_4.WS_LES_DED_TAX_AMT → EMP_REC_TYPE_4.WS_LES_DED_TAX_AMT | EMP_REC_TYPE_4.WS_LES_DED_TAX_AMT |
| LES_EMP_DETAIL_RECTYPE_4_TBL | DEDUCTION_AMT_YTD | exp_Final.DEDUCTION_AMT_YTD → jnr_LES_NUMBER.WS_LES_DED_TAX_YTD → fil_EMP_REC_TYPE_4.WS_LES_DED_TAX_YTD → exp_Convert.WS_LES_DED_TAX_YTD → fil_EMP_REC_TYPE_4_EMP_DETAIL.WS_LES_DED_TAX_YTD → Norm_EMP_REC_TYPE_4.WS_LES_DED_TAX_YTD → EMP_REC_TYPE_4.WS_LES_DED_TAX_YTD | EMP_REC_TYPE_4.WS_LES_DED_TAX_YTD |

## Mapping `m_LES_Load_LES_EMP_DETAIL_RECTYPE_5_TBL`

- Sessions: `s_LES_Load_LES_EMP_DETAIL_RECTYPE_5_TBL` (#10)
- Sources: `EMP_REC_TYPE_5`, `LES_EMP_DETAIL_TBL`
- Target instances: `LES_EMP_DETAIL_RECTYPE_5_TBL`

### Transformation `Norm_EMP_REC_TYPE_5` (Normalizer)

- **Reset**: `NO`
- **Restart**: `NO`

### Transformation `SQ_LES_EMP_DETAIL_TBL` (Source Qualifier)

- **Source Filter**: `LES_EMP_DETAIL_TBL.PP_END_YEAR = $$MAP_PP_END_YEAR AND LES_EMP_DETAIL_TBL.PP_NUM = $$MAP_PP_NUM`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `fil_EMP_REC_TYPE_5` (Filter)

- **Filter Condition**: `WS_LES_REC_TYPE5 = '*5'`

### Transformation `fil_EMP_REC_TYPE_5_EMP_DETAIL` (Filter)

- **Filter Condition**: `WS_LES_REC_TYPE5 = '*5' OR WS_LES_REC_TYPE5 = '*E'`

### Transformation `jnr_LES_NUMBER` (Joiner)

- **Join Condition**: `LES_NUMBER = EMP5_LES_NUMBER`
- **Join Type**: `Normal Join`
- **Null ordering in master**: `Null Is Highest Value`
- **Null ordering in detail**: `Null Is Highest Value`
- **Sorted Input**: `NO`

- Joiner `jnr_LES_NUMBER`: Normal Join ON `LES_NUMBER = EMP5_LES_NUMBER`
- Normalizer `Norm_EMP_REC_TYPE_5` (vsam=True, source EMP_REC_TYPE_5) occurs: —; generated: GK_EMP_REC_TYPE_5

### Target instance `LES_EMP_DETAIL_RECTYPE_5_TBL` (table `LES_EMP_DETAIL_RECTYPE_5_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LES_EMP_DETAIL_RECTYPE_5_TBL | PP_END_YEAR | exp_Final.PP_END_YEAR → jnr_LES_NUMBER.PP_END_YEAR → SQ_LES_EMP_DETAIL_TBL.PP_END_YEAR → LES_EMP_DETAIL_TBL.PP_END_YEAR | LES_EMP_DETAIL_TBL.PP_END_YEAR |
| LES_EMP_DETAIL_RECTYPE_5_TBL | PP_NUM | exp_Final.PP_NUM → jnr_LES_NUMBER.PP_NUM → SQ_LES_EMP_DETAIL_TBL.PP_NUM → LES_EMP_DETAIL_TBL.PP_NUM | LES_EMP_DETAIL_TBL.PP_NUM |
| LES_EMP_DETAIL_RECTYPE_5_TBL | LES_NUMBER | exp_Final.LES_NUMBER → jnr_LES_NUMBER.EMP5_LES_NUMBER → fil_EMP_REC_TYPE_5.EMP5_LES_NUMBER → exp_Convert.o_EMP5_LES_NUMBER = IIF(IS_NUMBER(v_LES_NUMBER), TO_INTEGER(v_LES_NUMBER) ) → exp_Convert.v_LES_NUMBER = IIF(WS_LES_REC_TYPE5 = '*E', SUBSTR(WS_LES_AEI_AMT_YTD_RDF, 2, 7) , v_LES_NUMBER) → fil_EMP_REC_TYPE_5_EMP_DETAIL.WS_LES_REC_TYPE5 → Norm_EMP_REC_TYPE_5.WS_LES_REC_TYPE5 → EMP_REC_TYPE_5.WS_LES_REC_TYPE5 → fil_EMP_REC_TYPE_5_EMP_DETAIL.WS_LES_AEI_AMT_YTD_RDF → Norm_EMP_REC_TYPE_5.WS_LES_AEI_AMT_YTD_RDF → EMP_REC_TYPE_5.WS_LES_AEI_AMT_YTD_RDF | EMP_REC_TYPE_5.WS_LES_AEI_AMT_YTD_RDF; EMP_REC_TYPE_5.WS_LES_REC_TYPE5 |
| LES_EMP_DETAIL_RECTYPE_5_TBL | PSEUDOSSN | exp_Final.PSEUDOSSN → jnr_LES_NUMBER.PSEUDOSSN → SQ_LES_EMP_DETAIL_TBL.PSEUDOSSN → LES_EMP_DETAIL_TBL.PSEUDOSSN | LES_EMP_DETAIL_TBL.PSEUDOSSN |
| LES_EMP_DETAIL_RECTYPE_5_TBL | ADV_ERND_INCOME_CREDIT_AMT | exp_Final.ADV_ERND_INCOME_CREDIT_AMT → jnr_LES_NUMBER.WS_LES_AEI_AMT → fil_EMP_REC_TYPE_5.WS_LES_AEI_AMT → exp_Convert.WS_LES_AEI_AMT → fil_EMP_REC_TYPE_5_EMP_DETAIL.WS_LES_AEI_AMT → Norm_EMP_REC_TYPE_5.WS_LES_AEI_AMT → EMP_REC_TYPE_5.WS_LES_AEI_AMT | EMP_REC_TYPE_5.WS_LES_AEI_AMT |
| LES_EMP_DETAIL_RECTYPE_5_TBL | ADV_ERND_INCOME_CREDIT_AMT_YTD | exp_Final.ADV_ERND_INCOME_CREDIT_AMT_YTD → jnr_LES_NUMBER.WS_LES_AEI_AMT_YTD → fil_EMP_REC_TYPE_5.WS_LES_AEI_AMT_YTD → exp_Convert.WS_LES_AEI_AMT_YTD → fil_EMP_REC_TYPE_5_EMP_DETAIL.WS_LES_AEI_AMT_YTD → Norm_EMP_REC_TYPE_5.WS_LES_AEI_AMT_YTD → EMP_REC_TYPE_5.WS_LES_AEI_AMT_YTD | EMP_REC_TYPE_5.WS_LES_AEI_AMT_YTD |
| LES_EMP_DETAIL_RECTYPE_5_TBL | NET_PAY_AMT | exp_Final.NET_PAY_AMT → jnr_LES_NUMBER.WS_LES_NET_PAY_AMT → fil_EMP_REC_TYPE_5.WS_LES_NET_PAY_AMT → exp_Convert.WS_LES_NET_PAY_AMT → fil_EMP_REC_TYPE_5_EMP_DETAIL.WS_LES_NET_PAY_AMT → Norm_EMP_REC_TYPE_5.WS_LES_NET_PAY_AMT → EMP_REC_TYPE_5.WS_LES_NET_PAY_AMT | EMP_REC_TYPE_5.WS_LES_NET_PAY_AMT |
| LES_EMP_DETAIL_RECTYPE_5_TBL | NET_PAY_AMT_YTD | exp_Final.NET_PAY_AMT_YTD → jnr_LES_NUMBER.WS_LES_NET_PAY_YTD → fil_EMP_REC_TYPE_5.WS_LES_NET_PAY_YTD → exp_Convert.WS_LES_NET_PAY_YTD → fil_EMP_REC_TYPE_5_EMP_DETAIL.WS_LES_NET_PAY_YTD → Norm_EMP_REC_TYPE_5.WS_LES_NET_PAY_YTD → EMP_REC_TYPE_5.WS_LES_NET_PAY_YTD | EMP_REC_TYPE_5.WS_LES_NET_PAY_YTD |
| LES_EMP_DETAIL_RECTYPE_5_TBL | TSP_SAVINGS | exp_Final.TSP_SAVINGS → jnr_LES_NUMBER.WS_LES_XVX7_TITLE → fil_EMP_REC_TYPE_5.WS_LES_XVX7_TITLE → exp_Convert.WS_LES_XVX7_TITLE → fil_EMP_REC_TYPE_5_EMP_DETAIL.WS_LES_XVX7_TITLE → Norm_EMP_REC_TYPE_5.WS_LES_XVX7_TITLE → EMP_REC_TYPE_5.WS_LES_XVX7_TITLE | EMP_REC_TYPE_5.WS_LES_XVX7_TITLE |
| LES_EMP_DETAIL_RECTYPE_5_TBL | TSP_SAVINGS_PCT | exp_Final.TSP_SAVINGS_PCT → jnr_LES_NUMBER.WS_LES_XVX7_PCT → fil_EMP_REC_TYPE_5.WS_LES_XVX7_PCT → exp_Convert.WS_LES_XVX7_PCT → fil_EMP_REC_TYPE_5_EMP_DETAIL.WS_LES_XVX7_PCT → Norm_EMP_REC_TYPE_5.WS_LES_XVX7_PCT → EMP_REC_TYPE_5.WS_LES_XVX7_PCT | EMP_REC_TYPE_5.WS_LES_XVX7_PCT |
| LES_EMP_DETAIL_RECTYPE_5_TBL | TITLEG_FUND | exp_Final.TITLEG_FUND → jnr_LES_NUMBER.WS_LES_GA_TIT → fil_EMP_REC_TYPE_5.WS_LES_GA_TIT → exp_Convert.WS_LES_GA_TIT → fil_EMP_REC_TYPE_5_EMP_DETAIL.WS_LES_GA_TIT → Norm_EMP_REC_TYPE_5.WS_LES_GA_TIT → EMP_REC_TYPE_5.WS_LES_GA_TIT | EMP_REC_TYPE_5.WS_LES_GA_TIT |
| LES_EMP_DETAIL_RECTYPE_5_TBL | TITLEG_FUND_PCT | exp_Final.TITLEG_FUND_PCT → jnr_LES_NUMBER.WS_LES_GA_PCT → fil_EMP_REC_TYPE_5.WS_LES_GA_PCT → exp_Convert.WS_LES_GA_PCT → fil_EMP_REC_TYPE_5_EMP_DETAIL.WS_LES_GA_PCT → Norm_EMP_REC_TYPE_5.WS_LES_GA_PCT → EMP_REC_TYPE_5.WS_LES_GA_PCT | EMP_REC_TYPE_5.WS_LES_GA_PCT |
| LES_EMP_DETAIL_RECTYPE_5_TBL | TITLEF_FUND | exp_Final.TITLEF_FUND → jnr_LES_NUMBER.WS_LES_FB_TIT → fil_EMP_REC_TYPE_5.WS_LES_FB_TIT → exp_Convert.WS_LES_FB_TIT → fil_EMP_REC_TYPE_5_EMP_DETAIL.WS_LES_FB_TIT → Norm_EMP_REC_TYPE_5.WS_LES_FB_TIT → EMP_REC_TYPE_5.WS_LES_FB_TIT | EMP_REC_TYPE_5.WS_LES_FB_TIT |
| LES_EMP_DETAIL_RECTYPE_5_TBL | TITLEF_FUND_PCT | exp_Final.TITLEF_FUND_PCT → jnr_LES_NUMBER.WS_LES_FB_PCT → fil_EMP_REC_TYPE_5.WS_LES_FB_PCT → exp_Convert.WS_LES_FB_PCT → fil_EMP_REC_TYPE_5_EMP_DETAIL.WS_LES_FB_PCT → Norm_EMP_REC_TYPE_5.WS_LES_FB_PCT → EMP_REC_TYPE_5.WS_LES_FB_PCT | EMP_REC_TYPE_5.WS_LES_FB_PCT |
| LES_EMP_DETAIL_RECTYPE_5_TBL | TITLEC_FUND | exp_Final.TITLEC_FUND → jnr_LES_NUMBER.WS_LES_CC_TIT → fil_EMP_REC_TYPE_5.WS_LES_CC_TIT → exp_Convert.WS_LES_CC_TIT → fil_EMP_REC_TYPE_5_EMP_DETAIL.WS_LES_CC_TIT → Norm_EMP_REC_TYPE_5.WS_LES_CC_TIT → EMP_REC_TYPE_5.WS_LES_CC_TIT | EMP_REC_TYPE_5.WS_LES_CC_TIT |
| LES_EMP_DETAIL_RECTYPE_5_TBL | TITLEC_FUND_PCT | exp_Final.TITLEC_FUND_PCT → jnr_LES_NUMBER.WS_LES_CC_PCT → fil_EMP_REC_TYPE_5.WS_LES_CC_PCT → exp_Convert.WS_LES_CC_PCT → fil_EMP_REC_TYPE_5_EMP_DETAIL.WS_LES_CC_PCT → Norm_EMP_REC_TYPE_5.WS_LES_CC_PCT → EMP_REC_TYPE_5.WS_LES_CC_PCT | EMP_REC_TYPE_5.WS_LES_CC_PCT |
| LES_EMP_DETAIL_RECTYPE_5_TBL | ROTH_SAVINGS | exp_Final.ROTH_SAVINGS → jnr_LES_NUMBER.WS_LES_ROTH_SV → fil_EMP_REC_TYPE_5.WS_LES_ROTH_SV → exp_Convert.WS_LES_ROTH_SV → fil_EMP_REC_TYPE_5_EMP_DETAIL.WS_LES_ROTH_SV → Norm_EMP_REC_TYPE_5.WS_LES_ROTH_SV → EMP_REC_TYPE_5.WS_LES_ROTH_SV | EMP_REC_TYPE_5.WS_LES_ROTH_SV |
| LES_EMP_DETAIL_RECTYPE_5_TBL | ROTH_SAVINGS_PCT | exp_Final.ROTH_SAVINGS_PCT → jnr_LES_NUMBER.WS_LES_ROTH_SV_PCT → fil_EMP_REC_TYPE_5.WS_LES_ROTH_SV_PCT → exp_Convert.WS_LES_ROTH_SV_PCT → fil_EMP_REC_TYPE_5_EMP_DETAIL.WS_LES_ROTH_SV_PCT → Norm_EMP_REC_TYPE_5.WS_LES_ROTH_SV_PCT → EMP_REC_TYPE_5.WS_LES_ROTH_SV_PCT | EMP_REC_TYPE_5.WS_LES_ROTH_SV_PCT |

## Mapping `m_LES_Load_LES_EMP_DETAIL_RECTYPE_6_TBL`

- Sessions: `s_LES_Load_LES_EMP_DETAIL_RECTYPE_6_TBL` (#11)
- Sources: `EMP_REC_TYPE_6`, `LES_EMP_DETAIL_TBL`
- Target instances: `LES_EMP_DETAIL_RECTYPE_6_TBL`

### Transformation `Norm_EMP_REC_TYPE_6` (Normalizer)

- **Reset**: `NO`
- **Restart**: `NO`

### Transformation `SQ_LES_EMP_DETAIL_TBL` (Source Qualifier)

- **Source Filter**: `LES_EMP_DETAIL_TBL.PP_END_YEAR = $$MAP_PP_END_YEAR AND LES_EMP_DETAIL_TBL.PP_NUM = $$MAP_PP_NUM`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `fil_EMP_REC_TYPE_6` (Filter)

- **Filter Condition**: `WS_LES_REC_TYPE6 = '*6'`

### Transformation `fil_EMP_REC_TYPE_6_EMP_DETAIL` (Filter)

- **Filter Condition**: `WS_LES_REC_TYPE6 = '*6' OR WS_LES_REC_TYPE6 = '*E'`

### Transformation `jnr_LES_NUMBER` (Joiner)

- **Join Condition**: `LES_NUMBER = EMP6_LES_NUMBER`
- **Join Type**: `Normal Join`
- **Null ordering in master**: `Null Is Highest Value`
- **Null ordering in detail**: `Null Is Highest Value`
- **Sorted Input**: `NO`

- Joiner `jnr_LES_NUMBER`: Normal Join ON `LES_NUMBER = EMP6_LES_NUMBER`
- Normalizer `Norm_EMP_REC_TYPE_6` (vsam=True, source EMP_REC_TYPE_6) occurs: —; generated: —

### Target instance `LES_EMP_DETAIL_RECTYPE_6_TBL` (table `LES_EMP_DETAIL_RECTYPE_6_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LES_EMP_DETAIL_RECTYPE_6_TBL | PP_END_YEAR | exp_Final.PP_END_YEAR → jnr_LES_NUMBER.PP_END_YEAR → SQ_LES_EMP_DETAIL_TBL.PP_END_YEAR → LES_EMP_DETAIL_TBL.PP_END_YEAR | LES_EMP_DETAIL_TBL.PP_END_YEAR |
| LES_EMP_DETAIL_RECTYPE_6_TBL | PP_NUM | exp_Final.PP_NUM → jnr_LES_NUMBER.PP_NUM → SQ_LES_EMP_DETAIL_TBL.PP_NUM → LES_EMP_DETAIL_TBL.PP_NUM | LES_EMP_DETAIL_TBL.PP_NUM |
| LES_EMP_DETAIL_RECTYPE_6_TBL | LES_NUMBER | exp_Final.LES_NUMBER → jnr_LES_NUMBER.EMP6_LES_NUMBER → fil_EMP_REC_TYPE_6.EMP6_LES_NUMBER → exp_Convert.o_EMP6_LES_NUMBER = IIF(IS_NUMBER(v_LES_NUMBER), TO_INTEGER(v_LES_NUMBER) ) → exp_Convert.v_LES_NUMBER = IIF(WS_LES_REC_TYPE6 = '*E', SUBSTR(WS_LES_VHVM_TITLE, 10, 7) , v_LES_NUMBER) → fil_EMP_REC_TYPE_6_EMP_DETAIL.WS_LES_REC_TYPE6 → Norm_EMP_REC_TYPE_6.WS_LES_REC_TYPE6 → EMP_REC_TYPE_6.WS_LES_REC_TYPE6 → fil_EMP_REC_TYPE_6_EMP_DETAIL.WS_LES_VHVM_TITLE → Norm_EMP_REC_TYPE_6.WS_LES_VHVM_TITLE → EMP_REC_TYPE_6.WS_LES_VHVM_TITLE | EMP_REC_TYPE_6.WS_LES_REC_TYPE6; EMP_REC_TYPE_6.WS_LES_VHVM_TITLE |
| LES_EMP_DETAIL_RECTYPE_6_TBL | PSEUDOSSN | exp_Final.PSEUDOSSN → jnr_LES_NUMBER.PSEUDOSSN → SQ_LES_EMP_DETAIL_TBL.PSEUDOSSN → LES_EMP_DETAIL_TBL.PSEUDOSSN | LES_EMP_DETAIL_TBL.PSEUDOSSN |
| LES_EMP_DETAIL_RECTYPE_6_TBL | EARNINGS_FOR_CURR_TSP | exp_Final.EARNINGS_FOR_CURR_TSP → jnr_LES_NUMBER.WS_LES_VHVM_TITLE → fil_EMP_REC_TYPE_6.WS_LES_VHVM_TITLE → exp_Convert.WS_LES_VHVM_TITLE → fil_EMP_REC_TYPE_6_EMP_DETAIL.WS_LES_VHVM_TITLE → Norm_EMP_REC_TYPE_6.WS_LES_VHVM_TITLE → EMP_REC_TYPE_6.WS_LES_VHVM_TITLE | EMP_REC_TYPE_6.WS_LES_VHVM_TITLE |
| LES_EMP_DETAIL_RECTYPE_6_TBL | EARNINGS_FOR_CURR_TSP_AMT | exp_Final.EARNINGS_FOR_CURR_TSP_AMT → jnr_LES_NUMBER.WS_LES_VHVM_AMT → fil_EMP_REC_TYPE_6.WS_LES_VHVM_AMT → exp_Convert.WS_LES_VHVM_AMT → fil_EMP_REC_TYPE_6_EMP_DETAIL.WS_LES_VHVM_AMT → Norm_EMP_REC_TYPE_6.WS_LES_VHVM_AMT → EMP_REC_TYPE_6.WS_LES_VHVM_AMT | EMP_REC_TYPE_6.WS_LES_VHVM_AMT |
| LES_EMP_DETAIL_RECTYPE_6_TBL | EARNINGS_FOR_YTD_TSP | exp_Final.EARNINGS_FOR_YTD_TSP → jnr_LES_NUMBER.WS_LES_VHVM_TITLE_YTD → fil_EMP_REC_TYPE_6.WS_LES_VHVM_TITLE_YTD → exp_Convert.WS_LES_VHVM_TITLE_YTD → fil_EMP_REC_TYPE_6_EMP_DETAIL.WS_LES_VHVM_TITLE_YTD → Norm_EMP_REC_TYPE_6.WS_LES_VHVM_TITLE_YTD → EMP_REC_TYPE_6.WS_LES_VHVM_TITLE_YTD | EMP_REC_TYPE_6.WS_LES_VHVM_TITLE_YTD |
| LES_EMP_DETAIL_RECTYPE_6_TBL | EARNINGS_FOR_YTD_TSP_AMT | exp_Final.EARNINGS_FOR_YTD_TSP_AMT → jnr_LES_NUMBER.WS_LES_VHVM_AMT_YTD → fil_EMP_REC_TYPE_6.WS_LES_VHVM_AMT_YTD → exp_Convert.WS_LES_VHVM_AMT_YTD → fil_EMP_REC_TYPE_6_EMP_DETAIL.WS_LES_VHVM_AMT_YTD → Norm_EMP_REC_TYPE_6.WS_LES_VHVM_AMT_YTD → EMP_REC_TYPE_6.WS_LES_VHVM_AMT_YTD | EMP_REC_TYPE_6.WS_LES_VHVM_AMT_YTD |

## Mapping `m_LES_Load_LES_EMP_DETAIL_RECTYPE_C_TBL`

- Sessions: `s_LES_Load_LES_EMP_DETAIL_RECTYPE_C_TBL` (#12)
- Sources: `EMP_REC_TYPE_C`, `LES_EMP_DETAIL_TBL`
- Target instances: `LES_EMP_DETAIL_RECTYPE_C_TBL`

### Transformation `Norm_EMP_REC_TYPE_C` (Normalizer)

- **Reset**: `NO`
- **Restart**: `NO`

### Transformation `SQ_LES_EMP_DETAIL_TBL` (Source Qualifier)

- **Source Filter**: `LES_EMP_DETAIL_TBL.PP_END_YEAR = $$MAP_PP_END_YEAR AND LES_EMP_DETAIL_TBL.PP_NUM = $$MAP_PP_NUM`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `fil_EMP_REC_TYPE_C` (Filter)

- **Filter Condition**: `WS_CURR_REC_TYPE = '*C'`

### Transformation `fil_EMP_REC_TYPE_C_EMP_DETAIL` (Filter)

- **Filter Condition**: `WS_CURR_REC_TYPE = '*C' OR WS_CURR_REC_TYPE = '*E'`

### Transformation `jnr_LES_NUMBER` (Joiner)

- **Join Condition**: `LES_NUMBER = EMPC_LES_NUMBER`
- **Join Type**: `Normal Join`
- **Null ordering in master**: `Null Is Highest Value`
- **Null ordering in detail**: `Null Is Highest Value`
- **Sorted Input**: `NO`

- Joiner `jnr_LES_NUMBER`: Normal Join ON `LES_NUMBER = EMPC_LES_NUMBER`
- Normalizer `Norm_EMP_REC_TYPE_C` (vsam=True, source EMP_REC_TYPE_C) occurs: —; generated: GK_EMP_REC_TYPE_C

### Target instance `LES_EMP_DETAIL_RECTYPE_C_TBL` (table `LES_EMP_DETAIL_RECTYPE_C_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LES_EMP_DETAIL_RECTYPE_C_TBL | PP_END_YEAR | exp_Final.PP_END_YEAR → jnr_LES_NUMBER.PP_END_YEAR → SQ_LES_EMP_DETAIL_TBL.PP_END_YEAR → LES_EMP_DETAIL_TBL.PP_END_YEAR | LES_EMP_DETAIL_TBL.PP_END_YEAR |
| LES_EMP_DETAIL_RECTYPE_C_TBL | PP_NUM | exp_Final.PP_NUM → jnr_LES_NUMBER.PP_NUM → SQ_LES_EMP_DETAIL_TBL.PP_NUM → LES_EMP_DETAIL_TBL.PP_NUM | LES_EMP_DETAIL_TBL.PP_NUM |
| LES_EMP_DETAIL_RECTYPE_C_TBL | LES_NUMBER | exp_Final.LES_NUMBER → jnr_LES_NUMBER.EMPC_LES_NUMBER → fil_EMP_REC_TYPE_C.EMPC_LES_NUMBER → exp_Convert.o_EMPC_LES_NUMBER = IIF(IS_NUMBER(v_LES_NUMBER), TO_INTEGER(v_LES_NUMBER) ) → exp_Convert.v_LES_NUMBER = IIF(WS_CURR_REC_TYPE = '*E', SUBSTR(WS_CURR_ERN_NAME1, 10, 3) \|\| SUBSTR(WS_CURR_HRS_DAYS1_RDF, 1, 4), v_LES_NUMBER) → fil_EMP_REC_TYPE_C_EMP_DETAIL.WS_CURR_REC_TYPE → Norm_EMP_REC_TYPE_C.WS_CURR_REC_TYPE → EMP_REC_TYPE_C.WS_CURR_REC_TYPE → fil_EMP_REC_TYPE_C_EMP_DETAIL.WS_CURR_ERN_NAME1 → Norm_EMP_REC_TYPE_C.WS_CURR_ERN_NAME1 → EMP_REC_TYPE_C.WS_CURR_ERN_NAME1 → fil_EMP_REC_TYPE_C_EMP_DETAIL.WS_CURR_HRS_DAYS1_RDF → Norm_EMP_REC_TYPE_C.WS_CURR_HRS_DAYS1_RDF → EMP_REC_TYPE_C.WS_CURR_HRS_DAYS1_RDF | EMP_REC_TYPE_C.WS_CURR_ERN_NAME1; EMP_REC_TYPE_C.WS_CURR_HRS_DAYS1_RDF; EMP_REC_TYPE_C.WS_CURR_REC_TYPE |
| LES_EMP_DETAIL_RECTYPE_C_TBL | PSEUDOSSN | exp_Final.PSEUDOSSN → jnr_LES_NUMBER.PSEUDOSSN → SQ_LES_EMP_DETAIL_TBL.PSEUDOSSN → LES_EMP_DETAIL_TBL.PSEUDOSSN | LES_EMP_DETAIL_TBL.PSEUDOSSN |
| LES_EMP_DETAIL_RECTYPE_C_TBL | CURR_EARN_ID | exp_Final.CURR_EARN_ID → jnr_LES_NUMBER.CURR_EARN_ID → fil_EMP_REC_TYPE_C.CURR_EARN_ID → exp_Convert.o_CURR_EARN_ID = v_CURR_EARN_ID → exp_Convert.v_CURR_EARN_ID = IIF(WS_CURR_REC_TYPE = '*E', 0, v_CURR_EARN_ID + 1) → fil_EMP_REC_TYPE_C_EMP_DETAIL.WS_CURR_REC_TYPE → Norm_EMP_REC_TYPE_C.WS_CURR_REC_TYPE → EMP_REC_TYPE_C.WS_CURR_REC_TYPE | EMP_REC_TYPE_C.WS_CURR_REC_TYPE |
| LES_EMP_DETAIL_RECTYPE_C_TBL | CURR_EARN_NAME1 | exp_Final.CURR_EARN_NAME1 → jnr_LES_NUMBER.WS_CURR_ERN_NAME1 → fil_EMP_REC_TYPE_C.WS_CURR_ERN_NAME1 → exp_Convert.o_WS_CURR_ERN_NAME1 = LTRIM(RTRIM(WS_CURR_ERN_NAME1)) → fil_EMP_REC_TYPE_C_EMP_DETAIL.WS_CURR_ERN_NAME1 → Norm_EMP_REC_TYPE_C.WS_CURR_ERN_NAME1 → EMP_REC_TYPE_C.WS_CURR_ERN_NAME1 | EMP_REC_TYPE_C.WS_CURR_ERN_NAME1 |
| LES_EMP_DETAIL_RECTYPE_C_TBL | CURR_EARN_NAME1_HOURS | exp_Final.CURR_EARN_NAME1_HOURS → jnr_LES_NUMBER.WS_CURR_HRS_DAYS1 → fil_EMP_REC_TYPE_C.WS_CURR_HRS_DAYS1 → exp_Convert.WS_CURR_HRS_DAYS1 → fil_EMP_REC_TYPE_C_EMP_DETAIL.WS_CURR_HRS_DAYS1 → Norm_EMP_REC_TYPE_C.WS_CURR_HRS_DAYS1 → EMP_REC_TYPE_C.WS_CURR_HRS_DAYS1 | EMP_REC_TYPE_C.WS_CURR_HRS_DAYS1 |
| LES_EMP_DETAIL_RECTYPE_C_TBL | CURR_EARN_NAME1_AMT | exp_Final.CURR_EARN_NAME1_AMT → jnr_LES_NUMBER.WS_CURR_AMT1 → fil_EMP_REC_TYPE_C.WS_CURR_AMT1 → exp_Convert.WS_CURR_AMT1 → fil_EMP_REC_TYPE_C_EMP_DETAIL.WS_CURR_AMT1 → Norm_EMP_REC_TYPE_C.WS_CURR_AMT1 → EMP_REC_TYPE_C.WS_CURR_AMT1 | EMP_REC_TYPE_C.WS_CURR_AMT1 |
| LES_EMP_DETAIL_RECTYPE_C_TBL | CURR_EARN_NAME2 | exp_Final.CURR_EARN_NAME2 → jnr_LES_NUMBER.WS_CURR_ERN_NAME2 → fil_EMP_REC_TYPE_C.WS_CURR_ERN_NAME2 → exp_Convert.o_WS_CURR_ERN_NAME2 = LTRIM(RTRIM(WS_CURR_ERN_NAME2)) → fil_EMP_REC_TYPE_C_EMP_DETAIL.WS_CURR_ERN_NAME2 → Norm_EMP_REC_TYPE_C.WS_CURR_ERN_NAME2 → EMP_REC_TYPE_C.WS_CURR_ERN_NAME2 | EMP_REC_TYPE_C.WS_CURR_ERN_NAME2 |
| LES_EMP_DETAIL_RECTYPE_C_TBL | CURR_EARN_NAME2_HOURS | exp_Final.CURR_EARN_NAME2_HOURS → jnr_LES_NUMBER.WS_CURR_HRS_DAYS2 → fil_EMP_REC_TYPE_C.WS_CURR_HRS_DAYS2 → exp_Convert.WS_CURR_HRS_DAYS2 → fil_EMP_REC_TYPE_C_EMP_DETAIL.WS_CURR_HRS_DAYS2 → Norm_EMP_REC_TYPE_C.WS_CURR_HRS_DAYS2 → EMP_REC_TYPE_C.WS_CURR_HRS_DAYS2 | EMP_REC_TYPE_C.WS_CURR_HRS_DAYS2 |
| LES_EMP_DETAIL_RECTYPE_C_TBL | CURR_EARN_NAME2_AMT | exp_Final.CURR_EARN_NAME2_AMT → jnr_LES_NUMBER.WS_CURR_AMT2 → fil_EMP_REC_TYPE_C.WS_CURR_AMT2 → exp_Convert.WS_CURR_AMT2 → fil_EMP_REC_TYPE_C_EMP_DETAIL.WS_CURR_AMT2 → Norm_EMP_REC_TYPE_C.WS_CURR_AMT2 → EMP_REC_TYPE_C.WS_CURR_AMT2 | EMP_REC_TYPE_C.WS_CURR_AMT2 |
| LES_EMP_DETAIL_RECTYPE_C_TBL | CURR_EARN_NAME3 | exp_Final.CURR_EARN_NAME3 → jnr_LES_NUMBER.WS_CURR_ERN_NAME3 → fil_EMP_REC_TYPE_C.WS_CURR_ERN_NAME3 → exp_Convert.o_WS_CURR_ERN_NAME3 = LTRIM(RTRIM(WS_CURR_ERN_NAME3)) → fil_EMP_REC_TYPE_C_EMP_DETAIL.WS_CURR_ERN_NAME3 → Norm_EMP_REC_TYPE_C.WS_CURR_ERN_NAME3 → EMP_REC_TYPE_C.WS_CURR_ERN_NAME3 | EMP_REC_TYPE_C.WS_CURR_ERN_NAME3 |
| LES_EMP_DETAIL_RECTYPE_C_TBL | CURR_EARN_NAME3_HOURS | exp_Final.CURR_EARN_NAME3_HOURS → jnr_LES_NUMBER.WS_CURR_HRS_DAYS3 → fil_EMP_REC_TYPE_C.WS_CURR_HRS_DAYS3 → exp_Convert.WS_CURR_HRS_DAYS3 → fil_EMP_REC_TYPE_C_EMP_DETAIL.WS_CURR_HRS_DAYS3 → Norm_EMP_REC_TYPE_C.WS_CURR_HRS_DAYS3 → EMP_REC_TYPE_C.WS_CURR_HRS_DAYS3 | EMP_REC_TYPE_C.WS_CURR_HRS_DAYS3 |
| LES_EMP_DETAIL_RECTYPE_C_TBL | CURR_EARN_NAME3_AMT | exp_Final.CURR_EARN_NAME3_AMT → jnr_LES_NUMBER.WS_CURR_AMT3 → fil_EMP_REC_TYPE_C.WS_CURR_AMT3 → exp_Convert.WS_CURR_AMT3 → fil_EMP_REC_TYPE_C_EMP_DETAIL.WS_CURR_AMT3 → Norm_EMP_REC_TYPE_C.WS_CURR_AMT3 → EMP_REC_TYPE_C.WS_CURR_AMT3 | EMP_REC_TYPE_C.WS_CURR_AMT3 |

## Mapping `m_LES_Load_LES_EMP_DETAIL_RECTYPE_R_TBL`

- Sessions: `s_LES_Load_LES_EMP_DETAIL_RECTYPE_R_TBL` (#13)
- Sources: `EMP_REC_TYPE_R`, `LES_EMP_DETAIL_TBL`
- Target instances: `LES_EMP_DETAIL_RECTYPE_R_TBL`

### Transformation `Norm_EMP_REC_TYPE_R` (Normalizer)

- **Reset**: `NO`
- **Restart**: `NO`

### Transformation `SQ_LES_EMP_DETAIL_TBL` (Source Qualifier)

- **Source Filter**: `LES_EMP_DETAIL_TBL.PP_END_YEAR = $$MAP_PP_END_YEAR AND LES_EMP_DETAIL_TBL.PP_NUM = $$MAP_PP_NUM`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `fil_EMP_REC_TYPE_R` (Filter)

- **Filter Condition**: `WS_RETR_REC_TYPE = '*R'`

### Transformation `fil_EMP_REC_TYPE_R_EMP_DETAIL` (Filter)

- **Filter Condition**: `WS_RETR_REC_TYPE = '*R' OR WS_RETR_REC_TYPE = '*E'`

### Transformation `jnr_LES_NUMBER` (Joiner)

- **Join Condition**: `LES_NUMBER = EMPR_LES_NUMBER`
- **Join Type**: `Normal Join`
- **Null ordering in master**: `Null Is Highest Value`
- **Null ordering in detail**: `Null Is Highest Value`
- **Sorted Input**: `NO`

- Joiner `jnr_LES_NUMBER`: Normal Join ON `LES_NUMBER = EMPR_LES_NUMBER`
- Normalizer `Norm_EMP_REC_TYPE_R` (vsam=True, source EMP_REC_TYPE_R) occurs: —; generated: GK_EMP_REC_TYPE_R

### Target instance `LES_EMP_DETAIL_RECTYPE_R_TBL` (table `LES_EMP_DETAIL_RECTYPE_R_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LES_EMP_DETAIL_RECTYPE_R_TBL | PP_END_YEAR | exp_Final.PP_END_YEAR → jnr_LES_NUMBER.PP_END_YEAR → SQ_LES_EMP_DETAIL_TBL.PP_END_YEAR → LES_EMP_DETAIL_TBL.PP_END_YEAR | LES_EMP_DETAIL_TBL.PP_END_YEAR |
| LES_EMP_DETAIL_RECTYPE_R_TBL | PP_NUM | exp_Final.PP_NUM → jnr_LES_NUMBER.PP_NUM → SQ_LES_EMP_DETAIL_TBL.PP_NUM → LES_EMP_DETAIL_TBL.PP_NUM | LES_EMP_DETAIL_TBL.PP_NUM |
| LES_EMP_DETAIL_RECTYPE_R_TBL | LES_NUMBER | exp_Final.LES_NUMBER → jnr_LES_NUMBER.EMPR_LES_NUMBER → fil_EMP_REC_TYPE_R.EMPR_LES_NUMBER → exp_Convert.o_EMPR_LES_NUMBER = IIF(IS_NUMBER(v_LES_NUMBER), TO_INTEGER(v_LES_NUMBER) ) → exp_Convert.v_LES_NUMBER = IIF(WS_RETR_REC_TYPE = '*E', SUBSTR(WS_RETR_ERN_NAME1, 10, 3) \|\| SUBSTR(WS_RETR_HRS_DAYS1_RDF, 1, 4), v_LES_NUMBER) → fil_EMP_REC_TYPE_R_EMP_DETAIL.WS_RETR_REC_TYPE → Norm_EMP_REC_TYPE_R.WS_RETR_REC_TYPE → EMP_REC_TYPE_R.WS_RETR_REC_TYPE → fil_EMP_REC_TYPE_R_EMP_DETAIL.WS_RETR_ERN_NAME1 → Norm_EMP_REC_TYPE_R.WS_RETR_ERN_NAME1 → EMP_REC_TYPE_R.WS_RETR_ERN_NAME1 → fil_EMP_REC_TYPE_R_EMP_DETAIL.WS_RETR_HRS_DAYS1_RDF → Norm_EMP_REC_TYPE_R.WS_RETR_HRS_DAYS1_RDF → EMP_REC_TYPE_R.WS_RETR_HRS_DAYS1_RDF | EMP_REC_TYPE_R.WS_RETR_ERN_NAME1; EMP_REC_TYPE_R.WS_RETR_HRS_DAYS1_RDF; EMP_REC_TYPE_R.WS_RETR_REC_TYPE |
| LES_EMP_DETAIL_RECTYPE_R_TBL | PSEUDOSSN | exp_Final.PSEUDOSSN → jnr_LES_NUMBER.PSEUDOSSN → SQ_LES_EMP_DETAIL_TBL.PSEUDOSSN → LES_EMP_DETAIL_TBL.PSEUDOSSN | LES_EMP_DETAIL_TBL.PSEUDOSSN |
| LES_EMP_DETAIL_RECTYPE_R_TBL | RETRO_ACTIVE_ID | exp_Final.RETRO_ACTIVE_ID → jnr_LES_NUMBER.RETRO_ACTIVE_ID → fil_EMP_REC_TYPE_R.RETRO_ACTIVE_ID → exp_Convert.o_RETRO_ACTIVE_ID = v_RETRO_ACTIVE_ID → exp_Convert.v_RETRO_ACTIVE_ID = IIF(WS_RETR_REC_TYPE = '*E', 0, v_RETRO_ACTIVE_ID + 1) → fil_EMP_REC_TYPE_R_EMP_DETAIL.WS_RETR_REC_TYPE → Norm_EMP_REC_TYPE_R.WS_RETR_REC_TYPE → EMP_REC_TYPE_R.WS_RETR_REC_TYPE | EMP_REC_TYPE_R.WS_RETR_REC_TYPE |
| LES_EMP_DETAIL_RECTYPE_R_TBL | RETRO_ACTIVE_EARN_NAME1 | exp_Final.RETRO_ACTIVE_EARN_NAME1 → jnr_LES_NUMBER.WS_RETR_ERN_NAME1 → fil_EMP_REC_TYPE_R.WS_RETR_ERN_NAME1 → exp_Convert.o_WS_RETR_ERN_NAME1 = LTRIM(RTRIM(WS_RETR_ERN_NAME1)) → fil_EMP_REC_TYPE_R_EMP_DETAIL.WS_RETR_ERN_NAME1 → Norm_EMP_REC_TYPE_R.WS_RETR_ERN_NAME1 → EMP_REC_TYPE_R.WS_RETR_ERN_NAME1 | EMP_REC_TYPE_R.WS_RETR_ERN_NAME1 |
| LES_EMP_DETAIL_RECTYPE_R_TBL | RETRO_ACTIVE_EARN_NAME1_HOURS | exp_Final.RETRO_ACTIVE_EARN_NAME1_HOURS → jnr_LES_NUMBER.WS_RETR_HRS_DAYS1 → fil_EMP_REC_TYPE_R.WS_RETR_HRS_DAYS1 → exp_Convert.WS_RETR_HRS_DAYS1 → fil_EMP_REC_TYPE_R_EMP_DETAIL.WS_RETR_HRS_DAYS1 → Norm_EMP_REC_TYPE_R.WS_RETR_HRS_DAYS1 → EMP_REC_TYPE_R.WS_RETR_HRS_DAYS1 | EMP_REC_TYPE_R.WS_RETR_HRS_DAYS1 |
| LES_EMP_DETAIL_RECTYPE_R_TBL | RETRO_ACTIVE_EARN_NAME1_AMT | exp_Final.RETRO_ACTIVE_EARN_NAME1_AMT → jnr_LES_NUMBER.WS_RETR_AMT1 → fil_EMP_REC_TYPE_R.WS_RETR_AMT1 → exp_Convert.WS_RETR_AMT1 → fil_EMP_REC_TYPE_R_EMP_DETAIL.WS_RETR_AMT1 → Norm_EMP_REC_TYPE_R.WS_RETR_AMT1 → EMP_REC_TYPE_R.WS_RETR_AMT1 | EMP_REC_TYPE_R.WS_RETR_AMT1 |
| LES_EMP_DETAIL_RECTYPE_R_TBL | RETRO_ACTIVE_EARN_NAME2 | exp_Final.RETRO_ACTIVE_EARN_NAME2 → jnr_LES_NUMBER.WS_RETR_ERN_NAME2 → fil_EMP_REC_TYPE_R.WS_RETR_ERN_NAME2 → exp_Convert.o_WS_RETR_ERN_NAME2 = LTRIM(RTRIM(WS_RETR_ERN_NAME2)) → fil_EMP_REC_TYPE_R_EMP_DETAIL.WS_RETR_ERN_NAME2 → Norm_EMP_REC_TYPE_R.WS_RETR_ERN_NAME2 → EMP_REC_TYPE_R.WS_RETR_ERN_NAME2 | EMP_REC_TYPE_R.WS_RETR_ERN_NAME2 |
| LES_EMP_DETAIL_RECTYPE_R_TBL | RETRO_ACTIVE_EARN_NAME2_HOURS | exp_Final.RETRO_ACTIVE_EARN_NAME2_HOURS → jnr_LES_NUMBER.WS_RETR_HRS_DAYS2 → fil_EMP_REC_TYPE_R.WS_RETR_HRS_DAYS2 → exp_Convert.WS_RETR_HRS_DAYS2 → fil_EMP_REC_TYPE_R_EMP_DETAIL.WS_RETR_HRS_DAYS2 → Norm_EMP_REC_TYPE_R.WS_RETR_HRS_DAYS2 → EMP_REC_TYPE_R.WS_RETR_HRS_DAYS2 | EMP_REC_TYPE_R.WS_RETR_HRS_DAYS2 |
| LES_EMP_DETAIL_RECTYPE_R_TBL | RETRO_ACTIVE_EARN_NAME2_AMT | exp_Final.RETRO_ACTIVE_EARN_NAME2_AMT → jnr_LES_NUMBER.WS_RETR_AMT2 → fil_EMP_REC_TYPE_R.WS_RETR_AMT2 → exp_Convert.WS_RETR_AMT2 → fil_EMP_REC_TYPE_R_EMP_DETAIL.WS_RETR_AMT2 → Norm_EMP_REC_TYPE_R.WS_RETR_AMT2 → EMP_REC_TYPE_R.WS_RETR_AMT2 | EMP_REC_TYPE_R.WS_RETR_AMT2 |
| LES_EMP_DETAIL_RECTYPE_R_TBL | RETRO_ACTIVE_EARN_NAME3 | exp_Final.RETRO_ACTIVE_EARN_NAME3 → jnr_LES_NUMBER.WS_RETR_ERN_NAME3 → fil_EMP_REC_TYPE_R.WS_RETR_ERN_NAME3 → exp_Convert.o_WS_RETR_ERN_NAME3 = LTRIM(RTRIM(WS_RETR_ERN_NAME3)) → fil_EMP_REC_TYPE_R_EMP_DETAIL.WS_RETR_ERN_NAME3 → Norm_EMP_REC_TYPE_R.WS_RETR_ERN_NAME3 → EMP_REC_TYPE_R.WS_RETR_ERN_NAME3 | EMP_REC_TYPE_R.WS_RETR_ERN_NAME3 |
| LES_EMP_DETAIL_RECTYPE_R_TBL | RETRO_ACTIVE_EARN_NAME3_HOURS | exp_Final.RETRO_ACTIVE_EARN_NAME3_HOURS → jnr_LES_NUMBER.WS_RETR_HRS_DAYS3 → fil_EMP_REC_TYPE_R.WS_RETR_HRS_DAYS3 → exp_Convert.WS_RETR_HRS_DAYS3 → fil_EMP_REC_TYPE_R_EMP_DETAIL.WS_RETR_HRS_DAYS3 → Norm_EMP_REC_TYPE_R.WS_RETR_HRS_DAYS3 → EMP_REC_TYPE_R.WS_RETR_HRS_DAYS3 | EMP_REC_TYPE_R.WS_RETR_HRS_DAYS3 |
| LES_EMP_DETAIL_RECTYPE_R_TBL | RETRO_ACTIVE_EARN_NAME3_AMT | exp_Final.RETRO_ACTIVE_EARN_NAME3_AMT → jnr_LES_NUMBER.WS_RETR_AMT3 → fil_EMP_REC_TYPE_R.WS_RETR_AMT3 → exp_Convert.WS_RETR_AMT3 → fil_EMP_REC_TYPE_R_EMP_DETAIL.WS_RETR_AMT3 → Norm_EMP_REC_TYPE_R.WS_RETR_AMT3 → EMP_REC_TYPE_R.WS_RETR_AMT3 | EMP_REC_TYPE_R.WS_RETR_AMT3 |

## Mapping `m_LES_Load_LES_EMP_DETAIL_RECTYPE_D_TBL`

- Sessions: `s_LES_Load_LES_EMP_DETAIL_RECTYPE_D_TBL` (#14)
- Sources: `EMP_REC_TYPE_D`, `LES_EMP_DETAIL_TBL`
- Target instances: `LES_EMP_DETAIL_RECTYPE_D_TBL`

### Transformation `Norm_EMP_REC_TYPE_D` (Normalizer)

- **Reset**: `NO`
- **Restart**: `NO`

### Transformation `SQ_LES_EMP_DETAIL_TBL` (Source Qualifier)

- **Source Filter**: `LES_EMP_DETAIL_TBL.PP_END_YEAR = $$MAP_PP_END_YEAR AND LES_EMP_DETAIL_TBL.PP_NUM = $$MAP_PP_NUM`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `fil_EMP_REC_TYPE_D` (Filter)

- **Filter Condition**: `WS_DED_REC_TYPE = '*D'`

### Transformation `fil_EMP_REC_TYPE_D_EMP_DETAIL` (Filter)

- **Filter Condition**: `WS_DED_REC_TYPE = '*D' OR WS_DED_REC_TYPE = '*E'`

### Transformation `jnr_LES_NUMBER` (Joiner)

- **Join Condition**: `LES_NUMBER = EMPD_LES_NUMBER`
- **Join Type**: `Normal Join`
- **Null ordering in master**: `Null Is Highest Value`
- **Null ordering in detail**: `Null Is Highest Value`
- **Sorted Input**: `NO`

- Joiner `jnr_LES_NUMBER`: Normal Join ON `LES_NUMBER = EMPD_LES_NUMBER`
- Normalizer `Norm_EMP_REC_TYPE_D` (vsam=True, source EMP_REC_TYPE_D) occurs: —; generated: —

### Target instance `LES_EMP_DETAIL_RECTYPE_D_TBL` (table `LES_EMP_DETAIL_RECTYPE_D_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LES_EMP_DETAIL_RECTYPE_D_TBL | PP_END_YEAR | exp_Final.PP_END_YEAR → jnr_LES_NUMBER.PP_END_YEAR → SQ_LES_EMP_DETAIL_TBL.PP_END_YEAR → LES_EMP_DETAIL_TBL.PP_END_YEAR | LES_EMP_DETAIL_TBL.PP_END_YEAR |
| LES_EMP_DETAIL_RECTYPE_D_TBL | PP_NUM | exp_Final.PP_NUM → jnr_LES_NUMBER.PP_NUM → SQ_LES_EMP_DETAIL_TBL.PP_NUM → LES_EMP_DETAIL_TBL.PP_NUM | LES_EMP_DETAIL_TBL.PP_NUM |
| LES_EMP_DETAIL_RECTYPE_D_TBL | LES_NUMBER | exp_Final.LES_NUMBER → jnr_LES_NUMBER.EMPD_LES_NUMBER → fil_EMP_REC_TYPE_D.EMPD_LES_NUMBER → exp_Convert.o_EMPD_LES_NUMBER = IIF(IS_NUMBER(v_LES_NUMBER), TO_INTEGER(v_LES_NUMBER) ) → exp_Convert.v_LES_NUMBER = IIF(WS_DED_REC_TYPE = '*E', SUBSTR(WS_DED_NAME1, 10, 3) \|\| SUBSTR(WS_DED_CODE1, 1, 4), v_LES_NUMBER) → fil_EMP_REC_TYPE_D_EMP_DETAIL.WS_DED_REC_TYPE → Norm_EMP_REC_TYPE_D.WS_DED_REC_TYPE → EMP_REC_TYPE_D.WS_DED_REC_TYPE → fil_EMP_REC_TYPE_D_EMP_DETAIL.WS_DED_NAME1 → Norm_EMP_REC_TYPE_D.WS_DED_NAME1 → EMP_REC_TYPE_D.WS_DED_NAME1 → fil_EMP_REC_TYPE_D_EMP_DETAIL.WS_DED_CODE1 → Norm_EMP_REC_TYPE_D.WS_DED_CODE1 → EMP_REC_TYPE_D.WS_DED_CODE1 | EMP_REC_TYPE_D.WS_DED_CODE1; EMP_REC_TYPE_D.WS_DED_NAME1; EMP_REC_TYPE_D.WS_DED_REC_TYPE |
| LES_EMP_DETAIL_RECTYPE_D_TBL | PSEUDOSSN | exp_Final.PSEUDOSSN → jnr_LES_NUMBER.PSEUDOSSN → SQ_LES_EMP_DETAIL_TBL.PSEUDOSSN → LES_EMP_DETAIL_TBL.PSEUDOSSN | LES_EMP_DETAIL_TBL.PSEUDOSSN |
| LES_EMP_DETAIL_RECTYPE_D_TBL | DEDUCTION_ID | exp_Final.DEDUCTION_ID → jnr_LES_NUMBER.DEDUCTION_ID → fil_EMP_REC_TYPE_D.DEDUCTION_ID → exp_Convert.o_DEDUCTION_ID = v_DEDUCTION_ID → exp_Convert.v_DEDUCTION_ID = IIF(WS_DED_REC_TYPE = '*E', 0, v_DEDUCTION_ID + 1) → fil_EMP_REC_TYPE_D_EMP_DETAIL.WS_DED_REC_TYPE → Norm_EMP_REC_TYPE_D.WS_DED_REC_TYPE → EMP_REC_TYPE_D.WS_DED_REC_TYPE | EMP_REC_TYPE_D.WS_DED_REC_TYPE |
| LES_EMP_DETAIL_RECTYPE_D_TBL | DEDUCTION_1_NAME | exp_Final.DEDUCTION_1_NAME → jnr_LES_NUMBER.WS_DED_NAME1 → fil_EMP_REC_TYPE_D.WS_DED_NAME1 → exp_Convert.o_WS_DED_NAME1 = LTRIM(RTRIM(WS_DED_NAME1)) → fil_EMP_REC_TYPE_D_EMP_DETAIL.WS_DED_NAME1 → Norm_EMP_REC_TYPE_D.WS_DED_NAME1 → EMP_REC_TYPE_D.WS_DED_NAME1 | EMP_REC_TYPE_D.WS_DED_NAME1 |
| LES_EMP_DETAIL_RECTYPE_D_TBL | DEDUCTION_1_CODE | exp_Final.DEDUCTION_1_CODE → jnr_LES_NUMBER.WS_DED_CODE1 → fil_EMP_REC_TYPE_D.WS_DED_CODE1 → exp_Convert.WS_DED_CODE1 → fil_EMP_REC_TYPE_D_EMP_DETAIL.WS_DED_CODE1 → Norm_EMP_REC_TYPE_D.WS_DED_CODE1 → EMP_REC_TYPE_D.WS_DED_CODE1 | EMP_REC_TYPE_D.WS_DED_CODE1 |
| LES_EMP_DETAIL_RECTYPE_D_TBL | DEDUCTION_1_AMT | exp_Final.DEDUCTION_1_AMT → jnr_LES_NUMBER.WS_DED_AMT1 → fil_EMP_REC_TYPE_D.WS_DED_AMT1 → exp_Convert.WS_DED_AMT1 → fil_EMP_REC_TYPE_D_EMP_DETAIL.WS_DED_AMT1 → Norm_EMP_REC_TYPE_D.WS_DED_AMT1 → EMP_REC_TYPE_D.WS_DED_AMT1 | EMP_REC_TYPE_D.WS_DED_AMT1 |
| LES_EMP_DETAIL_RECTYPE_D_TBL | DEDUCTION_1_AMT_YTD | exp_Final.DEDUCTION_1_AMT_YTD → jnr_LES_NUMBER.WS_DED_AMT_YTD1 → fil_EMP_REC_TYPE_D.WS_DED_AMT_YTD1 → exp_Convert.WS_DED_AMT_YTD1 → fil_EMP_REC_TYPE_D_EMP_DETAIL.WS_DED_AMT_YTD1 → Norm_EMP_REC_TYPE_D.WS_DED_AMT_YTD1 → EMP_REC_TYPE_D.WS_DED_AMT_YTD1 | EMP_REC_TYPE_D.WS_DED_AMT_YTD1 |
| LES_EMP_DETAIL_RECTYPE_D_TBL | DEDUCTION_2_NAME | exp_Final.DEDUCTION_2_NAME → jnr_LES_NUMBER.WS_DED_NAME2 → fil_EMP_REC_TYPE_D.WS_DED_NAME2 → exp_Convert.o_WS_DED_NAME2 = LTRIM(RTRIM(WS_DED_NAME2)) → fil_EMP_REC_TYPE_D_EMP_DETAIL.WS_DED_NAME2 → Norm_EMP_REC_TYPE_D.WS_DED_NAME2 → EMP_REC_TYPE_D.WS_DED_NAME2 | EMP_REC_TYPE_D.WS_DED_NAME2 |
| LES_EMP_DETAIL_RECTYPE_D_TBL | DEDUCTION_2_CODE | exp_Final.DEDUCTION_2_CODE → jnr_LES_NUMBER.WS_DED_CODE2 → fil_EMP_REC_TYPE_D.WS_DED_CODE2 → exp_Convert.WS_DED_CODE2 → fil_EMP_REC_TYPE_D_EMP_DETAIL.WS_DED_CODE2 → Norm_EMP_REC_TYPE_D.WS_DED_CODE2 → EMP_REC_TYPE_D.WS_DED_CODE2 | EMP_REC_TYPE_D.WS_DED_CODE2 |
| LES_EMP_DETAIL_RECTYPE_D_TBL | DEDUCTION_2_AMT | exp_Final.DEDUCTION_2_AMT → jnr_LES_NUMBER.WS_DED_AMT2 → fil_EMP_REC_TYPE_D.WS_DED_AMT2 → exp_Convert.WS_DED_AMT2 → fil_EMP_REC_TYPE_D_EMP_DETAIL.WS_DED_AMT2 → Norm_EMP_REC_TYPE_D.WS_DED_AMT2 → EMP_REC_TYPE_D.WS_DED_AMT2 | EMP_REC_TYPE_D.WS_DED_AMT2 |
| LES_EMP_DETAIL_RECTYPE_D_TBL | DEDUCTION_2_AMT_YTD | exp_Final.DEDUCTION_2_AMT_YTD → jnr_LES_NUMBER.WS_DED_AMT_YTD2 → fil_EMP_REC_TYPE_D.WS_DED_AMT_YTD2 → exp_Convert.WS_DED_AMT_YTD2 → fil_EMP_REC_TYPE_D_EMP_DETAIL.WS_DED_AMT_YTD2 → Norm_EMP_REC_TYPE_D.WS_DED_AMT_YTD2 → EMP_REC_TYPE_D.WS_DED_AMT_YTD2 | EMP_REC_TYPE_D.WS_DED_AMT_YTD2 |

## Mapping `m_LES_Load_LES_EMP_DETAIL_RECTYPE_L_TBL`

- Sessions: `s_LES_Load_LES_EMP_DETAIL_RECTYPE_L_TBL` (#15)
- Sources: `EMP_REC_TYPE_L`, `LES_EMP_DETAIL_TBL`
- Target instances: `LES_EMP_DETAIL_RECTYPE_L_TBL`

### Transformation `Norm_EMP_REC_TYPE_L` (Normalizer)

- **Reset**: `NO`
- **Restart**: `NO`

### Transformation `SQ_LES_EMP_DETAIL_TBL` (Source Qualifier)

- **Source Filter**: `LES_EMP_DETAIL_TBL.PP_END_YEAR = $$MAP_PP_END_YEAR AND LES_EMP_DETAIL_TBL.PP_NUM = $$MAP_PP_NUM`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `fil_EMP_REC_TYPE_L` (Filter)

- **Filter Condition**: `WS_LV_REC_TYPE = '*L'`

### Transformation `fil_EMP_REC_TYPE_L_EMP_DETAIL` (Filter)

- **Filter Condition**: `WS_LV_REC_TYPE = '*L' OR WS_LV_REC_TYPE = '*E'`

### Transformation `jnr_LES_NUMBER` (Joiner)

- **Join Condition**: `LES_NUMBER = EMPL_LES_NUMBER`
- **Join Type**: `Normal Join`
- **Null ordering in master**: `Null Is Highest Value`
- **Null ordering in detail**: `Null Is Highest Value`
- **Sorted Input**: `NO`

- Joiner `jnr_LES_NUMBER`: Normal Join ON `LES_NUMBER = EMPL_LES_NUMBER`
- Normalizer `Norm_EMP_REC_TYPE_L` (vsam=True, source EMP_REC_TYPE_L) occurs: —; generated: GK_EMP_REC_TYPE_L

### Target instance `LES_EMP_DETAIL_RECTYPE_L_TBL` (table `LES_EMP_DETAIL_RECTYPE_L_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LES_EMP_DETAIL_RECTYPE_L_TBL | PP_END_YEAR | exp_Final.PP_END_YEAR → jnr_LES_NUMBER.PP_END_YEAR → SQ_LES_EMP_DETAIL_TBL.PP_END_YEAR → LES_EMP_DETAIL_TBL.PP_END_YEAR | LES_EMP_DETAIL_TBL.PP_END_YEAR |
| LES_EMP_DETAIL_RECTYPE_L_TBL | PP_NUM | exp_Final.PP_NUM → jnr_LES_NUMBER.PP_NUM → SQ_LES_EMP_DETAIL_TBL.PP_NUM → LES_EMP_DETAIL_TBL.PP_NUM | LES_EMP_DETAIL_TBL.PP_NUM |
| LES_EMP_DETAIL_RECTYPE_L_TBL | LES_NUMBER | exp_Final.LES_NUMBER → jnr_LES_NUMBER.EMPL_LES_NUMBER → fil_EMP_REC_TYPE_L.EMPL_LES_NUMBER → exp_Convert.o_EMPL_LES_NUMBER = IIF(IS_NUMBER(v_LES_NUMBER), TO_INTEGER(v_LES_NUMBER) ) → exp_Convert.v_LES_NUMBER = IIF(WS_LV_REC_TYPE = '*E', SUBSTR(WS_LV_NAME, 10, 3) \|\| SUBSTR(WS_LV_PRIOR_YR_BAL_RDF, 1, 4), v_LES_NUMBER) → fil_EMP_REC_TYPE_L_EMP_DETAIL.WS_LV_REC_TYPE → Norm_EMP_REC_TYPE_L.WS_LV_REC_TYPE → EMP_REC_TYPE_L.WS_LV_REC_TYPE → fil_EMP_REC_TYPE_L_EMP_DETAIL.WS_LV_NAME → Norm_EMP_REC_TYPE_L.WS_LV_NAME → EMP_REC_TYPE_L.WS_LV_NAME → fil_EMP_REC_TYPE_L_EMP_DETAIL.WS_LV_PRIOR_YR_BAL_RDF → Norm_EMP_REC_TYPE_L.WS_LV_PRIOR_YR_BAL_RDF → EMP_REC_TYPE_L.WS_LV_PRIOR_YR_BAL_RDF | EMP_REC_TYPE_L.WS_LV_NAME; EMP_REC_TYPE_L.WS_LV_PRIOR_YR_BAL_RDF; EMP_REC_TYPE_L.WS_LV_REC_TYPE |
| LES_EMP_DETAIL_RECTYPE_L_TBL | PSEUDOSSN | exp_Final.PSEUDOSSN → jnr_LES_NUMBER.PSEUDOSSN → SQ_LES_EMP_DETAIL_TBL.PSEUDOSSN → LES_EMP_DETAIL_TBL.PSEUDOSSN | LES_EMP_DETAIL_TBL.PSEUDOSSN |
| LES_EMP_DETAIL_RECTYPE_L_TBL | LEAVE_ID | exp_Final.LEAVE_ID → jnr_LES_NUMBER.LEAVE_ID → fil_EMP_REC_TYPE_L.LEAVE_ID → exp_Convert.o_LEAVE_ID = v_LEAVE_ID → exp_Convert.v_LEAVE_ID = IIF(WS_LV_REC_TYPE = '*E', 0, v_LEAVE_ID + 1) → fil_EMP_REC_TYPE_L_EMP_DETAIL.WS_LV_REC_TYPE → Norm_EMP_REC_TYPE_L.WS_LV_REC_TYPE → EMP_REC_TYPE_L.WS_LV_REC_TYPE | EMP_REC_TYPE_L.WS_LV_REC_TYPE |
| LES_EMP_DETAIL_RECTYPE_L_TBL | LEAVE_NAME | exp_Final.LEAVE_NAME → jnr_LES_NUMBER.WS_LV_NAME → fil_EMP_REC_TYPE_L.WS_LV_NAME → exp_Convert.o_WS_LV_NAME = LTRIM(RTRIM(WS_LV_NAME)) → fil_EMP_REC_TYPE_L_EMP_DETAIL.WS_LV_NAME → Norm_EMP_REC_TYPE_L.WS_LV_NAME → EMP_REC_TYPE_L.WS_LV_NAME | EMP_REC_TYPE_L.WS_LV_NAME |
| LES_EMP_DETAIL_RECTYPE_L_TBL | LEAVE_PRIOR_YEAR_BAL | exp_Final.LEAVE_PRIOR_YEAR_BAL → jnr_LES_NUMBER.WS_LV_PRIOR_YR_BAL → fil_EMP_REC_TYPE_L.WS_LV_PRIOR_YR_BAL → exp_Convert.WS_LV_PRIOR_YR_BAL → fil_EMP_REC_TYPE_L_EMP_DETAIL.WS_LV_PRIOR_YR_BAL → Norm_EMP_REC_TYPE_L.WS_LV_PRIOR_YR_BAL → EMP_REC_TYPE_L.WS_LV_PRIOR_YR_BAL | EMP_REC_TYPE_L.WS_LV_PRIOR_YR_BAL |
| LES_EMP_DETAIL_RECTYPE_L_TBL | LEAVE_EARNED_CPP | exp_Final.LEAVE_EARNED_CPP → jnr_LES_NUMBER.WS_LV_ACCR_PP → fil_EMP_REC_TYPE_L.WS_LV_ACCR_PP → exp_Convert.WS_LV_ACCR_PP → fil_EMP_REC_TYPE_L_EMP_DETAIL.WS_LV_ACCR_PP → Norm_EMP_REC_TYPE_L.WS_LV_ACCR_PP → EMP_REC_TYPE_L.WS_LV_ACCR_PP | EMP_REC_TYPE_L.WS_LV_ACCR_PP |
| LES_EMP_DETAIL_RECTYPE_L_TBL | LEAVE_EARNED_YTD | exp_Final.LEAVE_EARNED_YTD → jnr_LES_NUMBER.WS_LV_ACCR_YTD → fil_EMP_REC_TYPE_L.WS_LV_ACCR_YTD → exp_Convert.WS_LV_ACCR_YTD → fil_EMP_REC_TYPE_L_EMP_DETAIL.WS_LV_ACCR_YTD → Norm_EMP_REC_TYPE_L.WS_LV_ACCR_YTD → EMP_REC_TYPE_L.WS_LV_ACCR_YTD | EMP_REC_TYPE_L.WS_LV_ACCR_YTD |
| LES_EMP_DETAIL_RECTYPE_L_TBL | LEAVE_USED_CPP | exp_Final.LEAVE_USED_CPP → jnr_LES_NUMBER.WS_LV_USED_CURR_PP → fil_EMP_REC_TYPE_L.WS_LV_USED_CURR_PP → exp_Convert.WS_LV_USED_CURR_PP → fil_EMP_REC_TYPE_L_EMP_DETAIL.WS_LV_USED_CURR_PP → Norm_EMP_REC_TYPE_L.WS_LV_USED_CURR_PP → EMP_REC_TYPE_L.WS_LV_USED_CURR_PP | EMP_REC_TYPE_L.WS_LV_USED_CURR_PP |
| LES_EMP_DETAIL_RECTYPE_L_TBL | LEAVE_USED_YTD | exp_Final.LEAVE_USED_YTD → jnr_LES_NUMBER.WS_LV_USED_YTD → fil_EMP_REC_TYPE_L.WS_LV_USED_YTD → exp_Convert.WS_LV_USED_YTD → fil_EMP_REC_TYPE_L_EMP_DETAIL.WS_LV_USED_YTD → Norm_EMP_REC_TYPE_L.WS_LV_USED_YTD → EMP_REC_TYPE_L.WS_LV_USED_YTD | EMP_REC_TYPE_L.WS_LV_USED_YTD |
| LES_EMP_DETAIL_RECTYPE_L_TBL | LEAVE_DONATED | exp_Final.LEAVE_DONATED → jnr_LES_NUMBER.WS_LV_DONATE_RET → fil_EMP_REC_TYPE_L.WS_LV_DONATE_RET → exp_Convert.WS_LV_DONATE_RET → fil_EMP_REC_TYPE_L_EMP_DETAIL.WS_LV_DONATE_RET → Norm_EMP_REC_TYPE_L.WS_LV_DONATE_RET → EMP_REC_TYPE_L.WS_LV_DONATE_RET | EMP_REC_TYPE_L.WS_LV_DONATE_RET |
| LES_EMP_DETAIL_RECTYPE_L_TBL | LEAVE_CURR_BAL | exp_Final.LEAVE_CURR_BAL → jnr_LES_NUMBER.WS_LV_CURR_BAL → fil_EMP_REC_TYPE_L.WS_LV_CURR_BAL → exp_Convert.WS_LV_CURR_BAL → fil_EMP_REC_TYPE_L_EMP_DETAIL.WS_LV_CURR_BAL → Norm_EMP_REC_TYPE_L.WS_LV_CURR_BAL → EMP_REC_TYPE_L.WS_LV_CURR_BAL | EMP_REC_TYPE_L.WS_LV_CURR_BAL |
| LES_EMP_DETAIL_RECTYPE_L_TBL | LEAVE_USE_OR_LOSE_TERM_DTE | exp_Final.LEAVE_USE_OR_LOSE_TERM_DTE → jnr_LES_NUMBER.LV_TERM_DATE → fil_EMP_REC_TYPE_L.LV_TERM_DATE → exp_Convert.o_LV_TERM_DATE = IIF(IS_DATE(v_LV_TERM_DATE, 'MM/DD/RR'), TO_DATE(v_LV_TERM_DATE, 'MM/DD/RR') ) → exp_Convert.v_LV_TERM_DATE = LTRIM(RTRIM(WS_LV_TERM_DATE)) → fil_EMP_REC_TYPE_L_EMP_DETAIL.WS_LV_TERM_DATE → Norm_EMP_REC_TYPE_L.WS_LV_TERM_DATE → EMP_REC_TYPE_L.WS_LV_TERM_DATE | EMP_REC_TYPE_L.WS_LV_TERM_DATE |
| LES_EMP_DETAIL_RECTYPE_L_TBL | LEAVE_USE_OR_LOSE_TERM_BAL_HRS | exp_Final.LEAVE_USE_OR_LOSE_TERM_BAL_HRS → jnr_LES_NUMBER.LV_TERM_BAL_HRS → fil_EMP_REC_TYPE_L.LV_TERM_BAL_HRS → exp_Convert.o_LV_TERM_BAL_HRS = IIF(IS_NUMBER(v_LV_TERM_DATE), TO_DECIMAL(v_LV_TERM_DATE, 2) ) → exp_Convert.v_LV_TERM_DATE = LTRIM(RTRIM(WS_LV_TERM_DATE)) → fil_EMP_REC_TYPE_L_EMP_DETAIL.WS_LV_TERM_DATE → Norm_EMP_REC_TYPE_L.WS_LV_TERM_DATE → EMP_REC_TYPE_L.WS_LV_TERM_DATE | EMP_REC_TYPE_L.WS_LV_TERM_DATE |

## Mapping `m_LES_Load_LES_EMP_DETAIL_RECTYPE_U_TBL`

- Sessions: `s_LES_Load_LES_EMP_DETAIL_RECTYPE_U_TBL` (#16)
- Sources: `EMP_REC_TYPE_U`, `LES_EMP_DETAIL_TBL`
- Target instances: `LES_EMP_DETAIL_RECTYPE_U_TBL`

### Transformation `Norm_EMP_REC_TYPE_U` (Normalizer)

- **Reset**: `NO`
- **Restart**: `NO`

### Transformation `SQ_LES_EMP_DETAIL_TBL` (Source Qualifier)

- **Source Filter**: `LES_EMP_DETAIL_TBL.PP_END_YEAR = $$MAP_PP_END_YEAR AND LES_EMP_DETAIL_TBL.PP_NUM = $$MAP_PP_NUM`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `fil_EMP_REC_TYPE_U` (Filter)

- **Filter Condition**: `WS_EMPLR_REC_TYPE = '*U'`

### Transformation `fil_EMP_REC_TYPE_U_EMP_DETAIL` (Filter)

- **Filter Condition**: `WS_EMPLR_REC_TYPE = '*U' OR WS_EMPLR_REC_TYPE = '*E'`

### Transformation `jnr_LES_NUMBER` (Joiner)

- **Join Condition**: `LES_NUMBER = EMPU_LES_NUMBER`
- **Join Type**: `Normal Join`
- **Null ordering in master**: `Null Is Highest Value`
- **Null ordering in detail**: `Null Is Highest Value`
- **Sorted Input**: `NO`

- Joiner `jnr_LES_NUMBER`: Normal Join ON `LES_NUMBER = EMPU_LES_NUMBER`
- Normalizer `Norm_EMP_REC_TYPE_U` (vsam=True, source EMP_REC_TYPE_U) occurs: —; generated: GK_EMP_REC_TYPE_U

### Target instance `LES_EMP_DETAIL_RECTYPE_U_TBL` (table `LES_EMP_DETAIL_RECTYPE_U_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LES_EMP_DETAIL_RECTYPE_U_TBL | PP_END_YEAR | exp_Final.PP_END_YEAR → jnr_LES_NUMBER.PP_END_YEAR → SQ_LES_EMP_DETAIL_TBL.PP_END_YEAR → LES_EMP_DETAIL_TBL.PP_END_YEAR | LES_EMP_DETAIL_TBL.PP_END_YEAR |
| LES_EMP_DETAIL_RECTYPE_U_TBL | PP_NUM | exp_Final.PP_NUM → jnr_LES_NUMBER.PP_NUM → SQ_LES_EMP_DETAIL_TBL.PP_NUM → LES_EMP_DETAIL_TBL.PP_NUM | LES_EMP_DETAIL_TBL.PP_NUM |
| LES_EMP_DETAIL_RECTYPE_U_TBL | LES_NUMBER | exp_Final.LES_NUMBER → jnr_LES_NUMBER.EMPU_LES_NUMBER → fil_EMP_REC_TYPE_U.EMPU_LES_NUMBER → exp_Convert.o_EMPU_LES_NUMBER = IIF(IS_NUMBER(v_LES_NUMBER), TO_INTEGER(v_LES_NUMBER) ) → exp_Convert.v_LES_NUMBER = IIF(WS_EMPLR_REC_TYPE = '*E', SUBSTR(WS_EMPLR_CONT_NAME1, 10, 3) \|\| SUBSTR(WS_EMPLR_CONT_AMT1_RDF, 1, 4), v_LES_NUMBER) → fil_EMP_REC_TYPE_U_EMP_DETAIL.WS_EMPLR_REC_TYPE → Norm_EMP_REC_TYPE_U.WS_EMPLR_REC_TYPE → EMP_REC_TYPE_U.WS_EMPLR_REC_TYPE → fil_EMP_REC_TYPE_U_EMP_DETAIL.WS_EMPLR_CONT_NAME1 → Norm_EMP_REC_TYPE_U.WS_EMPLR_CONT_NAME1 → EMP_REC_TYPE_U.WS_EMPLR_CONT_NAME1 → fil_EMP_REC_TYPE_U_EMP_DETAIL.WS_EMPLR_CONT_AMT1_RDF → Norm_EMP_REC_TYPE_U.WS_EMPLR_CONT_AMT1_RDF → EMP_REC_TYPE_U.WS_EMPLR_CONT_AMT1_RDF | EMP_REC_TYPE_U.WS_EMPLR_CONT_AMT1_RDF; EMP_REC_TYPE_U.WS_EMPLR_CONT_NAME1; EMP_REC_TYPE_U.WS_EMPLR_REC_TYPE |
| LES_EMP_DETAIL_RECTYPE_U_TBL | PSEUDOSSN | exp_Final.PSEUDOSSN → jnr_LES_NUMBER.PSEUDOSSN → SQ_LES_EMP_DETAIL_TBL.PSEUDOSSN → LES_EMP_DETAIL_TBL.PSEUDOSSN | LES_EMP_DETAIL_TBL.PSEUDOSSN |
| LES_EMP_DETAIL_RECTYPE_U_TBL | EMPLOYER_CONTR_ID | exp_Final.EMPLOYER_CONTR_ID → jnr_LES_NUMBER.EMPLOYER_CONTR_ID → fil_EMP_REC_TYPE_U.EMPLOYER_CONTR_ID → exp_Convert.o_EMPLOYER_CONTR_ID = v_EMPLOYER_CONTR_ID → exp_Convert.v_EMPLOYER_CONTR_ID = IIF(WS_EMPLR_REC_TYPE = '*E', 0, v_EMPLOYER_CONTR_ID + 1) → fil_EMP_REC_TYPE_U_EMP_DETAIL.WS_EMPLR_REC_TYPE → Norm_EMP_REC_TYPE_U.WS_EMPLR_REC_TYPE → EMP_REC_TYPE_U.WS_EMPLR_REC_TYPE | EMP_REC_TYPE_U.WS_EMPLR_REC_TYPE |
| LES_EMP_DETAIL_RECTYPE_U_TBL | EMPLOYER_CONTR_1_NAME | exp_Final.EMPLOYER_CONTR_1_NAME → jnr_LES_NUMBER.WS_EMPLR_CONT_NAME1 → fil_EMP_REC_TYPE_U.WS_EMPLR_CONT_NAME1 → exp_Convert.o_WS_EMPLR_CONT_NAME1 = LTRIM(RTRIM(WS_EMPLR_CONT_NAME1)) → fil_EMP_REC_TYPE_U_EMP_DETAIL.WS_EMPLR_CONT_NAME1 → Norm_EMP_REC_TYPE_U.WS_EMPLR_CONT_NAME1 → EMP_REC_TYPE_U.WS_EMPLR_CONT_NAME1 | EMP_REC_TYPE_U.WS_EMPLR_CONT_NAME1 |
| LES_EMP_DETAIL_RECTYPE_U_TBL | EMPLOYER_CONTR_1_AMT | exp_Final.EMPLOYER_CONTR_1_AMT → jnr_LES_NUMBER.WS_EMPLR_CONT_AMT1 → fil_EMP_REC_TYPE_U.WS_EMPLR_CONT_AMT1 → exp_Convert.WS_EMPLR_CONT_AMT1 → fil_EMP_REC_TYPE_U_EMP_DETAIL.WS_EMPLR_CONT_AMT1 → Norm_EMP_REC_TYPE_U.WS_EMPLR_CONT_AMT1 → EMP_REC_TYPE_U.WS_EMPLR_CONT_AMT1 | EMP_REC_TYPE_U.WS_EMPLR_CONT_AMT1 |
| LES_EMP_DETAIL_RECTYPE_U_TBL | EMPLOYER_CONTR_1_AMT_YTD | exp_Final.EMPLOYER_CONTR_1_AMT_YTD → jnr_LES_NUMBER.WS_EMPLR_CONT_AMT_YTD1 → fil_EMP_REC_TYPE_U.WS_EMPLR_CONT_AMT_YTD1 → exp_Convert.WS_EMPLR_CONT_AMT_YTD1 → fil_EMP_REC_TYPE_U_EMP_DETAIL.WS_EMPLR_CONT_AMT_YTD1 → Norm_EMP_REC_TYPE_U.WS_EMPLR_CONT_AMT_YTD1 → EMP_REC_TYPE_U.WS_EMPLR_CONT_AMT_YTD1 | EMP_REC_TYPE_U.WS_EMPLR_CONT_AMT_YTD1 |
| LES_EMP_DETAIL_RECTYPE_U_TBL | EMPLOYER_CONTR_2_NAME | exp_Final.EMPLOYER_CONTR_2_NAME → jnr_LES_NUMBER.WS_EMPLR_CONT_NAME2 → fil_EMP_REC_TYPE_U.WS_EMPLR_CONT_NAME2 → exp_Convert.o_WS_EMPLR_CONT_NAME2 = LTRIM(RTRIM(WS_EMPLR_CONT_NAME2)) → fil_EMP_REC_TYPE_U_EMP_DETAIL.WS_EMPLR_CONT_NAME2 → Norm_EMP_REC_TYPE_U.WS_EMPLR_CONT_NAME2 → EMP_REC_TYPE_U.WS_EMPLR_CONT_NAME2 | EMP_REC_TYPE_U.WS_EMPLR_CONT_NAME2 |
| LES_EMP_DETAIL_RECTYPE_U_TBL | EMPLOYER_CONTR_2_AMT | exp_Final.EMPLOYER_CONTR_2_AMT → jnr_LES_NUMBER.WS_EMPLR_CONT_AMT2 → fil_EMP_REC_TYPE_U.WS_EMPLR_CONT_AMT2 → exp_Convert.WS_EMPLR_CONT_AMT2 → fil_EMP_REC_TYPE_U_EMP_DETAIL.WS_EMPLR_CONT_AMT2 → Norm_EMP_REC_TYPE_U.WS_EMPLR_CONT_AMT2 → EMP_REC_TYPE_U.WS_EMPLR_CONT_AMT2 | EMP_REC_TYPE_U.WS_EMPLR_CONT_AMT2 |
| LES_EMP_DETAIL_RECTYPE_U_TBL | EMPLOYER_CONTR_2_AMT_YTD | exp_Final.EMPLOYER_CONTR_2_AMT_YTD → jnr_LES_NUMBER.WS_EMPLR_CONT_AMT_YTD2 → fil_EMP_REC_TYPE_U.WS_EMPLR_CONT_AMT_YTD2 → exp_Convert.WS_EMPLR_CONT_AMT_YTD2 → fil_EMP_REC_TYPE_U_EMP_DETAIL.WS_EMPLR_CONT_AMT_YTD2 → Norm_EMP_REC_TYPE_U.WS_EMPLR_CONT_AMT_YTD2 → EMP_REC_TYPE_U.WS_EMPLR_CONT_AMT_YTD2 | EMP_REC_TYPE_U.WS_EMPLR_CONT_AMT_YTD2 |

## Mapping `m_LES_Load_LES_EMP_DETAIL_RECTYPE_M_TBL`

- Sessions: `s_LES_Load_LES_EMP_DETAIL_RECTYPE_M_TBL` (#17)
- Sources: `EMP_REC_TYPE_M`, `LES_EMP_DETAIL_TBL`
- Target instances: `LES_EMP_DETAIL_RECTYPE_M_TBL`

### Transformation `Norm_EMP_REC_TYPE_M` (Normalizer)

- **Reset**: `NO`
- **Restart**: `NO`

### Transformation `SQ_LES_EMP_DETAIL_TBL` (Source Qualifier)

- **Source Filter**: `LES_EMP_DETAIL_TBL.PP_END_YEAR = $$MAP_PP_END_YEAR AND LES_EMP_DETAIL_TBL.PP_NUM = $$MAP_PP_NUM`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `fil_EMP_REC_TYPE_M` (Filter)

- **Filter Condition**: `WS_RMK_REC_TYPE = '*M'`

### Transformation `fil_EMP_REC_TYPE_M_EMP_DETAIL` (Filter)

- **Filter Condition**: `WS_RMK_REC_TYPE = '*M' OR WS_RMK_REC_TYPE = '*E'`

### Transformation `jnr_LES_NUMBER` (Joiner)

- **Join Condition**: `LES_NUMBER = EMPM_LES_NUMBER`
- **Join Type**: `Normal Join`
- **Null ordering in master**: `Null Is Highest Value`
- **Null ordering in detail**: `Null Is Highest Value`
- **Sorted Input**: `NO`

- Joiner `jnr_LES_NUMBER`: Normal Join ON `LES_NUMBER = EMPM_LES_NUMBER`
- Normalizer `Norm_EMP_REC_TYPE_M` (vsam=True, source EMP_REC_TYPE_M) occurs: —; generated: —

### Target instance `LES_EMP_DETAIL_RECTYPE_M_TBL` (table `LES_EMP_DETAIL_RECTYPE_M_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LES_EMP_DETAIL_RECTYPE_M_TBL | PP_END_YEAR | exp_Final.PP_END_YEAR → jnr_LES_NUMBER.PP_END_YEAR → SQ_LES_EMP_DETAIL_TBL.PP_END_YEAR → LES_EMP_DETAIL_TBL.PP_END_YEAR | LES_EMP_DETAIL_TBL.PP_END_YEAR |
| LES_EMP_DETAIL_RECTYPE_M_TBL | PP_NUM | exp_Final.PP_NUM → jnr_LES_NUMBER.PP_NUM → SQ_LES_EMP_DETAIL_TBL.PP_NUM → LES_EMP_DETAIL_TBL.PP_NUM | LES_EMP_DETAIL_TBL.PP_NUM |
| LES_EMP_DETAIL_RECTYPE_M_TBL | LES_NUMBER | exp_Final.LES_NUMBER → jnr_LES_NUMBER.EMPM_LES_NUMBER → fil_EMP_REC_TYPE_M.EMPM_LES_NUMBER → exp_Convert.o_EMPM_LES_NUMBER = IIF(IS_NUMBER(v_LES_NUMBER), TO_INTEGER(v_LES_NUMBER) ) → exp_Convert.v_LES_NUMBER = IIF(WS_RMK_REC_TYPE = '*E', SUBSTR(WS_RMK_MSG, 10, 7) , v_LES_NUMBER) → fil_EMP_REC_TYPE_M_EMP_DETAIL.WS_RMK_REC_TYPE → Norm_EMP_REC_TYPE_M.WS_RMK_REC_TYPE → EMP_REC_TYPE_M.WS_RMK_REC_TYPE → fil_EMP_REC_TYPE_M_EMP_DETAIL.WS_RMK_MSG → Norm_EMP_REC_TYPE_M.WS_RMK_MSG → EMP_REC_TYPE_M.WS_RMK_MSG | EMP_REC_TYPE_M.WS_RMK_MSG; EMP_REC_TYPE_M.WS_RMK_REC_TYPE |
| LES_EMP_DETAIL_RECTYPE_M_TBL | PSEUDOSSN | exp_Final.PSEUDOSSN → jnr_LES_NUMBER.PSEUDOSSN → SQ_LES_EMP_DETAIL_TBL.PSEUDOSSN → LES_EMP_DETAIL_TBL.PSEUDOSSN | LES_EMP_DETAIL_TBL.PSEUDOSSN |
| LES_EMP_DETAIL_RECTYPE_M_TBL | REMARK_ID | exp_Final.REMARK_ID → jnr_LES_NUMBER.REMARK_ID → fil_EMP_REC_TYPE_M.REMARK_ID → exp_Convert.o_REMARK_ID = v_REMARK_ID → exp_Convert.v_REMARK_ID = IIF(WS_RMK_REC_TYPE = '*E', 0, v_REMARK_ID + 1) → fil_EMP_REC_TYPE_M_EMP_DETAIL.WS_RMK_REC_TYPE → Norm_EMP_REC_TYPE_M.WS_RMK_REC_TYPE → EMP_REC_TYPE_M.WS_RMK_REC_TYPE | EMP_REC_TYPE_M.WS_RMK_REC_TYPE |
| LES_EMP_DETAIL_RECTYPE_M_TBL | REMARK_TEXT | exp_Final.REMARK_TEXT → jnr_LES_NUMBER.WS_RMK_MSG → fil_EMP_REC_TYPE_M.WS_RMK_MSG → exp_Convert.WS_RMK_MSG → fil_EMP_REC_TYPE_M_EMP_DETAIL.WS_RMK_MSG → Norm_EMP_REC_TYPE_M.WS_RMK_MSG → EMP_REC_TYPE_M.WS_RMK_MSG | EMP_REC_TYPE_M.WS_RMK_MSG |

## Mapping `m_LES_Load_LES_EMP_DETAIL_RECTYPE_T_TBL`

- Sessions: `s_LES_Load_LES_EMP_DETAIL_RECTYPE_T_TBL` (#18)
- Sources: `EMP_REC_TYPE_T`, `LES_EMP_DETAIL_TBL`
- Target instances: `LES_EMP_DETAIL_RECTYPE_T_TBL`

### Transformation `Norm_EMP_REC_TYPE_T` (Normalizer)

- **Reset**: `NO`
- **Restart**: `NO`

### Transformation `SQ_LES_EMP_DETAIL_TBL` (Source Qualifier)

- **Source Filter**: `LES_EMP_DETAIL_TBL.PP_END_YEAR = $$MAP_PP_END_YEAR and LES_EMP_DETAIL_TBL.PP_NUM = $$MAP_PP_NUM`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `fil_EMP_REC_TYPE_T` (Filter)

- **Filter Condition**: `WS_TA_RECORD_TYPE = '*T'`

### Transformation `fil_EMP_REC_TYPE_T_EMP_DETAIL` (Filter)

- **Filter Condition**: `WS_TA_RECORD_TYPE = '*T' OR WS_TA_RECORD_TYPE = '*E'`

### Transformation `jnr_LES_NUMBER` (Joiner)

- **Join Condition**: `LES_NUMBER = EMPT_LES_NUMBER`
- **Join Type**: `Normal Join`
- **Null ordering in master**: `Null Is Highest Value`
- **Null ordering in detail**: `Null Is Highest Value`
- **Sorted Input**: `NO`

- Joiner `jnr_LES_NUMBER`: Normal Join ON `LES_NUMBER = EMPT_LES_NUMBER`
- Normalizer `Norm_EMP_REC_TYPE_T` (vsam=True, source EMP_REC_TYPE_T) occurs: —; generated: —

### Target instance `LES_EMP_DETAIL_RECTYPE_T_TBL` (table `LES_EMP_DETAIL_RECTYPE_T_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LES_EMP_DETAIL_RECTYPE_T_TBL | PP_END_YEAR | exp_Final.PP_END_YEAR → jnr_LES_NUMBER.PP_END_YEAR → SQ_LES_EMP_DETAIL_TBL.PP_END_YEAR → LES_EMP_DETAIL_TBL.PP_END_YEAR | LES_EMP_DETAIL_TBL.PP_END_YEAR |
| LES_EMP_DETAIL_RECTYPE_T_TBL | PP_NUM | exp_Final.PP_NUM → jnr_LES_NUMBER.PP_NUM → SQ_LES_EMP_DETAIL_TBL.PP_NUM → LES_EMP_DETAIL_TBL.PP_NUM | LES_EMP_DETAIL_TBL.PP_NUM |
| LES_EMP_DETAIL_RECTYPE_T_TBL | LES_NUMBER | exp_Final.LES_NUMBER → jnr_LES_NUMBER.EMPT_LES_NUMBER → fil_EMP_REC_TYPE_T.EMPT_LES_NUMBER → exp_Convert.o_EMPT_LES_NUMBER = IIF(IS_NUMBER(v_LES_NUMBER), TO_INTEGER(v_LES_NUMBER) ) → exp_Convert.v_LES_NUMBER = IIF(WS_TA_RECORD_TYPE= '*E', SUBSTR(WS_TA_LV_NAME, 10, 3) \|\| SUBSTR(WS_TA_LV_DATE_TAKEN, 1, 4), v_LES_NUMBER) → fil_EMP_REC_TYPE_T_EMP_DETAIL.WS_TA_RECORD_TYPE → Norm_EMP_REC_TYPE_T.WS_TA_RECORD_TYPE → EMP_REC_TYPE_T.WS_TA_RECORD_TYPE → fil_EMP_REC_TYPE_T_EMP_DETAIL.WS_TA_LV_NAME → Norm_EMP_REC_TYPE_T.WS_TA_LV_NAME → EMP_REC_TYPE_T.WS_TA_LV_NAME → fil_EMP_REC_TYPE_T_EMP_DETAIL.WS_TA_LV_DATE_TAKEN → Norm_EMP_REC_TYPE_T.WS_TA_LV_DATE_TAKEN → EMP_REC_TYPE_T.WS_TA_LV_DATE_TAKEN | EMP_REC_TYPE_T.WS_TA_LV_DATE_TAKEN; EMP_REC_TYPE_T.WS_TA_LV_NAME; EMP_REC_TYPE_T.WS_TA_RECORD_TYPE |
| LES_EMP_DETAIL_RECTYPE_T_TBL | PSEUDOSSN | exp_Final.PSEUDOSSN → jnr_LES_NUMBER.PSEUDOSSN → SQ_LES_EMP_DETAIL_TBL.PSEUDOSSN → LES_EMP_DETAIL_TBL.PSEUDOSSN | LES_EMP_DETAIL_TBL.PSEUDOSSN |
| LES_EMP_DETAIL_RECTYPE_T_TBL | TIME_ATTEND_ID | exp_Final.TIME_ATTEND_ID → jnr_LES_NUMBER.TA_ID → fil_EMP_REC_TYPE_T.TA_ID → exp_Convert.o_TA_ID = v_TA_ID → exp_Convert.v_TA_ID = IIF(WS_TA_RECORD_TYPE = '*E', 0, v_TA_ID + 1) → fil_EMP_REC_TYPE_T_EMP_DETAIL.WS_TA_RECORD_TYPE → Norm_EMP_REC_TYPE_T.WS_TA_RECORD_TYPE → EMP_REC_TYPE_T.WS_TA_RECORD_TYPE | EMP_REC_TYPE_T.WS_TA_RECORD_TYPE |
| LES_EMP_DETAIL_RECTYPE_T_TBL | LEAVE_NAME | exp_Final.LEAVE_NAME → jnr_LES_NUMBER.WS_TA_LV_NAME → fil_EMP_REC_TYPE_T.WS_TA_LV_NAME → exp_Convert.o_WS_TA_LV_NAME = LTRIM(RTRIM(WS_TA_LV_NAME)) → fil_EMP_REC_TYPE_T_EMP_DETAIL.WS_TA_LV_NAME → Norm_EMP_REC_TYPE_T.WS_TA_LV_NAME → EMP_REC_TYPE_T.WS_TA_LV_NAME | EMP_REC_TYPE_T.WS_TA_LV_NAME |
| LES_EMP_DETAIL_RECTYPE_T_TBL | LEAVE_TAKEN_DTE | exp_Final.LEAVE_TAKEN_DTE → jnr_LES_NUMBER.DATE_TAKEN → fil_EMP_REC_TYPE_T.DATE_TAKEN → exp_Convert.o_DATE_TAKEN = IIF(IS_DATE(v_DATE_TAKEN, 'MM/DD/RR'), TO_DATE(v_DATE_TAKEN, 'MM/DD/RR') ) → exp_Convert.v_DATE_TAKEN = SUBSTR(WS_TA_LV_DATE_TAKEN, 1, 2) \|\| '/' \|\| SUBSTR(WS_TA_LV_DATE_TAKEN, 3, 2) \|\| '/' \|\| SUBSTR(WS_TA_LV_DATE_TAKEN, 5, 2) --Convert DATE TAKEN to MM/DD/RR format → fil_EMP_REC_TYPE_T_EMP_DETAIL.WS_TA_LV_DATE_TAKEN → Norm_EMP_REC_TYPE_T.WS_TA_LV_DATE_TAKEN → EMP_REC_TYPE_T.WS_TA_LV_DATE_TAKEN | EMP_REC_TYPE_T.WS_TA_LV_DATE_TAKEN |
| LES_EMP_DETAIL_RECTYPE_T_TBL | LEAVE_HOURS | exp_Final.LEAVE_HOURS → jnr_LES_NUMBER.WS_TA_LV_HOURS → fil_EMP_REC_TYPE_T.WS_TA_LV_HOURS → exp_Convert.WS_TA_LV_HOURS → fil_EMP_REC_TYPE_T_EMP_DETAIL.WS_TA_LV_HOURS → Norm_EMP_REC_TYPE_T.WS_TA_LV_HOURS → EMP_REC_TYPE_T.WS_TA_LV_HOURS | EMP_REC_TYPE_T.WS_TA_LV_HOURS |

## Mapping `m_LES_Load_LES_PRIMARY_DATA_TBL`

- Sessions: `s_LES_Load_LES_PRIMARY_DATA_TBL` (#19)
- Sources: `LES_EMP_DETAIL_RECTYPE_1_TBL`, `LES_EMP_DETAIL_RECTYPE_2_TBL`, `LES_EMP_DETAIL_RECTYPE_3_TBL`, `LES_EMP_DETAIL_RECTYPE_4_TBL`, `LES_EMP_DETAIL_RECTYPE_5_TBL`, `LES_EMP_DETAIL_RECTYPE_6_TBL`, `LES_EMP_DETAIL_TBL`, `LES_HEADER_TBL`
- Target instances: `LES_PRIMARY_DATA_TBL`

### Transformation `SQ_LES_EMP_DETAIL_TBL` (Source Qualifier)

- **Sql Query**: `SELECT le.PP_END_YEAR, le.PP_NUM, lh.PP_END_DTE, le.PSEUDOSSN, le.LES_NUMBER, le.LES_DELIVERY_IND, TRIM(lh.HDR_LOC_ID) HDR_LOC_ID, TRIM(lh.HDR_LOC_NAME) HDR_LOC_NAME, TRIM(lh.SYSTEM_ID) SYSTEM_ID, lh.TRANSMISSION_DTE, r1.PAY_DTE, TRIM(r1.EMPLOYEE_NAME) EMPLOYEE_NAME, TRIM(r1.PAY_PLAN_CD) PAY_PLAN_CD, TRIM(r1.GRADE) GRADE, TRIM(r1.STEP) STEP, r1.HRLY_RATE, r1.BASE_OT_RATE, r1.BASE_PAY, r1.LOCALITY_ADJ, r1.ADJ_BASE_PAY, r1.LOCALITY_PERCENTAGE, r1.FLSA_STATUS, r1.LV_SCD_DTE, r1.MIL_LV_CARRY, r1.LV_YR_END_DTE, r1.LAST_INCREASE_DTE, r2.NET_PAY_FINANCIAL_ORG, r2.ALLOT1_FINANCIAL_ORG, r2.ALLOT2_FINANCIAL_ORG, TRIM(r2.FEDERAL_TAX) FEDERAL_TAX, r2.FED_MARITAL_STATUS, r2.FED_EXCEPTIONS, r2.FED_ADDNL_WITHHOLDING, TRIM(r2.STATE1_TAX) STATE1_TAX, r2.STATE1_MARITAL_STATUS, r2.STATE1_EXCEPTIONS, r2.STATE1_ADDNL_AMOUNT, TRIM(r2.STATE2_TAX) STATE2_TAX, r2.STATE2_MARITAL_STATUS, TRIM(r3.STATE2_EXCEPTIONS) STATE2_EXCEPTIONS, r3.STATE2_ADDNL_AMOUNT, TRIM(r3.LOCAL1_TAX) LOCAL1_TAX, r3.LOCAL1_MARITAL_STATUS, TRIM(r3.LOCAL1_EXCEPTIONS) LOCAL1_EXCEPTIONS, r3.LOCAL1_ADDNL_AMOUNT, TRIM(r3.LOCAL1_TAX_NAME) LOCAL1_TAX_NAME, TRIM(r3.LOCAL2_TAX) LOCAL2_TAX, r3.LOCAL2_MARITAL_STATUS, TRIM(r3.LOCAL2_EXCEPTIONS) LOCAL2_EXCEPTIONS, r3.LOCAL2_ADDNL_AMOUNT, TRIM(r3.LOCAL2_TAX_NAME) LOCAL2_TAX_NAME, TRIM(r3.CSRS) CSRS, r3.CSRS_CUM_AMT, TRIM(r3.BIWEEKLY_AMT) BIWEEKLY_AMT, r3.BIWEEKLY_ANNUITY, TRIM(r3.MILITARY_DEPOSIT) MILITARY_DEPOSIT, r4.MIL_DEPOSIT_PAID, TRIM(r4.MIL_DEPOSIT_2) MIL_DEPOSIT_2, r4.MIL_DEPOSIT_BAL, r4.GROSS_PAY_AMT, r4.GROSS_PAY_AMT_YTD, r4.TAXABLE_WAGE_AMT, r4.TAXABLE_WAGE_AMT_YTD, r4.NONTAXABLE_WAGE_AMT, r4.NONTAXABLE_WAGE_AMT_YTD, r4.TAX_DEFERRED_AMT, r4.TAX_DEFERRED_AMT_YTD, r4.DEDUCTION_AMT, r4.DEDUCTION_AMT_YTD, r5.ADV_ERND_INCOME_CREDIT_AMT, r5.ADV_ERND_INCOME_CREDIT_AMT_YTD, r5.NET_PAY_AMT, r5.NET_PAY_AMT_YTD, TRIM(r5.TSP_SAVINGS) TSP_SAVINGS, r5.TSP_SAVINGS_PCT, TRIM(r5.TITLEG_FUND) TITLEG_FUND, r5.TITLEG_FUND_PCT, TRIM(r5.TITLEF_FUND) TITLEF_FUND, r5.TITLEF_FUND_PCT, TRIM(r5.TITLEC_FUND) TITLEF_FUND, r5.TITLEC_FUND_PCT, TRIM(r5.ROTH_SAVINGS) ROTH_SAVINGS, r5.ROTH_SAVINGS_PCT, TRIM(r6.EARNINGS_FOR_CURR_TSP) EARNINGS_FOR_CURR_TSP, r6.EARNINGS_FOR_CURR_TSP_AMT, TRIM(r6.EARNINGS_FOR_YTD_TSP) EARNINGS_FOR_YTD_TSP, r6.EARNINGS_FOR_YTD_TSP_AMT FROM LES_EMP_DETAIL_TBL le, LES_HEADER_TBL lh, LES_EMP_DETAIL_RECTYPE_1_TBL r1, LES_EMP_DETAIL_RECTYPE_2_TBL r2, LES_EMP_DETAIL_RECTYPE_3_TBL r3, LES_EMP_DETAIL_RECTYPE_4_TBL r4, LES_EMP_DETAIL_RECTYPE_5_TBL r5, LES_EMP_DETAIL_RECTYPE_6_TBL r6 WHERE le.PP_END_YEAR = $$MAP_PP_END_YEAR AND le.PP_NUM = $$MAP_PP_NUM AND ( lh.PP_END_YEAR = $$MAP_PP_END_YEAR AND lh.PP_NUM = $$MAP_PP_NUM AND lh.PP_END_YEAR = le.PP_END_YEAR AND lh.PP_NUM = le.PP_NUM ) AND ( r1.PP_END_YEAR = $$MAP_PP_END_YEAR AND r1.PP_NUM = $$MAP_PP_NUM AND r1.PP_END_YEAR = le.PP_END_YEAR AND r1.PP_NUM = le.PP_NUM AND r1.LES_NUMBER = le.LES_NUMBER AND r1.PSEUDOSSN = le.PSEUDOSSN ) AND ( r2.PP_END_YEAR = $$MAP_PP_END_YEAR AND r2.PP_NUM = $$MAP_PP_NUM AND r2.PP_END_YEAR = le.PP_END_YEAR AND r2.PP_NUM = r2.PP_NUM AND r2.LES_NUMBER = le.LES_NUMBER AND r2.PSEUDOSSN = le.PSEUDOSSN ) AND ( r3.PP_END_YEAR = $$MAP_PP_END_YEAR AND r3.PP_NUM = $$MAP_PP_NUM AND r3.PP_END_YEAR = le.PP_END_YEAR AND r3.PP_NUM = le.PP_NUM AND r3.LES_NUMBER = le.LES_NUMBER AND r3.PSEUDOSSN = le.PSEUDOSSN ) AND ( r4.PP_END_YEAR = $$MAP_PP_END_YEAR AND r4.PP_NUM = $$MAP_PP_NUM AND r4.PP_END_YEAR = le.PP_END_YEAR AND r4.PP_NUM = le.PP_NUM AND r4.LES_NUMBER = le.LES_NUMBER AND r4.PSEUDOSSN = le.PSEUDOSSN ) AND ( r5.PP_END_YEAR = $$MAP_PP_END_YEAR AND r5.PP_NUM = $$MAP_PP_NUM AND r5.PP_END_YEAR = le.PP_END_YEAR AND r5.PP_NUM = le.PP_NUM AND r5.LES_NUMBER = le.LES_NUMBER AND r5.PSEUDOSSN = le.PSEUDOSSN ) AND ( r6.PP_END_YEAR = $$MAP_PP_END_YEAR AND r6.PP_NUM = $$MAP_PP_NUM AND r6.PP_END_YEAR = le.PP_END_YEAR AND r6.PP_NUM = le.PP_NUM AND r6.LES_NUMBER = le.LES_NUMBER AND r6.PSEUDOSSN = le.PSEUDOSSN )`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `lkp_PSEUDOSSN` (Lookup Procedure)

- **Lookup table name**: `PSEUDOSSN_TBL`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `PSEUDOSSN = in_PSEUDOSSN`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `lkp_Pay_Period` (Lookup Procedure)

- **Lookup table name**: `PAY_PERIOD`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `PP_START_DTE <= in_PP_DATE AND PP_END_DTE >= in_PP_DATE`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

- Lookup `lkp_PSEUDOSSN`: table `PSEUDOSSN_TBL` (exists in export: **False**), condition `PSEUDOSSN = in_PSEUDOSSN`, multiple-match policy `Use Any Value`.
- Lookup `lkp_Pay_Period`: table `PAY_PERIOD` (exists in export: **True**), condition `PP_START_DTE <= in_PP_DATE AND PP_END_DTE >= in_PP_DATE`, multiple-match policy `Use Any Value`.
- SQL override `SQ_LES_EMP_DETAIL_TBL` positional bindings: 1 → `PP_END_YEAR` = `le.PP_END_YEAR`; 2 → `PP_NUM` = `le.PP_NUM`; 3 → `PP_END_DTE` = `lh.PP_END_DTE`; 4 → `PSEUDOSSN` = `le.PSEUDOSSN`; 5 → `LES_NUMBER` = `le.LES_NUMBER`; 6 → `LES_DELIVERY_IND` = `le.LES_DELIVERY_IND`; 7 → `PP_END_DTE1` = `TRIM(lh.HDR_LOC_ID) HDR_LOC_ID`; 8 → `HDR_LOC_ID` = `TRIM(lh.HDR_LOC_NAME) HDR_LOC_NAME`; 9 → `HDR_LOC_NAME` = `TRIM(lh.SYSTEM_ID) SYSTEM_ID`; 10 → `SYSTEM_ID` = `lh.TRANSMISSION_DTE`; 11 → `TRANSMISSION_DTE` = `r1.PAY_DTE`; 12 → `PP_END_DTE2` = `TRIM(r1.EMPLOYEE_NAME) EMPLOYEE_NAME`; 13 → `LES_NUMBER1` = `TRIM(r1.PAY_PLAN_CD) PAY_PLAN_CD`; 14 → `PSEUDOSSN1` = `TRIM(r1.GRADE) GRADE`; 15 → `PAY_DTE` = `TRIM(r1.STEP) STEP`; 16 → `EMPLOYEE_NAME` = `r1.HRLY_RATE`; 17 → `PAY_PLAN_CD` = `r1.BASE_OT_RATE`; 18 → `GRADE` = `r1.BASE_PAY`; 19 → `STEP` = `r1.LOCALITY_ADJ`; 20 → `HRLY_RATE` = `r1.ADJ_BASE_PAY`; 21 → `BASE_OT_RATE` = `r1.LOCALITY_PERCENTAGE`; 22 → `BASE_PAY` = `r1.FLSA_STATUS`; 23 → `LOCALITY_ADJ` = `r1.LV_SCD_DTE`; 24 → `ADJ_BASE_PAY` = `r1.MIL_LV_CARRY`; 25 → `LOCALITY_PERCENTAGE` = `r1.LV_YR_END_DTE`; 26 → `FLSA_STATUS` = `r1.LAST_INCREASE_DTE`; 27 → `LV_SCD_DTE` = `r2.NET_PAY_FINANCIAL_ORG`; 28 → `MIL_LV_CARRY` = `r2.ALLOT1_FINANCIAL_ORG`; 29 → `LV_YR_END_DTE` = `r2.ALLOT2_FINANCIAL_ORG`; 30 → `LAST_INCREASE_DTE` = `TRIM(r2.FEDERAL_TAX) FEDERAL_TAX`; 31 → `PP_END_DTE3` = `r2.FED_MARITAL_STATUS`; 32 → `LES_NUMBER2` = `r2.FED_EXCEPTIONS`; 33 → `PSEUDOSSN2` = `r2.FED_ADDNL_WITHHOLDING`; 34 → `NET_PAY_FINANCIAL_ORG` = `TRIM(r2.STATE1_TAX) STATE1_TAX`; 35 → `ALLOT1_FINANCIAL_ORG` = `r2.STATE1_MARITAL_STATUS`; 36 → `ALLOT2_FINANCIAL_ORG` = `r2.STATE1_EXCEPTIONS`; 37 → `FEDERAL_TAX` = `r2.STATE1_ADDNL_AMOUNT`; 38 → `FED_MARITAL_STATUS` = `TRIM(r2.STATE2_TAX) STATE2_TAX`; 39 → `FED_EXCEPTIONS` = `r2.STATE2_MARITAL_STATUS`; 40 → `FED_ADDNL_WITHHOLDING` = `TRIM(r3.STATE2_EXCEPTIONS) STATE2_EXCEPTIONS`; 41 → `STATE1_TAX` = `r3.STATE2_ADDNL_AMOUNT`; 42 → `STATE1_MARITAL_STATUS` = `TRIM(r3.LOCAL1_TAX) LOCAL1_TAX`; 43 → `STATE1_EXCEPTIONS` = `r3.LOCAL1_MARITAL_STATUS`; 44 → `STATE1_ADDNL_AMOUNT` = `TRIM(r3.LOCAL1_EXCEPTIONS) LOCAL1_EXCEPTIONS`; 45 → `STATE2_TAX` = `r3.LOCAL1_ADDNL_AMOUNT`; 46 → `STATE2_MARITAL_STATUS` = `TRIM(r3.LOCAL1_TAX_NAME) LOCAL1_TAX_NAME`; 47 → `PP_END_DTE4` = `TRIM(r3.LOCAL2_TAX) LOCAL2_TAX`; 48 → `LES_NUMBER3` = `r3.LOCAL2_MARITAL_STATUS`; 49 → `PSEUDOSSN3` = `TRIM(r3.LOCAL2_EXCEPTIONS) LOCAL2_EXCEPTIONS`; 50 → `STATE2_EXCEPTIONS` = `r3.LOCAL2_ADDNL_AMOUNT`; 51 → `STATE2_ADDNL_AMOUNT` = `TRIM(r3.LOCAL2_TAX_NAME) LOCAL2_TAX_NAME`; 52 → `LOCAL1_TAX` = `TRIM(r3.CSRS) CSRS`; 53 → `LOCAL1_MARITAL_STATUS` = `r3.CSRS_CUM_AMT`; 54 → `LOCAL1_EXCEPTIONS` = `TRIM(r3.BIWEEKLY_AMT) BIWEEKLY_AMT`; 55 → `LOCAL1_ADDNL_AMOUNT` = `r3.BIWEEKLY_ANNUITY`; 56 → `LOCAL1_TAX_NAME` = `TRIM(r3.MILITARY_DEPOSIT) MILITARY_DEPOSIT`; 57 → `LOCAL2_TAX` = `r4.MIL_DEPOSIT_PAID`; 58 → `LOCAL2_MARITAL_STATUS` = `TRIM(r4.MIL_DEPOSIT_2) MIL_DEPOSIT_2`; 59 → `LOCAL2_EXCEPTIONS` = `r4.MIL_DEPOSIT_BAL`; 60 → `LOCAL2_ADDNL_AMOUNT` = `r4.GROSS_PAY_AMT`; 61 → `LOCAL2_TAX_NAME` = `r4.GROSS_PAY_AMT_YTD`; 62 → `CSRS` = `r4.TAXABLE_WAGE_AMT`; 63 → `CSRS_CUM_AMT` = `r4.TAXABLE_WAGE_AMT_YTD`; 64 → `BIWEEKLY_AMT` = `r4.NONTAXABLE_WAGE_AMT`; 65 → `BIWEEKLY_ANNUITY` = `r4.NONTAXABLE_WAGE_AMT_YTD`; 66 → `MILITARY_DEPOSIT` = `r4.TAX_DEFERRED_AMT`; 67 → `PP_END_DTE5` = `r4.TAX_DEFERRED_AMT_YTD`; 68 → `LES_NUMBER4` = `r4.DEDUCTION_AMT`; 69 → `PSEUDOSSN4` = `r4.DEDUCTION_AMT_YTD`; 70 → `MIL_DEPOSIT_PAID` = `r5.ADV_ERND_INCOME_CREDIT_AMT`; 71 → `MIL_DEPOSIT_2` = `r5.ADV_ERND_INCOME_CREDIT_AMT_YTD`; 72 → `MIL_DEPOSIT_BAL` = `r5.NET_PAY_AMT`; 73 → `GROSS_PAY_AMT` = `r5.NET_PAY_AMT_YTD`; 74 → `GROSS_PAY_AMT_YTD` = `TRIM(r5.TSP_SAVINGS) TSP_SAVINGS`; 75 → `TAXABLE_WAGE_AMT` = `r5.TSP_SAVINGS_PCT`; 76 → `TAXABLE_WAGE_AMT_YTD` = `TRIM(r5.TITLEG_FUND) TITLEG_FUND`; 77 → `NONTAXABLE_WAGE_AMT` = `r5.TITLEG_FUND_PCT`; 78 → `NONTAXABLE_WAGE_AMT_YTD` = `TRIM(r5.TITLEF_FUND) TITLEF_FUND`; 79 → `TAX_DEFERRED_AMT` = `r5.TITLEF_FUND_PCT`; 80 → `TAX_DEFERRED_AMT_YTD` = `TRIM(r5.TITLEC_FUND) TITLEF_FUND`; 81 → `DEDUCTION_AMT` = `r5.TITLEC_FUND_PCT`; 82 → `DEDUCTION_AMT_YTD` = `TRIM(r5.ROTH_SAVINGS) ROTH_SAVINGS`; 83 → `PP_END_DTE6` = `r5.ROTH_SAVINGS_PCT`; 84 → `LES_NUMBER5` = `TRIM(r6.EARNINGS_FOR_CURR_TSP) EARNINGS_FOR_CURR_TSP`; 85 → `PSEUDOSSN5` = `r6.EARNINGS_FOR_CURR_TSP_AMT`; 86 → `ADV_ERND_INCOME_CREDIT_AMT` = `TRIM(r6.EARNINGS_FOR_YTD_TSP) EARNINGS_FOR_YTD_TSP`; 87 → `ADV_ERND_INCOME_CREDIT_AMT_YTD` = `r6.EARNINGS_FOR_YTD_TSP_AMT`

### Target instance `LES_PRIMARY_DATA_TBL` (table `LES_PRIMARY_DATA_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LES_PRIMARY_DATA_TBL | PP_END_YEAR | exp_Final.PP_END_YEAR → exp_Stage.PP_END_YEAR → exp_Initial.PP_END_YEAR → SQ_LES_EMP_DETAIL_TBL.PP_END_YEAR → LES_EMP_DETAIL_TBL.PP_END_YEAR | LES_EMP_DETAIL_TBL.PP_END_YEAR |
| LES_PRIMARY_DATA_TBL | PP_NUM | exp_Final.PP_NUM → exp_Stage.PP_NUM → exp_Initial.PP_NUM → SQ_LES_EMP_DETAIL_TBL.PP_NUM → LES_EMP_DETAIL_TBL.PP_NUM | LES_EMP_DETAIL_TBL.PP_NUM |
| LES_PRIMARY_DATA_TBL | LES_NUMBER | exp_Final.LES_NUMBER → exp_Stage.LES_NUMBER → exp_Initial.LES_NUMBER → SQ_LES_EMP_DETAIL_TBL.LES_NUMBER → LES_EMP_DETAIL_TBL.LES_NUMBER | LES_EMP_DETAIL_TBL.LES_NUMBER |
| LES_PRIMARY_DATA_TBL | PSEUDOSSN | exp_Final.PSEUDOSSN → exp_Stage.PSEUDOSSN → exp_Initial.PSEUDOSSN → SQ_LES_EMP_DETAIL_TBL.PSEUDOSSN → LES_EMP_DETAIL_TBL.PSEUDOSSN | LES_EMP_DETAIL_TBL.PSEUDOSSN |
| LES_PRIMARY_DATA_TBL | PP_END_DTE | exp_Final.PP_END_DTE → exp_Stage.PP_END_DTE → exp_Initial.PP_END_DTE → SQ_LES_EMP_DETAIL_TBL.PP_END_DTE → LES_HEADER_TBL.PP_END_DTE | LES_HEADER_TBL.PP_END_DTE |
| LES_PRIMARY_DATA_TBL | HDR_LOC_ID | exp_Final.HDR_LOC_ID → exp_Stage.HDR_LOC_ID → exp_Initial.HDR_LOC_ID → SQ_LES_EMP_DETAIL_TBL.HDR_LOC_ID → LES_HEADER_TBL.HDR_LOC_ID | LES_HEADER_TBL.HDR_LOC_ID |
| LES_PRIMARY_DATA_TBL | HDR_LOC_NAME | exp_Final.HDR_LOC_NAME → exp_Stage.HDR_LOC_NAME → exp_Initial.HDR_LOC_NAME → SQ_LES_EMP_DETAIL_TBL.HDR_LOC_NAME → LES_HEADER_TBL.HDR_LOC_NAME | LES_HEADER_TBL.HDR_LOC_NAME |
| LES_PRIMARY_DATA_TBL | SYSTEM_ID | exp_Final.SYSTEM_ID → exp_Stage.SYSTEM_ID → exp_Initial.SYSTEM_ID → SQ_LES_EMP_DETAIL_TBL.SYSTEM_ID → LES_HEADER_TBL.SYSTEM_ID | LES_HEADER_TBL.SYSTEM_ID |
| LES_PRIMARY_DATA_TBL | TRANSMISSION_DTE | exp_Final.TRANSMISSION_DTE → exp_Stage.TRANSMISSION_DTE → exp_Initial.TRANSMISSION_DTE → SQ_LES_EMP_DETAIL_TBL.TRANSMISSION_DTE → LES_HEADER_TBL.TRANSMISSION_DTE | LES_HEADER_TBL.TRANSMISSION_DTE |
| LES_PRIMARY_DATA_TBL | SSN | exp_Final.SSN → exp_Stage.o_SSN = IIF(ISNULL(lkp_SSN), PSEUDOSSN, lkp_SSN) → lkp_PSEUDOSSN.SSN [lookup PSEUDOSSN_TBL.SSN ON PSEUDOSSN = in_PSEUDOSSN] → exp_Initial.PSEUDOSSN → SQ_LES_EMP_DETAIL_TBL.PSEUDOSSN → LES_EMP_DETAIL_TBL.PSEUDOSSN | LES_EMP_DETAIL_TBL.PSEUDOSSN; LES_EMP_DETAIL_TBL.PSEUDOSSN (lookup key); PSEUDOSSN_TBL.SSN (lookup) |
| LES_PRIMARY_DATA_TBL | EMPLID | exp_Final.EMPLID → exp_Stage.lkp_EMPLID → lkp_PSEUDOSSN.EMPLID [lookup PSEUDOSSN_TBL.EMPLID ON PSEUDOSSN = in_PSEUDOSSN] | LES_EMP_DETAIL_TBL.PSEUDOSSN (lookup key); PSEUDOSSN_TBL.EMPLID (lookup) |
| LES_PRIMARY_DATA_TBL | TK_NUM | exp_Final.TK_NUM → exp_Stage.lkp_TK_NUM → lkp_PSEUDOSSN.TK_NUM [lookup PSEUDOSSN_TBL.TK_NUM ON PSEUDOSSN = in_PSEUDOSSN] | LES_EMP_DETAIL_TBL.PSEUDOSSN (lookup key); PSEUDOSSN_TBL.TK_NUM (lookup) |
| LES_PRIMARY_DATA_TBL | LES_DELIVERY_IND | exp_Final.LES_DELIVERY_IND → exp_Stage.LES_DELIVERY_IND → exp_Initial.LES_DELIVERY_IND → SQ_LES_EMP_DETAIL_TBL.LES_DELIVERY_IND → LES_EMP_DETAIL_TBL.LES_DELIVERY_IND | LES_EMP_DETAIL_TBL.LES_DELIVERY_IND |
| LES_PRIMARY_DATA_TBL | PAY_DTE | exp_Final.PAY_DTE → exp_Stage.PAY_DTE → exp_Initial.PAY_DTE → SQ_LES_EMP_DETAIL_TBL.PAY_DTE → LES_EMP_DETAIL_RECTYPE_1_TBL.PAY_DTE | LES_EMP_DETAIL_RECTYPE_1_TBL.PAY_DTE |
| LES_PRIMARY_DATA_TBL | EMPLOYEE_NAME | exp_Final.EMPLOYEE_NAME → exp_Stage.EMPLOYEE_NAME → exp_Initial.EMPLOYEE_NAME → SQ_LES_EMP_DETAIL_TBL.EMPLOYEE_NAME → LES_EMP_DETAIL_RECTYPE_1_TBL.EMPLOYEE_NAME | LES_EMP_DETAIL_RECTYPE_1_TBL.EMPLOYEE_NAME |
| LES_PRIMARY_DATA_TBL | PAY_PLAN_CD | exp_Final.PAY_PLAN_CD → exp_Stage.PAY_PLAN_CD → exp_Initial.PAY_PLAN_CD → SQ_LES_EMP_DETAIL_TBL.PAY_PLAN_CD → LES_EMP_DETAIL_RECTYPE_1_TBL.PAY_PLAN_CD | LES_EMP_DETAIL_RECTYPE_1_TBL.PAY_PLAN_CD |
| LES_PRIMARY_DATA_TBL | GRADE | exp_Final.GRADE → exp_Stage.GRADE → exp_Initial.GRADE → SQ_LES_EMP_DETAIL_TBL.GRADE → LES_EMP_DETAIL_RECTYPE_1_TBL.GRADE | LES_EMP_DETAIL_RECTYPE_1_TBL.GRADE |
| LES_PRIMARY_DATA_TBL | STEP | exp_Final.STEP → exp_Stage.STEP → exp_Initial.STEP → SQ_LES_EMP_DETAIL_TBL.STEP → LES_EMP_DETAIL_RECTYPE_1_TBL.STEP | LES_EMP_DETAIL_RECTYPE_1_TBL.STEP |
| LES_PRIMARY_DATA_TBL | HRLY_RATE | exp_Final.HRLY_RATE → exp_Stage.HRLY_RATE → exp_Initial.HRLY_RATE → SQ_LES_EMP_DETAIL_TBL.HRLY_RATE → LES_EMP_DETAIL_RECTYPE_1_TBL.HRLY_RATE | LES_EMP_DETAIL_RECTYPE_1_TBL.HRLY_RATE |
| LES_PRIMARY_DATA_TBL | BASE_OT_RATE | exp_Final.BASE_OT_RATE → exp_Stage.BASE_OT_RATE → exp_Initial.BASE_OT_RATE → SQ_LES_EMP_DETAIL_TBL.BASE_OT_RATE → LES_EMP_DETAIL_RECTYPE_1_TBL.BASE_OT_RATE | LES_EMP_DETAIL_RECTYPE_1_TBL.BASE_OT_RATE |
| LES_PRIMARY_DATA_TBL | BASE_PAY | exp_Final.BASE_PAY → exp_Stage.BASE_PAY → exp_Initial.BASE_PAY → SQ_LES_EMP_DETAIL_TBL.BASE_PAY → LES_EMP_DETAIL_RECTYPE_1_TBL.BASE_PAY | LES_EMP_DETAIL_RECTYPE_1_TBL.BASE_PAY |
| LES_PRIMARY_DATA_TBL | LOCALITY_ADJ | exp_Final.LOCALITY_ADJ → exp_Stage.LOCALITY_ADJ → exp_Initial.LOCALITY_ADJ → SQ_LES_EMP_DETAIL_TBL.LOCALITY_ADJ → LES_EMP_DETAIL_RECTYPE_1_TBL.LOCALITY_ADJ | LES_EMP_DETAIL_RECTYPE_1_TBL.LOCALITY_ADJ |
| LES_PRIMARY_DATA_TBL | ADJ_BASE_PAY | exp_Final.ADJ_BASE_PAY → exp_Stage.ADJ_BASE_PAY → exp_Initial.ADJ_BASE_PAY → SQ_LES_EMP_DETAIL_TBL.ADJ_BASE_PAY → LES_EMP_DETAIL_RECTYPE_1_TBL.ADJ_BASE_PAY | LES_EMP_DETAIL_RECTYPE_1_TBL.ADJ_BASE_PAY |
| LES_PRIMARY_DATA_TBL | LOCALITY_PERCENTAGE | exp_Final.LOCALITY_PERCENTAGE → exp_Stage.LOCALITY_PERCENTAGE → exp_Initial.LOCALITY_PERCENTAGE → SQ_LES_EMP_DETAIL_TBL.LOCALITY_PERCENTAGE → LES_EMP_DETAIL_RECTYPE_1_TBL.LOCALITY_PERCENTAGE | LES_EMP_DETAIL_RECTYPE_1_TBL.LOCALITY_PERCENTAGE |
| LES_PRIMARY_DATA_TBL | FLSA_STATUS | exp_Final.FLSA_STATUS → exp_Stage.FLSA_STATUS → exp_Initial.FLSA_STATUS → SQ_LES_EMP_DETAIL_TBL.FLSA_STATUS → LES_EMP_DETAIL_RECTYPE_1_TBL.FLSA_STATUS | LES_EMP_DETAIL_RECTYPE_1_TBL.FLSA_STATUS |
| LES_PRIMARY_DATA_TBL | LV_SCD_DTE | exp_Final.LV_SCD_DTE → exp_Stage.LV_SCD_DTE → exp_Initial.LV_SCD_DTE → SQ_LES_EMP_DETAIL_TBL.LV_SCD_DTE → LES_EMP_DETAIL_RECTYPE_1_TBL.LV_SCD_DTE | LES_EMP_DETAIL_RECTYPE_1_TBL.LV_SCD_DTE |
| LES_PRIMARY_DATA_TBL | MIL_LV_CARRY | exp_Final.MIL_LV_CARRY → exp_Stage.MIL_LV_CARRY → exp_Initial.MIL_LV_CARRY → SQ_LES_EMP_DETAIL_TBL.MIL_LV_CARRY → LES_EMP_DETAIL_RECTYPE_1_TBL.MIL_LV_CARRY | LES_EMP_DETAIL_RECTYPE_1_TBL.MIL_LV_CARRY |
| LES_PRIMARY_DATA_TBL | LV_YR_END_DTE | exp_Final.LV_YR_END_DTE → exp_Stage.LV_YR_END_DTE → exp_Initial.LV_YR_END_DTE → SQ_LES_EMP_DETAIL_TBL.LV_YR_END_DTE → LES_EMP_DETAIL_RECTYPE_1_TBL.LV_YR_END_DTE | LES_EMP_DETAIL_RECTYPE_1_TBL.LV_YR_END_DTE |
| LES_PRIMARY_DATA_TBL | LAST_INCREASE_DTE | exp_Final.LAST_INCREASE_DTE → exp_Stage.LAST_INCREASE_DTE → exp_Initial.LAST_INCREASE_DTE → SQ_LES_EMP_DETAIL_TBL.LAST_INCREASE_DTE → LES_EMP_DETAIL_RECTYPE_1_TBL.LAST_INCREASE_DTE | LES_EMP_DETAIL_RECTYPE_1_TBL.LAST_INCREASE_DTE |
| LES_PRIMARY_DATA_TBL | NET_PAY_FINANCIAL_ORG | exp_Final.NET_PAY_FINANCIAL_ORG → exp_Stage.NET_PAY_FINANCIAL_ORG → exp_Initial.NET_PAY_FINANCIAL_ORG → SQ_LES_EMP_DETAIL_TBL.NET_PAY_FINANCIAL_ORG → LES_EMP_DETAIL_RECTYPE_2_TBL.NET_PAY_FINANCIAL_ORG | LES_EMP_DETAIL_RECTYPE_2_TBL.NET_PAY_FINANCIAL_ORG |
| LES_PRIMARY_DATA_TBL | ALLOT1_FINANCIAL_ORG | exp_Final.ALLOT1_FINANCIAL_ORG → exp_Stage.ALLOT1_FINANCIAL_ORG → exp_Initial.ALLOT1_FINANCIAL_ORG → SQ_LES_EMP_DETAIL_TBL.ALLOT1_FINANCIAL_ORG → LES_EMP_DETAIL_RECTYPE_2_TBL.ALLOT1_FINANCIAL_ORG | LES_EMP_DETAIL_RECTYPE_2_TBL.ALLOT1_FINANCIAL_ORG |
| LES_PRIMARY_DATA_TBL | ALLOT2_FINANCIAL_ORG | exp_Final.ALLOT2_FINANCIAL_ORG → exp_Stage.ALLOT2_FINANCIAL_ORG → exp_Initial.ALLOT2_FINANCIAL_ORG → SQ_LES_EMP_DETAIL_TBL.ALLOT2_FINANCIAL_ORG → LES_EMP_DETAIL_RECTYPE_2_TBL.ALLOT2_FINANCIAL_ORG | LES_EMP_DETAIL_RECTYPE_2_TBL.ALLOT2_FINANCIAL_ORG |
| LES_PRIMARY_DATA_TBL | FEDERAL_TAX | exp_Final.FEDERAL_TAX → exp_Stage.FEDERAL_TAX → exp_Initial.FEDERAL_TAX → SQ_LES_EMP_DETAIL_TBL.FEDERAL_TAX → LES_EMP_DETAIL_RECTYPE_2_TBL.FEDERAL_TAX | LES_EMP_DETAIL_RECTYPE_2_TBL.FEDERAL_TAX |
| LES_PRIMARY_DATA_TBL | FED_MARITAL_STATUS | exp_Final.FED_MARITAL_STATUS → exp_Stage.FED_MARITAL_STATUS → exp_Initial.FED_MARITAL_STATUS → SQ_LES_EMP_DETAIL_TBL.FED_MARITAL_STATUS → LES_EMP_DETAIL_RECTYPE_2_TBL.FED_MARITAL_STATUS | LES_EMP_DETAIL_RECTYPE_2_TBL.FED_MARITAL_STATUS |
| LES_PRIMARY_DATA_TBL | FED_EXCEPTIONS | exp_Final.FED_EXCEPTIONS → exp_Stage.FED_EXCEPTIONS → exp_Initial.FED_EXCEPTIONS → SQ_LES_EMP_DETAIL_TBL.FED_EXCEPTIONS → LES_EMP_DETAIL_RECTYPE_2_TBL.FED_EXCEPTIONS | LES_EMP_DETAIL_RECTYPE_2_TBL.FED_EXCEPTIONS |
| LES_PRIMARY_DATA_TBL | FED_ADDNL_WITHHOLDING | exp_Final.FED_ADDNL_WITHHOLDING → exp_Stage.FED_ADDNL_WITHHOLDING → exp_Initial.FED_ADDNL_WITHHOLDING → SQ_LES_EMP_DETAIL_TBL.FED_ADDNL_WITHHOLDING → LES_EMP_DETAIL_RECTYPE_2_TBL.FED_ADDNL_WITHHOLDING | LES_EMP_DETAIL_RECTYPE_2_TBL.FED_ADDNL_WITHHOLDING |
| LES_PRIMARY_DATA_TBL | STATE1_TAX | exp_Final.STATE1_TAX → exp_Stage.STATE1_TAX → exp_Initial.STATE1_TAX → SQ_LES_EMP_DETAIL_TBL.STATE1_TAX → LES_EMP_DETAIL_RECTYPE_2_TBL.STATE1_TAX | LES_EMP_DETAIL_RECTYPE_2_TBL.STATE1_TAX |
| LES_PRIMARY_DATA_TBL | STATE1_MARITAL_STATUS | exp_Final.STATE1_MARITAL_STATUS → exp_Stage.STATE1_MARITAL_STATUS → exp_Initial.STATE1_MARITAL_STATUS → SQ_LES_EMP_DETAIL_TBL.STATE1_MARITAL_STATUS → LES_EMP_DETAIL_RECTYPE_2_TBL.STATE1_MARITAL_STATUS | LES_EMP_DETAIL_RECTYPE_2_TBL.STATE1_MARITAL_STATUS |
| LES_PRIMARY_DATA_TBL | STATE1_EXCEPTIONS | exp_Final.STATE1_EXCEPTIONS → exp_Stage.STATE1_EXCEPTIONS → exp_Initial.STATE1_EXCEPTIONS → SQ_LES_EMP_DETAIL_TBL.STATE1_EXCEPTIONS → LES_EMP_DETAIL_RECTYPE_2_TBL.STATE1_EXCEPTIONS | LES_EMP_DETAIL_RECTYPE_2_TBL.STATE1_EXCEPTIONS |
| LES_PRIMARY_DATA_TBL | STATE1_ADDNL_AMOUNT | exp_Final.STATE1_ADDNL_AMOUNT → exp_Stage.STATE1_ADDNL_AMOUNT → exp_Initial.STATE1_ADDNL_AMOUNT → SQ_LES_EMP_DETAIL_TBL.STATE1_ADDNL_AMOUNT → LES_EMP_DETAIL_RECTYPE_2_TBL.STATE1_ADDNL_AMOUNT | LES_EMP_DETAIL_RECTYPE_2_TBL.STATE1_ADDNL_AMOUNT |
| LES_PRIMARY_DATA_TBL | STATE2_TAX | exp_Final.STATE2_TAX → exp_Stage.STATE2_TAX → exp_Initial.STATE2_TAX → SQ_LES_EMP_DETAIL_TBL.STATE2_TAX → LES_EMP_DETAIL_RECTYPE_2_TBL.STATE2_TAX | LES_EMP_DETAIL_RECTYPE_2_TBL.STATE2_TAX |
| LES_PRIMARY_DATA_TBL | STATE2_MARITAL_STATUS | exp_Final.STATE2_MARITAL_STATUS → exp_Stage.STATE2_MARITAL_STATUS → exp_Initial.STATE2_MARITAL_STATUS → SQ_LES_EMP_DETAIL_TBL.STATE2_MARITAL_STATUS → LES_EMP_DETAIL_RECTYPE_2_TBL.STATE2_MARITAL_STATUS | LES_EMP_DETAIL_RECTYPE_2_TBL.STATE2_MARITAL_STATUS |
| LES_PRIMARY_DATA_TBL | STATE2_EXCEPTIONS | exp_Final.STATE2_EXCEPTIONS → exp_Stage.STATE2_EXCEPTIONS → exp_Initial.STATE2_EXCEPTIONS → SQ_LES_EMP_DETAIL_TBL.STATE2_EXCEPTIONS → LES_EMP_DETAIL_RECTYPE_3_TBL.STATE2_EXCEPTIONS | LES_EMP_DETAIL_RECTYPE_3_TBL.STATE2_EXCEPTIONS |
| LES_PRIMARY_DATA_TBL | STATE2_ADDNL_AMOUNT | exp_Final.STATE2_ADDNL_AMOUNT → exp_Stage.STATE2_ADDNL_AMOUNT → exp_Initial.STATE2_ADDNL_AMOUNT → SQ_LES_EMP_DETAIL_TBL.STATE2_ADDNL_AMOUNT → LES_EMP_DETAIL_RECTYPE_3_TBL.STATE2_ADDNL_AMOUNT | LES_EMP_DETAIL_RECTYPE_3_TBL.STATE2_ADDNL_AMOUNT |
| LES_PRIMARY_DATA_TBL | LOCAL1_TAX | exp_Final.LOCAL1_TAX → exp_Stage.LOCAL1_TAX → exp_Initial.LOCAL1_TAX → SQ_LES_EMP_DETAIL_TBL.LOCAL1_TAX → LES_EMP_DETAIL_RECTYPE_3_TBL.LOCAL1_TAX | LES_EMP_DETAIL_RECTYPE_3_TBL.LOCAL1_TAX |
| LES_PRIMARY_DATA_TBL | LOCAL1_MARITAL_STATUS | exp_Final.LOCAL1_MARITAL_STATUS → exp_Stage.LOCAL1_MARITAL_STATUS → exp_Initial.LOCAL1_MARITAL_STATUS → SQ_LES_EMP_DETAIL_TBL.LOCAL1_MARITAL_STATUS → LES_EMP_DETAIL_RECTYPE_3_TBL.LOCAL1_MARITAL_STATUS | LES_EMP_DETAIL_RECTYPE_3_TBL.LOCAL1_MARITAL_STATUS |
| LES_PRIMARY_DATA_TBL | LOCAL1_EXCEPTIONS | exp_Final.LOCAL1_EXCEPTIONS → exp_Stage.LOCAL1_EXCEPTIONS → exp_Initial.LOCAL1_EXCEPTIONS → SQ_LES_EMP_DETAIL_TBL.LOCAL1_EXCEPTIONS → LES_EMP_DETAIL_RECTYPE_3_TBL.LOCAL1_EXCEPTIONS | LES_EMP_DETAIL_RECTYPE_3_TBL.LOCAL1_EXCEPTIONS |
| LES_PRIMARY_DATA_TBL | LOCAL1_ADDNL_AMOUNT | exp_Final.LOCAL1_ADDNL_AMOUNT → exp_Stage.LOCAL1_ADDNL_AMOUNT → exp_Initial.LOCAL1_ADDNL_AMOUNT → SQ_LES_EMP_DETAIL_TBL.LOCAL1_ADDNL_AMOUNT → LES_EMP_DETAIL_RECTYPE_3_TBL.LOCAL1_ADDNL_AMOUNT | LES_EMP_DETAIL_RECTYPE_3_TBL.LOCAL1_ADDNL_AMOUNT |
| LES_PRIMARY_DATA_TBL | LOCAL1_TAX_NAME | exp_Final.LOCAL1_TAX_NAME → exp_Stage.LOCAL1_TAX_NAME → exp_Initial.LOCAL1_TAX_NAME → SQ_LES_EMP_DETAIL_TBL.LOCAL1_TAX_NAME → LES_EMP_DETAIL_RECTYPE_3_TBL.LOCAL1_TAX_NAME | LES_EMP_DETAIL_RECTYPE_3_TBL.LOCAL1_TAX_NAME |
| LES_PRIMARY_DATA_TBL | LOCAL2_TAX | exp_Final.LOCAL2_TAX → exp_Stage.LOCAL2_TAX → exp_Initial.LOCAL2_TAX → SQ_LES_EMP_DETAIL_TBL.LOCAL2_TAX → LES_EMP_DETAIL_RECTYPE_3_TBL.LOCAL2_TAX | LES_EMP_DETAIL_RECTYPE_3_TBL.LOCAL2_TAX |
| LES_PRIMARY_DATA_TBL | LOCAL2_MARITAL_STATUS | exp_Final.LOCAL2_MARITAL_STATUS → exp_Stage.LOCAL2_MARITAL_STATUS → exp_Initial.LOCAL2_MARITAL_STATUS → SQ_LES_EMP_DETAIL_TBL.LOCAL2_MARITAL_STATUS → LES_EMP_DETAIL_RECTYPE_3_TBL.LOCAL2_MARITAL_STATUS | LES_EMP_DETAIL_RECTYPE_3_TBL.LOCAL2_MARITAL_STATUS |
| LES_PRIMARY_DATA_TBL | LOCAL2_EXCEPTIONS | exp_Final.LOCAL2_EXCEPTIONS → exp_Stage.LOCAL2_EXCEPTIONS → exp_Initial.LOCAL2_EXCEPTIONS → SQ_LES_EMP_DETAIL_TBL.LOCAL2_EXCEPTIONS → LES_EMP_DETAIL_RECTYPE_3_TBL.LOCAL2_EXCEPTIONS | LES_EMP_DETAIL_RECTYPE_3_TBL.LOCAL2_EXCEPTIONS |
| LES_PRIMARY_DATA_TBL | LOCAL2_ADDNL_AMOUNT | exp_Final.LOCAL2_ADDNL_AMOUNT → exp_Stage.LOCAL2_ADDNL_AMOUNT → exp_Initial.LOCAL2_ADDNL_AMOUNT → SQ_LES_EMP_DETAIL_TBL.LOCAL2_ADDNL_AMOUNT → LES_EMP_DETAIL_RECTYPE_3_TBL.LOCAL2_ADDNL_AMOUNT | LES_EMP_DETAIL_RECTYPE_3_TBL.LOCAL2_ADDNL_AMOUNT |
| LES_PRIMARY_DATA_TBL | LOCAL2_TAX_NAME | exp_Final.LOCAL2_TAX_NAME → exp_Stage.LOCAL2_TAX_NAME → exp_Initial.LOCAL2_TAX_NAME → SQ_LES_EMP_DETAIL_TBL.LOCAL2_TAX_NAME → LES_EMP_DETAIL_RECTYPE_3_TBL.LOCAL2_TAX_NAME | LES_EMP_DETAIL_RECTYPE_3_TBL.LOCAL2_TAX_NAME |
| LES_PRIMARY_DATA_TBL | CSRS | exp_Final.CSRS → exp_Stage.CSRS → exp_Initial.CSRS → SQ_LES_EMP_DETAIL_TBL.CSRS → LES_EMP_DETAIL_RECTYPE_3_TBL.CSRS | LES_EMP_DETAIL_RECTYPE_3_TBL.CSRS |
| LES_PRIMARY_DATA_TBL | CSRS_CUM_AMT | exp_Final.CSRS_CUM_AMT → exp_Stage.CSRS_CUM_AMT → exp_Initial.CSRS_CUM_AMT → SQ_LES_EMP_DETAIL_TBL.CSRS_CUM_AMT → LES_EMP_DETAIL_RECTYPE_3_TBL.CSRS_CUM_AMT | LES_EMP_DETAIL_RECTYPE_3_TBL.CSRS_CUM_AMT |
| LES_PRIMARY_DATA_TBL | BIWEEKLY_AMT | exp_Final.BIWEEKLY_AMT → exp_Stage.BIWEEKLY_AMT → exp_Initial.BIWEEKLY_AMT → SQ_LES_EMP_DETAIL_TBL.BIWEEKLY_AMT → LES_EMP_DETAIL_RECTYPE_3_TBL.BIWEEKLY_AMT | LES_EMP_DETAIL_RECTYPE_3_TBL.BIWEEKLY_AMT |
| LES_PRIMARY_DATA_TBL | BIWEEKLY_ANNUITY | exp_Final.BIWEEKLY_ANNUITY → exp_Stage.BIWEEKLY_ANNUITY → exp_Initial.BIWEEKLY_ANNUITY → SQ_LES_EMP_DETAIL_TBL.BIWEEKLY_ANNUITY → LES_EMP_DETAIL_RECTYPE_3_TBL.BIWEEKLY_ANNUITY | LES_EMP_DETAIL_RECTYPE_3_TBL.BIWEEKLY_ANNUITY |
| LES_PRIMARY_DATA_TBL | MILITARY_DEPOSIT | exp_Final.MILITARY_DEPOSIT → exp_Stage.MILITARY_DEPOSIT → exp_Initial.MILITARY_DEPOSIT → SQ_LES_EMP_DETAIL_TBL.MILITARY_DEPOSIT → LES_EMP_DETAIL_RECTYPE_3_TBL.MILITARY_DEPOSIT | LES_EMP_DETAIL_RECTYPE_3_TBL.MILITARY_DEPOSIT |
| LES_PRIMARY_DATA_TBL | MIL_DEPOSIT_PAID | exp_Final.MIL_DEPOSIT_PAID → exp_Stage.MIL_DEPOSIT_PAID → exp_Initial.MIL_DEPOSIT_PAID → SQ_LES_EMP_DETAIL_TBL.MIL_DEPOSIT_PAID → LES_EMP_DETAIL_RECTYPE_4_TBL.MIL_DEPOSIT_PAID | LES_EMP_DETAIL_RECTYPE_4_TBL.MIL_DEPOSIT_PAID |
| LES_PRIMARY_DATA_TBL | MIL_DEPOSIT_2 | exp_Final.MIL_DEPOSIT_2 → exp_Stage.MIL_DEPOSIT_2 → exp_Initial.MIL_DEPOSIT_2 → SQ_LES_EMP_DETAIL_TBL.MIL_DEPOSIT_2 → LES_EMP_DETAIL_RECTYPE_4_TBL.MIL_DEPOSIT_2 | LES_EMP_DETAIL_RECTYPE_4_TBL.MIL_DEPOSIT_2 |
| LES_PRIMARY_DATA_TBL | MIL_DEPOSIT_BAL | exp_Final.MIL_DEPOSIT_BAL → exp_Stage.MIL_DEPOSIT_BAL → exp_Initial.MIL_DEPOSIT_BAL → SQ_LES_EMP_DETAIL_TBL.MIL_DEPOSIT_BAL → LES_EMP_DETAIL_RECTYPE_4_TBL.MIL_DEPOSIT_BAL | LES_EMP_DETAIL_RECTYPE_4_TBL.MIL_DEPOSIT_BAL |
| LES_PRIMARY_DATA_TBL | GROSS_PAY_AMT | exp_Final.GROSS_PAY_AMT → exp_Stage.GROSS_PAY_AMT → exp_Initial.GROSS_PAY_AMT → SQ_LES_EMP_DETAIL_TBL.GROSS_PAY_AMT → LES_EMP_DETAIL_RECTYPE_4_TBL.GROSS_PAY_AMT | LES_EMP_DETAIL_RECTYPE_4_TBL.GROSS_PAY_AMT |
| LES_PRIMARY_DATA_TBL | GROSS_PAY_AMT_YTD | exp_Final.GROSS_PAY_AMT_YTD → exp_Stage.GROSS_PAY_AMT_YTD → exp_Initial.GROSS_PAY_AMT_YTD → SQ_LES_EMP_DETAIL_TBL.GROSS_PAY_AMT_YTD → LES_EMP_DETAIL_RECTYPE_4_TBL.GROSS_PAY_AMT_YTD | LES_EMP_DETAIL_RECTYPE_4_TBL.GROSS_PAY_AMT_YTD |
| LES_PRIMARY_DATA_TBL | TAXABLE_WAGE_AMT | exp_Final.TAXABLE_WAGE_AMT → exp_Stage.TAXABLE_WAGE_AMT → exp_Initial.TAXABLE_WAGE_AMT → SQ_LES_EMP_DETAIL_TBL.TAXABLE_WAGE_AMT → LES_EMP_DETAIL_RECTYPE_4_TBL.TAXABLE_WAGE_AMT | LES_EMP_DETAIL_RECTYPE_4_TBL.TAXABLE_WAGE_AMT |
| LES_PRIMARY_DATA_TBL | TAXABLE_WAGE_AMT_YTD | exp_Final.TAXABLE_WAGE_AMT_YTD → exp_Stage.TAXABLE_WAGE_AMT_YTD → exp_Initial.TAXABLE_WAGE_AMT_YTD → SQ_LES_EMP_DETAIL_TBL.TAXABLE_WAGE_AMT_YTD → LES_EMP_DETAIL_RECTYPE_4_TBL.TAXABLE_WAGE_AMT_YTD | LES_EMP_DETAIL_RECTYPE_4_TBL.TAXABLE_WAGE_AMT_YTD |
| LES_PRIMARY_DATA_TBL | NONTAXABLE_WAGE_AMT | exp_Final.NONTAXABLE_WAGE_AMT → exp_Stage.NONTAXABLE_WAGE_AMT → exp_Initial.NONTAXABLE_WAGE_AMT → SQ_LES_EMP_DETAIL_TBL.NONTAXABLE_WAGE_AMT → LES_EMP_DETAIL_RECTYPE_4_TBL.NONTAXABLE_WAGE_AMT | LES_EMP_DETAIL_RECTYPE_4_TBL.NONTAXABLE_WAGE_AMT |
| LES_PRIMARY_DATA_TBL | NONTAXABLE_WAGE_AMT_YTD | exp_Final.NONTAXABLE_WAGE_AMT_YTD → exp_Stage.NONTAXABLE_WAGE_AMT_YTD → exp_Initial.NONTAXABLE_WAGE_AMT_YTD → SQ_LES_EMP_DETAIL_TBL.NONTAXABLE_WAGE_AMT_YTD → LES_EMP_DETAIL_RECTYPE_4_TBL.NONTAXABLE_WAGE_AMT_YTD | LES_EMP_DETAIL_RECTYPE_4_TBL.NONTAXABLE_WAGE_AMT_YTD |
| LES_PRIMARY_DATA_TBL | TAX_DEFERRED_AMT | exp_Final.TAX_DEFERRED_AMT → exp_Stage.TAX_DEFERRED_AMT → exp_Initial.TAX_DEFERRED_AMT → SQ_LES_EMP_DETAIL_TBL.TAX_DEFERRED_AMT → LES_EMP_DETAIL_RECTYPE_4_TBL.TAX_DEFERRED_AMT | LES_EMP_DETAIL_RECTYPE_4_TBL.TAX_DEFERRED_AMT |
| LES_PRIMARY_DATA_TBL | TAX_DEFERRED_AMT_YTD | exp_Final.TAX_DEFERRED_AMT_YTD → exp_Stage.TAX_DEFERRED_AMT_YTD → exp_Initial.TAX_DEFERRED_AMT_YTD → SQ_LES_EMP_DETAIL_TBL.TAX_DEFERRED_AMT_YTD → LES_EMP_DETAIL_RECTYPE_4_TBL.TAX_DEFERRED_AMT_YTD | LES_EMP_DETAIL_RECTYPE_4_TBL.TAX_DEFERRED_AMT_YTD |
| LES_PRIMARY_DATA_TBL | DEDUCTION_AMT | exp_Final.DEDUCTION_AMT → exp_Stage.DEDUCTION_AMT → exp_Initial.DEDUCTION_AMT → SQ_LES_EMP_DETAIL_TBL.DEDUCTION_AMT → LES_EMP_DETAIL_RECTYPE_4_TBL.DEDUCTION_AMT | LES_EMP_DETAIL_RECTYPE_4_TBL.DEDUCTION_AMT |
| LES_PRIMARY_DATA_TBL | DEDUCTION_AMT_YTD | exp_Final.DEDUCTION_AMT_YTD → exp_Stage.DEDUCTION_AMT_YTD → exp_Initial.DEDUCTION_AMT_YTD → SQ_LES_EMP_DETAIL_TBL.DEDUCTION_AMT_YTD → LES_EMP_DETAIL_RECTYPE_4_TBL.DEDUCTION_AMT_YTD | LES_EMP_DETAIL_RECTYPE_4_TBL.DEDUCTION_AMT_YTD |
| LES_PRIMARY_DATA_TBL | ADV_ERND_INCOME_CREDIT_AMT_YTD | exp_Final.ADV_ERND_INCOME_CREDIT_AMT_YTD → exp_Stage.ADV_ERND_INCOME_CREDIT_AMT_YTD → exp_Initial.ADV_ERND_INCOME_CREDIT_AMT_YTD → SQ_LES_EMP_DETAIL_TBL.ADV_ERND_INCOME_CREDIT_AMT_YTD → LES_EMP_DETAIL_RECTYPE_5_TBL.ADV_ERND_INCOME_CREDIT_AMT_YTD | LES_EMP_DETAIL_RECTYPE_5_TBL.ADV_ERND_INCOME_CREDIT_AMT_YTD |
| LES_PRIMARY_DATA_TBL | NET_PAY_AMT | exp_Final.NET_PAY_AMT → exp_Stage.NET_PAY_AMT → exp_Initial.NET_PAY_AMT → SQ_LES_EMP_DETAIL_TBL.NET_PAY_AMT → LES_EMP_DETAIL_RECTYPE_5_TBL.NET_PAY_AMT | LES_EMP_DETAIL_RECTYPE_5_TBL.NET_PAY_AMT |
| LES_PRIMARY_DATA_TBL | NET_PAY_AMT_YTD | exp_Final.NET_PAY_AMT_YTD → exp_Stage.NET_PAY_AMT_YTD → exp_Initial.NET_PAY_AMT_YTD → SQ_LES_EMP_DETAIL_TBL.NET_PAY_AMT_YTD → LES_EMP_DETAIL_RECTYPE_5_TBL.NET_PAY_AMT_YTD | LES_EMP_DETAIL_RECTYPE_5_TBL.NET_PAY_AMT_YTD |
| LES_PRIMARY_DATA_TBL | TSP_SAVINGS | exp_Final.TSP_SAVINGS → exp_Stage.TSP_SAVINGS → exp_Initial.TSP_SAVINGS → SQ_LES_EMP_DETAIL_TBL.TSP_SAVINGS → LES_EMP_DETAIL_RECTYPE_5_TBL.TSP_SAVINGS | LES_EMP_DETAIL_RECTYPE_5_TBL.TSP_SAVINGS |
| LES_PRIMARY_DATA_TBL | TSP_SAVINGS_PCT | exp_Final.TSP_SAVINGS_PCT → exp_Stage.TSP_SAVINGS_PCT → exp_Initial.TSP_SAVINGS_PCT → SQ_LES_EMP_DETAIL_TBL.TSP_SAVINGS_PCT → LES_EMP_DETAIL_RECTYPE_5_TBL.TSP_SAVINGS_PCT | LES_EMP_DETAIL_RECTYPE_5_TBL.TSP_SAVINGS_PCT |
| LES_PRIMARY_DATA_TBL | TITLEG_FUND | exp_Final.TITLEG_FUND → exp_Stage.TITLEG_FUND → exp_Initial.TITLEG_FUND → SQ_LES_EMP_DETAIL_TBL.TITLEG_FUND → LES_EMP_DETAIL_RECTYPE_5_TBL.TITLEG_FUND | LES_EMP_DETAIL_RECTYPE_5_TBL.TITLEG_FUND |
| LES_PRIMARY_DATA_TBL | TITLEG_FUND_PCT | exp_Final.TITLEG_FUND_PCT → exp_Stage.TITLEG_FUND_PCT → exp_Initial.TITLEG_FUND_PCT → SQ_LES_EMP_DETAIL_TBL.TITLEG_FUND_PCT → LES_EMP_DETAIL_RECTYPE_5_TBL.TITLEG_FUND_PCT | LES_EMP_DETAIL_RECTYPE_5_TBL.TITLEG_FUND_PCT |
| LES_PRIMARY_DATA_TBL | TITLEF_FUND | exp_Final.TITLEF_FUND → exp_Stage.TITLEF_FUND → exp_Initial.TITLEF_FUND → SQ_LES_EMP_DETAIL_TBL.TITLEF_FUND → LES_EMP_DETAIL_RECTYPE_5_TBL.TITLEF_FUND | LES_EMP_DETAIL_RECTYPE_5_TBL.TITLEF_FUND |
| LES_PRIMARY_DATA_TBL | TITLEF_FUND_PCT | exp_Final.TITLEF_FUND_PCT → exp_Stage.TITLEF_FUND_PCT → exp_Initial.TITLEF_FUND_PCT → SQ_LES_EMP_DETAIL_TBL.TITLEF_FUND_PCT → LES_EMP_DETAIL_RECTYPE_5_TBL.TITLEF_FUND_PCT | LES_EMP_DETAIL_RECTYPE_5_TBL.TITLEF_FUND_PCT |
| LES_PRIMARY_DATA_TBL | TITLEC_FUND | exp_Final.TITLEC_FUND → exp_Stage.TITLEC_FUND → exp_Initial.TITLEC_FUND → SQ_LES_EMP_DETAIL_TBL.TITLEC_FUND → LES_EMP_DETAIL_RECTYPE_5_TBL.TITLEC_FUND | LES_EMP_DETAIL_RECTYPE_5_TBL.TITLEC_FUND |
| LES_PRIMARY_DATA_TBL | TITLEC_FUND_PCT | exp_Final.TITLEC_FUND_PCT → exp_Stage.TITLEC_FUND_PCT → exp_Initial.TITLEC_FUND_PCT → SQ_LES_EMP_DETAIL_TBL.TITLEC_FUND_PCT → LES_EMP_DETAIL_RECTYPE_5_TBL.TITLEC_FUND_PCT | LES_EMP_DETAIL_RECTYPE_5_TBL.TITLEC_FUND_PCT |
| LES_PRIMARY_DATA_TBL | ROTH_SAVINGS | exp_Final.ROTH_SAVINGS → exp_Stage.ROTH_SAVINGS → exp_Initial.ROTH_SAVINGS → SQ_LES_EMP_DETAIL_TBL.ROTH_SAVINGS → LES_EMP_DETAIL_RECTYPE_5_TBL.ROTH_SAVINGS | LES_EMP_DETAIL_RECTYPE_5_TBL.ROTH_SAVINGS |
| LES_PRIMARY_DATA_TBL | ROTH_SAVINGS_PCT | exp_Final.ROTH_SAVINGS_PCT → exp_Stage.ROTH_SAVINGS_PCT → exp_Initial.ROTH_SAVINGS_PCT → SQ_LES_EMP_DETAIL_TBL.ROTH_SAVINGS_PCT → LES_EMP_DETAIL_RECTYPE_5_TBL.ROTH_SAVINGS_PCT | LES_EMP_DETAIL_RECTYPE_5_TBL.ROTH_SAVINGS_PCT |
| LES_PRIMARY_DATA_TBL | EARNINGS_FOR_CURR_TSP | exp_Final.EARNINGS_FOR_CURR_TSP → exp_Stage.EARNINGS_FOR_CURR_TSP → exp_Initial.EARNINGS_FOR_CURR_TSP → SQ_LES_EMP_DETAIL_TBL.EARNINGS_FOR_CURR_TSP → LES_EMP_DETAIL_RECTYPE_6_TBL.EARNINGS_FOR_CURR_TSP | LES_EMP_DETAIL_RECTYPE_6_TBL.EARNINGS_FOR_CURR_TSP |
| LES_PRIMARY_DATA_TBL | EARNINGS_FOR_CURR_TSP_AMT | exp_Final.EARNINGS_FOR_CURR_TSP_AMT → exp_Stage.EARNINGS_FOR_CURR_TSP_AMT → exp_Initial.EARNINGS_FOR_CURR_TSP_AMT → SQ_LES_EMP_DETAIL_TBL.EARNINGS_FOR_CURR_TSP_AMT → LES_EMP_DETAIL_RECTYPE_6_TBL.EARNINGS_FOR_CURR_TSP_AMT | LES_EMP_DETAIL_RECTYPE_6_TBL.EARNINGS_FOR_CURR_TSP_AMT |
| LES_PRIMARY_DATA_TBL | EARNINGS_FOR_YTD_TSP | exp_Final.EARNINGS_FOR_YTD_TSP → exp_Stage.EARNINGS_FOR_YTD_TSP → exp_Initial.EARNINGS_FOR_YTD_TSP → SQ_LES_EMP_DETAIL_TBL.EARNINGS_FOR_YTD_TSP → LES_EMP_DETAIL_RECTYPE_6_TBL.EARNINGS_FOR_YTD_TSP | LES_EMP_DETAIL_RECTYPE_6_TBL.EARNINGS_FOR_YTD_TSP |
| LES_PRIMARY_DATA_TBL | EARNINGS_FOR_YTD_TSP_AMT | exp_Final.EARNINGS_FOR_YTD_TSP_AMT → exp_Stage.EARNINGS_FOR_YTD_TSP_AMT → exp_Initial.EARNINGS_FOR_YTD_TSP_AMT → SQ_LES_EMP_DETAIL_TBL.EARNINGS_FOR_YTD_TSP_AMT → LES_EMP_DETAIL_RECTYPE_6_TBL.EARNINGS_FOR_YTD_TSP_AMT | LES_EMP_DETAIL_RECTYPE_6_TBL.EARNINGS_FOR_YTD_TSP_AMT |
| LES_PRIMARY_DATA_TBL | REMARK_TEXT | (not connected — NULL) | — |

## Mapping `m_LES_Load_LES_EMP_DETAIL_CURR_EARN_TBL`

- Sessions: `s_LES_Load_LES_EMP_DETAIL_CURR_EARN_TBL` (#20)
- Sources: `LES_EMP_DETAIL_RECTYPE_C_TBL`
- Target instances: `LES_EMP_DETAIL_CURR_EARN_TBL`

### Transformation `SQ_LES_EMP_DETAIL_RECTYPE_C_TBL` (Source Qualifier)

- **Sql Query**: `SELECT a.PP_END_YEAR, a.PP_NUM, a.LES_NUMBER, a.PSEUDOSSN, a.CURR_EARN_ID, TRIM(a.CURR_EARN_NAME1) CURR_EARN_NAME1 , a.CURR_EARN_NAME1_HOURS, a.CURR_EARN_NAME1_AMT, TRIM(a.CURR_EARN_NAME2) CURR_EARN_NAME2 , a.CURR_EARN_NAME2_HOURS, a.CURR_EARN_NAME2_AMT, a.CURR_EARN_NAME3, a.CURR_EARN_NAME3_HOURS, a.CURR_EARN_NAME3_AMT FROM LES_EMP_DETAIL_RECTYPE_C_TBL a WHERE a.PP_END_YEAR = $$MAP_PP_END_YEAR AND a.PP_NUM = $$MAP_PP_NUM`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `fil_Remove_Blank_Current_Earnings` (Filter)

- **Filter Condition**: `NOT ISNULL(CURR_EARN_NAME) AND LTRIM(RTRIM(CURR_EARN_NAME)) != ''`

### Transformation `nrm_EMP_CURR_EARN` (Normalizer)

- **Reset**: `NO`
- **Restart**: `NO`

- Normalizer `nrm_EMP_CURR_EARN` (vsam=False) occurs: CURR_EARN_AMT×3, CURR_EARN_HOURS×3, CURR_EARN_NAME×3; generated: GK_CURR_EARN_NAME, GCID_CURR_EARN_NAME, GCID_CURR_EARN_HOURS, GCID_CURR_EARN_AMT
- SQL override `SQ_LES_EMP_DETAIL_RECTYPE_C_TBL` positional bindings: 1 → `PP_END_YEAR` = `a.PP_END_YEAR`; 2 → `PP_NUM` = `a.PP_NUM`; 3 → `LES_NUMBER` = `a.LES_NUMBER`; 4 → `PSEUDOSSN` = `a.PSEUDOSSN`; 5 → `CURR_EARN_ID` = `a.CURR_EARN_ID`; 6 → `CURR_EARN_NAME1` = `TRIM(a.CURR_EARN_NAME1) CURR_EARN_NAME1`; 7 → `CURR_EARN_NAME1_HOURS` = `a.CURR_EARN_NAME1_HOURS`; 8 → `CURR_EARN_NAME1_AMT` = `a.CURR_EARN_NAME1_AMT`; 9 → `CURR_EARN_NAME2` = `TRIM(a.CURR_EARN_NAME2) CURR_EARN_NAME2`; 10 → `CURR_EARN_NAME2_HOURS` = `a.CURR_EARN_NAME2_HOURS`; 11 → `CURR_EARN_NAME2_AMT` = `a.CURR_EARN_NAME2_AMT`; 12 → `CURR_EARN_NAME3` = `a.CURR_EARN_NAME3`; 13 → `CURR_EARN_NAME3_HOURS` = `a.CURR_EARN_NAME3_HOURS`; 14 → `CURR_EARN_NAME3_AMT` = `a.CURR_EARN_NAME3_AMT`

### Target instance `LES_EMP_DETAIL_CURR_EARN_TBL` (table `LES_EMP_DETAIL_CURR_EARN_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LES_EMP_DETAIL_CURR_EARN_TBL | PP_END_YEAR | exp_Final.PP_END_YEAR → exp_Convert.PP_END_YEAR → fil_Remove_Blank_Current_Earnings.PP_END_YEAR → nrm_EMP_CURR_EARN.PP_END_YEAR [normalizer: one row per occurrence of PP_END_YEAR_in] → exp_Initial.PP_END_YEAR → SQ_LES_EMP_DETAIL_RECTYPE_C_TBL.PP_END_YEAR → LES_EMP_DETAIL_RECTYPE_C_TBL.PP_END_YEAR | LES_EMP_DETAIL_RECTYPE_C_TBL.PP_END_YEAR |
| LES_EMP_DETAIL_CURR_EARN_TBL | PP_NUM | exp_Final.PP_NUM → exp_Convert.PP_NUM → fil_Remove_Blank_Current_Earnings.PP_NUM → nrm_EMP_CURR_EARN.PP_NUM [normalizer: one row per occurrence of PP_NUM_in] → exp_Initial.PP_NUM → SQ_LES_EMP_DETAIL_RECTYPE_C_TBL.PP_NUM → LES_EMP_DETAIL_RECTYPE_C_TBL.PP_NUM | LES_EMP_DETAIL_RECTYPE_C_TBL.PP_NUM |
| LES_EMP_DETAIL_CURR_EARN_TBL | LES_NUMBER | exp_Final.LES_NUMBER → exp_Convert.LES_NUMBER → fil_Remove_Blank_Current_Earnings.LES_NUMBER → nrm_EMP_CURR_EARN.LES_NUMBER [normalizer: one row per occurrence of LES_NUMBER_in] → exp_Initial.LES_NUMBER → SQ_LES_EMP_DETAIL_RECTYPE_C_TBL.LES_NUMBER → LES_EMP_DETAIL_RECTYPE_C_TBL.LES_NUMBER | LES_EMP_DETAIL_RECTYPE_C_TBL.LES_NUMBER |
| LES_EMP_DETAIL_CURR_EARN_TBL | PSEUDOSSN | exp_Final.PSEUDOSSN → exp_Convert.PSEUDOSSN → fil_Remove_Blank_Current_Earnings.PSEUDOSSN → nrm_EMP_CURR_EARN.PSEUDOSSN [normalizer: one row per occurrence of PSEUDOSSN_in] → exp_Initial.PSEUDOSSN → SQ_LES_EMP_DETAIL_RECTYPE_C_TBL.PSEUDOSSN → LES_EMP_DETAIL_RECTYPE_C_TBL.PSEUDOSSN | LES_EMP_DETAIL_RECTYPE_C_TBL.PSEUDOSSN |
| LES_EMP_DETAIL_CURR_EARN_TBL | CURR_EARN_ID | exp_Final.CURR_EARN_ID → exp_Convert.o_CURR_EARN_ID = v_CURR_EARN_ID → exp_Convert.v_CURR_EARN_ID = IIF(v_CURR_EARN_ID = 0, 1, v_CURR_EARN_ID + 1) | literal/expression: IIF(v_CURR_EARN_ID = 0, 1, v_CURR_EARN_ID + 1) |
| LES_EMP_DETAIL_CURR_EARN_TBL | CURR_EARN_NAME | exp_Final.CURR_EARN_NAME → exp_Convert.CURR_EARN_NAME → fil_Remove_Blank_Current_Earnings.CURR_EARN_NAME → nrm_EMP_CURR_EARN.CURR_EARN_NAME [normalizer: one row per occurrence of CURR_EARN_NAME_in1, CURR_EARN_NAME_in2, CURR_EARN_NAME_in3] → exp_Initial.CURR_EARN_NAME1 → SQ_LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME1 → LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME1 → exp_Initial.CURR_EARN_NAME2 → SQ_LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME2 → LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME2 → exp_Initial.CURR_EARN_NAME3 → SQ_LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME3 → LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME3 | LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME1; LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME2; LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME3 |
| LES_EMP_DETAIL_CURR_EARN_TBL | CURR_EARN_HOURS | exp_Final.CURR_EARN_HOURS → exp_Convert.CURR_EARN_HOURS → fil_Remove_Blank_Current_Earnings.CURR_EARN_HOURS → nrm_EMP_CURR_EARN.CURR_EARN_HOURS [normalizer: one row per occurrence of CURR_EARN_HOURS_in1, CURR_EARN_HOURS_in2, CURR_EARN_HOURS_in3] → exp_Initial.CURR_EARN_NAME1_HOURS → SQ_LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME1_HOURS → LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME1_HOURS → exp_Initial.CURR_EARN_NAME2_HOURS → SQ_LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME2_HOURS → LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME2_HOURS → exp_Initial.CURR_EARN_NAME3_HOURS → SQ_LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME3_HOURS → LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME3_HOURS | LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME1_HOURS; LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME2_HOURS; LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME3_HOURS |
| LES_EMP_DETAIL_CURR_EARN_TBL | CURR_EARN_AMT | exp_Final.CURR_EARN_AMT → exp_Convert.CURR_EARN_AMT → fil_Remove_Blank_Current_Earnings.CURR_EARN_AMT → nrm_EMP_CURR_EARN.CURR_EARN_AMT [normalizer: one row per occurrence of CURR_EARN_AMT_in1, CURR_EARN_AMT_in2, CURR_EARN_AMT_in3] → exp_Initial.CURR_EARN_NAME1_AMT → SQ_LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME1_AMT → LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME1_AMT → exp_Initial.CURR_EARN_NAME2_AMT → SQ_LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME2_AMT → LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME2_AMT → exp_Initial.CURR_EARN_NAME3_AMT → SQ_LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME3_AMT → LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME3_AMT | LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME1_AMT; LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME2_AMT; LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME3_AMT |

## Mapping `m_LES_Load_LES_EMP_DETAIL_RETRO_EARN_TBL`

- Sessions: `s_LES_Load_LES_EMP_DETAIL_RETRO_EARN_TBL` (#21)
- Sources: `LES_EMP_DETAIL_RECTYPE_R_TBL`
- Target instances: `LES_EMP_DETAIL_RETRO_EARN_TBL`

### Transformation `SQ_LES_EMP_DETAIL_RECTYPE_R_TBL` (Source Qualifier)

- **Sql Query**: `SELECT a.PP_END_YEAR, a.PP_NUM, a.LES_NUMBER, a.PSEUDOSSN, a.RETRO_ACTIVE_ID, TRIM(a.RETRO_ACTIVE_EARN_NAME1) RETRO_ACTIVE_EARN_NAME1, a.RETRO_ACTIVE_EARN_NAME1_HOURS, a.RETRO_ACTIVE_EARN_NAME1_AMT, TRIM(a.RETRO_ACTIVE_EARN_NAME2) RETRO_ACTIVE_EARN_NAME2, a.RETRO_ACTIVE_EARN_NAME2_HOURS, a.RETRO_ACTIVE_EARN_NAME2_AMT, TRIM(a.RETRO_ACTIVE_EARN_NAME3) RETRO_ACTIVE_EARN_NAME3, a.RETRO_ACTIVE_EARN_NAME3_HOURS, a.RETRO_ACTIVE_EARN_NAME3_AMT FROM LES_EMP_DETAIL_RECTYPE_R_TBL a WHERE a.PP_END_YEAR = $$MAP_PP_END_YEAR AND a.PP_NUM = $$MAP_PP_NUM`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `fil_Remove_Blank_Retroactive_Earnings` (Filter)

- **Filter Condition**: `NOT ISNULL(RETRO_EARN_NAME) AND LTRIM(RTRIM(RETRO_EARN_NAME)) != ''`

### Transformation `nrm_EMP_RETRO_EARN` (Normalizer)

- **Reset**: `NO`
- **Restart**: `NO`

- Normalizer `nrm_EMP_RETRO_EARN` (vsam=False) occurs: RETRO_EARN_AMT×3, RETRO_EARN_HOURS×3, RETRO_EARN_NAME×3; generated: GK_RETRO_EARN_NAME, GCID_RETRO_EARN_NAME, GCID_RETRO_EARN_HOURS, GCID_RETRO_EARN_AMT
- SQL override `SQ_LES_EMP_DETAIL_RECTYPE_R_TBL` positional bindings: 1 → `PP_END_YEAR` = `a.PP_END_YEAR`; 2 → `PP_NUM` = `a.PP_NUM`; 3 → `LES_NUMBER` = `a.LES_NUMBER`; 4 → `PSEUDOSSN` = `a.PSEUDOSSN`; 5 → `RETRO_ACTIVE_ID` = `a.RETRO_ACTIVE_ID`; 6 → `RETRO_ACTIVE_EARN_NAME1` = `TRIM(a.RETRO_ACTIVE_EARN_NAME1) RETRO_ACTIVE_EARN_NAME1`; 7 → `RETRO_ACTIVE_EARN_NAME1_HOURS` = `a.RETRO_ACTIVE_EARN_NAME1_HOURS`; 8 → `RETRO_ACTIVE_EARN_NAME1_AMT` = `a.RETRO_ACTIVE_EARN_NAME1_AMT`; 9 → `RETRO_ACTIVE_EARN_NAME2` = `TRIM(a.RETRO_ACTIVE_EARN_NAME2) RETRO_ACTIVE_EARN_NAME2`; 10 → `RETRO_ACTIVE_EARN_NAME2_HOURS` = `a.RETRO_ACTIVE_EARN_NAME2_HOURS`; 11 → `RETRO_ACTIVE_EARN_NAME2_AMT` = `a.RETRO_ACTIVE_EARN_NAME2_AMT`; 12 → `RETRO_ACTIVE_EARN_NAME3` = `TRIM(a.RETRO_ACTIVE_EARN_NAME3) RETRO_ACTIVE_EARN_NAME3`; 13 → `RETRO_ACTIVE_EARN_NAME3_HOURS` = `a.RETRO_ACTIVE_EARN_NAME3_HOURS`; 14 → `RETRO_ACTIVE_EARN_NAME3_AMT` = `a.RETRO_ACTIVE_EARN_NAME3_AMT`

### Target instance `LES_EMP_DETAIL_RETRO_EARN_TBL` (table `LES_EMP_DETAIL_RETRO_EARN_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LES_EMP_DETAIL_RETRO_EARN_TBL | PP_END_YEAR | exp_Final.PP_END_YEAR → exp_Convert.PP_END_YEAR → fil_Remove_Blank_Retroactive_Earnings.PP_END_YEAR → nrm_EMP_RETRO_EARN.PP_END_YEAR [normalizer: one row per occurrence of PP_END_YEAR_in] → exp_Initial.PP_END_YEAR → SQ_LES_EMP_DETAIL_RECTYPE_R_TBL.PP_END_YEAR → LES_EMP_DETAIL_RECTYPE_R_TBL.PP_END_YEAR | LES_EMP_DETAIL_RECTYPE_R_TBL.PP_END_YEAR |
| LES_EMP_DETAIL_RETRO_EARN_TBL | PP_NUM | exp_Final.PP_NUM → exp_Convert.PP_NUM → fil_Remove_Blank_Retroactive_Earnings.PP_NUM → nrm_EMP_RETRO_EARN.PP_NUM [normalizer: one row per occurrence of PP_NUM_in] → exp_Initial.PP_NUM → SQ_LES_EMP_DETAIL_RECTYPE_R_TBL.PP_NUM → LES_EMP_DETAIL_RECTYPE_R_TBL.PP_NUM | LES_EMP_DETAIL_RECTYPE_R_TBL.PP_NUM |
| LES_EMP_DETAIL_RETRO_EARN_TBL | LES_NUMBER | exp_Final.LES_NUMBER → exp_Convert.LES_NUMBER → fil_Remove_Blank_Retroactive_Earnings.LES_NUMBER → nrm_EMP_RETRO_EARN.LES_NUMBER [normalizer: one row per occurrence of LES_NUMBER_in] → exp_Initial.LES_NUMBER → SQ_LES_EMP_DETAIL_RECTYPE_R_TBL.LES_NUMBER → LES_EMP_DETAIL_RECTYPE_R_TBL.LES_NUMBER | LES_EMP_DETAIL_RECTYPE_R_TBL.LES_NUMBER |
| LES_EMP_DETAIL_RETRO_EARN_TBL | PSEUDOSSN | exp_Final.PSEUDOSSN → exp_Convert.PSEUDOSSN → fil_Remove_Blank_Retroactive_Earnings.PSEUDOSSN → nrm_EMP_RETRO_EARN.PSEUDOSSN [normalizer: one row per occurrence of PSEUDOSSN_in] → exp_Initial.PSEUDOSSN → SQ_LES_EMP_DETAIL_RECTYPE_R_TBL.PSEUDOSSN → LES_EMP_DETAIL_RECTYPE_R_TBL.PSEUDOSSN | LES_EMP_DETAIL_RECTYPE_R_TBL.PSEUDOSSN |
| LES_EMP_DETAIL_RETRO_EARN_TBL | RETRO_ACTIVE_ID | exp_Final.RETRO_ACTIVE_ID → exp_Convert.o_RETRO_ACTIVE_ID = v_RETRO_ACTIVE_ID → exp_Convert.v_RETRO_ACTIVE_ID = IIF(v_RETRO_ACTIVE_ID = 0, 1, v_RETRO_ACTIVE_ID + 1) | literal/expression: IIF(v_RETRO_ACTIVE_ID = 0, 1, v_RETRO_ACTIVE_ID + 1) |
| LES_EMP_DETAIL_RETRO_EARN_TBL | RETRO_ACTIVE_EARN_NAME | exp_Final.RETRO_ACTIVE_EARN_NAME → exp_Convert.RETRO_EARN_NAME → fil_Remove_Blank_Retroactive_Earnings.RETRO_EARN_NAME → nrm_EMP_RETRO_EARN.RETRO_EARN_NAME [normalizer: one row per occurrence of RETRO_EARN_NAME_in1, RETRO_EARN_NAME_in2, RETRO_EARN_NAME_in3] → exp_Initial.RETRO_ACTIVE_EARN_NAME1 → SQ_LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME1 → LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME1 → exp_Initial.RETRO_ACTIVE_EARN_NAME2 → SQ_LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME2 → LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME2 → exp_Initial.RETRO_ACTIVE_EARN_NAME3 → SQ_LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME3 → LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME3 | LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME1; LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME2; LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME3 |
| LES_EMP_DETAIL_RETRO_EARN_TBL | RETRO_ACTIVE_EARN_HOURS | exp_Final.RETRO_ACTIVE_EARN_HOURS → exp_Convert.RETRO_EARN_HOURS → fil_Remove_Blank_Retroactive_Earnings.RETRO_EARN_HOURS → nrm_EMP_RETRO_EARN.RETRO_EARN_HOURS [normalizer: one row per occurrence of RETRO_EARN_HOURS_in1, RETRO_EARN_HOURS_in2, RETRO_EARN_HOURS_in3] → exp_Initial.RETRO_ACTIVE_EARN_NAME1_HOURS → SQ_LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME1_HOURS → LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME1_HOURS → exp_Initial.RETRO_ACTIVE_EARN_NAME2_HOURS → SQ_LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME2_HOURS → LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME2_HOURS → exp_Initial.RETRO_ACTIVE_EARN_NAME3_HOURS → SQ_LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME3_HOURS → LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME3_HOURS | LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME1_HOURS; LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME2_HOURS; LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME3_HOURS |
| LES_EMP_DETAIL_RETRO_EARN_TBL | RETRO_ACTIVE_EARN_AMT | exp_Final.RETRO_ACTIVE_EARN_AMT → exp_Convert.RETRO_EARN_AMT → fil_Remove_Blank_Retroactive_Earnings.RETRO_EARN_AMT → nrm_EMP_RETRO_EARN.RETRO_EARN_AMT [normalizer: one row per occurrence of RETRO_EARN_AMT_in1, RETRO_EARN_AMT_in2, RETRO_EARN_AMT_in3] → exp_Initial.RETRO_ACTIVE_EARN_NAME1_AMT → SQ_LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME1_AMT → LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME1_AMT → exp_Initial.RETRO_ACTIVE_EARN_NAME2_AMT → SQ_LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME2_AMT → LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME2_AMT → exp_Initial.RETRO_ACTIVE_EARN_NAME3_AMT → SQ_LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME3_AMT → LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME3_AMT | LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME1_AMT; LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME2_AMT; LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME3_AMT |

## Mapping `m_LES_Load_LES_EMP_DETAIL_LEAVE_TBL`

- Sessions: `s_LES_Load_LES_EMP_DETAIL_LEAVE_TBL` (#22)
- Sources: `LES_EMP_DETAIL_RECTYPE_L_TBL`
- Target instances: `LES_EMP_DETAIL_LEAVE_TBL`

### Transformation `SQ_LES_EMP_DETAIL_RECTYPE_L_TBL` (Source Qualifier)

- **Sql Query**: `SELECT a.PP_END_YEAR, a.PP_NUM, a.LES_NUMBER, a.PSEUDOSSN, a.LEAVE_ID, TRIM(a.LEAVE_NAME) LEAVE_NAME, a.LEAVE_PRIOR_YEAR_BAL, a.LEAVE_EARNED_CPP, a.LEAVE_EARNED_YTD, a.LEAVE_USED_CPP, a.LEAVE_USED_YTD, a.LEAVE_DONATED, a.LEAVE_CURR_BAL, a.LEAVE_USE_OR_LOSE_TERM_DTE, a.LEAVE_USE_OR_LOSE_TERM_BAL_HRS FROM LES_EMP_DETAIL_RECTYPE_L_TBL a WHERE a.PP_END_YEAR = $$MAP_PP_END_YEAR AND a.PP_NUM = $$MAP_PP_NUM`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

- SQL override `SQ_LES_EMP_DETAIL_RECTYPE_L_TBL` positional bindings: 1 → `PP_END_YEAR` = `a.PP_END_YEAR`; 2 → `PP_NUM` = `a.PP_NUM`; 3 → `LES_NUMBER` = `a.LES_NUMBER`; 4 → `PSEUDOSSN` = `a.PSEUDOSSN`; 5 → `LEAVE_ID` = `a.LEAVE_ID`; 6 → `LEAVE_NAME` = `TRIM(a.LEAVE_NAME) LEAVE_NAME`; 7 → `LEAVE_PRIOR_YEAR_BAL` = `a.LEAVE_PRIOR_YEAR_BAL`; 8 → `LEAVE_EARNED_CPP` = `a.LEAVE_EARNED_CPP`; 9 → `LEAVE_EARNED_YTD` = `a.LEAVE_EARNED_YTD`; 10 → `LEAVE_USED_CPP` = `a.LEAVE_USED_CPP`; 11 → `LEAVE_USED_YTD` = `a.LEAVE_USED_YTD`; 12 → `LEAVE_DONATED` = `a.LEAVE_DONATED`; 13 → `LEAVE_CURR_BAL` = `a.LEAVE_CURR_BAL`; 14 → `LEAVE_USE_OR_LOSE_TERM_DTE` = `a.LEAVE_USE_OR_LOSE_TERM_DTE`; 15 → `LEAVE_USE_OR_LOSE_TERM_BAL_HRS` = `a.LEAVE_USE_OR_LOSE_TERM_BAL_HRS`

### Target instance `LES_EMP_DETAIL_LEAVE_TBL` (table `LES_EMP_DETAIL_LEAVE_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LES_EMP_DETAIL_LEAVE_TBL | PP_END_YEAR | exp_Final.PP_END_YEAR → exp_Initial.PP_END_YEAR → SQ_LES_EMP_DETAIL_RECTYPE_L_TBL.PP_END_YEAR → LES_EMP_DETAIL_RECTYPE_L_TBL.PP_END_YEAR | LES_EMP_DETAIL_RECTYPE_L_TBL.PP_END_YEAR |
| LES_EMP_DETAIL_LEAVE_TBL | PP_NUM | exp_Final.PP_NUM → exp_Initial.PP_NUM → SQ_LES_EMP_DETAIL_RECTYPE_L_TBL.PP_NUM → LES_EMP_DETAIL_RECTYPE_L_TBL.PP_NUM | LES_EMP_DETAIL_RECTYPE_L_TBL.PP_NUM |
| LES_EMP_DETAIL_LEAVE_TBL | LES_NUMBER | exp_Final.LES_NUMBER → exp_Initial.LES_NUMBER → SQ_LES_EMP_DETAIL_RECTYPE_L_TBL.LES_NUMBER → LES_EMP_DETAIL_RECTYPE_L_TBL.LES_NUMBER | LES_EMP_DETAIL_RECTYPE_L_TBL.LES_NUMBER |
| LES_EMP_DETAIL_LEAVE_TBL | PSEUDOSSN | exp_Final.PSEUDOSSN → exp_Initial.PSEUDOSSN → SQ_LES_EMP_DETAIL_RECTYPE_L_TBL.PSEUDOSSN → LES_EMP_DETAIL_RECTYPE_L_TBL.PSEUDOSSN | LES_EMP_DETAIL_RECTYPE_L_TBL.PSEUDOSSN |
| LES_EMP_DETAIL_LEAVE_TBL | LEAVE_ID | exp_Final.LEAVE_ID → exp_Initial.o_LEAVE_ID = v_LEAVE_ID → exp_Initial.v_LEAVE_ID = IIF(v_LEAVE_ID = 0, 1, v_LEAVE_ID + 1) | literal/expression: IIF(v_LEAVE_ID = 0, 1, v_LEAVE_ID + 1) |
| LES_EMP_DETAIL_LEAVE_TBL | LEAVE_NAME | exp_Final.LEAVE_NAME → exp_Initial.LEAVE_NAME → SQ_LES_EMP_DETAIL_RECTYPE_L_TBL.LEAVE_NAME → LES_EMP_DETAIL_RECTYPE_L_TBL.LEAVE_NAME | LES_EMP_DETAIL_RECTYPE_L_TBL.LEAVE_NAME |
| LES_EMP_DETAIL_LEAVE_TBL | LEAVE_PRIOR_YEAR_BAL | exp_Final.LEAVE_PRIOR_YEAR_BAL → exp_Initial.LEAVE_PRIOR_YEAR_BAL → SQ_LES_EMP_DETAIL_RECTYPE_L_TBL.LEAVE_PRIOR_YEAR_BAL → LES_EMP_DETAIL_RECTYPE_L_TBL.LEAVE_PRIOR_YEAR_BAL | LES_EMP_DETAIL_RECTYPE_L_TBL.LEAVE_PRIOR_YEAR_BAL |
| LES_EMP_DETAIL_LEAVE_TBL | LEAVE_EARNED_CPP | exp_Final.LEAVE_EARNED_CPP → exp_Initial.LEAVE_EARNED_CPP → SQ_LES_EMP_DETAIL_RECTYPE_L_TBL.LEAVE_EARNED_CPP → LES_EMP_DETAIL_RECTYPE_L_TBL.LEAVE_EARNED_CPP | LES_EMP_DETAIL_RECTYPE_L_TBL.LEAVE_EARNED_CPP |
| LES_EMP_DETAIL_LEAVE_TBL | LEAVE_EARNED_YTD | exp_Final.LEAVE_EARNED_YTD → exp_Initial.LEAVE_EARNED_YTD → SQ_LES_EMP_DETAIL_RECTYPE_L_TBL.LEAVE_EARNED_YTD → LES_EMP_DETAIL_RECTYPE_L_TBL.LEAVE_EARNED_YTD | LES_EMP_DETAIL_RECTYPE_L_TBL.LEAVE_EARNED_YTD |
| LES_EMP_DETAIL_LEAVE_TBL | LEAVE_USED_CPP | exp_Final.LEAVE_USED_CPP → exp_Initial.LEAVE_USED_CPP → SQ_LES_EMP_DETAIL_RECTYPE_L_TBL.LEAVE_USED_CPP → LES_EMP_DETAIL_RECTYPE_L_TBL.LEAVE_USED_CPP | LES_EMP_DETAIL_RECTYPE_L_TBL.LEAVE_USED_CPP |
| LES_EMP_DETAIL_LEAVE_TBL | LEAVE_USED_YTD | exp_Final.LEAVE_USED_YTD → exp_Initial.LEAVE_USED_YTD → SQ_LES_EMP_DETAIL_RECTYPE_L_TBL.LEAVE_USED_YTD → LES_EMP_DETAIL_RECTYPE_L_TBL.LEAVE_USED_YTD | LES_EMP_DETAIL_RECTYPE_L_TBL.LEAVE_USED_YTD |
| LES_EMP_DETAIL_LEAVE_TBL | LEAVE_DONATED | exp_Final.LEAVE_DONATED → exp_Initial.LEAVE_DONATED → SQ_LES_EMP_DETAIL_RECTYPE_L_TBL.LEAVE_DONATED → LES_EMP_DETAIL_RECTYPE_L_TBL.LEAVE_DONATED | LES_EMP_DETAIL_RECTYPE_L_TBL.LEAVE_DONATED |
| LES_EMP_DETAIL_LEAVE_TBL | LEAVE_CURR_BAL | exp_Final.LEAVE_CURR_BAL → exp_Initial.LEAVE_CURR_BAL → SQ_LES_EMP_DETAIL_RECTYPE_L_TBL.LEAVE_CURR_BAL → LES_EMP_DETAIL_RECTYPE_L_TBL.LEAVE_CURR_BAL | LES_EMP_DETAIL_RECTYPE_L_TBL.LEAVE_CURR_BAL |
| LES_EMP_DETAIL_LEAVE_TBL | LEAVE_USE_OR_LOSE_TERM_DTE | exp_Final.LEAVE_USE_OR_LOSE_TERM_DTE → exp_Initial.LEAVE_USE_OR_LOSE_TERM_DTE → SQ_LES_EMP_DETAIL_RECTYPE_L_TBL.LEAVE_USE_OR_LOSE_TERM_DTE → LES_EMP_DETAIL_RECTYPE_L_TBL.LEAVE_USE_OR_LOSE_TERM_DTE | LES_EMP_DETAIL_RECTYPE_L_TBL.LEAVE_USE_OR_LOSE_TERM_DTE |
| LES_EMP_DETAIL_LEAVE_TBL | LEAVE_USE_OR_LOSE_TERM_BAL_HRS | exp_Final.LEAVE_USE_OR_LOSE_TERM_BAL_HRS → exp_Initial.LEAVE_USE_OR_LOSE_TERM_BAL_HRS → SQ_LES_EMP_DETAIL_RECTYPE_L_TBL.LEAVE_USE_OR_LOSE_TERM_BAL_HRS → LES_EMP_DETAIL_RECTYPE_L_TBL.LEAVE_USE_OR_LOSE_TERM_BAL_HRS | LES_EMP_DETAIL_RECTYPE_L_TBL.LEAVE_USE_OR_LOSE_TERM_BAL_HRS |

## Mapping `m_LESRPT_Load_LESC`

- Sessions: `s_LESRPT_Load_LESC` (#23)
- Sources: `LES_EMP_DETAIL_RECTYPE_C_TBL`
- Target instances: `LESC`

### Transformation `SEQTRANS` (Sequence)

- **Start Value**: `0`
- **Increment By**: `1`
- **End Value**: `9223372036854775807`
- **Current Value**: `1825331`
- **Cycle**: `NO`
- **Number of Cached Values**: `0`
- **Reset**: `NO`

### Transformation `SQ_LES_EMP_DETAIL_RECTYPE_C_TBL` (Source Qualifier)

- **Sql Query**: `SELECT PP_END_YEAR, PP_NUM, LES_NUMBER, PSEUDOSSN, CURR_EARN_ID, CURR_EARN_NAME1, CURR_EARN_NAME1_HOURS, CURR_EARN_NAME1_AMT, CURR_EARN_NAME2, CURR_EARN_NAME2_HOURS, CURR_EARN_NAME2_AMT, CURR_EARN_NAME3, CURR_EARN_NAME3_HOURS, CURR_EARN_NAME3_AMT FROM LES_EMP_DETAIL_RECTYPE_C_TBL WHERE PP_END_YEAR = $$MAP_PP_END_YEAR AND PP_NUM = $$MAP_PP_NUM ORDER BY 1, 2, 3, 4, 5`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `lkp_LESC_KEY` (Lookup Procedure)

- **Lookup Sql Override**: `SELECT MAX(LESC.LESC_KEY) as LESC_KEY FROM LESC`
- **Lookup table name**: `LESC`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `LESC_KEY >= in_KEY`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

- Sequence `SEQTRANS`: start=0 current=1825331 increment=1 cycle=NO reset=NO → LESC
- Lookup `lkp_LESC_KEY`: table `LESC` (exists in export: **True**), condition `LESC_KEY >= in_KEY`, multiple-match policy `Use Any Value`.
- SQL override `SQ_LES_EMP_DETAIL_RECTYPE_C_TBL` positional bindings: 1 → `PP_END_YEAR` = `PP_END_YEAR`; 2 → `PP_NUM` = `PP_NUM`; 3 → `LES_NUMBER` = `LES_NUMBER`; 4 → `PSEUDOSSN` = `PSEUDOSSN`; 5 → `CURR_EARN_ID` = `CURR_EARN_ID`; 6 → `CURR_EARN_NAME1` = `CURR_EARN_NAME1`; 7 → `CURR_EARN_NAME1_HOURS` = `CURR_EARN_NAME1_HOURS`; 8 → `CURR_EARN_NAME1_AMT` = `CURR_EARN_NAME1_AMT`; 9 → `CURR_EARN_NAME2` = `CURR_EARN_NAME2`; 10 → `CURR_EARN_NAME2_HOURS` = `CURR_EARN_NAME2_HOURS`; 11 → `CURR_EARN_NAME2_AMT` = `CURR_EARN_NAME2_AMT`; 12 → `CURR_EARN_NAME3` = `CURR_EARN_NAME3`; 13 → `CURR_EARN_NAME3_HOURS` = `CURR_EARN_NAME3_HOURS`; 14 → `CURR_EARN_NAME3_AMT` = `CURR_EARN_NAME3_AMT`
- Unconnected lookup call `exp_Initial.v_LKP_LESC_KEY`: `IIF(v_COUNTER = 1, :LKP.LKP_LESC_KEY(1), v_LKP_LESC_KEY )`.

### Target instance `LESC` (table `LESC`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LESC | LESC_KEY | exp_Final.LESC_KEY = v_LESC_KEY → exp_Final.v_LESC_KEY = IIF(v_PREV_LESC_KEY = 0 or ISNULL(v_PREV_LESC_KEY), MAX_LESC_KEY + 1, v_LESC_KEY + 1 ) → exp_Final.v_PREV_LESC_KEY = v_LESC_KEY → exp_Final.v_LESC_KEY (cycle/depth limit) → exp_Initial.o_MAX_LESC_KEY = v_LKP_LESC_KEY → exp_Initial.v_LKP_LESC_KEY = IIF(v_COUNTER = 1, :LKP.LKP_LESC_KEY(1), v_LKP_LESC_KEY ) → exp_Initial.v_COUNTER = IIF(v_COUNTER = 0 or ISNULL(v_COUNTER), 1, v_COUNTER + 1) | LKP_LESC_KEY (unconnected lookup LKP_LESC_KEY); literal/expression: IIF(v_COUNTER = 0 or ISNULL(v_COUNTER), 1, v_COUNTER + 1) |
| LESC | MASTER_ID | exp_Final.MASTER_ID → exp_Initial.LES_NUMBER → SQ_LES_EMP_DETAIL_RECTYPE_C_TBL.LES_NUMBER → LES_EMP_DETAIL_RECTYPE_C_TBL.LES_NUMBER | LES_EMP_DETAIL_RECTYPE_C_TBL.LES_NUMBER |
| LESC | SSN | exp_Final.SSN → exp_Initial.PSEUDOSSN → SQ_LES_EMP_DETAIL_RECTYPE_C_TBL.PSEUDOSSN → LES_EMP_DETAIL_RECTYPE_C_TBL.PSEUDOSSN | LES_EMP_DETAIL_RECTYPE_C_TBL.PSEUDOSSN |
| LESC | PYR | exp_Final.PYR → exp_Initial.PP_END_YEAR → SQ_LES_EMP_DETAIL_RECTYPE_C_TBL.PP_END_YEAR → LES_EMP_DETAIL_RECTYPE_C_TBL.PP_END_YEAR | LES_EMP_DETAIL_RECTYPE_C_TBL.PP_END_YEAR |
| LESC | PPN | exp_Final.PPN → exp_Initial.PP_NUM → SQ_LES_EMP_DETAIL_RECTYPE_C_TBL.PP_NUM → LES_EMP_DETAIL_RECTYPE_C_TBL.PP_NUM | LES_EMP_DETAIL_RECTYPE_C_TBL.PP_NUM |
| LESC | SEQ | (not connected — NULL) | — |
| LESC | CURR_ERN_NAME1 | exp_Final.CURR_ERN_NAME1 → exp_Initial.CURR_EARN_NAME1 → SQ_LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME1 → LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME1 | LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME1 |
| LESC | CURR_HRS_DAYS1 | exp_Final.CURR_HRS_DAYS1 → exp_Initial.CURR_EARN_NAME1_HOURS → SQ_LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME1_HOURS → LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME1_HOURS | LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME1_HOURS |
| LESC | CURR_AMT1 | exp_Final.CURR_AMT1 → exp_Initial.CURR_EARN_NAME1_AMT → SQ_LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME1_AMT → LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME1_AMT | LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME1_AMT |
| LESC | CURR_ERN_NAME2 | exp_Final.CURR_ERN_NAME2 → exp_Initial.CURR_EARN_NAME2 → SQ_LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME2 → LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME2 | LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME2 |
| LESC | CURR_HRS_DAYS2 | exp_Final.CURR_HRS_DAYS2 → exp_Initial.CURR_EARN_NAME2_HOURS → SQ_LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME2_HOURS → LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME2_HOURS | LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME2_HOURS |
| LESC | CURR_AMT2 | exp_Final.CURR_AMT2 → exp_Initial.CURR_EARN_NAME2_AMT → SQ_LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME2_AMT → LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME2_AMT | LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME2_AMT |
| LESC | CURR_ERN_NAME3 | exp_Final.CURR_ERN_NAME3 → exp_Initial.CURR_EARN_NAME3 → SQ_LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME3 → LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME3 | LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME3 |
| LESC | CURR_HRS_DAYS3 | exp_Final.CURR_HRS_DAYS3 → exp_Initial.CURR_EARN_NAME3_HOURS → SQ_LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME3_HOURS → LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME3_HOURS | LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME3_HOURS |
| LESC | CURR_AMT3 | exp_Final.CURR_AMT3 → exp_Initial.CURR_EARN_NAME3_AMT → SQ_LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME3_AMT → LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME3_AMT | LES_EMP_DETAIL_RECTYPE_C_TBL.CURR_EARN_NAME3_AMT |
| LESC | MAN | (not connected — NULL) | — |
| LESC | LOAD_NBR | exp_Final.o_LOAD_NBR = 1 | literal/expression: 1 |
| LESC | CREATE_DT | exp_Final.o_CREATE_DT = SESSSTARTTIME | literal/expression: SESSSTARTTIME |
| LESC | CREATE_BY | (not connected — NULL) | — |
| LESC | UPDATE_DT | (not connected — NULL) | — |
| LESC | UPDATE_BY | (not connected — NULL) | — |
| LESC | NEW_SEQ_NBR | exp_Final.NEW_SEQ_NBR → SEQTRANS.NEXTVAL [sequence start=0 increment=1 current=1825331 cycle=NO reset=NO] | SEQTRANS (generated) |

## Mapping `m_LESRPT_Load_LESD`

- Sessions: `s_LESRPT_Load_LESD` (#24)
- Sources: `LES_EMP_DETAIL_RECTYPE_D_TBL`
- Target instances: `LESD`

### Transformation `SEQTRANS` (Sequence)

- **Start Value**: `0`
- **Increment By**: `1`
- **End Value**: `9223372036854775807`
- **Current Value**: `10347492`
- **Cycle**: `NO`
- **Number of Cached Values**: `0`
- **Reset**: `NO`

### Transformation `SQ_LES_EMP_DETAIL_RECTYPE_D_TBL` (Source Qualifier)

- **Sql Query**: `SELECT PP_END_YEAR, PP_NUM, LES_NUMBER, PSEUDOSSN, DEDUCTION_ID, DEDUCTION_1_NAME, DEDUCTION_1_CODE, DEDUCTION_1_AMT, DEDUCTION_1_AMT_YTD, DEDUCTION_2_NAME, DEDUCTION_2_CODE, DEDUCTION_2_AMT, DEDUCTION_2_AMT_YTD FROM LES_EMP_DETAIL_RECTYPE_D_TBL WHERE PP_END_YEAR = $$MAP_PP_END_YEAR AND PP_NUM = $$MAP_PP_NUM ORDER BY 1, 2, 3, 4, 5`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `lkp_MAX_LESD_KEY` (Lookup Procedure)

- **Lookup Sql Override**: `SELECT MAX(LESD.LESD_KEY) as LESD_KEY FROM LESD`
- **Lookup table name**: `LESD`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `LESD_KEY >= in_KEY`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

- Sequence `SEQTRANS`: start=0 current=10347492 increment=1 cycle=NO reset=NO → LESD
- Lookup `lkp_MAX_LESD_KEY`: table `LESD` (exists in export: **True**), condition `LESD_KEY >= in_KEY`, multiple-match policy `Use Any Value`.
- SQL override `SQ_LES_EMP_DETAIL_RECTYPE_D_TBL` positional bindings: 1 → `PP_END_YEAR` = `PP_END_YEAR`; 2 → `PP_NUM` = `PP_NUM`; 3 → `LES_NUMBER` = `LES_NUMBER`; 4 → `PSEUDOSSN` = `PSEUDOSSN`; 5 → `DEDUCTION_ID` = `DEDUCTION_ID`; 6 → `DEDUCTION_1_NAME` = `DEDUCTION_1_NAME`; 7 → `DEDUCTION_1_CODE` = `DEDUCTION_1_CODE`; 8 → `DEDUCTION_1_AMT` = `DEDUCTION_1_AMT`; 9 → `DEDUCTION_1_AMT_YTD` = `DEDUCTION_1_AMT_YTD`; 10 → `DEDUCTION_2_NAME` = `DEDUCTION_2_NAME`; 11 → `DEDUCTION_2_CODE` = `DEDUCTION_2_CODE`; 12 → `DEDUCTION_2_AMT` = `DEDUCTION_2_AMT`; 13 → `DEDUCTION_2_AMT_YTD` = `DEDUCTION_2_AMT_YTD`
- Unconnected lookup call `exp_Initial.v_MAX_LESD_KEY`: `IIF(v_COUNTER = 1, :LKP.LKP_MAX_LESD_KEY(1), v_MAX_LESD_KEY)`.

### Target instance `LESD` (table `LESD`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LESD | LESD_KEY | exp_Final.o_LESD_KEY = v_LESD_KEY → exp_Final.v_LESD_KEY = IIF(v_PREV_LESD_KEY = 0 or ISNULL(v_PREV_LESD_KEY), MAX_LESD_KEY + 1, v_LESD_KEY + 1 ) → exp_Final.v_PREV_LESD_KEY = v_LESD_KEY → exp_Final.v_LESD_KEY (cycle/depth limit) → exp_Initial.o_MAX_LESD_KEY = v_MAX_LESD_KEY → exp_Initial.v_MAX_LESD_KEY = IIF(v_COUNTER = 1, :LKP.LKP_MAX_LESD_KEY(1), v_MAX_LESD_KEY) → exp_Initial.v_COUNTER = IIF(v_COUNTER = 0 or ISNULL(v_COUNTER), 1, v_COUNTER + 1) | LKP_MAX_LESD_KEY (unconnected lookup LKP_MAX_LESD_KEY); literal/expression: IIF(v_COUNTER = 0 or ISNULL(v_COUNTER), 1, v_COUNTER + 1) |
| LESD | MASTER_ID | exp_Final.MASTER_ID → exp_Initial.LES_NUMBER → SQ_LES_EMP_DETAIL_RECTYPE_D_TBL.LES_NUMBER → LES_EMP_DETAIL_RECTYPE_D_TBL.LES_NUMBER | LES_EMP_DETAIL_RECTYPE_D_TBL.LES_NUMBER |
| LESD | SSN | exp_Final.SSN → exp_Initial.PSEUDOSSN → SQ_LES_EMP_DETAIL_RECTYPE_D_TBL.PSEUDOSSN → LES_EMP_DETAIL_RECTYPE_D_TBL.PSEUDOSSN | LES_EMP_DETAIL_RECTYPE_D_TBL.PSEUDOSSN |
| LESD | PYR | exp_Final.PYR → exp_Initial.PP_END_YEAR → SQ_LES_EMP_DETAIL_RECTYPE_D_TBL.PP_END_YEAR → LES_EMP_DETAIL_RECTYPE_D_TBL.PP_END_YEAR | LES_EMP_DETAIL_RECTYPE_D_TBL.PP_END_YEAR |
| LESD | PPN | exp_Final.PPN → exp_Initial.PP_NUM → SQ_LES_EMP_DETAIL_RECTYPE_D_TBL.PP_NUM → LES_EMP_DETAIL_RECTYPE_D_TBL.PP_NUM | LES_EMP_DETAIL_RECTYPE_D_TBL.PP_NUM |
| LESD | SEQ | (not connected — NULL) | — |
| LESD | DED_NAME1 | exp_Final.DED_NAME1 → exp_Initial.DEDUCTION_1_NAME → SQ_LES_EMP_DETAIL_RECTYPE_D_TBL.DEDUCTION_1_NAME → LES_EMP_DETAIL_RECTYPE_D_TBL.DEDUCTION_1_NAME | LES_EMP_DETAIL_RECTYPE_D_TBL.DEDUCTION_1_NAME |
| LESD | DED_CODE1 | exp_Final.DED_CODE1 → exp_Initial.DEDUCTION_1_CODE → SQ_LES_EMP_DETAIL_RECTYPE_D_TBL.DEDUCTION_1_CODE → LES_EMP_DETAIL_RECTYPE_D_TBL.DEDUCTION_1_CODE | LES_EMP_DETAIL_RECTYPE_D_TBL.DEDUCTION_1_CODE |
| LESD | DED_AMT1 | exp_Final.DED_AMT1 → exp_Initial.DEDUCTION_1_AMT → SQ_LES_EMP_DETAIL_RECTYPE_D_TBL.DEDUCTION_1_AMT → LES_EMP_DETAIL_RECTYPE_D_TBL.DEDUCTION_1_AMT | LES_EMP_DETAIL_RECTYPE_D_TBL.DEDUCTION_1_AMT |
| LESD | DED_AMT_YTD1 | exp_Final.DED_AMT_YTD1 → exp_Initial.DEDUCTION_1_AMT_YTD → SQ_LES_EMP_DETAIL_RECTYPE_D_TBL.DEDUCTION_1_AMT_YTD → LES_EMP_DETAIL_RECTYPE_D_TBL.DEDUCTION_1_AMT_YTD | LES_EMP_DETAIL_RECTYPE_D_TBL.DEDUCTION_1_AMT_YTD |
| LESD | DED_NAME2 | exp_Final.DED_NAME2 → exp_Initial.DEDUCTION_2_NAME → SQ_LES_EMP_DETAIL_RECTYPE_D_TBL.DEDUCTION_2_NAME → LES_EMP_DETAIL_RECTYPE_D_TBL.DEDUCTION_2_NAME | LES_EMP_DETAIL_RECTYPE_D_TBL.DEDUCTION_2_NAME |
| LESD | DED_CODE2 | exp_Final.DED_CODE2 → exp_Initial.DEDUCTION_2_CODE → SQ_LES_EMP_DETAIL_RECTYPE_D_TBL.DEDUCTION_2_CODE → LES_EMP_DETAIL_RECTYPE_D_TBL.DEDUCTION_2_CODE | LES_EMP_DETAIL_RECTYPE_D_TBL.DEDUCTION_2_CODE |
| LESD | DED_AMT2 | exp_Final.DED_AMT2 → exp_Initial.DEDUCTION_2_AMT → SQ_LES_EMP_DETAIL_RECTYPE_D_TBL.DEDUCTION_2_AMT → LES_EMP_DETAIL_RECTYPE_D_TBL.DEDUCTION_2_AMT | LES_EMP_DETAIL_RECTYPE_D_TBL.DEDUCTION_2_AMT |
| LESD | DED_AMT_YTD2 | exp_Final.DED_AMT_YTD2 → exp_Initial.DEDUCTION_2_AMT_YTD → SQ_LES_EMP_DETAIL_RECTYPE_D_TBL.DEDUCTION_2_AMT_YTD → LES_EMP_DETAIL_RECTYPE_D_TBL.DEDUCTION_2_AMT_YTD | LES_EMP_DETAIL_RECTYPE_D_TBL.DEDUCTION_2_AMT_YTD |
| LESD | MAN | (not connected — NULL) | — |
| LESD | LOAD_NBR | exp_Final.o_LOAD_NBR = 1 | literal/expression: 1 |
| LESD | CREATE_DT | exp_Final.o_CREATE_DT = SESSSTARTTIME | literal/expression: SESSSTARTTIME |
| LESD | CREATE_BY | (not connected — NULL) | — |
| LESD | UPDATE_DT | (not connected — NULL) | — |
| LESD | UPDATE_BY | (not connected — NULL) | — |
| LESD | NEW_SEQ_NBR | exp_Final.NEW_SEQ_NBR → SEQTRANS.NEXTVAL [sequence start=0 increment=1 current=10347492 cycle=NO reset=NO] | SEQTRANS (generated) |

## Mapping `m_LESRPT_Load_LESL`

- Sessions: `s_LESRPT_Load_LESL` (#25)
- Sources: `LES_EMP_DETAIL_LEAVE_TBL`
- Target instances: `LESL`

### Transformation `SQ_LES_EMP_DETAIL_LEAVE_TBL` (Source Qualifier)

- **Sql Query**: `SELECT PP_END_YEAR, PP_NUM, LES_NUMBER, PSEUDOSSN, LEAVE_ID, LEAVE_NAME, LEAVE_PRIOR_YEAR_BAL, LEAVE_EARNED_CPP, LEAVE_EARNED_YTD, LEAVE_USED_CPP, LEAVE_USED_YTD, LEAVE_DONATED, LEAVE_CURR_BAL, LEAVE_USE_OR_LOSE_TERM_DTE, LEAVE_USE_OR_LOSE_TERM_BAL_HRS FROM LES_EMP_DETAIL_LEAVE_TBL WHERE PP_END_YEAR = $$MAP_PP_END_YEAR AND PP_NUM = $$MAP_PP_NUM ORDER BY 1, 2, 3, 4, 5`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `lkp_LESL_KEY` (Lookup Procedure)

- **Lookup Sql Override**: `SELECT MAX(LESL.LESL_KEY) as LESL_KEY FROM LESL`
- **Lookup table name**: `LESL`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `LESL_KEY >= in_KEY`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

- Lookup `lkp_LESL_KEY`: table `LESL` (exists in export: **True**), condition `LESL_KEY >= in_KEY`, multiple-match policy `Use Any Value`.
- SQL override `SQ_LES_EMP_DETAIL_LEAVE_TBL` positional bindings: 1 → `PP_END_YEAR` = `PP_END_YEAR`; 2 → `PP_NUM` = `PP_NUM`; 3 → `LES_NUMBER` = `LES_NUMBER`; 4 → `PSEUDOSSN` = `PSEUDOSSN`; 5 → `LEAVE_ID` = `LEAVE_ID`; 6 → `LEAVE_NAME` = `LEAVE_NAME`; 7 → `LEAVE_PRIOR_YEAR_BAL` = `LEAVE_PRIOR_YEAR_BAL`; 8 → `LEAVE_EARNED_CPP` = `LEAVE_EARNED_CPP`; 9 → `LEAVE_EARNED_YTD` = `LEAVE_EARNED_YTD`; 10 → `LEAVE_USED_CPP` = `LEAVE_USED_CPP`; 11 → `LEAVE_USED_YTD` = `LEAVE_USED_YTD`; 12 → `LEAVE_DONATED` = `LEAVE_DONATED`; 13 → `LEAVE_CURR_BAL` = `LEAVE_CURR_BAL`; 14 → `LEAVE_USE_OR_LOSE_TERM_DTE` = `LEAVE_USE_OR_LOSE_TERM_DTE`; 15 → `LEAVE_USE_OR_LOSE_TERM_BAL_HRS` = `LEAVE_USE_OR_LOSE_TERM_BAL_HRS`
- Unconnected lookup call `exp_Initial.v_LKP_LESL_KEY`: `IIF(v_COUNTER = 1, :LKP.LKP_LESL_KEY(1), v_LKP_LESL_KEY)`.

### Target instance `LESL` (table `LESL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LESL | LESL_KEY | exp_Final.o_LESL_KEY = v_LESL_KEY → exp_Final.v_LESL_KEY = IIF(v_PREV_LESL_KEY = 0 or ISNULL(v_PREV_LESL_KEY), MAX_LESL_KEY + 1, v_LESL_KEY + 1 ) → exp_Final.v_PREV_LESL_KEY = v_LESL_KEY → exp_Final.v_LESL_KEY (cycle/depth limit) → exp_Initial.o_MAX_LESL_KEY = v_LKP_LESL_KEY → exp_Initial.v_LKP_LESL_KEY = IIF(v_COUNTER = 1, :LKP.LKP_LESL_KEY(1), v_LKP_LESL_KEY) → exp_Initial.v_COUNTER = IIF(v_COUNTER = 0 or ISNULL(v_COUNTER), 1, v_COUNTER + 1) | LKP_LESL_KEY (unconnected lookup LKP_LESL_KEY); literal/expression: IIF(v_COUNTER = 0 or ISNULL(v_COUNTER), 1, v_COUNTER + 1) |
| LESL | MASTER_ID | exp_Final.MASTER_ID → exp_Initial.LES_NUMBER → SQ_LES_EMP_DETAIL_LEAVE_TBL.LES_NUMBER → LES_EMP_DETAIL_LEAVE_TBL.LES_NUMBER | LES_EMP_DETAIL_LEAVE_TBL.LES_NUMBER |
| LESL | SSN | exp_Final.SSN → exp_Initial.PSEUDOSSN → SQ_LES_EMP_DETAIL_LEAVE_TBL.PSEUDOSSN → LES_EMP_DETAIL_LEAVE_TBL.PSEUDOSSN | LES_EMP_DETAIL_LEAVE_TBL.PSEUDOSSN |
| LESL | PYR | exp_Final.PYR → exp_Initial.PP_END_YEAR → SQ_LES_EMP_DETAIL_LEAVE_TBL.PP_END_YEAR → LES_EMP_DETAIL_LEAVE_TBL.PP_END_YEAR | LES_EMP_DETAIL_LEAVE_TBL.PP_END_YEAR |
| LESL | PPN | exp_Final.PPN → exp_Initial.PP_NUM → SQ_LES_EMP_DETAIL_LEAVE_TBL.PP_NUM → LES_EMP_DETAIL_LEAVE_TBL.PP_NUM | LES_EMP_DETAIL_LEAVE_TBL.PP_NUM |
| LESL | SEQ | exp_Final.SEQ = TO_CHAR(v_SEQ_NBR) → exp_Final.v_SEQ_NBR = DECODE(TRUE, ISNULL(v_PREV_LES_NUMBER) OR v_PREV_LES_NUMBER = 0, 1, LES_NUMBER = v_PREV_LES_NUMBER, v_SEQ_NBR + 1, 1) → exp_Final.v_PREV_LES_NUMBER = LES_NUMBER → exp_Initial.LES_NUMBER → SQ_LES_EMP_DETAIL_LEAVE_TBL.LES_NUMBER → LES_EMP_DETAIL_LEAVE_TBL.LES_NUMBER | LES_EMP_DETAIL_LEAVE_TBL.LES_NUMBER |
| LESL | LV_NAME | exp_Final.LV_NAME → exp_Initial.LEAVE_NAME → SQ_LES_EMP_DETAIL_LEAVE_TBL.LEAVE_NAME → LES_EMP_DETAIL_LEAVE_TBL.LEAVE_NAME | LES_EMP_DETAIL_LEAVE_TBL.LEAVE_NAME |
| LESL | LV_PRIOR_YR_BAL | exp_Final.LV_PRIOR_YR_BAL → exp_Initial.LEAVE_PRIOR_YEAR_BAL → SQ_LES_EMP_DETAIL_LEAVE_TBL.LEAVE_PRIOR_YEAR_BAL → LES_EMP_DETAIL_LEAVE_TBL.LEAVE_PRIOR_YEAR_BAL | LES_EMP_DETAIL_LEAVE_TBL.LEAVE_PRIOR_YEAR_BAL |
| LESL | LV_ACCR_PP | exp_Final.LV_ACCR_PP → exp_Initial.LEAVE_EARNED_CPP → SQ_LES_EMP_DETAIL_LEAVE_TBL.LEAVE_EARNED_CPP → LES_EMP_DETAIL_LEAVE_TBL.LEAVE_EARNED_CPP | LES_EMP_DETAIL_LEAVE_TBL.LEAVE_EARNED_CPP |
| LESL | LV_ACCR_YTD | exp_Final.LV_ACCR_YTD → exp_Initial.LEAVE_EARNED_YTD → SQ_LES_EMP_DETAIL_LEAVE_TBL.LEAVE_EARNED_YTD → LES_EMP_DETAIL_LEAVE_TBL.LEAVE_EARNED_YTD | LES_EMP_DETAIL_LEAVE_TBL.LEAVE_EARNED_YTD |
| LESL | LV_USED_CURR_PP | exp_Final.LV_USED_CURR_PP → exp_Initial.LEAVE_USED_CPP → SQ_LES_EMP_DETAIL_LEAVE_TBL.LEAVE_USED_CPP → LES_EMP_DETAIL_LEAVE_TBL.LEAVE_USED_CPP | LES_EMP_DETAIL_LEAVE_TBL.LEAVE_USED_CPP |
| LESL | LV_USED_YTD | exp_Final.LV_USED_YTD → exp_Initial.LEAVE_USED_YTD → SQ_LES_EMP_DETAIL_LEAVE_TBL.LEAVE_USED_YTD → LES_EMP_DETAIL_LEAVE_TBL.LEAVE_USED_YTD | LES_EMP_DETAIL_LEAVE_TBL.LEAVE_USED_YTD |
| LESL | LV_DONATE_RET | exp_Final.LV_DONATE_RET → exp_Initial.LEAVE_DONATED → SQ_LES_EMP_DETAIL_LEAVE_TBL.LEAVE_DONATED → LES_EMP_DETAIL_LEAVE_TBL.LEAVE_DONATED | LES_EMP_DETAIL_LEAVE_TBL.LEAVE_DONATED |
| LESL | LV_CURR_BAL | exp_Final.LV_CURR_BAL → exp_Initial.LEAVE_CURR_BAL → SQ_LES_EMP_DETAIL_LEAVE_TBL.LEAVE_CURR_BAL → LES_EMP_DETAIL_LEAVE_TBL.LEAVE_CURR_BAL | LES_EMP_DETAIL_LEAVE_TBL.LEAVE_CURR_BAL |
| LESL | LV_TERM_DATE | exp_Final.o_LV_TERM_DATE = DECODE (TRUE, NOT ISNULL(LEAVE_USE_OR_LOSE_TERM_DTE), TO_CHAR(LEAVE_USE_OR_LOSE_TERM_DTE, 'MM/DD/YYYY'), NOT ISNULL(LEAVE_USE_OR_LOSE_TERM_BAL_HRS), TO_CHAR(LEAVE_USE_OR_LOSE_TERM_BAL_HRS), ' ') → exp_Initial.LEAVE_USE_OR_LOSE_TERM_DTE → SQ_LES_EMP_DETAIL_LEAVE_TBL.LEAVE_USE_OR_LOSE_TERM_DTE → LES_EMP_DETAIL_LEAVE_TBL.LEAVE_USE_OR_LOSE_TERM_DTE → exp_Initial.LEAVE_USE_OR_LOSE_TERM_BAL_HRS → SQ_LES_EMP_DETAIL_LEAVE_TBL.LEAVE_USE_OR_LOSE_TERM_BAL_HRS → LES_EMP_DETAIL_LEAVE_TBL.LEAVE_USE_OR_LOSE_TERM_BAL_HRS | LES_EMP_DETAIL_LEAVE_TBL.LEAVE_USE_OR_LOSE_TERM_BAL_HRS; LES_EMP_DETAIL_LEAVE_TBL.LEAVE_USE_OR_LOSE_TERM_DTE |
| LESL | MAN | (not connected — NULL) | — |
| LESL | LOAD_NBR | exp_Final.o_LOAD_NBR = 1 | literal/expression: 1 |
| LESL | CREATE_DT | exp_Final.o_CREATE_DT = SESSSTARTTIME | literal/expression: SESSSTARTTIME |
| LESL | CREATE_BY | (not connected — NULL) | — |
| LESL | UPDATE_DT | (not connected — NULL) | — |
| LESL | UPDATE_BY | (not connected — NULL) | — |
| LESL | NEW_SEQ_NBR | exp_Final.SEQ = TO_CHAR(v_SEQ_NBR) → exp_Final.v_SEQ_NBR = DECODE(TRUE, ISNULL(v_PREV_LES_NUMBER) OR v_PREV_LES_NUMBER = 0, 1, LES_NUMBER = v_PREV_LES_NUMBER, v_SEQ_NBR + 1, 1) → exp_Final.v_PREV_LES_NUMBER = LES_NUMBER → exp_Initial.LES_NUMBER → SQ_LES_EMP_DETAIL_LEAVE_TBL.LES_NUMBER → LES_EMP_DETAIL_LEAVE_TBL.LES_NUMBER | LES_EMP_DETAIL_LEAVE_TBL.LES_NUMBER |

## Mapping `m_LESRPT_Load_LESM`

- Sessions: `s_LESRPT_Load_LESM` (#26)
- Sources: `LES_EMP_DETAIL_RECTYPE_M_TBL`
- Target instances: `LESM`

### Transformation `SQ_LES_EMP_DETAIL_RECTYPE_M_TBL` (Source Qualifier)

- **Source Filter**: `PP_END_YEAR = $$MAP_PP_END_YEAR AND PP_NUM = $$MAP_PP_NUM`
- **Number Of Sorted Ports**: `5`
- **Select Distinct**: `NO`

### Transformation `lkp_LESM_KEY` (Lookup Procedure)

- **Lookup Sql Override**: `SELECT MAX(LESM.LESM_KEY) as LESM_KEY FROM LESM`
- **Lookup table name**: `LESM`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `LESM_KEY >= in_KEY`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

- Lookup `lkp_LESM_KEY`: table `LESM` (exists in export: **True**), condition `LESM_KEY >= in_KEY`, multiple-match policy `Use Any Value`.
- Unconnected lookup call `exp_Initial.v_LKP_LESM_KEY`: `IIF(v_COUNTER = 1, :LKP.LKP_LESM_KEY(1), v_LKP_LESM_KEY)`.

### Target instance `LESM` (table `LESM`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LESM | LESM_KEY | exp_Final.LESM_KEY = v_LESM_KEY → exp_Final.v_LESM_KEY = IIF(v_PREV_LESM_KEY = 0 or ISNULL(v_PREV_LESM_KEY), MAX_LESM_KEY + 1, v_LESM_KEY + 1 ) → exp_Final.v_PREV_LESM_KEY = v_LESM_KEY → exp_Final.v_LESM_KEY (cycle/depth limit) → exp_Initial.o_MAX_LESM_KEY = v_LKP_LESM_KEY → exp_Initial.v_LKP_LESM_KEY = IIF(v_COUNTER = 1, :LKP.LKP_LESM_KEY(1), v_LKP_LESM_KEY) → exp_Initial.v_COUNTER = IIF(v_COUNTER = 0 or ISNULL(v_COUNTER), 1, v_COUNTER + 1) | LKP_LESM_KEY (unconnected lookup LKP_LESM_KEY); literal/expression: IIF(v_COUNTER = 0 or ISNULL(v_COUNTER), 1, v_COUNTER + 1) |
| LESM | MASTER_ID | exp_Final.MASTER_ID → exp_Initial.LES_NUMBER → SQ_LES_EMP_DETAIL_RECTYPE_M_TBL.LES_NUMBER → LES_EMP_DETAIL_RECTYPE_M_TBL.LES_NUMBER | LES_EMP_DETAIL_RECTYPE_M_TBL.LES_NUMBER |
| LESM | SSN | exp_Final.SSN → exp_Initial.PSEUDOSSN → SQ_LES_EMP_DETAIL_RECTYPE_M_TBL.PSEUDOSSN → LES_EMP_DETAIL_RECTYPE_M_TBL.PSEUDOSSN | LES_EMP_DETAIL_RECTYPE_M_TBL.PSEUDOSSN |
| LESM | PYR | exp_Final.PYR → exp_Initial.PP_END_YEAR → SQ_LES_EMP_DETAIL_RECTYPE_M_TBL.PP_END_YEAR → LES_EMP_DETAIL_RECTYPE_M_TBL.PP_END_YEAR | LES_EMP_DETAIL_RECTYPE_M_TBL.PP_END_YEAR |
| LESM | PPN | exp_Final.PPN → exp_Initial.PP_NUM → SQ_LES_EMP_DETAIL_RECTYPE_M_TBL.PP_NUM → LES_EMP_DETAIL_RECTYPE_M_TBL.PP_NUM | LES_EMP_DETAIL_RECTYPE_M_TBL.PP_NUM |
| LESM | SEQ | exp_Final.SEQ → exp_Initial.REMARK_ID → SQ_LES_EMP_DETAIL_RECTYPE_M_TBL.REMARK_ID → LES_EMP_DETAIL_RECTYPE_M_TBL.REMARK_ID | LES_EMP_DETAIL_RECTYPE_M_TBL.REMARK_ID |
| LESM | RMK_MSG | exp_Final.RMK_MSG → exp_Initial.REMARK_TEXT → SQ_LES_EMP_DETAIL_RECTYPE_M_TBL.REMARK_TEXT → LES_EMP_DETAIL_RECTYPE_M_TBL.REMARK_TEXT | LES_EMP_DETAIL_RECTYPE_M_TBL.REMARK_TEXT |
| LESM | MAN | (not connected — NULL) | — |
| LESM | LOAD_NBR | exp_Final.o_LOAD_NBR = 1 | literal/expression: 1 |
| LESM | CREATE_DT | (not connected — NULL) | — |
| LESM | CREATE_BY | (not connected — NULL) | — |
| LESM | UPDATE_DT | (not connected — NULL) | — |
| LESM | UPDATE_BY | (not connected — NULL) | — |
| LESM | NEW_SEQ_NBR | exp_Final.NEW_SEQ_NBR → exp_Initial.REMARK_ID → SQ_LES_EMP_DETAIL_RECTYPE_M_TBL.REMARK_ID → LES_EMP_DETAIL_RECTYPE_M_TBL.REMARK_ID | LES_EMP_DETAIL_RECTYPE_M_TBL.REMARK_ID |

## Mapping `m_LESRPT_Load_LESR`

- Sessions: `s_LESRPT_Load_LESR` (#27)
- Sources: `LES_EMP_DETAIL_RECTYPE_R_TBL`
- Target instances: `LESR`

### Transformation `SEQTRANS` (Sequence)

- **Start Value**: `258630`
- **Increment By**: `1`
- **End Value**: `9223372036854775807`
- **Current Value**: `180666`
- **Cycle**: `NO`
- **Number of Cached Values**: `0`
- **Reset**: `NO`

### Transformation `SQ_LES_EMP_DETAIL_RECTYPE_R_TBL` (Source Qualifier)

- **Sql Query**: `SELECT PP_END_YEAR, PP_NUM, LES_NUMBER, PSEUDOSSN, RETRO_ACTIVE_ID, RETRO_ACTIVE_EARN_NAME1, RETRO_ACTIVE_EARN_NAME1_HOURS, RETRO_ACTIVE_EARN_NAME1_AMT, RETRO_ACTIVE_EARN_NAME2, RETRO_ACTIVE_EARN_NAME2_HOURS, RETRO_ACTIVE_EARN_NAME2_AMT, RETRO_ACTIVE_EARN_NAME3, RETRO_ACTIVE_EARN_NAME3_HOURS, RETRO_ACTIVE_EARN_NAME3_AMT FROM LES_EMP_DETAIL_RECTYPE_R_TBL WHERE PP_END_YEAR = $$MAP_PP_END_YEAR AND PP_NUM = $$MAP_PP_NUM ORDER BY 1, 2, 3, 4, 5`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `lkp_LESR_KEY` (Lookup Procedure)

- **Lookup Sql Override**: `SELECT MAX(LESR.LESR_KEY) as LESR_KEY FROM LESR`
- **Lookup table name**: `LESR`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `LESR_KEY >= in_KEY`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

- Sequence `SEQTRANS`: start=258630 current=180666 increment=1 cycle=NO reset=NO → LESR
- Lookup `lkp_LESR_KEY`: table `LESR` (exists in export: **True**), condition `LESR_KEY >= in_KEY`, multiple-match policy `Use Any Value`.
- SQL override `SQ_LES_EMP_DETAIL_RECTYPE_R_TBL` positional bindings: 1 → `PP_END_YEAR` = `PP_END_YEAR`; 2 → `PP_NUM` = `PP_NUM`; 3 → `LES_NUMBER` = `LES_NUMBER`; 4 → `PSEUDOSSN` = `PSEUDOSSN`; 5 → `RETRO_ACTIVE_ID` = `RETRO_ACTIVE_ID`; 6 → `RETRO_ACTIVE_EARN_NAME1` = `RETRO_ACTIVE_EARN_NAME1`; 7 → `RETRO_ACTIVE_EARN_NAME1_HOURS` = `RETRO_ACTIVE_EARN_NAME1_HOURS`; 8 → `RETRO_ACTIVE_EARN_NAME1_AMT` = `RETRO_ACTIVE_EARN_NAME1_AMT`; 9 → `RETRO_ACTIVE_EARN_NAME2` = `RETRO_ACTIVE_EARN_NAME2`; 10 → `RETRO_ACTIVE_EARN_NAME2_HOURS` = `RETRO_ACTIVE_EARN_NAME2_HOURS`; 11 → `RETRO_ACTIVE_EARN_NAME2_AMT` = `RETRO_ACTIVE_EARN_NAME2_AMT`; 12 → `RETRO_ACTIVE_EARN_NAME3` = `RETRO_ACTIVE_EARN_NAME3`; 13 → `RETRO_ACTIVE_EARN_NAME3_HOURS` = `RETRO_ACTIVE_EARN_NAME3_HOURS`; 14 → `RETRO_ACTIVE_EARN_NAME3_AMT` = `RETRO_ACTIVE_EARN_NAME3_AMT`
- Unconnected lookup call `exp_Initial.v_LKP_LESR_KEY`: `IIF(v_COUNTER = 1, :LKP.LKP_LESR_KEY(1), v_LKP_LESR_KEY)`.

### Target instance `LESR` (table `LESR`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LESR | LESR_KEY | exp_Final.o_LESR_KEY = v_LESR_KEY → exp_Final.v_LESR_KEY = IIF(v_PREV_LESR_KEY = 0 or ISNULL(v_PREV_LESR_KEY), MAX_LESR_KEY + 1, v_LESR_KEY + 1) → exp_Final.v_PREV_LESR_KEY = v_LESR_KEY → exp_Final.v_LESR_KEY (cycle/depth limit) → exp_Initial.o_MAX_LESR_KEY = v_LKP_LESR_KEY → exp_Initial.v_LKP_LESR_KEY = IIF(v_COUNTER = 1, :LKP.LKP_LESR_KEY(1), v_LKP_LESR_KEY) → exp_Initial.v_COUNTER = IIF(v_COUNTER = 0 or ISNULL(v_COUNTER), 1, v_COUNTER + 1) | LKP_LESR_KEY (unconnected lookup LKP_LESR_KEY); literal/expression: IIF(v_COUNTER = 0 or ISNULL(v_COUNTER), 1, v_COUNTER + 1) |
| LESR | MASTER_ID | exp_Final.MASTER_ID → exp_Initial.LES_NUMBER → SQ_LES_EMP_DETAIL_RECTYPE_R_TBL.LES_NUMBER → LES_EMP_DETAIL_RECTYPE_R_TBL.LES_NUMBER | LES_EMP_DETAIL_RECTYPE_R_TBL.LES_NUMBER |
| LESR | SSN | exp_Final.SSN → exp_Initial.PSEUDOSSN → SQ_LES_EMP_DETAIL_RECTYPE_R_TBL.PSEUDOSSN → LES_EMP_DETAIL_RECTYPE_R_TBL.PSEUDOSSN | LES_EMP_DETAIL_RECTYPE_R_TBL.PSEUDOSSN |
| LESR | PYR | exp_Final.PYR → exp_Initial.PP_END_YEAR → SQ_LES_EMP_DETAIL_RECTYPE_R_TBL.PP_END_YEAR → LES_EMP_DETAIL_RECTYPE_R_TBL.PP_END_YEAR | LES_EMP_DETAIL_RECTYPE_R_TBL.PP_END_YEAR |
| LESR | PPN | exp_Final.PPN → exp_Initial.PP_NUM → SQ_LES_EMP_DETAIL_RECTYPE_R_TBL.PP_NUM → LES_EMP_DETAIL_RECTYPE_R_TBL.PP_NUM | LES_EMP_DETAIL_RECTYPE_R_TBL.PP_NUM |
| LESR | SEQ | (not connected — NULL) | — |
| LESR | RETR_ERN_NAME1 | exp_Final.RETR_ERN_NAME1 → exp_Initial.RETRO_ACTIVE_EARN_NAME1 → SQ_LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME1 → LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME1 | LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME1 |
| LESR | RETR_HRS_DAYS1 | exp_Final.RETR_HRS_DAYS1 → exp_Initial.RETRO_ACTIVE_EARN_NAME1_HOURS → SQ_LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME1_HOURS → LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME1_HOURS | LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME1_HOURS |
| LESR | RETR_AMT1 | exp_Final.RETR_AMT1 → exp_Initial.RETRO_ACTIVE_EARN_NAME1_AMT → SQ_LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME1_AMT → LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME1_AMT | LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME1_AMT |
| LESR | RETR_ERN_NAME2 | exp_Final.RETR_ERN_NAME2 → exp_Initial.RETRO_ACTIVE_EARN_NAME2 → SQ_LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME2 → LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME2 | LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME2 |
| LESR | RETR_HRS_DAYS2 | exp_Final.RETR_HRS_DAYS2 → exp_Initial.RETRO_ACTIVE_EARN_NAME2_HOURS → SQ_LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME2_HOURS → LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME2_HOURS | LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME2_HOURS |
| LESR | RETR_AMT2 | exp_Final.RETR_AMT2 → exp_Initial.RETRO_ACTIVE_EARN_NAME2_AMT → SQ_LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME2_AMT → LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME2_AMT | LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME2_AMT |
| LESR | RETR_ERN_NAME3 | exp_Final.RETR_ERN_NAME3 → exp_Initial.RETRO_ACTIVE_EARN_NAME3 → SQ_LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME3 → LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME3 | LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME3 |
| LESR | RETR_HRS_DAYS3 | exp_Final.RETR_HRS_DAYS3 → exp_Initial.RETRO_ACTIVE_EARN_NAME3_HOURS → SQ_LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME3_HOURS → LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME3_HOURS | LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME3_HOURS |
| LESR | RETR_AMT3 | exp_Final.RETR_AMT3 → exp_Initial.RETRO_ACTIVE_EARN_NAME3_AMT → SQ_LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME3_AMT → LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME3_AMT | LES_EMP_DETAIL_RECTYPE_R_TBL.RETRO_ACTIVE_EARN_NAME3_AMT |
| LESR | MAN | (not connected — NULL) | — |
| LESR | LOAD_NBR | exp_Final.o_LOAD_NBR = 1 | literal/expression: 1 |
| LESR | CREATE_DT | exp_Final.o_CREATE_DT = SESSSTARTTIME | literal/expression: SESSSTARTTIME |
| LESR | CREATE_BY | (not connected — NULL) | — |
| LESR | UPDATE_DT | (not connected — NULL) | — |
| LESR | UPDATE_BY | (not connected — NULL) | — |
| LESR | NEW_SEQ_NBR | exp_Final.NEW_SEQ_NBR → SEQTRANS.NEXTVAL [sequence start=258630 increment=1 current=180666 cycle=NO reset=NO] | SEQTRANS (generated) |

## Mapping `m_LESRPT_Load_LESS`

- Sessions: `s_LESRPT_Load_LESS` (#28)
- Sources: `LES_PRIMARY_DATA_TBL`
- Target instances: `LESS`

### Transformation `SQ_LES_PRIMARY_DATA_TBL` (Source Qualifier)

- **Source Filter**: `PP_END_YEAR = $$MAP_PP_END_YEAR AND PP_NUM = $$MAP_PP_NUM`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `lkp_MAX_LESS_KEY` (Lookup Procedure)

- **Lookup Sql Override**: `SELECT MAX(LESS.LESS_KEY) as LESS_KEY FROM LESS`
- **Lookup table name**: `LESS`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `LESS_KEY >= in_KEY`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

- Lookup `lkp_MAX_LESS_KEY`: table `LESS` (exists in export: **True**), condition `LESS_KEY >= in_KEY`, multiple-match policy `Use Any Value`.
- Unconnected lookup call `exp_Initial.v_LKP_LESS_KEY`: `IIF(v_COUNTER = 1, :LKP.LKP_MAX_LESS_KEY(1), v_LKP_LESS_KEY)`.

### Target instance `LESS` (table `LESS`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LESS | LESS_KEY | exp_Final.LESS_KEY = v_LESS_KEY → exp_Final.v_LESS_KEY = IIF(v_PREV_LESS_KEY = 0 or ISNULL(v_PREV_LESS_KEY), MAX_LESS_KEY + 1, v_LESS_KEY + 1 ) → exp_Final.v_PREV_LESS_KEY = v_LESS_KEY → exp_Final.v_LESS_KEY (cycle/depth limit) → exp_Initial.o_MAX_LESS_KEY = v_LKP_LESS_KEY → exp_Initial.v_LKP_LESS_KEY = IIF(v_COUNTER = 1, :LKP.LKP_MAX_LESS_KEY(1), v_LKP_LESS_KEY) → exp_Initial.v_COUNTER = IIF(v_COUNTER = 0 or ISNULL(v_COUNTER), 1, v_COUNTER + 1) | LKP_MAX_LESS_KEY (unconnected lookup LKP_MAX_LESS_KEY); literal/expression: IIF(v_COUNTER = 0 or ISNULL(v_COUNTER), 1, v_COUNTER + 1) |
| LESS | MASTER_ID | exp_Final.MASTER_ID → exp_Initial.LES_NUMBER → SQ_LES_PRIMARY_DATA_TBL.LES_NUMBER → LES_PRIMARY_DATA_TBL.LES_NUMBER | LES_PRIMARY_DATA_TBL.LES_NUMBER |
| LESS | SSN | exp_Final.SSN → exp_Initial.PSEUDOSSN → SQ_LES_PRIMARY_DATA_TBL.PSEUDOSSN → LES_PRIMARY_DATA_TBL.PSEUDOSSN | LES_PRIMARY_DATA_TBL.PSEUDOSSN |
| LESS | PYR | exp_Final.PYR → exp_Initial.PP_END_YEAR → SQ_LES_PRIMARY_DATA_TBL.PP_END_YEAR → LES_PRIMARY_DATA_TBL.PP_END_YEAR | LES_PRIMARY_DATA_TBL.PP_END_YEAR |
| LESS | PPN | exp_Final.PPN → exp_Initial.PP_NUM → SQ_LES_PRIMARY_DATA_TBL.PP_NUM → LES_PRIMARY_DATA_TBL.PP_NUM | LES_PRIMARY_DATA_TBL.PP_NUM |
| LESS | TKN | exp_Final.TKN → exp_Initial.TK_NUM → SQ_LES_PRIMARY_DATA_TBL.TK_NUM → LES_PRIMARY_DATA_TBL.TK_NUM | LES_PRIMARY_DATA_TBL.TK_NUM |
| LESS | PPD_END_DT | exp_Final.PPD_END_DT → exp_Initial.PP_END_DTE → SQ_LES_PRIMARY_DATA_TBL.PP_END_DTE → LES_PRIMARY_DATA_TBL.PP_END_DTE | LES_PRIMARY_DATA_TBL.PP_END_DTE |
| LESS | PAY_DT | exp_Final.PAY_DT → exp_Initial.PAY_DTE → SQ_LES_PRIMARY_DATA_TBL.PAY_DTE → LES_PRIMARY_DATA_TBL.PAY_DTE | LES_PRIMARY_DATA_TBL.PAY_DTE |
| LESS | EYE_NME | exp_Final.EYE_NME → exp_Initial.EMPLOYEE_NAME → SQ_LES_PRIMARY_DATA_TBL.EMPLOYEE_NAME → LES_PRIMARY_DATA_TBL.EMPLOYEE_NAME | LES_PRIMARY_DATA_TBL.EMPLOYEE_NAME |
| LESS | PAY_PLAN | exp_Final.PAY_PLAN → exp_Initial.PAY_PLAN_CD → SQ_LES_PRIMARY_DATA_TBL.PAY_PLAN_CD → LES_PRIMARY_DATA_TBL.PAY_PLAN_CD | LES_PRIMARY_DATA_TBL.PAY_PLAN_CD |
| LESS | PAY_GRADE | exp_Final.PAY_GRADE → exp_Initial.GRADE → SQ_LES_PRIMARY_DATA_TBL.GRADE → LES_PRIMARY_DATA_TBL.GRADE | LES_PRIMARY_DATA_TBL.GRADE |
| LESS | PAY_STEP | exp_Final.PAY_STEP → exp_Initial.STEP → SQ_LES_PRIMARY_DATA_TBL.STEP → LES_PRIMARY_DATA_TBL.STEP | LES_PRIMARY_DATA_TBL.STEP |
| LESS | HRLY_RATE | exp_Final.HRLY_RATE → exp_Initial.HRLY_RATE → SQ_LES_PRIMARY_DATA_TBL.HRLY_RATE → LES_PRIMARY_DATA_TBL.HRLY_RATE | LES_PRIMARY_DATA_TBL.HRLY_RATE |
| LESS | BASIC_OT_RATE | exp_Final.BASIC_OT_RATE → exp_Initial.BASE_OT_RATE → SQ_LES_PRIMARY_DATA_TBL.BASE_OT_RATE → LES_PRIMARY_DATA_TBL.BASE_OT_RATE | LES_PRIMARY_DATA_TBL.BASE_OT_RATE |
| LESS | BASIC_PAY | exp_Final.BASIC_PAY → exp_Initial.BASE_PAY → SQ_LES_PRIMARY_DATA_TBL.BASE_PAY → LES_PRIMARY_DATA_TBL.BASE_PAY | LES_PRIMARY_DATA_TBL.BASE_PAY |
| LESS | LOCAL_ADJ | exp_Final.LOCAL_ADJ → exp_Initial.LOCALITY_ADJ → SQ_LES_PRIMARY_DATA_TBL.LOCALITY_ADJ → LES_PRIMARY_DATA_TBL.LOCALITY_ADJ | LES_PRIMARY_DATA_TBL.LOCALITY_ADJ |
| LESS | ADJ_BASIC_PAY | exp_Final.ADJ_BASIC_PAY → exp_Initial.ADJ_BASE_PAY → SQ_LES_PRIMARY_DATA_TBL.ADJ_BASE_PAY → LES_PRIMARY_DATA_TBL.ADJ_BASE_PAY | LES_PRIMARY_DATA_TBL.ADJ_BASE_PAY |
| LESS | LOCAL_PCT | exp_Final.LOCAL_PCT → exp_Initial.LOCALITY_PERCENTAGE → SQ_LES_PRIMARY_DATA_TBL.LOCALITY_PERCENTAGE → LES_PRIMARY_DATA_TBL.LOCALITY_PERCENTAGE | LES_PRIMARY_DATA_TBL.LOCALITY_PERCENTAGE |
| LESS | FLSA | exp_Final.FLSA → exp_Initial.FLSA_STATUS → SQ_LES_PRIMARY_DATA_TBL.FLSA_STATUS → LES_PRIMARY_DATA_TBL.FLSA_STATUS | LES_PRIMARY_DATA_TBL.FLSA_STATUS |
| LESS | SCD_LEAVE_DT | exp_Final.SCD_LEAVE_DT → exp_Initial.LV_SCD_DTE → SQ_LES_PRIMARY_DATA_TBL.LV_SCD_DTE → LES_PRIMARY_DATA_TBL.LV_SCD_DTE | LES_PRIMARY_DATA_TBL.LV_SCD_DTE |
| LESS | MAX_LV_CRY | exp_Final.MAX_LV_CRY → exp_Initial.MIL_LV_CARRY → SQ_LES_PRIMARY_DATA_TBL.MIL_LV_CARRY → LES_PRIMARY_DATA_TBL.MIL_LV_CARRY | LES_PRIMARY_DATA_TBL.MIL_LV_CARRY |
| LESS | LV_YR_END_DT | exp_Final.LV_YR_END_DT → exp_Initial.LV_YR_END_DTE → SQ_LES_PRIMARY_DATA_TBL.LV_YR_END_DTE → LES_PRIMARY_DATA_TBL.LV_YR_END_DTE | LES_PRIMARY_DATA_TBL.LV_YR_END_DTE |
| LESS | DATE_LST_INC | exp_Final.DATE_LST_INC → exp_Initial.LAST_INCREASE_DTE → SQ_LES_PRIMARY_DATA_TBL.LAST_INCREASE_DTE → LES_PRIMARY_DATA_TBL.LAST_INCREASE_DTE | LES_PRIMARY_DATA_TBL.LAST_INCREASE_DTE |
| LESS | NETPAY_FINORG | exp_Final.NETPAY_FINORG → exp_Initial.NET_PAY_FINANCIAL_ORG → SQ_LES_PRIMARY_DATA_TBL.NET_PAY_FINANCIAL_ORG → LES_PRIMARY_DATA_TBL.NET_PAY_FINANCIAL_ORG | LES_PRIMARY_DATA_TBL.NET_PAY_FINANCIAL_ORG |
| LESS | ALLT1_FINORG | exp_Final.ALLT1_FINORG → exp_Initial.ALLOT1_FINANCIAL_ORG → SQ_LES_PRIMARY_DATA_TBL.ALLOT1_FINANCIAL_ORG → LES_PRIMARY_DATA_TBL.ALLOT1_FINANCIAL_ORG | LES_PRIMARY_DATA_TBL.ALLOT1_FINANCIAL_ORG |
| LESS | ALLT2_FINORG | exp_Final.ALLT2_FINORG → exp_Initial.ALLOT2_FINANCIAL_ORG → SQ_LES_PRIMARY_DATA_TBL.ALLOT2_FINANCIAL_ORG → LES_PRIMARY_DATA_TBL.ALLOT2_FINANCIAL_ORG | LES_PRIMARY_DATA_TBL.ALLOT2_FINANCIAL_ORG |
| LESS | FED_TIT | exp_Final.FED_TIT → exp_Initial.FEDERAL_TAX → SQ_LES_PRIMARY_DATA_TBL.FEDERAL_TAX → LES_PRIMARY_DATA_TBL.FEDERAL_TAX | LES_PRIMARY_DATA_TBL.FEDERAL_TAX |
| LESS | FED_MS | exp_Final.FED_MS → exp_Initial.FED_MARITAL_STATUS → SQ_LES_PRIMARY_DATA_TBL.FED_MARITAL_STATUS → LES_PRIMARY_DATA_TBL.FED_MARITAL_STATUS | LES_PRIMARY_DATA_TBL.FED_MARITAL_STATUS |
| LESS | FED_ITW_XMP | exp_Final.FED_ITW_XMP → exp_Initial.FED_EXCEPTIONS → SQ_LES_PRIMARY_DATA_TBL.FED_EXCEPTIONS → LES_PRIMARY_DATA_TBL.FED_EXCEPTIONS | LES_PRIMARY_DATA_TBL.FED_EXCEPTIONS |
| LESS | FED_ADDTL | exp_Final.FED_ADDTL → exp_Initial.FED_ADDNL_WITHHOLDING → SQ_LES_PRIMARY_DATA_TBL.FED_ADDNL_WITHHOLDING → LES_PRIMARY_DATA_TBL.FED_ADDNL_WITHHOLDING | LES_PRIMARY_DATA_TBL.FED_ADDNL_WITHHOLDING |
| LESS | ST_TX1_TIT | exp_Final.ST_TX1_TIT → exp_Initial.STATE1_TAX → SQ_LES_PRIMARY_DATA_TBL.STATE1_TAX → LES_PRIMARY_DATA_TBL.STATE1_TAX | LES_PRIMARY_DATA_TBL.STATE1_TAX |
| LESS | ST_TX1_MS | exp_Final.ST_TX1_MS → exp_Initial.STATE1_MARITAL_STATUS → SQ_LES_PRIMARY_DATA_TBL.STATE1_MARITAL_STATUS → LES_PRIMARY_DATA_TBL.STATE1_MARITAL_STATUS | LES_PRIMARY_DATA_TBL.STATE1_MARITAL_STATUS |
| LESS | ST_TX1_XMP | exp_Final.ST_TX1_XMP → exp_Initial.STATE1_EXCEPTIONS → SQ_LES_PRIMARY_DATA_TBL.STATE1_EXCEPTIONS → LES_PRIMARY_DATA_TBL.STATE1_EXCEPTIONS | LES_PRIMARY_DATA_TBL.STATE1_EXCEPTIONS |
| LESS | ST_TX1_ADDTL | exp_Final.ST_TX1_ADDTL → exp_Initial.STATE1_ADDNL_AMOUNT → SQ_LES_PRIMARY_DATA_TBL.STATE1_ADDNL_AMOUNT → LES_PRIMARY_DATA_TBL.STATE1_ADDNL_AMOUNT | LES_PRIMARY_DATA_TBL.STATE1_ADDNL_AMOUNT |
| LESS | ST_TX2_TIT | exp_Final.ST_TX2_TIT → exp_Initial.STATE2_TAX → SQ_LES_PRIMARY_DATA_TBL.STATE2_TAX → LES_PRIMARY_DATA_TBL.STATE2_TAX | LES_PRIMARY_DATA_TBL.STATE2_TAX |
| LESS | ST_TX2_MS | exp_Final.ST_TX2_MS → exp_Initial.STATE2_MARITAL_STATUS → SQ_LES_PRIMARY_DATA_TBL.STATE2_MARITAL_STATUS → LES_PRIMARY_DATA_TBL.STATE2_MARITAL_STATUS | LES_PRIMARY_DATA_TBL.STATE2_MARITAL_STATUS |
| LESS | ST_TX2_XMP | exp_Final.ST_TX2_XMP → exp_Initial.STATE2_EXCEPTIONS → SQ_LES_PRIMARY_DATA_TBL.STATE2_EXCEPTIONS → LES_PRIMARY_DATA_TBL.STATE2_EXCEPTIONS | LES_PRIMARY_DATA_TBL.STATE2_EXCEPTIONS |
| LESS | ST_TX2_ADDTL | exp_Final.ST_TX2_ADDTL → exp_Initial.STATE2_ADDNL_AMOUNT → SQ_LES_PRIMARY_DATA_TBL.STATE2_ADDNL_AMOUNT → LES_PRIMARY_DATA_TBL.STATE2_ADDNL_AMOUNT | LES_PRIMARY_DATA_TBL.STATE2_ADDNL_AMOUNT |
| LESS | LC_TX1_TIT | exp_Final.LC_TX1_TIT → exp_Initial.LOCAL1_TAX → SQ_LES_PRIMARY_DATA_TBL.LOCAL1_TAX → LES_PRIMARY_DATA_TBL.LOCAL1_TAX | LES_PRIMARY_DATA_TBL.LOCAL1_TAX |
| LESS | LC_TX1_MS | exp_Final.LC_TX1_MS → exp_Initial.LOCAL1_MARITAL_STATUS → SQ_LES_PRIMARY_DATA_TBL.LOCAL1_MARITAL_STATUS → LES_PRIMARY_DATA_TBL.LOCAL1_MARITAL_STATUS | LES_PRIMARY_DATA_TBL.LOCAL1_MARITAL_STATUS |
| LESS | LC_TX1_XMP | exp_Final.LC_TX1_XMP → exp_Initial.LOCAL1_EXCEPTIONS → SQ_LES_PRIMARY_DATA_TBL.LOCAL1_EXCEPTIONS → LES_PRIMARY_DATA_TBL.LOCAL1_EXCEPTIONS | LES_PRIMARY_DATA_TBL.LOCAL1_EXCEPTIONS |
| LESS | LC_TX1_ADDTL | exp_Final.LC_TX1_ADDTL → exp_Initial.LOCAL1_ADDNL_AMOUNT → SQ_LES_PRIMARY_DATA_TBL.LOCAL1_ADDNL_AMOUNT → LES_PRIMARY_DATA_TBL.LOCAL1_ADDNL_AMOUNT | LES_PRIMARY_DATA_TBL.LOCAL1_ADDNL_AMOUNT |
| LESS | LC_TX1_NME | exp_Final.LC_TX1_NME → exp_Initial.LOCAL1_TAX_NAME → SQ_LES_PRIMARY_DATA_TBL.LOCAL1_TAX_NAME → LES_PRIMARY_DATA_TBL.LOCAL1_TAX_NAME | LES_PRIMARY_DATA_TBL.LOCAL1_TAX_NAME |
| LESS | LC_TX2_TIT | exp_Final.LC_TX2_TIT → exp_Initial.LOCAL2_TAX → SQ_LES_PRIMARY_DATA_TBL.LOCAL2_TAX → LES_PRIMARY_DATA_TBL.LOCAL2_TAX | LES_PRIMARY_DATA_TBL.LOCAL2_TAX |
| LESS | LC_TX2_MS | exp_Final.LC_TX2_MS → exp_Initial.LOCAL2_MARITAL_STATUS → SQ_LES_PRIMARY_DATA_TBL.LOCAL2_MARITAL_STATUS → LES_PRIMARY_DATA_TBL.LOCAL2_MARITAL_STATUS | LES_PRIMARY_DATA_TBL.LOCAL2_MARITAL_STATUS |
| LESS | LC_TX2_XMP | exp_Final.LC_TX2_XMP → exp_Initial.LOCAL2_EXCEPTIONS → SQ_LES_PRIMARY_DATA_TBL.LOCAL2_EXCEPTIONS → LES_PRIMARY_DATA_TBL.LOCAL2_EXCEPTIONS | LES_PRIMARY_DATA_TBL.LOCAL2_EXCEPTIONS |
| LESS | LC_TX2_ADDTL | exp_Final.LC_TX2_ADDTL → exp_Initial.LOCAL2_ADDNL_AMOUNT → SQ_LES_PRIMARY_DATA_TBL.LOCAL2_ADDNL_AMOUNT → LES_PRIMARY_DATA_TBL.LOCAL2_ADDNL_AMOUNT | LES_PRIMARY_DATA_TBL.LOCAL2_ADDNL_AMOUNT |
| LESS | LC_TX2_NME | exp_Final.LC_TX2_NME → exp_Initial.LOCAL2_TAX_NAME → SQ_LES_PRIMARY_DATA_TBL.LOCAL2_TAX_NAME → LES_PRIMARY_DATA_TBL.LOCAL2_TAX_NAME | LES_PRIMARY_DATA_TBL.LOCAL2_TAX_NAME |
| LESS | CSRS_TIT | exp_Final.CSRS_TIT → exp_Initial.CSRS → SQ_LES_PRIMARY_DATA_TBL.CSRS → LES_PRIMARY_DATA_TBL.CSRS | LES_PRIMARY_DATA_TBL.CSRS |
| LESS | CSRS_CUMM_AMT | exp_Final.CSRS_CUMM_AMT → exp_Initial.CSRS_CUM_AMT → SQ_LES_PRIMARY_DATA_TBL.CSRS_CUM_AMT → LES_PRIMARY_DATA_TBL.CSRS_CUM_AMT | LES_PRIMARY_DATA_TBL.CSRS_CUM_AMT |
| LESS | BIWK_TIT | exp_Final.BIWK_TIT → exp_Initial.BIWEEKLY_AMT → SQ_LES_PRIMARY_DATA_TBL.BIWEEKLY_AMT → LES_PRIMARY_DATA_TBL.BIWEEKLY_AMT | LES_PRIMARY_DATA_TBL.BIWEEKLY_AMT |
| LESS | BIWK_ANNTY | exp_Final.BIWK_ANNTY → exp_Initial.BIWEEKLY_ANNUITY → SQ_LES_PRIMARY_DATA_TBL.BIWEEKLY_ANNUITY → LES_PRIMARY_DATA_TBL.BIWEEKLY_ANNUITY | LES_PRIMARY_DATA_TBL.BIWEEKLY_ANNUITY |
| LESS | MILDPS_TIT | exp_Final.MILDPS_TIT → exp_Initial.MILITARY_DEPOSIT → SQ_LES_PRIMARY_DATA_TBL.MILITARY_DEPOSIT → LES_PRIMARY_DATA_TBL.MILITARY_DEPOSIT | LES_PRIMARY_DATA_TBL.MILITARY_DEPOSIT |
| LESS | MILDPS_PD | exp_Final.MILDPS_PD → exp_Initial.MIL_DEPOSIT_PAID → SQ_LES_PRIMARY_DATA_TBL.MIL_DEPOSIT_PAID → LES_PRIMARY_DATA_TBL.MIL_DEPOSIT_PAID | LES_PRIMARY_DATA_TBL.MIL_DEPOSIT_PAID |
| LESS | MILDPS_TIT2 | exp_Final.MILDPS_TIT2 → exp_Initial.MIL_DEPOSIT_2 → SQ_LES_PRIMARY_DATA_TBL.MIL_DEPOSIT_2 → LES_PRIMARY_DATA_TBL.MIL_DEPOSIT_2 | LES_PRIMARY_DATA_TBL.MIL_DEPOSIT_2 |
| LESS | MILDPS_OWED | exp_Final.MILDPS_OWED → exp_Initial.MIL_DEPOSIT_BAL → SQ_LES_PRIMARY_DATA_TBL.MIL_DEPOSIT_BAL → LES_PRIMARY_DATA_TBL.MIL_DEPOSIT_BAL | LES_PRIMARY_DATA_TBL.MIL_DEPOSIT_BAL |
| LESS | GRS_PAY_AMT | exp_Final.GRS_PAY_AMT → exp_Initial.GROSS_PAY_AMT → SQ_LES_PRIMARY_DATA_TBL.GROSS_PAY_AMT → LES_PRIMARY_DATA_TBL.GROSS_PAY_AMT | LES_PRIMARY_DATA_TBL.GROSS_PAY_AMT |
| LESS | GRS_PAY_YTD | exp_Final.GRS_PAY_YTD → exp_Initial.GROSS_PAY_AMT_YTD → SQ_LES_PRIMARY_DATA_TBL.GROSS_PAY_AMT_YTD → LES_PRIMARY_DATA_TBL.GROSS_PAY_AMT_YTD | LES_PRIMARY_DATA_TBL.GROSS_PAY_AMT_YTD |
| LESS | TAX_WGE_AMT | exp_Final.TAX_WGE_AMT → exp_Initial.TAXABLE_WAGE_AMT → SQ_LES_PRIMARY_DATA_TBL.TAXABLE_WAGE_AMT → LES_PRIMARY_DATA_TBL.TAXABLE_WAGE_AMT | LES_PRIMARY_DATA_TBL.TAXABLE_WAGE_AMT |
| LESS | TAX_WGE_YTD | exp_Final.TAX_WGE_YTD → exp_Initial.TAXABLE_WAGE_AMT_YTD → SQ_LES_PRIMARY_DATA_TBL.TAXABLE_WAGE_AMT_YTD → LES_PRIMARY_DATA_TBL.TAXABLE_WAGE_AMT_YTD | LES_PRIMARY_DATA_TBL.TAXABLE_WAGE_AMT_YTD |
| LESS | NTAX_WGE_AMT | exp_Final.NTAX_WGE_AMT → exp_Initial.NONTAXABLE_WAGE_AMT → SQ_LES_PRIMARY_DATA_TBL.NONTAXABLE_WAGE_AMT → LES_PRIMARY_DATA_TBL.NONTAXABLE_WAGE_AMT | LES_PRIMARY_DATA_TBL.NONTAXABLE_WAGE_AMT |
| LESS | NTAX_WGE_YTD | exp_Final.NTAX_WGE_YTD → exp_Initial.NONTAXABLE_WAGE_AMT_YTD → SQ_LES_PRIMARY_DATA_TBL.NONTAXABLE_WAGE_AMT_YTD → LES_PRIMARY_DATA_TBL.NONTAXABLE_WAGE_AMT_YTD | LES_PRIMARY_DATA_TBL.NONTAXABLE_WAGE_AMT_YTD |
| LESS | DEF_TAX_AMT | exp_Final.DEF_TAX_AMT → exp_Initial.TAX_DEFERRED_AMT → SQ_LES_PRIMARY_DATA_TBL.TAX_DEFERRED_AMT → LES_PRIMARY_DATA_TBL.TAX_DEFERRED_AMT | LES_PRIMARY_DATA_TBL.TAX_DEFERRED_AMT |
| LESS | DEF_TAX_YTD | exp_Final.DEF_TAX_YTD → exp_Initial.TAX_DEFERRED_AMT_YTD → SQ_LES_PRIMARY_DATA_TBL.TAX_DEFERRED_AMT_YTD → LES_PRIMARY_DATA_TBL.TAX_DEFERRED_AMT_YTD | LES_PRIMARY_DATA_TBL.TAX_DEFERRED_AMT_YTD |
| LESS | DED_TAX_AMT | exp_Final.DED_TAX_AMT → exp_Initial.DEDUCTION_AMT → SQ_LES_PRIMARY_DATA_TBL.DEDUCTION_AMT → LES_PRIMARY_DATA_TBL.DEDUCTION_AMT | LES_PRIMARY_DATA_TBL.DEDUCTION_AMT |
| LESS | DED_TAX_YTD | exp_Final.DED_TAX_YTD → exp_Initial.DEDUCTION_AMT_YTD → SQ_LES_PRIMARY_DATA_TBL.DEDUCTION_AMT_YTD → LES_PRIMARY_DATA_TBL.DEDUCTION_AMT_YTD | LES_PRIMARY_DATA_TBL.DEDUCTION_AMT_YTD |
| LESS | AEI_AMT | exp_Final.AEI_AMT | — |
| LESS | AEI_AMT_YTD | exp_Final.AEI_AMT_YTD → exp_Initial.ADV_ERND_INCOME_CREDIT_AMT_YTD → SQ_LES_PRIMARY_DATA_TBL.ADV_ERND_INCOME_CREDIT_AMT_YTD → LES_PRIMARY_DATA_TBL.ADV_ERND_INCOME_CREDIT_AMT_YTD | LES_PRIMARY_DATA_TBL.ADV_ERND_INCOME_CREDIT_AMT_YTD |
| LESS | NET_PAY_AMT | exp_Final.NET_PAY_AMT → exp_Initial.NET_PAY_AMT → SQ_LES_PRIMARY_DATA_TBL.NET_PAY_AMT → LES_PRIMARY_DATA_TBL.NET_PAY_AMT | LES_PRIMARY_DATA_TBL.NET_PAY_AMT |
| LESS | NET_PAY_YTD | exp_Final.NET_PAY_YTD → exp_Initial.NET_PAY_AMT_YTD → SQ_LES_PRIMARY_DATA_TBL.NET_PAY_AMT_YTD → LES_PRIMARY_DATA_TBL.NET_PAY_AMT_YTD | LES_PRIMARY_DATA_TBL.NET_PAY_AMT_YTD |
| LESS | XVX7_TITLE | (not connected — NULL) | — |
| LESS | XVX7_PCT | (not connected — NULL) | — |
| LESS | GA_TIT | (not connected — NULL) | — |
| LESS | GA_PCT | (not connected — NULL) | — |
| LESS | FB_TIT | (not connected — NULL) | — |
| LESS | FB_PCT | (not connected — NULL) | — |
| LESS | CC_TIT | (not connected — NULL) | — |
| LESS | CC_PCT | (not connected — NULL) | — |
| LESS | VHVM_TITLE | (not connected — NULL) | — |
| LESS | VHVM_AMT | (not connected — NULL) | — |
| LESS | VHVM_TITLE_YTD | (not connected — NULL) | — |
| LESS | VHVM_AMT_YTD | (not connected — NULL) | — |
| LESS | MAN | (not connected — NULL) | — |
| LESS | EMPLID | exp_Final.EMPLID → exp_Initial.EMPLID → SQ_LES_PRIMARY_DATA_TBL.EMPLID → LES_PRIMARY_DATA_TBL.EMPLID | LES_PRIMARY_DATA_TBL.EMPLID |
| LESS | ROTH_SAVING | exp_Final.ROTH_SAVING → exp_Initial.ROTH_SAVINGS → SQ_LES_PRIMARY_DATA_TBL.ROTH_SAVINGS → LES_PRIMARY_DATA_TBL.ROTH_SAVINGS | LES_PRIMARY_DATA_TBL.ROTH_SAVINGS |
| LESS | ROTH_PCT | (not connected — NULL) | — |
| LESS | LOAD_NBR | exp_Final.o_LOAD_NBR = 1 | literal/expression: 1 |
| LESS | CREATE_DT | exp_Final.o_CREATE_DT = SESSSTARTTIME | literal/expression: SESSSTARTTIME |
| LESS | CREATE_BY | (not connected — NULL) | — |
| LESS | UPDATE_DT | (not connected — NULL) | — |
| LESS | UPDATE_BY | (not connected — NULL) | — |

## Mapping `m_LESRPT_Load_LEST`

- Sessions: `s_LESRPT_Load_LEST` (#29)
- Sources: `LES_EMP_DETAIL_RECTYPE_T_TBL`
- Target instances: `LEST`

### Transformation `SEQTRANS` (Sequence)

- **Start Value**: `17911290`
- **Increment By**: `1`
- **End Value**: `9223372036854775807`
- **Current Value**: `3686821`
- **Cycle**: `NO`
- **Number of Cached Values**: `0`
- **Reset**: `NO`

### Transformation `SQ_LES_EMP_DETAIL_RECTYPE_T_TBL` (Source Qualifier)

- **Source Filter**: `PP_END_YEAR = $$MAP_PP_END_YEAR AND PP_NUM = $$MAP_PP_NUM`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `lkp_LEST_KEY` (Lookup Procedure)

- **Lookup Sql Override**: `SELECT MAX(LEST.LEST_KEY) as LEST_KEY FROM LEST`
- **Lookup table name**: `LEST`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `LEST_KEY >= in_KEY`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

- Sequence `SEQTRANS`: start=17911290 current=3686821 increment=1 cycle=NO reset=NO → LEST
- Lookup `lkp_LEST_KEY`: table `LEST` (exists in export: **True**), condition `LEST_KEY >= in_KEY`, multiple-match policy `Use Any Value`.
- Unconnected lookup call `exp_Initial.v_LKP_LEST_KEY`: `IIF(v_COUNTER = 1, :LKP.LKP_LEST_KEY(1), v_LKP_LEST_KEY)`.

### Target instance `LEST` (table `LEST`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LEST | LEST_KEY | exp_Final.LEST_KEY = v_LEST_KEY → exp_Final.v_LEST_KEY = IIF(v_PREV_LEST_KEY = 0 or ISNULL(v_PREV_LEST_KEY), MAX_LEST_KEY + 1, v_LEST_KEY + 1) → exp_Final.v_PREV_LEST_KEY = v_LEST_KEY → exp_Final.v_LEST_KEY (cycle/depth limit) → exp_Initial.o_MAX_LEST_KEY = v_LKP_LEST_KEY → exp_Initial.v_LKP_LEST_KEY = IIF(v_COUNTER = 1, :LKP.LKP_LEST_KEY(1), v_LKP_LEST_KEY) → exp_Initial.v_COUNTER = IIF(v_COUNTER = 0 or ISNULL(v_COUNTER), 1, v_COUNTER + 1) | LKP_LEST_KEY (unconnected lookup LKP_LEST_KEY); literal/expression: IIF(v_COUNTER = 0 or ISNULL(v_COUNTER), 1, v_COUNTER + 1) |
| LEST | MASTER_ID | exp_Final.MASTER_ID → exp_Initial.LES_NUMBER → SQ_LES_EMP_DETAIL_RECTYPE_T_TBL.LES_NUMBER → LES_EMP_DETAIL_RECTYPE_T_TBL.LES_NUMBER | LES_EMP_DETAIL_RECTYPE_T_TBL.LES_NUMBER |
| LEST | SSN | exp_Final.SSN → exp_Initial.PSEUDOSSN → SQ_LES_EMP_DETAIL_RECTYPE_T_TBL.PSEUDOSSN → LES_EMP_DETAIL_RECTYPE_T_TBL.PSEUDOSSN | LES_EMP_DETAIL_RECTYPE_T_TBL.PSEUDOSSN |
| LEST | PYR | exp_Final.PYR → exp_Initial.PP_END_YEAR → SQ_LES_EMP_DETAIL_RECTYPE_T_TBL.PP_END_YEAR → LES_EMP_DETAIL_RECTYPE_T_TBL.PP_END_YEAR | LES_EMP_DETAIL_RECTYPE_T_TBL.PP_END_YEAR |
| LEST | PPN | exp_Final.PPN → exp_Initial.PP_NUM → SQ_LES_EMP_DETAIL_RECTYPE_T_TBL.PP_NUM → LES_EMP_DETAIL_RECTYPE_T_TBL.PP_NUM | LES_EMP_DETAIL_RECTYPE_T_TBL.PP_NUM |
| LEST | SEQ | (not connected — NULL) | — |
| LEST | MAN | (not connected — NULL) | — |
| LEST | LEAVE_NAME | exp_Final.LEAVE_NAME → exp_Initial.LEAVE_NAME → SQ_LES_EMP_DETAIL_RECTYPE_T_TBL.LEAVE_NAME → LES_EMP_DETAIL_RECTYPE_T_TBL.LEAVE_NAME | LES_EMP_DETAIL_RECTYPE_T_TBL.LEAVE_NAME |
| LEST | LEAVE_DATE_TAKEN | exp_Final.LEAVE_DATE_TAKEN → exp_Initial.LEAVE_TAKEN_DTE → SQ_LES_EMP_DETAIL_RECTYPE_T_TBL.LEAVE_TAKEN_DTE → LES_EMP_DETAIL_RECTYPE_T_TBL.LEAVE_TAKEN_DTE | LES_EMP_DETAIL_RECTYPE_T_TBL.LEAVE_TAKEN_DTE |
| LEST | LEAVE_HOURS | exp_Final.LEAVE_HOURS → exp_Initial.LEAVE_HOURS → SQ_LES_EMP_DETAIL_RECTYPE_T_TBL.LEAVE_HOURS → LES_EMP_DETAIL_RECTYPE_T_TBL.LEAVE_HOURS | LES_EMP_DETAIL_RECTYPE_T_TBL.LEAVE_HOURS |
| LEST | LOAD_NBR | exp_Final.LOAD_NBR → SEQTRANS.NEXTVAL [sequence start=17911290 increment=1 current=3686821 cycle=NO reset=NO] | SEQTRANS (generated) |
| LEST | CREATE_DT | exp_Final.o_CREATE_DT = SESSSTARTTIME | literal/expression: SESSSTARTTIME |
| LEST | CREATE_BY | (not connected — NULL) | — |
| LEST | UPDATE_DT | (not connected — NULL) | — |
| LEST | UPDATE_BY | (not connected — NULL) | — |
| LEST | NEW_SEQ_NBR | exp_Final.NEW_SEQ_NBR → SEQTRANS.NEXTVAL [sequence start=17911290 increment=1 current=3686821 cycle=NO reset=NO] | SEQTRANS (generated) |

## Mapping `m_LESRPT_Load_LESU`

- Sessions: `s_LESRPT_Load_LESU` (#30)
- Sources: `LES_EMP_DETAIL_RECTYPE_U_TBL`
- Target instances: `LESU`

### Transformation `SEQTRANS` (Sequence)

- **Start Value**: `0`
- **Increment By**: `1`
- **End Value**: `9223372036854775807`
- **Current Value**: `6238046`
- **Cycle**: `NO`
- **Number of Cached Values**: `0`
- **Reset**: `NO`

### Transformation `SQ_LES_EMP_DETAIL_RECTYPE_U_TBL` (Source Qualifier)

- **Sql Query**: `SELECT PP_END_YEAR, PP_NUM, LES_NUMBER, PSEUDOSSN, EMPLOYER_CONTR_ID, EMPLOYER_CONTR_1_NAME, EMPLOYER_CONTR_1_AMT, EMPLOYER_CONTR_1_AMT_YTD, EMPLOYER_CONTR_2_NAME, EMPLOYER_CONTR_2_AMT, EMPLOYER_CONTR_2_AMT_YTD FROM LES_EMP_DETAIL_RECTYPE_U_TBL WHERE PP_END_YEAR = $$MAP_PP_END_YEAR AND PP_NUM = $$MAP_PP_NUM ORDER BY 1, 2, 3, 4, 5`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `lkp_LESU_KEY` (Lookup Procedure)

- **Lookup Sql Override**: `SELECT MAX(LESU.LESU_KEY) as LESU_KEY FROM LESU`
- **Lookup table name**: `LESU`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `LESU_KEY >= in_KEY`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

- Sequence `SEQTRANS`: start=0 current=6238046 increment=1 cycle=NO reset=NO → LESU
- Lookup `lkp_LESU_KEY`: table `LESU` (exists in export: **True**), condition `LESU_KEY >= in_KEY`, multiple-match policy `Use Any Value`.
- SQL override `SQ_LES_EMP_DETAIL_RECTYPE_U_TBL` positional bindings: 1 → `PP_END_YEAR` = `PP_END_YEAR`; 2 → `PP_NUM` = `PP_NUM`; 3 → `LES_NUMBER` = `LES_NUMBER`; 4 → `PSEUDOSSN` = `PSEUDOSSN`; 5 → `EMPLOYER_CONTR_ID` = `EMPLOYER_CONTR_ID`; 6 → `EMPLOYER_CONTR_1_NAME` = `EMPLOYER_CONTR_1_NAME`; 7 → `EMPLOYER_CONTR_1_AMT` = `EMPLOYER_CONTR_1_AMT`; 8 → `EMPLOYER_CONTR_1_AMT_YTD` = `EMPLOYER_CONTR_1_AMT_YTD`; 9 → `EMPLOYER_CONTR_2_NAME` = `EMPLOYER_CONTR_2_NAME`; 10 → `EMPLOYER_CONTR_2_AMT` = `EMPLOYER_CONTR_2_AMT`; 11 → `EMPLOYER_CONTR_2_AMT_YTD` = `EMPLOYER_CONTR_2_AMT_YTD`
- Unconnected lookup call `exp_Initial.v_LKP_LESU_KEY`: `IIF(v_COUNTER = 1, :LKP.LKP_LESU_KEY(1), v_LKP_LESU_KEY)`.

### Target instance `LESU` (table `LESU`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LESU | LESU_KEY | exp_Final.o_LESU_KEY = v_LESU_KEY → exp_Final.v_LESU_KEY = IIF(v_PREV_LESU_KEY = 0 or ISNULL(v_PREV_LESU_KEY), MAX_LESU_KEY + 1, v_LESU_KEY + 1) → exp_Final.v_PREV_LESU_KEY = v_LESU_KEY → exp_Final.v_LESU_KEY (cycle/depth limit) → exp_Initial.o_MAX_LESU_KEY = v_LKP_LESU_KEY → exp_Initial.v_LKP_LESU_KEY = IIF(v_COUNTER = 1, :LKP.LKP_LESU_KEY(1), v_LKP_LESU_KEY) → exp_Initial.v_COUNTER = IIF(v_COUNTER = 0 or ISNULL(v_COUNTER), 1, v_COUNTER + 1) | LKP_LESU_KEY (unconnected lookup LKP_LESU_KEY); literal/expression: IIF(v_COUNTER = 0 or ISNULL(v_COUNTER), 1, v_COUNTER + 1) |
| LESU | MASTER_ID | exp_Final.MASTER_ID → exp_Initial.LES_NUMBER → SQ_LES_EMP_DETAIL_RECTYPE_U_TBL.LES_NUMBER → LES_EMP_DETAIL_RECTYPE_U_TBL.LES_NUMBER | LES_EMP_DETAIL_RECTYPE_U_TBL.LES_NUMBER |
| LESU | SSN | exp_Final.SSN → exp_Initial.PSEUDOSSN → SQ_LES_EMP_DETAIL_RECTYPE_U_TBL.PSEUDOSSN → LES_EMP_DETAIL_RECTYPE_U_TBL.PSEUDOSSN | LES_EMP_DETAIL_RECTYPE_U_TBL.PSEUDOSSN |
| LESU | PYR | exp_Final.PYR → exp_Initial.PP_END_YEAR → SQ_LES_EMP_DETAIL_RECTYPE_U_TBL.PP_END_YEAR → LES_EMP_DETAIL_RECTYPE_U_TBL.PP_END_YEAR | LES_EMP_DETAIL_RECTYPE_U_TBL.PP_END_YEAR |
| LESU | PPN | exp_Final.PPN → exp_Initial.PP_NUM → SQ_LES_EMP_DETAIL_RECTYPE_U_TBL.PP_NUM → LES_EMP_DETAIL_RECTYPE_U_TBL.PP_NUM | LES_EMP_DETAIL_RECTYPE_U_TBL.PP_NUM |
| LESU | BEN_NAME1 | exp_Final.BEN_NAME1 → exp_Initial.EMPLOYER_CONTR_1_NAME → SQ_LES_EMP_DETAIL_RECTYPE_U_TBL.EMPLOYER_CONTR_1_NAME → LES_EMP_DETAIL_RECTYPE_U_TBL.EMPLOYER_CONTR_1_NAME | LES_EMP_DETAIL_RECTYPE_U_TBL.EMPLOYER_CONTR_1_NAME |
| LESU | BEN_AMT1 | exp_Final.BEN_AMT1 → exp_Initial.EMPLOYER_CONTR_1_AMT → SQ_LES_EMP_DETAIL_RECTYPE_U_TBL.EMPLOYER_CONTR_1_AMT → LES_EMP_DETAIL_RECTYPE_U_TBL.EMPLOYER_CONTR_1_AMT | LES_EMP_DETAIL_RECTYPE_U_TBL.EMPLOYER_CONTR_1_AMT |
| LESU | BEN_AMT_YTD1 | exp_Final.BEN_AMT_YTD1 → exp_Initial.EMPLOYER_CONTR_1_AMT_YTD → SQ_LES_EMP_DETAIL_RECTYPE_U_TBL.EMPLOYER_CONTR_1_AMT_YTD → LES_EMP_DETAIL_RECTYPE_U_TBL.EMPLOYER_CONTR_1_AMT_YTD | LES_EMP_DETAIL_RECTYPE_U_TBL.EMPLOYER_CONTR_1_AMT_YTD |
| LESU | BEN_NAME2 | exp_Final.BEN_NAME2 → exp_Initial.EMPLOYER_CONTR_2_NAME → SQ_LES_EMP_DETAIL_RECTYPE_U_TBL.EMPLOYER_CONTR_2_NAME → LES_EMP_DETAIL_RECTYPE_U_TBL.EMPLOYER_CONTR_2_NAME | LES_EMP_DETAIL_RECTYPE_U_TBL.EMPLOYER_CONTR_2_NAME |
| LESU | BEN_AMT2 | exp_Final.BEN_AMT2 → exp_Initial.EMPLOYER_CONTR_2_AMT → SQ_LES_EMP_DETAIL_RECTYPE_U_TBL.EMPLOYER_CONTR_2_AMT → LES_EMP_DETAIL_RECTYPE_U_TBL.EMPLOYER_CONTR_2_AMT | LES_EMP_DETAIL_RECTYPE_U_TBL.EMPLOYER_CONTR_2_AMT |
| LESU | BEN_AMT_YTD2 | exp_Final.BEN_AMT_YTD2 → exp_Initial.EMPLOYER_CONTR_2_AMT_YTD → SQ_LES_EMP_DETAIL_RECTYPE_U_TBL.EMPLOYER_CONTR_2_AMT_YTD → LES_EMP_DETAIL_RECTYPE_U_TBL.EMPLOYER_CONTR_2_AMT_YTD | LES_EMP_DETAIL_RECTYPE_U_TBL.EMPLOYER_CONTR_2_AMT_YTD |
| LESU | SEQ | (not connected — NULL) | — |
| LESU | MAN | (not connected — NULL) | — |
| LESU | LOAD_NBR | exp_Final.o_LOAD_NBR = 1 | literal/expression: 1 |
| LESU | CREATE_DT | exp_Final.o_CREATE_DT = SESSSTARTTIME | literal/expression: SESSSTARTTIME |
| LESU | CREATE_BY | (not connected — NULL) | — |
| LESU | UPDATE_DT | (not connected — NULL) | — |
| LESU | UPDATE_BY | (not connected — NULL) | — |
| LESU | NEW_SEQ_NBR | exp_Final.NEW_SEQ_NBR → SEQTRANS.NEXTVAL [sequence start=0 increment=1 current=6238046 cycle=NO reset=NO] | SEQTRANS (generated) |

## Mapping `m_LES_NIH_FILE`

- Sessions: `s_LES_NIH_FILE` (#31)
- Sources: `LES_EMPLOYEE_DETAIL`
- Target instances: `LES_NIH_EMPLOYEE_DETAIL`, `LES_NIH_EMPLOYEE_SUMMARY_TBL`

### Transformation `SQ_LES_EMPLOYEE_DETAIL` (Source Qualifier)

- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `fil_Header_Trailer` (Filter)

- **Filter Condition**: `SUBSTR(RECORD_TYPE,1,1) != '0' AND SUBSTR(RECORD_TYPE,1,1) != '2'`

### Transformation `fil_NIH_EMPLOYEE_DETAIL` (Filter)

- **Filter Condition**: `NIH_RECORD_FLAG = TRUE AND RECORD_TYPE = '*E'`

### Transformation `fil_NIH_Records` (Filter)

- **Filter Condition**: `NIH_RECORD_FLAG = TRUE`

### Transformation `lkp_Current_Pay_Period` (Lookup Procedure)

- **Lookup table name**: `PAY_PERIOD`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `CURR_PP_FLAG = in_CURR_PP_FLAG`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `lkp_PSEUDOSSN_TBL` (Lookup Procedure)

- **Lookup table name**: `PSEUDOSSN_TBL`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `PSEUDOSSN = in_DFAS_SOCIAL_SECURITY_NUMBER`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

- Lookup `lkp_Current_Pay_Period`: table `PAY_PERIOD` (exists in export: **True**), condition `CURR_PP_FLAG = in_CURR_PP_FLAG`, multiple-match policy `Use Any Value`.
- Lookup `lkp_PSEUDOSSN_TBL`: table `PSEUDOSSN_TBL` (exists in export: **False**), condition `PSEUDOSSN = in_DFAS_SOCIAL_SECURITY_NUMBER`, multiple-match policy `Use Any Value`.

### Target instance `LES_NIH_EMPLOYEE_DETAIL` (table `LES_NIH_EMPLOYEE_DETAIL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LES_NIH_EMPLOYEE_DETAIL | RECORD_TYPE | fil_NIH_Records.RECORD_TYPE → exp_Flag_NIH_Record.RECORD_TYPE → exp_Initial.RECORD_TYPE → fil_Header_Trailer.RECORD_TYPE → SQ_LES_EMPLOYEE_DETAIL.RECORD_TYPE → LES_EMPLOYEE_DETAIL.RECORD_TYPE | LES_EMPLOYEE_DETAIL.RECORD_TYPE |
| LES_NIH_EMPLOYEE_DETAIL | SSN | fil_NIH_Records.SOCIAL_SECURITY_NUMBER → exp_Flag_NIH_Record.o_SOCIAL_SECURITY_NUMBER = IIF(SOCIAL_SECURITY_NUMBER != lkp_SSN, lkp_SSN, SOCIAL_SECURITY_NUMBER) → exp_Initial.SOCIAL_SECURITY_NUMBER → fil_Header_Trailer.SOCIAL_SECURITY_NUMBER → SQ_LES_EMPLOYEE_DETAIL.SOCIAL_SECURITY_NUMBER → LES_EMPLOYEE_DETAIL.SOCIAL_SECURITY_NUMBER → lkp_PSEUDOSSN_TBL.SSN [lookup PSEUDOSSN_TBL.SSN ON PSEUDOSSN = in_DFAS_SOCIAL_SECURITY_NUMBER] | LES_EMPLOYEE_DETAIL.SOCIAL_SECURITY_NUMBER; LES_EMPLOYEE_DETAIL.SOCIAL_SECURITY_NUMBER (lookup key); PSEUDOSSN_TBL.SSN (lookup) |
| LES_NIH_EMPLOYEE_DETAIL | LES_NUMBER | fil_NIH_Records.LES_NUMBER → exp_Flag_NIH_Record.LES_NUMBER → exp_Initial.LES_NUMBER → fil_Header_Trailer.LES_NUMBER → SQ_LES_EMPLOYEE_DETAIL.LES_NUMBER → LES_EMPLOYEE_DETAIL.LES_NUMBER | LES_EMPLOYEE_DETAIL.LES_NUMBER |
| LES_NIH_EMPLOYEE_DETAIL | LES_DELIVERY_INDICATOR | fil_NIH_Records.LES_DELIVERY_INDICATOR → exp_Flag_NIH_Record.LES_DELIVERY_INDICATOR → exp_Initial.LES_DELIVERY_INDICATOR → fil_Header_Trailer.LES_DELIVERY_INDICATOR → SQ_LES_EMPLOYEE_DETAIL.LES_DELIVERY_INDICATOR → LES_EMPLOYEE_DETAIL.LES_DELIVERY_INDICATOR | LES_EMPLOYEE_DETAIL.LES_DELIVERY_INDICATOR |
| LES_NIH_EMPLOYEE_DETAIL | FILLER | fil_NIH_Records.FILLER → exp_Flag_NIH_Record.FILLER → exp_Initial.FILLER → fil_Header_Trailer.FILLER → SQ_LES_EMPLOYEE_DETAIL.FILLER → LES_EMPLOYEE_DETAIL.FILLER | LES_EMPLOYEE_DETAIL.FILLER |

### Target instance `LES_NIH_EMPLOYEE_SUMMARY_TBL` (table `LES_NIH_EMPLOYEE_SUMMARY_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LES_NIH_EMPLOYEE_SUMMARY_TBL | PP_END_YEAR | exp_Final.PP_END_YEAR → lkp_Current_Pay_Period.PP_END_YEAR [lookup PAY_PERIOD.PP_END_YEAR ON CURR_PP_FLAG = in_CURR_PP_FLAG] | PAY_PERIOD.PP_END_YEAR (lookup); literal/expression: 'Y' (lookup key) |
| LES_NIH_EMPLOYEE_SUMMARY_TBL | PP_NUM | exp_Final.PP_NUM → lkp_Current_Pay_Period.PP_NUM [lookup PAY_PERIOD.PP_NUM ON CURR_PP_FLAG = in_CURR_PP_FLAG] | PAY_PERIOD.PP_NUM (lookup); literal/expression: 'Y' (lookup key) |
| LES_NIH_EMPLOYEE_SUMMARY_TBL | LES_NUMBER | exp_Final.LES_NUMBER → exp_Set_Curr_Flag.LES_NUMBER → fil_NIH_EMPLOYEE_DETAIL.LES_NUMBER → exp_Flag_NIH_Record.LES_NUMBER → exp_Initial.LES_NUMBER → fil_Header_Trailer.LES_NUMBER → SQ_LES_EMPLOYEE_DETAIL.LES_NUMBER → LES_EMPLOYEE_DETAIL.LES_NUMBER | LES_EMPLOYEE_DETAIL.LES_NUMBER |
| LES_NIH_EMPLOYEE_SUMMARY_TBL | SSN | exp_Final.SSN → exp_Set_Curr_Flag.SOCIAL_SECURITY_NUMBER → fil_NIH_EMPLOYEE_DETAIL.SOCIAL_SECURITY_NUMBER → exp_Flag_NIH_Record.o_SOCIAL_SECURITY_NUMBER = IIF(SOCIAL_SECURITY_NUMBER != lkp_SSN, lkp_SSN, SOCIAL_SECURITY_NUMBER) → exp_Initial.SOCIAL_SECURITY_NUMBER → fil_Header_Trailer.SOCIAL_SECURITY_NUMBER → SQ_LES_EMPLOYEE_DETAIL.SOCIAL_SECURITY_NUMBER → LES_EMPLOYEE_DETAIL.SOCIAL_SECURITY_NUMBER → lkp_PSEUDOSSN_TBL.SSN [lookup PSEUDOSSN_TBL.SSN ON PSEUDOSSN = in_DFAS_SOCIAL_SECURITY_NUMBER] | LES_EMPLOYEE_DETAIL.SOCIAL_SECURITY_NUMBER; LES_EMPLOYEE_DETAIL.SOCIAL_SECURITY_NUMBER (lookup key); PSEUDOSSN_TBL.SSN (lookup) |

## Mapping `m_LES_Build_Message_Counters`

- Sessions: `s_LES_Build_Message_Counters` (#32)
- Sources: `EMP_REC_TYPE_E`, `ERROR_TBL`, `LES_NIH_EMPLOYEE_SUMMARY_TBL`, `LES_PRIMARY_DATA_TBL`
- Target instances: `COUNTER_TBL`, `LES_MESSAGE_FILE`

### Transformation `Norm_EMP_REC_TYPE_E` (Normalizer)

- **Reset**: `NO`
- **Restart**: `NO`

### Transformation `SQ_ERROR_TBL` (Source Qualifier)

- **Sql Query**: `SELECT a.PROCESS_NAME, a.ERROR_DATE FROM ERROR_TBL a, (SELECT MAX(b1.ERROR_DATE) as ERROR_DATE FROM ERROR_TBL b1 WHERE b1.ERROR_DATE >= TRUNC(SYSDATE) AND b1.PROCESS_NAME = 'm_LES_Load_LES_EMP_DETAIL_TBL' AND b1.PP_END_YEAR = $$MAP_PP_END_YEAR AND b1.PP_NUM = $$MAP_PP_NUM ) b WHERE a.ERROR_DATE = b.ERROR_DATE AND a.PROCESS_NAME = 'm_LES_Load_LES_EMP_DETAIL_TBL' AND a.PP_END_YEAR = $$MAP_PP_END_YEAR AND a.PP_NUM = $$MAP_PP_NUM`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `SQ_LES_NIH_EMPLOYEE_SUMMARY_TBL` (Source Qualifier)

- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `SQ_LES_PRIMARY_DATA_TBL` (Source Qualifier)

- **Source Filter**: `LES_PRIMARY_DATA_TBL.PP_END_YEAR = $$MAP_PP_END_YEAR AND LES_PRIMARY_DATA_TBL.PP_NUM = $$MAP_PP_NUM`
- **Number Of Sorted Ports**: `0`
- **Select Distinct**: `NO`

### Transformation `agg_Count_Error_Records` (Aggregator)

- **Sorted Input**: `NO`

### Transformation `agg_Count_Input_Records` (Aggregator)

- **Sorted Input**: `NO`

### Transformation `agg_Count_Loaded_Records` (Aggregator)

- **Sorted Input**: `NO`

### Transformation `agg_Count_NIH_Records` (Aggregator)

- **Sorted Input**: `NO`

### Transformation `fil_EMPLOYEE_DETAIL` (Filter)

- **Filter Condition**: `WS_EMP_REC_TYPE = '*E'`

### Transformation `jnr_Input_Loaded_NIH_Errors` (Joiner)

- **Join Condition**: `CONSTANT_ERRORS = CONSTANT_INPUTS`
- **Join Type**: `Full Outer Join`
- **Null ordering in master**: `Null Is Highest Value`
- **Null ordering in detail**: `Null Is Highest Value`
- **Sorted Input**: `NO`

### Transformation `jnr_Inputs_Loaded` (Joiner)

- **Join Condition**: `CONSTANT_LOADED = CONSTANT_INPUTS`
- **Join Type**: `Full Outer Join`
- **Null ordering in master**: `Null Is Highest Value`
- **Null ordering in detail**: `Null Is Highest Value`
- **Sorted Input**: `NO`

### Transformation `jnr_Inputs_Loaded_NIH` (Joiner)

- **Join Condition**: `CONSTANT_NIH = CONSTANT_INPUTS`
- **Join Type**: `Full Outer Join`
- **Null ordering in master**: `Null Is Highest Value`
- **Null ordering in detail**: `Null Is Highest Value`
- **Sorted Input**: `NO`

### Transformation `lkp_Current_Pay_Period` (Lookup Procedure)

- **Lookup table name**: `PAY_PERIOD`
- **Lookup policy on multiple match**: `Use Any Value`
- **Lookup condition**: `CURR_PP_FLAG = in_CURR_PP_FLAG`
- **Source Type**: `Database`
- **Dynamic Lookup Cache**: `NO`

### Transformation `nrm_Counters` (Normalizer)

- **Reset**: `NO`
- **Restart**: `NO`

- Joiner `jnr_Input_Loaded_NIH_Errors`: Full Outer Join ON `CONSTANT_ERRORS = CONSTANT_INPUTS`
- Joiner `jnr_Inputs_Loaded`: Full Outer Join ON `CONSTANT_LOADED = CONSTANT_INPUTS`
- Joiner `jnr_Inputs_Loaded_NIH`: Full Outer Join ON `CONSTANT_NIH = CONSTANT_INPUTS`
- Normalizer `Norm_EMP_REC_TYPE_E` (vsam=True, source EMP_REC_TYPE_E) occurs: —; generated: —
- Normalizer `nrm_Counters` (vsam=False) occurs: COUNTER_DESCRIPTION×4, COUNTER_VALUE×4; generated: GK_COUNTER_DESCRIPTION, GCID_COUNTER_DESCRIPTION, GCID_COUNTER_VALUE
- Lookup `lkp_Current_Pay_Period`: table `PAY_PERIOD` (exists in export: **True**), condition `CURR_PP_FLAG = in_CURR_PP_FLAG`, multiple-match policy `Use Any Value`.
- SQL override `SQ_ERROR_TBL` positional bindings: 1 → `PROCESS_NAME` = `a.PROCESS_NAME`; 2 → `ERROR_MESSAGE` = `a.ERROR_DATE`

### Target instance `COUNTER_TBL` (table `COUNTER_TBL`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| COUNTER_TBL | RUN_DATE | exp_Final_Counters.RUN_DATE → exp_Stage_Counters.o_RUN_DATE = SESSSTARTTIME | literal/expression: SESSSTARTTIME |
| COUNTER_TBL | PROCESS_NAME | exp_Final_Counters.PROCESS_NAME → exp_Stage_Counters.o_MAPPING_NAME = $PMMappingName | literal/expression: $PMMappingName |
| COUNTER_TBL | COUNTER_DESCRIPTION | exp_Final_Counters.COUNTER_DESCRIPTION → exp_Stage_Counters.COUNTER_DESCRIPTION → nrm_Counters.COUNTER_DESCRIPTION [normalizer: one row per occurrence of COUNTER_DESCRIPTION_in1, COUNTER_DESCRIPTION_in2, COUNTER_DESCRIPTION_in3, COUNTER_DESCRIPTION_in4] → exp_Pay_Period.COUNTER_DESCRIPTION_1 → exp_Counters.o_COUNTER_DESCRIPTION_1 = 'Input Records' → exp_Pay_Period.COUNTER_DESCRIPTION_2 → exp_Counters.o_COUNTER_DESCRIPTION_2 = 'Records Loaded' → exp_Pay_Period.COUNTER_DESCRIPTION_3 → exp_Counters.o_COUNTER_DESCRIPTION_3 = 'NIH Records' → exp_Pay_Period.COUNTER_DESCRIPTION_4 → exp_Counters.o_COUNTER_DESCRIPTION_4 = 'Records not found on Pseudo' | literal/expression: 'Input Records'; literal/expression: 'NIH Records'; literal/expression: 'Records Loaded'; literal/expression: 'Records not found on Pseudo' |
| COUNTER_TBL | COUNTER_VALUE | exp_Final_Counters.COUNTER_VALUE → exp_Stage_Counters.COUNTER_VALUE → nrm_Counters.COUNTER_VALUE [normalizer: one row per occurrence of COUNTER_VALUE_in1, COUNTER_VALUE_in2, COUNTER_VALUE_in3, COUNTER_VALUE_in4] → exp_Pay_Period.COUNT_INPUTS → exp_Counters.COUNT_INPUTS → jnr_Input_Loaded_NIH_Errors.COUNT_INPUTS → jnr_Inputs_Loaded_NIH.COUNT_INPUTS → jnr_Inputs_Loaded.COUNT_INPUTS → exp_Input_Counters.COUNT_INPUTS → agg_Count_Input_Records.COUNT_INPUTS = COUNT(WS_EMP_LES_NUM) → exp_Init_Inputs.WS_EMP_LES_NUM → fil_EMPLOYEE_DETAIL.WS_EMP_LES_NUM → Norm_EMP_REC_TYPE_E.WS_EMP_LES_NUM → EMP_REC_TYPE_E.WS_EMP_LES_NUM → exp_Pay_Period.COUNT_LOADED_RECORDS → exp_Counters.COUNT_LOADED_RECORDS → jnr_Input_Loaded_NIH_Errors.COUNT_LOADED_RECORDS → jnr_Inputs_Loaded_NIH.COUNT_LOADED_RECORDS → jnr_Inputs_Loaded.COUNT_LOADED_RECORDS → exp_Loaded_Counters.COUNT_LOADED_RECORDS → agg_Count_Loaded_Records.COUNT_LOADED_RECORDS = COUNT(LES_NUMBER) → exp_Init_Loaded_Records.LES_NUMBER → SQ_LES_PRIMARY_DATA_TBL.LES_NUMBER → LES_PRIMARY_DATA_TBL.LES_NUMBER → exp_Pay_Period.COUNT_NIH_RECORDS → exp_Counters.COUNT_NIH_RECORDS → jnr_Input_Loaded_NIH_Errors.COUNT_NIH_RECORDS → jnr_Inputs_Loaded_NIH.COUNT_NIH_RECORDS → exp_NIH_Counters.COUNT_NIH_RECORDS → agg_Count_NIH_Records.COUNT_NIH_RECORDS = COUNT(LES_NUMBER) → exp_Init_NIH.LES_NUMBER → SQ_LES_NIH_EMPLOYEE_SUMMARY_TBL.LES_NUMBER → LES_NIH_EMPLOYEE_SUMMARY_TBL.LES_NUMBER → exp_Pay_Period.COUNT_ERRORS → exp_Counters.COUNT_ERRORS → jnr_Input_Loaded_NIH_Errors.COUNT_ERRORS → exp_Error_Count.COUNT_ERRORS → agg_Count_Error_Records.COUNT_ERRORS = COUNT(*) | EMP_REC_TYPE_E.WS_EMP_LES_NUM; LES_NIH_EMPLOYEE_SUMMARY_TBL.LES_NUMBER; LES_PRIMARY_DATA_TBL.LES_NUMBER; literal/expression: COUNT(*) |
| COUNTER_TBL | PP_END_YEAR | exp_Final_Counters.PP_END_YEAR → exp_Stage_Counters.PP_END_YEAR → nrm_Counters.PP_END_YEAR [normalizer: one row per occurrence of PP_END_YEAR_in] → exp_Pay_Period.PP_END_YEAR → lkp_Current_Pay_Period.PP_END_YEAR [lookup PAY_PERIOD.PP_END_YEAR ON CURR_PP_FLAG = in_CURR_PP_FLAG] | PAY_PERIOD.PP_END_YEAR (lookup); literal/expression: 'Y' (lookup key) |
| COUNTER_TBL | PP_NUM | exp_Final_Counters.PP_NUM → exp_Stage_Counters.PP_NUM → nrm_Counters.PP_NUM [normalizer: one row per occurrence of PP_NUM_in] → exp_Pay_Period.PP_NUM → lkp_Current_Pay_Period.PP_NUM [lookup PAY_PERIOD.PP_NUM ON CURR_PP_FLAG = in_CURR_PP_FLAG] | PAY_PERIOD.PP_NUM (lookup); literal/expression: 'Y' (lookup key) |
| COUNTER_TBL | CYCLE_ID | (not connected — NULL) | — |

### Target instance `LES_MESSAGE_FILE` (table `LES_MESSAGE_FILE`)

| Target | Target Column | Expression / Rule | Source(s) |
|---|---|---|---|
| LES_MESSAGE_FILE | SUBJECT | exp_Final_Message.SUBJECT → exp_Build_Message.o_SUBJECT = SETVARIABLE($$MAP_SUBJECT, v_SUBJECT) → exp_Build_Message.v_SUBJECT = v_ENVIRONMENT \|\| 'LES Process Completed Successfully for: ' \|\| TO_CHAR(PP_END_YEAR) \|\| '-' \|\| v_PP_NUM → exp_Build_Message.v_ENVIRONMENT = DECODE(SUBSTR($PMRepositoryServiceName, 1, 4), 'Dev_', 'Dev: ', 'Test', 'Test: ', 'Prod', 'Prod: ') → lkp_Current_Pay_Period.PP_END_YEAR [lookup PAY_PERIOD.PP_END_YEAR ON CURR_PP_FLAG = in_CURR_PP_FLAG] → exp_Build_Message.v_PP_NUM = IIF(PP_NUM < 10, LPAD(TO_CHAR(PP_NUM), 2, '0'), TO_CHAR(PP_NUM) ) → lkp_Current_Pay_Period.PP_NUM [lookup PAY_PERIOD.PP_NUM ON CURR_PP_FLAG = in_CURR_PP_FLAG] | PAY_PERIOD.PP_END_YEAR (lookup); PAY_PERIOD.PP_NUM (lookup); literal/expression: 'Y' (lookup key); literal/expression: DECODE(SUBSTR($PMRepositoryServiceName, 1, 4), 'Dev_', 'Dev: ', 'Test', 'Test: ', 'Prod', 'Prod: ') |
| LES_MESSAGE_FILE | MESSAGE | exp_Final_Message.MESSAGE → exp_Build_Message.o_MESSAGE = SETVARIABLE($$MAP_MESSAGE, v_MESSAGE) → exp_Build_Message.v_MESSAGE = 'Number of Input Records = ' \|\| TO_CHAR(COUNTER_1) \|\| CHR(10) \|\| 'Number of Records loaded = ' \|\| TO_CHAR(COUNTER_2) \|\| CHR(10) \|\| 'Number of NIH Records = ' \|\| TO_CHAR(COUNTER_3) \|\| CHR(10) \|\| 'Number of Records Not on Pseudo = ' \|\| TO_CHAR(COUNTER_4) → exp_Counters.COUNT_INPUTS → jnr_Input_Loaded_NIH_Errors.COUNT_INPUTS → jnr_Inputs_Loaded_NIH.COUNT_INPUTS → jnr_Inputs_Loaded.COUNT_INPUTS → exp_Input_Counters.COUNT_INPUTS → agg_Count_Input_Records.COUNT_INPUTS = COUNT(WS_EMP_LES_NUM) → exp_Init_Inputs.WS_EMP_LES_NUM → fil_EMPLOYEE_DETAIL.WS_EMP_LES_NUM → Norm_EMP_REC_TYPE_E.WS_EMP_LES_NUM → EMP_REC_TYPE_E.WS_EMP_LES_NUM → exp_Counters.COUNT_LOADED_RECORDS → jnr_Input_Loaded_NIH_Errors.COUNT_LOADED_RECORDS → jnr_Inputs_Loaded_NIH.COUNT_LOADED_RECORDS → jnr_Inputs_Loaded.COUNT_LOADED_RECORDS → exp_Loaded_Counters.COUNT_LOADED_RECORDS → agg_Count_Loaded_Records.COUNT_LOADED_RECORDS = COUNT(LES_NUMBER) → exp_Init_Loaded_Records.LES_NUMBER → SQ_LES_PRIMARY_DATA_TBL.LES_NUMBER → LES_PRIMARY_DATA_TBL.LES_NUMBER → exp_Counters.COUNT_NIH_RECORDS → jnr_Input_Loaded_NIH_Errors.COUNT_NIH_RECORDS → jnr_Inputs_Loaded_NIH.COUNT_NIH_RECORDS → exp_NIH_Counters.COUNT_NIH_RECORDS → agg_Count_NIH_Records.COUNT_NIH_RECORDS = COUNT(LES_NUMBER) → exp_Init_NIH.LES_NUMBER → SQ_LES_NIH_EMPLOYEE_SUMMARY_TBL.LES_NUMBER → LES_NIH_EMPLOYEE_SUMMARY_TBL.LES_NUMBER → exp_Counters.COUNT_ERRORS → jnr_Input_Loaded_NIH_Errors.COUNT_ERRORS → exp_Error_Count.COUNT_ERRORS → agg_Count_Error_Records.COUNT_ERRORS = COUNT(*) | EMP_REC_TYPE_E.WS_EMP_LES_NUM; LES_NIH_EMPLOYEE_SUMMARY_TBL.LES_NUMBER; LES_PRIMARY_DATA_TBL.LES_NUMBER; literal/expression: COUNT(*) |

