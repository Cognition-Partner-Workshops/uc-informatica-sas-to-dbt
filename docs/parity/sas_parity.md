# Parity Report

Baseline: `baseline/sas`  |  Actual: `dbt/sas/dev.duckdb`

## ACCT_EXCEPTIONS
- rows: baseline=32 actual=32
- columns compared: 28
- result: **MATCH** (all values within tolerance)

## CAPITAL_ADEQUACY
- rows: baseline=1 actual=1
- columns compared: 11
- result: **MATCH** (all values within tolerance)

## CLAIMS_REGISTER
- rows: baseline=190 actual=190
- columns compared: 22
- result: **MATCH** (all values within tolerance)

## CLAIMS_REVIEW_QUEUE
- rows: baseline=101 actual=101
- columns compared: 19
- result: **MATCH** (all values within tolerance)

## CUST_ACCOUNTS_DAILY
- rows: baseline=466 actual=466
- columns compared: 33
- result: **MATCH** (all values within tolerance)

## DAILY_TRANSACTIONS
- rows: baseline=18903 actual=18903
- columns compared: 10
- result: **MATCH** (all values within tolerance)

## DELINQUENCY_AGING
- rows: baseline=70 actual=70
- columns compared: 7
- result: **MATCH** (all values within tolerance)

## FRAUD_ALERTS
- rows: baseline=19 actual=19
- columns compared: 18
- result: **MATCH** (all values within tolerance)

## LLP_COVERAGE
- rows: baseline=6 actual=6
- columns compared: 8
- result: **MATCH** (all values within tolerance)

## LOSS_RATIO_SUMMARY
- rows: baseline=8 actual=8
- columns compared: 9
- result: **MATCH** (all values within tolerance)

## MONTHLY_RWA
- rows: baseline=59 actual=59
- columns compared: 7
- result: **MATCH** (all values within tolerance)

## POLICY_VALUATION
- rows: baseline=166 actual=166
- columns compared: 35
- result: **MATCH** (all values within tolerance)

## RISK_MIGRATION
- rows: baseline=195 actual=195
- columns compared: 7
- result: **MATCH** (all values within tolerance)

## RISK_SCORES
- rows: baseline=236 actual=236
- columns compared: 34
- result: **MATCH** (all values within tolerance)

## RISK_SUMMARY
- rows: baseline=12 actual=12
- columns compared: 7
- result: **MATCH** (all values within tolerance)

## RUNNING_BALANCES
- rows: baseline=610 actual=610
- columns compared: 4
- result: **MATCH** (all values within tolerance)

## TXN_ANOMALIES
- rows: baseline=46 actual=46
- columns compared: 23
- result: **MATCH** (all values within tolerance)

**Overall: PARITY VERIFIED**
