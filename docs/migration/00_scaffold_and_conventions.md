# PySpark conversion of `wf_demo_mapping` — shared scaffold, conventions and recovered semantics

Authoritative design input for every milestone. Everything in "Recovered semantics" below was read
directly out of `legacy/informatica/wf_demo_mapping.XML` (line numbers are that file) and is settled —
do not re-derive it, and do not "fix" it. Where a statement is labelled **DECISION**, the XML does not
determine the behaviour and the stated choice is binding.

## 1. Project layout (fixed)

```
pyspark/informatica/
  README.md                       # how to run local + Snowflake
  requirements-local.txt          # pyspark==3.5.*, pandas<3 (comparator), pyyaml
  conf/local.yml                  # io: csv  (paths under repo)
  conf/snowflake.yml              # io: snowflake (account/user/role/wh/db, schema suffix from env)
  parity/keys.json                # target -> key columns (input to the UNMODIFIED tools/parity_diff.py)
  informatica_pyspark/
    __init__.py
    config.py       # RunConfig / RunContext
    session.py      # build_spark(cfg) -> SparkSession
    io.py           # IO abstraction: CsvIO, SnowflakeIO
    schemas.py      # explicit StructType per source / lookup / pre-existing target, from the XML
    infa.py         # Informatica expression-function semantics (see §4)
    mappings/__init__.py        # REGISTRY: name -> module
    mappings/m_demo_mapping1.py
    mappings/m_demo_mapping2.py
    mappings/m_demo_mapping3.py
    workflow.py     # wf_demo_mapping runner (§5)
    cli.py          # `python -m informatica_pyspark.cli mapping --name ... | workflow` + --config
  tests/                          # pytest for infa.py semantics (optional but encouraged)
```

One project, one entry point per mapping, one workflow runner. No per-mapping scripts, no duplicated
IO or session code, no dbt reuse of any kind.

## 2. Mapping module contract (fixed)

Every `mappings/m_demo_mappingN.py` exposes exactly:

```python
TARGETS: list[str]                      # target *instance* names it writes
def run(ctx: RunContext) -> dict[str, DataFrame]   # instance name -> DataFrame
```

* Returned DataFrames have **exactly the target's `TARGETFIELD` columns, in `FIELDNUMBER` order**,
  with the target's names/case. Unconnected target columns are present and NULL-filled.
* `run()` never writes and never calls `spark.stop()`; the caller writes via `ctx.io`.
* A mapping that must fail the run raises `InformaticaAbort` (defined in `infa.py`); it must raise
  **before any of its targets are written**, matching the legacy session failing wholesale.
* All wall-clock functions read `ctx.cfg.business_date` (`date(2024,1,31)`). `current_date()` /
  `current_timestamp()` must not appear anywhere in the project.

## 3. IO abstraction (fixed)

`ctx.io.read(name) -> DataFrame` for the seven inputs (`demo_source1..5`, `lkp_demo_source1..3`,
`demo_target1` pre-existing state), `ctx.io.write(instance, df)` for the seven target instances.

* Schemas come from `schemas.py` (explicit `StructType`, never `inferSchema`).
* **Line ordinal.** `read()` attaches `__line_ordinal` (0-based physical order of the input) to
  `lkp_demo_source1`, `lkp_demo_source2`, `lkp_demo_source3` and the pre-existing `demo_target1`;
  the lookups' `Use Last Value` / `Use Any Value` policies are resolved with it (§4). Mapping code
  must drop `__line_ordinal` before returning.
* `CsvIO.write` produces exactly one file `<out_dir>/<INSTANCE>.csv` (`coalesce(1)`, header,
  then rename the part file). Value formatting must match `tools/informatica_baseline.py`'s
  `save()`: timestamps `yyyy-MM-dd HH:mm:ss` with a trailing ` 00:00:00` collapsed to `yyyy-MM-dd`,
  dates `yyyy-MM-dd`, NULL as empty field. Formatting is centralised in `io.py` — not per mapping.
* `SnowflakeIO` reads/writes the same logical names against the run schemas; the transformation code
  in `mappings/` is byte-identical between the two modes. Everything Snowflake-specific lives in
  `io.py` / `conf/snowflake.yml`.

## 4. Informatica semantics helpers (`infa.py`)

Implement these once, use everywhere:

