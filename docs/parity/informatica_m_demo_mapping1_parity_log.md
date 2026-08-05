# m_demo_mapping1 parity failure log

## Failure 1 — `demo_target3.SELL_ST_DT`

- **Parity output under pandas 3.0.5:** `column SELL_ST_DT: 4/4 rows differ (first at {'PRODUCT_ID': 'PRD0001'}: baseline=np.float64(nan) actual=nan)`
- **Baseline value:** `np.float64(nan)` for every row (the baseline CSV has an empty field).
- **Actual value:** `nan` for every row.
- **XML fact:** `o_SELL_ST_DT = TO_DATE(TO_CHAR(SYSDATE),'DD/MM/YYYY')`; the pinned `31JAN2024` renders with month/day ordering, so parsing it as `DD/MM/YYYY` makes day `31` an invalid month and Informatica returns NULL.
- **Root cause:** This was not a model or XML mismatch. The parity harness was written against pandas 2. With pandas 3.0.5, `compare()` calls `bs.fillna("\0").astype(str)`; pandas 3 no longer silently upcasts the baseline float64 all-NaN column, while the actual object/string column fills to `"\x00"`, causing two NULLs to compare unequal.
- **Resolution:** Pinned the harness environment to `pandas==2.3.3` (`pandas<3`), restored the model expression to `cast(null as date)`, regenerated the baseline, and reran parity successfully. The recorded parity run uses pandas `2.3.3`.

## Deliberately induced counterfactuals

Each entry below is a deliberate one-at-a-time wrong implementation, not an accidental
failure. For each experiment, the wrong model was built and the exact required parity
command was run, then the model was restored before the next experiment. The wrong
models were materialized with `dbt build --exclude resource_type:unit_test` so that the
correct-expectation unit tests would not block downstream marts; parity itself used the
same unmodified command as the final run.

### Counterfactual 2a — `demo_target6.CR8_DT` from `demo_source4.CR8_DT`

- **Change:** Replaced the SQL override's pinned timestamp expression with `s4.CR8_DT`.
- **Verbatim parity output:**

```text
## DEMO_TARGET3
- rows: baseline=4 actual=4
- columns compared: 8
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET5
- rows: baseline=2 actual=2
- columns compared: 5
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET6
- rows: baseline=2 actual=2
- columns compared: 12
- **MISMATCH**:
  - column CR8_DT: 2/2 rows differ (first at {'ACCT_ID': np.int64(1001)}: baseline='2024-01-31' actual='2023-08-18')
```

- **XML fact:** The SQL override's fifth select expression is `SYSTIMESTAMP`, and
  positional SQ binding assigns that expression to `CR8_DT`; `demo_source4.CR8_DT`
  is discarded.
- **Resolution:** Restored the pinned business-date timestamp expression. Final parity
  passed.

### Counterfactual 2b — `demo_target6.TX_TYPE_CD` from `ACCT_ID`

- **Change:** Replaced `l3.TX_TYPE_CD as o_ACCT_ID` with `q.ACCT_ID as o_ACCT_ID`.
- **Verbatim parity output:**

```text
## DEMO_TARGET3
- rows: baseline=4 actual=4
- columns compared: 8
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET5
- rows: baseline=2 actual=2
- columns compared: 5
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET6
- rows: baseline=2 actual=2
- columns compared: 12
- **MISMATCH**:
  - column TX_TYPE_CD: 2/2 rows differ (first at {'ACCT_ID': np.int64(1001)}: baseline='DR' actual=np.int64(1001))
```

- **XML fact:** `exp_TRANS.o_ACCT_ID = :LKP.lkp_TRANS1(ACCT_ID)`;
  `lkp_TRANS1` returns `TX_TYPE_CD` from `lkp_demo_source3`. The target port is
  named `TX_TYPE_CD`, not the lookup key.
- **Resolution:** Restored the left join to the deduplicated lookup return port.
  Final parity passed.

### Counterfactual 2c — Lookup first physical row instead of Use Last Value

- **Change:** Changed `order by __seed_row desc` to `order by __seed_row asc` in
  all three `int_m1_lkp_*` models.
- **Verbatim parity output:**

```text
## DEMO_TARGET3
- rows: baseline=4 actual=4
- columns compared: 8
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET5
- rows: baseline=2 actual=2
- columns compared: 5
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET6
- rows: baseline=2 actual=2
- columns compared: 12
- **MISMATCH**:
  - column TX_TYPE_CD: 1/2 rows differ (first at {'ACCT_ID': np.int64(1002)}: baseline='DR' actual='TR')
```

