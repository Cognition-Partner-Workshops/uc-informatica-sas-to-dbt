from pathlib import Path

from informatica_pyspark.lineage import Lineage, generate_lineage
from informatica_pyspark.targets import PHYSICAL_TARGETS


def test_lineage_traps_have_xml_evidence():
    graph = Lineage()
    chain = graph.chain("m_demo_mapping1", "demo_target6", "TX_TYPE_CD")
    assert [(x[0], x[1], x[2]) for x in chain[:3]] == [
        ("demo_target6", "TX_TYPE_CD", 786),
        ("agg_TRANS", "o_ACCT_ID", 815),
        ("exp_TRANS1", "o_ACCT_ID", 831),
    ]
    assert chain[3][:2] == ("exp_TRANS", "o_ACCT_ID")
    assert graph.expression("m_demo_mapping1", "exp_TRANS", "o_ACCT_ID") == \
        ":LKP.lkp_TRANS1(ACCT_ID)"  # XML line 608
    assert graph.sq_position_table()[4] == (5, "CR8_DT", "SYSTIMESTAMP")  # XML line 580
    assert graph.sq_position_table()[13][1:] == (
        "TX_TYPE_CD", "STRCMP(demo_source4.ACCT_STAT_CD,demo_source3.TX_TYPE_CD)")
    assert ("sq_demo_source4", "TX_TYPE_CD") not in {
        (edge.from_instance, edge.from_field)
        for edge in graph.edges if edge.mapping == "m_demo_mapping1"
    }
    assert graph.chain("m_demo_mapping1", "demo_target6", "ACCT_TYP")[1][:2] == (
        "agg_TRANS", "o_acc_trim")  # XML line 787
    assert graph.chain("m_demo_mapping2", "demo_target1_UPD", "Key")[1][:2] == (
        "UPDTRANS", "Key2")  # XML line 356
    assert graph.chain("m_demo_mapping2", "demo_target1_UPD", "UPDATED_BY")[1][:2] == (
        "UPDTRANS", "o_UPDATED_BY2")  # XML line 363
    assert graph.chain("m_demo_mapping2", "demo_target1_INS", "Key")[1][:2] == (
        "SEQTRANS", "NEXTVAL")  # XML line 373


def test_physical_targets_and_dead_ports():
    graph = Lineage()
    assert PHYSICAL_TARGETS["demo_target1"] == [
        "Key", "LEAD_CO_MNE", "BRANCH_CO_MNE", "MIS_DATE", "ID", "DESCRIPTION", "SHORT_NAME",
        "CREATED_BY", "CREATED_TIME", "UPDATED_BY", "UPDATED_TIME", "ACTIVE_FLAG", "START_DATE",
        "END_DATE",
    ]
    assert PHYSICAL_TARGETS["demo_target2"] == [
        "Title", "Gender", "First_Name", "Middle_Name", "Last_Name", "Member_Identifier",
        "Member_Suffix", "Date_of_Birth", "Member_Number", "Soc_Number", "Type_Code",
        "Relationship_to_Subscriber_Code", "Relationship_to_Subscriber_Code_Label", "Effective_Date",
    ]
    assert "exp_TRANS2.SELL_ED_DT" in graph.dead_ports("m_demo_mapping1")
    assert "sq_demo_source4.TX_TYPE_CD" in graph.dead_ports("m_demo_mapping1")
    assert "EXPTRANS.MD5_src" in graph.dead_ports("m_demo_mapping2")
    assert "EXPTRANS.Relationship_to_Subscriber_Code_Label" in graph.dead_ports("m_demo_mapping3")


def test_lineage_cli_output_is_deterministic(tmp_path):
    output = tmp_path / "lineage.md"
    output.write_text(generate_lineage())
    committed = Path(__file__).resolve().parents[3] / "docs/pyspark/lineage.md"
    assert output.read_text() == committed.read_text()
