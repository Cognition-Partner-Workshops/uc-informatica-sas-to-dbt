#!/usr/bin/env bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
SCRATCH="$(mktemp -d)"
trap 'rm -rf "$SCRATCH"' EXIT

cd "$ROOT"
python3 tools/informatica_baseline.py
dbt build --project-dir dbt/informatica --profiles-dir dbt/informatica
dbt run --project-dir dbt/informatica --profiles-dir dbt/informatica \
  --select demo_target1
dbt test --project-dir dbt/informatica --profiles-dir dbt/informatica \
  --select test_demo_target1_upd_preserves_preexisting_columns

cp "$ROOT/baseline/informatica/demo_target1_INS.csv" "$SCRATCH/"
cp "$ROOT/baseline/informatica/demo_target1_UPD.csv" "$SCRATCH/"

python3 "$ROOT/tools/parity_diff.py" \
  --baseline "$SCRATCH" \
  --actual "$ROOT/dbt/informatica/dev.duckdb" \
  --schema main \
  --keys "$ROOT/tools/keys/informatica_keys.json" \
  --report "$ROOT/docs/parity/informatica_m_demo_mapping2_parity.md"
