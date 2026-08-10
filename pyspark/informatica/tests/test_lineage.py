from pathlib import Path

from informatica_pyspark.lineage import Lineage, generate_lineage
from informatica_pyspark.mappings import MAPPINGS
from informatica_pyspark.targets import PHYSICAL_TARGETS


def test_lineage_traps_have_xml_evidence():
    graph = Lineage()
    chain = graph.chain("m_demo_mapping1", "demo_target6", "TX_TYPE_CD")
    assert [(x[0], x[1], x[2]) for x in chain[:3]] == [
        ("demo_target6", "TX_TYPE_CD", 786),
        ("agg_TRANS", "o_ACCT_ID", 815),
        ("rtr_TRANS", "o_ACCT_ID1", 815),
    ]
    assert chain[3][:2] == ("rtr_TRANS", "o_ACCT_ID")
    assert chain[4][:2] == ("exp_TRANS1", "o_ACCT_ID")
    assert graph.router_details("m_demo_mapping1", "rtr_TRANS", "o_ACCT_ID1") == {
        "group": "demo_target6_GRP", "expression": "ACCT_TYP = 'SB'",
    }, "XML lines 668/689: router group resolution changed"
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
    contradictions = {
        ("demo_target6", "TX_TYPE_CD"): ("agg_TRANS.TX_TYPE_CD", "agg_TRANS.o_ACCT_ID"),
        ("demo_target6", "ACCT_TYP"): ("agg_TRANS.ACCT_TYP", "agg_TRANS.o_acc_trim"),
        ("demo_target1_UPD", "Key"): ("UPDTRANS.Key", "UPDTRANS.Key2"),
        ("demo_target1_UPD", "UPDATED_BY"): ("UPDTRANS.UPDATED_BY", "UPDTRANS.o_UPDATED_BY2"),
        ("demo_target1_INS", "Key"): ("SEQTRANS.Key", "SEQTRANS.NEXTVAL"),
    }
    for (instance, field), (name_match, actual) in contradictions.items():
        chain = graph.chain(
            "m_demo_mapping1" if instance == "demo_target6" else "m_demo_mapping2",
            instance, field,
        )
        assert name_match not in {f"{name}.{port}" for name, port, _ in chain}, (
            f"XML lines 786/787/356/363/373: name-matched port {name_match} unexpectedly present")
        assert actual == f"{chain[1][0]}.{chain[1][1]}", (
            f"XML lines 786/787/356/363/373: true connector source changed")
    details = graph.lookup_details("m_demo_mapping1", "lkp_TRANS1")
    assert details == {
        "table": "lkp_demo_source3", "condition": "ACCT_ID =  IN_ACCT_ID",
        "policy": "Use Last Value", "table_line": 533, "condition_line": 537,
        "policy_line": 536,
    }, "XML lines 533/536/537: lkp_TRANS1 metadata changed"
    assert graph.session_bindings() == [
        ("s_m_demo_mapping3", "m_demo_mapping3", 1169),
        ("s_m_demo_mapping1", "m_demo_mapping1", 1236),
        ("s_m_demo_mapping2", "m_demo_mapping2", 1365),
    ], "XML lines 1169/1236/1365: session bindings changed"
    assert graph.instance_line("m_demo_mapping2", "demo_target1_UPD") == 345, \
        "XML line 345: shared physical target instance changed"
    assert graph.instance_line("m_demo_mapping2", "demo_target1_INS") == 346, \
        "XML line 346: shared physical target instance changed"
    assert graph.instance_line("m_demo_mapping3", "demo_target21") == 1009, \
        "XML line 1009: shared physical target instance changed"
    assert graph.instance_line("m_demo_mapping3", "demo_target2") == 1010, \
        "XML line 1010: shared physical target instance changed"
    assert {
        "m_demo_mapping1": {
            "sources": ("demo_source3", "demo_source4", "demo_source5",
                        "lkp_demo_source1", "lkp_demo_source2", "lkp_demo_source3"),
            "targets": ("demo_target6", "demo_target5", "demo_target3"),
        },
        "m_demo_mapping2": {
            "sources": ("demo_source1", "demo_target1"),
            "targets": ("demo_target1_UPD", "demo_target1_INS"),
        },
        "m_demo_mapping3": {
            "sources": ("demo_source2",), "targets": ("demo_target21", "demo_target2"),
        },
    } == {
        "m_demo_mapping1": {
            "sources": MAPPINGS["m_demo_mapping1"].sources,
            "targets": tuple(x["NAME"] for x in graph.target_instances("m_demo_mapping1")),
        },
        "m_demo_mapping2": {
            "sources": MAPPINGS["m_demo_mapping2"].sources,
            "targets": tuple(x["NAME"] for x in graph.target_instances("m_demo_mapping2")),
        },
        "m_demo_mapping3": {
            "sources": ("demo_source2",), "targets": tuple(x["NAME"] for x in graph.target_instances("m_demo_mapping3")),
        },
    }, "XML mapping/source/target declarations changed"


