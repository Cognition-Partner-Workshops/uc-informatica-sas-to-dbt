# Informatica PowerCenter to PySpark migration report

## Executive decision

This migration reproduces the demonstrated behavior of the PowerCenter workflow
locally and in Snowflake, including several counterintuitive connector paths and
the known `ABORT()` failure. It is strong evidence for retiring PowerCenter for
the exercised contract and seed data. It is not, by itself, evidence that the
workflow is correct for unseen data, production scale, or failure recovery.

The recommendation is **conditional retirement**: proceed only after the
pre-cutover checklist at the end of this report is accepted, and do not present
the current implementation as a transactional replacement. The migrated code
is intentionally bug-compatible with the legacy workflow where parity required
it.

This report is based on the merged integration line at `2c14f99`, which includes
the Snowflake abort proof. The local results cited below were independently
re-verified from a clean clone at integration commit `14ce396`; that matters
because the Snowflake milestone changed `io.py`, `config.py`, `cli.py`, and
`workflow.py` after the individual mapping checks.

## What was migrated

The deliverable contains:

- Three mappings:
  - `m_demo_mapping1`
  - `m_demo_mapping2`
  - `m_demo_mapping3`
- Seven target instances:
  - `demo_target1_INS`
  - `demo_target1_UPD`
  - `demo_target2`
  - `demo_target21`
  - `demo_target3`
  - `demo_target5`
  - `demo_target6`
- One workflow, `wf_demo_mapping`, with the connector-derived execution order:
  `m_demo_mapping2 → m_demo_mapping1 → m_demo_mapping3`.

The shared implementation uses one mapping transformation layer and two IO
implementations. Local CSV and Snowflake execution therefore exercise the same
mapping code; only the `InformaticaIO` implementation differs.

The complete connector-derived field paths are in the
[lineage report](lineage.md). The complete construct-level conversion inventory
is in the [conversion comparison](conversion_comparison.md):

- 247 constructs total
- 144 migrated or represented
- 103 not migrated by design
- HIGH: 111
- MEDIUM: 21
- LOW: 12
- NOT MIGRATED: 103

## How the migration was proved

### Local proof

The clean-clone re-verification at `14ce396` established:

- Baseline target row counts: `4/3/3/3/4/2/2`, in the target order listed above.
- Pytest: **29 passed**.
- `run-workflow --io local`: exit code **0**.
- All seven target CSVs were produced.
- The unmodified `tools/parity_diff.py`, its existing keys file, and its
  `1e-6` tolerance: exit code **0**.
- Comparator verdict: **Overall: PARITY VERIFIED**.

The local comparator is the committed
[parity report](parity_report.txt) in the integration branch. The clean-clone
run used a separate report path and did not overwrite that artifact.

The abort fixture was run through the full workflow:

- Exit code: **1**
- Failing mapping: `m_demo_mapping3`
- Exception:
  `InformaticaAbort: Relationship_to_Subscriber_Code_Labe valuel is null`
- No m3 target files were written.

The current tip after the Snowflake abort milestone has **30** tests; the local
proof number above intentionally remains the independently re-verified **29**
at `14ce396`, rather than mixing results from different commits.

Controls also held in the clean clone:

- No source under `pyspark/informatica/` calls `current_date`,
  `current_timestamp`, `datetime.now`, or `time.time`.
- `git diff origin/main -- legacy tools baseline` is empty.
- The comparator, its keys, and its `1e-6` tolerance were not changed.

### Snowflake proof

The warehouse proof is recorded in
[snowflake_proof.md](snowflake_proof.md). It used the fixed business date
`2024-01-31` and run `20260807073611 UTC` in database
`DEVIN_MIGRATION_DEMO`, with timestamped schemas left standing for inspection:

- `SOURCE_INFORMATICA_20260807073611`
- `BASELINE_INFORMATICA_20260807073611`
- `PYSPARK_INFORMATICA_20260807073611`

The successful run produced all seven targets with counts `4/3/3/3/4/2/2`.
For every target:

