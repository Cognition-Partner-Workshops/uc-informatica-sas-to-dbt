Playbook: Legacy ETL (Informatica / SAS) → dbt Migration with Parity Verification

## Overview
Reverse-engineer a legacy ETL artifact (an Informatica PowerCenter XML export or a suite of SAS
programs) in `Cognition-Partner-Workshops/uc-informatica-sas-to-dbt` into a column-level
source-to-target mapping (STM), rewrite the logic as a dbt project (Snowflake-compatible SQL,
executed on DuckDB), and prove row-level parity between a deterministic baseline of the legacy
semantics and the dbt build.

## What's Needed From User
- Which track to migrate: `informatica` (legacy/informatica/wf_demo_mapping.XML) or `sas`
  (legacy/sas/programs/*.sas)
- Optional: subset of mappings/programs if not migrating the whole track

## Procedure
1. Install prerequisites: `python3 -m pip install duckdb dbt-duckdb pandas`
2. Read the legacy artifacts for the chosen track (`legacy/informatica/` or `legacy/sas/`) and the
   tool contract in `tools/README.md`
3. Run the track's lineage extractor (`tools/informatica_lineage.py` or `tools/sas_lineage.py`) to
   generate the STM into `docs/stm/` (JSON + Markdown); review the STM against the legacy source
   and correct the extractor if any transformation is missing or wrong
4. Run the track's baseline runner (`tools/informatica_baseline.py` or `tools/sas_baseline.py`) to
   materialize the legacy-semantics outputs into `baseline/<track>/` from the seed data (business
   date pinned to 31JAN2024)
5. Build the dbt project under `dbt/` (profile: dbt-duckdb): one staging model per legacy source,
   intermediate models for transformation steps, mart models matching each legacy target —
   Snowflake-compatible SQL only (no DuckDB-only syntax)
6. Add dbt schema tests (not_null/unique on keys, accepted_values on coded columns) mirroring the
   STM's key and domain constraints
7. Run `dbt build` and fix failures until the project builds green
8. Run `tools/parity_diff.py` comparing `baseline/<track>/` against the dbt output tables; iterate
   on the dbt models until the diff reports full parity (exit code 0)
9. Commit the STM docs, dbt project, and parity report (`docs/parity/`); open a PR titled
   `<track>: STM + dbt migration with verified parity`

## Specifications
- STM captures every target column's lineage: source column(s), transformation expression chain,
  lookups/joins with conditions, filters/router groups, aggregations
- dbt build completes with all schema tests passing
- `tools/parity_diff.py` exits 0: identical row counts and values (numeric tolerance 1e-6) for
  every legacy target
- PR contains: `docs/stm/*`, `dbt/*`, `docs/parity/*` and no edits to `legacy/`

## Advice and Pointers
- The legacy code under `legacy/` is the source of truth — never modify it to make parity pass
- Informatica: port-level lineage lives in CONNECTOR elements; watch for SQL overrides in Source
  Qualifiers, MD5-based change detection, router groups, and :LKP expressions
- SAS: watch for PROC FORMAT-driven recodes, %MACRO parameters defaulting to the run date, hash
  object lookups in claims_processing, and RETAIN/BY-group logic that needs window functions
- Insurance seed inputs may not exist yet — synthesize them deterministically (fixed seed) under
  `legacy/sas/data/csv/raw_ins/` consistent with the columns the programs read

## Forbidden Actions
- Do not modify anything under `legacy/` except adding missing seed data directories
- Do not weaken `tools/parity_diff.py` tolerances or skip targets to force a green result
- Do not use DuckDB-only SQL constructs in dbt models
