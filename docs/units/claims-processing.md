# Unit Verification Packet — claims_processing.sas

Track: SAS → dbt (branch `devin/sas-track`)
Legacy artifact: `legacy/sas/programs/claims_processing.sas`
Business date: 31JAN2024 (pinned)

## 1. Unit Overview

`claims_processing.sas` is the daily insurance claims intake and adjudication job
(scheduled 08:00 via Control-M `INS_DAILY_01`). The program is a single macro
`%claims_processing(proc_date=&CURR_DT)` that:

1. **Ingest & validate** — reads the daily feed `RAW_INS.CLAIMS_FEED_YYYYMMDD`
   (dataset name derived from `proc_date` via `putn(..., yymmddn8.)`) and validates
   each claim with a **hash-object lookup** (`declare hash h_pol`) loaded from
   `RAW_INS.POLICIES` filtered to `STATUS='ACTIVE'` (key `POLICY_ID`; data
   `POLICY_TYPE`, `EFFECTIVE_DATE`, `EXPIRATION_DATE`, `SUM_INSURED`, `DEDUCTIBLE`).
   Three sequential checks reject a claim: policy not found/inactive
   (`h_pol.find() ne 0`), loss date outside the policy period, and claimed amount
   exceeding sum insured. Rejects go to `WORK.CLAIMS_INVALID` (WORK-only, never
   persisted); survivors to `WORK.CLAIMS_VALID`.
2. **Fraud screening** — PROC SQL left join to `TERA_DW.FRAUD_INDICATORS` on
   `POLICY_ID` + `CLAIMANT_ID`, deriving `FRAUD_RISK` bands
   (`>=80` → HIGH, `>=50` → MEDIUM, else LOW). HIGH-risk rows become
   `WORK.FRAUD_ALERTS` with `ALERT_REASON` (fraud score + indicator flags) and
   `ALERT_DATE = "&proc_date"d`; a `%sendmail` SIU notification fires when any exist.
3. **Auto-adjudication** — sequential first-match-wins rules with `RETURN`:
   HIGH fraud → `DENY` / approved 0 → **manual review queue**; LOW risk and
   `CLAIMED_AMOUNT <= 5000` with `POLICY_TYPE in ('AUTO','HOME','RENT')` → `APPR`
   with `APPROVED_AMOUNT = max(0, CLAIMED_AMOUNT - DEDUCTIBLE)`; LOW risk within
   25% of sum insured and `<= 50000` → `APPR` (same approved-amount formula);
   everything else → `PEND` with a composed reason, `APPROVED_AMOUNT = .`,
   routed to manual review.
4. **Register update** — auto-adjudicated + manual-review rows are combined,
   stamped with `PROCESSING_DATE = "&proc_date"d` and
   `CLAIM_STATUS = ADJUDICATION_RESULT` (displayed via the `$CLMSTAT.` format),
   then `PROC APPEND FORCE`-ed into the persistent targets.

**Sources (from the legacy program header and body):**

| Source | Role |
|---|---|
| `RAW_INS.CLAIMS_FEED_YYYYMMDD` | daily claims feed (existence-checked; `%goto ABORT` if missing) |
| `RAW_INS.POLICIES` | hash lookup, ACTIVE policies only |
| `TERA_DW.FRAUD_INDICATORS` | fraud scores / indicator flags (left join) |

**Targets:**

| Target | Content |
|---|---|
| `STG_INS.CLAIMS_REGISTER` | all adjudicated claims (APPR/DENY/PEND) with processing date and status |
| `STG_INS.CLAIMS_REVIEW_QUEUE` | manual review queue (DENY high-fraud + PEND) |
| `STG_INS.FRAUD_ALERTS` | HIGH fraud-risk claims routed to SIU |

**dbt implementation (existing on `devin/sas-track`):** staging models
`stg_claims_feed`, `stg_policies`, `stg_fraud_indicators`; intermediates
`int_claims_valid` (hash lookup as inner join on ACTIVE policies + validation
filters), `int_fraud_check`, `int_claims_adjudicated`; marts `claims_register`
(with `claim_status_desc` materializing the `$CLMSTAT.` format via seed
`fmt_claim_status`), `claims_review_queue`, `fraud_alerts`.

## 2. STM Excerpt (claims_processing only)

Extracted from `docs/stm/sas_stm.md` (regenerated this run with
`python3 tools/sas_lineage.py`).


