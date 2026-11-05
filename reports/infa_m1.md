# Reconciliation

| Object | Status | Baseline rows | Actual rows | Matched rows |
|---|---|---:|---:|---:|
| DEMO_TARGET1_INS | RED | 4 |  |  |

`DEMO_TARGET1_INS`: {"baseline_rows": 4, "error": "Missing target", "status": "RED"}

| DEMO_TARGET1_UPD | RED | 3 |  |  |

`DEMO_TARGET1_UPD`: {"baseline_rows": 3, "error": "Missing target", "status": "RED"}

| DEMO_TARGET2 | RED | 3 |  |  |

`DEMO_TARGET2`: {"baseline_rows": 3, "error": "Missing target", "status": "RED"}

| DEMO_TARGET21 | RED | 3 |  |  |

`DEMO_TARGET21`: {"baseline_rows": 3, "error": "Missing target", "status": "RED"}

| DEMO_TARGET3 | GREEN | 4 | 4 | 4 |
| DEMO_TARGET5 | GREEN | 2 | 2 | 2 |
| DEMO_TARGET6 | GREEN | 2 | 2 | 2 |

Full match: False
