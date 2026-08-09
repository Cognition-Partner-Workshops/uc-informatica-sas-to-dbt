"""Assemble the first-class comparison document from existing fragments."""

import re
from pathlib import Path


RUBRIC = """## Confidence rubric

- **HIGH** — semantics unambiguous in the XML AND at least one baseline row would fail parity if
  the conversion were wrong.
- **MEDIUM** — unambiguous but weakly exercised: the output is constant/degenerate in the seed
  data, so parity cannot catch a wrong conversion.
- **LOW** — the conversion rests on a judgement call the XML does not determine; name the
  alternative that was rejected.
- **NOT MIGRATED** — deliberate (e.g. dead port with no outgoing connector); name every one.
"""


def main():
    root = Path(__file__).resolve().parents[3]
    comparison = root / "docs/pyspark/comparison"
    fragments = sorted(comparison.glob("*.md"))
    sections = []
    rows = []
    for fragment in fragments:
        text = fragment.read_text().strip()
        sections.append(f"## {fragment.stem}\n\n{text}")
        rows.extend(line for line in text.splitlines() if line.startswith("|") and
                    not line.startswith("|---") and "Mapping |" not in line)
    confidence = {name: sum(f"| **{name}**" in row or f"| {name} |" in row for row in rows)
                  for name in ("HIGH", "MEDIUM", "LOW", "NOT MIGRATED")}
    output = [
        "# Informatica → PySpark conversion comparison", "",
        f"- Total rows: {len(rows)}",
        f"- Migrated: {len(rows) - confidence['NOT MIGRATED']}",
        f"- Not-migrated-by-design: {confidence['NOT MIGRATED']}",
        f"- Confidence split: {confidence}",
        "- Review these first: LOW rows, then MEDIUM rows covering workflow failure paths.",
        "- LOW rows grouped by decision: see `docs/pyspark/decisions.md`.",
        "", RUBRIC,
        "", "\n\n".join(sections), "",
    ]
    (root / "docs/pyspark/conversion_comparison.md").write_text("\n".join(output))


if __name__ == "__main__":
    main()
