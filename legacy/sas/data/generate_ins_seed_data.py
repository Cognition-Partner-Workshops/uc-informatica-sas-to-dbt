#!/usr/bin/env python3
"""Generate the deterministic insurance seed data used by Programs/Insurance.

Produces the CSV extracts that stand in for the RAW_INS source tables read by
claims_processing.sas and policy_valuation.sas, plus FRAUD_INDICATORS.csv which
stands in for TERA_DW.FRAUD_INDICATORS (kept under raw_ins/ so the insurance
seed data lives in a single directory).

Output is byte-for-byte reproducible: the RNG is seeded and rows are written in
a fixed order. Business date matches the banking seed data (31JAN2024).

Rows are shaped so that every branch of the two insurance programs is
exercised: inactive/unknown policies, loss dates outside the policy period,
claims exceeding the sum insured, HIGH/MEDIUM/LOW fraud recodes, both
auto-approval rules, every manual-review (PEND) reason combination, claims
inside and outside the 12-month experience window, and premium payments with
POSTED/LATE/RETURNED statuses inside and outside the fiscal year.

Usage:
    python3 legacy/sas/data/generate_ins_seed_data.py [--out legacy/sas/data/csv/raw_ins]
"""

import argparse
import csv
import os
import random
from datetime import date, timedelta

BUSINESS_DATE = date(2024, 1, 31)
SEED = 20240131
N_POLICIES = 320
N_FEED_CLAIMS = 260

POLICY_TYPES = ("AUTO", "HOME", "RENT", "WL", "TL", "UL", "HLTH", "UMBR")
POLICY_TYPE_WEIGHTS = (28, 22, 8, 8, 12, 6, 12, 4)
POLICY_STATUSES = ("ACTIVE", "LAPSED", "CANCELLED", "EXPIRED")
POLICY_STATUS_WEIGHTS = (78, 9, 7, 6)
RISK_CATEGORIES = ("STD", "PREF", "SPRM", "SUB", "DEC")
RISK_CATEGORY_WEIGHTS = (46, 26, 10, 14, 4)
UW_CLASSES = ("UW1", "UW2", "UW3", "UW4")
CLAIM_STATUSES = ("OPEN", "INV", "ADJ", "PEND", "APPR", "DENY", "PAID", "CLOS")
CLAIM_STATUS_WEIGHTS = (14, 6, 8, 10, 16, 8, 24, 14)
CAUSE_CODES = ("COLL", "COMP", "FIRE", "THEFT", "WATER", "WIND", "LIAB", "MED", "OTHER")
PAYMENT_STATUSES = ("POSTED", "LATE", "RETURNED")
PAYMENT_STATUS_WEIGHTS = (82, 13, 5)

SUM_INSURED_BY_TYPE = {
    "AUTO": (25000, 100000),
    "HOME": (150000, 900000),
    "RENT": (15000, 60000),
    "WL": (50000, 1000000),
    "TL": (100000, 2000000),
    "UL": (100000, 1500000),
    "HLTH": (50000, 500000),
    "UMBR": (1000000, 5000000),
}

MONTHS = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN",
          "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")


def sas_date(value):
    if value is None:
        return ""
    return f"{value.day:02d}{MONTHS[value.month - 1]}{value.year}"


def money(value):
    return f"{value:.2f}"


def write_csv(path, header, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)
    print(f"  {path}: {len(rows)} rows")