def test_physical_targets_and_dead_ports():
    graph = Lineage()
    expected_targets = {
        "demo_target1": ["Key", "LEAD_CO_MNE", "BRANCH_CO_MNE", "MIS_DATE", "ID", "DESCRIPTION",
                         "SHORT_NAME", "CREATED_BY", "CREATED_TIME", "UPDATED_BY", "UPDATED_TIME",
                         "ACTIVE_FLAG", "START_DATE", "END_DATE"],
        "demo_target2": ["Title", "Gender", "First_Name", "Middle_Name", "Last_Name",
                         "Member_Identifier", "Member_Suffix", "Date_of_Birth", "Member_Number",
                         "Soc_Number", "Type_Code", "Relationship_to_Subscriber_Code",
                         "Relationship_to_Subscriber_Code_Label", "Effective_Date"],
        "demo_target3": ["PRODUCT_ID", "PRODUCT_NM", "PRODUCT_NO", "COLOR", "STD_COST",
                         "LIST_PRICE", "SELL_ST_DT", "SELL_ED_DT"],
        "demo_target5": ["ACCT_ID", "FIRST_NM", "LAST_NM", "BAL_AMT", "CRDT_SCORE"],
        "demo_target6": ["ACCT_ID", "ACCT_TYP", "ACCT_DESC", "CR8_DT", "CRDT_LN", "CLSR_DT",
                         "ACCT_STAT_CD", "TX_ID", "ACCT_KEY", "TX_DTTM", "TX_AMT", "TX_TYPE_CD"],
    }
    assert PHYSICAL_TARGETS == expected_targets, "XML TARGETFIELD FIELDNUMBER lists changed"
    assert {x["NAME"]: x["TRANSFORMATION_NAME"] for x in graph.target_instances("m_demo_mapping2")} == {
        "demo_target1_UPD": "demo_target1", "demo_target1_INS": "demo_target1",
    }, "XML lines 345/346: shared physical target binding changed"
    assert {x["NAME"]: x["TRANSFORMATION_NAME"] for x in graph.target_instances("m_demo_mapping3")} == {
        "demo_target21": "demo_target2", "demo_target2": "demo_target2",
    }, "XML lines 1009/1010: shared physical target binding changed"
    expected_dead = {
        "m_demo_mapping2": {
            "EXPTRANS.MD5_src", "EXPTRANS.MD5_tgt", "LKPTRANS.ACTIVE_FLAG",
            "LKPTRANS.CREATED_BY", "LKPTRANS.CREATED_TIME", "LKPTRANS.END_DATE", "LKPTRANS.ID",
            "LKPTRANS.ID1", "LKPTRANS.START_DATE", "LKPTRANS.UPDATED_BY", "LKPTRANS.UPDATED_TIME",
            "RTRTRANS.BRANCH_CO_MNE", "RTRTRANS.BRANCH_CO_MNE1", "RTRTRANS.BRANCH_CO_MNE11",
            "RTRTRANS.BRANCH_CO_MNE12", "RTRTRANS.BRANCH_CO_MNE13", "RTRTRANS.BRANCH_CO_MNE3",
            "RTRTRANS.Changed_Flag", "RTRTRANS.Changed_Flag1", "RTRTRANS.Changed_Flag2",
            "RTRTRANS.DESCRIPTION", "RTRTRANS.DESCRIPTION1", "RTRTRANS.DESCRIPTION11",
            "RTRTRANS.DESCRIPTION12", "RTRTRANS.DESCRIPTION13", "RTRTRANS.DESCRIPTION3",
            "RTRTRANS.ID", "RTRTRANS.ID2", "RTRTRANS.Key", "RTRTRANS.Key1", "RTRTRANS.Key2",
            "RTRTRANS.LEAD_CO_MNE", "RTRTRANS.LEAD_CO_MNE1", "RTRTRANS.LEAD_CO_MNE11",
            "RTRTRANS.LEAD_CO_MNE12", "RTRTRANS.LEAD_CO_MNE13", "RTRTRANS.LEAD_CO_MNE3",
            "RTRTRANS.MIS_DATE", "RTRTRANS.MIS_DATE1", "RTRTRANS.MIS_DATE11",
            "RTRTRANS.MIS_DATE12", "RTRTRANS.MIS_DATE13", "RTRTRANS.MIS_DATE3",
            "RTRTRANS.New_Flag", "RTRTRANS.New_Flag1", "RTRTRANS.New_Flag2", "RTRTRANS.SHORT_NAME",
            "RTRTRANS.SHORT_NAME1", "RTRTRANS.SHORT_NAME11", "RTRTRANS.SHORT_NAME12",
            "RTRTRANS.SHORT_NAME13", "RTRTRANS.SHORT_NAME3", "RTRTRANS.o_CREATED_BY",
            "RTRTRANS.o_CREATED_BY2", "RTRTRANS.o_CREATED_TIME", "RTRTRANS.o_CREATED_TIME2",
            "RTRTRANS.o_UPDATED_BY", "RTRTRANS.o_UPDATED_BY1", "RTRTRANS.o_UPDATED_BY2",
            "RTRTRANS.o_UPDATED_TIME", "RTRTRANS.o_UPDATED_TIME1", "RTRTRANS.o_UPDATED_TIME2",
            "SEQTRANS.CURRVAL", "UPDTRANS.Changed_Flag2", "UPDTRANS.New_Flag2",
            "UPDTRANS.o_CREATED_BY2", "UPDTRANS.o_CREATED_TIME2",
        },
        "m_demo_mapping1": {
            "SEQ_GEN.CURRVAL", "agg_TRANS.TX_AMT", "exp_TRANS.CRDT_LN", "exp_TRANS1.ACCT_DESC",
            "exp_TRANS2.SELL_ED_DT", "exp_TRANS2.SELL_ST_DT", "lkp_TRANS1.ACCT_ID",
            "lkp_TRANS1.IN_ACCT_ID", "lkp_TRANS1.TX_TYPE_CD", "lkp_TRANS1.TX_TYPE_DESC",
            "lkp_TRANS2.ACCT_ID", "lkp_TRANS2.AGE", "lkp_TRANS2.CUST_ADDR",
            "lkp_TRANS2.CUST_EML_ADDR", "lkp_TRANS2.CUST_ID", "lkp_TRANS2.CUST_PHN",
            "lkp_TRANS2.CUST_TYP", "lkp_TRANS2.DOB", "lkp_TRANS2.IN_ACCT_ID", "lkp_TRANS2.LAST_NM",
            "lkp_TRANS3.AVG_INC_AMT", "lkp_TRANS3.CURR_CRDT_BAL_AMT", "lkp_TRANS3.CUST_ID",
            "lkp_TRANS3.IN_CUST_ID", "lkp_TRANS3.MAX_CRDT_LMT", "lkp_TRANS3.MAX_CRDT_SCORE",
            "lkp_TRANS3.MIN_CRDT_SCORE", "rtr_TRANS.ACCT_ID", "rtr_TRANS.ACCT_ID3",
            "rtr_TRANS.ACCT_STAT_CD", "rtr_TRANS.ACCT_STAT_CD2", "rtr_TRANS.ACCT_STAT_CD3",
            "rtr_TRANS.ACCT_TYP", "rtr_TRANS.ACCT_TYP1", "rtr_TRANS.ACCT_TYP2",
            "rtr_TRANS.ACCT_TYP3", "rtr_TRANS.BAL_AMT", "rtr_TRANS.BAL_AMT1",
            "rtr_TRANS.BAL_AMT3", "rtr_TRANS.CLSR_DT", "rtr_TRANS.CLSR_DT2",
            "rtr_TRANS.CLSR_DT3", "rtr_TRANS.CR8_DT", "rtr_TRANS.CR8_DT2",
            "rtr_TRANS.CR8_DT3", "rtr_TRANS.CRDT_SCORE", "rtr_TRANS.CRDT_SCORE1",
            "rtr_TRANS.CRDT_SCORE3", "rtr_TRANS.FIRST_NM", "rtr_TRANS.FIRST_NM1",
            "rtr_TRANS.FIRST_NM3", "rtr_TRANS.LAST_NM", "rtr_TRANS.LAST_NM1",
            "rtr_TRANS.LAST_NM3", "rtr_TRANS.TX_AMT", "rtr_TRANS.TX_AMT2",
            "rtr_TRANS.TX_AMT3", "rtr_TRANS.TX_DTTM", "rtr_TRANS.TX_DTTM2",
            "rtr_TRANS.TX_DTTM3", "rtr_TRANS.TX_ID", "rtr_TRANS.TX_ID2", "rtr_TRANS.TX_ID3",
            "rtr_TRANS.o_ACCT_DESC", "rtr_TRANS.o_ACCT_DESC2", "rtr_TRANS.o_ACCT_DESC3",
            "rtr_TRANS.o_ACCT_ID", "rtr_TRANS.o_ACCT_ID2", "rtr_TRANS.o_ACCT_ID3",
            "rtr_TRANS.o_acc_trim", "rtr_TRANS.o_acc_trim2", "rtr_TRANS.o_acc_trim3",
            "rtr_TRANS.o_crdt_trim", "rtr_TRANS.o_crdt_trim2", "rtr_TRANS.o_crdt_trim3",
            "sq_demo_source4.TX_TYPE_CD",
        },
        "m_demo_mapping3": {
            "EXPTRANS.Relationship_to_Subscriber_Code_Label", "RTRTRANS.Birth_Date",
            "RTRTRANS.Birth_Date2", "RTRTRANS.First_Name", "RTRTRANS.First_Name2",
            "RTRTRANS.Gender_Code", "RTRTRANS.Gender_Code2", "RTRTRANS.Last_Name",
            "RTRTRANS.Last_Name2", "RTRTRANS.Member_ID", "RTRTRANS.Member_ID2",
            "RTRTRANS.Member_Record_Number", "RTRTRANS.Member_Record_Number2",
            "RTRTRANS.Member_Suffix", "RTRTRANS.Member_Suffix2", "RTRTRANS.Member_Type_Code",
            "RTRTRANS.Member_Type_Code2", "RTRTRANS.Middle_Name", "RTRTRANS.Middle_Name2",
            "RTRTRANS.Original_Effective_Date", "RTRTRANS.Original_Effective_Date2",
            "RTRTRANS.Relationship_to_Subscriber_Code", "RTRTRANS.Relationship_to_Subscriber_Code2",
            "RTRTRANS.Relationship_to_Subscriber_Code_Label",
            "RTRTRANS.Relationship_to_Subscriber_Code_Label2", "RTRTRANS.Social_Security_Number",
            "RTRTRANS.Social_Security_Number2", "RTRTRANS.Title", "RTRTRANS.Title2",
        },
    }
    for mapping, required in expected_dead.items():
        assert graph.dead_ports(mapping) == required, (
            f"XML connector lines for {mapping}: complete dead-port set changed")


