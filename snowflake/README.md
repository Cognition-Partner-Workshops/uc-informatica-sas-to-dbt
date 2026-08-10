# Snowflake milestone 5 proof

This directory contains the reproducible Snowflake source load, baseline load, proof
queries, and the captured warehouse result in `PROOF.md`.

## Fixed run

The captured run uses database `DEVIN_MIGRATION_DEMO` and:

```text
RUN_ID=20260809T234500Z
SOURCE_SCHEMA=SOURCE_INFORMATICA_20260809T234500Z
TARGET_SCHEMA=PYSPARK_INFORMATICA_20260809T234500Z
BASELINE_SCHEMA=BASELINE_INFORMATICA_20260809T234500Z
```

The loader checks `information_schema.schemata` before creating the three schemas.
It refuses to continue if any of them already exists. The schemas are intentionally
left standing as run evidence.

## Environment

Use the pinned virtual environment:

```bash
source /home/ubuntu/venvs/pyspark-informatica/bin/activate
```

Snowflake authentication uses key-pair authentication. Set the connection variables
without putting credentials in this repository:

```bash
export SNOWFLAKE_ACCOUNT='YD76133.us-east-2.aws'
export SNOWFLAKE_USER='devin_demo'
export SNOWFLAKE_ROLE='devin_migration_demo'
export SNOWFLAKE_WAREHOUSE='devin_demo_wh'
# SNOWFLAKE_PRIVATE_KEY contains the PEM contents supplied by the org secret.
export SNOWFLAKE_PRIVATE_KEY='-----BEGIN PRIVATE KEY-----...'
export SNOWFLAKE_PRIVATE_KEY_PATH='/home/ubuntu/.snowflake/devin_demo.pem'
```

When starting from the `SNOWFLAKE_PRIVATE_KEY` environment value, write it outside
the repository without printing it:

```bash
umask 077
printf '%s' "$SNOWFLAKE_PRIVATE_KEY" > "$SNOWFLAKE_PRIVATE_KEY_PATH"
chmod 600 "$SNOWFLAKE_PRIVATE_KEY_PATH"
```

The private-key value is written to the PEM path outside the repository with mode
`600`. The Spark adapter converts that PEM to base64 PKCS8 DER in memory. Neither
the PEM nor the converted key belongs in a committed file.

The cached Spark jars are:

```text
net.snowflake:spark-snowflake_2.12:3.2.1-spark_3.5
  spark-snowflake_2.12-3.2.1-spark_3.5.jar
  sha256=776cd7a1f6230eb3c11508be50ec4bb0f0a7ff08034183a688da7aef792b0db1

net.snowflake:snowflake-jdbc:4.0.2
  snowflake-jdbc-4.0.2.jar
  sha256=8447eff0cf04cd327ab6b6f642a3a21ac2c1c2f2ce442953a11f5cf2b0fcd4bb
```

They are cached under `~/.cache/informatica-pyspark/jars`.

## End-to-end order

From the repository root:

```bash
python tools/informatica_baseline.py
python snowflake/load_sources.py

PYTHONPATH=pyspark/informatica \
python -m informatica_pyspark.cli run-workflow \
  --io snowflake \
  --source-variant normal \
  --account "$SNOWFLAKE_ACCOUNT" \
  --user "$SNOWFLAKE_USER" \
  --role "$SNOWFLAKE_ROLE" \
  --warehouse "$SNOWFLAKE_WAREHOUSE" \
  --database DEVIN_MIGRATION_DEMO \
  --source-schema SOURCE_INFORMATICA_20260809T234500Z \
  --target-schema PYSPARK_INFORMATICA_20260809T234500Z \
  --baseline-schema BASELINE_INFORMATICA_20260809T234500Z \
  --private-key-path "$SNOWFLAKE_PRIVATE_KEY_PATH"

python snowflake/load_baselines.py
python snowflake/run_proof.py
```

`load_baselines.py` verifies every baseline CSV header against the corresponding
migrated table's exact ordered column list, creates each baseline table with `LIKE`,
then uses `PUT` and `COPY INTO` with empty fields loaded as `NULL`.

The SQL files can also be run individually in order:

```text
01_objects.sql
02_row_counts.sql
03_checksums.sql
04_minus.sql
05_query_history.sql
06_verdict.sql
```

`06_verdict.sql` is a single copy-pasteable statement. `run_proof.py` executes all
six SQL files and writes the captured result rows, together with schema/table
evidence and three migrated-target samples, to `PROOF.md`.

The transformation demonstration SQL and its captured warehouse output are documented
in [`TRANSFORMATIONS.md`](TRANSFORMATIONS.md).
