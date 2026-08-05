# `wf_demo_mapping` orchestration mapping

This document covers the orchestration layer only. It does not define dbt
models or claim that the model projects are reconciled on `main`.

The source workflow declaration identifies `wf_demo_mapping`, PowerCenter
server `IDW_PCINTG01`, `SUSPEND_ON_ERROR = NO`, and
`REUSABLE_SCHEDULER = NO` (legacy XML lines 1132-1134). Its scheduler is
`ONDEMAND` (lines 1133-1134).

## Legacy defect: unconditional Decision1 link and asymmetric Stop parent

The legacy graph must be reproduced before it is changed:

* `Decision1` evaluates `$s_m_demo_mapping2.Status = 1` (lines 1158-1159).
* A failed Decision1 condition routes to `Failed_Email1` via
  `$Decision1.Condition = 0` (line 1467).
* `Failed_Email1` has no `Control` downstream.
* The link from `Decision1` to `s_m_demo_mapping1` has no condition (line
  1470), so step 2 runs even when step 1 fails.
* `Start → s_m_demo_mapping2` is unconditional (line 1471).
* `Failed_Email2 → Control` is unconditional (line 1468), and `Control` has
  `Control Option = "Stop parent"` (lines 1152-1153). Therefore, only a
  step-2 failure stops the parent workflow.
* `Decision2.Condition = 1 → s_m_demo_mapping3` is line 1469.
* `Decision3.Condition = 1 → SuccessEmail` and
  `Decision3.Condition = 0 → Failed_Email3` are lines 1466 and 1475.
  `Failed_Email3` has no Control downstream.

The default workflow in `orchestration/wf_demo_mapping.yml` reproduces this
asymmetry: step 1 uses `continue-on-error: true`, its failure notification
fires, and step 2 runs unconditionally. A step-2 failure is notified and
leaves the workflow failed; step 3 runs only after step 2 succeeds.
Notification steps are placeholders, not an invented mail integration.
The workflow is intentionally kept under `orchestration/`, rather than
`.github/workflows/`, until the dbt project lands on `main`; it would be
broken if activated today because `main` has no reconciled dbt project. Move
it to `.github/workflows/` at that point.
The workflow assumes a DuckDB target and installs `dbt-duckdb`; a Snowflake
target would swap the adapter installation and profile configuration.

The recommended follow-up is the strict dbt Cloud alternative in
`orchestration/dbt_cloud/job_wf_demo_mapping_strict_fail_fast.json`. A dbt
Cloud job's `execute_steps` always stop at the first failing step, so one
dbt Cloud job cannot reproduce the legacy step-1-failure behavior. The strict
alternative deliberately gates step 2 on step 1 and is therefore **not**
faithful to the legacy graph.

## Legacy task to dbt equivalent