def build_policies(rng):
    policies = []
    for i in range(1, N_POLICIES + 1):
        policy_type = rng.choices(POLICY_TYPES, weights=POLICY_TYPE_WEIGHTS, k=1)[0]
        status = rng.choices(POLICY_STATUSES, weights=POLICY_STATUS_WEIGHTS, k=1)[0]

        effective = BUSINESS_DATE - timedelta(days=rng.randint(30, 1400))
        term_years = rng.choice([1, 1, 1, 3, 5, 10]) if policy_type in ("AUTO", "HOME", "RENT", "HLTH", "UMBR") else rng.choice([10, 20, 30])
        expiration = effective + timedelta(days=365 * term_years)
        if status == "EXPIRED" or (status == "ACTIVE" and rng.random() < 0.04):
            # some active-but-expired rows fall out of the in-force filter
            expiration = BUSINESS_DATE - timedelta(days=rng.randint(5, 200))
        elif status == "ACTIVE" and rng.random() < 0.10:
            # renewal-due within 3 months of the valuation date
            expiration = BUSINESS_DATE + timedelta(days=rng.randint(5, 58))
        if status == "ACTIVE" and rng.random() < 0.03:
            # not yet effective at the valuation date
            effective = BUSINESS_DATE + timedelta(days=rng.randint(10, 90))
            expiration = effective + timedelta(days=365)

        lo, hi = SUM_INSURED_BY_TYPE[policy_type]
        sum_insured = float(rng.randrange(lo, hi, 500))
        deductible = float(rng.choice([0, 250, 500, 1000, 2500, 5000]))
        annual_premium = round(sum_insured * rng.uniform(0.004, 0.035) + rng.uniform(50, 400), 2)

        policies.append({
            "POLICY_ID": f"P{i:07d}",
            "CUSTOMER_ID": f"C{rng.randint(1, 250):07d}",
            "POLICY_TYPE": policy_type,
            "STATUS": status,
            "EFFECTIVE_DATE": effective,
            "EXPIRATION_DATE": expiration,
            "ANNUAL_PREMIUM": annual_premium,
            "SUM_INSURED": sum_insured,
            "DEDUCTIBLE": deductible,
            "RISK_CATEGORY": rng.choices(RISK_CATEGORIES, weights=RISK_CATEGORY_WEIGHTS, k=1)[0],
            "UNDERWRITING_CLASS": rng.choice(UW_CLASSES),
            "AGENT_ID": f"AG{rng.randint(1, 60):04d}",
            "BRANCH_CODE": f"BR{rng.randint(1, 25):03d}",
        })
    return policies


def build_claims(rng, policies):
    """Historical claims register rows (RAW_INS.CLAIMS) for policy_valuation."""
    rows = []
    seq = 0
    for policy in policies:
        n_claims = rng.choices([0, 1, 2, 3, 5], weights=[46, 28, 15, 8, 3], k=1)[0]
        for _ in range(n_claims):
            seq += 1
            # mostly inside the 12-month window (>= 01JAN2023), some older
            if rng.random() < 0.82:
                loss = BUSINESS_DATE - timedelta(days=rng.randint(0, 394))
            else:
                loss = BUSINESS_DATE - timedelta(days=rng.randint(395, 900))
            status = rng.choices(CLAIM_STATUSES, weights=CLAIM_STATUS_WEIGHTS, k=1)[0]
            incurred = round(rng.uniform(250, min(policy["SUM_INSURED"], 180000)), 2)
            if status in ("PAID", "CLOS", "APPR"):
                paid = round(incurred * rng.uniform(0.55, 1.0), 2)
                reserved = round(incurred - paid, 2)
            elif status == "DENY":
                paid = 0.0
                reserved = 0.0
            else:
                paid = round(incurred * rng.uniform(0.0, 0.4), 2)
                reserved = round(incurred - paid, 2)
            rows.append({
                "CLAIM_ID": f"CL{seq:07d}",
                "POLICY_ID": policy["POLICY_ID"],
                "CLAIMANT_ID": f"CM{rng.randint(1, 400):06d}",
                "LOSS_DATE": loss,
                "REPORT_DATE": loss + timedelta(days=rng.randint(0, 21)),
                "CLAIM_STATUS": status,
                "INCURRED_AMOUNT": incurred,
                "PAID_AMOUNT": paid,
                "RESERVED_AMOUNT": reserved,
            })
    return rows


def build_premiums(rng, policies):
    rows = []
    seq = 0
    for policy in policies:
        if policy["STATUS"] not in ("ACTIVE", "LAPSED"):
            continue
        monthly = round(policy["ANNUAL_PREMIUM"] / 12, 2)
        # payments across Nov 2023 - Jan 2024; only >= 01JAN2024 count YTD
        for pay_month in (date(2023, 11, 15), date(2023, 12, 15), date(2024, 1, 15)):
            if rng.random() < 0.12:
                continue  # missed payment
            seq += 1
            status = rng.choices(PAYMENT_STATUSES, weights=PAYMENT_STATUS_WEIGHTS, k=1)[0]
            pay_date = pay_month + timedelta(days=rng.randint(0, 12) if status == "LATE" else rng.randint(0, 5))
            if pay_date > BUSINESS_DATE:
                pay_date = BUSINESS_DATE
            rows.append({
                "PAYMENT_ID": f"PM{seq:07d}",
                "POLICY_ID": policy["POLICY_ID"],
                "PAYMENT_DATE": pay_date,
                "PREMIUM_AMOUNT": monthly,
                "PAYMENT_STATUS": status,
            })
    return rows


