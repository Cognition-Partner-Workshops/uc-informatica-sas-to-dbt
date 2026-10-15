# credit_risk_scoring — branch coverage (PROVISIONAL)

Authority: `legacy/sas/programs/credit_risk_scoring.sas` (line numbers below), `legacy/sas/macros/parmv.sas`, `nobs.sas`, `lock.sas`
(called via autocall, not `%include`d), `legacy/sas/config/autoexec_local.sas`. The program uses no user-defined format
(no `put(...,$fmt.)`); only display formats (`date9.`, `8.4`, `percent8.4`, `dollar18.2`, `datetime20.`), so there are no
format OTHER/unmatched-label decisions, and no `||`/`catx`, `sum()`, `FIRST./LAST.` or `RETAIN` logic in this program.

Seed = `legacy/sas/data/csv` at the default params (score_date=31JAN2024, model_id=CRM-2023-Q4-v2). `STG_BANK.CUST_ACCOUNTS_DAILY`
for the seed is the `load_customer_accounts` output (`baseline/sas/CUST_ACCOUNTS_DAILY.csv`, 466 rows). Counts are rows taking
that side (per CUST_ACCOUNTS_DAILY row for Step 1, per WORK.SCORED row for Steps 2-3, per PROC MEANS group for CRE-D30,
per run for parameter/append/lock decisions). Exercised = Y only if every side, including dead-code sides marked
(unreachable), is hit by the seed.

Totals: **35 decision points, 6 exercised by seed, 29 not exercised.** Every reachable side is covered by
at least one scenario; sides marked (unreachable) cannot be hit by any input without changing the SAS code.

