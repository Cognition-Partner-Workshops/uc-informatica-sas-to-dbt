# Legacy Data Estate → dbt Migration

A representative legacy data estate — an **Informatica PowerCenter** workflow and a suite of
**banking SAS programs** — together with deterministic helper tools that reverse-engineer the
legacy logic into a source-to-target mapping (STM) and verify that a rewritten **dbt** project
produces identical results.

Target platform: **dbt running on DuckDB with Snowflake-compatible SQL** — fully self-contained,
no external warehouse required. The generated models are written so they can be pointed at
Snowflake with minimal changes.

## The two migration tracks

| Track | Legacy source | Deliverable |
|---|---|---|
| Informatica → dbt | `legacy/informatica/wf_demo_mapping.XML` (PowerCenter export: 3 mappings, 3 sessions, 1 workflow) | STM document + dbt models reproducing each mapping |
| SAS → dbt | `legacy/sas/programs/` (6 programs — banking: account snapshot, transaction ETL, credit-risk scoring, regulatory reporting; insurance: claims processing with hash-object lookups, policy valuation) | STM document + dbt models reproducing each program |

## Repository layout

```
legacy/
├── informatica/
│   └── wf_demo_mapping.XML        # PowerCenter repository export (source of truth)
│       # m_demo_mapping1: 3 sources, joins + lookups + aggregator + router → 3 targets
│       # m_demo_mapping2: SCD-style insert/update detection (MD5 compare, router, update strategy)
│       # m_demo_mapping3: member/subscriber validation with ABORT guards + router
└── sas/
    ├── programs/                  # unmodified legacy programs (migration source of truth)
    │   # banking: load_customer_accounts, daily_transaction_processing,
    │   #          credit_risk_scoring, monthly_regulatory_reporting
    │   # insurance: claims_processing (declare hash), policy_valuation
    ├── macros/                    # %parmv, %nobs, %lock, %export_xlsx, %sendmail
    ├── formats/banking_formats.sas
    ├── config/autoexec_local.sas  # libref contract (ORA_DW, RAW_BANK, STG_BANK, CURATED, RPT)
    └── data/csv/                  # seed data (business date 31JAN2024), deterministic generator
        # banking inputs shipped; insurance inputs (RAW_INS.POLICIES, CLAIMS,
        # PREMIUMS, CLAIMS_FEED_20240131) are synthesized by the migration tooling

tools/                             # deterministic helper tools (see tools/README.md)
docs/                              # generated STM documents land here
dbt/                               # the target dbt project (created by the migration)
.workshop/playbooks/               # the migration playbook source
```

## How a migration run works

1. **Reverse-engineer** — run the lineage extractors in `tools/` against the legacy artifacts to
   produce a machine-readable STM (`docs/stm/*.json`) and a human-readable STM document
   (`docs/stm/*.md`) capturing source → transformation → target at column/port level.
2. **Rewrite** — generate/author dbt models (staging → intermediate → marts) that implement the
   STM logic in Snowflake-compatible SQL, with schema tests.
3. **Verify** — run the deterministic baseline runner (executes the legacy semantics against the
   seed data in DuckDB) and `tools/parity_diff.py` to prove row-level equivalence between the
   legacy baseline and the dbt output.

## Prerequisites

```
python3 -m pip install duckdb dbt-duckdb pandas
```

### Informatica before-state

The Informatica worker inputs are the deterministic CSVs in
`legacy/informatica/data/`. They cover `demo_source1` through `demo_source5`, the
pre-existing `demo_target1` lookup state, and the three reconstructed lookup
CSVs (`lkp_demo_source1`, `lkp_demo_source2`, `lkp_demo_source3`). Those lookup
schemas are reconstructed from the lookup transformation ports because the tables
are not defined anywhere in the PowerCenter export; the generated STM records
that fact.

The business/run date is pinned to **31JAN2024**. `Use Last Value` lookups are
made reproducible by selecting the last physical seeded row for duplicate lookup
keys, and the pre-existing target state includes a duplicate `ID` so the
`Use Any Value` tie-break is observable. The baseline tool also exposes an
explicit `--trigger-abort` opt-in that loads a separate bad-row seed set and
hard-fails on the `ABORT()` path.

Run the before-state tools from the repository root:

```
python3 tools/informatica_lineage.py
python3 tools/informatica_baseline.py
```
