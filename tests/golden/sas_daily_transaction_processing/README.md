# Golden-dataset kit: daily_transaction_processing (PROVISIONAL)

This kit is the input for a future run of the real SAS program `legacy/sas/programs/daily_transaction_processing.sas`. Each scenario is small enough to check by hand and targets decision points listed in `COVERAGE.md` (IDs `DAI-D01`..`DAI-D37`).

**Everything under `expected_provisional/` is hand-derived from the SAS source; it is not SAS output.** No SAS runtime was available. Once a SAS host has run the scenarios, its outputs replace these files as the golden results; until then, a mismatch against them means "re-check", not "wrong".

## Layout

- `scenarios.json`: manifest (`id`, `description`, `decision_ids`, `params` = macro parameters, `targets`).
- `scenarios/<id>/inputs/<libref>/<DATASET>.csv`: input datasets. The libref directory is lower-case (`raw_bank`, `curated`, `stg_bank`). Same conventions as `legacy/sas/data/csv`: dates are DATE9. text, an empty field is missing. `stg_bank/CUST_ACCOUNTS_DAILY.csv` is supplied directly in the upstream column layout; columns the program does not read are left empty. `curated/DAILY_TRANSACTIONS.csv` is the pre-run history. `curated/TXN_ANOMALIES.csv`, when present, is the pre-run anomaly table.
- `scenarios/<id>/expected_provisional/<TARGET>.csv`: expected post-run state of `CURATED.DAILY_TRANSACTIONS`, `CURATED.TXN_ANOMALIES` and `CURATED.RUNNING_BALANCES`. Columns and order follow the legacy targets (`DAILY_TRANSACTIONS` keeps the 10 base columns because of `PROC APPEND ... FORCE`). There are no wall-clock timestamp columns in these targets. Dates are written as ISO `YYYY-MM-DD` and numbers as raw values (no `dollar18.2` formatting), as in `baseline/sas/`. A header-only file means the table is absent or empty after the run.

## Running on a SAS host

1. Create the librefs `RAW_BANK`, `STG_BANK`, `CURATED` on empty scratch locations. Import every CSV under `inputs/<libref>/` as `<LIBREF>.<DATASET>`, with DATE9. columns read as SAS dates and empty fields as missing. Keep trailing blanks inside quoted values (S15). A dataset with no CSV must not exist (S11 has no history; S12 has no 31JAN2024 feed).
2. `%include` the program after making the macros available at `/opt/sas/custom/macros/` (`parmv.sas`, `nobs.sas`, `lock.sas` from `legacy/sas/macros`). Call `%daily_transaction_processing(txn_date=<params.txn_date>)`.
3. Export the three CURATED targets and compare them with `tools/parity_diff.py` (keys in `tools/keys/sas_keys.json`). S03 (fan-out) and S06 (re-used TRANSACTION_ID) produce duplicate keys on purpose; compare those scenarios on all columns.
4. S14 needs another SAS session to hold a lock on `CURATED.DAILY_TRANSACTIONS` for the whole run (e.g. `lock CURATED.DAILY_TRANSACTIONS;` and never clearing it). This is an operational precondition and cannot be expressed in the CSVs.

## Scenarios

