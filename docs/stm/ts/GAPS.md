# Gap register: ts PowerCenter exports → dbt on Snowflake

What a dbt unit **can't** rebuild from the 11 folder exports in `legacy/informatica_ts/` alone, and how each item is handled. Counts come from the STM JSON (`docs/stm/ts/*.json`, from `tools/ts_lineage.py`) and from reading the scripts in `Cognition-Partner-Workshops/ts-informatica-powercenter`.

## Scope line

- **In scope:** the 11 workflows exported under `XML/` (108 mappings, see [INVENTORY.md](INVENTORY.md)). Each one becomes one dbt unit.
- **Out of scope, recorded here only:** every shell and SQL script outside `XML/`: `actstage_load`, `ehrp2biis_preload`, `ehrp2biis_afterload.sql`, `Transfer Scripts/*` (7), `Maintenance Scripts/*` (2). Nothing from them is ported. Most of the work they do calls SQL files or procedures that aren't in the repo, so porting them would be guesswork.
- The root `Pseudossn` file is a byte-identical copy of `XML/Pseudossn`. It isn't a separate unit.
- This register has no names, email addresses, hosts, accounts or directories taken from the scripts or exports. Where the source has one, the row says what kind of identifier it is and leaves the value out.

## Treatments

| Code | Meaning |
|---|---|
| `SOURCE` | Read as a plain table in `SOURCE_<token>`, loaded from synthetic seeds. The legacy reader or format isn't reproduced. |
| `TABLE` | The legacy target, whether a file, mainframe dataset or Oracle table, becomes a dbt mart table with the legacy name and column order. Writing the physical file is left out. |
| `DERIVE` | Rebuilt in SQL from data the unit already has, for example a run variable computed from `PAY_PERIOD`. |
| `VAR` | A dbt `var()` with a documented default. It is pinned for the parity run. |
| `EMPTY` | Prior state that isn't in the exports, such as rows from earlier runs or the current value of a sequence, is treated as empty or zero. The reference executor (baseline) uses the same convention. |
| `NULL` | Emitted as a typed `NULL`, which is what PowerCenter writes for the column. |
| `DROP` | Orchestration with no data effect inside the warehouse, such as a file move, mail or transfer. Recorded here and not ported. |
| `OUT` | Out of scope by decision. It has a data effect, but the logic is missing or sits outside the 11 workflows. |

## Cross-cutting gaps

