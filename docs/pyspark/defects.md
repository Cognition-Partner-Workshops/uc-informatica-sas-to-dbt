# Legacy defects reproduced

## Milestone 0

These behaviors are intentionally reproduced rather than fixed:

- Empty `Decision1 → s_m_demo_mapping1` condition at XML line 1470 causes mapping1 to run even
  when mapping2 fails.
- `sq_demo_source4.TX_TYPE_CD` receives positional `STRCMP(...)` at line 580 and has no outgoing
  connector; the computed value is discarded.
- `sq_demo_source4.CR8_DT` receives positional bare `SYSTIMESTAMP` at line 580.
- `TO_DATE(TO_CHAR(SYSDATE),'DD/MM/YYYY')` at line 662 is unparseable for the pinned date and
  yields NULL.
- The AES/MD5 comparison is incomparable; the baseline's constant representation is preserved.
- Email typos and spacing are preserved: lines 1140, 1150, and 1167.

## m_demo_mapping1
These mapping-1 defects are reproduced rather than fixed:

- **XML line 580 — positional SQL override discard.** The fourteenth SELECT
  expression, `STRCMP(demo_source4.ACCT_STAT_CD,demo_source3.TX_TYPE_CD)`, binds
  positionally to `sq_demo_source4.TX_TYPE_CD`. That port has no outgoing connector,
  so the computed value is placed in `WRK_SQL_TX_TYPE_CD` and discarded. It is
  not allowed to reach `demo_target6.TX_TYPE_CD`; the target instead receives the
  unconnected lookup return from `lkp_TRANS1`.
- **XML line 662 — unparsable derived date.** `TO_DATE(TO_CHAR(SYSDATE),'DD/MM/YYYY')`
  evaluates through the shared `to_char` and `to_date` primitives. The default
  `TO_CHAR` rendering is `01/31/2024 00:00:00`, which cannot be parsed by
  `DD/MM/YYYY`, so `demo_target3.SELL_ST_DT` is NULL for all four rows. The defect
  is intentionally reproduced rather than replaced with the business date.

## m_demo_mapping2
These behaviors are intentionally reproduced rather than fixed:

- **AES/MD5 comparison defect (XML lines 177-179).** `AES_DECRYPT(...)` produces a value
  incomparable with the hexadecimal `MD5(...)`, so every matched row is flagged `Update`.
  The migration reproduces this defect rather than fixing the comparison.
- **Two-argument IIF NULL branches (XML lines 176 and 179).** `New_Flag` is NULL for matched
  rows and `Changed_Flag` is NULL for unmatched rows. The migration reproduces this defect rather
  than adding false branches.
- **Dead ports and DEFAULT1 group.** Lookup ports `BRANCH_CO_MNE1`, `MIS_DATE1`,
  `DESCRIPTION1`, and `SHORT_NAME1` are carried into the expression/router but have no target
  connector; RTRTRANS `DEFAULT1` (XML lines 245-262) has no outgoing connector. These are
  reproduced as dead/not-migrated outputs rather than invented target writes.

## m_demo_mapping3
- **RECOVERED DEFECT — SQL override silently discards NULL member types.** XML line 916 filters
  with `demo_source2.Member_Type_Code is not null`; the implementation reproduces this and the
  seed row Member_ID 30005 is absent from both outputs rather than fixing the discard.
- **RECOVERED DEFECT — dead same-name label port.** XML line 1086 connects
  `EXPTRANS.o_Relationship_to_Subscriber_Code_Label` to the router. The pass-through port at
  XML line 942 has no outgoing connector, so the implementation reproduces the guarded `o_` port
  as the label source rather than name-matching the dead port.
- **RECOVERED DEFECT — DEFAULT1 silently drops rows.** XML lines 993–1006 define DEFAULT1 output
  ports and XML line 949 defines the default group, but no DEFAULT1 port has an outgoing connector.
  The implementation reproduces the missing edge and does not route DEFAULT1 anywhere; the
  mutually exclusive conditions make it unreachable in the normal seed.
