# Informatica conversion comparison

This headline is assembled from the committed, frozen per-mapping conversion
tables. Counts were parsed from each table's confidence-count section; they
were not re-derived from the XML.

## Headline counts

| Mapping | Total | Migrated (HIGH + MEDIUM + LOW) | Deliberately not migrated | HIGH | MEDIUM | LOW | NOT MIGRATED |
|---|---:|---:|---:|---:|---:|---:|---:|
| `m_demo_mapping1` | 84 | 74 | 10 | 51 | 12 | 11 | 10 |
| `m_demo_mapping2` | 38 | 32 | 6 | 20 | 8 | 4 | 6 |
| `m_demo_mapping3` | 36 | 20 | 16 | 18 | 1 | 1 | 16 |
| **Overall** | **158** | **126** | **32** | **89** | **21** | **16** | **32** |

The totals intentionally preserve the per-mapping table row counts, including
the duplicate dead-port entries called out by `m_demo_mapping1`.

## Prioritised review list

1. **DECISION-1 — aggregator pass-through row selection (`m_demo_mapping1`,
   L443–453).** Selecting the highest `TX_ID` rather than arrival order can
   silently change otherwise plausible pass-through fields.
2. **DECISION-2 — sequence consumption order (`m_demo_mapping1`, L430).**
   Arrival-order sequence consumption would produce plausible but wrong keys.
3. **DECISION-3 — lookup multiple-match policy (`m_demo_mapping1`, L498/L624;
   `m_demo_mapping2`, L280).** Stored physical ordinals are required to make
   `Use Last Value` and `Use Any Value` deterministic.
4. **DECISION-4 — AES sentinel (`m_demo_mapping2`, L190–191).** Replacing the
   literal sentinel with a real hash changes update classification plausibly.
5. **DECISION-5 — per-instance materialisation (`m_demo_mapping2`, L328–340).**
   Same-named discarded `DEFAULT1` ports must not be mistaken for update ports.
6. **DECISION-6 — separate router outputs (`m_demo_mapping3`, L1009–1010).**
   Combining the two target instances loses a key parity control.
7. MEDIUM-confidence SQL overrides, pass-through expressions, and constants
   remain listed in the per-mapping tables for targeted review.

## LOW rows grouped by decision

| Decision | Mapping(s) | LOW rows / judgement covered |
|---|---|---|
| DECISION-1 | `m_demo_mapping1` | Aggregator pass-through `TX_ID`, `TX_DTTM`, `o_ACCT_DESC`, superseded `TX_AMT`, `o_crdt_trim`, `CLSR_DT`, `ACCT_STAT_CD`, `CR8_DT`, `o_ACCT_ID`, and `o_acc_trim`. |
| DECISION-2 | `m_demo_mapping1` | `SEQ_GEN.NEXTVAL` consumption order for `demo_target6.ACCT_KEY`. |
| DECISION-3 | `m_demo_mapping1`, `m_demo_mapping2` | Lookup multiple-match policies and physical-order tie-breaks. |
| DECISION-4 | `m_demo_mapping2` | AES sentinel used by update classification. |
| DECISION-5 | `m_demo_mapping2` | Insert/update per-instance materialisation and router-port interpretation. |
| DECISION-6 | `m_demo_mapping3` | Separate target-instance materialisation. |

Detailed expressions, XML line numbers, conversion locations, and reasons:

- [m_demo_mapping1](conversion_table/m_demo_mapping1.md)
- [m_demo_mapping2](conversion_table/m_demo_mapping2.md)
- [m_demo_mapping3](conversion_table/m_demo_mapping3.md)
- [workflow](conversion_table/workflow.md)
