# Informatica PySpark migration

Milestone 0 supplies the runtime, connector-graph lineage, workflow scaffold, and expression
primitives. Mapping bodies remain intentionally stubbed until their implementation milestones.

## Local

```bash
source /home/ubuntu/venvs/pyspark-informatica/bin/activate
PYTHONPATH=pyspark/informatica python -m informatica_pyspark.cli lineage \
  --out docs/pyspark/lineage.md
PYTHONPATH=pyspark/informatica python -m informatica_pyspark.cli run-workflow \
  --io local --source-variant normal --target-dir out/pyspark/local
```

Use `--source-variant abort` for the deterministic abort fixture. Mapping commands use
`run-mapping m_demo_mappingN`.

## Snowflake

Install the pinned requirements and provide the Snowflake account, user, role, warehouse,
database, source schema, target schema, and private-key configuration through the eventual
runner configuration. The Snowflake adapter uses the `snowflake` Spark data source and never
changes mapping transformation code.

## Verification

The committed parity evidence at `docs/parity/informatica_pyspark_parity.md` is re-runnable:
regenerate it with the baseline, workflow, and parity commands below; the generated file is
expected to be committed.

```bash
pytest pyspark/informatica/tests
python tools/informatica_baseline.py
PYTHONPATH=pyspark/informatica python -m informatica_pyspark.cli run-workflow \
  --io local --target-dir out/pyspark/local
python pyspark/informatica/scripts/run_parity.py --actual out/pyspark/local
python pyspark/informatica/scripts/run_parity.py --help
```
