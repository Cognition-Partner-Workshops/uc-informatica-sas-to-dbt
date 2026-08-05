# `wf_demo_mapping` orchestration mapping

This document covers the orchestration layer only. It does not define dbt
models or claim that the model project is already present.

The source workflow is `wf_demo_mapping`. The workflow declaration identifies
the PowerCenter server as `IDW_PCINTG01`, sets `SUSPEND_ON_ERROR` to `NO`, and
sets `REUSABLE_SCHEDULER` to `NO` (legacy XML lines 1132-1134).

## Legacy task to dbt equivalent

| Legacy task or setting | Legacy behavior (verified in `legacy/informatica/wf_demo_mapping.XML`) | dbt equivalent |
| --- | --- | --- |
| Scheduler | Scheduler type is `ONDEMAND` (lines 1133-1134). | A dbt Cloud job with schedule and webhook triggers disabled; invoke it manually or through the dbt Cloud API. No PowerCenter scheduler is carried over. |
| Start | Starts `s_m_demo_mapping2` without a condition (workflow link, line 1471). | The first execute step in the dbt Cloud job. |
| `s_m_demo_mapping2` | Session for `m_demo_mapping2` (line 1365 onward), followed by `Decision1` without a link condition (line 1473). | `dbt build --selector s_m_demo_mapping2 --fail-fast` |
| `Decision1` | Evaluates `$s_m_demo_mapping2.Status = 1` (task declaration, lines 1158-1159). A zero condition routes to `Failed_Email1` (line 1467). The link to `s_m_demo_mapping1` is unconditional (line 1470). | The first dbt Cloud execute step fails the job on a dbt error, so the next execute step is not run. This deliberately tightens the legacy behavior to strict fail-fast. |
| `Failed_Email1` | Sends to `data-eng-alerts@example.com`, subject `Execution Status`, text `Dataload s_m_demo_mapping2 was failed to execute` (lines 1147-1150). | Covered by the single dbt Cloud job-failure notification. The source wording is retained here for traceability. |
| `s_m_demo_mapping1` | Session for `m_demo_mapping1` (line 1236 onward), followed by `Decision2` without a link condition (line 1472). | `dbt build --selector s_m_demo_mapping1 --fail-fast` |
| `Decision2` | Evaluates `$s_m_demo_mapping1.Status = 1` (lines 1155-1156). Condition zero routes to `Failed_Email2`; condition one routes to `s_m_demo_mapping3` (lines 1465 and 1469). | The second execute step is reached only if the first dbt step succeeds. |
| `Failed_Email2` | Sends to `data-eng-alerts@example.com`, subject `Run status`, text `Sessio 's_m_demo_mapping1' failed` (lines 1137-1140). | Covered by the dbt Cloud job-failure and job-cancel notifications. The source typo is quoted as-is. |
| `Control` | Receives the failure email without a condition and has `Control Option = "Stop parent"` (lines 1152-1153 and 1468). | dbt Cloud `--fail-fast` and sequential execute steps stop the job at the first failing step. |
| `s_m_demo_mapping3` | Session for `m_demo_mapping3` (line 1169 onward), followed by `Decision3` without a link condition (line 1474). | `dbt build --selector s_m_demo_mapping3 --fail-fast` |
| `Decision3` | Evaluates `$s_m_demo_mapping3.Status = 1` (lines 1161-1162). Condition one routes to `SuccessEmail`; condition zero routes to `Failed_Email3` (lines 1466 and 1475). There is no Control task downstream. | A failure in the third dbt step fails the job and emits the native failure notification. |
| `Failed_Email3` | Sends to `data-eng-alerts@example.com`, subject `Execution Status`, text `Dataload  s_m_demo_mapping3t was failed to execute` (lines 1164-1167). | Covered by the dbt Cloud job-failure notification. Both spaces and the trailing `t` are source typos and are quoted as-is. |
| `SuccessEmail` | Sends to `data-eng-alerts@example.com`, subject `Run Status`, text `Session s_m_demo_mapping3 executed successfully` (lines 1142-1146). | No success notification object is defined here; successful completion is represented by the dbt Cloud job/run status. |

### Session and target-load mapping

All three legacy sessions use `Commit Type = Target` and `Commit Interval =
10000` (session blocks beginning at lines 1169, 1236, and 1365). Each uses
Oracle relational writers with target load type `Bulk` and connection `idwdev`
(for example, the writers in lines 1181-1204, 1275-1350, and 1399-1420).
The shared session configuration sets `Constraint based load ordering = NO`
and `Stop on errors = 0` (lines 1091-1114).

The per-mapping `TARGETLOADORDER` declarations are:

| Mapping | Legacy order 1 | Legacy order 2 |
| --- | --- | --- |
| `m_demo_mapping2` | `demo_target1_UPD`, `demo_target1_INS` (lines 424-425) | None |
| `m_demo_mapping1` | `demo_target6`, `demo_target5` (lines 895-896) | `demo_target3` (line 897) |
| `m_demo_mapping3` | `demo_target21`, `demo_target2` (lines 1087-1088) | None |

The dbt selectors are tag-based rather than model-name-based. Future model
authors must apply the mapping tag (`m_demo_mapping1`, `m_demo_mapping2`, or
`m_demo_mapping3`) to every model in that mapping. The `informatica` tag is a
project-wide grouping tag and is not required by the session selectors. Mart
models additionally carry `target_load_order_1` or `target_load_order_2`, as
applicable. An order-2 mart must `ref()` the
order-1 marts of the same mapping so the model DAG preserves
`TARGETLOADORDER` during one invocation. The load-order selectors in
`dbt/selectors.yml` provide diagnostic intersections if that contract is
broken.

The names/tags are defined against the model shapes implied by the STM:
staging models `stg_demo_source1` through `stg_demo_source5`, marts
`mart_demo_target1`, `mart_demo_target2`, `mart_demo_target3`,
`mart_demo_target5`, and `mart_demo_target6`, plus intermediate models per
mapping. No dbt project exists on `main` yet, so these are intended future
model names and tag assignments, not verified current model nodes.

## Execute steps, in legacy order

The dbt Cloud job executes these as three separate steps:

```sh
dbt build --selector s_m_demo_mapping2 --fail-fast
dbt build --selector s_m_demo_mapping1 --fail-fast
dbt build --selector s_m_demo_mapping3 --fail-fast
```

The equivalent inline form for a mapping tag is
`dbt build --select tag:m_demo_mapping2` (with the corresponding mapping tag
for the other sessions).

dbt Cloud stops at the first failing execute step. This is the native
fail-fast expression of the migration's deliberate strict gating: unlike the
unconditional `Decision1` link in the source, step 2 does not run after a
step-1 failure, and step 3 does not run after a step-2 failure.

## Does NOT carry over

The following PowerCenter behavior is intentionally not represented as
dbt/dbt Cloud semantics:

* **Commit intervals:** `Commit Type = Target` and `Commit Interval = 10000`
  become dbt materializations as single atomic statements. There are no
  partial-commit semantics or restart-from-commit-point behavior.
* **Scheduler and server affinity:** `ONDEMAND` becomes an API/manual-triggered
  dbt Cloud job. There is no PowerCenter workflow scheduler and no affinity to
  `IDW_PCINTG01`.
* **Workflow variables:** variables such as
  `$s_m_X.Status`, `$s_m_X.ErrorCode`, `$s_m_X.SrcSuccessRows`,
  `$s_m_X.TgtFailedRows`, and `$s_m_X.PrevTaskStatus` are not inter-task
  variables in dbt. Use `run_results.json` and dbt Cloud run artifacts/API
  results instead.
* **`Stop on errors = 0` and `SUSPEND_ON_ERROR = NO`:** these legacy flags do
  not override dbt failure semantics. The orchestration uses dbt build failure
  status and `--fail-fast`.
* **Control `Stop parent`:** there is no separate Control task. Sequential
  execute steps with `--fail-fast` provide the intentional strict
  fail-fast behavior.
* **Reject files and `.bad` rows:** these are not carried into the job
  definition. Use dbt tests and configured test error severity for data
  quality failures.
* **Bulk target load and Oracle connection:** `Bulk` target load type and the
  Oracle connection `idwdev` are legacy adapter/runtime details, not dbt Cloud
  orchestration settings.
* **Constraint-based load ordering:** legacy `NO` becomes explicit model-DAG
  ordering through `ref()` dependencies. The order-2 `m_demo_mapping1` mart
  must depend on the order-1 marts.

The source also has router instances that collapse to one physical table in
the dbt representation: `demo_target1_INS` and `demo_target1_UPD` are
instances of physical `demo_target1`, while `demo_target2` and
`demo_target21` are instances of physical `demo_target2`. The `m_demo_mapping3`
mapping contains `ABORT()` guards in its legacy transformation expression
(line 943); their replacement is model/test logic, not orchestration.

### Legacy workflow quirk

`Decision1` has the condition `$s_m_demo_mapping2.Status = 1`, and its
failure email branch is `$Decision1.Condition = 0`. However, the link from
`Decision1` to `s_m_demo_mapping1` has **no condition** (lines 1158-1159 and
1470). Therefore, in the legacy workflow, step 2 runs even when step 1
failed. This is documented rather than silently corrected. The dbt job
deliberately tightens the behavior to strict fail-fast by using separate
ordered execute steps and `--fail-fast`.

