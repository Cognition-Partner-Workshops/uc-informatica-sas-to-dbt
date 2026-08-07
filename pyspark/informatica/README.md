# Informatica PySpark scaffold

This project intentionally follows `docs/migration/00_scaffold_and_conventions.md`.
Mappings return target-instance DataFrames and the caller owns all writes.

## Local setup

From the repository root:

```bash
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r pyspark/informatica/requirements-local.txt
export PYTHONPATH="$PWD/pyspark/informatica"
```

Java 17 is required. Run the local CSV mode with:

```bash
.venv/bin/python -m informatica_pyspark.cli --config pyspark/informatica/conf/local.yml workflow
```

Snowflake mode uses the same mapping code and is configured in
`conf/snowflake.yml`; account credentials and connector wiring are intentionally
reserved for a later milestone.

## Parity keys

The minimal unique keys in the generated Informatica baseline are:

| Target instance | Key |
|---|---|
| demo_target1_INS | ID |
| demo_target1_UPD | ID |
| demo_target2 | Member_Identifier |
| demo_target21 | Member_Identifier |
| demo_target3 | PRODUCT_ID |
| demo_target5 | ACCT_ID |
| demo_target6 | ACCT_ID |

These are checked for uniqueness before parity comparisons. Each target is
materialized separately, even where Informatica instances share a physical
target definition.
