"""Build the PII classification for run SF_20261015_DS.

Inputs (committed under evidence/):
  columns_inventory.csv         information_schema.columns of SOURCE_/DBT_/SCAI_/BASELINE_ schemas
  system_classify_results.json  CALL SYSTEM$CLASSIFY(<table>, {'auto_tag': false}) per base table
Outputs:
  seeds/pii_classification.csv  one row per classified personal-data column (dbt seed)
  seeds/pii_reviewed_not_masked.csv  columns looked at and deliberately left clear
  CLASSIFICATION.md             the same two tables for reviewers
  sql/04_apply_pii_tags.sql     ALTER TABLE ... SET TAG statements

Usage: python3 scripts/build_classification.py [--mask-org-unit-codes]
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = "DEVIN_MIGRATION_DEMO"
TAG = f"{DB}.DBT_SF_20261015_DS.PII_CATEGORY"
SCHEMAS = (
    "SOURCE_SF_20261015_DS",
    "DBT_SF_20261015_DS",
    "SCAI_SF_20261015_DS",
    "BASELINE_SF_20261015_DS",
)

# Column-name fallback: column -> (category, confidence).
NAME_RULES = {
    "FIRST_NAME": ("NAME", "HIGH"), "LAST_NAME": ("NAME", "HIGH"), "MIDDLE_NAME": ("NAME", "HIGH"),
    "FIRST_NM": ("NAME", "HIGH"), "LAST_NM": ("NAME", "HIGH"),
    "TITLE": ("NAME", "MEDIUM"), "MEMBER_SUFFIX": ("NAME", "MEDIUM"),
    "PRIMARY_EMAIL": ("EMAIL", "HIGH"), "CUST_EML_ADDR": ("EMAIL", "HIGH"),
    "PHONE_NUMBER": ("PHONE", "HIGH"), "CUST_PHN": ("PHONE", "HIGH"),
    "CUST_ADDR": ("STREET_ADDRESS", "HIGH"),
    "DATE_OF_BIRTH": ("DATE_OF_BIRTH", "HIGH"), "BIRTH_DATE": ("DATE_OF_BIRTH", "HIGH"), "DOB": ("DATE_OF_BIRTH", "HIGH"),
    "AGE": ("AGE", "HIGH"),
    "GENDER": ("GENDER", "HIGH"), "GENDER_CODE": ("GENDER", "HIGH"),
    "SOCIAL_SECURITY_NUMBER": ("NATIONAL_ID", "HIGH"), "SOC_NUMBER": ("NATIONAL_ID", "HIGH"),
    "SSN_HASH": ("NATIONAL_ID", "HIGH"),
    "CUSTOMER_ID": ("CUSTOMER_ID", "HIGH"), "CUST_ID": ("CUSTOMER_ID", "HIGH"),
    "CLAIMANT_ID": ("CUSTOMER_ID", "HIGH"),
    "MEMBER_ID": ("CUSTOMER_ID", "HIGH"), "MEMBER_IDENTIFIER": ("CUSTOMER_ID", "HIGH"),
    "MEMBER_NUMBER": ("CUSTOMER_ID", "HIGH"), "MEMBER_RECORD_NUMBER": ("CUSTOMER_ID", "HIGH"),
    "OFFICER_ID": ("STAFF_ID", "MEDIUM"), "AGENT_ID": ("STAFF_ID", "MEDIUM"),
}
ORG_UNIT_CODES = {"BRANCH_ID", "BRANCH_CODE", "LEAD_CO_MNE", "BRANCH_CO_MNE"}

# Columns deliberately left clear: column -> reason.
NOT_PERSONAL = {
    "ACCT_AGE_MONTHS": "Age of the account, not of a person (SYSTEM$CLASSIFY false positive)",
    "POLICY_AGE_MONTHS": "Age of the policy, not of a person (SYSTEM$CLASSIFY false positive)",
    "REGION_CODE": "Six coarse sales regions (NE, MW, W ...); not identifying on its own",
    "BRANCH_ID": "Branch code (B015 ...): organisational unit, not a person (decision option A)",
    "BRANCH_CODE": "Branch code (BR016 ...): organisational unit, not a person (decision option A)",
    "LEAD_CO_MNE": "Tenant/company mnemonic (BNK01 ...): organisational unit (decision option A)",
    "BRANCH_CO_MNE": "Branch company mnemonic (BR101 ...): organisational unit (decision option A)",
    "CREATED_BY": "Always the service account IDWUSER",
    "UPDATED_BY": "Always the service account IDWUSER",
}

# Identifier keys named in tools/keys/*.json that are personal data.
KEYS_FILES = [ROOT.parents[1] / "tools" / "keys" / "informatica_keys.json",
              ROOT.parents[1] / "tools" / "keys" / "sas_keys.json"]


def personal_keys():
    keys = set()
    for path in KEYS_FILES:
        for cols in json.loads(path.read_text()).values():
            keys.update(c.upper() for c in cols)
    return {k for k in keys if k in NAME_RULES}


def main():
    mask_org = "--mask-org-unit-codes" in sys.argv
    if mask_org:
        for col in ORG_UNIT_CODES:
            NAME_RULES[col] = ("ORG_UNIT", "MEDIUM")
            NOT_PERSONAL.pop(col)

    classify = json.loads((ROOT / "evidence" / "system_classify_results.json").read_text())
    key_cols = personal_keys()
    with open(ROOT / "evidence" / "columns_inventory.csv") as f:
        inventory = [r for r in csv.DictReader(f) if r["schema"] in SCHEMAS]

    rows, reviewed = [], []
    for r in inventory:
        fq = f"{r['schema']}.{r['table']}"
        if fq not in classify:  # views: masked through the base table they select from
            continue
        col = r["column"]
        rec = classify[fq].get("classification_result", {}).get(col, {}).get("recommendation")
        if col in NOT_PERSONAL:
            src = f"SYSTEM$CLASSIFY said {rec['semantic_category']} ({rec['confidence']}); overruled" if rec else "column name"
            reviewed.append([r["schema"], r["table"], col, r["type"], src, NOT_PERSONAL[col]])
            continue
        if col not in NAME_RULES:
            if rec:
                raise SystemExit(f"unreviewed SYSTEM$CLASSIFY hit: {fq}.{col} {rec['semantic_category']}")
            continue
        category, confidence = NAME_RULES[col]
        if rec:
            source, confidence = f"SYSTEM$CLASSIFY ({rec['semantic_category']})", rec["confidence"]
        elif col in key_cols:
            source = "tools/keys/*.json + column name"
        else:
            source = "column name"
        rows.append([r["schema"], r["table"], col, r["type"], category, source, confidence])

    rows.sort()
    reviewed.sort()
    header = ["schema_name", "table_name", "column_name", "data_type", "pii_category", "source", "confidence"]
    with open(ROOT / "seeds" / "pii_classification.csv", "w", newline="") as f:
        csv.writer(f).writerows([header] + rows)
    rheader = ["schema_name", "table_name", "column_name", "data_type", "source", "reason_left_clear"]
    with open(ROOT / "seeds" / "pii_reviewed_not_masked.csv", "w", newline="") as f:
        csv.writer(f).writerows([rheader] + reviewed)

    with open(ROOT / "sql" / "04_apply_pii_tags.sql", "w") as f:
        f.write("-- Generated by scripts/build_classification.py from seeds/pii_classification.csv. Do not edit by hand.\n")
        f.write("-- Run as SF_20261015_DS_DBT (APPLY TAG on account). Setting the tag attaches the masking policy for the column's data type.\n")
        for s, t, c, _, cat, _, _ in rows:
            f.write(f"alter table {DB}.{s}.{t} modify column {c} set tag {TAG} = '{cat}';\n")

    rollback_path = ROOT / "sql" / "99_rollback.sql"
    rollback_sql = rollback_path.read_text()
    marker = f"alter tag {TAG} unset"
    _, found, rollback_tail = rollback_sql.partition(marker)
    if not found:
        raise SystemExit(f"could not find rollback policy-detach section in {rollback_path}")
    rollback_tail = marker + rollback_tail
    with open(rollback_path, "w") as f:
        f.write("-- Generated by scripts/build_classification.py from seeds/pii_classification.csv. Do not edit by hand.\n")
        f.write("-- Run as SF_20261015_DS_DBT before teardown, after the demo objects are no longer needed.\n")
        for s, t, c, _, _, _, _ in rows:
            f.write(f"alter table {DB}.{s}.{t} modify column {c} unset tag {TAG};\n")
        f.write(rollback_tail)

    def md(hdr, body):
        out = ["| " + " | ".join(hdr) + " |", "|" + "---|" * len(hdr)]
        out += ["| " + " | ".join(b) + " |" for b in body]
        return "\n".join(out)

    by_schema = {s: sum(1 for x in rows if x[0] == s) for s in SCHEMAS}
    (ROOT / "CLASSIFICATION.md").write_text(
        "# PII classification, run SF_20261015_DS\n\n"
        "Generated by `scripts/build_classification.py`; edit the rules there, not this file.\n\n"
        f"**{len(rows)} personal-data columns** in base tables "
        + ", ".join(f"{s} {n}" for s, n in by_schema.items())
        + ". Views are not listed: the policy is attached to the base-table column, so every view that selects it returns the masked value too.\n\n"
        "Sources, in order of precedence: `SYSTEM$CLASSIFY` (works on this account through `CALL`; raw output in "
        "`evidence/system_classify_results.json`), then key columns named in `tools/keys/*.json`, then the column name. "
        "Confidence is Snowflake's when it classified the column, otherwise mine.\n\n"
        "## Masked columns\n\n" + md(header, rows) + "\n\n"
        "## Reviewed and left clear\n\n" + md(rheader, reviewed) + "\n")
    print(f"{len(rows)} classified, {len(reviewed)} reviewed-not-masked; per schema {by_schema}")


if __name__ == "__main__":
    main()
