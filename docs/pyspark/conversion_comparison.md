# Informatica → PySpark conversion comparison

- Total rows: 22
- Migrated: 22
- Not-migrated-by-design: 0
- Confidence split: {'HIGH': 13, 'MEDIUM': 9, 'LOW': 0, 'NOT MIGRATED': 0}
- Review these first: LOW rows, then MEDIUM rows covering workflow failure paths.
- LOW rows grouped by decision: see `docs/pyspark/decisions.md`.

## Confidence rubric

- **HIGH** — semantics unambiguous in the XML AND at least one baseline row would fail parity if
  the conversion were wrong.
- **MEDIUM** — unambiguous but weakly exercised: the output is constant/degenerate in the seed
  data, so parity cannot catch a wrong conversion.
- **LOW** — the conversion rests on a judgement call the XML does not determine; name the
  alternative that was rejected.
- **NOT MIGRATED** — deliberate (e.g. dead port with no outgoing connector); name every one.


## workflow

| Mapping | Transformation | Port / Object | XML line | Original Informatica code (verbatim) | Converted PySpark code (file:lines + snippet) | Confidence | Reason & closing action |
|---|---|---|---:|---|---|---|---|
| wf_demo_mapping | Decision1 | Decision expression | 1159 | `$s_m_demo_mapping2.Status = 1` | `workflow/runner.py` decision1 | HIGH | Recovered directly from XML; add a failing mapping2 fixture (covered by workflow tests). |
| wf_demo_mapping | Decision2 | Decision expression | 1156 | `$s_m_demo_mapping1.Status = 1` | `workflow/runner.py` decision2 | HIGH | Recovered directly from XML; add a failing mapping1 fixture (covered by workflow tests). |
| wf_demo_mapping | Decision3 | Decision expression | 1162 | `$s_m_demo_mapping3.Status = 1` | `workflow/runner.py` decision3 | HIGH | Recovered directly from XML; add a failing mapping3 fixture (covered by workflow tests). |
| wf_demo_mapping | Link | Start → s_m_demo_mapping2 | 1471 | `` | `workflow/runner.py` start dispatch | MEDIUM | Empty condition is unexercised on a green run; closing action: retain failure-path workflow fixture. |
| wf_demo_mapping | Link | s_m_demo_mapping2 → Decision1 | 1473 | `` | `workflow/runner.py` mapping2 decision | MEDIUM | Empty condition is unexercised on a green run; closing action: retain injected outcome tests. |
| wf_demo_mapping | Link | Decision1 → Failed_Email1 | 1467 | `$Decision1.Condition = 0` | `workflow/runner.py` email dispatch | MEDIUM | Failure email path is not exercised by green seed data; closing action: injected mapping2 failure test. |
| wf_demo_mapping | Link | Decision1 → s_m_demo_mapping1 | 1470 | `` | `workflow/runner.py` unconditional mapping1 dispatch | HIGH | Legacy defect intentionally reproduced; test mapping2 failure path. |
| wf_demo_mapping | Link | s_m_demo_mapping1 → Decision2 | 1472 | `` | `workflow/runner.py` mapping1 decision | MEDIUM | Empty condition is unexercised on a green run; closing action: injected outcome tests. |
| wf_demo_mapping | Link | Decision2 → Failed_Email2 | 1465 | `$Decision2.Condition = 0` | `workflow/runner.py` email dispatch | MEDIUM | Failure email path is not exercised by green seed data; closing action: injected mapping1 failure test. |
| wf_demo_mapping | Link | Decision2 → s_m_demo_mapping3 | 1469 | `$Decision2.Condition = 1` | `workflow/runner.py` mapping3 dispatch | HIGH | Recovered and exercised by success/failure fixtures. |
| wf_demo_mapping | Link | Failed_Email2 → Control | 1468 | `` | `workflow/runner.py` stop-parent return | MEDIUM | Control path is not exercised by green seed data; closing action: injected mapping1 failure test. |
| wf_demo_mapping | Link | s_m_demo_mapping3 → Decision3 | 1474 | `` | `workflow/runner.py` mapping3 decision | MEDIUM | Empty condition is unexercised on a green run; closing action: injected outcome tests. |
| wf_demo_mapping | Link | Decision3 → SuccessEmail | 1466 | `$Decision3.Condition = 1` | `workflow/runner.py` success email | HIGH | Exact success payload covered by workflow tests. |
| wf_demo_mapping | Link | Decision3 → Failed_Email3 | 1475 | `$Decision3.Condition = 0` | `workflow/runner.py` failure email | MEDIUM | Failure email path is not exercised by green seed data; closing action: injected mapping3 failure test. |
| wf_demo_mapping | Email | Failed_Email2 | 1140 | `Sessio 's_m_demo_mapping1' failed` | `workflow/runner.py:EMAILS` | HIGH | Byte-for-byte recovered string; exact assertion present. |
| wf_demo_mapping | Email | SuccessEmail | 1145 | `Session s_m_demo_mapping3 executed successfully` | `workflow/runner.py:EMAILS` | HIGH | Byte-for-byte recovered string; exact assertion present. |
| wf_demo_mapping | Email | Failed_Email1 | 1150 | `Dataload s_m_demo_mapping2 was failed to execute` | `workflow/runner.py:EMAILS` | HIGH | Byte-for-byte recovered string; exact assertion present. |
| wf_demo_mapping | Email | Failed_Email3 | 1167 | `Dataload  s_m_demo_mapping3t was failed to execute` | `workflow/runner.py:EMAILS` | HIGH | Byte-for-byte recovered string; exact assertion present. |
| wf_demo_mapping | Control | Control option | 1153 | `Stop parent` | `workflow/runner.py` stop-parent return | MEDIUM | Legacy control behavior is weakly exercised; closing action: injected mapping1 failure test. |
| wf_demo_mapping | Binding | s_m_demo_mapping2 → m_demo_mapping2 | 1236 | `MAPPINGNAME = "m_demo_mapping2"` | `workflow/runner.py` mapping dispatch | HIGH | Session binding recovered from XML. |
| wf_demo_mapping | Binding | s_m_demo_mapping1 → m_demo_mapping1 | 1169 | `MAPPINGNAME = "m_demo_mapping1"` | `workflow/runner.py` mapping dispatch | HIGH | Session binding recovered from XML. |
| wf_demo_mapping | Binding | s_m_demo_mapping3 → m_demo_mapping3 | 1365 | `MAPPINGNAME = "m_demo_mapping3"` | `workflow/runner.py` mapping dispatch | HIGH | Session binding recovered from XML. |
