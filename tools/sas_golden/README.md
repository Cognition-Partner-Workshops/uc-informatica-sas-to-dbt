# SAS golden-dataset harness

This harness turns the six branch-coverage kits in `tests/golden/sas_<program>/` into real SAS golden outputs, then
uses those outputs to check the dbt ports scenario by scenario.

**Status: provisional.** Every `expected_provisional/` file was derived by hand from the SAS source; no SAS runtime
was available. `tools/sas_baseline.py` is a Python/DuckDB re-implementation and served only as a second opinion. An
expected file is golden only once a licensed SAS host has produced it with `run_golden.sas` and someone has reviewed
the diff against the provisional file. Coverage and the suspected divergences are listed in
[`docs/golden/SAS_COVERAGE.md`](../../docs/golden/SAS_COVERAGE.md).

| File | Purpose |
|---|---|
| `run_golden.sas` | SAS driver: runs each scenario against the **unmodified** `legacy/sas/programs/<program>.sas` and writes `scenarios/<id>/golden/<TARGET>.csv` + `_status.txt` |
| `golden_plan.sas` | Generated plan: one block per scenario, with an explicit INPUT statement for each CSV. Do not edit |
| `build_plan.py` | Regenerates `golden_plan.sas` from `tests/golden/*/scenarios.json` (`--check` exits 1 when the plan is stale) |
| `stubs/{sendmail,lock,export_xlsx}.sas` | No-op stand-ins for the side-effect macros (see "Stubs") |
| `compare_golden.py` | Compares expected vs actual for every scenario/target using `tools/parity_diff.py` (unchanged) and `tools/keys/sas_keys.json` |

## Runbook

### 1. Run the driver on the SAS host

Requirements: SAS 9.4 M5 or later (Base SAS; `autoexec_local.sas` uses open-code `%if`), a checkout of this branch, and
write access to `/opt/sas/custom`. The programs `%include "/opt/sas/custom/macros/<m>.sas"` by absolute path. The
driver stages `parmv`/`nobs` from `legacy/sas/macros` and the stubs into `/opt/sas/custom/macros` (for `%include`) and
`/opt/sas/custom/Macro` (the `autoexec_local.sas` autocall path, which is how `credit_risk_scoring` reaches `%lock`).

Run one batch session per scenario. Sessions isolate global macro variables and WORK, and batch mode gives the
syntax-check (OBS=0) behaviour that several expected outcomes depend on:

```sh
export GOLDEN_REPO=$PWD GOLDEN_LOG_DIR=$HOME/golden_logs   # logs stay OUTSIDE the repo
mkdir -p "$GOLDEN_LOG_DIR"
python3 - <<'PY' > /tmp/golden_scenarios.txt
import glob, json, os
for m in sorted(glob.glob("tests/golden/sas_*/scenarios.json")):
    prog = os.path.basename(os.path.dirname(m))[4:]
    for s in json.load(open(m)):
        print(f"{prog}:{s['id']}")
PY
while read -r sc; do
  sas -nodms -noautoexec -sysin tools/sas_golden/run_golden.sas -sysparm "$sc" \
      -log "$GOLDEN_LOG_DIR/driver_${sc/:/__}.log"
done < /tmp/golden_scenarios.txt
```

`-sysparm "<program>"` runs every scenario of one program; an empty `-sysparm` runs all 94 in a single session.
Optional settings: `GOLDEN_SAS_ROOT` (default `/opt/sas/custom`), `GOLDEN_REAL_MACROS` (e.g. `lock` to stage the real
`legacy/sas/macros/lock.sas` instead of the stub), `GOLDEN_OUT` (output folder name, default `golden`).

What the driver does for each scenario (details are in the header of `run_golden.sas`):

1. It creates a fresh data root under WORK with the directory layout of `legacy/sas/config/autoexec_local.sas`, sets
   `SAS_DATA_ROOT`/`SAS_REPO_ROOT` and `%include`s `autoexec_local.sas` itself. Librefs, options and global macro
   variables are therefore the ones the programs expect.
2. It compiles `legacy/sas/formats/*.sas` into `BANKING`/`INSURANCE`, then sets `CURR_DT` (the scenario's date
   parameter or `run_date`, else 31JAN2024) and `PREV_YM` (`report_month`, else 202401).
3. It reads `inputs/<libref>/<DATASET>.csv` with explicit informats. Dates are DATE9. or ISO, an empty field is
   missing, and `*_DESC` companion columns are dropped because they are not SAS variables. A CSV that is absent
   creates no dataset. `raw_ins/FRAUD_INDICATORS.csv` is also loaded as `TERA_DW.FRAUD_INDICATORS`, which is what
   `claims_processing` reads.
4. It copies the program byte for byte up to `%mend <program>;`, `%include`s that copy, and calls the macro once with
   the scenario's `params`. The trailing self-invocation (e.g. `%claims_processing(proc_date=&CURR_DT);`) is the only
   text left out: it would run with default parameters, and for APPEND/INSERT targets two calls would double the rows.
   The driver aborts the scenario if anything other than that one call follows `%mend`.
5. It records SYSCC, leaves syntax-check mode, and exports each target with `baseline/sas/<TARGET>.csv` column order.
   Dates are written YYYY-MM-DD, numbers unformatted (BEST32.), formats are stripped, and missing is written as an
   empty field. `*_DESC` = `put(<var>, <format>.)`. Wall-clock `LOAD_TIMESTAMP`/`SCORE_TIMESTAMP` are left out.
   Extra SAS columns are appended, so differences in shape show up in the diff. A listed target that is absent after
   the run is written header-only.