| ID | Gap | Affected | Treatment |
|---|---|---|---|
| G-01 | The parameter file `BIIS_parms.iparms` isn't in the repo. It supplies `$Param_*` (directories, file names) and the `$$WF_*_EMAIL_LIST` values. | 10 workflows (all except EHRP2BIIS_UPDATE, which has no parameter file) | Directory, file-name and email parameters go with the command and email tasks they feed: `DROP`. A parameter that shows up in mapping logic becomes `VAR`. |
| G-02 | Pay-period run state passes between sessions as workflow variables (`$$WF_PP_END_YEAR`, `$$WF_PP_NUM`, `$$WF_PP_YEAR_NUM`, `$$WF_PP_END_YEAR_LAST_DIGIT`, `$$WF_CYCLE_ID`, `$$WF_NEW_MER_FLAG`). They are set by pre- and post-session variable assignment and by `SETVARIABLE` in the *Current Pay Period* / *Set Calendar* sessions. | 10 workflows (all except EHRP2BIIS_UPDATE) | `DERIVE`: one intermediate model per unit reads `PAY_PERIOD` where `CURR_PP_FLAG = 'Y'`, and `$$WF_CYCLE_ID` comes from the `CPM_CYCLE_TBL` model. A `VAR` override is allowed for the pinned run. |
| G-03 | Email tasks: 49 in total (session success/failure emails and workflow emails). The `$$WF_SUBJECT` / `$$WF_MESSAGE` text is built by the *Build Message* mappings. | All 11 | Sending mail: `DROP`. The message-file targets that hold the text are still built: `TABLE`. |
| G-04 | Shell file handling in Command tasks: 37 commands. They archive inputs with `mv` (10), copy or rename outputs with `cp` (8), clear outputs with `remove_file.sh` before a session (8), join header and data files with `cat` (2), archive a directory with `archive_files.sh` (1), and call transfer scripts (8, see G-05). | COMPTIME 1, CPM 4, CPM_AFPS 9, CPM_CDC 6, CPM_NIH 6, CPM_OIG 3, FDA_Leave 3, LES 3, Pseudossn 2 | `DROP`. Header and data stay separate marts; joining them into one file is an export step. |
| G-05 | Outbound `sftp` to an external dropbox host, with `mailx` confirmations (`Transfer Scripts/*`). 6 scripts are called from Command tasks; `nih_transfer_les` isn't called by any workflow. | CPM_AFPS (`afps_transfer` ×3), CPM_CDC (`cdc_transfer`), CPM_NIH (`nih_cpm_transfer`), CPM_OIG (`oig_transfer`), FDA_Leave (`fda_transfer`), LES (`nih_les_transfer`) | `DROP`. Host, accounts and recipient lists are intentionally left out. |
| G-06 | Dummy mappings that exist only to host Command tasks: `HI_GENERIC_SRC_TBL` → `GENERIC_TARGET_FILE`. | CPM `m_Generic_Mapping`; CPM_AFPS `0760`, `0860`, `1000`; CPM_CDC `m_CPM_CDC_Concatenate_Files`; CPM_NIH `m_CPM_NIH_Concatenate_Files`; FDA_Leave `m_1100_PM_FDA_Send_Email` | No model. The commands they carry fall under G-04 and G-05. |
| G-07 | Flat-file targets (38): fixed-width or delimited files, plus file names built from pay-period variables. | COMPTIME 2, CPM 3, CPM_AFPS 7, CPM_CDC 4, CPM_NIH 4, CPM_OIG 3, FDA_Leave 5, LES 5, Pay_Calendar 2, Pseudossn 3 | `TABLE`. File naming and layout padding: `DROP`. |
| G-08 | Flat-file sources (6), with header and trailer records. | COMPTIME `U0287D01`; FDA_Leave `HI_PM_FDA_TATRAN_FLAT`, `HI_PM_FDA_TATRAN_FLAT_FILE_NAME`; LES `LES_EMPLOYEE_DETAIL`; Pseudossn `PSEUDOSSN_FILE`, `PSEUDOSSN_FILE_TK_NUM` | `SOURCE`, one row per file record. Header and trailer rows stay rows, and the mapping's own filters are reproduced. |
| G-09 | VSAM sources (20) read through VSAM Normalizers, including COBOL `OCCURS` / `REDEFINES` and packed or EBCDIC decoding. | CPM 5 (`MER_FILE`, `PAD_FILE`, `PAYMASTER_FILE`, `PAYMASTER_THREE`, `YTD_FILE`); LES 15 (`EMP_REC_TYPE_0..6, C, D, E, L, M, R, T, U`) | `SOURCE`: a plain table at record level, one column per elementary item, with the seeds already decoded. `OCCURS` groups are unpivoted in staging, following the Normalizer definition in the STM. Copybook decoding: `DROP`. |
| G-10 | PowerExchange `PWX_SEQ_NRDB2` targets (6), which write mainframe sequential datasets. | CPM_AFPS `feeder_FEEDER_RECORD`; CPM_CDC `cdchdr_WS_CDC_HDR`, `cdcskel_WS_PAY_OUT_REC`; CPM_NIH `nihhdr_WS_NIH_HDR`, `nihtest_NIH_PAYROLL_MASTER`; CPM_OIG `oigsgndec_SKPAYROLL_MASTER` | `TABLE`. Writing the dataset: `DROP`. |
| G-11 | Append writers: 57 Oracle writer instances run without *Truncate target table*, so earlier runs' rows (`ERROR_TBL`, `COUNTER_TBL`, `CPM_NEWPAY_TBL`, the `LES*` tables and others) carry over. 24 truncate-and-load writers are exact. | COMPTIME 2, CPM 5, CPM_AFPS 4, EHRP2BIIS_UPDATE 3, FDA_Leave 7, LES 28, Pay_Calendar 3, Pseudossn 5 | `EMPTY`: each mart holds this run's rows only. Truncate-and-load writers become `table` materializations. |
| G-12 | Update Strategy / data-driven sessions that change rows in place. | CPM_AFPS `0050` and FDA_Leave `0050` (`CPM_CYCLE_TBL`); Pay_Calendar `Reset` / `Set` (`PAY_PERIOD`, `PAY_PERIOD_PARAM`, `RESET_PAY_PERIOD`); Pseudossn `Update_Timekeeper_Number` (`PSEUDOSSN_TBL`); CPM_OIG `Load_CPM_OIG_File` (expression `0` = `DD_INSERT`) | `DERIVE`: the mart is the table after the update (source rows with the updates applied), not an in-place `UPDATE`. CPM_OIG is a plain insert. |
| G-13 | Mappings that load the same table in sequence, where a later mapping reads or updates an earlier mapping's target. | Pseudossn (`PSEUDOSSN_TBL`: load, then update, then insert SDA rows); FDA_Leave (`HI_PM_FDA_TATRAN_TBL`: `0100` load, then `0200` adds rows) | `DERIVE`: one intermediate model per step and one mart for the final state, in session order. |
| G-14 | Target columns with no connector (747 across all units, e.g. EHRP2BIIS_UPDATE 311, CPM_CDC 197). | All 11 | `NULL`. The STMs list each column as `(not connected — NULL)`. |
| G-15 | Target Post-SQL: after the load, it deletes `HI_PM_FDA_TATRAN_TBL` rows for employees who have no record type `12`. | FDA_Leave `m_0100_PM_FDA_Load_TATRAN_To_DB` | `DERIVE`: written as a `WHERE ... IN` filter in the mart. The SQL is in the export. |