- Migrated-minus-baseline returned zero rows.
- Baseline-minus-migrated returned zero rows.
- The single-statement `HASH_AGG` comparison verdict was `PASS`.

The Snowflake abort proof used run `20260807075158`:

- Exit code: **1**
- Failure came from `m_demo_mapping3` and the same
  `InformaticaAbort` message.
- Five tables from mappings 2 and 1 were present.
- m3's two target tables were never created.

The Snowflake implementation adds explicit source row-order materialization,
identifier-case handling, timestamp discipline, and the shared
`TARGET_INSTANCE_SCHEMAS` registry. That registry is validated at write time by
both IO implementations.

The Snowflake-specific choices and limitations are recorded in
[decisions_snowflake.md](decisions_snowflake.md).

## Lineage traps that name matching would get wrong

The migration follows XML `CONNECTOR` edges, not similarly named ports. Several
examples are material to whether the replacement is actually the same workflow:

1. **m1 `demo_target5.FIRST_NM`** comes from
   `lkp_demo_source1.FIRST_NM`, not the same-named `demo_source3` field.
   Likewise, **`demo_target5.CRDT_SCORE`** comes from
   `lkp_demo_source2.CRDT_SCORE`, not the similarly named source 3 column.
2. **m1 `demo_target6.TX_TYPE_CD`** is fed through the lookup call named
   `o_ACCT_ID`; the connector sends that value to `TX_TYPE_CD`. The resulting
   value is the lookup transaction code, not an account ID.
3. **m2 update ports** are fed from the router's `Update` group even though
   `UPDTRANS` contains same-named ports associated with the unconnected
   `DEFAULT1` group. Name matching would route the wrong group and lose update
   rows.
4. **m3 `NEWGROUP1` and `NEWGROUP2`** do not map by suffix or group ordinal:
   `NEWGROUP1` (`ISNULL(Social_Security_Number)`) feeds `demo_target2`, while
   `NEWGROUP2` (`NOT ISNULL(...)`) feeds `demo_target21`.
5. m1's positional Source Qualifier binding maps the `SYSTIMESTAMP` select item
   to `CR8_DT`, and m1's `TX_TYPE_CD` SQL-override output is unconnected. Both
   are connector/position facts, not sensible name-based mappings.

The source paths, target paths, XML references, and observed trap values are
documented in [lineage.md](lineage.md).

## Legacy defects reproduced deliberately

This is a parity migration, not a cleanup release. Where the legacy behavior is
observable and the design contract requires it, the PySpark implementation is
bug-compatible.

### m2 AES/MD5 always-update defect

The legacy `MD5_src` expression applies `AES_DECRYPT` to a lookup value, but the
repository does not contain the ciphertext/key pair or an Informatica runtime
that could recover the result. The conversion therefore uses the documented
`LEGACY_AES_VALUE` sentinel.

The live legacy expression compares:

- `MD5_tgt`: an MD5 hash of the source business fields
- `MD5_src`: the unrecoverable AES-decrypted lookup value

These are incomparable value spaces. Consequently, `MD5_tgt != MD5_src` is
always true for matched rows, and every matched row is flagged `Update`. The
migration reproduces that behavior instead of inventing a decryption result,
returning NULL, or silently correcting the comparison. Those alternatives would
change observable legacy behavior and break parity.

This was the right call for a parity migration, but it is not a claim that the
business rule is desirable. A follow-up correction would need an agreed
cryptographic input/key contract, a same-domain hash definition, a decision on
how existing target rows should be reclassified, and a separately approved
data-reprocessing plan. It should be delivered as an intentional behavior
change, not folded into retirement of PowerCenter.

Other deliberately reproduced behavior includes:

- The m1 positional `SYSTIMESTAMP` binding and resulting business-date value.
- m1's malformed-date expression yielding NULL rather than using the source
  date.
- NULL router semantics for the empty `ACCT_TYP` case.
- m3's hard `ABORT()` behavior and the legacy typo in its message.
- Typed NULLs for unconnected target ports.

