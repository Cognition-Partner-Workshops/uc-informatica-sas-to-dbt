#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/../.."
python3 tools/parity_diff.py \
  --baseline baseline/informatica \
  --actual dbt/informatica/dev.duckdb \
  --schema main \
  --keys tools/keys/informatica_keys.json \
  --report docs/parity/informatica_parity.md
