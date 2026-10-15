# Legacy ETL to dbt on Snowflake, told from the Snowflake seat

A bank runs its daily and monthly data estate on Informatica PowerCenter, a shelf of SAS programs and Oracle stored procedures. Snowflake's own tooling, SnowConvert AI (`scai`), converts the Oracle SQL and replatforms the Informatica XML into dbt projects; SAS it does not convert. Devin takes the whole estate. It inventories it before anyone funds a model, runs `scai` for the parts Snowflake converts and fixes what the tool leaves behind, rewrites the six SAS programs by hand with one child session per program, proves every target against the legacy answer row for row inside Snowflake, opens one pull request per unit with dbt tests and a parity report, and closes on the number the Snowflake account team tracks: warehouse credits burned by the migrated workloads, read from ACCOUNT_USAGE.

Everything below ran on 2026-10-15 under run token `SF_20261015_DS`. Nothing was merged, `main` is untouched in both repositories, and the one red result is still red.

## Sign in

Open the Field Kit and pick area **ISV and platform**, identity **Snowflake**. At the organisation selector choose **Partner Demo - ViewOnly**. Every session below belongs to that persona (user `user-1ebf34d1b99245ce804d3d10738b8e63`), so they appear in its sidebar; a session opened while signed in as someone else shows read only.

Repositories: `Cognition-Partner-Workshops/uc-informatica-sas-to-dbt` (Informatica XML, six SAS programs, baseline and parity tools, every PR of the run) and `Cognition-Partner-Workshops/ts-informatica-powercenter` (three Oracle SQL*Plus scripts and eleven PowerCenter exports from a health-records estate, read only).

Snowflake: account `yd76133.us-east-2.aws`, database `DEVIN_MIGRATION_DEMO`, schemas `SOURCE_SF_20261015_DS`, `BASELINE_SF_20261015_DS`, `DBT_SF_20261015_DS`, `SCAI_SF_20261015_DS`, `ORACLE_SF_20261015_DS`, warehouse `SF_20261015_DS_WH` with resource monitor `SF_20261015_DS_MON` (5 credits). The reader user `SF_20261015_DS_READER_USER` is the one to sign into Snowsight with in the room; its password is with the builder, and it can read the source and baseline schemas and the warehouse pages and nothing else.

The target standard every session was measured against is the ViewOnly org skill `snowflake-dbt-target-standard` (Customize, Skills, Organization). It fixes the project layout under `dbt/<unit>/`, the schema and naming rules, the tests from `tools/keys/*.json`, the `RUN:<token>` tag and `legacy_unit` meta on every model, the one warehouse, and the parity report `tools/parity_diff.py` has to write before a PR opens.

## Before the room

The baseline is the frozen legacy answer, and it lives on branch `baseline/SF_20261015_DS` and in PR #53, which stays open: https://github.com/Cognition-Partner-Workshops/uc-informatica-sas-to-dbt/pull/53. If it has been torn down, rebuild it from a clean clone of that branch at commit 8316570 or later (the loader fix 2b57542 and the teardown fix are on it) in about two and a half minutes with the commands in `baseline/SF_20261015_DS/README.md`; the README carries the per-step timings and the credits of the load. The loader generates new passwords every run and writes them only to the credential file it names, so after a rebuild re-create the six ViewOnly secrets (`SF_DEMO_USER`, `SF_DEMO_PASSWORD`, `SF_DEMO_ROLE`, `SF_DEMO_WAREHOUSE`, `SF_DEMO_DATABASE`, `SF_RUN_TOKEN`) from that file through `POST /v3/organizations/{org}/secrets` or Settings, Secrets, and sign into Snowsight once as `SF_20261015_DS_DEMO` before the live act. The reader password for the room comes from the same file.

Open these tabs before you start, signed in as the persona: the five sessions below, PR #53, the PR list filtered to base `baseline/SF_20261015_DS`, and a Snowsight worksheet as the reader user with `baseline/SF_20261015_DS/room_query.sql` pasted in. The acts are pre-run; only act 5 starts live.

