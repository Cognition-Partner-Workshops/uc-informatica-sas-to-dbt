# Informatica Snowflake scaffold

This project stages nine frozen inputs from FSX_20261105_DB.INFA_SOURCE as
views in exactly INFA_TARGET. No mapping transformations or target marts are
implemented yet. Intermediate and mart folders reserve each mapping's scope.

## Run from the repository root

Use the existing dbt virtual environment (dbt-core 1.12, dbt-snowflake 1.10):

```sh
source ~/venv-dbt/bin/activate
```

Supply these environment variables securely in the current shell; never store
credentials in the repository:

- `SNOWFLAKE_NFR_ACCOUNT`
- `SNOWFLAKE_NFR_USER`
- `SNOWFLAKE_NFR_PRIVATE_KEY`: PEM content, not a filename
- `SNOWFLAKE_NFR_ROLE`
- `SNOWFLAKE_NFR_WAREHOUSE`: FSX_20261105_WH

```sh
unset SNOWFLAKE_HOST
dbt debug --project-dir dbt/informatica_snowflake --profiles-dir dbt/informatica_snowflake --target snowflake
dbt build --project-dir dbt/informatica_snowflake --profiles-dir dbt/informatica_snowflake --target snowflake
```

Use `--select staging` to build only the staging layer. SEED_ROW is retained on
lookup inputs and DEMO_TARGET1 to preserve physical tie ordering; staging does
not deduplicate, filter, join, trim or parse business values. Casts match the
landing contract, including VARCHAR F/T codes and date strings.

All models inherit the run tag. Staging models have per-model legacy_unit
metadata; future intermediate/mart models inherit it from their mapping folder.
