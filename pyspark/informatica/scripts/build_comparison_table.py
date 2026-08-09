"""Assemble and audit the first-class comparison document."""

from collections import Counter, defaultdict
from pathlib import Path
import re
from xml.etree import ElementTree


RUBRIC = """## Confidence rubric

- **HIGH** — semantics unambiguous in the XML AND at least one baseline row would fail parity if
  the conversion were wrong.
- **MEDIUM** — unambiguous but weakly exercised: the output is constant/degenerate in the seed
  data, so parity cannot catch a wrong conversion.
- **LOW** — the conversion rests on a judgement call the XML does not determine; name the
  alternative that was rejected.
- **NOT MIGRATED** — deliberate (e.g. dead port with no outgoing connector); name every one.
"""


def _cells(line):
    content = line.strip().strip("|")
    cells = []
    current = []
    in_code = False
    for character in content:
        if character == "`":
            in_code = not in_code
        if character == "|" and not in_code:
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(character)
    cells.append("".join(current).strip())
    return cells


def _table_rows(text):
    rows = []
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = _cells(line)
        if len(cells) != 8 or cells[0] == "Mapping" or set(cells[0]) <= {"-"}:
            continue
        rows.append(
            {
                "mapping": cells[0],
                "transformation": cells[1],
                "object": cells[2],
                "xml_line": cells[3],
                "original": cells[4],
                "converted": cells[5],
                "confidence": cells[6],
                "reason": cells[7],
            }
        )
    return rows


def _xml_expression_rows(xml_path):
    rows = []
    mapping = None
    transformation = None
    for line_number, line in enumerate(xml_path.read_text().splitlines(), 1):
        if line.lstrip().startswith("<MAPPING "):
            mapping = re.search(r'NAME ="([^"]+)"', line).group(1)
        if line.lstrip().startswith("<TRANSFORMATION "):
            transformation = re.search(r'NAME ="([^"]+)"', line).group(1)
        if line.lstrip().startswith("<TRANSFORMFIELD "):
            field = ElementTree.fromstring(line).attrib
            if field.get("EXPRESSION"):
                rows.append(
                    (mapping, transformation, field["NAME"], line_number)
                )
        if line.lstrip().startswith("</TRANSFORMATION>"):
            transformation = None
        if line.lstrip().startswith("</MAPPING>"):
            mapping = None
    return rows


def _xml_line_numbers(xml_path, names):
    return {
        line_number
        for line_number, line in enumerate(xml_path.read_text().splitlines(), 1)
        if any(
            f'NAME ="{name}"' in line
            and re.search(r'VALUE ="([^"]+)"', line)
            and re.search(r'VALUE ="([^"]+)"', line).group(1)
            for name in names
        )
    }


def _row_covers_line(row, line):
    for token in re.split(r"[,/ ]+", row["xml_line"]):
        if not token:
            continue
        if "-" in token:
            try:
                start, end = (int(part) for part in token.split("-", 1))
            except ValueError:
                continue
            if start <= line <= end:
                return True
        else:
            try:
                if int(token) == line:
                    return True
            except ValueError:
                continue
    return False


def _xml_control_lines(xml_path):
    controls = []
    current_type = None
    for line_number, line in enumerate(xml_path.read_text().splitlines(), 1):
        if line.lstrip().startswith("<TRANSFORMATION "):
            match = re.search(r'TYPE ="([^"]+)"', line)
            current_type = match.group(1) if match else None
        if line.lstrip().startswith("<GROUP ") and 'EXPRESSION ="' in line:
            controls.append(line_number)
        if (
            line.lstrip().startswith("<TRANSFORMFIELD ")
            and 'EXPRESSIONTYPE ="GROUPBY"' in line
        ):
            controls.append(line_number)
        if current_type == "Sequence" and 'TABLEATTRIBUTE NAME ="' in line:
            if re.search(
                r'NAME ="(Start Value|Increment By|Current Value)"', line
            ):
                controls.append(line_number)
        if line.lstrip().startswith("</TRANSFORMATION>"):
            current_type = None
    return controls


