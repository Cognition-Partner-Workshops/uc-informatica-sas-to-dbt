# Parity Report

Baseline: `snowflake/BASELINE_SF_20261015_DS`  |  Actual: `snowflake/SCAI_SF_20261015_DS`

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
  - column TX_DTTM: 2/2 rows differ (first at {'ACCT_ID': np.int64(1001)}: baseline='54041295-06-21 01:00:00' actual='2024-01-15 11:00:00')

**Overall: PARITY FAILED**