**Purpose:** Ingest new claims from feed, validate against policy data, apply auto-adjudication rules, route for manual review, and update claims register.

**Macro:** `%claims_processing` — parameters: `proc_date=&CURR_DT`

**Inputs:** `RAW_INS.&feed_ds`, `RAW_INS.POLICIES`, `STG_INS.CLAIMS_REGISTER`, `STG_INS.CLAIMS_REVIEW_QUEUE`, `STG_INS.FRAUD_ALERTS`, `TERA_DW.FRAUD_INDICATORS` (feed pattern: `CLAIMS_FEED_YYYYMMDD`)
**Persistent outputs:** `STG_INS.CLAIMS_REGISTER`, `STG_INS.CLAIMS_REVIEW_QUEUE`, `STG_INS.FRAUD_ALERTS`

| Output Dataset | Column | Derivation | Source(s) |
|---|---|---|---|
| WORK.CLAIMS_VALID / WORK.CLAIMS_INVALID | *(step)* | hash h_pol(dataset: "RAW_INS.POLICIES(where=(STATUS='ACTIVE'))") key=POLICY_ID data=POLICY_TYPE,EFFECTIVE_DATE,EXPIRATION_DATE,SUM_INSURED,DEDUCTIBLE; DROP (all outputs): VALIDATION_ERROR RC | RAW_INS.&FEED_DS |
| WORK.CLAIMS_VALID / WORK.CLAIMS_INVALID | RC | `h_pol.find()` | RAW_INS.&FEED_DS |
| WORK.CLAIMS_VALID / WORK.CLAIMS_INVALID | VALIDATION_ERROR | if `rc ne 0` then `catx(' ', 'Policy not found or inactive:', POLICY_ID)` | RAW_INS.&FEED_DS |
| WORK.CLAIMS_VALID / WORK.CLAIMS_INVALID | VALIDATION_ERROR | if `LOSS_DATE < EFFECTIVE_DATE or LOSS_DATE > EXPIRATION_DATE` then `catx(' ', 'Loss date', put(LOSS_DATE, date9.), 'outside policy period', put(EFFECTIVE_DATE, date9.), '-', put(EXPIRATION_DATE, date9.))` | RAW_INS.&FEED_DS |
| WORK.CLAIMS_VALID / WORK.CLAIMS_INVALID | VALIDATION_ERROR | if `CLAIMED_AMOUNT > SUM_INSURED` then `catx(' ', 'Claimed amount', put(CLAIMED_AMOUNT, dollar18.2), 'exceeds sum insured', put(SUM_INSURED, dollar18.2))` | RAW_INS.&FEED_DS |
| WORK.CLAIMS_INVALID | *(row output)* | when `rc ne 0` | RAW_INS.&FEED_DS |
| WORK.CLAIMS_INVALID | *(row output)* | when `LOSS_DATE < EFFECTIVE_DATE or LOSS_DATE > EXPIRATION_DATE` | RAW_INS.&FEED_DS |
| WORK.CLAIMS_INVALID | *(row output)* | when `CLAIMED_AMOUNT > SUM_INSURED` | RAW_INS.&FEED_DS |
| WORK.CLAIMS_VALID | *(row output)* | always | RAW_INS.&FEED_DS |
| WORK.CLAIMS_VALID / WORK.CLAIMS_INVALID | EFFECTIVE_DATE | display format `date9.` | RAW_INS.&FEED_DS |
| WORK.CLAIMS_VALID / WORK.CLAIMS_INVALID | EXPIRATION_DATE | display format `date9.` | RAW_INS.&FEED_DS |
| WORK.FRAUD_CHECK | *(step)* | left join TERA_DW.FRAUD_INDICATORS f on c.POLICY_ID = f.POLICY_ID and c.CLAIMANT_ID = f.CLAIMANT_ID | WORK.CLAIMS_VALID c; TERA_DW.FRAUD_INDICATORS f |
| WORK.FRAUD_CHECK | C.* | `pass-through (all columns)` | WORK.CLAIMS_VALID c; TERA_DW.FRAUD_INDICATORS f |
| WORK.FRAUD_CHECK | FRAUD_SCORE | `f.FRAUD_SCORE` | WORK.CLAIMS_VALID c; TERA_DW.FRAUD_INDICATORS f |
| WORK.FRAUD_CHECK | INDICATOR_FLAGS | `f.INDICATOR_FLAGS` | WORK.CLAIMS_VALID c; TERA_DW.FRAUD_INDICATORS f |
| WORK.FRAUD_CHECK | FRAUD_RISK | `case when f.FRAUD_SCORE >= 80 then 'HIGH' when f.FRAUD_SCORE >= 50 then 'MEDIUM' else 'LOW' end` | WORK.CLAIMS_VALID c; TERA_DW.FRAUD_INDICATORS f |
| WORK.FRAUD_ALERTS | *(step)* | WHERE FRAUD_RISK = 'HIGH' | WORK.FRAUD_CHECK |
| WORK.FRAUD_ALERTS | ALERT_REASON | `catx('; ', catx(' ', 'Fraud score:', put(FRAUD_SCORE, 4.)), INDICATOR_FLAGS)` | WORK.FRAUD_CHECK |
| WORK.FRAUD_ALERTS | ALERT_DATE | `"&proc_date"d` | WORK.FRAUD_CHECK |
| WORK.FRAUD_ALERTS | ALERT_DATE | display format `date9.` | WORK.FRAUD_CHECK |
| WORK.AUTO_ADJUDICATED / WORK.MANUAL_REVIEW | ADJUDICATION_RESULT | if `FRAUD_RISK = 'HIGH'` then `'DENY'` | WORK.FRAUD_CHECK |
| WORK.AUTO_ADJUDICATED / WORK.MANUAL_REVIEW | ADJUDICATION_REASON | if `FRAUD_RISK = 'HIGH'` then `'High fraud risk - SIU referral'` | WORK.FRAUD_CHECK |
| WORK.AUTO_ADJUDICATED / WORK.MANUAL_REVIEW | APPROVED_AMOUNT | if `FRAUD_RISK = 'HIGH'` then `0` | WORK.FRAUD_CHECK |
| WORK.AUTO_ADJUDICATED / WORK.MANUAL_REVIEW | ADJUDICATION_RESULT | if `FRAUD_RISK = 'LOW' and CLAIMED_AMOUNT <= 5000 and POLICY_TYPE in ('AUTO','HOME','RENT')` then `'APPR'` | WORK.FRAUD_CHECK |
| WORK.AUTO_ADJUDICATED / WORK.MANUAL_REVIEW | ADJUDICATION_REASON | if `FRAUD_RISK = 'LOW' and CLAIMED_AMOUNT <= 5000 and POLICY_TYPE in ('AUTO','HOME','RENT')` then `'Auto-approved: low risk, small claim'` | WORK.FRAUD_CHECK |
| WORK.AUTO_ADJUDICATED / WORK.MANUAL_REVIEW | APPROVED_AMOUNT | if `FRAUD_RISK = 'LOW' and CLAIMED_AMOUNT <= 5000 and POLICY_TYPE in ('AUTO','HOME','RENT')` then `max(0, CLAIMED_AMOUNT - DEDUCTIBLE)` | WORK.FRAUD_CHECK |
| WORK.AUTO_ADJUDICATED / WORK.MANUAL_REVIEW | ADJUDICATION_RESULT | if `FRAUD_RISK = 'LOW' and CLAIMED_AMOUNT <= SUM_INSURED * 0.25 and CLAIMED_AMOUNT <= 50000` then `'APPR'` | WORK.FRAUD_CHECK |
| WORK.AUTO_ADJUDICATED / WORK.MANUAL_REVIEW | ADJUDICATION_REASON | if `FRAUD_RISK = 'LOW' and CLAIMED_AMOUNT <= SUM_INSURED * 0.25 and CLAIMED_AMOUNT <= 50000` then `'Auto-approved: within 25% of sum insured'` | WORK.FRAUD_CHECK |
| WORK.AUTO_ADJUDICATED / WORK.MANUAL_REVIEW | APPROVED_AMOUNT | if `FRAUD_RISK = 'LOW' and CLAIMED_AMOUNT <= SUM_INSURED * 0.25 and CLAIMED_AMOUNT <= 50000` then `max(0, CLAIMED_AMOUNT - DEDUCTIBLE)` | WORK.FRAUD_CHECK |
| WORK.AUTO_ADJUDICATED / WORK.MANUAL_REVIEW | ADJUDICATION_RESULT | `'PEND'` | WORK.FRAUD_CHECK |
| WORK.AUTO_ADJUDICATED / WORK.MANUAL_REVIEW | ADJUDICATION_REASON | `catx('; ', ifc(FRAUD_RISK='MEDIUM', 'Medium fraud risk', ''), ifc(CLAIMED_AMOUNT > 50000, 'Large claim', ''), ifc(CLAIMED_AMOUNT > SUM_INSURED * 0.25, 'Exceeds 25% threshold', ''))` | WORK.FRAUD_CHECK |
| WORK.AUTO_ADJUDICATED / WORK.MANUAL_REVIEW | APPROVED_AMOUNT | `.` | WORK.FRAUD_CHECK |
| WORK.MANUAL_REVIEW | *(row output)* | when `FRAUD_RISK = 'HIGH'` | WORK.FRAUD_CHECK |
| WORK.AUTO_ADJUDICATED | *(row output)* | when `FRAUD_RISK = 'LOW' and CLAIMED_AMOUNT <= 5000 and POLICY_TYPE in ('AUTO','HOME','RENT')` | WORK.FRAUD_CHECK |
| WORK.AUTO_ADJUDICATED | *(row output)* | when `FRAUD_RISK = 'LOW' and CLAIMED_AMOUNT <= SUM_INSURED * 0.25 and CLAIMED_AMOUNT <= 50000` | WORK.FRAUD_CHECK |
| WORK.MANUAL_REVIEW | *(row output)* | always | WORK.FRAUD_CHECK |
| WORK.CLAIMS_COMBINED | PROCESSING_DATE | `"&proc_date"d` | WORK.AUTO_ADJUDICATED, WORK.MANUAL_REVIEW |
| WORK.CLAIMS_COMBINED | CLAIM_STATUS | `ADJUDICATION_RESULT` | WORK.AUTO_ADJUDICATED, WORK.MANUAL_REVIEW |
| WORK.CLAIMS_COMBINED | PROCESSING_DATE | display format `date9.` | WORK.AUTO_ADJUDICATED, WORK.MANUAL_REVIEW |
| WORK.CLAIMS_COMBINED | CLAIM_STATUS | display format `$CLMSTAT.` | WORK.AUTO_ADJUDICATED, WORK.MANUAL_REVIEW |
| STG_INS.CLAIMS_REGISTER | *(all columns of base)* | PROC APPEND FORCE (extra columns dropped) | WORK.CLAIMS_COMBINED |
| STG_INS.CLAIMS_REVIEW_QUEUE | *(all columns of base)* | PROC APPEND FORCE (extra columns dropped) | WORK.MANUAL_REVIEW |
| STG_INS.FRAUD_ALERTS | *(all columns of base)* | PROC APPEND FORCE (extra columns dropped) | WORK.FRAUD_ALERTS |

