# Parity Report

Baseline: `baseline/informatica`  |  Actual: `dbt/informatica/dev.duckdb`

## DEMO_TARGET1_INS
- rows: baseline=80 actual=80
- columns compared: 14
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET1_UPD
- rows: baseline=0 actual=0
- columns compared: 14
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET2
- rows: baseline=100 actual=100
- columns compared: 14
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET21
- rows: baseline=75 actual=75
- columns compared: 14
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET3
- rows: baseline=120 actual=120
- columns compared: 8
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET5
- rows: baseline=252 actual=252
- columns compared: 5
- result: **MATCH** (all values within tolerance)

## DEMO_TARGET6
- rows: baseline=17 actual=17
- columns compared: 12
- result: **MATCH** (all values within tolerance)

**Overall: PARITY VERIFIED**