## Lineage the tool could not resolve

`tools/ts_lineage.py` resolved every mapplet port: 0 unresolved for `mplt_Convert_Num_To_Prec7`, which CPM mappings instantiate 20 times and which becomes a dbt macro. That leaves 15 target columns it couldn't fully trace:

| ID | Columns | Affected | Why | Treatment |
|---|---|---|---|---|
| L-01 | `LESC_KEY`, `LESD_KEY`, `LESL_KEY`, `LESM_KEY`, `LESR_KEY`, `LESS_KEY`, `LEST_KEY`, `LESU_KEY` (8) | LES `m_LESRPT_Load_LES{C,D,L,M,R,S,T,U}` | The key is a running variable port (`v_COUNTER`) seeded by an unconnected lookup of `MAX(key)` on the target itself (`:LKP.LKP_*_KEY(1)`), so the trace cycles. Five of these mappings also use a `SEQTRANS` sequence whose persisted *Current Value* lives in the repository. | `EMPTY` + `DERIVE`: with no prior target rows, the max is NULL→0, and the key is `row_number()` over the legacy sort order, plus a `VAR` offset that defaults to 0. Sequence current values aren't reproduced. The baseline uses the same rule. |
| L-02 | `CPM_PAD_DETAIL_STG_TBL.FILLER0`; `CPM_PM3_STG_TBL.PYF_FILLER_PDT`, `PYF_HIS_PGRANGE_RT3`, `PYF_MPH_PGRANGE_RT3`; `CPM_NEWPAY_STG_TYPE_3_TBL.PYF_PAY_TAC_TYP_LINE`, `PYF_PAY_DET_CD` (6) | CPM `m_CPM_Load_CPM_PAD_Staging_Tables`, `m_CPM_Load_CPM_PMR_Staging_Tables`, `m_CPM_Load_CPM_NEWPAY_STG_TYPE_3_TBL` | The chain ends at an Expression or Aggregator port that has no expression and no incoming connector. | `NULL`. |
| L-03 | `LESS.AEI_AMT` (1) | LES `m_LESRPT_Load_LESS` | Same as L-02. | `NULL`. |

## Scripts outside `XML/` (out of scope)

| ID | Script | What it does | Affected | Treatment |
|---|---|---|---|---|
| S-01 | `actstage_load` (ksh) | Runs SQL\*Plus on `action_stage_load`, a SQL file **not in the repo**, using credentials read from files in the account home directory. It greps the log for success and sends a `mailx` notice to a recipient list. | Upstream of EHRP2BIIS_UPDATE (action staging) | `OUT`. The staging tables it fills are `SOURCE`. |
| S-02 | `ehrp2biis_preload` (ksh) | Runs SQL\*Plus on `step01`, which is **not in the repo**, then `uuencode`s the log and sends it with `mailx`. | Before EHRP2BIIS_UPDATE | `OUT`. `NWK_NEW_EHRP_ACTIONS_TBL` and `PS_GVT_JOB` are `SOURCE` as given. |
| S-03 | `ehrp2biis_afterload.sql`, inline DML | Clears `retnd1_step_cd = '0.0000000000000'` on the day's `NWK_ACTION_SECONDARY_TBL` rows. Sets `PROCESS_TABLE.P_STARTDT` from WIP-status changes. Appends the day's `NWK_ACTION_*` rows into `ACTION_PRIMARY_ALL` / `ACTION_SECONDARY_ALL` / `ACTION_REMARKS_ALL`, deletes and reinserts cancelled actions, and truncates `NWK_NEW_EHRP_ACTIONS_TBL`. It qualifies tables with a person-named schema and reads `NWK_ACTION_REMARKS_TBL`, which no XML mapping writes. | After EHRP2BIIS_UPDATE | `OUT`. The EHRP2BIIS_UPDATE marts are the workflow output before the afterload runs. The retained-step clean is the only piece that is self-contained; it's a candidate follow-up and isn't applied. |
| S-04 | `ehrp2biis_afterload.sql`, procedures **not in the repo** (8) | `update_sequence_number_tbl_p`, `chk_ehrp2biis_wip_status_p`, `HISTDBA.UPDT_ERP2BIIS_CRE8_REMARKS01_P`, `HISTDBA.UPDATE_ERP2BIIS_NO900S01_P`, `HISTDBA.ERP2BIIS_CRE8_REMARKS_900S01`, `HISTDBA.UPDATE_ERP2BIIS_900SONLY01_P`, `HISTDBA.UPDT_ORIG_CANCELLED_TRANS01_P`, `HISTDBA.GATHER_EHRP2BIIS_RUNCOUNTS_P` | After EHRP2BIIS_UPDATE | `OUT`, can't be reproduced. `SEQUENCE_NUM_TBL`, a lookup in `m_EHRP2BIIS_UPDATE` that `update_sequence_number_tbl_p` advances after each load, is a static `SOURCE`. |
| S-05 | `Transfer Scripts/*` (7) | `sftp` push plus `mailx` (see G-05). | CPM_AFPS, CPM_CDC, CPM_NIH, CPM_OIG, FDA_Leave, LES | `DROP` |
| S-06 | `Maintenance Scripts/remove_file`, `archive_files` | Delete a file before a session; move a directory into archive with a pay-period suffix (see G-04). | CPM_AFPS, CPM_CDC, CPM_NIH, CPM_OIG (remove); LES (archive) | `DROP` |