| id | txn_date | decisions | what it exercises |
|---|---|---|---|
| S01_validation_rules | 31JAN2024 | DAI-D02, DAI-D05, DAI-D06, DAI-D07, DAI-D08, DAI-D09, DAI-D10, DAI-D11, DAI-D22 | Each validation rule rejects one row (missing/blank-only TRANSACTION_ID, missing ACCOUNT_ID, missing amount, |amount| > 1e7 both signs, invalid / blank / lower-case type, future date, multi-rule failure); boundary rows pass (|amount| = 1e7, date = run date, earlier date, missing date). The missing-date row sorts first in its BY group. |
| S02_running_balance | 31JAN2024 | DAI-D16, DAI-D17, DAI-D19, DAI-D20, DAI-D22, DAI-D28, DAI-D29, DAI-D31, DAI-D32 | RETAIN running balance across all ten valid types in two accounts: reset at FIRST.ACCOUNT_ID, credit/debit/signed groups, negative amount on a debit type (abs), missing-date row first, same-date ties ordered by TRANSACTION_ID; second account goes overdrawn (OVERDRAFT outranks LARGE_WITHDRAWAL). |
| S03_join_paths | 31JAN2024 | DAI-D14, DAI-D18, DAI-D21, DAI-D27, DAI-D28, DAI-D29, DAI-D30, DAI-D32 | LEFT JOIN to STG_BANK.CUST_ACCOUNTS_DAILY: duplicated snapshot row (fan-out), missing CUSTOMER_ID (ORPHAN_ACCOUNT reached), missing CURRENT_BALANCE (missing propagates to POST/RUNNING_BALANCE -> OVERDRAFT), orphan WDR where LARGE_WITHDRAWAL outranks ORPHAN, account absent from snapshot with history (HIGH_AMOUNT despite missing balance) and without history (OVERDRAFT). |
| S04_stats_window | 31JAN2024 | DAI-D23, DAI-D24, DAI-D25, DAI-D26, DAI-D27, DAI-D31 | PROC SQL history statistics: 90-day lower bound inclusive (02NOV2023 in, 01NOV2023 out), missing-date history excluded, history dated after the run date included (no upper bound), STD = 0, single history row (STD missing), missing history amount ignored by AVG/STD, no history; Z_SCORE exactly 3 is not HIGH_AMOUNT. |
| S05_anomaly_priority | 31JAN2024 | DAI-D27, DAI-D28, DAI-D29, DAI-D31, DAI-D32 | Anomaly CASE boundaries and priority: WDR exactly 0.9 x PRE (not LARGE_WITHDRAWAL) vs just above, RUNNING_BALANCE exactly 0 (not OVERDRAFT), HIGH_AMOUNT outranks OVERDRAFT and LARGE_WITHDRAWAL, OVERDRAFT outranks LARGE_WITHDRAWAL after an earlier credit, LARGE_WITHDRAWAL tests the snapshot PRE balance not the running balance. |
| S06_prior_anomalies_append | 31JAN2024 | DAI-D33, DAI-D34, DAI-D35, DAI-D37 | CURATED.TXN_ANOMALIES already exists with two rows: new anomalies are PROC APPENDed after them; a feed TRANSACTION_ID already present in history is appended again (no de-duplication) to CURATED.DAILY_TRANSACTIONS. |
| S07_no_new_anomalies | 31JAN2024 | DAI-D31, DAI-D33, DAI-D34 | No feed row is anomalous (%nobs(WORK.TXN_ANOMALIES)=0): the PROC APPEND to CURATED.TXN_ANOMALIES is skipped, so the pre-existing table is left unchanged. |
| S08_empty_feed | 31JAN2024 | DAI-D04, DAI-D12, DAI-D33 | Feed dataset exists but has 0 rows: all work tables are empty, nothing is appended to DAILY_TRANSACTIONS, RUNNING_BALANCES is replaced by an empty table, TXN_ANOMALIES is not created. |
| S09_all_rejected | 31JAN2024 | DAI-D04, DAI-D05, DAI-D07, DAI-D10, DAI-D12, DAI-D33 | Feed has rows but every row fails validation: same outputs as an empty feed (no append, empty RUNNING_BALANCES, no anomalies). |
| S10_empty_history | 31JAN2024 | DAI-D24, DAI-D26, DAI-D27, DAI-D28, DAI-D35 | CURATED.DAILY_TRANSACTIONS exists with 0 rows: no statistics, every Z_SCORE missing, no HIGH_AMOUNT even for a very large deposit; output DAILY_TRANSACTIONS holds only the new rows. |
| S11_history_absent | 31JAN2024 | DAI-D35, DAI-D33 | CURATED.DAILY_TRANSACTIONS does not exist. LOW CONFIDENCE: the TXN_STATS PROC SQL errors, WORK.TXN_ANOMALIES is not created, %nobs returns blank and the %if comparison stops the macro after PROC APPEND has created CURATED.DAILY_TRANSACTIONS from WORK.TXN_WITH_BALANCE (19 columns); RUNNING_BALANCES and TXN_ANOMALIES are not written. |
| S12_feed_absent | 31JAN2024 | DAI-D03 | RAW_BANK.TXN_FEED_20240131 does not exist (only the previous day feed is present): %goto ABORT, all targets unchanged. |
| S13_blank_txn_date | (blank) | DAI-D01 | txn_date passed blank. LOW CONFIDENCE: %parmv flags the missing parameter but its result is not tested; the feed name resolves without a date, exist() is false and the macro aborts with all targets unchanged. |
| S14_lock_held | 31JAN2024 | DAI-D36 | CURATED.DAILY_TRANSACTIONS is locked by another session for the whole run (operational precondition, not data). LOW CONFIDENCE: the %lock call is positional against a keyword-only macro so no lock is acquired; PROC APPEND fails with a lock error and DAILY_TRANSACTIONS is unchanged, while RUNNING_BALANCES and TXN_ANOMALIES are still written (assumes no OBS=0 syntax-check escalation). |
| S15_trailing_blanks | 31JAN2024 | DAI-D09, DAI-D13, DAI-D15, DAI-D29 | Trailing blanks in TRANSACTION_TYPE and ACCOUNT_ID: SAS character comparison pads with blanks, so "DEP " is a valid type and "A9000131 " joins to and sorts with "A9000131". |
| S16_mid_month_date | 15JAN2024 | DAI-D02, DAI-D10, DAI-D23, DAI-D27 | Mid-month run date 15JAN2024: feed TXN_FEED_20240115; 90-day stats window starts 17OCT2023 (included) and excludes 16OCT2023; next-day row rejected as future-dated. |
| S17_leap_day_date | 29FEB2024 | DAI-D02, DAI-D10, DAI-D23, DAI-D27 | Leap-day run date 29FEB2024: feed TXN_FEED_20240229; 90-day stats window starts 01DEC2023 (included) and excludes 30NOV2023; next-day row rejected as future-dated. |
| S18_quarter_end_date | 31MAR2024 | DAI-D02, DAI-D10, DAI-D23, DAI-D27 | Quarter-end run date 31MAR2024: feed TXN_FEED_20240331; 90-day stats window starts 01JAN2024 (included) and excludes 31DEC2023; next-day row rejected as future-dated. |
| S19_year_end_date | 31DEC2023 | DAI-D02, DAI-D10, DAI-D23, DAI-D27 | Year-end run date 31DEC2023: feed TXN_FEED_20231231; 90-day stats window starts 02OCT2023 (included) and excludes 01OCT2023; next-day row rejected as future-dated. |

