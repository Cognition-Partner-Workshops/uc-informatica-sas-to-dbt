#!/usr/bin/env bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
SCRATCH="$(mktemp -d)"
trap 'rm -rf "$SCRATCH"' EXIT

cd "$ROOT"
python3 tools/informatica_baseline.py
dbt build --target snowflake --project-dir dbt/informatica --profiles-dir dbt/informatica

cp "$ROOT/baseline/informatica/demo_target1_INS.csv" "$SCRATCH/"
cp "$ROOT/baseline/informatica/demo_target1_UPD.csv" "$SCRATCH/"

python3 "$ROOT/tools/parity_diff.py" \
  --baseline "$SCRATCH" \
  --actual snowflake \
  --schema "${SNOWFLAKE_SCHEMA:?SNOWFLAKE_SCHEMA must be set}" \
  --keys "$ROOT/tools/keys/informatica_keys.json" \
  --report "$ROOT/docs/parity/informatica_m_demo_mapping2_snowflake_parity.md"
