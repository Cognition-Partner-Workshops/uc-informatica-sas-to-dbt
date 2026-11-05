# infa_m23 — DuckDB conversion

Run from the repository root (Python 3.10+):

```sh
PROJECT=dbt/informatica_snowflake/m_demo_mapping2_3
python -m pip install -r requirements.txt -r "$PROJECT/requirements.txt"
export INFA_DUCKDB_PATH="$PWD/$PROJECT/target/infa.duckdb"
python "$PROJECT/load_inputs.py"
dbt build --project-dir "$PROJECT" --profiles-dir "$PROJECT"
python tools/parity_nfr.py --token INFA_M23 --duckdb "$INFA_DUCKDB_PATH" --schema main --report reports/infa_m23.md
pytest -q
pytest -q "$PROJECT/tests/test_conversion.py"
ruff check tools tests
```

The profile and loader default to `target/infa.duckdb` relative to the working
directory when INFA_DUCKDB_PATH is unset. Use an absolute environment path to
avoid ambiguity. Inputs are isolated in `infa_src_infa_m23`; only the four
target tables are materialized in `main`. Loading replaces only this group's
three input tables and preserves physical ordering as SEED_ROW. Empty CSV
fields become SQL NULL; literal null markers and F/T codes remain VARCHAR.
No Snowflake connection is used.

## Legacy decisions

- m_demo_mapping2 looks up the static demo_target1 pre-state, not prior dbt
  outputs. The accepted Use Any Value convention selects the highest numeric
  Key per ID, breaking ties with the last physical seeded row.
- Unmatched rows take the insert path; the sequence's current value is 57,
  increment 1. Deterministic ID/seed ordering assigns 57 onward on each rebuild.
- Matched rows take DD_UPDATE. The legacy AES-decrypted lookup value and
  source MD5 occupy incomparable value spaces; as in the accepted baseline,
  all matched rows update, even when their descriptive fields are unchanged.
  This is fixture semantics, not a new cryptographic implementation.
- Insert/update outputs are separate operation payloads, not a merged final
  target state. Unconnected target columns are typed SQL NULL. Audit values
  are IDWUSER and the pinned business date 2024-01-31.
- m_demo_mapping3 filters null Member_Type_Code before expression evaluation,
  aborts on a real SQL NULL relationship label in any qualifying row, and
  routes on SQL NULL social-security number. A literal textual null label is
  passed through. Both router branches retain the original target columns.

The parity tool currently requires --token even offline and checks all seven
baseline targets. Therefore the exact command without --token fails argument
parsing; with the dummy token above it reports four GREEN matches but exits 1
and prints Full match: False because the three sibling targets are absent.
This does not imply a difference in these four models. The generated JSON is
not committed; the Markdown report contains per-target row counts.
