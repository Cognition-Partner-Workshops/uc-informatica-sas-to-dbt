# Reconciliation

| Object | Status | Baseline rows | Actual rows | Matched rows |
|---|---|---:|---:|---:|
| DEMO_TARGET1_INS | GREEN | 4 | 4 | 4 |
| DEMO_TARGET1_UPD | GREEN | 3 | 3 | 3 |
| DEMO_TARGET2 | GREEN | 3 | 3 | 3 |
| DEMO_TARGET21 | GREEN | 3 | 3 | 3 |
| DEMO_TARGET3 | RED | 4 |  |  |

`DEMO_TARGET3`: {"baseline_rows": 4, "error": "Missing target", "status": "RED"}

| DEMO_TARGET5 | RED | 2 |  |  |

`DEMO_TARGET5`: {"baseline_rows": 2, "error": "Missing target", "status": "RED"}

| DEMO_TARGET6 | RED | 2 |  |  |

`DEMO_TARGET6`: {"baseline_rows": 2, "error": "Missing target", "status": "RED"}


Full match: False