- **XML fact:** All three lookup transformations use `Use Last Value`. The seeded
  duplicate `lkp_demo_source3.ACCT_ID=1002` has last row `TX_TYPE_CD='DR'`;
  selecting the first row incorrectly returns `'TR'`.
- **Resolution:** Restored descending seed-row ordering in all three lookup models.
  Final parity passed.

### Counterfactual 2d — Aggregator grouped by `ACCT_ID + TX_ID`

- **Change:** Added `TX_ID` to the aggregation window partition, inventing a
  second grouping key.
- **Verbatim parity output:**

```text
## DEMO_TARGET3
- rows: baseline=4 actual=4
- columns compared: 8
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET5
- rows: baseline=2 actual=2
- columns compared: 5
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET6
- rows: baseline=2 actual=2
- columns compared: 12
- **MISMATCH**:
  - column TX_AMT: 1/2 rows differ (first at {'ACCT_ID': np.int64(1001)}: baseline=np.float64(2031.24) actual=np.float64(-100.0))
```

- **XML fact:** `ACCT_ID` is the only `EXPRESSIONTYPE=GROUPBY` port in
  `agg_TRANS`; `o_TX_AMT` is `SUM(TX_AMT)` across all rows for that account.
- **Resolution:** Restored ACCT_ID-only partitioning and retained the unrounded
  plain SUM. Final parity passed.

### Counterfactual 2e — Route DEFAULT1/NULL `ACCT_TYP` rows to `demo_target5`

- **Change:** Added a NULL `ACCT_TYP` branch to `demo_target5_GRP` and included
  NULLs in the router filter.
- **Verbatim parity output:**

```text
## DEMO_TARGET3
- rows: baseline=4 actual=4
- columns compared: 8
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET5
- rows: baseline=2 actual=3
- columns compared: 5
- **MISMATCH**:
  - row count mismatch: baseline=2 actual=3

## DEMO_TARGET6
- rows: baseline=2 actual=2
- columns compared: 12
- result: **MATCH** (all values within tolerance)
```

- **XML fact:** `DEFAULT1` is connected to no target. SQL NULL comparisons match
  neither `ACCT_TYP = 'SB'` nor `ACCT_TYP != 'SB'`, so the NULL `ACCT_TYP` row is
  dropped.
- **Resolution:** Restored the explicit two-predicate router filter and unconnected
  DEFAULT1 behavior. Final parity passed.

### Counterfactual 2f — `demo_target5.FIRST_NM` from `demo_source3`

- **Change:** Added `demo_source3.FIRST_NM` to the SQL-override projection and
  replaced the lookup return with that source value.
- **Verbatim parity output:**

```text
## DEMO_TARGET3
- rows: baseline=4 actual=4
- columns compared: 8
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET5
- rows: baseline=2 actual=2
- columns compared: 5
- **MISMATCH**:
  - column FIRST_NM: 1/2 rows differ (first at {'ACCT_ID': np.int64(1004)}: baseline='AVA' actual='NINA')

## DEMO_TARGET6
- rows: baseline=2 actual=2
- columns compared: 12
- result: **MATCH** (all values within tolerance)
```

- **XML fact:** `FIRST_NM` is `lkp_TRANS2.FIRST_NM`, returned by
  `lkp_demo_source1` on `ACCT_ID`; it is not `demo_source3.FIRST_NM`.
- **Resolution:** Restored the lookup return port. Final parity passed.

### Counterfactual 2g — Parse `SELL_ED_DT` using declared `mm/dd/yyyy`

- **Change:** Reversed the month/day extraction to emulate the flat file's
  declared `mm/dd/yyyy` format instead of the expression's DD/MM/YYYY format.
- **Verbatim parity output:**

```text
## DEMO_TARGET3
- rows: baseline=4 actual=4
- columns compared: 8
- **MISMATCH**:
  - column SELL_ED_DT: 4/4 rows differ (first at {'PRODUCT_ID': 'PRD0001'}: baseline='2024-07-17' actual=nan)

## DEMO_TARGET5
- rows: baseline=2 actual=2
- columns compared: 5
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET6
- rows: baseline=2 actual=2
- columns compared: 12
- result: **MATCH** (all values within tolerance)
```

- **XML fact:** `exp_TRANS2.o_SELL_ED_DT = TO_DATE(SELL_ED_DT,'DD/MM/YYYY')`.
  The flat-file declared format does not override this expression. The seeded
  values such as `17/07/2024` are valid under DD/MM/YYYY but invalid when read
  as mm/dd/yyyy.
- **Resolution:** Restored DD/MM/YYYY reconstruction with NULL-on-invalid
  `TRY_CAST`. Final parity passed.
