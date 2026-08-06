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

* `seeds/` is the source layer. Five source CSVs remain byte-for-byte copies
  of the recovered files under `legacy/informatica/data/`. The four
  lookup-state seeds are regenerated with a trailing `SEED_ROW` ordinal;
  stripping that column reproduces the legacy CSV content. `demo_target1.csv`
  is intentionally a seed because it is the pre-existing target state used as
  the mapping 2 lookup.
* `models/staging/stg_<name>.sql` is one view per seed. Ordinary staging models
  only rename/type-pass through the seed. Lookup staging models also resolve
  Informatica's multiple-match policy.
* `models/intermediate/int_<mapping_number>__<step>.sql` are mapping-step
  views. Child sessions add these.
* `models/marts/<target_instance_lowercase>.sql` are table models. Children add
  exactly the seven target instances; this shared scaffold intentionally has
  zero mart models.

Identifiers are never quoted. Write identifiers in the legacy's own casing and
let each engine fold them according to its identifier rules. This applies even
to `Key`, which remains unquoted.

## Seed type decision

Seed column types exactly mirror `tools/informatica_baseline.py`'s `load()`
definitions. This preserves the legacy source contract rather than inferring
types from CSV contents. In particular, `demo_source5` date columns and
`demo_source4.CRDT_LN` remain `VARCHAR`.

Run `python3 dbt/informatica/scripts/sync_seeds.py` to recopy and verify the
nine files. It checks the five byte-identical files directly, and checks the
four ordinal seeds both with `SEED_ROW` stripped and against the expected
`1..N` sequence. `data/abort/` is deliberately excluded.

## Lookup-order decision

Snowflake does not expose physical CSV row order, so
`scripts/sync_seeds.py` adds a trailing `SEED_ROW` ordinal to the four
lookup-state seeds. `SEED_ROW` is a `DECISION`: it makes recovered physical
file order representable in a warehouse table. The lookup ordering itself is
`RECOVERED` from the XML policies: `SEED_ROW DESC` for each `Use Last Value`
lookup, and `Key DESC, SEED_ROW DESC` for mapping 2's `Use Any Value`.
The staging models drop `SEED_ROW` from their public output.

The actual duplicate winners prove the rule matches the baseline:

* `lkp_demo_source1`, `ACCT_ID=1002`: `SEED_ROW DESC` selects the
  `ZOE ... 999 High Street ... CORP` row, which is the last seed row.
* `lkp_demo_source2`, `CUST_ID=70032`: `SEED_ROW DESC` selects the `450`
  row, which is the last seed row.
* `lkp_demo_source3`, `ACCT_ID=1002`: `SEED_ROW DESC` selects
  `DR / Debit posting last`, which is the last seed row.
* `demo_target1`, `ID=REC00002`: `Key DESC, SEED_ROW DESC` selects key `99`,
  matching the baseline's highest-key winner and physical-row tie-break rule.

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

The unmodified `tools/parity_diff.py` comparator requires `pandas<3` because
an all-NULL DATE column can be normalized differently under pandas 3. This is
an environment requirement of the comparator, not a modelling constraint.
Use the pinned interpreter with `PARITY_PYTHON=/home/ubuntu/venv-p2/bin/python
./run_parity.sh`.

After child mart models exist, run `./run_parity.sh` from the project
directory to compare the DuckDB target tables with `baseline/informatica/`.

For Snowflake evidence, run
`scripts/load_baseline_snowflake.py` to load type-matched baseline tables,
`scripts/verify_snowflake.py` for explicit row-count/MINUS/object/history
queries, and `scripts/parity_snowflake.py` for the unmodified comparator
against exported Snowflake tables. The complete evidence is recorded in
`docs/evidence/snowflake_verification.md`.
