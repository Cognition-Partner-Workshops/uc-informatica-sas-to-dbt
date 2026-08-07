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

## Snowflake milestone E

Install the local Snowflake client dependency with:

```bash
.venv/bin/pip install -r pyspark/informatica/requirements-local.txt
```

The provisioning generator is `tools/snowflake_milestone_e.py`. It reads the
private key only from the `SNOWFLAKE_PRIVATE_KEY` environment variable and
writes a temporary mode-0600 PEM outside the repository. It creates fresh
namespaced source, migrated-target, and baseline schemas only after checking
`information_schema.schemata`, loads all typed tables, materializes
`__LINE_ORDINAL` for lookup inputs and pre-existing `demo_target1`, and
generates normalized comparison views and a proof statement under ignored
`build/`.

The first real Snowflake provisioning run is recorded in
`docs/migration/snowflake_milestone_e.md`. Do not reuse its schemas for another
run; pass a fresh `--run-id`.

If Maven Central is rate-limited, provision the pinned connector artifacts
outside the repository and pass that directory to the verifier:

```bash
PYTHONPATH=pyspark/informatica .venv/bin/python \
  pyspark/informatica/tools/provision_snowflake_jars.py \
  --output /tmp/snowflake-spark-jars
PYTHONPATH=pyspark/informatica .venv/bin/python \
  pyspark/informatica/tools/snowflake_verify.py \
  --run-id <RUNID> --jars-dir /tmp/snowflake-spark-jars
```

The verifier executes the generated proof, queries Snowflake query history,
performs a Spark connector write/read round-trip, and drops its throwaway
table. Spark key-pair authentication receives the Base64-encoded PKCS8 DER
form required by the connector; the source PEM remains outside the repository.

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

Uniqueness is verified against the regenerated baseline seed, never assumed
from the target definition. `demo_target5` is unique on `ACCT_ID` only for this
seed; if a non-SB account has multiple transactions, its fallback key set is
`["ACCT_ID", "TX_ID"]`.

The pre-existing `demo_target1` state is read with an explicit schema:
`Key` is numeric (`DOUBLE`) and duplicate `ID` rows are retained with their
physical `__line_ordinal`. This preserves the DECISION-3 `Use Any Value`
fixture, which chooses highest `Key` and then highest physical ordinal.
