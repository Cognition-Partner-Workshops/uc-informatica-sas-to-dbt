#!/usr/bin/env python3
"""Deterministic synthesized seed data for the Informatica track.

Generates banking-flavored CSVs for every source/lookup table read by the three
mappings in legacy/informatica/wf_demo_mapping.XML. Columns and types match the
SOURCEFIELD declarations in the XML. A fixed random seed makes every run
byte-identical. Row mixes deliberately exercise every router branch:

- m_demo_mapping1: accounts with ACCT_TYP='SB' (demo_target6 branch), other
  account types (demo_target5 branch), and NULL ACCT_TYP (unconnected DEFAULT).
- m_demo_mapping2: demo_source1 rows whose ID exists in the demo_target1
  pre-image (matched -> Update branch candidates) and brand-new IDs (Insert).
- m_demo_mapping3: members with NULL Member_Type_Code (filtered out = invalid),
  and among valid rows both NULL and non-NULL Social_Security_Number.

Run from the repo root: python3 legacy/informatica/data/generate_seed_data.py
"""
import csv
import os
import random

SEED = 20240131
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
BUSINESS_DATE = "2024-01-31"

FIRST = ["AVA", "LIAM", "NOAH", "MIA", "ZOE", "ELI", "IVY", "MAX", "LEO", "KAI",
         "ANNA", "OMAR", "NINA", "RAVI", "SARA", "TOM"]
LAST = ["RIVERA", "CHEN", "PATEL", "KIM", "SILVA", "OKAFOR", "NOVAK", "HAYES",
        "DUBOIS", "MORI", "COSTA", "IQBAL", "LARSEN", "BAKER", "SINGH", "WEISS"]
COLORS = ["Black", "Silver", "Blue", "Red", "Green", "White"]
TX_DESCS = ["ATM WITHDRAWAL", "POS PURCHASE", "ONLINE TRANSFER", "SALARY CREDIT",
            "UTILITY PAYMENT", "CARD PAYMENT", "STANDING ORDER", "CASH DEPOSIT"]


def write_csv(name, header, rows):
    path = os.path.join(OUT_DIR, name)
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)
    print(f"wrote {path} ({len(rows)} rows)")


def gen_demo_source1_and_target1(rng):
    """m_demo_mapping2: flat-file feed + demo_target1 pre-image (SCD lookup)."""
    # Pre-image: 57 existing rows, Key 1..57 (SEQTRANS current value is 57).
    pre_rows = []
    pre_ids = []
    for k in range(1, 58):
        rid = f"REC{k:05d}"
        pre_ids.append(rid)
        pre_rows.append([
            k, f"BNK{rng.randint(1, 9):02d}", f"BR{rng.randint(100, 999)}",
            "2023-12-31", rid,
            f"General ledger account {k:03d}", f"GL{k:04d}",
            "IDWUSER", "2023-12-31", "IDWUSER", "2023-12-31",
            "Y", "2023-01-01", "9999-12-31",
        ])
    write_csv("demo_target1.csv",
              ["Key", "LEAD_CO_MNE", "BRANCH_CO_MNE", "MIS_DATE", "ID",
               "DESCRIPTION", "SHORT_NAME", "CREATED_BY", "CREATED_TIME",
               "UPDATED_BY", "UPDATED_TIME", "ACTIVE_FLAG", "START_DATE",
               "END_DATE"], pre_rows)

    # Source feed: 40 matched rows (half with changed attributes -> Update
    # candidates) + 80 new IDs (Insert branch). Sorted by ID so that the
    # file order equals ID order (sequence assignment is deterministic).
    rows = []
    matched = rng.sample(pre_ids, 40)
    for i, rid in enumerate(matched):
        pre = pre_rows[pre_ids.index(rid)]
        changed = i % 2 == 0
        rows.append([
            pre[1], pre[2], BUSINESS_DATE, rid,
            (pre[5] + " REVISED") if changed else pre[5],
            pre[6],
        ])
    for k in range(58, 138):
        rows.append([
            f"BNK{rng.randint(1, 9):02d}", f"BR{rng.randint(100, 999)}",
            BUSINESS_DATE, f"REC{k:05d}",
            f"General ledger account {k:03d}", f"GL{k:04d}",
        ])
    rows.sort(key=lambda r: r[3])
    write_csv("demo_source1.csv",
              ["LEAD_CO_MNE", "BRANCH_CO_MNE", "MIS_DATE", "ID", "DESCRIPTION",
               "SHORT_NAME"], rows)


