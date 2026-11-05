# m_demo_mapping1 — independent semantics review

Scope: DEMO_TARGET5, DEMO_TARGET6, DEMO_TARGET3 of `MAPPING NAME="m_demo_mapping1"` in
`legacy/informatica/wf_demo_mapping.XML` (lines 428-899). Everything in sections 1-2 is
derived from the XML (TRANSFORMFIELD / TABLEATTRIBUTE / CONNECTOR elements) and the seed
CSVs in `legacy/informatica/data/`. Section 3 compares that derivation to
`tools/informatica_baseline.py::mapping1()`, which is the parity oracle. Sections 4-5 cover
the dbt models and the offline parity run.

Business date (SYSDATE / SYSTIMESTAMP) is pinned to 2024-01-31 per `tools/README.md`.

## 1. Per-transformation semantics

### Data flow

```
demo_source3 ─┐
              ├─ sq_demo_source4 (SQL override) ─ exp_TRANS ─┬─ lkp_TRANS2 (connected) ─┐
demo_source4 ─┘                                  │           └─ lkp_TRANS3 (connected) ─┤
                                                 │  :LKP.lkp_TRANS1 (unconnected)        │
                                                 └───────────────────────────────── exp_TRANS1
                                                                                          │
                                                                                      rtr_TRANS
                                     demo_target6_GRP ── agg_TRANS ─┬─ demo_target6 ◄── SEQ_GEN.NEXTVAL
                                     demo_target5_GRP ──────────────┴─ demo_target5
                                     DEFAULT1 ── (not connected: rows dropped)

demo_source5 (flat file) ─ SQ_demo_source5 ─ exp_TRANS2 ─ demo_target3
```

TARGETLOADORDER: demo_target6 = 1, demo_target5 = 1, demo_target3 = 2 (no data dependency
between the pipelines; order is irrelevant for content).

### sq_demo_source4 (Source Qualifier, associated sources demo_source3 + demo_source4)

`Sql Query` override (verbatim, CR/LF collapsed):

```sql
SELECT demo_source4.ACCT_ID, demo_source4.ACCT_TYP, demo_source4.ACCT_DESC, demo_source4.CRDT_LN,
       SYSTIMESTAMP, demo_source4.CLSR_DT, demo_source4.ACCT_STAT_CD,
       demo_source3.TX_ID, demo_source3.LAST_NM, demo_source3.TX_DTTM, demo_source3.TX_AMT,
       demo_source3.BAL_AMT, demo_source3.CUST_ID,
       STRCMP(demo_source4.ACCT_STAT_CD, demo_source3.TX_TYPE_CD)
FROM demo_source3 INNER JOIN demo_source4 ON demo_source3.ACCT_ID = demo_source4.ACCT_ID
ORDER BY demo_source4.ACCT_ID
```

- Override columns bind **positionally** to the SQ ports in TRANSFORMFIELD order:
  ACCT_ID, ACCT_TYP, ACCT_DESC, CRDT_LN, **CR8_DT**, CLSR_DT, ACCT_STAT_CD, TX_ID, LAST_NM,
  TX_DTTM, TX_AMT, BAL_AMT, CUST_ID, **TX_TYPE_CD**.
- Position 5 `SYSTIMESTAMP` lands in port `CR8_DT`; the source column demo_source4.CR8_DT is
  connected to the SQ but never selected, so it is ignored. CR8_DT = run timestamp
  (pinned: 2024-01-31 00:00:00).
- Position 14 `STRCMP(...)` lands in port `TX_TYPE_CD`. SQ.TX_TYPE_CD has no outgoing
  CONNECTOR, so the value is discarded. (STRCMP is not an Oracle function; on the real
  `oracle` DBD the override would fail at parse time. Treated as a no-op, as in the baseline.)
- INNER JOIN on ACCT_ID: accounts without transactions and transactions without accounts are
  dropped. With the seeds all 6 demo_source3 rows join (1001 x2, 1002..1005 x1).
