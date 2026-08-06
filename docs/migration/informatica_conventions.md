# Informatica migration conventions

## Scope and recovered-versus-decision convention

This project migrates the three mappings and the `wf_demo_mapping` workflow
recovered from `legacy/informatica/wf_demo_mapping.XML`. Every model must carry
a header comment block for each non-trivial column:

* `RECOVERED` identifies the XML element and expression that supplied the rule.
* `DECISION` identifies a portability or determinism choice made here and the
  alternative rejected.

Email tasks are out of scope: dbt has no equivalent notification task.

## Layers and names

The dbt project lives at `dbt/informatica/` and is named
`informatica_migration`.

* `seeds/` is the source layer. These nine CSVs are byte-for-byte copies of
  the recovered files under `legacy/informatica/data/`. `demo_target1.csv` is
  intentionally a seed because it is the pre-existing target state used as
  the mapping 2 lookup.
* `models/staging/stg_<name>.sql` is one view per seed. Ordinary staging models
  only rename/type-pass through the seed. Lookup staging models also resolve
  Informatica's multiple-match policy.
* `models/intermediate/int_<mapping_number>__<step>.sql` are mapping-step
  views. Child sessions add these.
* `models/marts/<target_instance_lowercase>.sql` are table models. Children add
  exactly the seven target instances; this shared scaffold intentionally has
  zero mart models.

Identifiers are unquoted except where a reserved identifier requires quoting.
The `Key` seed column is referenced as `"KEY"` in uppercase where necessary.

## Seed type decision

Seed column types exactly mirror `tools/informatica_baseline.py`'s `load()`
definitions. This preserves the legacy source contract rather than inferring
types from CSV contents. In particular, `demo_source5` date columns and
`demo_source4.CRDT_LN` remain `VARCHAR`.

Run `python3 dbt/informatica/scripts/sync_seeds.py` to recopy and verify the
nine files. `data/abort/` is deliberately excluded.

## Lookup-order decision

Snowflake does not expose physical CSV row order, so the staging layer uses a
deterministic descending lexicographic ordering of stable data columns to
stand in for physical order. Each model puts the column that distinguishes its
known final physical row first, followed by deterministic tie-breakers. The
ordering is explicit in each `row_number()` window; no unordered window is
used. This is a `DECISION` (the rejected alternative is relying on file/scan
order).

The actual duplicate winners prove the rule matches the baseline:

* `lkp_demo_source1`, `ACCT_ID=1002`: `CUST_ADDR DESC` selects the
  `ZOE ... 999 High Street ... CORP` row, which is the last seed row.
* `lkp_demo_source2`, `CUST_ID=70032`: `CRDT_SCORE DESC` selects the `450`
  row, which is the last seed row.
* `lkp_demo_source3`, `ACCT_ID=1002`: `TX_TYPE_DESC DESC` selects
  `DR / Debit posting last`, which is the last seed row.
* `demo_target1`, `ID=REC00002`: `"KEY" DESC` selects key `99`; all remaining
  columns are deterministic tie-breakers, matching the baseline's highest-key
  winner (and its last-row tie-break rule).

## Workflow equivalence

The recovered workflow is sequential:

`Start → s_m_demo_mapping2 → Decision1 → s_m_demo_mapping1 →
Decision2(condition=1) → s_m_demo_mapping3 → Decision3 → SuccessEmail`.

Each decision's zero branch goes to its failed email task. `Failed_Email2`
then goes to `Control`, which aborts the workflow. dbt tags every model with
`informatica` and its recovered session tag. `run_workflow.sh` runs the three
session selectors in sequence with `set -e`, so a failed build stops all
downstream sessions.

## Running

From `dbt/informatica/`:

```bash
source /home/ubuntu/venv-dbt/bin/activate
dbt seed --target dev
dbt build --target dev
./run_workflow.sh
./run_workflow.sh --target snowflake
```

Snowflake requires `SNOWFLAKE_PRIVATE_KEY_PATH`; the key is never committed.
The schema defaults to `DBT_INFORMATICA_20260806` and can be overridden with
`SNOWFLAKE_SCHEMA`.

After child mart models exist, run `./run_parity.sh` from the project
directory to compare the DuckDB target tables with `baseline/informatica/`.
