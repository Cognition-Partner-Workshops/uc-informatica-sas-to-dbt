# Informatica PowerCenter → PySpark migration, with Snowflake proof

`legacy/informatica/wf_demo_mapping.XML` (three mappings, seven target instances) is reimplemented as
one PySpark project under `pyspark/informatica/`, proved row-for-row against the legacy baseline both
locally and in real Snowflake. Legacy behaviour is reproduced **including its defects**.

## 1. Milestones

| # | Milestone | Owned by | PR | Verification result |
|---|---|---|---|---|
| A | Shared scaffold (layout, session/config, IO abstraction, `infa.py` semantics, workflow runner), connector-graph field lineage, confidence rubric, parity keys | orchestrator | [#25](https://github.com/Cognition-Partner-Workshops/uc-informatica-sas-to-dbt/pull/25) | 5 unit tests pass; baseline regenerates (7 CSVs) and `--trigger-abort` exits 1; key uniqueness PASS 7/7; lineage self-assertions 6/6 PASS |
| B | `m_demo_mapping1` → `demo_target3`, `demo_target5`, `demo_target6` | [child session](https://partner-workshops.devinenterprise.com/sessions/93d6debf92ed4914a3baa557bb36613d) | [#32](https://github.com/Cognition-Partner-Workshops/uc-informatica-sas-to-dbt/pull/32) | parity exit 0, 3/3 MATCH; 84 table rows |
| C | `m_demo_mapping2` → `demo_target1_INS`, `demo_target1_UPD` | [child session](https://partner-workshops.devinenterprise.com/sessions/d0400cefa35f42c79f9efc08d6b42a6f) | [#30](https://github.com/Cognition-Partner-Workshops/uc-informatica-sas-to-dbt/pull/30) | parity exit 0, 2/2 MATCH; 38 table rows |
| D | `m_demo_mapping3` → `demo_target2`, `demo_target21`, plus the `ABORT()` direction and the per-input override that makes the abort fixture a config change | [child session](https://partner-workshops.devinenterprise.com/sessions/b26fd2570fe44ae2be90db0bf529bd68) | [#31](https://github.com/Cognition-Partner-Workshops/uc-informatica-sas-to-dbt/pull/31) | parity exit 0, 2/2 MATCH; mapping-level abort exits 1, no target written; 36 table rows |
| E+F | Snowflake execution through the same modules, integration, end-to-end local + warehouse proof, assembled comparison table | orchestrator | [#34](https://github.com/Cognition-Partner-Workshops/uc-informatica-sas-to-dbt/pull/34) | local workflow exit 0, unmodified comparator exit 0 with 7/7 MATCH; abort run exits 1 with no mapping3 target; Snowflake proof 7/7 PASS; 13 tests pass |

All milestone PRs landed in `integration/pyspark-informatica`. Nothing was merged into `main`; the
integration PR into `main` is left open.

## 2. Conversion comparison table

`docs/migration/conversion_comparison_table.md` (assembled from the frozen per-mapping tables in
`docs/migration/conversion_table/`, plus `workflow.md` for the workflow tasks/links).

| | Total | Migrated | Not migrated | HIGH | MEDIUM | LOW | NOT MIGRATED |
|---|---:|---:|---:|---:|---:|---:|---:|
| `m_demo_mapping1` | 84 | 74 | 10 | 51 | 12 | 11 | 10 |
| `m_demo_mapping2` | 38 | 32 | 6 | 20 | 8 | 4 | 6 |
| `m_demo_mapping3` | 36 | 20 | 16 | 18 | 1 | 1 | 16 |
| **Overall** | **158** | **126** | **32** | **89** | **21** | **16** | **32** |

Rubric: **HIGH** = unambiguous in the XML *and* a wrong conversion would fail parity on the seed;
**MEDIUM** = unambiguous but weakly exercised (constant or degenerate seed output, so parity cannot
catch it); **LOW** = rests on a judgement call the XML does not determine, with the rejected
alternative named; **NOT MIGRATED** = deliberate omission (each dead port named individually).

The 16 LOW rows collapse onto six distinct judgement calls (§6); the 32 NOT MIGRATED rows are dead
ports taken from the lineage extractor's no-outgoing-connector list.

## 3. Snowflake proof

Account `YD76133.us-east-2.aws`, user `devin_demo`, role `devin_migration_demo`, warehouse
`devin_demo_wh`, database `devin_migration_demo`, key-pair auth (private key from the
`SNOWFLAKE_PRIVATE_KEY` secret; never written into the repo or any log). Run id `20260807T0658Z`.
`information_schema.schemata` was checked first and returned only `BASELINE_INFORMATICA`,
`DBT_INFORMATICA`, `INFORMATION_SCHEMA` — neither pre-existing schema was touched. Created and left
standing: `SOURCE_INFORMATICA_20260807T0658Z`, `PYSPARK_INFORMATICA_20260807T0658Z`,
`BASELINE_INFORMATICA_20260807T0658Z`.

Sources (9 tables, typed DDL generated from `schemas.py`) were loaded into the source schema; the
**same** mapping modules then ran through `SnowflakeIO` and wrote the seven target instances into the
migrated schema (`SNOWFLAKE_WORKFLOW_EXIT:0`). The baseline CSVs were loaded into the baseline schema
with identical DDL, and both sides are compared through generated `V_<TARGET>` views sharing one
normalised projection. Full SQL: `docs/migration/snowflake_proof_20260807T0658Z.sql`; provisioning and
query-history record: `docs/migration/snowflake_milestone_e.md`.

### One statement, one row per target — counts, checksums, verdict

```sql
with chk as (
  select 'DEMO_TARGET1_INS' as target,
         (select count(*)    from BASELINE_INFORMATICA_20260807T0658Z.V_DEMO_TARGET1_INS) as baseline_rows,
         (select count(*)    from PYSPARK_INFORMATICA_20260807T0658Z.V_DEMO_TARGET1_INS)  as migrated_rows,
         (select hash_agg(*) from BASELINE_INFORMATICA_20260807T0658Z.V_DEMO_TARGET1_INS) as baseline_hash,
         (select hash_agg(*) from PYSPARK_INFORMATICA_20260807T0658Z.V_DEMO_TARGET1_INS)  as migrated_hash,
         (select count(*) from (select * from BASELINE_INFORMATICA_20260807T0658Z.V_DEMO_TARGET1_INS
                                minus select * from PYSPARK_INFORMATICA_20260807T0658Z.V_DEMO_TARGET1_INS)) as baseline_minus_migrated,
         (select count(*) from (select * from PYSPARK_INFORMATICA_20260807T0658Z.V_DEMO_TARGET1_INS
                                minus select * from BASELINE_INFORMATICA_20260807T0658Z.V_DEMO_TARGET1_INS)) as migrated_minus_baseline
  union all /* ... six further branches, one per target ... */
)
select target, baseline_rows, migrated_rows, baseline_hash, migrated_hash,
       baseline_minus_migrated, migrated_minus_baseline,
       case when baseline_rows = migrated_rows and baseline_hash = migrated_hash
                 and baseline_minus_migrated = 0 and migrated_minus_baseline = 0
            then 'PASS' else 'FAIL' end as verdict
from chk order by target;
```

Actual output:

```text
TARGET            BASE  MIGR  BASELINE_HASH         MIGRATED_HASH         B-M  M-B  VERDICT
DEMO_TARGET1_INS     4     4   8128491501339877599   8128491501339877599    0    0  PASS
DEMO_TARGET1_UPD     3     3  -5257889502721467851  -5257889502721467851    0    0  PASS
DEMO_TARGET2         3     3   3123907108787439864   3123907108787439864    0    0  PASS
DEMO_TARGET21        3     3  -5462086455473858760  -5462086455473858760    0    0  PASS
DEMO_TARGET3         4     4   2979066879702683896   2979066879702683896    0    0  PASS
DEMO_TARGET5         2     2  -4578390602032457200  -4578390602032457200    0    0  PASS
DEMO_TARGET6         2     2   -987830873279475629   -987830873279475629    0    0  PASS
```

### Query-history evidence

```sql
select query_id, query_text, start_time, end_time, rows_produced,
       warehouse_name, execution_status
from table(devin_migration_demo.information_schema.query_history(
  end_time_range_start => dateadd('hour', -3, current_timestamp()),
  result_limit => 200))
where warehouse_name = current_warehouse()
order by start_time desc;
```

```text
01c639bd-0107-4ec9-000f-dc5e0003a4ce ... proof statement                                    7  DEVIN_DEMO_WH  SUCCESS
01c639bc-0107-4ec9-000f-dc5e0003a49a ... CREATE OR REPLACE VIEW PYSPARK...V_DEMO_TARGET5     0  DEVIN_DEMO_WH  SUCCESS
01c639bc-0107-544d-000f-dc5e00034936 ... CREATE OR REPLACE VIEW BASELINE...V_DEMO_TARGET5    0  DEVIN_DEMO_WH  SUCCESS
01c639a2-0107-4ec9-000f-dc5e0003a2b6 ... CREATE SCHEMA "SOURCE_INFORMATICA_20260807T0658Z"   0  DEVIN_DEMO_WH  SUCCESS
01c639a2-0107-58c8-000f-dc5e000430c6 ... INSERT INTO ... DEMO_TARGET1                        5  DEVIN_DEMO_WH  SUCCESS
```

### Local proof (the same code, CSV IO)

```text
WORKFLOW_EXIT:0                     # mapping2 → mapping1 → mapping3
7/7 MATCH → Overall: PARITY VERIFIED  (tools/parity_diff.py, unmodified, pandas 2.3.3)
PARITY_EXIT:0
ABORT_WORKFLOW_EXIT:1               # demo_source2 overridden to legacy/informatica/data/abort/
NO_MAPPING3_TARGETS                 # deleted beforehand, not recreated
```

Legacy control for the same direction: `python3 tools/informatica_baseline.py --trigger-abort` exits 1.
Report committed at `docs/parity/informatica_end_to_end.md`.

## 4. Divergences caught by verification

| # | Caught by | Divergence | Resolution |
|---|---|---|---|
| 1 | Orchestrator review of the scaffold | CSV writer formatted **dates** as `yyyy-MM-dd HH:mm:ss` and did not collapse midnight timestamps, unlike the baseline's `save()`. Every `CREATED_TIME`/`UPDATED_TIME` row would have failed parity | formatting centralised in `io.py` and pinned by a byte-level test |
| 2 | Orchestrator review of the scaffold | `__line_ordinal` was derived from `monotonically_increasing_id()` over a possibly multi-partition read, so `Use Last Value` / `Use Any Value` were not reliably resolving to the last physical line | single partition + ordered `row_number()`, with a duplicate-key test |
| 3 | Orchestrator review of the scaffold | `infa_to_date` returning NULL on a mask mismatch was assumed, not verified — DEF-3 depends entirely on it | verified empirically under `ansi.enabled=false` / `timeParserPolicy=CORRECTED`, both directions tested; local output path also moved out of the read-only `baseline/` tree |
| 4 | Milestone B child, against the XML | `schemas.py` typed `demo_target3.SELL_ST_DT`/`SELL_ED_DT` as string where `TARGETFIELD` (XML L124–125) says `date`; `demo_target5` numerics likewise | schema corrected to the XML; Snowflake DDL became `DATE`/`NUMBER` |
| 5 | Milestone C child, reasoning about Snowflake | `demo_source1` had no line ordinal from `read()`, so DECISION-5's "physical file order" had no meaning in Snowflake, where row order does not exist — local parity would have stayed green while the warehouse silently used an arbitrary order | `read()` in both IO modes now owns the ordinal for a declared input set including `demo_source1`; Snowflake materialises it as a stored `__LINE_ORDINAL` column, verified against CSV line order for all five inputs |
| 6 | The Snowflake proof itself | first end-to-end run FAILed on `DEMO_TARGET5`: the standing normalised views predated divergence #4, so numerics were compared as raw text | views regenerated from the corrected schemas; proof logic and normalisation untouched |

Divergence 6 is the useful one: it is the control failing on a real difference rather than being
adjusted until it passed. The proof was also run once against empty migrated tables as a deliberate
negative control (7/7 FAIL with `migrated_rows = 0`) to show the verdict can fail.

## 5. Legacy defects reproduced

| ID | Defect | XML evidence | Reproduced as |
|---|---|---|---|
| DEF-1 | The Source Qualifier SQL override binds **positionally** to the port list. Select item 5 is `SYSTIMESTAMP`, so it lands in port `CR8_DT` and `demo_source4.CR8_DT` never reaches a target | override L580; positional SQ port list L566–579 | `CR8_DT` is the pinned business date in `demo_target6`; the source column is unused |
| DEF-1b | Select item 14, `STRCMP(demo_source4.ACCT_STAT_CD, demo_source3.TX_TYPE_CD)`, binds to port `TX_TYPE_CD`, which has **no outgoing connector** — computed and discarded | L580; no `CONNECTOR` from `sq_demo_source4.TX_TYPE_CD` | NOT MIGRATED, named in the table |
| DEF-2 | Impossible comparison: `MD5_src = AES_DECRYPT(LEAD_CO_MNE1, SUBSTR(SHORT_NAME,1,3), 256)` is compared against a 32-hex `MD5(...)` digest, so every matched row is flagged `Update` unconditionally | `MD5_src` L177, `MD5_tgt`/`Changed_Flag` L178–180 | modelled as an opaque sentinel that can never equal an MD5 digest (DECISION-4); all matched rows land in `demo_target1_UPD` |
| DEF-3 | `o_SELL_ST_DT = TO_DATE(TO_CHAR(SYSDATE),'DD/MM/YYYY')` — `TO_CHAR(SYSDATE)` yields the session default `MM/DD/YYYY HH24:MI:SS.US`, which can never match the mask, so `demo_target3.SELL_ST_DT` is NULL for every row while the source's real `SELL_ST_DT` is read and discarded | L662; session `DateTime Format String` L1103 | the conversion formats the business date the same way and parses it with the same mask, yielding an all-NULL date column — the defect is reproduced by mechanism, not hard-coded |
| DEF-4 | `rtr_TRANS.DEFAULT1` is unconnected, so rows with NULL `ACCT_TYP` satisfy neither `= 'SB'` nor `!= 'SB'` and are silently dropped | groups L667–670 | both branches use the literal conditions; NULL rows fall through. Not exercised by the seed → rated MEDIUM, not HIGH |
| DEF-5 | The workflow link `Decision1 → s_m_demo_mapping1` has an **empty** `CONDITION`, so mapping1 runs even when mapping2 failed; only mapping3 is actually gated | L1470 vs L1469 | `workflow.py` keeps the unconditional link and logs each XML task/decision by name |
| DEF-6 | `RTRTRANS.DEFAULT1` in mapping2 is unconnected — rows that are neither Insert nor Update are discarded. Its ports are **named identically** to `UPDTRANS`'s, so name-based lineage wires the discarded group to `demo_target1_UPD` | group L189; its ports L245–253 | router resolved by `GROUP` attribute; discard path preserved. Unreachable on this data because DEF-2 forces every matched row to `Update` → LOW/MEDIUM, never HIGH |

Two further traps in the lineage, not defects but wrong under name matching: `demo_target5.FIRST_NM` /
`CRDT_SCORE` come from lookups (`lkp_demo_source1` / `lkp_demo_source2`), not from the same-named
`demo_source3` columns — which the override does not even select; and `demo_target6.TX_TYPE_CD` arrives
through a port called `o_ACCT_ID`, fed by the unconnected `:LKP.lkp_TRANS1(ACCT_ID)` whose RETURN port
is `lkp_demo_source3.TX_TYPE_CD`. The extractor asserts all of these against the graph it builds.

## 6. Decisions where the XML leaves the behaviour undefined

| ID | Decision | Rejected alternative and why |
|---|---|---|
| DECISION-1 | Aggregator pass-through ports take the group's **highest `TX_ID`** row. Informatica returns the group's "last row", but the only ordering the XML gives is the override's `ORDER BY demo_source4.ACCT_ID` (L580, SQ `Number Of Sorted Ports = 1` at L583); `agg_TRANS` itself declares `Number Of Sorted Ports = 0` (L749) | physical arrival order of the join — the XML declares `Output is deterministic = NO` on that pipeline (L589, L755), so arrival order is not a contract the XML defines |
| DECISION-2 | `SEQ_GEN` (Current Value 281, L435) values are consumed by aggregated groups in **ascending `ACCT_ID`** order | arrival order — same non-repeatability argument; would produce plausible but unstable `ACCT_KEY`s |
| DECISION-3 | `Use Any Value` on the `demo_target1` lookup resolves to the **highest `Key`**, then highest line ordinal. Observable: the seed has two rows for `ID = REC00002`, `Key` 2 ("old key") and `Key` 99 ("new key") | first physical row, which would put `Key = 2` in `demo_target1_UPD`. Informatica does not define which value "any" is; the choice is recorded rather than hidden |
| DECISION-4 | `AES_DECRYPT` is unrecoverable and modelled as an opaque sentinel (see DEF-2) | implementing real AES-256: the first argument is a 5-character plaintext, not ciphertext, and a 3-character key is not a valid 256-bit key, so it would error or return garbage — and the branch outcome would be unchanged either way |
| DECISION-5 | `demo_target1_INS.Key` = 57 (`Current Value`, L320) + the 0-based ordinal of the row in `demo_source1`'s **physical file order**, among Insert-group rows | unordered assignment; the flat file is read sequentially, so file order *is* the arrival order. This is why the ordinal had to become a stored column in Snowflake (divergence #5) |
| DECISION-6 | Each **writer instance** is materialised separately (`demo_target1_INS`/`_UPD` over one physical `demo_target1`; `demo_target2`/`demo_target21` over one physical `demo_target2`) | unioning the instances into one table per physical target, which would destroy the per-instance parity control and the INS/UPD distinction |

Also recorded but not a judgement call: `lkp_TRANS2` and `lkp_TRANS3`'s `Use Last Value` policies are
**not verifiable on this seed** — their only duplicated keys belong to an SB account, which routes to
`demo_target6`, and `demo_target6` consumes neither of those lookup columns, so `Use First Value` would
produce a byte-identical `demo_target5`. They are rated MEDIUM. Closing that gap needs a non-SB account
with a duplicated lookup key in the seed.