| Legacy task or setting | Legacy behavior | Default faithful equivalent |
| --- | --- | --- |
| Scheduler | `ONDEMAND` (lines 1133-1134). | Manual/API-triggered `workflow_dispatch` job. No cron is defined. |
| Start | `Start → s_m_demo_mapping2` without a condition (line 1471). | First step of `orchestration/wf_demo_mapping.yml`. |
| `s_m_demo_mapping2` | Session for `m_demo_mapping2` starts at line 1365; `s_m_demo_mapping2 → Decision1` is unconditional (line 1473). | `dbt build --selector s_m_demo_mapping2 --project-dir dbt/informatica --profiles-dir dbt/informatica`, with `continue-on-error: true`. |
| `Decision1` | Evaluates `$s_m_demo_mapping2.Status = 1` (lines 1158-1159). Failure routes to `Failed_Email1` (line 1467), while the link to step 2 is unconditional (line 1470). | Failure notification followed by unconditional continuation to step 2. |
| `Failed_Email1` | Recipient `data-eng-alerts@example.com`, subject `Execution Status`, text `Dataload s_m_demo_mapping2 was failed to execute` (lines 1147-1150). | Placeholder notification step; recipient is retained as an environment value. |
| `s_m_demo_mapping1` | Session for `m_demo_mapping1` starts at line 1236; `s_m_demo_mapping1 → Decision2` is unconditional (line 1472). | `dbt build --selector s_m_demo_mapping1 --project-dir dbt/informatica --profiles-dir dbt/informatica`, run after step 1 regardless of step-1 outcome. |
| `Decision2` | Evaluates `$s_m_demo_mapping1.Status = 1` (lines 1155-1156). Failure routes to `Failed_Email2` (line 1465); success routes to step 3 (line 1469). | Step 2 failure is notified and leaves the workflow failed. Step 3 is conditional on step-2 success. |
| `Failed_Email2` | Recipient `data-eng-alerts@example.com`, subject `Run status`, text `Sessio 's_m_demo_mapping1' failed` (lines 1137-1140). | Placeholder notification followed by the failed job conclusion, equivalent to `Control` stopping the parent. |
| `Control` | `Control Option = "Stop parent"` (lines 1152-1153); reached from `Failed_Email2` (line 1468). | No separate Control task; the non-zero step-2 command result stops the workflow. |
| `s_m_demo_mapping3` | Session for `m_demo_mapping3` starts at line 1169; `s_m_demo_mapping3 → Decision3` is unconditional (line 1474). | `dbt build --selector s_m_demo_mapping3 --project-dir dbt/informatica --profiles-dir dbt/informatica`, only after step 2 succeeds. |
| `Decision3` | Evaluates `$s_m_demo_mapping3.Status = 1` (lines 1161-1162). Success routes to `SuccessEmail` (line 1466); failure routes to `Failed_Email3` (line 1475). | Success and failure placeholder notifications; no Control behavior is added to the final failure path. |
| `Failed_Email3` | Recipient `data-eng-alerts@example.com`, subject `Execution Status`, text `Dataload  s_m_demo_mapping3t was failed to execute` (lines 1164-1167). | Placeholder notification. The source spaces and trailing `t` are retained. |
| `SuccessEmail` | Recipient `data-eng-alerts@example.com`, subject `Run Status`, text `Session s_m_demo_mapping3 executed successfully` (lines 1142-1146). | Placeholder success notification. |

The faithful default intentionally omits `--fail-fast`: it must preserve the
cross-step asymmetry, while each dbt command still returns its normal failure
status. `--fail-fast` remains in the clearly-labelled strict alternative.

### Session and target-load mapping

All three legacy sessions use `Commit Type = Target` and `Commit Interval =
10000` (session blocks beginning at lines 1169, 1236, and 1365). Each uses
Oracle relational writers with target load type `Bulk` and connection `idwdev`
(writers in lines 1181-1204, 1275-1350, and 1399-1420). The shared session
configuration sets `Constraint based load ordering = NO` and `Stop on errors =
0` (lines 1091-1114).

| Mapping | Legacy order 1 | Legacy order 2 |
| --- | --- | --- |
| `m_demo_mapping2` | `demo_target1_UPD`, `demo_target1_INS` (lines 424-425) | None |
| `m_demo_mapping1` | `demo_target6`, `demo_target5` (lines 895-896) | `demo_target3` (line 897) |
| `m_demo_mapping3` | `demo_target21`, `demo_target2` (lines 1087-1088) | None |

## Selector contract and current model names

The selectors are defined in `dbt/informatica/selectors.yml`, next to the
real branches' `dbt/informatica/dbt_project.yml`.

The current selectors are name/FQN-based because the inspected real branches
carry no mapping tags:

| Selector | FQN targets and upstream expansion |
| --- | --- |
| `s_m_demo_mapping2` | `demo_target1`, `demo_target1_ins`, `demo_target1_upd` with `parents: true` |
| `s_m_demo_mapping1` | `demo_target3`, `demo_target5`, `demo_target6` with `parents: true` |
| `s_m_demo_mapping3` | `demo_target2`, `demo_target21`, `demo_target2_physical` with `parents: true` |
| `s_m_demo_mapping2_load_order_1` | `demo_target1_upd`, `demo_target1_ins` with `parents: true` |
| `s_m_demo_mapping1_load_order_1` | `demo_target5`, `demo_target6` with `parents: true` |
| `s_m_demo_mapping1_load_order_2` | `demo_target3` with `parents: true` |
| `s_m_demo_mapping3_load_order_1` | `demo_target21`, `demo_target2` with `parents: true` |

