#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"
target_args=()
if [[ "${1:-}" == "--target" ]]; then
  target_args=(--target "${2:?missing target name}")
fi

dbt seed "${target_args[@]}"
dbt build --selector session_s_m_demo_mapping2 "${target_args[@]}"
dbt build --selector session_s_m_demo_mapping1 "${target_args[@]}"
dbt build --selector session_s_m_demo_mapping3 "${target_args[@]}"