The mapping-specific rationale is linked here:

- [m1 decisions](decisions_m_demo_mapping1.md)
- [m2 decisions](decisions_m_demo_mapping2.md)
- [m3 decisions](decisions_m_demo_mapping3.md)

## Decisions where XML does not determine the answer

These are not ordinary row-level conversion omissions. They are decisions made
because the XML leaves a semantic choice open or because required runtime
material is unavailable. They should be reviewed as decisions, not counted as
independent defects.

### m1 aggregator within-group ordering

Nine of the twelve LOW-confidence constructs trace to one decision: which row
supplies aggregator pass-through values within an `ACCT_ID` group. The XML
defines grouping but does not define the transaction order within the group.
The implementation chooses the highest `TX_ID`.

That choice matches the seed baseline. File-order-last also happens to select
the same row on the seed data, so the seed does not discriminate those two
policies. First-row selection would fail the supplied parity case, but that does
not prove highest `TX_ID` is the production policy.

### m1 sequence ordering

The sequence state is explicit, but distributed Spark execution does not inherit
an Informatica partition order. The implementation assigns sequence values
using deterministic `ACCT_ID` ordering. This is preferable to arbitrary
partition order, but the XML does not establish that `ACCT_ID` is the intended
ordering rule for every production input.

### m2 `Use Any Value` winner

The XML does not specify which duplicate lookup row wins for `Use Any Value`.
The implementation chooses deterministically using the highest lookup `Key`.
The duplicate `REC00002` row makes this a concrete decision, not just a
theoretical implementation detail.

### m2 AES sentinel

The sentinel is the explicit substitute for an unrecoverable runtime result.
It preserves the observed always-update behavior but cannot establish what a
real Informatica AES evaluation would have returned under unavailable
credentials and ciphertext.

The aggregate [conversion comparison](conversion_comparison.md) groups the LOW
rows by these underlying decisions; it does not pretend that twelve rows
represent twelve independent uncertainties.

## Trust assessment

### What the evidence supports

I would stake the following parts of the retirement decision on the evidence
available:

- The connector-derived field mappings and target-instance assignments for the
  supplied workflow.
- The workflow order `2 → 1 → 3` and fail-fast behavior.
- The reproduced NULL, date/timestamp formatting, lookup-collapse, sequence
  rendering, and abort behavior on the exercised paths.
- Exact local parity for the seven committed seed targets.
- Exact warehouse parity for the seven timestamped Snowflake targets under the
  successful proof run.
- The fact that local and Snowflake runs use the same transformation logic with
  IO-specific handling.

### What the evidence does not establish

The evidence does **not** license these stronger claims:

- Parity is against a small seed dataset with only 2–4 rows per target, produced
  by `tools/informatica_baseline.py` from the same seed inputs. It demonstrates
  faithful reproduction on exercised paths, not correctness on unseen data.
- MEDIUM and LOW ratings exist precisely because the seed does not discriminate
  some alternatives. A passing parity result cannot turn those alternatives
  into HIGH-confidence facts.
- The Snowflake `MINUS` and `HASH_AGG` checks compare tables whose schemas and
  types are both built from the same `TARGET_INSTANCE_SCHEMAS` registry. A
  shared type-domain or projection error can therefore pass both sides of the
  warehouse comparison.
- The workflow is fail-fast but not transactional across mapping writes. A
  failure in m3 can leave m1 and m2 outputs committed. Consumers can observe an
  internally inconsistent run schema until a rerun or cleanup occurs.
- The abort proof covers a particular failure point and workload. It does not
  establish transactional behavior for every possible failure after a target
  create, append, connector error, or infrastructure failure.
- There is no CI pipeline that automatically reruns these checks on later
  changes. The evidence is a point-in-time proof, not a continuously enforced
  guarantee.
- The proof does not establish production-scale performance, partition behavior,
  spill behavior, operational alerting, or recovery time.

