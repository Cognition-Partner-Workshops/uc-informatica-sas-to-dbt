---
name: warehouse-exit-informatica
description: Land Informatica fixture inputs in a token database, reconcile converted targets and gate synthetic licence retirement.
---

# Informatica warehouse exit mechanics

The source of truth is legacy/informatica/wf_demo_mapping.XML. The mappings read
demo_source1 through demo_source5, the demo_target1 pre-state and the lkp CSVs in
legacy/informatica/data/. Keep legacy/ and baseline/SF_20261015_DS/ unchanged.
Install dependencies with `python3 -m pip install -r requirements.txt`.

To check deterministic seed regeneration, run
`python3 legacy/informatica/data/generate_seed_data.py` and inspect
`git diff --exit-code -- legacy/informatica/data` before proceeding.
Run `python3 tools/informatica_baseline.py`, then
`git diff --exit-code -- baseline/informatica`.
Never edit the seed or accepted baseline to make a target diff green.
The baseline uses business date 2024-01-31 and the existing lookup tie conventions.

Preview `python3 tools/sf_nfr_landing.py --token TOKEN --dry-run`.
Tokens use uppercase letters, digits and underscores. Live authentication
reads SNOWFLAKE_NFR_ACCOUNT, SNOWFLAKE_NFR_USER and SNOWFLAKE_NFR_PRIVATE_KEY
(PEM text), with optional SNOWFLAKE_NFR_ROLE and SNOWFLAKE_NFR_WAREHOUSE.
The connector removes SNOWFLAKE_HOST and parses the key in memory.
Keep credentials out of files and logs.

The loader creates TOKEN_DB.INFA_SOURCE and TOKEN_DB.INFA_BASELINE with an empty
TOKEN_DB.INFA_TARGET. TOKEN_DB and TOKEN_WH can be shared with the Teradata track.
`--expires ISO` sets the run comment; the default is 2026-11-12T23:59:00Z.
Explicit reload uses `--reload`, optionally with
`--tables INFA_SOURCE.DEMO_SOURCE1 INFA_BASELINE.DEMO_TARGET5`.
SEED_ROW preserves physical lookup ordering and duplicate pre-state rows.
The landing tool keeps one-letter F/T codes as VARCHAR and uses logical Parquet types.

Write converted models under dbt/informatica_snowflake/ and build into
TOKEN_DB.INFA_TARGET. Preserve every baseline target name, column and key.
Run `python3 tools/parity_nfr.py --token TOKEN --report reports/informatica.md`
to compare INFA_TARGET against INFA_BASELINE with the existing parity normalisation.
The command writes Markdown and JSON and exits 0 only for a full match.
An offline target copy uses `--duckdb PATH --schema main` and local baseline CSVs.
The existing tools/parity_snowflake.py connection path remains unchanged.

Run `python3 tools/licence_status.py --report reports/informatica.json --output reports/licence.md`.
The synthetic ledger marks a line RETIRED only when every covered target is green;
absent or failing targets keep the line BLOCKED. Costs are synthetic round numbers.

Preview `python3 tools/sf_nfr_teardown.py --token TOKEN --dry-run` before cleanup.
The default teardown drops only INFA_SOURCE, INFA_BASELINE and INFA_TARGET.
`--all` also drops the shared database, including Teradata schemas, and warehouse.
Teardown lists leftovers matching the token in either name or comment. Shared
Teradata objects are expected in the default leftover listing.
Run `pytest -q` and `ruff check tools tests` for offline checks.
