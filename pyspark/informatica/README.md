# Informatica PySpark scaffold

Run from the repository root with the package directory on `PYTHONPATH`:

```bash
export PYTHONPATH="$PWD/pyspark/informatica"
python -m informatica_pyspark.cli run-workflow \
  --business-date 2024-01-31 --io local --out-dir out/
```

The mapping modules are scaffold stubs until their milestones are implemented.
After implementation, compare outputs with the legacy baseline:

```bash
python tools/parity_diff.py --baseline baseline/informatica --actual out \
  --keys tools/keys/informatica_keys.json \
  --report docs/informatica_pyspark/parity_report.txt
```

Run the hard-failure fixture with its override directory:

```bash
python -m informatica_pyspark.cli run-mapping m_demo_mapping3 \
  --business-date 2024-01-31 --io local \
  --data-dir legacy/informatica/data/abort --out-dir out_abort/
```

## Re-run against Snowflake

Snowflake runs require the Spark Snowflake connector jar and JDBC 4.0.2:

```text
/home/ubuntu/spark-jars/spark-snowflake_2.12-3.2.1-spark_3.5.jar
/home/ubuntu/spark-jars/snowflake-jdbc-4.0.2.jar
```

Set `SNOWFLAKE_PRIVATE_KEY` in the environment without writing the key to disk.
The default jar pair can be replaced with `INFORMATICA_SPARK_JARS`.

Create fresh source and baseline schemas with the loader:

```bash
python pyspark/informatica/scripts/snowflake_load.py \
  --source-schema SOURCE_INFORMATICA_<ts> \
  --baseline-schema BASELINE_INFORMATICA_<ts> \
  --data-dir legacy/informatica/data \
  --baseline-dir baseline/informatica
```

Then run the workflow into a matching fresh target schema:

```bash
python -m informatica_pyspark.cli run-workflow \
  --business-date 2024-01-31 --io snowflake \
  --run-schema PYSPARK_INFORMATICA_<ts> \
  --src-schema SOURCE_INFORMATICA_<ts>
```

The captured warehouse proof for the validated run is in
`docs/informatica_pyspark/snowflake_proof.md`.