**Notes / ambiguities:**
- The hash object loads RAW_INS.POLICIES filtered to STATUS='ACTIVE'; a failed FIND (rc ne 0) covers both unknown and inactive policies. POLICY_ID is unique in the seed data so hash duplicate-key handling is not exercised.
- TERA_DW.FRAUD_INDICATORS is seeded as legacy/sas/data/csv/raw_ins/FRAUD_INDICATORS.csv (the insurance seed directory stands in for the Teradata libref).
- The `drop VALIDATION_ERROR rc;` statement applies to both step-1 outputs; WORK.CLAIMS_INVALID is WORK-only and not persisted.
- Adjudication rules are sequential with RETURN — first match wins. DENY (high fraud) rows go to the manual-review queue, not the auto-adjudicated set.
- $CLMSTAT. on CLAIM_STATUS is a display format; codes are stored. The migration adds an explicit CLAIM_STATUS_DESC column via a seed lookup implementing the format.


## 3. Verification Evidence

All commands run from the repo root on branch `devin/unit-claims-processing`
(based on `devin/sas-track`), dbt run from inside `dbt/sas`:

```bash
python3 -m pip install duckdb dbt-duckdb 'pandas<3'
python3 tools/sas_lineage.py      # -> docs/stm/sas_stm.json / sas_stm.md
python3 tools/sas_baseline.py     # -> baseline/sas/*
python3 tools/sas_load_raw.py     # -> raw seeds into dbt/sas/dev.duckdb
(cd dbt/sas && dbt build --profiles-dir . --no-partial-parse)
python3 tools/parity_diff.py --baseline baseline/sas --actual dbt/sas/dev.duckdb \
  --schema main --keys tools/keys/sas_keys.json --report /tmp/parity.md
```