def build_fraud_indicators(rng, policies, claimants_by_policy):
    """Stand-in for TERA_DW.FRAUD_INDICATORS keyed by POLICY_ID + CLAIMANT_ID."""
    rows = []
    flags_pool = ("PRIOR_CLAIMS", "ADDR_MISMATCH", "EARLY_CLAIM", "DUP_INVOICE",
                  "STAGED_LOSS", "WATCHLIST", "AGENT_FLAG")
    for policy_id, claimant_id in sorted(claimants_by_policy):
        r = rng.random()
        if r < 0.62:
            continue  # most claimants have no fraud indicator row at all
        if r < 0.80:
            score = rng.randint(5, 49)     # LOW
        elif r < 0.93:
            score = rng.randint(50, 79)    # MEDIUM
        else:
            score = rng.randint(80, 99)    # HIGH
        n_flags = 0 if score < 50 else (1 if score < 80 else rng.randint(2, 3))
        flags = "|".join(rng.sample(flags_pool, n_flags)) if n_flags else ""
        rows.append({
            "POLICY_ID": policy_id,
            "CLAIMANT_ID": claimant_id,
            "FRAUD_SCORE": score,
            "INDICATOR_FLAGS": flags,
        })
    return rows


def build_claims_feed(rng, policies):
    """Daily claims feed (RAW_INS.CLAIMS_FEED_20240131) for claims_processing."""
    rows = []
    active = [p for p in policies
              if p["STATUS"] == "ACTIVE"
              and p["EFFECTIVE_DATE"] <= BUSINESS_DATE <= p["EXPIRATION_DATE"]]
    inactive = [p for p in policies if p["STATUS"] != "ACTIVE"]
    small_types = [p for p in active if p["POLICY_TYPE"] in ("AUTO", "HOME", "RENT")]

    for i in range(1, N_FEED_CLAIMS + 1):
        claim_id = f"FC{i:07d}"
        claimant_id = f"CM{rng.randint(1, 400):06d}"
        bucket = rng.random()

        if bucket < 0.05:
            # unknown policy id -> invalid (policy not found)
            policy = rng.choice(active)
            policy_id = f"PX{i:06d}"
            loss = BUSINESS_DATE - timedelta(days=rng.randint(1, 60))
            claimed = round(rng.uniform(500, 20000), 2)
        elif bucket < 0.10:
            # inactive policy -> invalid (not in the ACTIVE hash)
            policy = rng.choice(inactive)
            policy_id = policy["POLICY_ID"]
            loss = policy["EFFECTIVE_DATE"] + timedelta(days=30)
            claimed = round(rng.uniform(500, 20000), 2)
        elif bucket < 0.16:
            # loss date outside the policy period
            policy = rng.choice(active)
            policy_id = policy["POLICY_ID"]
            loss = policy["EFFECTIVE_DATE"] - timedelta(days=rng.randint(5, 120))
            claimed = round(rng.uniform(500, 20000), 2)
        elif bucket < 0.21:
            # claimed amount exceeds sum insured
            policy = rng.choice(active)
            policy_id = policy["POLICY_ID"]
            loss = _loss_in_period(rng, policy)
            claimed = round(policy["SUM_INSURED"] * rng.uniform(1.05, 1.6), 2)
        elif bucket < 0.45 and small_types:
            # small claim on AUTO/HOME/RENT -> auto-approve rule 1 (if LOW fraud)
            policy = rng.choice(small_types)
            policy_id = policy["POLICY_ID"]
            loss = _loss_in_period(rng, policy)
            claimed = round(rng.uniform(150, 5000), 2)
        elif bucket < 0.72:
            # within 25% of sum insured and <= 50k -> auto-approve rule 2
            policy = rng.choice(active)
            policy_id = policy["POLICY_ID"]
            loss = _loss_in_period(rng, policy)
            claimed = round(min(policy["SUM_INSURED"] * rng.uniform(0.05, 0.24), 49000), 2)
        elif bucket < 0.86:
            # large claim (> 50k) but within sum insured -> PEND
            policy = rng.choice([p for p in active if p["SUM_INSURED"] > 60000])
            policy_id = policy["POLICY_ID"]
            loss = _loss_in_period(rng, policy)
            claimed = round(rng.uniform(50001, min(policy["SUM_INSURED"], 400000)), 2)
        else:
            # exceeds 25% threshold but under 50k -> PEND
            policy = rng.choice([p for p in active if p["SUM_INSURED"] * 0.30 < 48000])
            policy_id = policy["POLICY_ID"]
            loss = _loss_in_period(rng, policy)
            claimed = round(min(policy["SUM_INSURED"] * rng.uniform(0.30, 0.9), 48000), 2)

        rows.append({
            "CLAIM_ID": claim_id,
            "POLICY_ID": policy_id,
            "CLAIMANT_ID": claimant_id,
            "LOSS_DATE": loss,
            "REPORTED_DATE": BUSINESS_DATE,
            "CLAIMED_AMOUNT": claimed,
            "CAUSE_CODE": rng.choice(CAUSE_CODES),
            "DESCRIPTION": f"{rng.choice(CAUSE_CODES)} loss reported ref {rng.randint(100000, 999999)}",
        })
    return rows