## What is provisional and why

- All expected values are hand-derived. Arithmetic is IEEE double, as in SAS (for example `99.99000000000001` in S05). Compare with a tolerance.
- **Low confidence:**
  - S11 (history absent): the expected 19-column `DAILY_TRANSACTIONS` assumes PROC APPEND creates the base from `WORK.TXN_WITH_BALANCE` and the `%if &nobs_anom > 0` macro error then stops the run.
  - S13 (blank `txn_date`): assumes the feed name resolves to `TXN_FEED_` and the macro aborts.
  - S14 (lock held): assumes no OBS=0 syntax-check mode after the PROC APPEND error. If the batch session enters syntax-check mode, RUNNING_BALANCES and TXN_ANOMALIES would also be left unchanged.
- **SAS facts the expectations rely on:**
  - `REJECT_REASON` is dropped from both DATA-step outputs, and `WORK.TXN_REJECTED` is deleted at the end. Rejections are therefore only visible as missing rows.
  - `%lock(CURATED.DAILY_TRANSACTIONS)` and `%lock(CURATED.DAILY_TRANSACTIONS, unlock)` pass positional values to a keyword-only macro. SAS reports an error and no lock is ever taken.
  - `lock.sas` also references `%handle` and `%get_data_attr`, which are not in `legacy/sas/macros`. They are not reached because of the positional-parameter error.
  - SAS character comparison ignores trailing blanks (S15).
  - A missing numeric is lower than any number, so a missing RUNNING_BALANCE is `< 0` and a missing PRE_TXN_BALANCE makes `abs(x) > PRE*0.9` true.
- Scenario row order in the expected files follows SAS processing order: history first, then the new rows in `ACCOUNT_ID, TRANSACTION_DATE, TRANSACTION_ID` order with missing dates first. The comparison is key-based.