An order-2 mart must `ref()` the order-1 marts of the same mapping so one
invocation preserves `TARGETLOADORDER`. A tag-based form such as
`tag:m_demo_mappingN` is the preferred future shape once models carry mapping
tags. Name-based selection is used today only because the real models carry
no such tags.

The currently inspected model names are:

* Mapping 2: `demo_target1`, `demo_target1_ins`, `demo_target1_upd`,
  `int_demo_mapping2_lookup`, `stg_demo_source1`, and
  `stg_demo_target1_pre`.
* Mapping 3: `demo_target2`, `demo_target21`, `demo_target2_physical`,
  `int_m3_exptrans`, and `stg_demo_source2`.
* Mapping 1: no models exist on either inspected branch yet. The intended
  target names are `demo_target3`, `demo_target5`, and `demo_target6`, plus
  their upstreams.

The two branches carry separate dbt scaffolds at the same path
`dbt/informatica`, but with different project names:
`informatica_migration` for mapping 3 and `informatica_m_demo_mapping2` for
mapping 2. They conflict at the project scaffold level and selectors must be
re-run after the projects are reconciled on `main`.

## Execute steps

The faithful default workflow invokes:

```sh
dbt build --selector s_m_demo_mapping2 --project-dir dbt/informatica --profiles-dir dbt/informatica
dbt build --selector s_m_demo_mapping1 --project-dir dbt/informatica --profiles-dir dbt/informatica
dbt build --selector s_m_demo_mapping3 --project-dir dbt/informatica --profiles-dir dbt/informatica
```

The strict alternative invokes the same three selectors as dbt Cloud
`execute_steps`, with `--fail-fast`, but cannot reproduce the unconditional
Decision1 link.

## Does NOT carry over

The following PowerCenter behavior is not represented as dbt/dbt Cloud
semantics:

* **Commit intervals:** `Commit Type = Target` and `Commit Interval = 10000`
  become dbt materializations as atomic statements. There are no partial
  commits or restart-from-commit-point behavior.
* **Scheduler and server affinity:** `ONDEMAND` becomes manual/API-triggered
  execution. There is no PowerCenter scheduler and no affinity to
  `IDW_PCINTG01`.
* **Workflow variables:** `$s_m_X.Status`, `$s_m_X.ErrorCode`,
  `$s_m_X.SrcSuccessRows`, `$s_m_X.TgtFailedRows`, `$s_m_X.PrevTaskStatus`,
  and similar values become dbt artifacts such as `run_results.json` and dbt
  Cloud run artifacts/API results, not inter-task variables.
* **`Stop on errors = 0` and `SUSPEND_ON_ERROR = NO`:** these flags do not
  replace dbt command failure status.
* **Control `Stop parent`:** the faithful workflow uses the non-zero step-2
  command result; the strict alternative uses dbt Cloud's first-failure
  execute-step behavior.
* **Reject files and `.bad` rows:** use dbt tests and configured test severity
  for data quality failures.
* **Bulk target load and Oracle connection:** `Bulk` and `idwdev` are legacy
  adapter/runtime details, not dbt Cloud orchestration settings.
* **Constraint-based load ordering:** legacy `NO` becomes explicit DAG
  ordering through `ref()` dependencies.

The router-instance-to-physical-table collapse remains documented: mapping 2
has `demo_target1_INS` and `demo_target1_UPD` as instances of physical
`demo_target1`; mapping 3 has `demo_target2` and `demo_target21` as instances
of physical `demo_target2`. Mapping 3 also contains `ABORT()` guards; those
are model/test semantics, not orchestration.

## Verification status

### Mapping 3: verified against `devin/dbt-m_demo_mapping3` (PR #14)

The branch has project path `dbt/informatica`, project name
`informatica_migration`, and models `demo_target2`, `demo_target21`,
`demo_target2_physical`, `int_m3_exptrans`, and `stg_demo_source2`.

The repository selectors file was copied into the worktree without editing
the branch's committed files. Raw output follows:

