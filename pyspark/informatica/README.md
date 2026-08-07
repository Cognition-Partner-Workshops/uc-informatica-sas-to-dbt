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
