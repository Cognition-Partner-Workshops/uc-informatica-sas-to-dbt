# Workflow conversion table

Source: `legacy/informatica/wf_demo_mapping.XML`, workflow elements
L1465–1475, task definitions L1136–1168, and session attributes
L1217, L1346, and L1434.

| Mapping | Transformation | Port / element | Informatica code (verbatim) | XML line | PySpark conversion | Confidence | Reason |
|---|---|---|---|---:|---|---|---|
| workflow | `Start` | `Start → s_m_demo_mapping2` | empty `WORKFLOWLINK CONDITION` | 1471 | `workflow.py:run_workflow` starts with mapping2 | HIGH | First session is unconditionally scheduled. |
| workflow | `Decision1` | Decision expression | `$s_m_demo_mapping2.Status = 1` | 1158–1160 | Resolves mapping2 status and logs `Decision1` | HIGH | Direct task expression. |
| workflow | `Decision1` | success link | empty condition to `s_m_demo_mapping1` | 1470 | Mapping1 runs unconditionally, including after mapping2 failure | HIGH | Direct workflow link and reproduced defect. |
| workflow | `Decision1` | failure link | `$Decision1.Condition = 0` to `Failed_Email1` | 1467 | Logs `Failed_Email1` when mapping2 fails | HIGH | Direct workflow link. |
| workflow | `Failed_Email1` | Email task | Email subject/text from task definition | 1147–1151 | Logs status; no external email side effect | MEDIUM | Email delivery is outside local runtime. |
| workflow | `s_m_demo_mapping1` | source-row policy | `Treat source rows as = Insert` | 1346 | Writes mapping1 target instances through `ctx.io.write` | HIGH | Explicit session attribute. |
| workflow | `Decision2` | Decision expression | `$s_m_demo_mapping1.Status = 1` | 1155–1157 | Resolves mapping1 status and logs `Decision2` | HIGH | Direct task expression. |
| workflow | `Decision2` | success link | `$Decision2.Condition = 1` to `s_m_demo_mapping3` | 1469 | Runs mapping3 after mapping1 success | HIGH | Direct workflow link. |
| workflow | `Decision2` | failure link | `$Decision2.Condition = 0` to `Failed_Email2` | 1465 | Logs `Failed_Email2`, then stops parent | HIGH | Direct workflow link. |
| workflow | `Failed_Email2` | Email task | Email subject/text from task definition | 1137–1141 | Logs status; no external email side effect | MEDIUM | Email delivery is outside local runtime. |
| workflow | `Control` | control option | `Stop parent` | 1152–1154 | Returns non-zero after mapping1 failure | HIGH | Direct control-task option. |
| workflow | `Failed_Email2` | control link | empty condition to `Control` | 1468 | Logs `Control: Stop parent` | HIGH | Direct workflow link. |
| workflow | `s_m_demo_mapping2` | source-row policy | `Treat source rows as = Data driven` | 1434 | Preserves insert/update router instances | HIGH | Explicit session attribute. |
| workflow | `s_m_demo_mapping3` | source-row policy | `Treat source rows as = Insert` | 1217 | Writes `demo_target2` and `demo_target21` | HIGH | Explicit session attribute. |
| workflow | `Decision3` | Decision expression | `$s_m_demo_mapping3.Status = 1` | 1161–1163 | Resolves mapping3 status and logs `Decision3` | HIGH | Direct task expression. |
| workflow | `Decision3` | success link | `$Decision3.Condition = 1` to `SuccessEmail` | 1466 | Logs `SuccessEmail` | HIGH | Direct workflow link. |
| workflow | `Decision3` | failure link | `$Decision3.Condition = 0` to `Failed_Email3` | 1475 | Logs `Failed_Email3`; returns non-zero | HIGH | Direct workflow link. |
| workflow | `SuccessEmail` | Email task | Email subject/text from task definition | 1142–1146 | Logs status; no external email side effect | MEDIUM | Email delivery is outside local runtime. |
| workflow | `Failed_Email3` | Email task | Email subject/text from task definition | 1164–1168 | Logs status; no external email side effect | MEDIUM | Email delivery is outside local runtime. |