* `iif(cond, a, b=None)` — NULL when no else-branch (Informatica returns NULL, not error).
* `isnull(col)` / `not_isnull(col)`.
* `rtrim(col)`, `ltrim(col)` — trailing/leading blanks only.
* `infa_to_date(col, fmt)` — `TO_DATE` with an explicit Informatica format mask; returns NULL when
  the value does not match the mask (`to_date` in Spark with `spark.sql.ansi.enabled=false` and a
  corrective `try_to_date`-style wrapper). Used for `'DD/MM/YYYY'`.
* `md5_concat(*cols)` — `MD5(a || b || ...)`; Informatica `||` propagates NULL like Spark `concat`.
* `AES_DECRYPT` — **not recoverable**; see DEF-2 / DECISION-2.
* `lookup(df_lookup, keys, policy, ordinal_col)` — returns one row per key according to
  `Use Last Value` (highest `__line_ordinal`) or `Use Any Value` (see DECISION-3), so the lookup
  policy is expressed once rather than inlined per mapping.
* `sequence_nextval(df, order_cols, current_value)` — Informatica Sequence Generator: the Nth row to
  arrive gets `current_value + N - 1`.
* `InformaticaAbort(Exception)` and `abort_if(df, condition, message)` — raises when any row
  satisfies the condition, reproducing `ABORT()` as a run failure.

## 5. Workflow runner (`workflow.py`)

Reproduce `wf_demo_mapping` (XML L1465–1475) exactly, including its defect:

```
Start ─▶ s_m_demo_mapping2 ─▶ Decision1 ($s_m_demo_mapping2.Status = 1)
                                 ├── condition ""  ─▶ s_m_demo_mapping1     # UNCONDITIONAL (DEF-5)
                                 └── Condition = 0 ─▶ Failed_Email1
s_m_demo_mapping1 ─▶ Decision2 ($s_m_demo_mapping1.Status = 1)
                                 ├── Condition = 1 ─▶ s_m_demo_mapping3
                                 └── Condition = 0 ─▶ Failed_Email2 ─▶ Control (Stop parent)
s_m_demo_mapping3 ─▶ Decision3 ($s_m_demo_mapping3.Status = 1)
                                 ├── Condition = 1 ─▶ SuccessEmail
                                 └── Condition = 0 ─▶ Failed_Email3
```

* Session order is therefore **mapping2, mapping1, mapping3**.
* Decisions are evaluated from real session status; Email tasks are logged, not sent.
* The runner exits non-zero if any session failed (so the `ABORT()` fixture fails the run) and zero
  only when all three succeeded. `Control = Stop parent` stops the workflow after `Failed_Email2`.
* mapping1 runs even when mapping2 failed, because that link's `CONDITION` is empty — keep it and
  record it as DEF-5; do not add a guard.

## 6. Recovered semantics — `m_demo_mapping1` (demo_target3, demo_target5, demo_target6)

* `sq_demo_source4` **SQL override** (L580) binds **positionally** to the SQ's port list
  (ports in order: ACCT_ID, ACCT_TYP, ACCT_DESC, CRDT_LN, CR8_DT, CLSR_DT, ACCT_STAT_CD, TX_ID,
  LAST_NM, TX_DTTM, TX_AMT, BAL_AMT, CUST_ID, TX_TYPE_CD; L566–579):
  - select item 5 is `SYSTIMESTAMP` → lands in port **CR8_DT**, so `demo_source4.CR8_DT` never
    reaches any target; CR8_DT is the pinned business date (**DEF-1**).
  - select item 14 is `STRCMP(demo_source4.ACCT_STAT_CD, demo_source3.TX_TYPE_CD)` → lands in port
    **TX_TYPE_CD**, which has **no outgoing CONNECTOR** → computed and discarded (**DEF-1b**,
    NOT MIGRATED).
  - `demo_source3 INNER JOIN demo_source4 ON ACCT_ID`, `ORDER BY demo_source4.ACCT_ID`,
    `Number Of Sorted Ports = 1`, `Output is deterministic = NO`, `Output is repeatable = Never`.