| ID | SAS line(s) | Condition | Seed rows per side | Exercised by seed | Covering scenarios |
|---|---|---|---|---|---|
| CRE-D01 | 83 | WHERE a.SNAPSHOT_DATE = "&score_date"d (missing date never equals a date) | SNAPSHOT_DATE = score_date: 466<br>SNAPSHOT_DATE <> score_date (excluded): 0<br>SNAPSHOT_DATE missing (excluded): 0 | N | S01, S02, S03, S04, S05, S06, S07, S08, S09 |
| CRE-D02 | 84 | WHERE a.ACCOUNT_TYPE in ('MTG','AUTO','PERS','CC','LOC','HELC') | type in list: 236<br>type not in list (excluded): 230 | Y | S01, S02, S03, S04, S05, S06, S07, S08, S09 |
| CRE-D03 | 74-78 | LEFT JOIN ORA_DW.BUREAU_SCORES match / no match (incl. customer whose only rows are future-dated) | hit: 236<br>miss: 0 | N | S01, S02, S04, S05, S06, S07, S08, S09 |
| CRE-D04 | 76-78 | correlated max(SCORE_DATE) where SCORE_DATE <= score_date: latest row before / on score_date; future rows ignored | max SCORE_DATE < score_date: 236<br>max SCORE_DATE = score_date: 0<br>future-dated row(s) ignored: 0 | N | S01, S02, S04, S05, S06, S07, S08, S09 |
| CRE-D05 | 74-78 | latest bureau date unique vs tied (SQL join keeps every tied row -> fan-out) | single row on max date: 236<br>tie on max date (fan-out): 0 | N | S01, S02, S04, S05, S06, S07, S08, S09 |
| CRE-D06 | 76-78 | SAS missing ordering: missing SCORE_DATE satisfies <= score_date; max() ignores missing; missing = missing in join | no missing SCORE_DATE rows: 236<br>missing-date row ignored (dated max exists): 0<br>only missing-date rows qualify -> missing=missing match: 0 | N | S01, S02, S04, S05, S06, S07, S08, S09 |
| CRE-D07 | 75 | a.CUSTOMER_ID = b.CUSTOMER_ID with blank key (SAS: blank equals blank) | CUSTOMER_ID non-blank: 236<br>CUSTOMER_ID blank: 0<br>blank key matched blank bureau rows: 0 | N | S01, S02, S04, S05, S06, S07, S08, S09 |
| CRE-D08 | 79-80 | LEFT JOIN ORA_DW.PAYMENT_HISTORY match / no match | hit: 236<br>miss: 0 | N | S01, S02, S04, S05, S06, S07, S08, S09 |
| CRE-D09 | 79-80 | PAYMENT_HISTORY key unique vs duplicated (fan-out) | unique: 236<br>duplicate (fan-out): 0 | N | S01, S02, S04, S05, S06, S07, S08, S09 |
| CRE-D10 | 81-82 | LEFT JOIN ORA_DW.COLLATERAL match / no match | hit: 108<br>miss: 128 | Y | S01, S02, S04, S05, S06, S07, S08, S09 |
| CRE-D11 | 81-82 | COLLATERAL key unique vs duplicated (fan-out) | unique: 108<br>duplicate (fan-out): 0 | N | S01, S02, S04, S05, S06, S07, S08, S09 |
| CRE-D12 | 67-71 | CASE WHEN COLLATERAL_VALUE > 0 THEN CURRENT_BALANCE/COLLATERAL_VALUE ELSE . (missing > 0 is false; missing/x = missing) | COLLATERAL_VALUE > 0, balance present: 108<br>COLLATERAL_VALUE > 0, balance missing -> LTV missing: 0<br>COLLATERAL_VALUE = 0: 0<br>COLLATERAL_VALUE < 0: 0<br>no collateral row / value missing: 128 | N | S01, S02, S04, S05, S06, S07, S08, S09 |
| CRE-D13 | 99-107 | WOE_FICO: not missing(FICO_SCORE) then 6 bins, else 0.198 | >=760: 44<br>[720,760): 35<br>[680,720): 26<br>[640,680): 18<br>[600,640): 44<br><600: 69<br>missing: 0 | N | S01, S02, S04, S05, S06, S07, S08, S09 |
| CRE-D14 | 110-118 | WOE_UTIL: not missing(UTILIZATION_PCT) then 6 bins, else 0 | <=10: 4<br>(10,30]: 39<br>(30,50]: 41<br>(50,70]: 21<br>(70,90]: 7<br>>90: 9<br>missing: 115 | Y | S01, S02, S04, S05, S06, S07, S08, S09 |
| CRE-D15 | 121-126 | WOE_DPD: not missing(PMT_LATE_90_12MO) then =0 / =1 / other, else 0 | =0: 219<br>=1: 15<br>other (>=2): 2<br>missing: 0 | N | S01, S02, S04, S05, S06, S07, S08, S09 |
| CRE-D16 | 128-135 | WOE_AGE: not missing(ACCT_AGE_MONTHS) then 4 bins, else 0 | >=120: 96<br>[60,120): 70<br>[24,60): 44<br><24: 26<br>missing: 0 | N | S01, S02, S04, S05, S06, S07, S08, S09 |
| CRE-D17 | 138, 147 | WOE_LTV gate: ACCOUNT_TYPE in ('MTG','AUTO','HELC') else 0 | secured (MTG/AUTO/HELC): 108<br>unsecured: 128 | Y | S01, S02, S04, S05, S06, S07, S08, S09 |
| CRE-D18 | 139-145 | WOE_LTV: not missing(LTV) then 4 bins, else 0 | <=0.60: 28<br>(0.60,0.80]: 46<br>(0.80,1.00]: 24<br>>1.00: 10<br>missing: 0 | N | S01, S02, S04, S05, S06, S07, S08, S09 |
| CRE-D19 | 161-168 | LGD: secured with LTV / secured LTV missing 0.40 / CC 0.75 / else 0.50 | secured, LTV present: 108<br>secured, LTV missing -> 0.40: 0<br>CC -> 0.75: 91<br>other (PERS/LOC) -> 0.50: 37 | N | S01, S02, S04, S05, S06, S07, S08, S09 |
| CRE-D20 | 163 | LGD = max(0, min(1,(LTV-0.5)*0.8)) clamp sides | within [0,1]: 85<br>clamped to 0: 23<br>clamped to 1: 0 | N | S01, S02, S04, S05, S06, S07, S08, S09 |
| CRE-D21 | 172-175 | EAD: ACCOUNT_TYPE in ('CC','LOC','HELC') -> BAL + 0.5*(LIMIT-BAL) else BAL | revolving (CC/LOC/HELC): 121<br>term (MTG/AUTO/PERS): 115 | Y | S01, S02, S04, S05, S06, S07, S08, S09 |
| CRE-D22 | 173, 175, 179 | missing arithmetic with + - * (not sum()): missing operand -> EAD / EXPECTED_LOSS missing | EAD present: 236<br>CURRENT_BALANCE missing -> EAD/EL missing: 0<br>CREDIT_LIMIT missing (revolving) -> EAD/EL missing: 0 | N | S01, S02, S04, S05, S06, S07, S08, S09 |
| CRE-D23 | 183-189 | NEW_RISK_RATING IF/ELSE ladder on PD (PD is bounded to [0.01438, 0.12884] by the coefficients, so ratings 1, 2, 6, 7 are dead code) | rating 1 (unreachable): 0<br>rating 2 (unreachable): 0<br>rating 3: 99<br>rating 4: 137<br>rating 5: 0<br>rating 6 (unreachable): 0<br>rating 7 (unreachable): 0 | N | S01, S02, S04, S05, S06, S07, S08, S09 |
| CRE-D24 | 218-220 | RISK_MIGRATION inner join WORK.SCORED x CUST_ACCOUNTS_DAILY on ACCOUNT_ID (+ SNAPSHOT_DATE filter): 1 match vs many | one CAD match: 236<br>multiple CAD matches (fan-out): 0 | N | S01, S02, S04, S05, S06, S07, S08, S09 |
| CRE-D25 | 220-222 | WHERE (a.RISK_RATING ne s.NEW_RISK_RATING or a.RISK_RATING is null) | RISK_RATING ne NEW_RISK_RATING (kept): 189<br>RISK_RATING missing (kept): 6<br>RISK_RATING = NEW_RISK_RATING (dropped): 41 | Y | S01, S02, S04, S05, S06, S07, S08, S09 |
| CRE-D26 | 209-214 | CASE MIGRATION_DIRECTION (STABLE needs RISK_RATING = NEW_RISK_RATING, which the WHERE removes -> dead code) | NEW: 6<br>UPGRADE: 76<br>DOWNGRADE: 113<br>STABLE (unreachable): 0 | N | S01, S02, S04, S05, S06, S07, S08, S09 |
| CRE-D27 | 231-232 | PROC APPEND base=CURATED.RISK_SCORES: base absent/empty vs existing history (rows accumulate) | base absent/empty: 1<br>base has prior rows (accumulate): 0 | N | S01, S02, S03, S04, S05, S06, S07, S08, S09 |
| CRE-D28 | 238-239 | PROC APPEND base=CURATED.RISK_MIGRATION: base absent/empty vs existing history | base absent/empty: 1<br>base has prior rows (accumulate): 0 | N | S01, S02, S03, S04, S05, S06, S07, S08, S09 |
| CRE-D29 | 229, 234, 236, 241 + macros/lock.sas | %lock(...) calls are positional but %lock has only keyword parameters -> macro invocation ERROR, no lock taken; lock-acquired / lock-timeout (%abort cancel or SYSCC) branches cannot run as written | positional %lock call (macro error, lock never taken): 4<br>lock acquired (unreachable): 0<br>lock timeout -> abort/SYSCC (unreachable): 0 | N | S01, S02, S03, S04, S05, S06, S07, S08, S09 |
| CRE-D30 | 246-255 | PROC MEANS NWAY sum(EAD)/sum(EXPECTED_LOSS)/mean(): missing ignored; all-missing group -> missing sum | all EAD present: 12<br>some EAD missing -> ignored: 0<br>all EAD missing -> sum missing: 0 | N | S01, S02, S04, S05, S06, S07, S08, S09 |
| CRE-D31 | 246-261 + macros/nobs.sas | empty WORK.SCORED (%nobs = 0): zero-row outputs, PROC MEANS writes 0 obs | WORK.SCORED nobs > 0: 1<br>WORK.SCORED nobs = 0: 0 | N | S01, S02, S03, S04, S05, S06, S07, S08, S09 |
| CRE-D32 | 17, 19, 191, 220, autoexec_local.sas 74 | score_date value: default &CURR_DT=31JAN2024 (month-end), mid-month, quarter-end, year-end, leap day, blank | default 31JAN2024 (month-end): 1<br>mid-month: 0<br>quarter-end: 0<br>year-end: 0<br>leap day: 0<br>blank: 0 | N | S01, S02, S03, S04, S05, S06, S07, S08, S09, S10 |
| CRE-D33 | 17, 192 | model_id default CRM-2023-Q4-v2 vs override | default: 1<br>override: 0 | N | S01, S02, S03, S04, S05, S06, S07, S08, S09, S10 |
| CRE-D34 | 19-20 + macros/parmv.sas | %parmv(_req=1): non-blank vs blank model_id (ERROR logged, macro continues) vs blank score_date (ERROR, invalid ""d -> steps fail) | score_date & model_id non-blank: 1<br>model_id blank (ERROR, run continues): 0<br>score_date blank (ERROR, no output): 0 | N | S01, S02, S03, S04, S05, S06, S07, S08, S09, S10 |
| CRE-D35 | 19-20 + parmv.sas 205-208 | %parmv default _CASE=U rewrites the caller macro variable with %qupcase -> MODEL_ID is upper-cased | upcased: 1<br>unchanged: 0 | N | S01, S02, S03, S04, S05, S06, S07, S08, S09, S10 |