## Per workflow

Each unit ticket links to its section below. The rows it lists are the ones the unit has to honour.

### COMPTIME
G-01, G-02, G-03 (1 email), G-04 (1 `mv`), G-07 (2), G-08 (`U0287D01`), G-11 (`COMP_TIME_DAILY_TBL`, `COUNTER_TBL`), G-14 (3).

### CPM
G-01, G-02 (including `$$WF_NEW_MER_FLAG`), G-03 (6), G-04 (4 `mv`), G-06 (`m_Generic_Mapping`), G-07 (3), G-09 (5 VSAM), G-11 (`ERROR_TBL` ×2, `CPM_NEWPAY_TBL` ×2, `COUNTER_TBL`), G-14 (32), L-02. The mapplet `mplt_Convert_Num_To_Prec7` resolved fully and becomes a macro.

### CPM_AFPS
G-01, G-02 (including `$$WF_CYCLE_ID`, `$$WF_PP_END_YEAR_LAST_DIGIT`), G-03 (5), G-04 (9), G-05 (`afps_transfer` ×3), G-06 (`0760`, `0860`, `1000`), G-07 (7), G-10 (`feeder_FEEDER_RECORD`), G-11 (`CPM_CYCLE_TBL`, `ERROR_TBL`, `AFPS_COUNTER_TBL` ×2), G-12 (`0050`), G-14 (6), S-05, S-06.

### CPM_CDC
G-01, G-02, G-03 (7), G-04 (6, including the header+data `cat`), G-05 (`cdc_transfer`), G-06 (`Concatenate_Files`), G-07 (4), G-10 (2), G-14 (197), S-05, S-06.

### CPM_NIH
G-01, G-02, G-03 (7), G-04 (6, including the header+data `cat`), G-05 (`nih_cpm_transfer`), G-06 (`Concatenate_Files`), G-07 (4), G-10 (2), G-14 (7), S-05, S-06.

### CPM_OIG
G-01, G-02, G-03 (4), G-04 (3), G-05 (`oig_transfer`), G-07 (3), G-10 (`oigsgndec_SKPAYROLL_MASTER`), G-12 (`UPDTRANS` = `DD_INSERT`), G-14 (50), S-05, S-06.

### EHRP2BIIS_UPDATE
G-03 (1), G-11 (`EHRP_RECS_TRACKING_TBL`, `NWK_ACTION_PRIMARY_TBL`, `NWK_ACTION_SECONDARY_TBL`), G-14 (311), S-01, S-02, S-03, S-04. No parameter file and no Command tasks.

### FDA_Leave
G-01, G-02 (including `$$WF_CYCLE_ID`), G-03 (4), G-04 (3), G-05 (`fda_transfer`), G-06 (`m_1100_PM_FDA_Send_Email`), G-07 (5), G-08 (2), G-11 (7), G-12 (`0050`), G-13 (`HI_PM_FDA_TATRAN_TBL`), G-14 (5), G-15, S-05.

### LES
G-01, G-02, G-03 (1), G-04 (3, including `archive_files.sh`), G-05 (`nih_les_transfer`), G-07 (5), G-08 (`LES_EMPLOYEE_DETAIL`), G-09 (15 VSAM), G-11 (28), G-14 (54), L-01, L-03, S-05, S-06.

### Pay_Calendar
G-01, G-02, G-03 (4), G-07 (2), G-11 (3), G-12 (`PAY_PERIOD`, `PAY_PERIOD_PARAM`, `RESET_PAY_PERIOD`), G-14 (15). No Command tasks.

### Pseudossn
G-01, G-02, G-03 (9), G-04 (2 `mv`), G-07 (3), G-08 (2), G-11 (5), G-12 (`PSEUDOSSN_TBL`), G-13 (`PSEUDOSSN_TBL`), G-14 (67).