```text
$ dbt ls --selector s_m_demo_mapping2 --project-dir dbt/informatica --profiles-dir dbt/informatica
22:46:46  Running with dbt=1.12.0
22:46:46  Registered adapter: duckdb=1.10.1
22:46:47  Found 5 models, 13 data tests, 1 seed, 486 macros, 4 unit tests
22:46:47  [WARNING]: No nodes selected!

$ dbt ls --selector s_m_demo_mapping1 --project-dir dbt/informatica --profiles-dir dbt/informatica
22:46:49  Running with dbt=1.12.0
22:46:50  Registered adapter: duckdb=1.10.1
22:46:50  Found 5 models, 13 data tests, 1 seed, 486 macros, 4 unit tests
22:46:50  [WARNING]: No nodes selected!

$ dbt ls --selector s_m_demo_mapping3 --project-dir dbt/informatica --profiles-dir dbt/informatica
22:46:52  Running with dbt=1.12.0
22:46:53  Registered adapter: duckdb=1.10.1
22:46:53  Found 5 models, 13 data tests, 1 seed, 486 macros, 4 unit tests
informatica_migration.marts.demo_target2
informatica_migration.marts.demo_target21
informatica_migration.marts.demo_target2_physical
informatica_migration.intermediate.int_m3_exptrans
informatica_migration.staging.stg_demo_source2
informatica_migration.demo_source2
informatica_migration.accepted_values_demo_target21_Gender__M__F
informatica_migration.accepted_values_demo_target2_Gender__M__F
informatica_migration.demo_target2_newgroup1_invariant
informatica_migration.exptrans_o_relationship_to_subscriber_code_label_abort
informatica_migration.not_null_demo_target21_Member_Identifier
informatica_migration.not_null_demo_target21_Relationship_to_Subscriber_Code_Label
informatica_migration.not_null_demo_target21_Soc_Number
informatica_migration.not_null_demo_target2_Member_Identifier
informatica_migration.not_null_demo_target2_Relationship_to_Subscriber_Code_Label
informatica_migration.not_null_demo_target2_physical_Member_Identifier
informatica_migration.unique_demo_target21_Member_Identifier
informatica_migration.unique_demo_target2_Member_Identifier
informatica_migration.unique_demo_target2_physical_Member_Identifier
unit_test:informatica_migration.router_newgroup1_sends_ssn_null_rows_to_demo_target2
unit_test:informatica_migration.router_newgroup2_sends_ssn_present_rows_to_demo_target21
unit_test:informatica_migration.guarded_label_null_survives_exptrans_for_abort_test
unit_test:informatica_migration.sq_override_drops_null_member_type_code

$ dbt ls --selector s_m_demo_mapping2_load_order_1 --project-dir dbt/informatica --profiles-dir dbt/informatica
22:46:55  Running with dbt=1.12.0
22:46:56  Registered adapter: duckdb=1.10.1
22:46:56  Found 5 models, 13 data tests, 1 seed, 486 macros, 4 unit tests
22:46:56  [WARNING]: No nodes selected!

$ dbt ls --selector s_m_demo_mapping1_load_order_1 --project-dir dbt/informatica --profiles-dir dbt/informatica
22:46:58  Running with dbt=1.12.0
22:46:59  Registered adapter: duckdb=1.10.1
22:46:59  Found 5 models, 13 data tests, 1 seed, 486 macros, 4 unit tests
22:46:59  [WARNING]: No nodes selected!

$ dbt ls --selector s_m_demo_mapping1_load_order_2 --project-dir dbt/informatica --profiles-dir dbt/informatica
22:47:01  Running with dbt=1.12.0
22:47:01  Registered adapter: duckdb=1.10.1
22:47:02  Found 5 models, 13 data tests, 1 seed, 486 macros, 4 unit tests
22:47:02  [WARNING]: No nodes selected!

$ dbt ls --selector s_m_demo_mapping3_load_order_1 --project-dir dbt/informatica --profiles-dir dbt/informatica
22:47:04  Running with dbt=1.12.0
22:47:04  Registered adapter: duckdb=1.10.1
22:47:05  Found 5 models, 13 data tests, 1 seed, 486 macros, 4 unit tests
informatica_migration.marts.demo_target2
informatica_migration.marts.demo_target21
informatica_migration.intermediate.int_m3_exptrans
informatica_migration.staging.stg_demo_source2
informatica_migration.demo_source2
informatica_migration.accepted_values_demo_target21_Gender__M__F
informatica_migration.accepted_values_demo_target2_Gender__M__F
informatica_migration.demo_target2_newgroup1_invariant
informatica_migration.exptrans_o_relationship_to_subscriber_code_label_abort
informatica_migration.not_null_demo_target21_Member_Identifier
informatica_migration.not_null_demo_target21_Relationship_to_Subscriber_Code_Label
informatica_migration.not_null_demo_target2_Member_Identifier
informatica_migration.not_null_demo_target2_Relationship_to_Subscriber_Code_Label
informatica_migration.unique_demo_target21_Member_Identifier
informatica_migration.unique_demo_target2_Member_Identifier
unit_test:informatica_migration.router_newgroup1_sends_ssn_null_rows_to_demo_target2
unit_test:informatica_migration.router_newgroup2_sends_ssn_present_rows_to_demo_target21
unit_test:informatica_migration.guarded_label_null_survives_exptrans_for_abort_test
unit_test:informatica_migration.sq_override_drops_null_member_type_code
```

