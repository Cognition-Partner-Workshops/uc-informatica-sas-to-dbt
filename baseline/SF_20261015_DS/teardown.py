#!/usr/bin/env python3
"""Drop every Snowflake object of one demo run and prove the account is clean.

Lists the run objects two ways (SHOW ... LIKE on the run token, and the RUN tag in
SNOWFLAKE.ACCOUNT_USAGE.TAG_REFERENCES, which lags by up to two hours), drops
them when --yes is given, and prints the tag count the contract asks for plus
the warehouse's last metering row.

    python3 baseline/<token>/teardown.py --token SF_20261015_DS          # list only
    python3 baseline/<token>/teardown.py --token SF_20261015_DS --yes    # drop
"""
import argparse
import os
import sys
import re

import snowflake.connector

DB = "DEVIN_MIGRATION_DEMO"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--token", required=True)
    ap.add_argument("--yes", action="store_true", help="drop the objects (default lists them)")
    args = ap.parse_args()
    tok = args.token
    if not re.fullmatch(r"SF_[A-Z0-9]+_[A-Z]{2}", tok):
        sys.exit(f"token {tok!r} must look like SF_20261015_DS")
    expected = {
        "SCHEMA": {f"{DB}.{k}_{tok}" for k in ("SOURCE", "BASELINE", "DBT", "SCAI", "ORACLE")},
        "WAREHOUSE": {f"{tok}_WH"},
        "RESOURCE MONITOR": {f"{tok}_MON"},
        "USER": {f"{tok}_DEMO", f"{tok}_READER_USER"},
        "ROLE": {f"{tok}_DBT", f"{tok}_READER"},
    }
    cs = snowflake.connector.connect(
        account=os.environ.get("SNOWFLAKE_ACCOUNT", "yd76133.us-east-2.aws"),
        user=os.environ.get("SNOWFLAKE_USER", "SMITCHESCOGNITION"),
        password=os.environ.get("SNOWFLAKE_PASSWORD") or os.environ["SNOWFLAKE_PAT"],
        role=os.environ.get("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
    ).cursor()

    def q(sql):
        cs.execute(sql)
        return cs.fetchall()

    found = []
    for kind, sql, col in (
        ("SCHEMA", f"SHOW SCHEMAS LIKE '%_{tok}' IN DATABASE {DB}", 1),
        ("WAREHOUSE", f"SHOW WAREHOUSES LIKE '{tok}_WH'", 0),
        ("RESOURCE MONITOR", f"SHOW RESOURCE MONITORS LIKE '{tok}_MON'", 0),
        ("USER", f"SHOW USERS LIKE '{tok}_%'", 0),
        ("ROLE", f"SHOW ROLES LIKE '{tok}_%'", 1),
    ):
        # SHOW ... LIKE treats "_" as a one-character wildcard, so keep only the exact names
        for row in q(sql):
            name = f"{DB}.{row[col]}" if kind == "SCHEMA" else row[col]
            if name in expected[kind]:
                found.append((kind, name))

    print(f"objects named for {tok}:")
    for kind, name in found:
        print(f"  {kind:17s} {name}")

    tagged = q(f"""select object_database, object_schema, object_name, domain, tag_name, tag_value
        from snowflake.account_usage.tag_references
        where tag_name in ('RUN', 'EXPIRES') and tag_value like 'SF_%' and object_deleted is null
        order by domain, object_name""")
    print(f"\nlive tag references for SF_* runs in ACCOUNT_USAGE (lags up to 2 h): {len(tagged)}")
    for r in tagged:
        print("  ", " | ".join(str(x) for x in r))

    if not args.yes:
        print("\nnothing dropped; rerun with --yes to drop the objects listed above")
    else:
        # warehouse first so nothing can start a query mid-drop, monitor last since the
        # warehouse references it
        order = {"WAREHOUSE": 0, "USER": 1, "SCHEMA": 2, "ROLE": 3, "RESOURCE MONITOR": 4}
        for kind, name in sorted(found, key=lambda f: order[f[0]]):
            print(f"  DROP {kind} {name}")
            q(f"DROP {kind} IF EXISTS {name}")
        print("\nafter teardown:")
        for kind, sql, col in (
            ("SCHEMA", f"SHOW SCHEMAS LIKE '%_{tok}' IN DATABASE {DB}", 1),
            ("WAREHOUSE", f"SHOW WAREHOUSES LIKE '{tok}_WH'", 0),
            ("USER", f"SHOW USERS LIKE '{tok}_%'", 0),
            ("ROLE", f"SHOW ROLES LIKE '{tok}_%'", 1),
            ("RESOURCE MONITOR", f"SHOW RESOURCE MONITORS LIKE '{tok}_MON'", 0),
        ):
            left = [r[col] for r in q(sql)
                    if (f"{DB}.{r[col]}" if kind == "SCHEMA" else r[col]) in expected[kind]]
            print(f"  {kind.lower()}s: {len(left)}")

    n = q("""select count(*) from snowflake.account_usage.tag_references
        where tag_name in ('RUN','EXPIRES') and tag_value like 'SF_%'""")[0][0]
    print(f"\nselect count(*) from snowflake.account_usage.tag_references where tag_name in ('RUN','EXPIRES') and tag_value like 'SF_%'  ->  {n}")
    print("(ACCOUNT_USAGE keeps dropped objects with OBJECT_DELETED set, so this count only reaches zero when the tag rows age out; the live count is the one above.)")
    meter = q(f"""select start_time, end_time, credits_used from snowflake.account_usage.warehouse_metering_history
        where warehouse_name = '{tok}_WH' order by start_time desc limit 1""")
    print(f"last metering row for {tok}_WH: {meter[0] if meter else 'none yet (ACCOUNT_USAGE lags up to 3 h)'}")
    print(f"\nremaining by hand: remove the ViewOnly org secrets SF_DEMO_USER, SF_DEMO_PASSWORD, SF_DEMO_ROLE, SF_DEMO_WAREHOUSE, SF_DEMO_DATABASE, SF_RUN_TOKEN (Settings > Secrets, or DELETE /v3/organizations/{{org}}/secrets/{{id}}).")


if __name__ == "__main__":
    main()
