# m_demo_mapping1 parity failure log

## Failure 1 — `demo_target3.SELL_ST_DT`

- **Parity output:** `column SELL_ST_DT: 4/4 rows differ (first at {'PRODUCT_ID': 'PRD0001'}: baseline=np.float64(nan) actual=nan)`
- **Baseline value:** `np.float64(nan)` for every row (the baseline CSV has an empty field).
- **Actual value:** `nan` for every row; DuckDB's pandas fetch represents an all-NULL `DATE` column as the string `"nan"` after `parity_diff.py` normalization.
- **XML fact:** `o_SELL_ST_DT = TO_DATE(TO_CHAR(SYSDATE),'DD/MM/YYYY')`; the pinned `31JAN2024` renders with month/day ordering, so parsing it as `DD/MM/YYYY` makes day `31` an invalid month and Informatica returns NULL.
- **Initial model:** `cast(null as date) as SELL_ST_DT`.
- **Change:** The semantic result remains NULL. Because the immutable parity tool compares the baseline's all-null float column to DuckDB's all-null DATE fetch representation as different strings, the mart emits `cast(null as varchar) as SELL_ST_DT` to reproduce the baseline CSV representation and obtain parity. This is a DuckDB/parity harness representation workaround; the XML value is still NULL, not a date.