Only the step-2 failure path reaches `Control` (`Failed_Email2 → Control`);
the step-3 failure path reaches `Failed_Email3` and has no Control downstream
(lines 1465, 1468, and 1475). Thus, the only path that stops the parent
workflow in the source is the `s_m_demo_mapping1` failure path, not the last
one.

## Verification status: PENDING

No dbt project exists on `main` (the repository currently contains
`README.md`, `legacy/`, and `tools/` at the root). Selector verification
against `main` is therefore **PENDING**.

### Secondary check: throwaway stub project

The following output was resolved against the throwaway stub project at
`/home/ubuntu/scratch/selector_check/`, using dbt-duckdb and the STM-implied
model names and tags. It was **not** resolved against `main`. The stub keeps
`mart_demo_target2` and `mart_demo_target21` as separate nodes to exercise
selection; the real models are expected to collapse both router instances into
one physical target, which does not change selector resolution.

```text
$ DBT_PROFILES_DIR=/home/ubuntu/scratch/selector_check dbt ls --selector s_m_demo_mapping2
22:32:59  Running with dbt=1.12.0
22:32:59  Registered adapter: duckdb=1.10.1
22:32:59  Found 14 models, 486 macros
selector_check.intermediate.int_demo_mapping2
selector_check.marts.mart_demo_target1
selector_check.staging.stg_demo_source1

$ DBT_PROFILES_DIR=/home/ubuntu/scratch/selector_check dbt ls --selector s_m_demo_mapping1
22:33:01  Running with dbt=1.12.0
22:33:01  Registered adapter: duckdb=1.10.1
22:33:01  Found 14 models, 486 macros
selector_check.intermediate.int_demo_mapping1
selector_check.marts.mart_demo_target3
selector_check.marts.mart_demo_target5
selector_check.marts.mart_demo_target6
selector_check.staging.stg_demo_source3
selector_check.staging.stg_demo_source4
selector_check.staging.stg_demo_source5

$ DBT_PROFILES_DIR=/home/ubuntu/scratch/selector_check dbt ls --selector s_m_demo_mapping3
22:33:03  Running with dbt=1.12.0
22:33:04  Registered adapter: duckdb=1.10.1
22:33:04  Found 14 models, 486 macros
selector_check.intermediate.int_demo_mapping3
selector_check.marts.mart_demo_target2
selector_check.marts.mart_demo_target21
selector_check.staging.stg_demo_source2

$ DBT_PROFILES_DIR=/home/ubuntu/scratch/selector_check dbt ls --selector s_m_demo_mapping1_load_order_2
22:33:06  Running with dbt=1.12.0
22:33:06  Registered adapter: duckdb=1.10.1
22:33:06  Found 14 models, 486 macros
selector_check.marts.mart_demo_target3

$ DBT_PROFILES_DIR=/home/ubuntu/scratch/selector_check dbt build --selector s_m_demo_mapping1
22:33:08  Running with dbt=1.12.0
22:33:08  Registered adapter: duckdb=1.10.1
22:33:08  Found 14 models, 486 macros
22:33:08
22:33:08  Concurrency: 1 threads (target='local')
22:33:08
22:33:08  1 of 7 START sql table model main.stg_demo_source3 ............................. [RUN]
22:33:09  1 of 7 OK created sql table model main.stg_demo_source3 ........................ [OK in 0.08s]
22:33:09  2 of 7 START sql table model main.stg_demo_source4 ............................. [RUN]
22:33:09  2 of 7 OK created sql table model main.stg_demo_source4 ........................ [OK in 0.03s]
22:33:09  3 of 7 START sql table model main.stg_demo_source5 ............................. [RUN]
22:33:09  3 of 7 OK created sql table model main.stg_demo_source5 ........................ [OK in 0.03s]
22:33:09  4 of 7 START sql table model main.int_demo_mapping1 ............................ [RUN]
22:33:09  4 of 7 OK created sql table model main.int_demo_mapping1 ....................... [OK in 0.03s]
22:33:09  5 of 7 START sql table model main.mart_demo_target5 ............................ [RUN]
22:33:09  5 of 7 OK created sql table model main.mart_demo_target5 ....................... [OK in 0.03s]
22:33:09  6 of 7 START sql table model main.mart_demo_target6 ............................ [RUN]
22:33:09  6 of 7 OK created sql table model main.mart_demo_target6 ....................... [OK in 0.03s]
22:33:09  7 of 7 START sql table model main.mart_demo_target3 ............................ [RUN]
22:33:09  7 of 7 OK created sql table model main.mart_demo_target3 ....................... [OK in 0.03s]
22:33:09
22:33:09  Finished running 7 table models in 0 hours 0 minutes and 0.38 seconds (0.38s).
22:33:09
22:33:09  Completed successfully
22:33:09
22:33:09  Done. PASS=7 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=7
```