def _loss_in_period(rng, policy):
    start = max(policy["EFFECTIVE_DATE"], BUSINESS_DATE - timedelta(days=180))
    span = (min(policy["EXPIRATION_DATE"], BUSINESS_DATE) - start).days
    return start + timedelta(days=rng.randint(0, max(span, 0)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="legacy/sas/data/csv/raw_ins")
    args = parser.parse_args()
    rng = random.Random(SEED)

    policies = build_policies(rng)
    claims = build_claims(rng, policies)
    premiums = build_premiums(rng, policies)
    feed = build_claims_feed(rng, policies)
    claimant_keys = {(r["POLICY_ID"], r["CLAIMANT_ID"]) for r in feed}
    fraud = build_fraud_indicators(rng, policies, claimant_keys)

    write_csv(os.path.join(args.out, "POLICIES.csv"),
              ["POLICY_ID", "CUSTOMER_ID", "POLICY_TYPE", "STATUS", "EFFECTIVE_DATE",
               "EXPIRATION_DATE", "ANNUAL_PREMIUM", "SUM_INSURED", "DEDUCTIBLE",
               "RISK_CATEGORY", "UNDERWRITING_CLASS", "AGENT_ID", "BRANCH_CODE"],
              [[p["POLICY_ID"], p["CUSTOMER_ID"], p["POLICY_TYPE"], p["STATUS"],
                sas_date(p["EFFECTIVE_DATE"]), sas_date(p["EXPIRATION_DATE"]),
                money(p["ANNUAL_PREMIUM"]), money(p["SUM_INSURED"]), money(p["DEDUCTIBLE"]),
                p["RISK_CATEGORY"], p["UNDERWRITING_CLASS"], p["AGENT_ID"], p["BRANCH_CODE"]]
               for p in policies])

    write_csv(os.path.join(args.out, "CLAIMS.csv"),
              ["CLAIM_ID", "POLICY_ID", "CLAIMANT_ID", "LOSS_DATE", "REPORT_DATE",
               "CLAIM_STATUS", "INCURRED_AMOUNT", "PAID_AMOUNT", "RESERVED_AMOUNT"],
              [[c["CLAIM_ID"], c["POLICY_ID"], c["CLAIMANT_ID"], sas_date(c["LOSS_DATE"]),
                sas_date(c["REPORT_DATE"]), c["CLAIM_STATUS"], money(c["INCURRED_AMOUNT"]),
                money(c["PAID_AMOUNT"]), money(c["RESERVED_AMOUNT"])]
               for c in claims])

    write_csv(os.path.join(args.out, "PREMIUMS.csv"),
              ["PAYMENT_ID", "POLICY_ID", "PAYMENT_DATE", "PREMIUM_AMOUNT", "PAYMENT_STATUS"],
              [[p["PAYMENT_ID"], p["POLICY_ID"], sas_date(p["PAYMENT_DATE"]),
                money(p["PREMIUM_AMOUNT"]), p["PAYMENT_STATUS"]]
               for p in premiums])

    write_csv(os.path.join(args.out, "CLAIMS_FEED_20240131.csv"),
              ["CLAIM_ID", "POLICY_ID", "CLAIMANT_ID", "LOSS_DATE", "REPORTED_DATE",
               "CLAIMED_AMOUNT", "CAUSE_CODE", "DESCRIPTION"],
              [[f["CLAIM_ID"], f["POLICY_ID"], f["CLAIMANT_ID"], sas_date(f["LOSS_DATE"]),
                sas_date(f["REPORTED_DATE"]), money(f["CLAIMED_AMOUNT"]),
                f["CAUSE_CODE"], f["DESCRIPTION"]]
               for f in feed])

    write_csv(os.path.join(args.out, "FRAUD_INDICATORS.csv"),
              ["POLICY_ID", "CLAIMANT_ID", "FRAUD_SCORE", "INDICATOR_FLAGS"],
              [[f["POLICY_ID"], f["CLAIMANT_ID"], f["FRAUD_SCORE"], f["INDICATOR_FLAGS"]]
               for f in fraud])


if __name__ == "__main__":
    main()
