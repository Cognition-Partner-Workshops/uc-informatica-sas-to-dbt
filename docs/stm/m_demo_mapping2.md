# m_demo_mapping2 — ledger insert/update streams

## Contract and evidence

Source of truth: `legacy/informatica/wf_demo_mapping.XML`, mapping
`m_demo_mapping2`, its CONNECTORs and target instances
`demo_target1_INS` / `demo_target1_UPD`. Accepted behavior:
`tools/informatica_baseline.py::mapping2` and `load`.
Frozen outputs: `baseline/informatica/demo_target1_INS.csv` (4 rows) and
`demo_target1_UPD.csv` (3 rows). Keys: ID for both streams.
Only INFA_SOURCE staging refs are used in computation; INFA_BASELINE is
validation evidence, never a model input.

## Transformation chain

| Legacy transformation | dbt intermediate | Semantics |
|---|---|---|
| SQ_demo_source1 | int_m_demo_mapping2__sq | All six source fields; no filter/distinct/override |
| LKPTRANS | int_m_demo_mapping2__lookup | Static DEMO_TARGET1 pre-state, joined on source.ID = lookup.ID |
| EXPTRANS | int_m_demo_mapping2__expression | Lookup enrichment, new/changed flags, MD5, audit constants |
| RTRTRANS | int_m_demo_mapping2__router | Insert when New_Flag='Insert'; Update when Changed_Flag='Update'; default unused |
| SEQTRANS | int_m_demo_mapping2__sequence | Insert-only 56 + row_number ordered by ID; first value 57, increment 1 |
| UPDTRANS | int_m_demo_mapping2__update_strategy | DD_UPDATE stream; emit update rows rather than mutating pre-state |

Lookup duplicate rule: highest KEY, then highest SEED_ROW within ID, with
null keys last. The XML says “Use Any Value”; the accepted deterministic
baseline resolves that ambiguity. The pre-state stays duplicate-preserving
in staging. The lookup model alone selects one row per ID.

## Column lineage (baseline order)

All six business columns originate in DEMO_SOURCE1, through SQ, lookup
enrichment and EXPTRANS, then the appropriate router stream.

| Target column | DEMO_TARGET1_INS | DEMO_TARGET1_UPD |
|---|---|---|
| KEY | SEQTRANS: 56 + row_number over insert IDs | selected pre-state KEY |
| LEAD_CO_MNE | source.LEAD_CO_MNE unchanged | source.LEAD_CO_MNE unchanged |
| BRANCH_CO_MNE | source.BRANCH_CO_MNE unchanged | source.BRANCH_CO_MNE unchanged |
| MIS_DATE | source.MIS_DATE unchanged | source.MIS_DATE unchanged |
| ID | source.ID unchanged | source.ID unchanged |
| DESCRIPTION | source.DESCRIPTION unchanged | source.DESCRIPTION unchanged |
| SHORT_NAME | source.SHORT_NAME unchanged | source.SHORT_NAME unchanged |
| CREATED_BY | EXPTRANS constant IDWUSER | NULL (unconnected) |
| CREATED_TIME | EXPTRANS pinned 2024-01-31 00:00:00 | NULL (unconnected) |
| UPDATED_BY | NULL (unconnected) | EXPTRANS constant IDWUSER |
| UPDATED_TIME | NULL (unconnected) | EXPTRANS pinned 2024-01-31 00:00:00 |
| ACTIVE_FLAG | NULL (unconnected) | NULL (unconnected) |
| START_DATE | NULL (unconnected) | NULL (unconnected) |
| END_DATE | NULL (unconnected) | NULL (unconnected) |

## Accepted anomaly and domains

The XML's MD5_src is actually AES_DECRYPT(lookup.LEAD_CO_MNE,
SUBSTR(source.SHORT_NAME,1,3),256), while MD5_tgt hashes the concatenation
LEAD_CO_MNE || BRANCH_CO_MNE || MIS_DATE || DESCRIPTION || SHORT_NAME.
These are incomparable spaces. The accepted baseline represents MD5_src
as LEGACY_AES_VALUE and unconditionally flags every non-null matched KEY
as Update, including unchanged business values. This is deliberately not
“fixed” into ordinary MD5 SCD detection; no AES decryption is attempted.
New_Flag is Insert or NULL; Changed_Flag is Update or NULL. Neither is
a target column. Audit-user domain is IDWUSER; ACTIVE_FLAG has no connected
value list and remains NULL. No explicit ABORT occurs in this mapping.
XML default ERROR('transformation error') is not an additional business
guard in the accepted baseline.

Schema tests enforce both ID keys, audit-user domains and update-ID
relationships to the resolved lookup. Frozen parity and offline edge tests
cover unmatched inserts, matched updates, empty inputs and duplicate ties.
Snowflake baseline column names/order were inspected in information_schema
and SELECT *; KEY is uppercase. Loader-inferred DATE/TEXT types for date
strings/all-null fields are not reproduced as business defects: output
values follow the baseline and audit fields use timestamp_ntz.
