| Mapping | Transformation | Port / element | Informatica code (verbatim) | XML line | PySpark conversion (snippet or `file:lines`) | Confidence | Reason |
|---|---|---|---|---:|---|---|---|
| m_demo_mapping2 | SQ_demo_source1 | Sql Query | `` | 151 | `m_demo_mapping2.py:14` (`ctx.io.read` pass-through) | MEDIUM | A filter or reorder would be visible only on affected rows; the seed has no such edge case. |
| m_demo_mapping2 | EXPTRANS | LEAD_CO_MNE | `LEAD_CO_MNE` | 164 | `m_demo_mapping2.py:14` | HIGH | |
| m_demo_mapping2 | EXPTRANS | BRANCH_CO_MNE | `BRANCH_CO_MNE` | 165 | `m_demo_mapping2.py:14` | HIGH | |
| m_demo_mapping2 | EXPTRANS | MIS_DATE | `MIS_DATE` | 166 | `m_demo_mapping2.py:14` | HIGH | |
| m_demo_mapping2 | EXPTRANS | ID | `ID` | 167 | `m_demo_mapping2.py:14` | HIGH | |
| m_demo_mapping2 | EXPTRANS | DESCRIPTION | `DESCRIPTION` | 168 | `m_demo_mapping2.py:14` | HIGH | |
| m_demo_mapping2 | EXPTRANS | SHORT_NAME | `SHORT_NAME` | 169 | `m_demo_mapping2.py:14` | HIGH | |
| m_demo_mapping2 | EXPTRANS | Key | `Key` | 170 | `m_demo_mapping2.py:29-32` | HIGH | |
| m_demo_mapping2 | EXPTRANS | LEAD_CO_MNE1 | `LEAD_CO_MNE1` | 171 | `m_demo_mapping2.py:23-28` | MEDIUM | This lookup copy is dead downstream; parity would not catch a wrong dead-port value. |
| m_demo_mapping2 | EXPTRANS | BRANCH_CO_MNE1 | `BRANCH_CO_MNE1` | 172 | `m_demo_mapping2.py:23-28` | MEDIUM | This lookup copy is dead downstream; parity would not catch a wrong dead-port value. |
| m_demo_mapping2 | EXPTRANS | MIS_DATE1 | `MIS_DATE1` | 173 | `m_demo_mapping2.py:23-28` | MEDIUM | This lookup copy is dead downstream; parity would not catch a wrong dead-port value. |
| m_demo_mapping2 | EXPTRANS | DESCRIPTION1 | `DESCRIPTION1` | 174 | `m_demo_mapping2.py:23-28` | MEDIUM | This lookup copy is dead downstream; parity would not catch a wrong dead-port value. |
| m_demo_mapping2 | EXPTRANS | SHORT_NAME1 | `SHORT_NAME1` | 175 | `m_demo_mapping2.py:23-28` | MEDIUM | This lookup copy is dead downstream; parity would not catch a wrong dead-port value. |
| m_demo_mapping2 | EXPTRANS | New_Flag | `IIF(ISNULL(Key),'Insert')` | 176 | `m_demo_mapping2.py:33` | HIGH | |
| m_demo_mapping2 | EXPTRANS | MD5_src | `AES_DECRYPT(LEAD_CO_MNE1, SUBSTR(SHORT_NAME,1,3), 256)` | 177 | `m_demo_mapping2.py:34` (`LEGACY_AES_VALUE`) | LOW (DECISION-4) | Rejected real AES-256: input is plaintext and key is not a valid 256-bit key; seed parity cannot distinguish another unequal sentinel. |
| m_demo_mapping2 | EXPTRANS | MD5_tgt | `MD5(LEAD_CO_MNE || BRANCH_CO_MNE || MIS_DATE || DESCRIPTION || SHORT_NAME)` | 178 | `m_demo_mapping2.py:35-40` | HIGH | |
| m_demo_mapping2 | EXPTRANS | Changed_Flag | `IIF(NOT ISNULL(Key) AND  (MD5_tgt != MD5_src),'Update')` | 179 | `m_demo_mapping2.py:41-47` | HIGH | |
| m_demo_mapping2 | EXPTRANS | o_CREATED_BY | `'IDWUSER'` | 180 | `m_demo_mapping2.py:48` | HIGH | |
| m_demo_mapping2 | EXPTRANS | o_CREATED_TIME | `SYSDATE` | 181 | `m_demo_mapping2.py:49-52` | HIGH | |
| m_demo_mapping2 | EXPTRANS | o_UPDATED_BY | `'IDWUSER'` | 182 | `m_demo_mapping2.py:53` | HIGH | |
| m_demo_mapping2 | EXPTRANS | o_UPDATED_TIME | `SYSDATE` | 183 | `m_demo_mapping2.py:54-57` | HIGH | |
| m_demo_mapping2 | RTRTRANS | Insert | `New_Flag='Insert'` | 188 | `m_demo_mapping2.py:61-64` | HIGH | |
| m_demo_mapping2 | RTRTRANS | Update | `Changed_Flag='Update'` | 190 | `m_demo_mapping2.py:65` | HIGH | |
| m_demo_mapping2 | RTRTRANS | DEFAULT1 | *(default group; no expression)* | 189 | `m_demo_mapping2.py:61-65` (no default branch) | MEDIUM | A wrong NULL-filling/default output would appear only for neither-group rows; the seed does not exercise one. |
| m_demo_mapping2 | LKPTRANS | Lookup condition | `ID = ID1` | 286 | `m_demo_mapping2.py:16-21` | HIGH | |
| m_demo_mapping2 | LKPTRANS | Lookup policy | `Use Any Value` | 285 | `lookup(... policy="Use Any Value")` at `m_demo_mapping2.py:16-21` | LOW (DECISION-3) | Rejected first physical match; that would select Key 2 rather than Key 99 for REC00002. |
| m_demo_mapping2 | SEQTRANS | State | `Start Value=0; Increment By=1; Current Value=57; Cycle=NO; End Value=9223372036854775807` | 317-321 | `m_demo_mapping2.py:60-64` | LOW (DECISION-5) | Rejected unordered assignment; values follow source physical ordinal among inserts, and only this seed order controls parity. |
| m_demo_mapping2 | SEQTRANS | NEXTVAL | `NEXTVAL` | 315 | `sequence_nextval(..., current_value=57)` at `m_demo_mapping2.py:60-64` | HIGH | |
| m_demo_mapping2 | SEQTRANS | CURRVAL | `CURRVAL` | 316 | Not converted | NOT MIGRATED | Unconnected sequence output; adding it cannot affect parity. |
| m_demo_mapping2 | UPDTRANS | Update Strategy Expression | `DD_UPDATE` | 341 | `m_demo_mapping2.py:65` | HIGH | |
| m_demo_mapping2 | Mapping instances | `demo_target1_INS`, `demo_target1_UPD` | `INSTANCE` elements over target definition `demo_target1` | 345-346 | `m_demo_mapping2.py:10` and returned dict at `m_demo_mapping2.py:104` | LOW (DECISION-6) | Rejected unioning instances into one output; separate materialisation preserves the INS/UPD parity control. |
| m_demo_mapping2 | LKPTRANS | CREATED_BY; CREATED_TIME; UPDATED_BY; UPDATED_TIME; ACTIVE_FLAG; START_DATE; END_DATE | Lookup output ports with no outgoing connector | 273-279 | Not converted | NOT MIGRATED | Dead lookup ports; materialising them would not affect either target instance. |
| m_demo_mapping2 | RTRTRANS | LEAD_CO_MNE11; BRANCH_CO_MNE11; MIS_DATE11; DESCRIPTION11; SHORT_NAME11; New_Flag1; Changed_Flag1; o_UPDATED_BY1; o_UPDATED_TIME1; Key1 | `REF_FIELD` ports in Insert group | 215-226 | Not converted | NOT MIGRATED | Dead Insert-group ports; wiring them would expose lookup copies or flags that have no target connector. |
| m_demo_mapping2 | RTRTRANS | LEAD_CO_MNE13; BRANCH_CO_MNE13; MIS_DATE13; DESCRIPTION13; SHORT_NAME13; New_Flag3; Changed_Flag3; o_CREATED_BY3; o_CREATED_TIME3 | `REF_FIELD` ports in Update group | 233-241 | Not converted | NOT MIGRATED | Dead Update-group ports; connected update fields use the source-valued `*4` ports and `o_UPDATED_*3`. |
| m_demo_mapping2 | RTRTRANS / UPDTRANS | LEAD_CO_MNE3; BRANCH_CO_MNE3; MIS_DATE3; ID2; DESCRIPTION3; SHORT_NAME3; LEAD_CO_MNE12; BRANCH_CO_MNE12; MIS_DATE12; DESCRIPTION12; SHORT_NAME12; New_Flag2; Changed_Flag2; o_CREATED_BY2; o_CREATED_TIME2; o_UPDATED_BY2; o_UPDATED_TIME2; Key2 | `REF_FIELD` ports in DEFAULT1 group | 245-262 | Not converted | NOT MIGRATED | DEFAULT1 is unconnected; name matching these ports to UPDTRANS would incorrectly materialise discarded rows. |

Rubric: **HIGH** — semantics are unambiguous in the XML **and** at least one baseline row would fail parity if the conversion were wrong. **MEDIUM** — unambiguous, but weakly exercised: the output is constant or degenerate in the seed data, so parity cannot catch a wrong conversion. **LOW** — the conversion rests on a judgement call the XML does not determine; the row names the rejected alternative. **NOT MIGRATED** — deliberately not converted (for example, a port with no outgoing CONNECTOR).

Counts: HIGH 19, MEDIUM 7, LOW 5, NOT MIGRATED 5 (36 rows total). LOW rows rest on DECISION-3 (lookup policy), DECISION-4 (AES sentinel), DECISION-5 (sequence order), and DECISION-6 (per-instance materialisation).