- `ORDER BY demo_source4.ACCT_ID` only. Order *within* an ACCT_ID is unspecified
  (relevant for agg_TRANS, below). `Number Of Sorted Ports = 1` is consistent with this
  ordering but ignored when an override exists. Not DISTINCT; no source filter.
- demo_source3.FIRST_NM, demo_source3.CRDT_SCORE, demo_source3.TX_TYPE_CD,
  demo_source3.TX_DESC are **not** selected — FIRST_NM and CRDT_SCORE in the targets come
  from lookups, not from demo_source3.

### exp_TRANS (Expression)

| Port | Type | Expression |
|---|---|---|
| CRDT_LN | INPUT decimal(38,0) | (SQ string(38) -> implicit decimal conversion) |
| CLSR_DT, TX_DTTM, BAL_AMT, ACCT_DESC, ACCT_TYP, ACCT_STAT_CD, TX_ID, LAST_NM, TX_AMT, ACCT_ID, CR8_DT, CUST_ID | I/O | pass-through |
| o_acc_trim | OUT string(200), default ' ' | `RTRIM(ACCT_TYP)` |
| o_crdt_trim | OUT string(200), default ' ' | `LTRIM(CRDT_LN)` (CRDT_LN is decimal here, so the value is the number rendered as text, e.g. `'  8000'` -> 8000 -> `'8000'`) |
| o_ACCT_ID | OUT string(38), default ' ' | `:LKP.lkp_TRANS1(ACCT_ID)` (unconnected lookup; returns TX_TYPE_CD) |

Despite its name, `o_ACCT_ID` carries a **transaction type code**, and lands in
demo_target6.TX_TYPE_CD.

### Lookups

| Lookup | Mode | Table | Condition | Returned/used port | Multiple-match policy | Tie in seeds | Resolved value |
|---|---|---|---|---|---|---|---|
| lkp_TRANS1 | unconnected (`:LKP.` from exp_TRANS.o_ACCT_ID) | lkp_demo_source3 | `ACCT_ID = IN_ACCT_ID` | TX_TYPE_CD (LOOKUP/RETURN/OUTPUT) | Use Last Value | ACCT_ID 1002: rows `TR` (seed row 2) then `DR` (seed row 3) | `DR` |
| lkp_TRANS2 | connected (IN_ACCT_ID <- exp_TRANS.ACCT_ID) | lkp_demo_source1 | `ACCT_ID = IN_ACCT_ID` | FIRST_NM -> exp_TRANS1.FIRST_NM | Use Last Value | ACCT_ID 1002: `NINA` then `ZOE` | `ZOE` (1002 is SB, so not visible in DEMO_TARGET5) |
| lkp_TRANS3 | connected (IN_CUST_ID <- exp_TRANS.CUST_ID) | lkp_demo_source2 | `CUST_ID = IN_CUST_ID` | CRDT_SCORE -> exp_TRANS1.CRDT_SCORE | Use Last Value | CUST_ID 70032: 435 then 450 | 450 (CUST 70032 belongs to SB account 1002; not visible in any target) |

All three: static cache, no SQL override, no source filter, case-insensitive string compare,
default value empty -> no match yields NULL. Baseline tie-break convention: "last" = last
**physical seed row** (`ROW_NUMBER() OVER (PARTITION BY key ORDER BY __seed_row DESC) = 1`).
In real PowerCenter, "Use Last Value" means last row in cache order, which for a non-ordered
lookup query is not guaranteed to equal physical order; the seed convention is a fixture
decision. The only tie observable in m1 targets is lkp_TRANS1 / ACCT_ID 1002 ->
DEMO_TARGET6.TX_TYPE_CD = `DR` (first-value would give `TR`).

### exp_TRANS1 (Expression)

All ports I/O pass-through except `o_ACCT_DESC` = `RTRIM(ACCT_DESC)` (OUT string(50)).
Port precision changes that could truncate: FIRST_NM string(10) (lookup returns string(20)),
CRDT_SCORE becomes **string(38)** (lookup decimal). No seed value exceeds 10 chars, so no
truncation is observable.