The non-transactional Snowflake behavior is not hidden by this report: the
successful and abort evidence, along with the recommended production remedies,
are recorded in [snowflake_proof.md](snowflake_proof.md).

## Pre-cutover checklist

Before retiring the PowerCenter workflow, a human owner should:

1. **Resolve the LOW decisions.** Obtain the production rule for m1
   aggregator pass-through ordering, sequence ordering, and m2 `Use Any Value`
   duplicate resolution. Record the decision and update the conversion contract
   before treating those paths as production-approved.
2. **Approve or correct the m2 hash behavior.** Decide whether the
   `LEGACY_AES_VALUE` sentinel and always-update behavior are to remain
   bug-compatible or be corrected in a separately versioned business-logic
   change. Do not silently change it during cutover.
3. **Test production-shaped data.** Add representative duplicate lookups,
   multiple transactions per account, NULL/empty/whitespace cases, date
   boundaries, numeric extremes, and both m3 router branches. Include cases
   that distinguish the MEDIUM and LOW alternatives.
4. **Validate independently of the shared target registry.** Compare target
   schema and values against independently defined expectations, not only tables
   generated by `TARGET_INSTANCE_SCHEMAS`.
5. **Choose a publication/recovery protocol.** Add a transaction, swap-on-success
   staging schema, or run-status/consumer gate before production consumers can
   read a partially completed Snowflake run.
6. **Define failure cleanup.** Specify ownership, retention, and cleanup for
   timestamped successful and aborted schemas, including a rerun after a partial
   write.
7. **Rehearse operational controls.** Confirm credentials, warehouse sizing,
   permissions, query-history evidence, logging, alert routing, retries, and
   rollback ownership.
8. **Automate the proof.** Put the local parity, abort, protected-tree, and
   time-discipline checks into CI or an equivalent release gate. The current
   repository does not rerun them automatically.
9. **Run a parallel cutover comparison.** Execute the replacement beside
   PowerCenter on a production-shaped sample, inspect all seven target
   instances, and obtain sign-off for every MEDIUM/LOW decision.
10. **Only then retire PowerCenter.** Keep a rollback window and preserve the
    legacy workflow and evidence until the first production runs complete under
    the agreed recovery protocol.

## Milestones and supporting artifacts

The implementation milestones merged into the integration branch are:

- [#24 shared scaffold and design contract](https://github.com/Cognition-Partner-Workshops/uc-informatica-sas-to-dbt/pull/24)
- [#29 connector-derived field-level lineage](https://github.com/Cognition-Partner-Workshops/uc-informatica-sas-to-dbt/pull/29)
- [#27 m_demo_mapping1](https://github.com/Cognition-Partner-Workshops/uc-informatica-sas-to-dbt/pull/27)
- [#28 m_demo_mapping2](https://github.com/Cognition-Partner-Workshops/uc-informatica-sas-to-dbt/pull/28)
- [#26 m_demo_mapping3](https://github.com/Cognition-Partner-Workshops/uc-informatica-sas-to-dbt/pull/26)
- [#33 end-to-end workflow parity and assembled comparison table](https://github.com/Cognition-Partner-Workshops/uc-informatica-sas-to-dbt/pull/33)
- [#37 Snowflake execution and warehouse parity proof](https://github.com/Cognition-Partner-Workshops/uc-informatica-sas-to-dbt/pull/37)
- [#38 Snowflake ABORT() proof](https://github.com/Cognition-Partner-Workshops/uc-informatica-sas-to-dbt/pull/38)

Primary committed evidence:

- [Connector-derived lineage](lineage.md)
- [Conversion comparison](conversion_comparison.md)
- [Local parity report](parity_report.txt)
- [Snowflake proof](snowflake_proof.md)
- [m_demo_mapping1 decisions](decisions_m_demo_mapping1.md)
- [m_demo_mapping2 decisions](decisions_m_demo_mapping2.md)
- [m_demo_mapping3 decisions](decisions_m_demo_mapping3.md)
- [Snowflake decisions](decisions_snowflake.md)
