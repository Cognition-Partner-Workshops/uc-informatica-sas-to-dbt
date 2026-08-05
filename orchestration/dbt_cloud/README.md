# dbt Cloud API objects

The faithful default is `orchestration/wf_demo_mapping.yml`. It is a
workflow-dispatch-only GitHub Actions definition kept under `orchestration/`
until the dbt project lands on `main`; moving it to `.github/workflows/` before
then would create a broken workflow.

dbt Cloud `execute_steps` stop at the first failing step, so one dbt Cloud job
cannot reproduce the legacy unconditional `Decision1` link. The JSON in this
directory is therefore the clearly-labelled recommended strict alternative,
not the faithful default.

The JSON files use placeholders for account, project, environment, and job
definition identifiers. Replace them with identifiers from the target dbt
Cloud account before posting.

The strict alternative's execute steps use named selectors:

```sh
dbt build --selector s_m_demo_mapping2 --fail-fast
dbt build --selector s_m_demo_mapping1 --fail-fast
dbt build --selector s_m_demo_mapping3 --fail-fast
```

The faithful workflow uses the same named selectors with
`--project-dir dbt/informatica --profiles-dir dbt/informatica` and deliberately
omits `--fail-fast`. Its Failed_Email and SuccessEmail steps are placeholders
with recipient `data-eng-alerts@example.com`; replace the TODO channel only
after the approved notification integration is selected.
The workflow assumes a DuckDB target and installs `dbt-duckdb`; a Snowflake
target would swap the adapter installation and profile configuration.

```sh
curl --request POST \
  --url "https://cloud.getdbt.com/api/v2/accounts/<ACCOUNT_ID>/jobs/" \
  --header "Authorization: Token <DBT_CLOUD_API_TOKEN>" \
  --header "Content-Type: application/json" \
  --data @orchestration/dbt_cloud/job_wf_demo_mapping_strict_fail_fast.json

curl --request POST \
  --url "https://cloud.getdbt.com/api/v2/accounts/<ACCOUNT_ID>/notifications/" \
  --header "Authorization: Token <DBT_CLOUD_API_TOKEN>" \
  --header "Content-Type: application/json" \
  --data @orchestration/dbt_cloud/notifications_wf_demo_mapping.json
```

The legacy scheduler is `ONDEMAND`, so the strict alternative is API/manual-
trigger only.
If the business later requests a schedule, a separate configuration could set
an explicit cron such as `0 2 * * *` (02:00 UTC); that would be new behavior,
not a claim about the legacy workflow.