* Lookups (all `Use Last Value`, caching enabled):
  - `lkp_TRANS2` → `lkp_demo_source1` on `ACCT_ID = IN_ACCT_ID`; only **FIRST_NM** is connected
    onward (L832). `demo_target5.FIRST_NM` therefore comes from the *lookup*, **not** from
    `demo_source3.FIRST_NM` (which the SQL override does not even select). Name-matching lineage
    gets this wrong.
  - `lkp_TRANS3` → `lkp_demo_source2` on `CUST_ID = IN_CUST_ID`; only **CRDT_SCORE** connected
    (L833). Again: `demo_target5.CRDT_SCORE` is the lookup's value, not `demo_source3.CRDT_SCORE`.
  - `lkp_TRANS1` → `lkp_demo_source3` on `ACCT_ID = IN_ACCT_ID`, called **unconnected** as
    `:LKP.lkp_TRANS1(ACCT_ID)` in `exp_TRANS.o_ACCT_ID` (L608); its RETURN port is `TX_TYPE_CD`
    (L529). `o_ACCT_ID` flows exp_TRANS → exp_TRANS1 → rtr_TRANS → **`demo_target6.TX_TYPE_CD`**
    (L786). A port named `o_ACCT_ID` carrying a transaction-type code is lineage trap #2.
* `exp_TRANS`: `o_acc_trim = RTRIM(ACCT_TYP)` (L606), `o_crdt_trim = LTRIM(CRDT_LN)` (L607).
  `exp_TRANS1`: `o_ACCT_DESC = RTRIM(ACCT_DESC)` (L479).
* `rtr_TRANS` (L666): `demo_target6_GRP: ACCT_TYP = 'SB'`, `demo_target5_GRP: ACCT_TYP != 'SB'`,
  `DEFAULT1` **unconnected** → rows where `ACCT_TYP` is NULL satisfy neither condition and are
  silently dropped (**DEF-4**, reproduce; note the seed data does not exercise it).
* `agg_TRANS` (L442): group by **ACCT_ID** (`EXPRESSIONTYPE="GROUPBY"`, L452); `o_TX_AMT = SUM(TX_AMT)`
  (L454); every other port is a pass-through, i.e. Informatica returns the **last row of the group**.
  Input is sorted by ACCT_ID only, so "last row" within an account is undefined —
  **DECISION-1: last = row with the highest `TX_ID` in the account** (rejected alternative: physical
  arrival order of the join, which the XML declares non-repeatable).
* `SEQ_GEN` (L429): Start 1, Increment 1, **Current Value 281**, Cycle YES, End 2147483647.
  `NEXTVAL → demo_target6.ACCT_KEY`, one aggregated row per account →
  **DECISION-2: ACCT_KEY = 281 + (rank of ACCT_ID ascending) − 1**, i.e. groups consume NEXTVAL in
  ascending ACCT_ID order (rejected alternative: arrival order). `CURRVAL` unconnected → NOT MIGRATED.
* `exp_TRANS2` (L653): `o_SELL_ED_DT = TO_DATE(SELL_ED_DT,'DD/MM/YYYY')` (parses the seed's
  `dd/mm/yyyy` strings); `o_SELL_ST_DT = TO_DATE(TO_CHAR(SYSDATE),'DD/MM/YYYY')` — `TO_CHAR(SYSDATE)`
  yields the session default `MM/DD/YYYY HH24:MI:SS.US`, which can never match the `DD/MM/YYYY` mask,
  so **`demo_target3.SELL_ST_DT` is NULL for every row** (**DEF-3**; the source's real `SELL_ST_DT`
  is read, passed into the SQ and then never used). Reproduce as an all-NULL date column.

## 7. Recovered semantics — `m_demo_mapping2` (demo_target1_INS, demo_target1_UPD)

* `LKPTRANS` (L265) looks up **`demo_target1`** (the pre-existing target state) on `ID = ID1`,
  `Lookup policy on multiple match = Use Any Value` (L285), connection `$Target`. Only `Key` and the
  five value copies (`LEAD_CO_MNE1`, `BRANCH_CO_MNE1`, `MIS_DATE1`, `DESCRIPTION1`, `SHORT_NAME1`)
  are connected onward; `CREATED_BY … END_DATE` are dead (NOT MIGRATED).
  The seed has two rows for `ID = REC00002` (`Key` 2 and 99) so the tie-break is observable:
  **DECISION-3: `Use Any Value` = highest `Key`, then highest `__line_ordinal`** (rejected
  alternative: first physical row, which would put `Key = 2` in `demo_target1_UPD`).