def audit_coverage(root):
    comparison = root / "docs/pyspark/comparison"
    rows = []
    for fragment in sorted(comparison.glob("*.md")):
        rows.extend(_table_rows(fragment.read_text()))

    xml_path = root / "legacy/informatica/wf_demo_mapping.XML"
    expression_rows = _xml_expression_rows(xml_path)
    if len(expression_rows) != 89:
        raise AssertionError(
            f"XML expression count changed: expected 89, found {len(expression_rows)}"
        )
    missing = []
    for mapping, transformation, port, line in expression_rows:
        matches = [
            row for row in rows
            if row["mapping"] == mapping
            and row["transformation"] == transformation
            and row["xml_line"] == str(line)
            and row["object"].split()[0] == port
        ]
        if not matches:
            missing.append((mapping, transformation, port, line))
    if missing:
        raise AssertionError(f"Missing XML expression rows: {missing}")

    attribute_names = (
        "Sql Query",
        "Lookup condition",
        "Lookup policy on multiple match",
        "Update Strategy Expression",
    )
    attribute_lines = _xml_line_numbers(xml_path, attribute_names)
    control_lines = sorted(attribute_lines | set(_xml_control_lines(xml_path)))
    missing_attributes = sorted(
        line for line in control_lines
        if not any(_row_covers_line(row, line) for row in rows)
    )
    if missing_attributes:
        raise AssertionError(f"Missing XML control rows: {missing_attributes}")

    return {
        "rows": rows,
        "expression_count": len(expression_rows),
        "missing": missing,
        "missing_attributes": missing_attributes,
    }


def _decision_groups(root, low_rows):
    text = (root / "docs/pyspark/decisions.md").read_text()
    sections = {}
    current = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
        elif current and line.startswith("- **"):
            sections[current].append(line.lower())
    groups = defaultdict(list)
    for row in low_rows:
        haystack = f"{row['transformation']} {row['object']} {row['reason']}".lower()
        candidates = [
            section for section, bullets in sections.items()
            if any(
                token in bullet
                for bullet in bullets
                for token in haystack.replace("`", "").replace("(", " ").split()
                if len(token) > 4
            )
        ]
        groups[candidates[0] if candidates else "No matching decisions.md entry"].append(row)
    return groups


def main():
    root = Path(__file__).resolve().parents[3]
    comparison = root / "docs/pyspark/comparison"
    audit = audit_coverage(root)
    rows = audit["rows"]
    confidence = Counter(row["confidence"] for row in rows)
    expected_confidence = {"HIGH", "MEDIUM", "LOW", "NOT MIGRATED"}
    unexpected = set(confidence) - expected_confidence
    if unexpected:
        raise AssertionError(f"Unexpected confidence values: {sorted(unexpected)}")
    low_rows = [row for row in rows if row["confidence"] == "LOW"]
    review_rows = sorted(
        (row for row in rows if row["confidence"] in {"LOW", "MEDIUM"}),
        key=lambda row: (0 if row["confidence"] == "LOW" else 1,
                         row["mapping"], row["transformation"], row["object"]),
    )
    sections = [
        f"## {fragment.stem}\n\n{fragment.read_text().strip()}"
        for fragment in sorted(comparison.glob("*.md"))
    ]
    review = [
        f"- **{row['confidence']}** `{row['mapping']}` / `{row['transformation']}` / "
        f"`{row['object']}` (XML {row['xml_line']}): {row['reason']}"
        for row in review_rows
    ]
    grouped = []
    for decision, decision_rows in sorted(_decision_groups(root, low_rows).items()):
        grouped.append(f"### {decision}")
        grouped.extend(
            f"- `{row['mapping']}` / `{row['transformation']}` / `{row['object']}` "
            f"(XML {row['xml_line']})"
            for row in decision_rows
        )
    output = [
        "# Informatica → PySpark conversion comparison", "",
        f"- Total rows: {len(rows)}",
        f"- Migrated: {len(rows) - confidence['NOT MIGRATED']}",
        f"- Not-migrated-by-design: {confidence['NOT MIGRATED']}",
        f"- Confidence split: {dict(sorted(confidence.items()))}",
        f"- XML TRANSFORMFIELD expression coverage: {audit['expression_count']}/89",
        "- XML control coverage: SQL overrides, lookup conditions/policies, "
        "update strategy, sequence state, router conditions, and aggregator rows audited.",
        "",
        "## Review these first", "",
        *review, "",
        "## LOW rows grouped by underlying decision", "",
        *(grouped or ["No LOW-confidence rows."]), "",
        RUBRIC,
        "",
        "\n\n".join(sections), "",
    ]
    (root / "docs/pyspark/conversion_comparison.md").write_text("\n".join(output))
    print(
        f"Coverage audit: {audit['expression_count']}/89 TRANSFORMFIELD expressions; "
        f"{len(rows)} comparison rows"
    )


if __name__ == "__main__":
    main()
