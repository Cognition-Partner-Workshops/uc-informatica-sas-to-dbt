# Informatica PowerCenter -> PySpark: shared design contract

Authoritative spec for the migration of `legacy/informatica/wf_demo_mapping.XML`
(`m_demo_mapping1`, `m_demo_mapping2`, `m_demo_mapping3`, workflow `wf_demo_mapping`)
to a single PySpark project. Every milestone must conform to this document.

`legacy/`, `tools/` and `baseline/` are read-only. `tools/parity_diff.py`,
`tools/keys/informatica_keys.json`, the 1e-6 tolerance and the exit-code contract
are never modified.

## 1. Layout

```
pyspark/informatica/
  requirements.txt
  informatica_pyspark/
    __init__.py
    config.py          RunConfig (business date, IO mode, paths, Snowflake options)
    session.py         build_spark()
    io.py              SourceReader / TargetWriter: LocalCsvIO, SnowflakeIO
    functions.py       Informatica-semantics helpers (see section 4)
    mappings/
      __init__.py
      m_demo_mapping1.py
      m_demo_mapping2.py
      m_demo_mapping3.py
    workflow.py        wf_demo_mapping runner
    cli.py             entry point
  tests/
docs/informatica_pyspark/
  DESIGN.md                     this file
  lineage.md / lineage.json     connector-derived field-level lineage
  conversion_comparison.md      conversion comparison table (+ .csv)
  decisions.md                  ambiguity / legacy-defect decisions
  parity.md                     local parity evidence
  snowflake_proof.md            warehouse-side proof
```

Nothing is generated into `docs/stm/` (that path belongs to `tools/informatica_lineage.py`).

## 2. Entry points

```
python -m informatica_pyspark.cli run-mapping m_demo_mapping1 --business-date 2024-01-31 --io local  --out-dir out/
python -m informatica_pyspark.cli run-workflow                --business-date 2024-01-31 --io local  --out-dir out/
python -m informatica_pyspark.cli run-workflow                --business-date 2024-01-31 --io snowflake --run-schema PYSPARK_INFORMATICA_<ts>
```

`--business-date` is **required**, has no default, and is the only source of "now".
No mapping, helper or test may call `current_date()`, `current_timestamp()`,
`datetime.now()` or read the wall clock. `SYSDATE` / `SYSTIMESTAMP` resolve to
`cfg.business_date` (`2024-01-31`, midnight for timestamp contexts).

Exit codes: `0` success; non-zero on any mapping failure, including `ABORT()`.

## 3. Mapping module contract

Each `mappings/m_demo_mappingN.py` exposes exactly:

```python
def run(spark: SparkSession, cfg: RunConfig, io: InformaticaIO) -> dict[str, DataFrame]:
    """Key = Informatica target *instance* name, value = DataFrame in target-definition column order."""
```

* Keys are instance names, not target-definition names:
  `demo_target1_INS`, `demo_target1_UPD` (m2); `demo_target6`, `demo_target5`, `demo_target3` (m1);
  `demo_target2`, `demo_target21` (m3).
* Column names and order come from the `TARGET` definition in the XML.
* `run()` never writes; the caller writes via `io.write_target(instance, df)`.
  This keeps local and Snowflake runs on identical transformation code.
* Mappings must not read anything not declared through `io`.

## 4. Informatica semantics helpers (`functions.py`)

All conversions of Informatica functions go through named helpers so the comparison
table can point at one file/line per construct.

| Informatica | Helper | Semantics |
|---|---|---|
| `RTRIM(x)` / `LTRIM(x)` | `inf_rtrim` / `inf_ltrim` | trailing/leading spaces only, NULL-in NULL-out |
| `ISNULL(x)` | `inf_isnull` | true only for SQL NULL (empty string in a CSV numeric/date port is NULL) |
| `IIF(c, a)` (2-arg) | `inf_iif` | else-branch is NULL, not false |
| `MD5(x)` | `inf_md5` | lowercase hex md5 of the UTF-8 concatenation |
| `\|\|` | `inf_concat` | Informatica treats NULL as empty string in `\|\|` |
| `TO_DATE(x, 'DD/MM/YYYY')` | `inf_to_date_ddmmyyyy` | strict; unparseable -> NULL (no exception) |
| `AES_DECRYPT(...)` | `inf_aes_decrypt_unrecoverable` | returns the constant `LEGACY_AES_VALUE` (see decisions.md) |
| `ABORT(msg)` | `inf_abort` | raises `InformaticaAbort`; run fails non-zero |
| `SYSDATE` / `SYSTIMESTAMP` | `cfg.business_date` | never wall clock |