def gen_mapping1(rng):
    """m_demo_mapping1: accounts, transactions, and the three lookup tables."""
    n_accounts = 150
    acct_ids = list(range(1001, 1001 + n_accounts))
    acct_rows = []
    for i, aid in enumerate(acct_ids):
        if i % 10 == 9:
            typ = ""  # NULL ACCT_TYP -> unconnected DEFAULT router group
        elif i % 3 == 0:
            typ = "SB " if i % 6 == 0 else "SB"  # savings (trailing-space cases)
        else:
            typ = rng.choice(["CA", "FD", "LN"])
        acct_rows.append([
            aid, typ,
            f"Account {aid} ledger  " if i % 4 == 0 else f"Account {aid} ledger",
            f"  {rng.randint(1, 50) * 1000}" if i % 5 == 0
            else str(rng.randint(1, 50) * 1000),
            f"20{rng.randint(15, 23):02d}-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}",
            "" if i % 4 else "2025-06-30",
            rng.choice(["A", "C", "D"]),
        ])
    write_csv("demo_source4.csv",
              ["ACCT_ID", "ACCT_TYP", "ACCT_DESC", "CRDT_LN", "CR8_DT",
               "CLSR_DT", "ACCT_STAT_CD"], acct_rows)

    # Transactions: cover ~130 of the accounts (inner join drops the rest),
    # plus a few orphan ACCT_IDs that the join eliminates.
    tx_rows = []
    tx_id = 5001
    used_bal = set()
    covered = acct_ids[:130] + [9901, 9902, 9903]
    cust_of_acct = {aid: 70000 + (aid % 97) for aid in covered}
    for aid in covered:
        for _ in range(rng.randint(1, 4)):
            bal = round(rng.uniform(100, 99000) + tx_id / 100.0, 2)
            while bal in used_bal:
                bal = round(bal + 0.01, 2)
            used_bal.add(bal)
            tx_rows.append([
                tx_id, aid, rng.choice(FIRST), rng.choice(LAST),
                f"2024-01-{rng.randint(1, 30):02d} "
                f"{rng.randint(0, 23):02d}:{rng.randint(0, 59):02d}:00",
                round(rng.uniform(-5000, 5000), 2),
                rng.choice(["DR", "CR"]), bal, rng.choice(TX_DESCS),
                rng.randint(300, 850), cust_of_acct[aid],
            ])
            tx_id += 1
    tx_rows.sort(key=lambda r: (r[1], r[0]))  # ACCT_ID, TX_ID order
    write_csv("demo_source3.csv",
              ["TX_ID", "ACCT_ID", "FIRST_NM", "LAST_NM", "TX_DTTM", "TX_AMT",
               "TX_TYPE_CD", "BAL_AMT", "TX_DESC", "CRDT_SCORE", "CUST_ID"],
              tx_rows)

    # lkp_demo_source1: customer master keyed by ACCT_ID (some accounts absent).
    lkp1 = []
    for aid in acct_ids[:120]:
        lkp1.append([
            aid, cust_of_acct.get(aid, 70000 + (aid % 97)),
            rng.choice(FIRST), rng.choice(LAST),
            f"{rng.randint(1, 999)} High Street",
            f"{rng.randint(2000000000, 2999999999)}",
            f"c{aid}@mail.example",
            str(rng.randint(21, 79)),
            f"19{rng.randint(50, 99):02d}-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}",
            rng.choice(["RET", "CORP"]),
        ])
    write_csv("lkp_demo_source1.csv",
              ["ACCT_ID", "CUST_ID", "FIRST_NM", "LAST_NM", "CUST_ADDR",
               "CUST_PHN", "CUST_EML_ADDR", "AGE", "DOB", "CUST_TYP"], lkp1)

    # lkp_demo_source3: account-type reference keyed by ACCT_ID (some absent).
    lkp3 = [[aid, rng.choice(["DR", "CR", "TR"]),
             rng.choice(["Debit posting", "Credit posting", "Transfer posting"])]
            for aid in acct_ids[:125]]
    write_csv("lkp_demo_source3.csv", ["ACCT_ID", "TX_TYPE_CD", "TX_TYPE_DESC"],
              lkp3)

    # lkp_demo_source2: credit bureau data keyed by CUST_ID.
    cust_ids = sorted(set(cust_of_acct.values()))
    lkp2 = []
    for cid in cust_ids[:90]:
        score = rng.randint(300, 850)
        lkp2.append([cid, score, min(score + rng.randint(0, 60), 850),
                     max(score - rng.randint(0, 60), 300),
                     rng.randint(5, 200) * 1000,
                     round(rng.uniform(0, 80000), 2),
                     round(rng.uniform(2000, 25000), 2)])
    write_csv("lkp_demo_source2.csv",
              ["CUST_ID", "CRDT_SCORE", "MAX_CRDT_SCORE", "MIN_CRDT_SCORE",
               "MAX_CRDT_LMT", "CURR_CRDT_BAL_AMT", "AVG_INC_AMT"], lkp2)

    # demo_source5: product flat file, dates in DD/MM/YYYY as the mapping expects.
    prod_rows = []
    for pid in range(1, 121):
        prod_rows.append([
            f"PRD{pid:04d}", f"Card Product {pid:03d}", f"P{pid:03d}",
            rng.choice(COLORS), str(rng.randint(10, 999)),
            str(rng.randint(100, 999)),
            f"{rng.randint(1, 28):02d}/{rng.randint(1, 12):02d}/20{rng.randint(20, 23)}",
            f"{rng.randint(1, 28):02d}/{rng.randint(1, 12):02d}/20{rng.randint(24, 27)}",
        ])
    write_csv("demo_source5.csv",
              ["PRODUCT_ID", "PRODUCT_NM", "PRODUCT_NO", "COLOR", "STD_COST",
               "LIST_PRICE", "SELL_ST_DT", "SELL_ED_DT"], prod_rows)