def test_all_target_terminal_chains_are_literal_expected():
    graph = Lineage()
    expected = {
        "demo_target1_UPD": {"Key": ("LKPTRANS", "Key"), "LEAD_CO_MNE": ("demo_source1", "LEAD_CO_MNE"),
            "BRANCH_CO_MNE": ("demo_source1", "BRANCH_CO_MNE"), "MIS_DATE": ("demo_source1", "MIS_DATE"),
            "ID": ("demo_source1", "ID"), "DESCRIPTION": ("demo_source1", "DESCRIPTION"),
            "SHORT_NAME": ("demo_source1", "SHORT_NAME"), "CREATED_BY": ("demo_target1_UPD", "CREATED_BY"),
            "CREATED_TIME": ("demo_target1_UPD", "CREATED_TIME"), "UPDATED_BY": ("EXPTRANS", "o_UPDATED_BY"),
            "UPDATED_TIME": ("EXPTRANS", "o_UPDATED_TIME"), "ACTIVE_FLAG": ("demo_target1_UPD", "ACTIVE_FLAG"),
            "START_DATE": ("demo_target1_UPD", "START_DATE"), "END_DATE": ("demo_target1_UPD", "END_DATE")},
        "demo_target1_INS": {"Key": ("SEQTRANS", "NEXTVAL"), "LEAD_CO_MNE": ("demo_source1", "LEAD_CO_MNE"),
            "BRANCH_CO_MNE": ("demo_source1", "BRANCH_CO_MNE"), "MIS_DATE": ("demo_source1", "MIS_DATE"),
            "ID": ("demo_source1", "ID"), "DESCRIPTION": ("demo_source1", "DESCRIPTION"),
            "SHORT_NAME": ("demo_source1", "SHORT_NAME"), "CREATED_BY": ("EXPTRANS", "o_CREATED_BY"),
            "CREATED_TIME": ("EXPTRANS", "o_CREATED_TIME"), "UPDATED_BY": ("demo_target1_INS", "UPDATED_BY"),
            "UPDATED_TIME": ("demo_target1_INS", "UPDATED_TIME"), "ACTIVE_FLAG": ("demo_target1_INS", "ACTIVE_FLAG"),
            "START_DATE": ("demo_target1_INS", "START_DATE"), "END_DATE": ("demo_target1_INS", "END_DATE")},
        "demo_target6": {"ACCT_ID": ("demo_source4", "ACCT_ID"), "ACCT_TYP": ("exp_TRANS", "o_acc_trim"),
            "ACCT_DESC": ("exp_TRANS1", "o_ACCT_DESC"), "CR8_DT": ("demo_source4", "CR8_DT"),
            "CRDT_LN": ("exp_TRANS", "o_crdt_trim"), "CLSR_DT": ("demo_source4", "CLSR_DT"),
            "ACCT_STAT_CD": ("demo_source4", "ACCT_STAT_CD"), "TX_ID": ("demo_source3", "TX_ID"),
            "ACCT_KEY": ("SEQ_GEN", "NEXTVAL"), "TX_DTTM": ("demo_source3", "TX_DTTM"),
            "TX_AMT": ("agg_TRANS", "o_TX_AMT"), "TX_TYPE_CD": ("exp_TRANS", "o_ACCT_ID")},
        "demo_target5": {"ACCT_ID": ("demo_source4", "ACCT_ID"), "FIRST_NM": ("lkp_TRANS2", "FIRST_NM"),
            "LAST_NM": ("demo_source3", "LAST_NM"), "BAL_AMT": ("demo_source3", "BAL_AMT"),
            "CRDT_SCORE": ("lkp_TRANS3", "CRDT_SCORE")},
        "demo_target3": {"PRODUCT_ID": ("demo_source5", "PRODUCT_ID"), "PRODUCT_NM": ("demo_source5", "PRODUCT_NM"),
            "PRODUCT_NO": ("demo_source5", "PRODUCT_NO"), "COLOR": ("demo_source5", "COLOR"),
            "STD_COST": ("demo_source5", "STD_COST"), "LIST_PRICE": ("demo_source5", "LIST_PRICE"),
            "SELL_ST_DT": ("exp_TRANS2", "o_SELL_ST_DT"), "SELL_ED_DT": ("exp_TRANS2", "o_SELL_ED_DT")},
        "demo_target21": {"Title": ("demo_source2", "Title"), "Gender": ("demo_source2", "Gender_Code"),
            "First_Name": ("demo_source2", "First_Name"), "Middle_Name": ("demo_source2", "Middle_Name"),
            "Last_Name": ("demo_source2", "Last_Name"), "Member_Identifier": ("demo_source2", "Member_ID"),
            "Member_Suffix": ("demo_source2", "Member_Suffix"), "Date_of_Birth": ("demo_source2", "Birth_Date"),
            "Member_Number": ("demo_source2", "Member_Record_Number"), "Soc_Number": ("demo_source2", "Social_Security_Number"),
            "Type_Code": ("demo_source2", "Member_Type_Code"), "Relationship_to_Subscriber_Code": ("demo_source2", "Relationship_to_Subscriber_Code"),
            "Relationship_to_Subscriber_Code_Label": ("EXPTRANS", "o_Relationship_to_Subscriber_Code_Label"),
            "Effective_Date": ("demo_source2", "Original_Effective_Date")},
        "demo_target2": {"Title": ("demo_source2", "Title"), "Gender": ("demo_source2", "Gender_Code"),
            "First_Name": ("demo_source2", "First_Name"), "Middle_Name": ("demo_source2", "Middle_Name"),
            "Last_Name": ("demo_source2", "Last_Name"), "Member_Identifier": ("demo_source2", "Member_ID"),
            "Member_Suffix": ("demo_source2", "Member_Suffix"), "Date_of_Birth": ("demo_source2", "Birth_Date"),
            "Member_Number": ("demo_source2", "Member_Record_Number"), "Soc_Number": ("demo_source2", "Social_Security_Number"),
            "Type_Code": ("demo_source2", "Member_Type_Code"), "Relationship_to_Subscriber_Code": ("demo_source2", "Relationship_to_Subscriber_Code"),
            "Relationship_to_Subscriber_Code_Label": ("EXPTRANS", "o_Relationship_to_Subscriber_Code_Label"),
            "Effective_Date": ("demo_source2", "Original_Effective_Date")},
    }
    for instance, fields in expected.items():
        mapping = "m_demo_mapping2" if instance.startswith("demo_target1") else (
            "m_demo_mapping1" if instance in {"demo_target3", "demo_target5", "demo_target6"}
            else "m_demo_mapping3")
        for field, terminal in fields.items():
            assert graph.chain(mapping, instance, field)[-1][:2] == terminal, (
                f"XML connector lines: resolved chain for {instance}.{field} changed")


def test_lineage_cli_output_is_deterministic(tmp_path):
    output = tmp_path / "lineage.md"
    output.write_text(generate_lineage())
    committed = Path(__file__).resolve().parents[3] / "docs/pyspark/lineage.md"
    assert output.read_text() == committed.read_text()