`ABORT()` is a **run failure**, never a NULL fill. It is detected by evaluating the
guard predicate over the DataFrame and raising if any row matches, before any target
is written.

### Lookups

`lookup_use_last_value(lookup_df, keys, order_col)` and `lookup_use_any_value(...)`
are the only ways to resolve a `Lookup Procedure`. They collapse the lookup source to
one row per key **before** joining, so the join is a plain left join.

* `Use Last Value` = the **last physical row** of the lookup source, i.e. highest
  `__ROW_ORD` (section 5).
* `Use Any Value` = deterministic tie-break: highest value of the lookup's own key
  column (`Key` for `LKPTRANS` in m2). This is a judgment call, recorded in
  `decisions.md` and rated LOW in the comparison table.

### Unconnected lookups

`:LKP.lkp_TRANS1(ACCT_ID)` is called from an expression port. Implement as the same
`lookup_use_last_value` collapse plus a left join, returning the lookup's single
`Return Port`. The output port name may be misleading (`o_ACCT_ID` actually carries
`TX_TYPE_CD`) - follow the `CONNECTOR` graph, never the name.

## 5. Physical row order (`__ROW_ORD`)

`Use Last Value` and aggregator pass-through ports depend on physical row order, which
Spark does not preserve by default. Every source read therefore attaches an explicit
`__ROW_ORD` column:

* **Local CSV**: read the single file, `coalesce(1)`, then
  `monotonically_increasing_id()` - file order.
* **Snowflake**: the loader writes `__ROW_ORD` as a real column when it stages the CSVs,
  so both engines see the same order. Snowflake row order is otherwise undefined and
  must never be relied on.

`__ROW_ORD` is internal: it is dropped before a target DataFrame is returned from `run()`.

## 6. IO

```python
class InformaticaIO(Protocol):
    def read_source(self, name: str) -> DataFrame: ...   # demo_source1..5, lkp_demo_source1..3, demo_target1
    def write_target(self, instance: str, df: DataFrame) -> None:
```

* Schemas are declared explicitly in `io.py` (one `StructType` per source, from the XML
  `SOURCE`/`TARGET` field definitions). Never `inferSchema`.
* `LocalCsvIO` reads `legacy/informatica/data/` (override via `--data-dir`, used by the
  abort fixture: `--data-dir legacy/informatica/data/abort` falls back to the normal
  directory for files absent from the override dir) and writes
  `<out-dir>/<instance>.csv` as a single header CSV.
* `SnowflakeIO` reads `<src_schema>.<NAME>` and writes `<run_schema>.<INSTANCE>` via the
  `spark-snowflake` connector, key-pair auth from `SNOWFLAKE_PRIVATE_KEY`. The key is
  never logged, echoed or committed.

## 7. Workflow runner

From `WORKFLOWLINK` (XML lines 1465-1475) and the `Decision` tasks (1155-1163):

```
Start -> s_m_demo_mapping2 -> Decision1($s_m_demo_mapping2.Status = 1)
      -> s_m_demo_mapping1 -> Decision2($s_m_demo_mapping1.Status = 1)
      -> s_m_demo_mapping3 -> Decision3($s_m_demo_mapping3.Status = 1) -> SuccessEmail
```

Order is therefore **mapping2, mapping1, mapping3**. Each `Decision = 0` branch leads to a
`Failed_Email*` task, and `Failed_Email2 -> Control (Stop parent)`. Migrated as fail-fast:
a failed mapping stops the run immediately with a non-zero exit; downstream mappings do
not execute. Email tasks are logged, not sent (recorded as NOT MIGRATED).

## 8. Conversion comparison table