def gen_demo_source2(rng):
    """m_demo_mapping3: member records."""
    rows = []
    for mid in range(30001, 30201):
        i = mid - 30001
        invalid = i % 8 == 7  # NULL Member_Type_Code -> filtered out
        ssn_null = i % 2 == 0
        rows.append([
            rng.choice(["MR", "MS", "MRS", "DR"]),
            rng.choice(FIRST).title(), rng.choice(FIRST)[:1],
            rng.choice(LAST).title(), mid,
            rng.choice(["", "JR", "SR", "II"]),
            f"19{rng.randint(40, 99):02d}-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}",
            rng.choice(["M", "F"]),
            500000 + i,
            "" if ssn_null else 100000000 + i * 37,
            "" if invalid else rng.choice([1, 2, 3]),
            f"20{rng.randint(10, 23):02d}-{rng.randint(1, 12):02d}-01",
            rng.choice([1, 2, 18, 19]),
            # Label may only be NULL on rows that the SQL override filters out,
            # otherwise the ABORT() branch in EXPTRANS would fire.
            "" if (invalid and i % 16 == 15) else rng.choice(
                ["SELF", "SPOUSE", "CHILD", "OTHER"]),
        ])
    write_csv("demo_source2.csv",
              ["Title", "First_Name", "Middle_Name", "Last_Name", "Member_ID",
               "Member_Suffix", "Birth_Date", "Gender_Code",
               "Member_Record_Number", "Social_Security_Number",
               "Member_Type_Code", "Original_Effective_Date",
               "Relationship_to_Subscriber_Code",
               "Relationship_to_Subscriber_Code_Label"], rows)


def main():
    rng = random.Random(SEED)
    gen_demo_source1_and_target1(rng)
    gen_mapping1(rng)
    gen_demo_source2(rng)


if __name__ == "__main__":
    main()
