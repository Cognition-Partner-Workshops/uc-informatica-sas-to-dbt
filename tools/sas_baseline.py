#!/usr/bin/env python3
"""Deterministic re-implementation of the six legacy SAS programs' semantics.

Executes the legacy logic (as documented in docs/stm/sas_stm.md) in DuckDB
against the seed CSVs under legacy/sas/data/csv/ with the run date pinned to
31JAN2024, and writes one CSV per persistent output dataset into baseline/sas/.

Programs covered (in dependency order):
  1. load_customer_accounts       -> CUST_ACCOUNTS_DAILY, ACCT_EXCEPTIONS
  2. daily_transaction_processing -> DAILY_TRANSACTIONS, TXN_ANOMALIES, RUNNING_BALANCES
  3. credit_risk_scoring          -> RISK_SCORES, RISK_MIGRATION, RISK_SUMMARY
  4. monthly_regulatory_reporting -> MONTHLY_RWA, DELINQUENCY_AGING, LLP_COVERAGE,
                                     CAPITAL_ADEQUACY
  5. claims_processing            -> CLAIMS_REGISTER, CLAIMS_REVIEW_QUEUE, FRAUD_ALERTS
  6. policy_valuation             -> POLICY_VALUATION, LOSS_RATIO_SUMMARY

Faithfulness notes (see the STM "Notes / ambiguities" sections for detail):
  - SAS missing-value ordering is reproduced explicitly (missing < any number),
    e.g. NULL RUNNING_BALANCE -> OVERDRAFT, NULL LTV -> MTG risk weight 0.35.
  - The global DROP statement removes EXCEPTION_CODE/EXCEPTION_DESC from
    ACCT_EXCEPTIONS, and SNAPSHOT_DATE is unset (null) on exception rows.
  - Wall-clock LOAD_TIMESTAMP / SCORE_TIMESTAMP columns are excluded.
  - PROC APPEND FORCE keeps only the base-table columns of
    CURATED.DAILY_TRANSACTIONS (the 10 feed columns).
  - PROC FORMAT display recodes are materialized as *_DESC companion columns
    (identically in the dbt models, via seed lookup tables).

Usage:
    python3 tools/sas_baseline.py [--out baseline/sas]
"""

import argparse
import os
import sys

import duckdb

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sas_load_raw import REPO, load_all  # noqa: E402
from sas_lineage import parse_formats  # noqa: E402

RUN_DATE = "DATE '2024-01-31'"
REPORT_MONTH = "202401"
MODEL_ID = "CRM-2023-Q4-v2"


def fmt_case(fmt_name, col, formats, other_label):
    """Render a PROC FORMAT value mapping as a SQL CASE expression."""
    mapping = formats[fmt_name]["mapping"]
    parts = [f"case"]
    for code, label in mapping.items():
        if code.upper() == "OTHER":
            continue
        lab = label.replace("'", "''")
        parts.append(f" when {col} = '{code}' then '{lab}'" if not code.lstrip("-").isdigit()
                     else f" when {col} = {code} then '{lab}'")
    parts.append(f" else '{other_label}' end")
    return "".join(parts)