`docs/informatica_pyspark/conversion_comparison.md` plus a machine-readable
`conversion_comparison.csv` with identical rows. One row per:

* every `TRANSFORMFIELD` with a non-empty `EXPRESSION`
* every Source Qualifier SQL override / source filter
* every lookup condition and lookup policy
* every router `GROUP` condition
* every aggregator group-by port and aggregate port
* every sequence generator state

Columns, in order:

`mapping | transformation | port | informatica_code (verbatim) | xml_line | pyspark_code_or_ref | confidence | reason`

`xml_line` is a line number in `legacy/informatica/wf_demo_mapping.XML`.
`pyspark_code_or_ref` is either the converted expression or `path/to/file.py:LINE`.

Confidence rubric:

* **HIGH** - semantics unambiguous in the XML *and* at least one baseline row would
  fail parity if the conversion were wrong.
* **MEDIUM** - semantics unambiguous but weakly exercised: output is constant,
  degenerate, or the seed data would not catch an error. Reason required.
* **LOW** - conversion required a judgment call the XML does not determine. Reason
  required, and it must name the rejected alternative.
* **NOT MIGRATED** - deliberate omission (dead port, email task, unused lookup output).
  Reason required.

The document ends with: total expression count, migrated count, not-migrated-by-design
count, the confidence split, LOW rows grouped by the underlying decision, and a
prioritised "review these first" list.

## 9. Parity

`tools/parity_diff.py` is invoked unmodified:

```
python tools/parity_diff.py --baseline baseline/informatica --actual out \
  --keys tools/keys/informatica_keys.json --report docs/informatica_pyspark/parity_report.txt
```

Parity is only claimed on exit code 0. Never adjust keys, tolerance, comparator
behaviour, or the baseline to reach green.

The abort fixture must exit non-zero:

```
python -m informatica_pyspark.cli run-mapping m_demo_mapping3 --business-date 2024-01-31 \
  --io local --data-dir legacy/informatica/data/abort --out-dir out_abort/
```

## 10. Recorded legacy behaviour (reproduce, do not fix)

Detail and evidence live in `decisions.md`; summarised here so no milestone "fixes" them.

1. **m1 SQ override** selects `SYSTIMESTAMP` in position 5, which binds positionally to
   the `CR8_DT` port - `demo_target6.CR8_DT` is the run date, *not* `demo_source4.CR8_DT`.
2. **m1 `STRCMP(...)`** is the 14th select item and is connected to nothing: dead, NOT MIGRATED.
3. **m1 `o_SELL_ST_DT`** = `TO_DATE(TO_CHAR(SYSDATE),'DD/MM/YYYY')` is unparseable and
   yields NULL for every row.
4. **m1 lookups are name traps**: `demo_target5.FIRST_NM` comes from `lkp_demo_source1`
   (not `demo_source3.FIRST_NM`) and `demo_target5.CRDT_SCORE` comes from `lkp_demo_source2`
   (not `demo_source3.CRDT_SCORE`). Both differ in the seed data.
5. **m1 `o_ACCT_ID`** (unconnected lookup on `lkp_demo_source3`) carries `TX_TYPE_CD` into
   `demo_target6.TX_TYPE_CD` despite its name.
6. **m1 router default group** is unconnected: rows with NULL `ACCT_TYP` are dropped.
7. **m2 compares an AES-decrypted value to an MD5 hash**, so every matched row is flagged
   `Update`. Reproduced, not fixed.
8. **m2 lookup on the pre-existing target** matches two rows for `REC00002`
   (`Key` 2 and 99) under `Use Any Value`.
9. **m3 `ABORT()`** is a hard run failure.
10. **m3 router group naming is a trap**: `NEWGROUP1` (`ISNULL(Social_Security_Number)`)
    emits the `*1`-suffixed ports and is connected to **`demo_target2`**; `NEWGROUP2`
    (`NOT ISNULL(...)`) emits the `*3` ports and is connected to **`demo_target21`**.
    The unconnected `DEFAULT1` group is the one that owns the `*2`-suffixed ports, so
    suffix- or name-matching sends the data to the wrong target. Follow the `CONNECTOR`
    graph (XML lines 1017-1044).