Operational preconditions the CSVs cannot express:

- `daily_transaction_processing` S14_lock_held requires a second SAS session to hold a lock on
  `CURATED.DAILY_TRANSACTIONS` while the scenario runs. Without that lock, its golden output is not valid.
- `%ABORT:` in `claims_processing` is a label named like a SAS reserved word. If the host rejects it, record that
  as a finding rather than editing `legacy/`.

### 2. Commit the golden outputs

Review each `golden/_status.txt` (target existence, row counts, program SYSCC). Commit `golden/*.csv` and `_status.txt`
only, never logs. Logs contain host paths and account names. Before committing, check that the diff contains no user
names, e-mail addresses or host paths.

### 3. Diff golden against provisional

```sh
python3 tools/sas_golden/compare_golden.py --expected provisional --actual-subdir golden
```

Each mismatch is either a hand-derivation error (fix `expected_provisional/` or retire it) or a confirmed SAS
behaviour that changes a kit assumption (update the kit README/COVERAGE). The open assumptions are listed in each
kit README and summarised in the PR that added this harness. After review, `compare_golden.py` with the default
`--expected auto` prefers `golden/`.

### 4. Load scenario inputs into Snowflake and build dbt, one scenario at a time

For each scenario, in its own target schema (see prerequisites):

1. Load every `inputs/<libref>/<DATASET>.csv` into the source tables the unit's dbt project reads. Convert DATE9.
   (`31JAN2024`) and ISO dates to `DATE` and `30JAN2024:06:00:00` to `TIMESTAMP_NTZ`. Decide on one convention for
   empty character cells (SAS has blank, not NULL; several divergences depend on it, e.g. CLA-D08, CRE-D07). Prior-state
   inputs (`stg_ins/`, `stg_bank/`, `curated/`) seed the target tables that SAS appends to.
2. Run `dbt build` with the scenario's `params` mapped to the unit's vars (e.g. `run_date`, `model_id`, `lob`).
3. Export each mart to `<actual-root>/<kit>/<scenario_id>/<TARGET>.csv` with ISO dates.

### 5. Compare

```sh
python3 tools/sas_golden/compare_golden.py --actual-root <actual-root>
```

The script prints one row per scenario/target: `MATCH`, `MISMATCH` (first differing column), `MISSING` (target not
exported), `NO_ACTUAL`, or for scenarios whose expected outcome is "no target created" (`monthly_regulatory_reporting`
S18, `policy_valuation` S16/S17) `ABSENT_OK`/`ABSENT_FAIL`. Some fan-out scenarios repeat a key from
`sas_keys.json`, so sorting on that key is not deterministic. For those targets the script also runs parity_diff with
all columns as the key (`ALLCOL`), and that result decides the row. The exit code is 0 only if every row passes.

Local proof (no SAS, no Snowflake): comparing the provisional expectations with themselves passes all 94 scenarios /
263 rows:

```sh
python3 tools/sas_golden/compare_golden.py --expected provisional --actual-subdir expected_provisional
```

## Snowflake prerequisites

- **One writable schema per concurrent scenario run.** Each scenario needs its own source and target tables, because
  prior state and dated feeds differ per scenario. The run's demo role cannot `CREATE SCHEMA`: it can write only to
  the schemas provisioned for the run. Either run scenarios one after another in one schema, truncating between runs,
  or have an administrator grant extra schemas (for example one per program) before running in parallel.
- **Warehouse credit budget.** The run's warehouse sits under a resource monitor shared by every unit build. One
  unit build is 20-46 dbt nodes; 94 scenarios multiply that. Check the monitor's remaining quota and agree a budget
  before starting. Use an XS warehouse with auto-suspend, and build one program's scenarios serially.
- Do not commit credentials or profiles with secrets. Read them from the environment.

## Stubs

`tools/sas_golden/stubs/<m>.sas` defines `%macro <m> / parmbuff;`, which accepts any argument list and only logs a
NOTE. A stub replaces only a macro whose sole effect is outside the datasets:

| Macro | Used by | Why it is stubbed |
|---|---|---|
| `%sendmail` | claims_processing, load_customer_accounts | Sends e-mail. The programs pass `body=`, which the macro does not declare, and the macro needs `%seplist`, which is not in the repo |
| `%lock` | daily_transaction_processing, credit_risk_scoring (autocall), load_customer_accounts (included, never called) | Takes dataset locks. The calls are positional against a keyword-only macro, and the macro needs `%handle`/`%get_data_attr`, which are not in the repo |
| `%export_xlsx` | monthly_regulatory_reporting | Writes an XLSX workbook. Called with `file=`/`sheet=`, which it does not declare; needs `%export_dbms` (not in repo) |

The kits assume that, with the real macros, each of these calls fails at invocation and writes no data, so the stubs
should not change any dataset. Set `GOLDEN_REAL_MACROS="sendmail lock export_xlsx"` on one run to confirm this; route
`EMAIL_ONCALL` to a sink first.

## Regenerating the plan

Run `python3 tools/sas_golden/build_plan.py` after changing any `scenarios.json` or scenario CSV.
`python3 tools/sas_golden/build_plan.py --check` reports a stale plan. Column types are inferred once from every CSV
that shares a layout (seed, scenario inputs, expected outputs, `baseline/sas`), and character lengths are unified per
column name so that join and hash keys match across tables. A code column that contains a value with a leading
zero, such as `MERCHANT_CATEGORY` `0000`, is read as character.