## The acts, in presenting order

Scores are Pain (1 to 5, how much this hurts the bank today) times Async-cloud fit (1 to 5, how well the work suits an engineer that runs in the cloud without anyone watching).

### Act 0. Scoping before funding (Pain 4, Fit 4, score 16)

Session `ca69c38544184defb75a9d44463ddd91`, titled "Inventory before funding": https://partner-workshops.devinenterprise.com/sessions/ca69c38544184defb75a9d44463ddd91

Open the timeline at the inventory table, which lists twenty-three units across the two repositories (three Informatica mappings, six SAS programs, eleven PowerCenter workflows and three Oracle scripts), each with its source system, rows loaded in `SOURCE_SF_20261015_DS`, what `scai` converts on its own, what needs a human-style rewrite, and a risk from 1 to 5. The PowerCenter exports from the health-records repository show 567 personal-data fields counted by name and no quoted values; the wave plan puts them in a blocked fourth wave until a masking policy, landed source data and a baseline exist.

Devin asked one question, whether to migrate the insurance SAS programs in this wave or only banking. It waited, then took the default ("both tracks") when the answer came late. The persona later gave the same answer. The wave plan names `load_customer_accounts` as the fastest honest first result, and act 5 starts it live.

Say: "before a line of dbt exists the bank has a table it can fund against, and the first thing it will see working is already named".

### Act 5. Left for the room (Pain 3, Fit 4, score 12)

This act has no pre-run session, so as the persona you open a new session, paste the prompt from the section "The live prompt" below, and press start. Say what you are doing while it reads the repository: the session has the SAS program, the STM and the baseline keys from the branch, the Snowflake secrets from the org, and the target standard from the skill. Then switch to the finished sessions and come back to this one at the end; by then it is building or opening its PR.

### Act 1. Devin orchestrates, Snowflake converts (Pain 4, Fit 4, score 16)

Session `4c20f9c5d69246c7b913274c99922597`, titled "Snowflake converts, Devin fixes": https://partner-workshops.devinenterprise.com/sessions/4c20f9c5d69246c7b913274c99922597. PR #60: https://github.com/Cognition-Partner-Workshops/uc-informatica-sas-to-dbt/pull/60

Open the timeline where `scai code convert -e` runs on `wf_demo_mapping.xml` and the EWI table comes back (9 EWIs, 20 FDMs across the three mappings). Then open PR #60 at the per-file table: about 1,250 lines are SnowConvert's, kept as written in commit `2947745`, and about 410 are Devin's, the fixes for `STRCMP`, two sequence generators, `AES_DECRYPT` and the `ABORT()` guard, deterministic lookups, sources pointed at `SOURCE_SF_20261015_DS`, split targets, key tests and two `TO_DATE` casts. The builds went into `SCAI_SF_20261015_DS` and all seven targets match the baseline on rows and values.

