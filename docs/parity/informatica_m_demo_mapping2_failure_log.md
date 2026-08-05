# m_demo_mapping2 Verification Failure Log

This log records every parity failure encountered while implementing
`m_demo_mapping2`. The baseline and XML remain unchanged.

## Parity attempt 1 — failed

Command:

```text
scripts/parity_m_demo_mapping2.sh
```

The scoped parity diff reported:

```text
## DEMO_TARGET1_INS
- rows: baseline=4 actual=4
- columns compared: 14
- **MISMATCH**:
  - column UPDATED_TIME: 4/4 rows differ (first at {'ID': 'REC00004'}: baseline=np.float64(nan) actual=nan)
  - column START_DATE: 4/4 rows differ (first at {'ID': 'REC00004'}: baseline=np.float64(nan) actual=nan)
  - column END_DATE: 4/4 rows differ (first at {'ID': 'REC00004'}: baseline=np.float64(nan) actual=nan)

## DEMO_TARGET1_UPD
- rows: baseline=3 actual=3
- columns compared: 14
- **MISMATCH**:
  - column CREATED_TIME: 3/3 rows differ (first at {'ID': 'REC00001'}: baseline=np.float64(nan) actual=nan)
  - column START_DATE: 3/3 rows differ (first at {'ID': 'REC00001'}: baseline=np.float64(nan) actual=nan)
  - column END_DATE: 3/3 rows differ (first at {'ID': 'REC00001'}: baseline=np.float64(nan) actual=nan)

**Overall: PARITY FAILED**
```

The XML CONNECTOR list specifies those columns as unconnected on the
corresponding target instance, and `tools/informatica_baseline.py` writes them
as blank CSV fields. The unchanged parity tool reads an all-blank CSV column as
floating-point `NaN`; timestamp-typed NULL columns fetched from DuckDB were
normalized to the string `nan`, so the tool compared two logically NULL values
as different. The payload models were corrected to type their never-populated
columns as nullable `VARCHAR` expressions. DuckDB still coerces those columns
to the pre-existing target's timestamp types during the physical merge, while
the payload CSV comparison sees actual Python NULLs.

## Parity attempt 2 — passed

After the correction above:

```text
## DEMO_TARGET1_INS
- rows: baseline=4 actual=4
- columns compared: 14
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET1_UPD
- rows: baseline=3 actual=3
- columns compared: 14
- result: **MATCH** (all values within tolerance)

**Overall: PARITY VERIFIED**
```
