# Parity Report

Baseline: `snowflake/BASELINE_SF_20261015_DS`  |  Actual: `snowflake/SCAI_SF_20261015_DS`

## DEMO_TARGET2
- rows: baseline=3 actual=3
- columns compared: 14
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET21
- rows: baseline=3 actual=3
- columns compared: 14
- **MISMATCH**:
  - column GENDER: 3/3 rows differ (first at {'MEMBER_IDENTIFIER': np.float64(30002.0)}: baseline=np.False_ actual='F')

**Overall: PARITY FAILED**