def build(con, formats):
    steps = {}

    # ------------------------------------------------------------------
    # Program 1: load_customer_accounts (run_date=31JAN2024, region=ALL)
    # ------------------------------------------------------------------
    accttype_desc = fmt_case("$ACCTTYPE", "ACCOUNT_TYPE", formats, "Unknown")
    acctstat_desc = fmt_case("$ACCTSTAT", "ACCOUNT_STATUS", formats, "Unknown")
    riskrate_desc = fmt_case("RISKRATE", "RISK_RATING", formats, "Not Rated")
    custseg_desc = fmt_case("$CUSTSEG", "CUSTOMER_SEGMENT", formats, "Unclassified")
    region_desc = fmt_case("$REGION", "REGION_CODE", formats, "Unknown")

    con.execute(f"""
    create or replace table acct_base as
    select
      a.ACCOUNT_ID, a.CUSTOMER_ID, a.ACCOUNT_TYPE, a.ACCOUNT_STATUS,
      a.OPEN_DATE, a.CLOSE_DATE, a.CURRENT_BALANCE, a.AVAILABLE_BALANCE,
      a.CREDIT_LIMIT, a.INTEREST_RATE, a.BRANCH_ID, a.OFFICER_ID,
      a.LAST_ACTIVITY_DATE,
      d.FIRST_NAME, d.LAST_NAME, d.SSN_HASH, d.DATE_OF_BIRTH,
      d.CUSTOMER_SEGMENT, d.RISK_RATING, d.REGION_CODE, d.PRIMARY_EMAIL,
      d.PHONE_NUMBER,
      datediff('month', a.OPEN_DATE, {RUN_DATE}) as ACCT_AGE_MONTHS,
      datediff('day', a.LAST_ACTIVITY_DATE, {RUN_DATE}) as DAYS_INACTIVE,
      case when a.ACCOUNT_TYPE in ('CC','LOC','HELC') and a.CREDIT_LIMIT > 0
           then (a.CURRENT_BALANCE / a.CREDIT_LIMIT) * 100 end as UTILIZATION_PCT,
      case when datediff('day', a.LAST_ACTIVITY_DATE, {RUN_DATE}) > 365
                and a.ACCOUNT_STATUS = 'A' then 'Y' else 'N' end as DORMANCY_FLAG,
      case when a.CURRENT_BALANCE >= 250000 then 'Y' else 'N' end as HIGH_BALANCE_FLAG
    from ora_dw.cust_accounts a
    inner join ora_dw.cust_demographics d on a.CUSTOMER_ID = d.CUSTOMER_ID
    where a.ACCOUNT_STATUS not in ('W','C')
      and (a.OPEN_DATE <= {RUN_DATE} or a.OPEN_DATE is null)  -- SAS missing sorts low
    order by a.CUSTOMER_ID, a.ACCOUNT_ID
    """)

    steps["CUST_ACCOUNTS_DAILY"] = f"""
    select *,
      {accttype_desc} as ACCOUNT_TYPE_DESC,
      {acctstat_desc} as ACCOUNT_STATUS_DESC,
      {riskrate_desc} as RISK_RATING_DESC,
      {custseg_desc} as CUSTOMER_SEGMENT_DESC,
      {region_desc} as REGION_CODE_DESC,
      {RUN_DATE} as SNAPSHOT_DATE
    from acct_base
    """

    # Exception rows: the DATA-step DROP removes EXCEPTION_CODE/DESC from both
    # outputs, and SNAPSHOT_DATE is not yet assigned when exceptions are output.
    steps["ACCT_EXCEPTIONS"] = """
    select b.*, cast(null as date) as SNAPSHOT_DATE
    from acct_base b
    where b.ACCOUNT_TYPE in ('CHK','SAV','MMA','CD')
      and (b.CURRENT_BALANCE < 0 or b.CURRENT_BALANCE is null)  -- SAS missing < 0
    union all
    select b.*, cast(null as date)
    from acct_base b
    where b.UTILIZATION_PCT > 95
    union all
    select b.*, cast(null as date)
    from acct_base b
    where b.RISK_RATING is null
    """

    con.execute(f"create or replace table cust_accounts_daily as {steps['CUST_ACCOUNTS_DAILY']}")

    # ------------------------------------------------------------------
    # Program 2: daily_transaction_processing (txn_date=31JAN2024)
    # ------------------------------------------------------------------
    con.execute(f"""
    create or replace table txn_validated as
    select * from raw_bank.txn_feed_20240131
    where TRANSACTION_ID is not null
      and ACCOUNT_ID is not null
      and TRANSACTION_AMOUNT is not null
      and abs(TRANSACTION_AMOUNT) <= 10000000
      and TRANSACTION_TYPE in ('DEP','WDR','TRF','PMT','FEE','INT','ADJ','REV','CHG','REF')
      and (TRANSACTION_DATE <= {RUN_DATE} or TRANSACTION_DATE is null)  -- SAS missing sorts low
    """)

    con.execute("""
    create or replace table txn_with_balance as
    with enriched as (
      select
        t.*,
        a.ACCOUNT_TYPE, a.CUSTOMER_ID, a.CUSTOMER_SEGMENT, a.REGION_CODE,
        a.BRANCH_ID as ACCT_BRANCH_ID,
        a.CURRENT_BALANCE as PRE_TXN_BALANCE,
        case
          when t.TRANSACTION_TYPE in ('DEP','INT','REF','REV')
            then a.CURRENT_BALANCE + t.TRANSACTION_AMOUNT
          when t.TRANSACTION_TYPE in ('WDR','PMT','FEE','CHG')
            then a.CURRENT_BALANCE - abs(t.TRANSACTION_AMOUNT)
          when t.TRANSACTION_TYPE in ('TRF','ADJ')
            then a.CURRENT_BALANCE + t.TRANSACTION_AMOUNT
          else a.CURRENT_BALANCE
        end as POST_TXN_BALANCE,
        a.RISK_RATING,
        case
          when t.TRANSACTION_TYPE in ('DEP','INT','REF','REV') then t.TRANSACTION_AMOUNT
          when t.TRANSACTION_TYPE in ('WDR','PMT','FEE','CHG') then -abs(t.TRANSACTION_AMOUNT)
          when t.TRANSACTION_TYPE in ('TRF','ADJ') then t.TRANSACTION_AMOUNT
          else 0
        end as BAL_DELTA
      from txn_validated t
      left join cust_accounts_daily a on t.ACCOUNT_ID = a.ACCOUNT_ID
    )
    select
      TRANSACTION_ID, ACCOUNT_ID, TRANSACTION_DATE, TRANSACTION_TYPE,
      TRANSACTION_AMOUNT, CHANNEL, MERCHANT_CATEGORY, DESCRIPTION, POST_DATE,
      CURRENCY_CODE, ACCOUNT_TYPE, CUSTOMER_ID, CUSTOMER_SEGMENT, REGION_CODE,
      ACCT_BRANCH_ID as BRANCH_ID, PRE_TXN_BALANCE, POST_TXN_BALANCE, RISK_RATING,
      PRE_TXN_BALANCE + sum(BAL_DELTA) over (
        partition by ACCOUNT_ID
        order by TRANSACTION_DATE, TRANSACTION_ID
        rows between unbounded preceding and current row) as RUNNING_BALANCE
    from enriched
    order by ACCOUNT_ID, TRANSACTION_DATE, TRANSACTION_ID
    """)

    # z-score stats come from the curated history BEFORE the day's append
    con.execute(f"""
    create or replace table txn_stats as
    select
      ACCOUNT_ID,
      avg(abs(TRANSACTION_AMOUNT)) as AVG_TXN_AMT,
      stddev_samp(abs(TRANSACTION_AMOUNT)) as STD_TXN_AMT,
      count(*) as TXN_COUNT
    from curated_src.daily_transactions
    where TRANSACTION_DATE >= {RUN_DATE} - interval 90 day
    group by ACCOUNT_ID
    """)

    # SAS missing-value ordering: NULL RUNNING_BALANCE satisfies "< 0",
    # NULL PRE_TXN_BALANCE*0.9 satisfies "amount > ..."
    steps["TXN_ANOMALIES"] = """
    select * from (
      select
        e.*,
        s.AVG_TXN_AMT,
        s.STD_TXN_AMT,
        case when s.STD_TXN_AMT > 0
             then (abs(e.TRANSACTION_AMOUNT) - s.AVG_TXN_AMT) / s.STD_TXN_AMT
        end as Z_SCORE,
        case
          when (case when s.STD_TXN_AMT > 0
                     then (abs(e.TRANSACTION_AMOUNT) - s.AVG_TXN_AMT) / s.STD_TXN_AMT
                end) > 3 then 'HIGH_AMOUNT'
          when e.RUNNING_BALANCE < 0 or e.RUNNING_BALANCE is null then 'OVERDRAFT'
          when e.TRANSACTION_TYPE = 'WDR'
               and (e.PRE_TXN_BALANCE is null
                    or abs(e.TRANSACTION_AMOUNT) > e.PRE_TXN_BALANCE * 0.9)
            then 'LARGE_WITHDRAWAL'
          when e.CUSTOMER_ID is null then 'ORPHAN_ACCOUNT'
          else ''
        end as ANOMALY_TYPE
      from txn_with_balance e
      left join txn_stats s on e.ACCOUNT_ID = s.ACCOUNT_ID
    ) where ANOMALY_TYPE <> ''
    """

    # PROC APPEND FORCE: base structure wins -> only the 10 feed columns remain
    steps["DAILY_TRANSACTIONS"] = """
    select TRANSACTION_ID, ACCOUNT_ID, TRANSACTION_DATE, TRANSACTION_TYPE,
           TRANSACTION_AMOUNT, CHANNEL, MERCHANT_CATEGORY, DESCRIPTION,
           POST_DATE, CURRENCY_CODE
    from curated_src.daily_transactions
    union all
    select TRANSACTION_ID, ACCOUNT_ID, TRANSACTION_DATE, TRANSACTION_TYPE,
           TRANSACTION_AMOUNT, CHANNEL, MERCHANT_CATEGORY, DESCRIPTION,
           POST_DATE, CURRENCY_CODE
    from txn_with_balance
    """

    steps["RUNNING_BALANCES"] = """
    select ACCOUNT_ID, TRANSACTION_DATE, TRANSACTION_ID, RUNNING_BALANCE
    from txn_with_balance
    """

    # ------------------------------------------------------------------
    # Program 3: credit_risk_scoring (score_date=31JAN2024)
    # ------------------------------------------------------------------
    con.execute(f"""
    create or replace table scored as
    with latest_bureau as (
      select * from (
        select b.*,
               row_number() over (partition by CUSTOMER_ID order by SCORE_DATE desc) as rn
        from ora_dw.bureau_scores b
        where SCORE_DATE <= {RUN_DATE}
      ) where rn = 1
    ),
    score_input as (
      select
        a.ACCOUNT_ID, a.CUSTOMER_ID, a.ACCOUNT_TYPE, a.CURRENT_BALANCE,
        a.CREDIT_LIMIT, a.ACCT_AGE_MONTHS, a.DAYS_INACTIVE, a.UTILIZATION_PCT,
        a.CUSTOMER_SEGMENT, a.REGION_CODE,
        b.FICO_SCORE, b.VANTAGE_SCORE, b.BUREAU_INQS_6MO, b.BUREAU_TRADES_OPEN,
        b.BUREAU_DEROGS, b.BUREAU_UTIL_PCT, b.BUREAU_OLDEST_TRADE_MO,
        p.PMT_ONTIME_12MO, p.PMT_LATE_30_12MO, p.PMT_LATE_60_12MO,
        p.PMT_LATE_90_12MO, p.MAX_DAYS_PAST_DUE_EVER, p.MONTHS_SINCE_LAST_DPD,
        p.AVG_PMT_RATIO_12MO,
        c.COLLATERAL_VALUE, c.LAST_APPRAISAL_DATE,
        case when c.COLLATERAL_VALUE > 0
             then a.CURRENT_BALANCE / c.COLLATERAL_VALUE end as LTV
      from cust_accounts_daily a
      left join latest_bureau b on a.CUSTOMER_ID = b.CUSTOMER_ID
      left join ora_dw.payment_history p on a.ACCOUNT_ID = p.ACCOUNT_ID
      left join ora_dw.collateral c on a.ACCOUNT_ID = c.ACCOUNT_ID
      where a.SNAPSHOT_DATE = {RUN_DATE}
        and a.ACCOUNT_TYPE in ('MTG','AUTO','PERS','CC','LOC','HELC')
    ),
    woe as (
      select *,
        case when FICO_SCORE is null then 0.198
             when FICO_SCORE >= 760 then -1.204
             when FICO_SCORE >= 720 then -0.812
             when FICO_SCORE >= 680 then -0.356
             when FICO_SCORE >= 640 then 0.198
             when FICO_SCORE >= 600 then 0.654
             else 1.102 end as WOE_FICO,
        case when UTILIZATION_PCT is null then 0
             when UTILIZATION_PCT <= 10 then -0.956
             when UTILIZATION_PCT <= 30 then -0.521
             when UTILIZATION_PCT <= 50 then -0.102
             when UTILIZATION_PCT <= 70 then 0.334
             when UTILIZATION_PCT <= 90 then 0.789
             else 1.245 end as WOE_UTIL,
        case when PMT_LATE_90_12MO is null then 0
             when PMT_LATE_90_12MO = 0 then -0.678
             when PMT_LATE_90_12MO = 1 then 0.445
             else 1.567 end as WOE_DPD,
        case when ACCT_AGE_MONTHS is null then 0
             when ACCT_AGE_MONTHS >= 120 then -0.534
             when ACCT_AGE_MONTHS >= 60 then -0.289
             when ACCT_AGE_MONTHS >= 24 then 0.045
             else 0.456 end as WOE_AGE,
        case when ACCOUNT_TYPE not in ('MTG','AUTO','HELC') then 0
             when LTV is null then 0
             when LTV <= 0.60 then -0.712
             when LTV <= 0.80 then -0.234
             when LTV <= 1.00 then 0.356
             else 0.889 end as WOE_LTV
      from score_input
    ),
    logodds as (
      select *,
        -3.2145 + 0.412 * WOE_FICO + 0.198 * WOE_UTIL + 0.289 * WOE_DPD
                + 0.067 * WOE_AGE + 0.134 * WOE_LTV as LOG_ODDS
      from woe
    ),
    pd_calc as (
      select *, 1 / (1 + exp(-LOG_ODDS)) as PD from logodds
    )
    select
      ACCOUNT_ID, CUSTOMER_ID, ACCOUNT_TYPE, CURRENT_BALANCE, CREDIT_LIMIT,
      ACCT_AGE_MONTHS, DAYS_INACTIVE, UTILIZATION_PCT, CUSTOMER_SEGMENT,
      REGION_CODE, FICO_SCORE, VANTAGE_SCORE, BUREAU_INQS_6MO,
      BUREAU_TRADES_OPEN, BUREAU_DEROGS, BUREAU_UTIL_PCT,
      BUREAU_OLDEST_TRADE_MO, PMT_ONTIME_12MO, PMT_LATE_30_12MO,
      PMT_LATE_60_12MO, PMT_LATE_90_12MO, MAX_DAYS_PAST_DUE_EVER,
      MONTHS_SINCE_LAST_DPD, AVG_PMT_RATIO_12MO, COLLATERAL_VALUE,
      LAST_APPRAISAL_DATE, LTV,
      PD,
      case when ACCOUNT_TYPE in ('MTG','AUTO','HELC') then
             case when LTV is null then 0.40
                  else greatest(0, least(1, (LTV - 0.5) * 0.8)) end
           when ACCOUNT_TYPE = 'CC' then 0.75
           else 0.50 end as LGD,
      case when ACCOUNT_TYPE in ('CC','LOC','HELC')
           then CURRENT_BALANCE + 0.50 * (CREDIT_LIMIT - CURRENT_BALANCE)
           else CURRENT_BALANCE end as EAD,
      PD * (case when ACCOUNT_TYPE in ('MTG','AUTO','HELC') then
                   case when LTV is null then 0.40
                        else greatest(0, least(1, (LTV - 0.5) * 0.8)) end
                 when ACCOUNT_TYPE = 'CC' then 0.75
                 else 0.50 end)
         * (case when ACCOUNT_TYPE in ('CC','LOC','HELC')
                 then CURRENT_BALANCE + 0.50 * (CREDIT_LIMIT - CURRENT_BALANCE)
                 else CURRENT_BALANCE end) as EXPECTED_LOSS,
      case when PD < 0.005 then 1
           when PD < 0.01 then 2
           when PD < 0.03 then 3
           when PD < 0.07 then 4
           when PD < 0.15 then 5
           when PD < 0.30 then 6
           else 7 end as NEW_RISK_RATING,
      {RUN_DATE} as SCORE_DATE,
      '{MODEL_ID}' as MODEL_ID
    from pd_calc
    """)

    steps["RISK_SCORES"] = "select * from scored"

    steps["RISK_MIGRATION"] = f"""
    select
      {RUN_DATE} as SCORE_DATE,
      a.ACCOUNT_ID,
      a.RISK_RATING as PREV_RATING,
      s.NEW_RISK_RATING as CURR_RATING,
      case
        when a.RISK_RATING is null then 'NEW'
        when s.NEW_RISK_RATING < a.RISK_RATING then 'UPGRADE'
        when s.NEW_RISK_RATING > a.RISK_RATING then 'DOWNGRADE'
        else 'STABLE'
      end as MIGRATION_DIRECTION,
      s.PD,
      s.EXPECTED_LOSS
    from scored s
    inner join cust_accounts_daily a on s.ACCOUNT_ID = a.ACCOUNT_ID
    where a.SNAPSHOT_DATE = {RUN_DATE}
      and (a.RISK_RATING <> s.NEW_RISK_RATING or a.RISK_RATING is null)
    """

    steps["RISK_SUMMARY"] = """
    select
      ACCOUNT_TYPE,
      NEW_RISK_RATING,
      count(PD) as N_ACCOUNTS,
      avg(PD) as AVG_PD,
      avg(LGD) as AVG_LGD,
      sum(EAD) as TOTAL_EAD,
      sum(EXPECTED_LOSS) as TOTAL_EL
    from scored
    group by ACCOUNT_TYPE, NEW_RISK_RATING
    """

    # ------------------------------------------------------------------
    # Program 4: monthly_regulatory_reporting (report_month=202401)
    # month_end = 31JAN2024 = snapshot date
    # ------------------------------------------------------------------
    con.execute(f"""
    create or replace table monthly_rwa as
    with weighted as (
      select
        a.ACCOUNT_TYPE, a.CUSTOMER_SEGMENT, a.CURRENT_BALANCE,
        case
          when a.ACCOUNT_TYPE in ('CHK','SAV','MMA') then 0.00
          when a.ACCOUNT_TYPE = 'CD' then 0.00
          -- SAS missing ordering: NULL LTV satisfies "LTV <= 0.80"
          when a.ACCOUNT_TYPE = 'MTG' and (l.LTV <= 0.80 or l.LTV is null) then 0.35
          when a.ACCOUNT_TYPE = 'MTG' and l.LTV > 0.80 then 0.50
          when a.ACCOUNT_TYPE = 'HELC' then 0.50
          when a.ACCOUNT_TYPE in ('AUTO','PERS') then 0.75
          when a.ACCOUNT_TYPE = 'CC' then 0.75
          when a.ACCOUNT_TYPE = 'LOC' then 1.00
          else 1.00
        end as RISK_WEIGHT
      from cust_accounts_daily a
      left join ora_dw.loan_details l on a.ACCOUNT_ID = l.ACCOUNT_ID
      where a.SNAPSHOT_DATE = {RUN_DATE}
    )
    select
      '{REPORT_MONTH}' as REPORT_MONTH,
      ACCOUNT_TYPE,
      CUSTOMER_SEGMENT,
      RISK_WEIGHT,
      count(*) as N_ACCOUNTS,
      sum(CURRENT_BALANCE) as TOTAL_EXPOSURE,
      sum(CURRENT_BALANCE * RISK_WEIGHT) as RWA
    from weighted
    group by 1, 2, 3, 4
    """)
    steps["MONTHLY_RWA"] = "select * from monthly_rwa"

    steps["DELINQUENCY_AGING"] = f"""
    select
      '{REPORT_MONTH}' as REPORT_MONTH,
      a.ACCOUNT_TYPE,
      a.REGION_CODE,
      case
        when l.DAYS_PAST_DUE = 0 then 'Current'
        when l.DAYS_PAST_DUE between 1 and 29 then '1-29'
        when l.DAYS_PAST_DUE between 30 and 59 then '30-59'
        when l.DAYS_PAST_DUE between 60 and 89 then '60-89'
        when l.DAYS_PAST_DUE between 90 and 119 then '90-119'
        when l.DAYS_PAST_DUE between 120 and 179 then '120-179'
        when l.DAYS_PAST_DUE >= 180 then '180+'
        else 'Unknown'
      end as DELINQ_BUCKET,
      count(*) as N_ACCOUNTS,
      sum(a.CURRENT_BALANCE) as TOTAL_BALANCE,
      sum(l.PAST_DUE_AMOUNT) as TOTAL_PAST_DUE
    from cust_accounts_daily a
    left join ora_dw.loan_details l on a.ACCOUNT_ID = l.ACCOUNT_ID
    where a.SNAPSHOT_DATE = {RUN_DATE}
      and a.ACCOUNT_TYPE in ('MTG','AUTO','PERS','CC','LOC','HELC')
    group by 1, 2, 3, 4
    """

    steps["LLP_COVERAGE"] = f"""
    select
      '{REPORT_MONTH}' as REPORT_MONTH,
      a.ACCOUNT_TYPE,
      count(*) as N_LOANS,
      sum(a.CURRENT_BALANCE) as GROSS_LOANS,
      sum(l.ALLOWANCE_AMT) as TOTAL_ALLOWANCE,
      case when sum(a.CURRENT_BALANCE) > 0
           then sum(l.ALLOWANCE_AMT) / sum(a.CURRENT_BALANCE) * 100
           else 0 end as COVERAGE_PCT,
      sum(case when l.DAYS_PAST_DUE >= 90 then a.CURRENT_BALANCE else 0 end)
        as NPL_BALANCE,
      case when sum(case when l.DAYS_PAST_DUE >= 90 then a.CURRENT_BALANCE else 0 end) > 0
           then sum(l.ALLOWANCE_AMT)
                / sum(case when l.DAYS_PAST_DUE >= 90 then a.CURRENT_BALANCE else 0 end) * 100
           else 0 end as NPL_COVERAGE_PCT
    from cust_accounts_daily a
    inner join ora_dw.loan_details l on a.ACCOUNT_ID = l.ACCOUNT_ID
    where a.SNAPSHOT_DATE = {RUN_DATE}
      and a.ACCOUNT_TYPE in ('MTG','AUTO','PERS','CC','LOC','HELC')
    group by 1, 2
    """

    steps["CAPITAL_ADEQUACY"] = f"""
    select
      '{REPORT_MONTH}' as REPORT_MONTH,
      sum(RWA) as TOTAL_RWA,
      50000000 as CET1_CAPITAL,
      65000000 as TIER1_CAPITAL,
      80000000 as TOTAL_CAPITAL,
      case when sum(RWA) > 0 then 50000000 / sum(RWA) * 100 end as CET1_RATIO,
      case when sum(RWA) > 0 then 65000000 / sum(RWA) * 100 end as TIER1_RATIO,
      case when sum(RWA) > 0 then 80000000 / sum(RWA) * 100 end as TOTAL_CAPITAL_RATIO,
      case when sum(RWA) = 0 then 'PASS'
           when 50000000 / sum(RWA) * 100 >= 4.5 then 'PASS' else 'FAIL' end as CET1_STATUS,
      case when sum(RWA) = 0 then 'PASS'
           when 65000000 / sum(RWA) * 100 >= 6.0 then 'PASS' else 'FAIL' end as TIER1_STATUS,
      case when sum(RWA) = 0 then 'PASS'
           when 80000000 / sum(RWA) * 100 >= 8.0 then 'PASS' else 'FAIL' end
        as TOTAL_CAPITAL_STATUS
    from monthly_rwa
    """

    # ------------------------------------------------------------------
    # Program 5: claims_processing (proc_date=31JAN2024)
    # ------------------------------------------------------------------
    clmstat_desc = fmt_case("$CLMSTAT", "CLAIM_STATUS", formats, "Unknown")

    con.execute("""
    create or replace table claims_valid as
    select
      f.CLAIM_ID, f.POLICY_ID, f.CLAIMANT_ID, f.LOSS_DATE, f.REPORTED_DATE,
      f.CLAIMED_AMOUNT, f.CAUSE_CODE, f.DESCRIPTION,
      p.POLICY_TYPE, p.EFFECTIVE_DATE, p.EXPIRATION_DATE, p.SUM_INSURED,
      p.DEDUCTIBLE
    from raw_ins.claims_feed_20240131 f
    inner join raw_ins.policies p
      on f.POLICY_ID = p.POLICY_ID and p.STATUS = 'ACTIVE'
    where f.LOSS_DATE >= p.EFFECTIVE_DATE
      and f.LOSS_DATE <= p.EXPIRATION_DATE
      and f.CLAIMED_AMOUNT <= p.SUM_INSURED
    """)

    con.execute("""
    create or replace table fraud_check as
    select
      c.*,
      f.FRAUD_SCORE,
      f.INDICATOR_FLAGS,
      case when f.FRAUD_SCORE >= 80 then 'HIGH'
           when f.FRAUD_SCORE >= 50 then 'MEDIUM'
           else 'LOW' end as FRAUD_RISK
    from claims_valid c
    left join raw_ins.fraud_indicators f
      on c.POLICY_ID = f.POLICY_ID and c.CLAIMANT_ID = f.CLAIMANT_ID
    """)

    steps["FRAUD_ALERTS"] = f"""
    select
      *,
      case when INDICATOR_FLAGS is not null and trim(INDICATOR_FLAGS) <> ''
           then 'Fraud score: ' || cast(cast(FRAUD_SCORE as integer) as varchar)
                || '; ' || INDICATOR_FLAGS
           else 'Fraud score: ' || cast(cast(FRAUD_SCORE as integer) as varchar)
      end as ALERT_REASON,
      {RUN_DATE} as ALERT_DATE
    from fraud_check
    where FRAUD_RISK = 'HIGH'
    """

    con.execute("""
    create or replace table adjudicated as
    select
      *,
      case
        when FRAUD_RISK = 'HIGH' then 'DENY'
        when FRAUD_RISK = 'LOW' and CLAIMED_AMOUNT <= 5000
             and POLICY_TYPE in ('AUTO','HOME','RENT') then 'APPR'
        when FRAUD_RISK = 'LOW' and CLAIMED_AMOUNT <= SUM_INSURED * 0.25
             and CLAIMED_AMOUNT <= 50000 then 'APPR'
        else 'PEND'
      end as ADJUDICATION_RESULT,
      case
        when FRAUD_RISK = 'HIGH' then 'High fraud risk - SIU referral'
        when FRAUD_RISK = 'LOW' and CLAIMED_AMOUNT <= 5000
             and POLICY_TYPE in ('AUTO','HOME','RENT')
          then 'Auto-approved: low risk, small claim'
        when FRAUD_RISK = 'LOW' and CLAIMED_AMOUNT <= SUM_INSURED * 0.25
             and CLAIMED_AMOUNT <= 50000
          then 'Auto-approved: within 25% of sum insured'
        else concat_ws('; ',
               case when FRAUD_RISK = 'MEDIUM' then 'Medium fraud risk' end,
               case when CLAIMED_AMOUNT > 50000 then 'Large claim' end,
               case when CLAIMED_AMOUNT > SUM_INSURED * 0.25 then 'Exceeds 25% threshold' end)
      end as ADJUDICATION_REASON,
      case
        when FRAUD_RISK = 'HIGH' then 0
        when FRAUD_RISK = 'LOW' and CLAIMED_AMOUNT <= 5000
             and POLICY_TYPE in ('AUTO','HOME','RENT')
          then greatest(0, CLAIMED_AMOUNT - DEDUCTIBLE)
        when FRAUD_RISK = 'LOW' and CLAIMED_AMOUNT <= SUM_INSURED * 0.25
             and CLAIMED_AMOUNT <= 50000
          then greatest(0, CLAIMED_AMOUNT - DEDUCTIBLE)
      end as APPROVED_AMOUNT
    from fraud_check
    """)

    steps["CLAIMS_REGISTER"] = f"""
    select
      *,
      {RUN_DATE} as PROCESSING_DATE,
      ADJUDICATION_RESULT as CLAIM_STATUS,
      {clmstat_desc.replace('CLAIM_STATUS', 'ADJUDICATION_RESULT')} as CLAIM_STATUS_DESC
    from adjudicated
    """

    steps["CLAIMS_REVIEW_QUEUE"] = """
    select * from adjudicated
    where ADJUDICATION_RESULT in ('DENY', 'PEND')
    """

    # ------------------------------------------------------------------
    # Program 6: policy_valuation (val_date=31JAN2024, lob=ALL)
    # ------------------------------------------------------------------
    poltype_desc = fmt_case("$POLTYPE", "POLICY_TYPE", formats, "Unknown")
    riskcat_desc = fmt_case("$RISKCAT", "RISK_CATEGORY", formats, "Unrated")

    con.execute(f"""
    create or replace table policy_valuation as
    with inforce as (
      select
        p.POLICY_ID, p.CUSTOMER_ID, p.POLICY_TYPE, p.EFFECTIVE_DATE,
        p.EXPIRATION_DATE, p.ANNUAL_PREMIUM, p.SUM_INSURED, p.DEDUCTIBLE,
        p.RISK_CATEGORY, p.UNDERWRITING_CLASS, p.AGENT_ID, p.BRANCH_CODE,
        datediff('month', p.EFFECTIVE_DATE, {RUN_DATE}) as POLICY_AGE_MONTHS,
        datediff('month', {RUN_DATE}, p.EXPIRATION_DATE) as MONTHS_TO_EXPIRY,
        -- intnx('month', 31JAN2024, 3) = 01APR2024 (default BEGINNING alignment)
        case when p.EXPIRATION_DATE <= DATE '2024-04-01' then 'Y' else 'N' end
          as RENEWAL_DUE_FLAG,
        -- intck('month', max(eff, 01JAN2024), min(31JAN2024, exp)) = 0 at the
        -- January valuation date -> YTD earned premium is 0 for every policy
        p.ANNUAL_PREMIUM / 12 * least(12,
          datediff('month',
            greatest(p.EFFECTIVE_DATE, DATE '2024-01-01'),
            least({RUN_DATE}, p.EXPIRATION_DATE))) as YTD_EARNED_PREMIUM
      from raw_ins.policies p
      where p.STATUS = 'ACTIVE'
        and p.EFFECTIVE_DATE <= {RUN_DATE}
        and p.EXPIRATION_DATE >= {RUN_DATE}
    ),
    claims_exp as (
      select
        c.POLICY_ID,
        count(distinct c.CLAIM_ID) as NUM_CLAIMS,
        sum(c.INCURRED_AMOUNT) as TOTAL_INCURRED,
        sum(c.PAID_AMOUNT) as TOTAL_PAID,
        sum(c.RESERVED_AMOUNT) as TOTAL_RESERVED,
        max(c.LOSS_DATE) as LAST_CLAIM_DATE,
        sum(case when c.CLAIM_STATUS in ('OPEN','INV','ADJ','PEND')
                 then c.RESERVED_AMOUNT else 0 end) as OPEN_RESERVES,
        sum(case when c.CLAIM_STATUS = 'DENY' then 1 else 0 end) as DENIED_CLAIMS
      from raw_ins.claims c
      where c.LOSS_DATE >= DATE '2023-01-01'  -- intnx('month', val, -12) = 01JAN2023
        and c.LOSS_DATE <= {RUN_DATE}
      group by c.POLICY_ID
    ),
    premium_coll as (
      select
        POLICY_ID,
        sum(PREMIUM_AMOUNT) as COLLECTED_PREMIUM,
        sum(case when PAYMENT_STATUS = 'RETURNED' then PREMIUM_AMOUNT else 0 end)
          as RETURNED_PREMIUM,
        max(PAYMENT_DATE) as LAST_PAYMENT_DATE,
        count(case when PAYMENT_STATUS = 'LATE' then 1 end) as LATE_PAYMENTS
      from raw_ins.premiums
      where PAYMENT_DATE >= DATE '2024-01-01'  -- intnx('year', val, 0, 'B')
        and PAYMENT_DATE <= {RUN_DATE}
      group by POLICY_ID
    )
    select
      i.*,
      c.NUM_CLAIMS, c.TOTAL_INCURRED, c.TOTAL_PAID, c.TOTAL_RESERVED,
      c.LAST_CLAIM_DATE, c.OPEN_RESERVES, c.DENIED_CLAIMS,
      m.COLLECTED_PREMIUM, m.RETURNED_PREMIUM, m.LAST_PAYMENT_DATE, m.LATE_PAYMENTS,
      case when i.YTD_EARNED_PREMIUM > 0
           then coalesce(c.TOTAL_INCURRED, 0) / i.YTD_EARNED_PREMIUM end as LOSS_RATIO,
      case when i.YTD_EARNED_PREMIUM > 0
           then coalesce(c.TOTAL_INCURRED, 0) / i.YTD_EARNED_PREMIUM + 0.30
      end as COMBINED_RATIO,
      case when i.YTD_EARNED_PREMIUM > 0
                and coalesce(c.TOTAL_INCURRED, 0) / i.YTD_EARNED_PREMIUM + 0.30 <= 1.0
           then 'Y' else 'N' end as PREMIUM_ADEQUATE,
      greatest(0, i.YTD_EARNED_PREMIUM * 0.15 - coalesce(c.TOTAL_PAID, 0))
        as IBNR_ESTIMATE,
      coalesce(c.OPEN_RESERVES, 0)
        + greatest(0, i.YTD_EARNED_PREMIUM * 0.15 - coalesce(c.TOTAL_PAID, 0))
        as TOTAL_RESERVE,
      {RUN_DATE} as VALUATION_DATE,
      {poltype_desc.replace('POLICY_TYPE', 'i.POLICY_TYPE')} as POLICY_TYPE_DESC,
      {riskcat_desc.replace('RISK_CATEGORY', 'i.RISK_CATEGORY')} as RISK_CATEGORY_DESC
    from inforce i
    left join claims_exp c on i.POLICY_ID = c.POLICY_ID
    left join premium_coll m on i.POLICY_ID = m.POLICY_ID
    order by i.POLICY_ID
    """)
    steps["POLICY_VALUATION"] = "select * from policy_valuation"

    steps["LOSS_RATIO_SUMMARY"] = """
    select
      POLICY_TYPE,
      count(YTD_EARNED_PREMIUM) as N_POLICIES,
      sum(YTD_EARNED_PREMIUM) as TOTAL_EARNED,
      sum(TOTAL_INCURRED) as TOTAL_INCURRED,
      sum(TOTAL_PAID) as TOTAL_PAID,
      sum(TOTAL_RESERVE) as TOTAL_RESERVES,
      sum(IBNR_ESTIMATE) as TOTAL_IBNR,
      case when sum(YTD_EARNED_PREMIUM) > 0
           then sum(TOTAL_INCURRED) / sum(YTD_EARNED_PREMIUM) end as AGG_LOSS_RATIO,
      case when sum(YTD_EARNED_PREMIUM) > 0
           then sum(TOTAL_INCURRED) / sum(YTD_EARNED_PREMIUM) + 0.30
      end as AGG_COMBINED_RATIO
    from policy_valuation
    group by POLICY_TYPE
    """

    return steps


def write_outputs(con, steps, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    for name, sql in steps.items():
        df = con.execute(sql).fetch_df()
        for col in df.columns:
            if str(df[col].dtype).startswith("datetime64"):
                df[col] = df[col].dt.strftime("%Y-%m-%d")
        df.to_csv(os.path.join(out_dir, f"{name}.csv"), index=False)
        print(f"  baseline {name}: {len(df)} rows")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=os.path.join(REPO, "baseline", "sas"))
    args = parser.parse_args()

    con = duckdb.connect(":memory:")
    load_all(con)
    formats = parse_formats()
    steps = build(con, formats)
    write_outputs(con, steps, args.out)
    con.close()


if __name__ == "__main__":
    main()
