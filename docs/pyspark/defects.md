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