### Mapping 2: verified against `devin/dbt-m_demo_mapping2` (PR #15)

The branch has project path `dbt/informatica`, project name
`informatica_m_demo_mapping2`, and models `demo_target1`,
`demo_target1_ins`, `demo_target1_upd`, `int_demo_mapping2_lookup`,
`stg_demo_source1`, and `stg_demo_target1_pre`.

The repository selectors file was copied into the worktree without editing
the branch's committed files. Raw output follows:

```text
$ dbt ls --selector s_m_demo_mapping2 --project-dir dbt/informatica --profiles-dir dbt/informatica
22:47:07  Running with dbt=1.12.0
22:47:07  Registered adapter: duckdb=1.10.1
22:47:07  Found 6 models, 33 data tests, 2 sources, 486 macros, 6 unit tests
informatica_m_demo_mapping2.marts.demo_target1
informatica_m_demo_mapping2.marts.demo_target1_ins
informatica_m_demo_mapping2.marts.demo_target1_upd
informatica_m_demo_mapping2.intermediate.int_demo_mapping2_lookup
informatica_m_demo_mapping2.staging.stg_demo_source1
informatica_m_demo_mapping2.staging.stg_demo_target1_pre
source:informatica_m_demo_mapping2.legacy_informatica_m2.demo_source1
source:informatica_m_demo_mapping2.legacy_informatica_m2.demo_target1_pre
informatica_m_demo_mapping2.accepted_values_demo_target1_ins_CREATED_BY__IDWUSER
informatica_m_demo_mapping2.accepted_values_demo_target1_upd_UPDATED_BY__IDWUSER
informatica_m_demo_mapping2.accepted_values_int_demo_mapping2_lookup_Changed_Flag__True__Update
informatica_m_demo_mapping2.accepted_values_int_demo_mapping2_lookup_New_Flag__True__Insert
informatica_m_demo_mapping2.not_null_demo_target1_Key
informatica_m_demo_mapping2.not_null_demo_target1_ins_BRANCH_CO_MNE
informatica_m_demo_mapping2.not_null_demo_target1_ins_CREATED_BY
informatica_m_demo_mapping2.not_null_demo_target1_ins_CREATED_TIME
informatica_m_demo_mapping2.not_null_demo_target1_ins_DESCRIPTION
informatica_m_demo_mapping2.not_null_demo_target1_ins_ID
informatica_m_demo_mapping2.not_null_demo_target1_ins_Key
informatica_m_demo_mapping2.not_null_demo_target1_ins_LEAD_CO_MNE
informatica_m_demo_mapping2.not_null_demo_target1_ins_MIS_DATE
informatica_m_demo_mapping2.not_null_demo_target1_ins_SHORT_NAME
informatica_m_demo_mapping2.not_null_demo_target1_upd_BRANCH_CO_MNE
informatica_m_demo_mapping2.not_null_demo_target1_upd_DESCRIPTION
informatica_m_demo_mapping2.not_null_demo_target1_upd_ID
informatica_m_demo_mapping2.not_null_demo_target1_upd_Key
informatica_m_demo_mapping2.not_null_demo_target1_upd_LEAD_CO_MNE
informatica_m_demo_mapping2.not_null_demo_target1_upd_MIS_DATE
informatica_m_demo_mapping2.not_null_demo_target1_upd_SHORT_NAME
informatica_m_demo_mapping2.not_null_demo_target1_upd_UPDATED_BY
informatica_m_demo_mapping2.not_null_demo_target1_upd_UPDATED_TIME
informatica_m_demo_mapping2.not_null_int_demo_mapping2_lookup_ID
informatica_m_demo_mapping2.not_null_stg_demo_source1_ID
informatica_m_demo_mapping2.not_null_stg_demo_target1_pre_ID
informatica_m_demo_mapping2.not_null_stg_demo_target1_pre_Key
informatica_m_demo_mapping2.test_demo_target1_ins_never_populated
informatica_m_demo_mapping2.test_demo_target1_upd_never_populated
informatica_m_demo_mapping2.test_demo_target1_upd_preserves_preexisting_columns
informatica_m_demo_mapping2.unique_demo_target1_Key
informatica_m_demo_mapping2.unique_demo_target1_ins_ID
informatica_m_demo_mapping2.unique_demo_target1_ins_Key
unit_test:informatica_m_demo_mapping2.insert_payload_uses_sequence_var_and_lexicographic_id_order
unit_test:informatica_m_demo_mapping2.update_payload_uses_lookup_key_and_only_update_columns
unit_test:informatica_m_demo_mapping2.duplicate_lookup_id_uses_highest_key
informatica_m_demo_mapping2.iif_flags_are_null_when_conditions_are_false
unit_test:informatica_m_demo_mapping2.matched_source_row_is_update_only
unit_test:informatica_m_demo_mapping2.unmatched_source_row_is_insert_only

$ dbt ls --selector s_m_demo_mapping1 --project-dir dbt/informatica --profiles-dir dbt/informatica
22:47:09  Running with dbt=1.12.0
22:47:09  Registered adapter: duckdb=1.10.1
22:47:10  Found 6 models, 33 data tests, 2 sources, 486 macros, 6 unit tests
22:47:10  [WARNING]: No nodes selected!

$ dbt ls --selector s_m_demo_mapping3 --project-dir dbt/informatica --profiles-dir dbt/informatica
22:47:11  Running with dbt=1.12.0
22:47:12  Registered adapter: duckdb=1.10.1
22:47:12  Found 6 models, 33 data tests, 2 sources, 486 macros, 6 unit tests
22:47:12  [WARNING]: No nodes selected!

$ dbt ls --selector s_m_demo_mapping2_load_order_1 --project-dir dbt/informatica --profiles-dir dbt/informatica
22:47:14  Running with dbt=1.12.0
22:47:15  Registered adapter: duckdb=1.10.1
22:47:15  Found 6 models, 33 data tests, 2 sources, 486 macros, 6 unit tests
informatica_m_demo_mapping2.marts.demo_target1_ins
informatica_m_demo_mapping2.marts.demo_target1_upd
informatica_m_demo_mapping2.intermediate.int_demo_mapping2_lookup
informatica_m_demo_mapping2.staging.stg_demo_source1
informatica_m_demo_mapping2.staging.stg_demo_target1_pre
source:informatica_m_demo_mapping2.legacy_informatica_m2.demo_source1
source:informatica_m_demo_mapping2.legacy_informatica_m2.demo_target1_pre
informatica_m_demo_mapping2.accepted_values_demo_target1_ins_CREATED_BY__IDWUSER
informatica_m_demo_mapping2.accepted_values_demo_target1_upd_UPDATED_BY__IDWUSER
informatica_m_demo_mapping2.accepted_values_int_demo_mapping2_lookup_Changed_Flag__True__Update
informatica_m_demo_mapping2.accepted_values_int_demo_mapping2_lookup_New_Flag__True__Insert
informatica_m_demo_mapping2.not_null_demo_target1_ins_BRANCH_CO_MNE
informatica_m_demo_mapping2.not_null_demo_target1_ins_CREATED_BY
informatica_m_demo_mapping2.not_null_demo_target1_ins_CREATED_TIME
informatica_m_demo_mapping2.not_null_demo_target1_ins_DESCRIPTION
informatica_m_demo_mapping2.not_null_demo_target1_ins_ID
informatica_m_demo_mapping2.not_null_demo_target1_ins_Key
informatica_m_demo_mapping2.not_null_demo_target1_ins_LEAD_CO_MNE
informatica_m_demo_mapping2.not_null_demo_target1_ins_MIS_DATE
informatica_m_demo_mapping2.not_null_demo_target1_ins_SHORT_NAME
informatica_m_demo_mapping2.not_null_demo_target1_upd_BRANCH_CO_MNE
informatica_m_demo_mapping2.not_null_demo_target1_upd_DESCRIPTION
informatica_m_demo_mapping2.not_null_demo_target1_upd_ID
informatica_m_demo_mapping2.not_null_demo_target1_upd_Key
informatica_m_demo_mapping2.not_null_demo_target1_upd_LEAD_CO_MNE
informatica_m_demo_mapping2.not_null_demo_target1_upd_MIS_DATE
informatica_m_demo_mapping2.not_null_demo_target1_upd_SHORT_NAME
informatica_m_demo_mapping2.not_null_demo_target1_upd_UPDATED_BY
informatica_m_demo_mapping2.not_null_demo_target1_upd_UPDATED_TIME
informatica_m_demo_mapping2.not_null_int_demo_mapping2_lookup_ID
informatica_m_demo_mapping2.not_null_stg_demo_source1_ID
informatica_m_demo_mapping2.not_null_stg_demo_target1_pre_ID
informatica_m_demo_mapping2.not_null_stg_demo_target1_pre_Key
informatica_m_demo_mapping2.test_demo_target1_ins_never_populated
informatica_m_demo_mapping2.test_demo_target1_upd_never_populated
informatica_m_demo_mapping2.test_demo_target1_upd_preserves_preexisting_columns
informatica_m_demo_mapping2.unique_demo_target1_ins_ID
informatica_m_demo_mapping2.unique_demo_target1_ins_Key
unit_test:informatica_m_demo_mapping2.insert_payload_uses_sequence_var_and_lexicographic_id_order
unit_test:informatica_m_demo_mapping2.update_payload_uses_lookup_key_and_only_update_columns
unit_test:informatica_m_demo_mapping2.duplicate_lookup_id_uses_highest_key
informatica_m_demo_mapping2.iif_flags_are_null_when_conditions_are_false
unit_test:informatica_m_demo_mapping2.matched_source_row_is_update_only
unit_test:informatica_m_demo_mapping2.unmatched_source_row_is_insert_only

$ dbt ls --selector s_m_demo_mapping1_load_order_1 --project-dir dbt/informatica --profiles-dir dbt/informatica
22:47:17  Running with dbt=1.12.0
22:47:18  Registered adapter: duckdb=1.10.1
22:47:18  Found 6 models, 33 data tests, 2 sources, 486 macros, 6 unit tests
22:47:18  [WARNING]: No nodes selected!

$ dbt ls --selector s_m_demo_mapping1_load_order_2 --project-dir dbt/informatica --profiles-dir dbt/informatica
22:47:20  Running with dbt=1.12.0
22:47:20  Registered adapter: duckdb=1.10.1
22:47:21  Found 6 models, 33 data tests, 2 sources, 486 macros, 6 unit tests
22:47:21  [WARNING]: No nodes selected!

$ dbt ls --selector s_m_demo_mapping3_load_order_1 --project-dir dbt/informatica --profiles-dir dbt/informatica
22:47:23  Running with dbt=1.12.0
22:47:23  Registered adapter: duckdb=1.10.1
22:47:23  Found 6 models, 33 data tests, 2 sources, 486 macros, 6 unit tests
22:47:23  [WARNING]: No nodes selected!
```

### Mapping 1: PENDING

No inspected branch currently contains `demo_target3`, `demo_target5`, or
`demo_target6`. Mapping 1 selector verification remains **PENDING** until
those models and their upstream graph exist on a reconciled `main`.
