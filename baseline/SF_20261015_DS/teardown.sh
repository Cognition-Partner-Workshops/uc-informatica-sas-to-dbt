#!/usr/bin/env bash
# Drop every Snowflake object of run SF_20261015_DS. Needs SNOWFLAKE_PAT (or SNOWFLAKE_PASSWORD)
# for an ACCOUNTADMIN user in the environment. Without --yes it only lists.
set -euo pipefail
cd "$(dirname "$0")/../.."
python3 baseline/SF_20261015_DS/teardown.py --token SF_20261015_DS "$@"