Key run output:

```
sas_baseline.py:
  baseline FRAUD_ALERTS: 19 rows
  baseline CLAIMS_REGISTER: 190 rows
  baseline CLAIMS_REVIEW_QUEUE: 101 rows

sas_load_raw.py (this unit's inputs):
  loaded raw_ins.claims_feed_20240131: 260 rows
  loaded raw_ins.policies: 320 rows
  loaded raw_ins.fraud_indicators: 102 rows

dbt build:
  Finished running 8 seeds, 17 table models, 67 data tests, 25 view models
  Completed successfully
  Done. PASS=117 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=117
```

Parity report sections for this unit's targets (copied from `/tmp/parity.md`):

```
## CLAIMS_REGISTER
- rows: baseline=190 actual=190
- columns compared: 22
- result: **MATCH** (all values within tolerance)

## CLAIMS_REVIEW_QUEUE
- rows: baseline=101 actual=101
- columns compared: 19
- result: **MATCH** (all values within tolerance)

## FRAUD_ALERTS
- rows: baseline=19 actual=19
- columns compared: 18
- result: **MATCH** (all values within tolerance)
```

Overall report verdict: `**Overall: PARITY VERIFIED**` — **parity exit code: 0**.

Row counts per target: CLAIMS_REGISTER = 190, CLAIMS_REVIEW_QUEUE = 101,
FRAUD_ALERTS = 19 (baseline and dbt actual identical).

