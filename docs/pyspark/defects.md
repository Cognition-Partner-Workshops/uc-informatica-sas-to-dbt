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