* `EXPTRANS` (L163): `New_Flag = IIF(ISNULL(Key),'Insert')` (L176);
  `MD5_src = AES_DECRYPT(LEAD_CO_MNE1, SUBSTR(SHORT_NAME,1,3), 256)` (L177, LOCAL VARIABLE);
  `MD5_tgt = MD5(LEAD_CO_MNE || BRANCH_CO_MNE || MIS_DATE || DESCRIPTION || SHORT_NAME)` (L178);
  `Changed_Flag = IIF(NOT ISNULL(Key) AND (MD5_tgt != MD5_src),'Update')` (L179);
  `o_CREATED_BY = o_UPDATED_BY = 'IDWUSER'`, `o_CREATED_TIME = o_UPDATED_TIME = SYSDATE`.
  **DEF-2 (impossible comparison):** the change test compares an AES-decryption of a 5-character
  plaintext lookup column against a 32-hex MD5 digest — incomparable value spaces, so every matched
  row is flagged `Update` unconditionally. **DECISION-4:** model `MD5_src` as an opaque sentinel that
  can never equal an MD5 digest (rejected alternative: implement real AES-256 decryption — the input
  is not ciphertext and the 3-character key is not a valid 256-bit key, so it would either error or
  return garbage, and either way the branch outcome is unchanged).
* `RTRTRANS` (L186) — read the `GROUP` attribute of each `TRANSFORMFIELD`, **not the port-name
  suffix**; the suffixes are deliberately misleading:
  - `Insert` group (`New_Flag='Insert'`) ports `*2/ID1/Key1/o_*1` → `demo_target1_INS`
    (L365–372) with `SEQTRANS.NEXTVAL → demo_target1_INS.Key` (L373).
  - `Update` group (`Changed_Flag='Update'`) ports `LEAD_CO_MNE4, BRANCH_CO_MNE4, MIS_DATE4, ID3,
    DESCRIPTION4, SHORT_NAME4, Key3, o_UPDATED_*3` → `UPDTRANS` (L411–423) → `demo_target1_UPD`.
    The *source* values (not the looked-up `*1` copies, which are dead) are what land in the target.
  - `DEFAULT1` group ports are named `LEAD_CO_MNE3, MIS_DATE3, DESCRIPTION3, SHORT_NAME3, ID2, Key2,
    o_UPDATED_*2` — **the same names as UPDTRANS's own ports** (L328–340), which is lineage trap #1:
    matching by name wires the discarded-row group to `demo_target1_UPD`. `DEFAULT1` is unconnected;
    rows that are neither Insert nor Update are silently discarded (**DEF-6**).
* `SEQTRANS` (L314): Start 0, Increment 1, **Current Value 57**, Cycle NO.
  **DECISION-5: `demo_target1_INS.Key = 57 + (0-based ordinal of the row in `demo_source1` physical
  file order, among Insert-group rows)`** (rejected alternative: unordered assignment — the flat file
  is read sequentially, so file order is the arrival order).
* `UPDTRANS` (L327): `Update Strategy Expression = DD_UPDATE`, `Forward Rejected Rows = YES`; the
  session's `Treat source rows as = Data driven` (L1434). For the parity artefact this means the UPD
  instance carries the rows to be updated — it is not an in-place mutation of the CSV baseline.
* Target column coverage: `demo_target1_INS` gets Key, LEAD_CO_MNE, BRANCH_CO_MNE, MIS_DATE, ID,
  DESCRIPTION, SHORT_NAME, CREATED_BY, CREATED_TIME; `demo_target1_UPD` gets Key, LEAD_CO_MNE,
  BRANCH_CO_MNE, MIS_DATE, ID, DESCRIPTION, SHORT_NAME, UPDATED_BY, UPDATED_TIME. Every other
  `demo_target1` column is NULL in both (unconnected).

## 8. Recovered semantics — `m_demo_mapping3` (demo_target2, demo_target21)

* `SQ_demo_source2` SQL override (L916) = full column list `FROM demo_source2 where
  demo_source2.Member_Type_Code is not null` — a filter expressed in the override, not a Filter
  transformation, and the select list is positionally aligned with the SQ ports here.
* `EXPTRANS.o_Relationship_to_Subscriber_Code_Label` (L943):
  `iif(ISNULL(Relationship_to_Subscriber_Code_Label), ABORT('Relationship_to_Subscriber_Code_Labe
  valuel is null'), Relationship_to_Subscriber_Code_Label)` — a **hard run failure** on any
  filtered-in row with a NULL label, not a NULL fill. Must fail the run before writing, and must
  match `tools/informatica_baseline.py --trigger-abort` (non-zero exit). Note the typo in the
  message; keep it verbatim.
