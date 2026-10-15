# Decision coverage: daily_transaction_processing

Authority: `legacy/sas/programs/daily_transaction_processing.sas` (line numbers below) and the macros it `%include`s (`parmv.sas`, `nobs.sas`, `lock.sas`). The program uses no user-defined format: only `dollar18.2` (display only) is attached to balance columns, so there is no format OTHER / unmatched-label decision.

Seed counts: legacy seed `legacy/sas/data/csv` (TXN_FEED_20240131: 622 rows; curated DAILY_TRANSACTIONS: 18293 rows) loaded into local DuckDB, with STG_BANK.CUST_ACCOUNTS_DAILY taken from the committed upstream baseline output (466 accounts, unique ACCOUNT_ID), run date 31JAN2024. Row counts are feed rows unless stated; run-level decisions are counted in runs. Downstream decisions (D14 onward) count the 610 validated rows; D28-D30 count only rows that reach that WHEN of the prioritised CASE. A decision is exercised (Y) only when every reachable side is hit by the seed.

Totals: 37 decision points; exercised by seed: 9; not exercised: 28. Every side of every decision is covered by at least one scenario.

| ID | SAS line(s) | Condition | Seed rows per side | Exercised | Covering scenarios |
|---|---|---|---|---|---|
| DAI-D01 | 21, 25 (parmv.sas 134-191) | %parmv(txn_date, _req=1): txn_date supplied / blank (parmerr set but never tested) | supplied: 1 run; blank: 0 runs | N | S13 |
| DAI-D02 | 19, 25, 88, 167 | Run-date variant of &txn_date: 31JAN2024 default / mid-month / month-end leap day 29FEB2024 / quarter-end / year-end | 31JAN2024: 1 run; 15JAN2024, 29FEB2024, 31MAR2024, 31DEC2023: 0 runs | N | S01, S16, S17, S18, S19 |
| DAI-D03 | 36-40 | %sysfunc(exist(RAW_BANK.TXN_FEED_yyyymmdd)) = 0 -> %goto ABORT | exists: 1 run; absent: 0 runs | N | S12 |
| DAI-D04 | 42 (nobs.sas 193-243) | %nobs(feed) > 0 / = 0 (empty feed dataset) | >0: 1 run (622 rows); =0: 0 runs | N | S08, S09 |
| DAI-D05 | 53-56 | missing(TRANSACTION_ID) (empty or blank-only) -> reject / keep | reject: 2; pass: 620 | Y | S01, S09 |
| DAI-D06 | 59-62 | missing(ACCOUNT_ID) -> reject / keep | reject: 2; pass: 618 | Y | S01 |
| DAI-D07 | 65-68 | missing(TRANSACTION_AMOUNT) -> reject / keep | reject: 2; pass: 616 | Y | S01, S09 |
| DAI-D08 | 72-76 | abs(TRANSACTION_AMOUNT) > 10000000 -> reject / keep (boundary = 1e7 keeps) | reject: 2; pass: 614 (= 1e7: 0; negative amounts: 28) | Y | S01 |
| DAI-D09 | 80-84 | TRANSACTION_TYPE not in (DEP,WDR,TRF,PMT,FEE,INT,ADJ,REV,CHG,REF) -> reject / keep (blank and lower-case also reject) | reject: 2 (MISC, XFR); pass: 612 (blank type: 0) | Y | S01, S15 |
| DAI-D10 | 88-92 | TRANSACTION_DATE > run date -> reject / <= keep / missing keeps (missing sorts lowest) | future: 2; <= run date: 610 kept (all = run date); missing date: 0 | N | S01, S09, S16, S17, S18, S19 |
| DAI-D11 | 53-95 | Sequential IF ... return: a row failing several rules is rejected once, by its first failing rule (reason itself unobservable: REJECT_REASON dropped, TXN_REJECTED deleted at 241) | single-rule rejects: 12; multi-rule rejects: 0 | N | S01 |
| DAI-D12 | 95, 99 | WORK.TXN_VALIDATED has rows / is empty (all rows rejected) | >0: 1 run (610 rows); =0: 0 runs | N | S08, S09 |
| DAI-D13 | 80, 116-120, 146-150, 186 | SAS blank-padded character comparison: TRANSACTION_TYPE with trailing blank ("DEP ") equals "DEP" / exact value | trailing blank: 0; exact: 612 | N | S15 |
| DAI-D14 | 126-127 | LEFT JOIN STG_BANK.CUST_ACCOUNTS_DAILY on ACCOUNT_ID: one match / no match / several matches (fan-out) | one match: 610; no match: 0; several: 0 | N | S03 |
| DAI-D15 | 127, 128, 139 | ACCOUNT_ID with trailing blank joins, sorts and BY-groups with the unpadded value / exact value | trailing blank: 0; exact: 610 | N | S15 |
| DAI-D16 | 115-122 | POST_TXN_BALANCE CASE: credit types / debit types / TRF-ADJ / ELSE (unreachable after D09) | credit: 166; debit: 390; TRF/ADJ: 54; ELSE: 0 (unreachable) | Y | S02 |
| DAI-D17 | 118-119, 148-149 | abs() on debit types: positive amount / negative amount on WDR/PMT/FEE/CHG | positive: 390; negative: 0 (all 28 negatives are TRF/ADJ) | N | S02 |
| DAI-D18 | 114, 117-121 | Matched account with missing CURRENT_BALANCE -> PRE/POST_TXN_BALANCE missing (+/- propagate missing) / non-missing | missing: 0; non-missing: 610 | N | S03 |
| DAI-D19 | 143-144 | first.ACCOUNT_ID: RETAIN reset RUNNING_BALANCE = PRE_TXN_BALANCE / carry forward | first: 320; not first: 290 | Y | S02 |
| DAI-D20 | 146-151 | RUNNING_BALANCE IF / ELSE IF chain: credit / debit / TRF-ADJ / no branch (unreachable after D09) | credit: 166; debit: 390; TRF/ADJ: 54; none: 0 (unreachable) | Y | S02 |
| DAI-D21 | 144-151 | RUNNING_BALANCE uses "+" (not sum()): missing PRE_TXN_BALANCE (unmatched or missing balance) stays missing for the whole BY group / non-missing | missing: 0; non-missing: 610 | N | S03 |
| DAI-D22 | 128, 139 | ORDER BY / BY ACCOUNT_ID TRANSACTION_DATE TRANSACTION_ID: missing date sorts first / several dates per account / same-date ties broken by TRANSACTION_ID | missing-date rows: 0; accounts with >1 date: 0; same-date tie groups: 153 | N | S01, S02 |
| DAI-D23 | 167 | History WHERE TRANSACTION_DATE >= intnx(day, run date, -90): in window incl. boundary / before window / missing date (excluded) / dated after run date (included, no upper bound) | in window: 18293 (boundary day 02NOV2023: 219); before: 0; missing: 0; after run date: 0 | N | S04, S16, S17, S18, S19 |
| DAI-D24 | 163-164 | PROC SQL STD() (sample): >0 / =0 (all equal) / missing (one non-missing value) / no stats row (no history) | feed rows with STD>0: 610; =0: 0; missing: 0; no stats: 0 | N | S04, S10 |
| DAI-D25 | 163-165 | MEAN()/STD() ignore missing history amounts: some missing / none missing | missing amounts: 0; non-missing: 18293 | N | S04 |
| DAI-D26 | 178-182 | Z_SCORE CASE when STD_TXN_AMT > 0 (missing STD is not > 0) / ELSE missing | >0: 610; else: 0 | N | S04, S10 |
| DAI-D27 | 184 | calculated Z_SCORE > 3 -> HIGH_AMOUNT / <= 3 (boundary 3 not HIGH) / missing (not > 3) | >3: 16; <=3: 594 (=3: 0); missing: 0 | N | S03, S04, S05, S10, S16, S17, S18, S19 |
| DAI-D28 | 185 | RUNNING_BALANCE < 0 -> OVERDRAFT: negative / missing (SAS missing < 0 is true) / >= 0 (boundary 0 not OVERDRAFT); counted on rows reaching this WHEN | negative: 30; missing: 0; >=0: 564 (=0: 0) | N | S02, S03, S05, S10 |
| DAI-D29 | 186-188 | TRANSACTION_TYPE = 'WDR' and abs(amount) > PRE_TXN_BALANCE * 0.9 -> LARGE_WITHDRAWAL: true / WDR not above (boundary = 0.9x) / non-WDR; counted on rows reaching this WHEN | true: 0 (all 14 such rows already OVERDRAFT); WDR not above: 104; non-WDR: 460 | N | S02, S03, S05, S15 |
| DAI-D30 | 189 | missing(CUSTOMER_ID) -> ORPHAN_ACCOUNT: missing (reachable only for a matched account with blank CUSTOMER_ID; unmatched rows are OVERDRAFT first) / present; counted on rows reaching this WHEN | missing: 0; present: 564 | N | S03 |
| DAI-D31 | 190, 195 | ELSE '' and HAVING ANOMALY_TYPE ne '': anomalous row kept / non-anomalous row dropped | kept: 46; dropped: 564 | Y | S02, S04, S05, S07 |
| DAI-D32 | 183-191 | CASE priority when several conditions hold: HIGH over OVERDRAFT / OVERDRAFT over LARGE_WITHDRAWAL / LARGE_WITHDRAWAL over ORPHAN / HIGH on an unmatched account | H&O: 7; O&L: 14; L&R: 0; HIGH unmatched: 0 | N | S02, S03, S05 |
| DAI-D33 | 199, 213-217 | %if &nobs_anom > 0: append anomalies / skip append (0 anomalies) | >0: 1 run (46 rows); =0: 0 runs | N | S06, S07, S08, S09, S11 |
| DAI-D34 | 214-215 | PROC APPEND base=CURATED.TXN_ANOMALIES: base absent (created from data) / base exists (rows appended after existing rows) | absent: 1 run; exists: 0 runs | N | S06, S07 |
| DAI-D35 | 160-168, 206-208 | CURATED.DAILY_TRANSACTIONS history: exists with rows / exists empty / absent | rows: 1 run (18293); empty: 0; absent: 0 | N | S06, S10, S11 |
| DAI-D36 | 205, 211 (lock.sas 86-267) | %lock / PROC APPEND on CURATED.DAILY_TRANSACTIONS: member free / held by another session. %lock is called positionally but is keyword-only, so it fails before locking either way | free: 1 run; held: 0 runs | N | S14 |
| DAI-D37 | 206-208 | PROC APPEND has no de-duplication: feed TRANSACTION_ID already in history / new id | already in history: 0; new: 610 | N | S06 |
