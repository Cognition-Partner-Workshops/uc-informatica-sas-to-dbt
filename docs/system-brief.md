# System brief: legacy data estate → dbt

## Purpose

This is a representative migration toolkit for Informatica PowerCenter and SAS analytics, intended to document legacy transformations and verify equivalent dbt outputs. Its business examples cover customer accounts, transactions, credit risk, regulatory reporting, insurance claims and policy valuation. Intended users are migration/data-engineering teams (inference from the documented workflow), rather than customers using an application. [README](../README.md#L3-L17) [Migration workflow](../README.md#L46-L55)

## Architecture

The implementation is command-line Python and SQL around legacy PowerCenter XML and SAS programs. Lineage extractors produce JSON/Markdown source-to-target mappings; baseline runners reimplement legacy semantics in DuckDB and export CSVs; parity tools compare those answers with rewritten outputs. Dependencies include pandas, DuckDB, PyArrow and the Snowflake connector. [Tool contracts](../tools/README.md#L1-L25) [SAS baseline](../tools/sas_baseline.py#L1-L26) [Dependencies](../requirements.txt)

The documented target is dbt on DuckDB using Snowflake-compatible SQL; dbt authoring is a migration deliverable, not proof of a completed replacement. Execution is local batch tooling, with an optional Snowflake fixture path that provisions a run-scoped database and warehouse and uploads Parquet through staged `PUT`/`COPY INTO` commands. GitHub Actions runs an offline fixture/test/lint job on pushes and PRs. [Target and rewrite](../README.md#L8-L10) [Deliverable](../README.md#L40-L55) [Cloud loader](../tools/sf_nfr_landing.py#L68-L104) [CI](../.github/workflows/warehouse-fixture.yml#L1-L16)

## Data stores

Seed inputs and accepted baseline outputs are CSV files; SAS baselines use in-memory DuckDB, while the raw loader can persist a DuckDB database. Cloud landing uses `INFA_SOURCE`, `INFA_BASELINE` and initially empty `INFA_TARGET` schemas, with local Parquet intermediates. A separate frozen demo documents combined SAS/Informatica source and baseline schemas. [CSV contracts](../tools/README.md#L5-L20) [DuckDB](../tools/sas_baseline.py#L710-L720) [Persistent loader](../tools/sas_load_raw.py#L60-L68) [Landing](../tools/sf_nfr_landing.py#L78-L104) [Frozen demo](../baseline/SF_20261015_DS/README.md#L5-L14)

## Integrations

Inbound contracts are exported PowerCenter XML, SAS source and seeded files. The local SAS configuration substitutes directory-backed libraries for Oracle/Teradata engines; these stand-ins are not evidence of live warehouse connectivity. [Inputs](../tools/README.md#L5-L20) [Local configuration](../legacy/sas/config/autoexec_local.sas#L1-L10) [Library stand-ins](../legacy/sas/config/autoexec_local.sas#L59-L62)

Outbound integrations include Snowflake via its Python connector and local Markdown/JSON reconciliation reports. The NFR path reads environment-supplied account/user/private-key configuration and uses JWT authentication, parsing the key in memory; the older Snowflake parity path uses environment-supplied password authentication. Licence reporting labels retirement only for covered objects with GREEN results, and costs are explicitly synthetic. [JWT configuration](../tools/sf_nfr_common.py#L26-L37) [Password configuration](../tools/parity_snowflake.py#L33-L46) [Reports](../tools/parity_nfr.py#L129-L151) [Licence gate](../tools/licence_status.py#L11-L25)

## Top 3 operational risks

Business impacts below are inferences; mitigations are recommendations.

1. **High — Fixture parity is not production assurance.** Baselines emulate semantics on a fixed business date; lookup schemas are reconstructed and SAS wall-clock columns excluded. Matching these fixtures could still miss production differences affecting balances, risk or regulatory reporting. **Mitigation:** independently reconcile real legacy-engine outputs across representative dates and edge cases before cutover. [Baseline assumptions](../tools/informatica_baseline.py#L1-L19) [Reconstructed lookups](../README.md#L65-L78) [SAS exclusions](../tools/sas_baseline.py#L17-L26)

2. **High — Cloud cutover is not covered by CI.** The sole workflow runs offline, and landing deliberately leaves the target empty. A green PR therefore does not demonstrate a working dbt build or live authentication/loading/reconciliation, risking migration delays or premature retirement decisions. **Mitigation:** require a controlled end-to-end Snowflake/dbt rehearsal and full reconciliation before approving retirement. [CI scope](../.github/workflows/warehouse-fixture.yml#L1-L16) [Empty target](../tools/sf_nfr_landing.py#L128-L132) [Reconciliation gate](../tools/parity_nfr.py#L138-L151)

3. **Med — Shared-run data loss and cleanup exposure.** Landing configures zero-day retention; expiry is an object comment, while teardown requires explicit execution and `--all` drops the shared database/warehouse, including other-track schemas. Mistakes could destroy another team's rehearsal evidence or leave resources behind. **Mitigation:** isolate runs, schedule verified cleanup and require explicit ownership approval for shared-resource teardown. [Retention/expiry](../tools/sf_nfr_landing.py#L68-L96) [Teardown scope](../tools/sf_nfr_teardown.py#L9-L39)