* `RTRTRANS` (L946): `NEWGROUP1: ISNULL(Social_Security_Number)` → **`demo_target2`** (L1031–1044);
  `NEWGROUP2: NOT ISNULL(Social_Security_Number)` → **`demo_target21`** (L1017–1030); `DEFAULT1`
  unconnected (unreachable here, the two conditions are complementary). The group→target assignment
  is only visible in the CONNECTOR graph — `NEWGROUP1`/`NEWGROUP2` carry no hint.
* Port→column renames are real lineage, e.g. `Member_ID → Member_Identifier`,
  `Gender_Code → Gender`, `Social_Security_Number → Soc_Number`,
  `Member_Record_Number → Member_Number`, `Member_Type_Code → Type_Code`,
  `Original_Effective_Date → Effective_Date`, `Birth_Date → Date_of_Birth`.
* Both `demo_target2` and `demo_target21` are `INSTANCE` elements of the **one** `TARGET` definition
  `demo_target2` (L1009–1010); likewise `demo_target1_INS`/`demo_target1_UPD` over `demo_target1`
  (L345–346). **DECISION-6: each *instance* is materialised separately** (own CSV, own Snowflake
  table named after the instance), because the baseline and the parity control are per instance;
  the shared physical target definition is recorded in the lineage and comparison docs (rejected
  alternative: union the instances into one table, which would destroy the parity control and the
  INS/UPD distinction).

## 9. Comparison table (deliverable #3) — format and rubric

One row per transformation expression in the XML: every `TRANSFORMFIELD` with a non-empty
`EXPRESSION`, plus SQL overrides, lookup conditions and policies, router group conditions,
aggregator group-by/aggregate ports, and sequence-generator state.

Files: `docs/migration/conversion_table/m_demo_mapping1.md`, `…2.md`, `…3.md`, `…workflow.md`
(one per milestone, so children never edit the same file), assembled into
`docs/migration/conversion_comparison_table.md` with the headline counts.

Columns, in this order:

| Mapping | Transformation | Port / element | Informatica code (verbatim) | XML line | PySpark conversion (snippet or `file:lines`) | Confidence | Reason (required unless HIGH) |

Rubric (state it verbatim in the doc):

* **HIGH** — semantics are unambiguous in the XML **and** at least one baseline row would fail parity
  if the conversion were wrong.
* **MEDIUM** — unambiguous, but weakly exercised: the output is constant or degenerate in the seed
  data, so parity cannot catch a wrong conversion.
* **LOW** — the conversion rests on a judgement call the XML does not determine; the row must name
  the alternative that was rejected.
* **NOT MIGRATED** — deliberately not converted (e.g. a port with no outgoing CONNECTOR); every such
  element must be named.

Every non-HIGH row states, in one line, what a wrong conversion would look like and why the controls
would not catch it. LOW rows are grouped by the underlying decision (DECISION-1 … DECISION-6) so a
reviewer sees how few distinct judgement calls there are.

## 10. Parity (deliverable #4)

* `tools/parity_diff.py`, `tools/informatica_baseline.py`, `baseline/`, `legacy/` are **read-only**.
  The comparator runs unmodified, under `pandas<3` (pandas 3 mis-normalises the all-NULL DATE column
  in `demo_target3` and reports a false mismatch).
* Baseline: `python3 tools/informatica_baseline.py` (writes `baseline/informatica/*.csv`;
  `baseline/` is git-ignored, so every environment regenerates it).
* Actual: the PySpark CSV output directory. `tools/parity_diff.py --baseline baseline/informatica
  --actual <out_dir> --keys pyspark/informatica/parity/keys.json --report <report>` must exit 0 with
  all seven targets MATCH.
* Per-milestone runs may point `--baseline` at a scratch directory holding only that mapping's
  baseline CSVs; keys, tolerances and exit codes stay exactly as they are.
* `keys.json` keys must be **verified unique** in the baseline for their target (the comparator
  aligns rows by sorting on them; duplicate key values make the comparison order-dependent).
* Abort direction: `python3 tools/informatica_baseline.py --trigger-abort` exits non-zero, and the
  PySpark workflow run against `legacy/informatica/data/abort/demo_source2.csv` must also exit
  non-zero, with no target written for mapping3.
