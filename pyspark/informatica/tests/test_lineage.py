import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "pyspark" / "informatica" / "scripts" / "build_lineage.py"
OUTPUT = ROOT / "docs" / "informatica_pyspark" / "lineage.json"


def test_lineage_contains_connector_traps():
    subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True)
    document = json.loads(OUTPUT.read_text())
    mappings = {mapping["name"]: mapping for mapping in document["mappings"]}

    def column(mapping, instance, name):
        target = next(x for x in mappings[mapping]["targets"] if x["instance"] == instance)
        return next(x for x in target["columns"] if x["name"] == name)

    first_nm = column("m_demo_mapping1", "demo_target5", "FIRST_NM")
    assert any(any(step["instance"] == "lkp_TRANS2" for step in branch)
               for branch in first_nm["branches"])
    assert not any(any(step["instance"] == "demo_source3" and step["field"] == "FIRST_NM"
                       for step in branch) for branch in first_nm["branches"])

    tx_type = column("m_demo_mapping1", "demo_target6", "TX_TYPE_CD")
    assert any(any(step["hop_kind"] == "unconnected_lookup" and step["field"] == "TX_TYPE_CD"
                   for step in branch) for branch in tx_type["branches"])

    cr8 = column("m_demo_mapping1", "demo_target6", "CR8_DT")
    assert any(any(step.get("expression") == "SYSTIMESTAMP" for step in branch)
               for branch in cr8["branches"])

    target2 = column("m_demo_mapping3", "demo_target2", "Title")
    assert any(any(step.get("group") == "NEWGROUP1" for step in branch)
               for branch in target2["branches"])
