"""Assemble the project-wide Informatica conversion comparison."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DOCS = ROOT / "docs" / "informatica_pyspark"
FIELDS = [
    "mapping",
    "transformation",
    "port",
    "informatica_code",
    "xml_line",
    "pyspark_code_or_ref",
    "confidence",
    "reason",
]


WORKFLOW_ROWS = [
    {
        "mapping": "wf_demo_mapping",
        "transformation": "Decision1",
        "port": "Decision Name",
        "informatica_code": "$s_m_demo_mapping2.Status = 1",
        "xml_line": "1159",
        "pyspark_code_or_ref": "informatica_pyspark/workflow.py:WORKFLOW_ORDER",
        "confidence": "HIGH",
        "reason": "The workflow graph gates mapping1 on the mapping2 status decision.",
    },
    {
        "mapping": "wf_demo_mapping",
        "transformation": "Decision2",
        "port": "Decision Name",
        "informatica_code": "$s_m_demo_mapping1.Status = 1",
        "xml_line": "1156",
        "pyspark_code_or_ref": "informatica_pyspark/workflow.py:WORKFLOW_ORDER",
        "confidence": "HIGH",
        "reason": "The workflow graph gates mapping3 on the mapping1 status decision.",
    },
    {
        "mapping": "wf_demo_mapping",
        "transformation": "Decision3",
        "port": "Decision Name",
        "informatica_code": "$s_m_demo_mapping3.Status = 1",
        "xml_line": "1162",
        "pyspark_code_or_ref": "informatica_pyspark/workflow.py:run_workflow",
        "confidence": "HIGH",
        "reason": "The final decision controls the success or failure branch.",
    },
    {
        "mapping": "wf_demo_mapping",
        "transformation": "WORKFLOWLINK",
        "port": "Decision2 -> Failed_Email2",
        "informatica_code": "$Decision2.Condition = 0",
        "xml_line": "1465",
        "pyspark_code_or_ref": "informatica_pyspark/workflow.py:run_workflow",
        "confidence": "HIGH",
        "reason": "A failed mapping stops the workflow before downstream work; the email branch is logged.",
    },
    {
        "mapping": "wf_demo_mapping",
        "transformation": "WORKFLOWLINK",
        "port": "Decision3 -> SuccessEmail",
        "informatica_code": "$Decision3.Condition = 1",
        "xml_line": "1466",
        "pyspark_code_or_ref": "informatica_pyspark/workflow.py:run_workflow",
        "confidence": "HIGH",
        "reason": "Successful completion reaches the logged success task.",
    },
    {
        "mapping": "wf_demo_mapping",
        "transformation": "WORKFLOWLINK",
        "port": "Decision1 -> Failed_Email1",
        "informatica_code": "$Decision1.Condition = 0",
        "xml_line": "1467",
        "pyspark_code_or_ref": "informatica_pyspark/workflow.py:run_workflow",
        "confidence": "HIGH",
        "reason": "A failed mapping stops the workflow before downstream work; the email branch is logged.",
    },
    {
        "mapping": "wf_demo_mapping",
        "transformation": "WORKFLOWLINK",
        "port": "Failed_Email2 -> Control",
        "informatica_code": "",
        "xml_line": "1468",
        "pyspark_code_or_ref": "informatica_pyspark/workflow.py:run_workflow",
        "confidence": "HIGH",
        "reason": "The migrated fail-fast exception is the equivalent of Stop parent.",
    },
    {
        "mapping": "wf_demo_mapping",
        "transformation": "WORKFLOWLINK",
        "port": "Decision2 -> s_m_demo_mapping3",
        "informatica_code": "$Decision2.Condition = 1",
        "xml_line": "1469",
        "pyspark_code_or_ref": "informatica_pyspark/workflow.py:WORKFLOW_ORDER",
        "confidence": "HIGH",
        "reason": "The graph advances to mapping3 only after mapping1 succeeds.",
    },
    {
        "mapping": "wf_demo_mapping",
        "transformation": "WORKFLOWLINK",
        "port": "Decision1 -> s_m_demo_mapping1",
        "informatica_code": "",
        "xml_line": "1470",
        "pyspark_code_or_ref": "informatica_pyspark/workflow.py:WORKFLOW_ORDER",
        "confidence": "HIGH",
        "reason": "The graph advances to mapping1 after mapping2.",
    },
    {
        "mapping": "wf_demo_mapping",
        "transformation": "WORKFLOWLINK",
        "port": "Start -> s_m_demo_mapping2",
        "informatica_code": "",
        "xml_line": "1471",
        "pyspark_code_or_ref": "informatica_pyspark/workflow.py:WORKFLOW_ORDER",
        "confidence": "HIGH",
        "reason": "The workflow starts with mapping2.",
    },
    {
        "mapping": "wf_demo_mapping",
        "transformation": "WORKFLOWLINK",
        "port": "s_m_demo_mapping1 -> Decision2",
        "informatica_code": "",
        "xml_line": "1472",
        "pyspark_code_or_ref": "informatica_pyspark/workflow.py:run_workflow",
        "confidence": "HIGH",
        "reason": "Mapping completion feeds its decision gate.",
    },
    {
        "mapping": "wf_demo_mapping",
        "transformation": "WORKFLOWLINK",
        "port": "s_m_demo_mapping2 -> Decision1",
        "informatica_code": "",
        "xml_line": "1473",
        "pyspark_code_or_ref": "informatica_pyspark/workflow.py:run_workflow",
        "confidence": "HIGH",
        "reason": "Mapping completion feeds its decision gate.",
    },
    {
        "mapping": "wf_demo_mapping",
        "transformation": "WORKFLOWLINK",
        "port": "s_m_demo_mapping3 -> Decision3",
        "informatica_code": "",
        "xml_line": "1474",
        "pyspark_code_or_ref": "informatica_pyspark/workflow.py:run_workflow",
        "confidence": "HIGH",
        "reason": "Mapping completion feeds its final decision gate.",
    },
    {
        "mapping": "wf_demo_mapping",
        "transformation": "WORKFLOWLINK",
        "port": "Decision3 -> Failed_Email3",
        "informatica_code": "$Decision3.Condition = 0",
        "xml_line": "1475",
        "pyspark_code_or_ref": "informatica_pyspark/workflow.py:run_workflow",
        "confidence": "HIGH",
        "reason": "A failed final mapping stops the workflow; the email branch is logged.",
    },
    {
        "mapping": "wf_demo_mapping",
        "transformation": "TASK",
        "port": "Failed_Email2",
        "informatica_code": "Email task",
        "xml_line": "1137",
        "pyspark_code_or_ref": "informatica_pyspark/workflow.py:run_workflow",
        "confidence": "NOT MIGRATED",
        "reason": "Email is deliberately not sent; the failure is logged instead.",
    },
    {
        "mapping": "wf_demo_mapping",
        "transformation": "TASK",
        "port": "SuccessEmail",
        "informatica_code": "Email task",
        "xml_line": "1142",
        "pyspark_code_or_ref": "informatica_pyspark/workflow.py:run_workflow",
        "confidence": "NOT MIGRATED",
        "reason": "Email is deliberately not sent; successful completion is logged instead.",
    },
    {
        "mapping": "wf_demo_mapping",
        "transformation": "TASK",
        "port": "Failed_Email1",
        "informatica_code": "Email task",
        "xml_line": "1147",
        "pyspark_code_or_ref": "informatica_pyspark/workflow.py:run_workflow",
        "confidence": "NOT MIGRATED",
        "reason": "Email is deliberately not sent; the failure is logged instead.",
    },
    {
        "mapping": "wf_demo_mapping",
        "transformation": "TASK",
        "port": "Control",
        "informatica_code": "Control Option = Stop parent",
        "xml_line": "1152",
        "pyspark_code_or_ref": "informatica_pyspark/workflow.py:run_workflow",
        "confidence": "NOT MIGRATED",
        "reason": "The Control task is not invoked; raising the mapping failure is the fail-fast equivalent.",
    },
    {
        "mapping": "wf_demo_mapping",
        "transformation": "TASK",
        "port": "Failed_Email3",
        "informatica_code": "Email task",
        "xml_line": "1164",
        "pyspark_code_or_ref": "informatica_pyspark/workflow.py:run_workflow",
        "confidence": "NOT MIGRATED",
        "reason": "Email is deliberately not sent; the failure is logged instead.",
    },
]


def _read_fragment(number: int) -> list[dict[str, str]]:
    csv_path = DOCS / f"conversion_m_demo_mapping{number}.csv"
    md_path = DOCS / f"conversion_m_demo_mapping{number}.md"
    if not csv_path.is_file() or not md_path.is_file():
        raise ValueError(f"Missing conversion fragment: {csv_path} or {md_path}")
    with csv_path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != FIELDS:
            raise ValueError(
                f"{csv_path} has header {reader.fieldnames!r}; expected {FIELDS!r}"
            )
        rows = list(reader)
    if not rows:
        raise ValueError(f"{csv_path} is empty")
    for index, row in enumerate(rows, start=2):
        if any(row[field] is None for field in FIELDS):
            raise ValueError(f"{csv_path}:{index} has a malformed row")
        try:
            if int(row["xml_line"]) < 1:
                raise ValueError
        except ValueError as exc:
            raise ValueError(f"{csv_path}:{index} has invalid xml_line") from exc

    markdown = md_path.read_text()
    total_match = (
        re.search(r"Total conversion-table rows:\s*\**(\d+)", markdown)
        or re.search(r"Expression/decision count:\s*\**(\d+)", markdown)
        or re.search(r"Total comparison rows:\s*\**(\d+)", markdown)
    )
    migrated_match = re.search(
        r"Migrated(?: rows| or represented in (?:the )?runnable mapping)?"
        r":\s*\**(\d+)",
        markdown,
    )
    not_migrated_match = re.search(
        r"Not[- ]migrated[- ]by[- ]design:\s*\**(\d+)", markdown
    )
    confidence_match = re.search(
        r"(?:Confidence split|Confidence):\s*\**HIGH\s+(\d+),\s*MEDIUM\s+(\d+),\s*LOW\s+(\d+),\s*NOT MIGRATED\s+(\d+)",
        markdown,
    )
    if not all((total_match, migrated_match, not_migrated_match, confidence_match)):
        raise ValueError(f"{md_path} is missing a machine-checkable summary")
    counts = Counter(row["confidence"] for row in rows)
    expected_confidence = {
        "HIGH": int(confidence_match.group(1)),
        "MEDIUM": int(confidence_match.group(2)),
        "LOW": int(confidence_match.group(3)),
        "NOT MIGRATED": int(confidence_match.group(4)),
    }
    if len(rows) != int(total_match.group(1)):
        raise ValueError(f"{md_path} total disagrees with {csv_path}")
    if counts["NOT MIGRATED"] != int(not_migrated_match.group(1)):
        raise ValueError(f"{md_path} not-migrated count disagrees with {csv_path}")
    if len(rows) - counts["NOT MIGRATED"] != int(migrated_match.group(1)):
        raise ValueError(f"{md_path} migrated count disagrees with {csv_path}")
    if any(counts[key] != value for key, value in expected_confidence.items()):
        raise ValueError(f"{md_path} confidence split disagrees with {csv_path}")
    return rows


def _low_decision(row: dict[str, str]) -> str:
    reason = row["reason"]
    if row["mapping"] == "m_demo_mapping1" and "Aggregator pass-through" in reason:
        return "m1 aggregator pass-through ordering"
    if row["mapping"] == "m_demo_mapping1" and "Sequence generator" in reason:
        return "m1 sequence-generator row ordering"
    if row["mapping"] == "m_demo_mapping2" and "Use Any Value" in reason:
        return "m2 Use Any Value lookup winner"
    if row["mapping"] == "m_demo_mapping2" and (
        "AES" in reason or "sentinel" in reason or "comparison" in reason
    ):
        return "m2 unrecoverable AES sentinel and changed-flag comparison"
    return f"{row['mapping']} unresolved decision"


def _write_csv(rows: list[dict[str, str]]) -> None:
    path = DOCS / "conversion_comparison.csv"
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def _write_markdown(rows: list[dict[str, str]]) -> None:
    counts = Counter(row["confidence"] for row in rows)
    not_migrated = counts["NOT MIGRATED"]
    migrated = len(rows) - not_migrated
    lows: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        if row["confidence"] == "LOW":
            lows.setdefault(_low_decision(row), []).append(row)
    review = [
        ("m1 aggregator pass-through ordering", "Highest-impact unresolved row-selection decision."),
        ("m1 sequence-generator row ordering", "Controls generated target keys and is only weakly discriminated by seed data."),
        ("m2 Use Any Value lookup winner", "The duplicate REC00002 lookup row is a direct legacy ambiguity."),
        ("m2 unrecoverable AES sentinel and changed-flag comparison", "The sentinel reproduces the legacy always-update defect."),
        ("wf_demo_mapping fail-fast branches", "Verify downstream mappings remain blocked after an abort."),
    ]
    path = DOCS / "conversion_comparison.md"
    with path.open("w") as handle:
        handle.write("# Informatica conversion comparison\n\n")
        handle.write("| " + " | ".join(FIELDS) + " |\n")
        handle.write("| " + " | ".join("---" for _ in FIELDS) + " |\n")
        for row in rows:
            handle.write("| " + " | ".join(row[field].replace("|", r"\|") for field in FIELDS) + " |\n")
        handle.write("\n## Totals and confidence split\n\n")
        handle.write(f"- Total expression/construct count: **{len(rows)}**\n")
        handle.write(f"- Migrated or represented: **{migrated}**\n")
        handle.write(f"- Not migrated by design: **{not_migrated}**\n")
        handle.write(
            "- Confidence: "
            f"**HIGH {counts['HIGH']}, MEDIUM {counts['MEDIUM']}, "
            f"LOW {counts['LOW']}, NOT MIGRATED {counts['NOT MIGRATED']}**\n"
        )
        handle.write("\n## LOW rows grouped by underlying decision\n\n")
        if lows:
            for decision, decision_rows in lows.items():
                lines = ", ".join(
                    f"{row['mapping']}:{row['port']} (line {row['xml_line']})"
                    for row in decision_rows
                )
                handle.write(f"- **{decision}** ({len(decision_rows)} rows): {lines}\n")
        else:
            handle.write("- None.\n")
        handle.write("\n## Review these first\n\n")
        for index, (decision, reason) in enumerate(review, start=1):
            handle.write(f"{index}. **{decision}** — {reason}\n")


def main() -> None:
    rows = [row for number in (1, 2, 3) for row in _read_fragment(number)]
    rows.extend(WORKFLOW_ROWS)
    _write_csv(rows)
    _write_markdown(rows)
    print(f"wrote {len(rows)} rows to conversion_comparison.csv/.md")


if __name__ == "__main__":
    main()