### rtr_TRANS (Router)

| Group | Order | Filter | Connected to |
|---|---|---|---|
| demo_target6_GRP | 2 | `ACCT_TYP = 'SB'` | agg_TRANS -> demo_target6 |
| demo_target5_GRP | 3 | `ACCT_TYP != 'SB'` | demo_target5 |
| DEFAULT1 | 4 | (rows matching no group) | **nothing** -> rows dropped |

- Filters test the raw `ACCT_TYP` (not `o_acc_trim`), so `'SB '` with trailing blanks would
  go to demo_target5. No such seed value exists.
- NULL / blank ACCT_TYP: both `NULL = 'SB'` and `NULL != 'SB'` evaluate to NULL (not TRUE), so
  the row goes only to DEFAULT1, which is unconnected. ACCT_ID **1005** (ACCT_TYP empty in
  `demo_source4.csv`; empty = NULL in Oracle and in DuckDB's CSV reader) therefore appears in
  **neither** DEMO_TARGET5 nor DEMO_TARGET6. A model that uses `COALESCE(ACCT_TYP,'') != 'SB'`
  or `NOT (ACCT_TYP = 'SB')` with NULL-safe semantics would wrongly route 1005 to target5.
- Groups are not mutually exclusive in general, but with these two complementary predicates a
  non-NULL row goes to exactly one group.

### agg_TRANS (Aggregator, Sorted Input = YES, scope All Input)

- Group-by: `ACCT_ID` only (EXPRESSIONTYPE="GROUPBY").
- `o_TX_AMT = SUM(TX_AMT)` (OUT decimal(38,0)).
- Every other port (o_ACCT_DESC, TX_AMT input, o_crdt_trim, CLSR_DT, TX_ID, ACCT_STAT_CD,
  TX_DTTM, CR8_DT, o_ACCT_ID, o_acc_trim) is a non-aggregated I/O port: PowerCenter returns the
  value from the **last row received** for the group.
- Sorted Input requires input sorted by ACCT_ID; the SQ `ORDER BY demo_source4.ACCT_ID`
  satisfies this. Within an account, row order is unspecified by the XML, so "last row" is
  non-deterministic for accounts with >1 transaction. Only ACCT_ID 1001 has 2 SB transactions
  (5001, 5002).
- Output: one row per SB account (1001, 1002), emitted in ACCT_ID order.

### SEQ_GEN (Sequence Generator)

Start Value 1, Increment By 1, End Value 2147483647, **Current Value 281**, Cycle YES,
Number of Cached Values 0, Reset NO. NEXTVAL -> demo_target6.ACCT_KEY. The first value issued
in a run is the Current Value, so the aggregator's output rows receive 281, 282, ... in
arrival order (ACCT_ID ascending): 1001 -> 281, 1002 -> 282. (Because Reset = NO, a
re-run in PowerCenter would continue from 283; parity pins the first run.)

### SQ_demo_source5 / exp_TRANS2 (DEMO_TARGET3 pipeline)

SQ_demo_source5: no override, no filter, no sort — all 8 string ports pass through.

| exp_TRANS2 port | Type | Expression |
|---|---|---|
| PRODUCT_ID string(8), PRODUCT_NM string(50), PRODUCT_NO string(10), COLOR string(20), STD_COST string(10), LIST_PRICE string(10) | I/O | pass-through (no truncation with seeds) |
| SELL_ST_DT, SELL_ED_DT | INPUT string(10) | — |
| o_SELL_ST_DT | OUT date/time, default ' ' | `TO_DATE(TO_CHAR(SYSDATE),'DD/MM/YYYY')` |
| o_SELL_ED_DT | OUT date/time, default ' ' | `TO_DATE(SELL_ED_DT,'DD/MM/YYYY')` |

- `o_SELL_ST_DT` ignores the SELL_ST_DT input entirely. `TO_CHAR(SYSDATE)` with no format uses
  the session default `MM/DD/YYYY HH24:MI:SS` -> `'01/31/2024 00:00:00'`; parsing that with
  `DD/MM/YYYY` fails (month 31, trailing time). The baseline maps the failure to NULL for every
  row. (On a run date with day <= 12 it would instead yield a day/month-swapped date.)
- `o_SELL_ED_DT` parses the source string as day/month/year: `17/07/2024` -> 2024-07-17.

## 2. Per-target column lineage

### DEMO_TARGET5 (key ACCT_ID; routed rows with ACCT_TYP != 'SB')

| Target column | Port chain | Source column |
|---|---|---|
| ACCT_ID | rtr_TRANS.ACCT_ID2 <- exp_TRANS1.ACCT_ID <- exp_TRANS.ACCT_ID <- sq_demo_source4.ACCT_ID (pos 1) | demo_source4.ACCT_ID |
| FIRST_NM | rtr_TRANS.FIRST_NM2 <- exp_TRANS1.FIRST_NM <- lkp_TRANS2.FIRST_NM (ACCT_ID = exp_TRANS.ACCT_ID, last value) | lkp_demo_source1.FIRST_NM |
| LAST_NM | rtr_TRANS.LAST_NM2 <- exp_TRANS1.LAST_NM <- exp_TRANS.LAST_NM <- sq_demo_source4.LAST_NM (pos 9) | demo_source3.LAST_NM |
| BAL_AMT | rtr_TRANS.BAL_AMT2 <- exp_TRANS1.BAL_AMT <- exp_TRANS.BAL_AMT <- sq_demo_source4.BAL_AMT (pos 12) | demo_source3.BAL_AMT |
| CRDT_SCORE | rtr_TRANS.CRDT_SCORE2 <- exp_TRANS1.CRDT_SCORE <- lkp_TRANS3.CRDT_SCORE (CUST_ID = exp_TRANS.CUST_ID, last value) | lkp_demo_source2.CRDT_SCORE |

Note: FIRST_NM and CRDT_SCORE are **not** demo_source3.FIRST_NM / CRDT_SCORE. E.g. 1004:
FIRST_NM = `AVA` (lookup) not `NINA` (source3); CRDT_SCORE = 626 (lookup) not 409.
Expected rows: 1003, 1004 (1005 dropped by the router DEFAULT group).

### DEMO_TARGET6 (key ACCT_ID; one row per SB account)

| Target column | Port chain | Source column |
|---|---|---|
| ACCT_ID | agg_TRANS.ACCT_ID (GROUP BY) <- rtr.ACCT_ID1 <- exp_TRANS1 <- exp_TRANS <- SQ pos 1 | demo_source4.ACCT_ID |
| ACCT_TYP | agg.o_acc_trim (last) <- rtr.o_acc_trim1 <- exp_TRANS1 <- exp_TRANS.o_acc_trim = RTRIM(ACCT_TYP) | demo_source4.ACCT_TYP |
| ACCT_DESC | agg.o_ACCT_DESC (last) <- rtr.o_ACCT_DESC1 <- exp_TRANS1.o_ACCT_DESC = RTRIM(ACCT_DESC) | demo_source4.ACCT_DESC |
| CR8_DT | agg.CR8_DT (last) <- rtr.CR8_DT1 <- exp_TRANS1 <- exp_TRANS <- SQ.CR8_DT (pos 5 = SYSTIMESTAMP) | *none* (run timestamp; demo_source4.CR8_DT unused) |
| CRDT_LN | agg.o_crdt_trim (last) <- rtr.o_crdt_trim1 <- exp_TRANS1 <- exp_TRANS.o_crdt_trim = LTRIM(CRDT_LN as decimal) | demo_source4.CRDT_LN |
| CLSR_DT | agg.CLSR_DT (last) <- rtr.CLSR_DT1 <- exp_TRANS1 <- exp_TRANS <- SQ pos 6 | demo_source4.CLSR_DT |
| ACCT_STAT_CD | agg.ACCT_STAT_CD (last) <- rtr.ACCT_STAT_CD1 <- ... <- SQ pos 7 | demo_source4.ACCT_STAT_CD |
| TX_ID | agg.TX_ID (last) <- rtr.TX_ID1 <- ... <- SQ pos 8 | demo_source3.TX_ID |
| ACCT_KEY | SEQ_GEN.NEXTVAL (Current Value 281, +1 per agg output row) | *none* |
| TX_DTTM | agg.TX_DTTM (last) <- rtr.TX_DTTM1 <- ... <- SQ pos 10 | demo_source3.TX_DTTM |
| TX_AMT | agg.o_TX_AMT = SUM(TX_AMT) <- rtr.TX_AMT1 <- ... <- SQ pos 11 | demo_source3.TX_AMT |
| TX_TYPE_CD | agg.o_ACCT_ID (last) <- rtr.o_ACCT_ID1 <- exp_TRANS1 <- exp_TRANS.o_ACCT_ID = :LKP.lkp_TRANS1(ACCT_ID) | lkp_demo_source3.TX_TYPE_CD |

Note: TX_TYPE_CD is the lookup value keyed by ACCT_ID, **not** demo_source3.TX_TYPE_CD
(1001's last transaction 5002 is `CR` in source3, target gets `DR` from lkp_demo_source3).
Expected rows: 1001 (TX_ID 5002, TX_AMT 2031.24, ACCT_KEY 281, TX_TYPE_CD DR) and
1002 (TX_ID 5003, TX_AMT -1238.81, ACCT_KEY 282, TX_TYPE_CD DR via last-value tie).

### DEMO_TARGET3 (key PRODUCT_ID)

| Target column | Port chain | Source column |
|---|---|---|
| PRODUCT_ID | exp_TRANS2.PRODUCT_ID <- SQ_demo_source5.PRODUCT_ID | demo_source5.PRODUCT_ID |
| PRODUCT_NM | exp_TRANS2.PRODUCT_NM <- SQ | demo_source5.PRODUCT_NM |
| PRODUCT_NO | exp_TRANS2.PRODUCT_NO <- SQ | demo_source5.PRODUCT_NO |
| COLOR | exp_TRANS2.COLOR <- SQ | demo_source5.COLOR |
| STD_COST | exp_TRANS2.STD_COST <- SQ | demo_source5.STD_COST |
| LIST_PRICE | exp_TRANS2.LIST_PRICE <- SQ | demo_source5.LIST_PRICE |
| SELL_ST_DT | exp_TRANS2.o_SELL_ST_DT = TO_DATE(TO_CHAR(SYSDATE),'DD/MM/YYYY') | *none* (SYSDATE; demo_source5.SELL_ST_DT is read but unused) |
| SELL_ED_DT | exp_TRANS2.o_SELL_ED_DT = TO_DATE(SELL_ED_DT,'DD/MM/YYYY') | demo_source5.SELL_ED_DT |

## 3. Baseline (`tools/informatica_baseline.py::mapping1`) vs literal XML

The baseline matches the XML on every structural point: join type and key, positional
SYSTIMESTAMP -> CR8_DT, discarded STRCMP, lookup tables/conditions/return ports, router
predicates (including NULL ACCT_TYP falling to the unconnected DEFAULT group), group-by
ACCT_ID with SUM(TX_AMT), SEQ_GEN starting at 281, RTRIM/LTRIM placement, and day-first
parsing of SELL_ED_DT. Divergences / interpretation choices (documented, not changed —
parity is measured against the baseline):

| # | Area | Literal XML reading | Baseline behaviour | Visible in seeds? |
|---|---|---|---|---|
| D1 | agg_TRANS pass-through ports | value from the last row *received* per ACCT_ID; within-account order is unspecified (SQ only orders by ACCT_ID) | deterministic: row with **highest TX_ID** per ACCT_ID (`ROW_NUMBER() OVER (PARTITION BY ACCT_ID ORDER BY TX_ID DESC) = 1`) | Yes — 1001 -> TX_ID 5002 / TX_DTTM 2024-01-15 11:00 |
| D2 | Lookup "Use Last Value" | last row in lookup cache order (engine-defined) | last **physical seed row** per key | Yes — DEMO_TARGET6 1002 TX_TYPE_CD = `DR` |
| D3 | SEQ_GEN | NEXTVAL per agg output row in arrival order | `280 + DENSE_RANK() OVER (ORDER BY ACCT_ID)` — equivalent only because agg output is one row per ACCT_ID in ACCT_ID order and the run is the first (Reset = NO) | Same values (281, 282) |
| D4 | SYSTIMESTAMP -> CR8_DT | full run timestamp incl. time of day | pinned to `2024-01-31 00:00:00` (written as `2024-01-31`) | Yes |
| D5 | Decimal scale 0 | SQ/exp/agg ports and target columns TX_AMT, BAL_AMT are decimal/number(38,0); with high precision on, or on Oracle insert, amounts would be rounded to integers | amounts kept as DOUBLE: TX_AMT 2031.2399999999998, BAL_AMT 86284.15 | Yes (parity tolerance 1e-6 absorbs the float artefact, not integer rounding) |
| D6 | DEMO_TARGET6.ACCT_DESC varchar2(10) | `Account 1001 ledger` (19 chars) exceeds target precision; Oracle writer would reject the row (ORA-12899) or truncate | full 19-char value kept | Yes |
| D7 | DEMO_TARGET3 numeric target columns | PRODUCT_ID, PRODUCT_NO, STD_COST, LIST_PRICE are `number(15)`; `PRD0001` / `P001` are non-numeric -> rows would be rejected on load | values kept as strings | Yes |
| D8 | o_SELL_ST_DT | TO_DATE parse error is a transformation error; with output-port default `' '` the row may be skipped/logged rather than nulled | NULL for every row, row kept | Yes (SELL_ST_DT empty) |
| D9 | STRCMP in Oracle override | not an Oracle function; override would fail | ignored | n/a |
| D10 | o_crdt_trim | LTRIM applied to CRDT_LN after implicit string->decimal(38,0) conversion (non-numeric CRDT_LN would become NULL/error) | LTRIM on the raw VARCHAR | No — seeds are numeric; same result (`'  8000'` -> `8000`) |
| D11 | DEMO_TARGET5 PK ACCT_ID | multiple non-SB transactions per account would produce duplicate PK rows (rejects) | no de-dup either; seeds have one tx per non-SB account | No |

D5-D9 are cases where the literal PowerCenter-on-Oracle run would likely error or reject
rows; the baseline (and therefore the dbt models) implements the "intended" logical
semantics. Worth recording in the conversion README as accepted deviations.

## 4. Model review findings

Reviewed `models/` at the head of `devin/1793881468-infa-m1` (commit `7a4d007`).

**No semantic defects found.** All three targets implement the XML/baseline semantics:
INNER JOIN + pinned CR8_DT + dropped STRCMP (`staging/sq_demo_source4.sql`), Use Last Value
by highest `SEED_ROW` (`macros/lookup_last_value.sql`, same convention as the baseline),
lookup tables/keys/return ports correct (lkp_trans1 -> LKP_DEMO_SOURCE3.TX_TYPE_CD by
ACCT_ID, lkp_trans2 -> LKP_DEMO_SOURCE1.FIRST_NM by ACCT_ID, lkp_trans3 ->
LKP_DEMO_SOURCE2.CRDT_SCORE by CUST_ID), router predicates that drop NULL ACCT_TYP
(verified: 1005 is NULL in `infa_src_infa_m1.DEMO_SOURCE4` and absent from both targets),
SUM + highest-TX_ID pass-through + `280 + row_number()` ACCT_KEY, day-first SELL_ED_DT.

Non-blocking suggestions (robustness / documentation; none changes current output):

| # | File:line | Observation | Suggestion |
|---|---|---|---|
| S1 | `models/targets/DEMO_TARGET6.sql:16` | agg "last row" tie-break is `TX_ID desc`; equal or NULL TX_IDs within an account would make it non-deterministic | `order by TX_ID desc nulls last, TX_DTTM desc` (still matches the baseline on current seeds), and reference divergence D1 in the comment |
| S2 | `models/targets/DEMO_TARGET6.sql:29` | `280 + row_number()` is correct only because the CTE already has one row per ACCT_ID; baseline uses `DENSE_RANK` over the pre-filter rows | fine as is; optionally move `280` to a var (`seq_gen_current_value: 281`) and use `{{ var(...) }} - 1 + row_number()` so the SEQ_GEN Current Value is visible in `dbt_project.yml` |
| S3 | `models/targets/DEMO_TARGET5.sql:10`, `DEMO_TARGET6.sql:9` | NULL-ACCT_TYP drop relies on SQL three-valued logic of `!=`; a future refactor to `is distinct from` / `coalesce` would silently route 1005 to target5 | add a singular test, e.g. `tests/assert_null_acct_typ_dropped.sql`: `select ACCT_ID from {{ ref('DEMO_TARGET5') }} where ACCT_ID = 1005 union all select ACCT_ID from {{ ref('DEMO_TARGET6') }} where ACCT_ID = 1005` (project already declares `test-paths: ["tests"]`) |
| S4 | `models/targets/schema.yml:50` | the only observable lookup tie (lkp_TRANS1, ACCT_ID 1002 -> `DR`, first value would be `TR`) is not tested | add a singular test asserting `TX_TYPE_CD = 'DR'` for ACCT_ID 1002 so a change to the tie convention is caught by `dbt build`, not only by parity |
| S5 | `models/intermediate/exp_trans1.sql:18` | `ltrim(CRDT_LN)` on VARCHAR; XML converts CRDT_LN to decimal(38,0) first (D10) | equivalent on seeds; optionally note D10 in the comment. Do not cast — the baseline emits the string |
| S6 | `models/targets/DEMO_TARGET3.sql:14` | `strptime` raises on a malformed SELL_ED_DT and fails the whole model; the baseline's `CAST` also raises, so parity-consistent | keep; mention in README that a malformed date fails the build (PowerCenter would reject only the row) |
| S7 | `models/targets/DEMO_TARGET5.sql:11`, `DEMO_TARGET3.sql:16`, `DEMO_TARGET6.sql:35` | `order by` in table models has no semantic effect | harmless; may drop |
| S8 | `README.md` "Semantics follow..." paragraph | lists 1005, agg, SEQ_GEN, SELL_ST_DT, TX_AMT scale | also record D6 (ACCT_DESC exceeds varchar2(10)) and D7 (non-numeric values in number(15) DEMO_TARGET3 columns) as accepted deviations |

`unique` test on DEMO_TARGET5.ACCT_ID (`schema.yml:21`) matches the target PK; it would
fail — correctly flagging D11 — if a non-SB account ever had more than one transaction.

## 5. Parity result

Built per `README.md` (dbt-core 1.9 / dbt-duckdb 1.9, DuckDB only):

```
dbt run-operation load_infa_inputs   # 6 inputs loaded (6/5/4/6/6/6 rows)
dbt build                            # PASS=18 WARN=0 ERROR=0 SKIP=0 TOTAL=18
python3 tools/parity_nfr.py --token X --duckdb $INFA_DUCKDB_PATH --schema main --report reports/infa_m1_review.md
```

| Object | Status | Baseline rows | Actual rows | Matched rows |
|---|---|---:|---:|---:|
| DEMO_TARGET3 | GREEN | 4 | 4 | 4 |
| DEMO_TARGET5 | GREEN | 2 | 2 | 2 |
| DEMO_TARGET6 | GREEN | 2 | 2 | 2 |
| DEMO_TARGET1_INS / _UPD, DEMO_TARGET2 / 21 | RED (Missing target — other mappings, expected) | | | |

`Full match: False` / exit 1 solely because of the absent m_demo_mapping2/3 targets.
