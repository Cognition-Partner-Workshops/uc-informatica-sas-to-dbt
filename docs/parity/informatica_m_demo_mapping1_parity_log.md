# m_demo_mapping1 parity failure log

## Failure 1 — `demo_target3.SELL_ST_DT`

- **Parity output under pandas 3.0.5:** `column SELL_ST_DT: 4/4 rows differ (first at {'PRODUCT_ID': 'PRD0001'}: baseline=np.float64(nan) actual=nan)`
- **Baseline value:** `np.float64(nan)` for every row (the baseline CSV has an empty field).
- **Actual value:** `nan` for every row.
- **XML fact:** `o_SELL_ST_DT = TO_DATE(TO_CHAR(SYSDATE),'DD/MM/YYYY')`; the pinned `31JAN2024` renders with month/day ordering, so parsing it as `DD/MM/YYYY` makes day `31` an invalid month and Informatica returns NULL.
- **Root cause:** This was not a model or XML mismatch. The parity harness was written against pandas 2. With pandas 3.0.5, `compare()` calls `bs.fillna("\0").astype(str)`; pandas 3 no longer silently upcasts the baseline float64 all-NaN column, while the actual object/string column fills to `"\x00"`, causing two NULLs to compare unequal.
- **Resolution:** Pinned the harness environment to `pandas==2.3.3` (`pandas<3`), restored the model expression to `cast(null as date)`, regenerated the baseline, and reran parity successfully. The recorded parity run uses pandas `2.3.3`.
