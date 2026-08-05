# Deterministic Helper Tools

Contract for the migration helper tools. Every tool is plain Python 3 (stdlib + `duckdb` +
`pandas`), deterministic, and runnable from the repo root.

## Informatica track

| Tool | Input | Output |
|---|---|---|
| `informatica_lineage.py` | `legacy/informatica/wf_demo_mapping.XML` | `docs/stm/informatica_stm.json` + `docs/stm/informatica_stm.md` — per mapping: sources, targets, transformations, port-level lineage (target column → expression chain → source column), lookup conditions, router groups, SQL overrides |
| `informatica_baseline.py` | XML + `legacy/informatica/data/` seed CSVs | `baseline/informatica/<target>.csv` — deterministic execution of each mapping's semantics in DuckDB |

## SAS track

| Tool | Input | Output |
|---|---|---|
| `sas_lineage.py` | `legacy/sas/programs/*.sas` | `docs/stm/sas_stm.json` + `docs/stm/sas_stm.md` — per program: input librefs/datasets, output datasets, step-level lineage (PROC SQL joins, DATA-step derivations, formats, macro parameters) |
| `sas_baseline.py` | programs' semantics + `legacy/sas/data/csv/` | `baseline/sas/<dataset>.csv` — deterministic execution of the legacy program semantics in DuckDB (run date 31JAN2024) |

## Shared

| Tool | Input | Output |
|---|---|---|
| `parity_diff.py` | `--baseline <dir> --actual <duckdb path or dir> --keys <spec>` | `docs/parity/<track>_parity.md` — row counts, column-by-column compares (numeric tolerance 1e-6, date normalization), per-key row diffs; exit code 0 only on full parity |

## Rules

- No network access, no randomness, no wall-clock dependence (run date is pinned to 31JAN2024).
- Baselines implement the *legacy semantics as documented in the STM* — if the STM is wrong, the
  parity diff against the dbt build will surface it.
- Tools must be idempotent and safe to re-run.


### Informatica before-state details

Seeds live under `legacy/informatica/data/` and use the pinned business date
31JAN2024. The three lookup schemas are reconstructed from the lookup
transformation LOOKUP ports; they are not exported table definitions. For
repeatability, `Use Last Value` lookup ties select the last physical seeded row,
while the pre-existing target state uses the highest seeded key for the duplicate
`ID` so the `Use Any Value` tie-break is observable. The baseline script has an
explicit `--trigger-abort` opt-in that swaps in a separate bad-row seed set and
hard-fails on the `ABORT()` path. The lineage tool records connector-based port
lineage, including positional SQL override bindings and unconnected `:LKP.`
calls.
