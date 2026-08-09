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