Note: 190 register rows from a 260-row feed — 70 feed rows fail step-1
validation (inactive/unknown policy, loss date outside period, or claimed
amount over sum insured) and are dropped, matching the legacy
`WORK.CLAIMS_INVALID` branch which is never persisted.

## 4. Snowflake Notes

Items in this unit's SQL that a Snowflake deployment should review:

- **Hash-object semantics as inner join** — `int_claims_valid` renders the SAS
  hash lookup as an `inner join ... and p.status = 'ACTIVE'`. This is correct
  only while `POLICY_ID` is unique in `POLICIES`; SAS hash `find()` keeps the
  *first* loaded row on duplicate keys, while a join would fan out. If Snowflake
  source data can contain duplicate active policies, add a
  `qualify row_number() ... = 1` dedup (Snowflake supports `QUALIFY`).
- **`run_date` var, not dynamic dataset names** — the legacy feed name
  `CLAIMS_FEED_YYYYMMDD` is pinned via the dbt var `run_date='2024-01-31'` and a
  static `stg_claims_feed`. On Snowflake, parameterize the feed table/partition
  per run date (e.g. via a dbt var or dynamic source selection) rather than
  hard-coding.
- **String concatenation / `catx` emulation** — `alert_reason` and the PEND
  `adjudication_reason` are built with `||` and empty-string trimming to mimic
  `catx`'s skip-empty-arguments behavior. `||` with a NULL operand yields NULL
  in Snowflake (as in DuckDB); the models guard with `coalesce`/`trim` checks —
  keep those guards.
- **Numeric formatting in text** — `'Fraud score: ' || cast(cast(fraud_score as
  integer) as varchar)` reproduces SAS `put(FRAUD_SCORE, 4.)`. Verify Snowflake
  integer-to-varchar rendering matches if fraud scores can be non-integral.
- **`$CLMSTAT.` format** — materialized as the seed `fmt_claim_status` joined in
  `claims_register` (`claim_status_desc`). On Snowflake, load this seed (or a
  reference table) and keep the `coalesce(f.label, 'Unknown')` default.
- **APPEND vs full-refresh** — the legacy job `PROC APPEND`s daily into the
  register/queue/alert tables; the dbt models rebuild them for the pinned run
  date. A Snowflake deployment running daily should convert these marts to
  incremental models keyed on `processing_date` / `alert_date`.
- **Date handling** — `loss_date` between `effective_date`/`expiration_date`
  comparisons rely on true DATE types (ISO-8601 normalized in staging). Ensure
  Snowflake ingestion lands these as DATE, not VARCHAR.
- **SIU email side effect** — the `%sendmail` notification on fraud alerts is
  intentionally out of scope for dbt; wire an equivalent alert (e.g. Snowflake
  alert/task or downstream orchestration) if required operationally.
