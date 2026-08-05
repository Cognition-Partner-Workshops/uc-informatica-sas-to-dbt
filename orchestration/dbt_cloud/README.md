# dbt Cloud API objects

The JSON files use placeholders for account, project, environment, and job
definition identifiers. Replace them with identifiers from the target dbt
Cloud account before posting.

The job's execute steps use named selectors:

```sh
dbt build --selector s_m_demo_mapping2 --fail-fast
dbt build --selector s_m_demo_mapping1 --fail-fast
dbt build --selector s_m_demo_mapping3 --fail-fast
```

```sh
curl --request POST \
  --url "https://cloud.getdbt.com/api/v2/accounts/<ACCOUNT_ID>/jobs/" \
  --header "Authorization: Token <DBT_CLOUD_API_TOKEN>" \
  --header "Content-Type: application/json" \
  --data @orchestration/dbt_cloud/job_wf_demo_mapping.json

curl --request POST \
  --url "https://cloud.getdbt.com/api/v2/accounts/<ACCOUNT_ID>/notifications/" \
  --header "Authorization: Token <DBT_CLOUD_API_TOKEN>" \
  --header "Content-Type: application/json" \
  --data @orchestration/dbt_cloud/notifications_wf_demo_mapping.json
```

The legacy scheduler is `ONDEMAND`, so this job is API/manual-trigger only.
If the business later requests a schedule, a separate configuration could set
an explicit cron such as `0 2 * * *` (02:00 UTC); that would be new behavior,
not a claim about the legacy workflow.
