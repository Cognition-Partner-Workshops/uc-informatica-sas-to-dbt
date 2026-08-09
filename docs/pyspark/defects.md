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