The beat the Snowflake seat cares about: this session found a fault in the baseline, timestamps loaded as seconds instead of microseconds and a one-letter code loaded as a boolean, reported it with the offending years in the timeline, and the baseline owner fixed the loader (PR #53, commit `2b57542`) and reloaded. The session then re-ran parity and the match held.

Oracle converted at 0 percent and the session says why: the three scripts in `ts-informatica-powercenter` are shell wrappers and procedure calls with no table definitions, so there is nothing to deploy into `ORACLE_SF_20261015_DS`.

Say: "Snowflake's tool did the mechanical part and Devin did the rest, and you can read which lines are whose".

### Act 2. The long tail (Pain 5, Fit 5, score 25)

Parent session `4ea9db2df4bb4d12b82251720ae5ed87`, titled "Six SAS programs, six PRs": https://partner-workshops.devinenterprise.com/sessions/4ea9db2df4bb4d12b82251720ae5ed87

Open the parent at its final table: six rows, one per program, each with the child session, the PR, the dbt build result, the parity result and the ACU. The children, which keep the names the workflow gave them:

| Program | Child session | PR | dbt build | Parity |
|---|---|---|---|---|
| load_customer_accounts | https://partner-workshops.devinenterprise.com/sessions/206bad862a214f2894302ad0f4b83b14 | https://github.com/Cognition-Partner-Workshops/uc-informatica-sas-to-dbt/pull/56 | 47 pass, 3 fail (red, data-caused) | 466/466, 32/32 |
| monthly_regulatory_reporting | https://partner-workshops.devinenterprise.com/sessions/10dacd79d7e94500972e33b9048f2676 | https://github.com/Cognition-Partner-Workshops/uc-informatica-sas-to-dbt/pull/59 | 46 pass | 59/59, 70/70, 6/6, 1/1 |
| credit_risk_scoring | https://partner-workshops.devinenterprise.com/sessions/58540a1d65fe4cacbc90f63657679ef1 | https://github.com/Cognition-Partner-Workshops/uc-informatica-sas-to-dbt/pull/57 | 34 pass | 236/236, 195/195, 12/12 |
| daily_transaction_processing | https://partner-workshops.devinenterprise.com/sessions/4bf8e57c1be9418588be77e63b4e702c | https://github.com/Cognition-Partner-Workshops/uc-informatica-sas-to-dbt/pull/58 | 20 pass | 18903/18903, 610/610, 46/46 |
| policy_valuation | https://partner-workshops.devinenterprise.com/sessions/164831dfee69446181e5406fddef8f65 | https://github.com/Cognition-Partner-Workshops/uc-informatica-sas-to-dbt/pull/54 | 31 pass | 166/166, 8/8 |
| claims_processing | https://partner-workshops.devinenterprise.com/sessions/8787790f2e6748e2a29e77e68c2ac451 | https://github.com/Cognition-Partner-Workshops/uc-informatica-sas-to-dbt/pull/55 | 28 pass | 190/190, 101/101, 19/19 |

Open one child (claims_processing is a good one, it carries a SAS hash object and ordered rules with `RETURN`) and scroll to the dbt build and the parity run. Then open the parent again at its second pass, where it went through every Devin Review flag on five of the PRs, fixed the real ones (SAS missing-value handling in three programs, an unchecked input on #54, an empty-month case on #59), replied on the thread for the findings it judged correct as written, and re-ran parity on everything it touched.

Say: "six programs nobody wanted to port, written in parallel from the legacy source and the mapping document, each one proved against the old answer before its PR opened".

### Act 3. Validation a DBA believes (Pain 4, Fit 5, score 20)

Session `7b73810896e24de3b3dee1ff8ccae8a5`, titled "One honest red": https://partner-workshops.devinenterprise.com/sessions/7b73810896e24de3b3dee1ff8ccae8a5

Open PR #56 at the validation comment: https://github.com/Cognition-Partner-Workshops/uc-informatica-sas-to-dbt/pull/56. The comment has row counts per target, a hash of every keyed row (`hash_agg`) and the column-level mismatches, all read from Snowflake against `BASELINE_SF_20261015_DS`. Counts and hashes match, columns match, and the dbt tests stay red: `not_null(UTILIZATION_PCT)` fails on 18 rows, `not_null(RISK_RATING)` on 17, and the composite key on `ACCT_EXCEPTIONS` on one group. The baseline fails the same three tests by the same counts, so the model reproduces the legacy answer and the legacy data is what is wrong. Nobody hid it.

Then open the session's summary table: seven PRs (#54 to #60), every target matching on counts, hashes and columns. The session also started Devin Review on the two PRs that lacked it (#58 and #60), and it re-checked each PR at its final head after the review-fix commits landed. Its one caveat is in the timeline: the dbt tables were built one to four minutes before each head commit, so it can show the tables match the committed code only to that resolution.

Say: "the comparison a DBA would write by hand, posted on every PR by the engineer that did not write the models, and the red one stays red".

### Act 4. Credits (Pain 3, Fit 4, score 12)

Session `6ff944c32e3c4db6a370fc0282befdc1`: https://partner-workshops.devinenterprise.com/sessions/6ff944c32e3c4db6a370fc0282befdc1

Open the HTML page attached to the session. It reads `WAREHOUSE_METERING_HISTORY` and `QUERY_HISTORY` for `SF_20261015_DS_WH` and breaks the credits down by unit and by phase (baseline load, scai conversion, dbt builds, parity and validation). A separate row labelled baseline waste carries the 0.0647 credits a mistyped warehouse, `SF_SF_20261015_DS_WH`, burned before it was dropped during the baseline build. The Informatica plus SAS licence figure the page compares against is a labelled planning assumption; no such figure exists in either repository.

At its 04:51 UTC pull the page showed 1.129 credits for the run: dbt builds 0.360, SCAI conversion 0.255, parity checks 0.221, baseline load 0.103, baseline waste 0.0647, with the rest in small rows for the reader user's Snowsight checks and session overhead. The metering hour was still open, and a builder's reading at 05:10 UTC after the review-fix rebuilds and the final validation pass gave 1.238 credits on `SF_20261015_DS_WH` plus the 0.0647 waste, 1.303 in all, with the resource monitor at 1.24 of 5.00. Snowflake's per-query attribution view returned no rows for the run, so the page splits each hourly metering row across that hour's queries by execution time and says so; the totals are metered, the split is an estimate.

Say: "the whole migration, baseline included, cost under two credits on an X-Small warehouse, and every one of those credits has a unit and a phase against it".

### Act 6. The Migrations page (Pain 4, Fit 5, score 20)

Session `f44163a7c9034bb185a8d76ddbb4acee`, titled "Plan, approve, tickets run": https://partner-workshops.devinenterprise.com/sessions/f44163a7c9034bb185a8d76ddbb4acee. Board: https://partner-workshops.devinenterprise.com/org/partner-demo-viewonly/boards/8f0ad0aad6454dccb858fc9c4c2a116b (key `UNT5`).

The persona opened the Migrations page and typed one sentence: "Move the 11 Informatica PowerCenter workflows in Cognition-Partner-Workshops/ts-informatica-powercenter to dbt on Snowflake, same target standard and parity gate as baseline/SF_20261015_DS; nothing merges." Nothing else was attached. The Migration Agent read both repositories, counted 108 mappings across the 11 exports and drafted a plan of five phases and 22 steps in the Plan view: access and target standard, inventory of the 11 workflows, source data and legacy baseline, the dbt units (a Pay_Calendar pilot, then ten more), and the parity gate with a roll-up report.

Open the Plan view first and show what it asked for before approval. The decision on the run hosting the ts track was answered with the recommended option, add the ts track to the `SF_20261015_DS` schemas, so one run, one gate and one warehouse stay in place. The blocker "loading SOURCE_ and BASELINE_ needs ACCOUNTADMIN" was cleared with a note in its discussion: the builder who holds the admin credential runs the loader extension on their own machine, and workers keep `SF_20261015_DS_DBT` only. The agent rewrote the load step around that and the persona approved; the plan view reads "Approved by Snowflake (Read-Only)". Approval created 22 tickets with the plan's dependencies between them, and the board dispatched a worker to each ticket with nothing ahead of it.

Then open the board, where six tickets landed, each with a status note the manager checked against the branch:

| Ticket | Worker session | Result |
|---|---|---|
| UNT5-1 Set up the ts migration branch | `55fd658eb2e04d588c65afae98014a67` | Branch `migration/ts-powercenter` off the baseline, 11 exports copied byte for byte, commit e355c95 |
| UNT5-2 Verify Snowflake access and run budget | `4167f9c525174d36ae4cd11688a63358` | Signed in as the DBT role on the run warehouse, read and write checks, monitor at 1.33 of 5; found the dbt profile needs `host` as well as `account` |
| UNT5-3 Lineage extractor for folder exports | `c64fd4f8b9554f96867a61317e79957c` | `tools/ts_lineage.py`, counts match the XML (108 mappings, 752 transformations), commit 84cc246 |
| UNT5-4 STMs and inventory for 11 workflows | `b05ab6bb9a7041bf9c1532a91063f974` | 11 STM pairs and `docs/stm/ts/INVENTORY.md`, personal-data gate at zero hits, commit 3020c0d |
| UNT5-5 Key file for the ts targets | `9957893bbbfb43aabf391e8e600f7eba` | `tools/keys/ts_keys.json` for 102 targets, 50 of them keyed on all columns, commit 11aafd2 |
| UNT5-6 Gap register and scope line | `6df8369f8c2a468c86870250a3db4c57` | `docs/stm/ts/GAPS.md`, 11 XML workflows in scope, shell scripts out, commit 9397674 |

The manager asked these workers to commit straight to `migration/ts-powercenter`, so there are no PRs from the first six tickets; the plan's first PRs come with the unit tickets in phase 4. The persona then paused the board from its chat, since the board has no pause button: the agent stopped the worker it had just started on UNT5-7 (session `39b6a59652ef4cfe80f6b23227177859`, stopped before it pushed anything), moved the ticket back to Todo and left UNT5-7 to UNT5-22 unclaimed. That stop is deliberate. The act shows the plan, the decisions and the first tickets running; the remaining 16 tickets would spend the run's credits and expiry on 108 mappings, which is a project, and the board can be resumed from the same chat. Nothing is red; the act cost 24.4 ACU across the parent and seven workers.

## Pitch, one session per sentence

| Session | Sentence |
|---|---|
| Inventory before funding (`ca69c38544184defb75a9d44463ddd91`) | Devin read two repositories and gave the bank a 23-unit inventory and a wave plan before anyone paid for a model. |
| Snowflake converts, Devin fixes (`4c20f9c5d69246c7b913274c99922597`) | Devin ran Snowflake's own converter, fixed every warning it left, and found a fault in the baseline that nobody else had seen. |
| Six SAS programs, six PRs (`4ea9db2df4bb4d12b82251720ae5ed87`) | Devin fanned six SAS programs out to six engineers, collected six proven PRs, and then worked the review comments on all of them. |
| One honest red (`7b73810896e24de3b3dee1ff8ccae8a5`) | Devin compared every target to the legacy answer row by row inside Snowflake and left the one failing unit red with the reason. |
| Credits (`6ff944c32e3c4db6a370fc0282befdc1`) | Devin read ACCOUNT_USAGE and put a credit figure against every unit and phase of the migration, waste included. |
| Plan, approve, tickets run (`f44163a7c9034bb185a8d76ddbb4acee`) | Work arrives as tickets from an approved plan, and the first six landed on a branch before anyone wrote a unit. |
| The live one | A SAS program the audience watched start from an empty prompt box comes back as a tested, parity-checked PR. |

## The live prompt

Paste this as the persona into a new session (also at `/home/ubuntu/prompts/snowflake/prompts/act5_live.md` on the builder's machine):

```
Rewrite the SAS program legacy/sas/programs/load_customer_accounts.sas in uc-informatica-sas-to-dbt as a dbt project on Snowflake. Work on a branch off baseline/SF_20261015_DS, write staging, intermediate and mart models from the legacy source and the STM in docs/stm/sas_stm.md into dbt/sas_load_customer_accounts/, with tests mirroring tools/keys/sas_keys.json, and build into DBT_SF_20261015_DS as the demo user (SF_DEMO_* secrets: user, password, role, warehouse SF_20261015_DS_WH, database DEVIN_MIGRATION_DEMO, account in SNOWFLAKE_ACCOUNT).

Run parity against BASELINE_SF_20261015_DS with tools/parity_diff.py (DuckDB tool; a thin Snowflake wrapper beside it is fine, its tolerances are not) and open one PR with the parity table and the dbt test summary in the body. Follow the org skill snowflake-dbt-target-standard. Testing is pre-approved, leave the PR open, request Devin Review.
```

The pre-run version of this same unit is PR #56, so the room can compare its result with one that already exists. Expect the three data-caused test failures to appear again; that is the point.

## Known limits

- Act 6 stops after six tickets. The board was paused on purpose from the persona's chat; UNT5-7 to UNT5-22 sit in Todo, no unit PR exists yet, and the worker started on UNT5-7 was stopped before it pushed. The 50 targets with no natural key are compared on all columns.
- PR #56 is red. Three dbt tests fail (`not_null` on `UTILIZATION_PCT` and `RISK_RATING`, the composite key on `ACCT_EXCEPTIONS`). The baseline fails them identically, so the cause is the legacy data. The tests stay because the target standard requires them.
- Oracle converted 0 percent. The three `ts-informatica-powercenter` scripts are ksh wrappers and procedure calls; the SQL bodies they call are not in the repository and there are no table definitions to stub, so `ORACLE_SF_20261015_DS` is empty and act 1 documents why.
- **Act 1 built into `SCAI_SF_20261015_DS`**, not `DBT_SF_20261015_DS`, by instruction, so SnowConvert's output and the hand-written SAS projects can be told apart in Snowflake.
- The baseline had a loader fault. Timestamps were read as seconds and `GENDER` as a boolean. Act 1 found it; the loader on PR #53 was fixed and the five affected tables reloaded (commit `2b57542`, 20.8 s). Act 1 and act 3 re-ran against the reloaded data; models built before the reload that nobody re-ran would compare against the old values.
- Baseline waste row. A mistyped warehouse `SF_SF_20261015_DS_WH` ran for 0.0647 credits before it was dropped. The credits page shows it as its own row.
- Devin Review on PR #53 posted five findings. Commit 8316570 fixes the teardown's wildcard name match, validates the run token before it reaches SQL and clears a reused parity work directory. The `%let` stripping in `tools/sas_lineage.py` (a copied tool from `devin/sas-track`) and the loader's ACCOUNTADMIN default are answered on the PR and left as they are.
- The licence figure is an assumption. No Informatica plus SAS licence cost exists in either repository, so act 4's comparison uses a planning assumption and says so on the page.
- **Two Devin Review findings on PR #60 are left as decisions**, and two flags on PRs #54 and #56 were replied to without a change: the January valuation date gives zero earned premium for every policy on #54 (parity never exercises the loss-ratio path, a later-dated baseline would), and #56 does not need a new mapping document because nothing departs from `docs/stm/sas_stm.md`. The `accepted_values` tests that make an unknown code fail red stay as they are.
- DeepWiki timing. Act 0 reported no DeepWiki index on either repository. The repositories had been granted to the organisation an hour earlier and their index jobs completed later that morning; both now have a wiki and search index. Act 0's inventory came from the repository tools and the files.
- Workflow children ran in the parent's mode. The contract expected normal-mode children under a fusion parent; `run_workflow` created them in fusion mode. Their work is unaffected.
- PowerCenter exports are counted only. The health-records exports carry real names and addresses; act 0 counted 567 personal-data fields by column name, and the branches, PRs and this guide carry the counts alone. Those units are in a blocked wave.
- Pre-run PRs #1, #2, #13 to #16 and #18 carry a red validation comment from act 3's first pass; they are earlier work on the repository, outside this run, and were left as they were.

## Teardown

From a clone of `baseline/SF_20261015_DS`, with `SNOWFLAKE_PAT` in the environment:

```bash
python3 baseline/SF_20261015_DS/teardown.py --token SF_20261015_DS   # list what would go
bash baseline/SF_20261015_DS/teardown.sh --yes                       # drop it
```

It lists the run's objects by name and by tag, drops the warehouse, users, schemas, roles and monitor in that order, then prints `select count(*) from snowflake.account_usage.tag_references where tag_name in ('RUN','EXPIRES') and tag_value like 'SF_%'` and the warehouse's last metering row. Afterwards remove the six ViewOnly secrets (`SF_DEMO_USER`, `SF_DEMO_PASSWORD`, `SF_DEMO_ROLE`, `SF_DEMO_WAREHOUSE`, `SF_DEMO_DATABASE`, `SF_RUN_TOKEN`) under Settings, Secrets. The sessions and the PRs stay; nothing is merged.
