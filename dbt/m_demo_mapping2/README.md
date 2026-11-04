# m_demo_mapping2: account dimension on Snowflake

This is the general-ledger account dimension mapping in the PowerCenter XML:
`demo_source1` contains account descriptions and GL short names; `LKPTRANS`
looks up the pre-existing `demo_target1` by `ID`. The other mappings handle
transactions/products and member/subscriber records, not this dimension.

## Execution contract

- Business date is frozen to **2024-01-31**.
- `WH_INFA_ACCTDIM` and the database/schemas already exist. No infrastructure is provisioned.
- `SFNFR_20261104.INFA_ACCTDIM_SRC_SFNFR_20261104`: incoming `DEMO_SOURCE1`
  (7 rows) and pre-existing `DEMO_TARGET1` (5 physical rows, including a duplicate ID).
- `SFNFR_20261104.INFA_ACCTDIM_LEGACY_SFNFR_20261104`: deterministic baseline outputs.
- `SFNFR_20261104.INFA_ACCTDIM_SF_SFNFR_20261104`: all 11 dbt models, without custom-schema prefixing.
- Profile `snowflake` reads credentials only from `SFNFR_ACCOUNT`, `SFNFR_USER`,
  `SFNFR_ROLE`, `SFNFR_PRIVATE_KEY`. The PEM stays in the environment, never a file.
- Do not override the profile's warehouse/database/schema defaults for this run.

From the repository root, after binding those four secrets securely:

```sh
uv venv ~/sfenv
uv pip install --python ~/sfenv/bin/python snowflake-connector-python pandas duckdb cryptography
uv venv ~/dbtenv
uv pip install --python ~/dbtenv/bin/python dbt-snowflake
~/sfenv/bin/python tools/informatica_account_dim_snowflake.py load
~/dbtenv/bin/dbt build --project-dir dbt/m_demo_mapping2 --profiles-dir dbt/m_demo_mapping2 --target snowflake
~/sfenv/bin/python tools/informatica_account_dim_snowflake.py parity
```

The loader runs `tools/informatica_baseline.py` on the unmodified CSV seeds,
loads explicitly typed SRC tables, then replays its unchanged `mapping2()`
function from those exact Snowflake SRC rows. The replay must be byte-identical
to the seed baseline before LEGACY is loaded. Snowflake CSV exports feed the
unchanged `tools/parity_diff.py`; canonical Snowflake keyed hashes, multiset
EXCEPT and L2 profiles provide independent checks. Numeric tolerance remains 1e-6.
Parity generates Markdown and JSON evidence under `docs/parity/`.

This reference is the supplied deterministic DuckDB baseline, **not** an actual
PowerCenter runtime execution. Parity proves equivalence to that documented contract.

## Transformation correspondence

| XML | dbt intermediate suffix | Behavior |
|---|---|---|
| SQ_demo_source1 | sq_demo_source1 | Unfiltered source projection |
| LKPTRANS | lkptrans | Highest dimension key, last physical row for ties |
| EXPTRANS | exptrans | Lookup on ID, branch flags and frozen audit fields |
| RTRTRANS | rtrtrans_insert / rtrtrans_update | Branch filters |
| SEQTRANS | seqtrans | 57 + zero-based ID-ordered insert ordinal |
| UPDTRANS | updtrans | DD_UPDATE payload, not an actual merge |

The XML compares `AES_DECRYPT(...)` with `MD5(...)`, not two MD5 values.
The supplied baseline consequently marks every lookup-matched row Update;
we preserve that behavior even for unchanged attributes or a NULL source attribute.
The derived `MD5_TGT` is observable in the intermediate view but not a target port;
target parity does not validate an AES decryption result.

Unconnected `ACTIVE_FLAG`, `START_DATE`, `END_DATE` stay NULL in both outputs.
Insert `UPDATED_*` and update `CREATED_*` also stay NULL. These are two target
payloads, not a reconstructed SCD2 dimension. Sequence numbering is deliberately
replayable, not a persistent production surrogate-key allocator.

Staging does casts/renames only. Intermediate views mirror the XML transformations;
mart tables keep all 14 target columns in legacy order (uppercase SQL identifiers).
Every model inherits `RUN:SFNFR_20261104` and `meta.legacy_unit=m_demo_mapping2`.
Tests cover mart ID uniqueness/non-nullness, lookup relationships, coded domains,
branch conservation, sequence values, selected lookup keys and unconnected NULLs.
Unit fixtures exercise the matched-but-unchanged anomaly and lookup tie-breaking.

Lineage: `docs/stm/m_demo_mapping2_stm.md` and `.json`.
Evidence: `docs/parity/m_demo_mapping2_snowflake_parity.md` and `.json`.
