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

    for mapping in document["mappings"]:
        for target in mapping["targets"]:
            for target_column in target["columns"]:
                for branch in target_column["branches"]:
                    pairs = [(step["instance"], step["field"]) for step in branch]
                    assert all(left != right for left, right in zip(pairs, pairs[1:]))

    inventory = next(mapping["target_unconnected"] for mapping in document["mappings"]
                     if mapping["name"] == "m_demo_mapping2")
    assert {"instance": "demo_target1_INS", "field": "ACTIVE_FLAG", "connected": False,
            "reason": "no incoming CONNECTOR — column is NULL in the target"} in inventory

    assert document["workflow"]["execution_session_order"] == [
        "s_m_demo_mapping2", "s_m_demo_mapping1", "s_m_demo_mapping3"
    ]

    upd = column("m_demo_mapping2", "demo_target1_UPD", "LEAD_CO_MNE")
    path = upd["branches"][0]
    assert any(step["instance"] == "RTRTRANS" and step["field"] == "LEAD_CO_MNE4"
               and step["group"] == "Update" for step in path)
    assert not any(step["instance"] == "RTRTRANS" and step["field"] == "LEAD_CO_MNE2"
                   for step in path)

    upd_id = column("m_demo_mapping2", "demo_target1_UPD", "ID")
    assert any(step["instance"] == "RTRTRANS" and step["field"] == "ID3"
               and step["group"] == "Update" for step in upd_id["branches"][0])
