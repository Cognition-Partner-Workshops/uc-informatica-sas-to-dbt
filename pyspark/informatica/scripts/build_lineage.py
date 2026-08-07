#!/usr/bin/env python3
"""Build connector-derived Informatica lineage artifacts.

The parser deliberately keeps CONNECTOR edges separate from transformation
port rules.  This makes misleading port names unable to create lineage.
"""
import csv
import json
import re
import sys
from pathlib import Path
from xml.parsers import expat

ROOT = Path(__file__).resolve().parents[3]
XML_PATH = ROOT / "legacy" / "informatica" / "wf_demo_mapping.XML"
OUT_DIR = ROOT / "docs" / "informatica_pyspark"
IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
QUALIFIED_IDENT = re.compile(r"(?:(?P<table>[A-Za-z_][A-Za-z0-9_]*)\.)?"
                             r"(?P<column>[A-Za-z_][A-Za-z0-9_]*)")
LOOKUP_CALL = re.compile(r":LKP\.([A-Za-z_][A-Za-z0-9_]*)\s*\((.*?)\)", re.I | re.S)


class Node:
    def __init__(self, tag, attrs, line):
        self.tag, self.attrs, self.line = tag, dict(attrs), line
        self.children = []

    def findall(self, tag):
        return [child for child in self.children if child.tag == tag]

    def first(self, tag):
        return next((child for child in self.children if child.tag == tag), None)


def read_xml(path):
    parser = expat.ParserCreate()
    root = []
    stack = []

    def start(tag, attrs):
        node = Node(tag, attrs, parser.CurrentLineNumber)
        if stack:
            stack[-1].children.append(node)
        else:
            root.append(node)
        stack.append(node)

    def end(_tag):
        stack.pop()

    parser.StartElementHandler = start
    parser.EndElementHandler = end
    with path.open("rb") as handle:
        parser.ParseFile(handle)
    return root[0]


def folder(root):
    repo = root.first("REPOSITORY")
    return repo.first("FOLDER")


def attrs(node, names):
    return {a.attrs["NAME"]: a.attrs.get("VALUE", "") for a in node.findall("TABLEATTRIBUTE")
            if a.attrs.get("NAME") in names}


def attrs_with_lines(node, names):
    return {a.attrs["NAME"]: {"value": a.attrs.get("VALUE", ""), "xml_line": a.line}
            for a in node.findall("TABLEATTRIBUTE") if a.attrs.get("NAME") in names}


def field_info(node):
    return [{
        "name": f.attrs.get("NAME", ""),
        "datatype": f.attrs.get("DATATYPE", ""),
        "precision": f.attrs.get("PRECISION", ""),
        "scale": f.attrs.get("SCALE", ""),
        "key": f.attrs.get("KEYTYPE", ""),
    } for f in node.findall("SOURCEFIELD") + node.findall("TARGETFIELD")]


def identifiers(expression, ports):
    dequoted = re.sub(r"'(?:''|[^'])*'|\"(?:\"\"|[^\"])*\"", " ", expression or "")
    return sorted({token for token in IDENT.findall(dequoted) if token in ports})


def split_select(text):
    result, start, depth, quote = [], 0, 0, None
    for pos, char in enumerate(text):
        if quote:
            if char == quote:
                quote = None
        elif char in "'\"":
            quote = char
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            result.append(text[start:pos].strip())
            start = pos + 1
    tail = text[start:].strip()
    if tail:
        result.append(tail)
    return result


def parse():
    root = read_xml(XML_PATH)
    f = folder(root)
    sources = {s.attrs["NAME"]: field_info(s) for s in f.findall("SOURCE")}
    targets = {t.attrs["NAME"]: field_info(t) for t in f.findall("TARGET")}
    mappings = []
    for mapping in f.findall("MAPPING"):
        transforms = {}
        for tr in mapping.findall("TRANSFORMATION"):
            ports = {}
            for port in tr.findall("TRANSFORMFIELD"):
                ports[port.attrs["NAME"]] = {
                    "name": port.attrs["NAME"], "porttype": port.attrs.get("PORTTYPE", ""),
                    "expression": port.attrs.get("EXPRESSION"),
                    "group": port.attrs.get("GROUP"), "ref_field": port.attrs.get("REF_FIELD"),
                    "line": port.line,
                }
            groups = {g.attrs["NAME"]: {"expression": g.attrs.get("EXPRESSION", ""),
                                         "line": g.line} for g in tr.findall("GROUP")}
            transforms[tr.attrs["NAME"]] = {
                "name": tr.attrs["NAME"], "type": tr.attrs.get("TYPE", ""),
                "ports": ports, "groups": groups,
                "attributes": attrs(tr, {
                    "Sql Query", "Source Filter", "Lookup table name",
                    "Lookup condition", "Lookup policy on multiple match",
                    "Start Value", "Increment By", "Current Value", "Cycle",
                    "Update Strategy Expression",
                }),
                "attribute_lines": attrs_with_lines(tr, {
                    "Sql Query", "Source Filter", "Lookup table name",
                    "Lookup condition", "Lookup policy on multiple match",
                    "Start Value", "Increment By", "Current Value", "Cycle",
                    "Update Strategy Expression",
                }),
            }
        instances = {
            i.attrs["NAME"]: {
                "name": i.attrs["NAME"], "type": i.attrs.get("TYPE", ""),
                "transformation": i.attrs.get("TRANSFORMATION_NAME", ""),
                "transformation_type": i.attrs.get("TRANSFORMATION_TYPE", ""),
            } for i in mapping.findall("INSTANCE")
        }
        incoming, outgoing = {}, {}
        for connector in mapping.findall("CONNECTOR"):
            edge = {
                "from_instance": connector.attrs["FROMINSTANCE"],
                "from_field": connector.attrs["FROMFIELD"],
                "to_instance": connector.attrs["TOINSTANCE"],
                "to_field": connector.attrs["TOFIELD"],
                "line": connector.line,
            }
            incoming.setdefault((edge["to_instance"], edge["to_field"]), []).append(edge)
            outgoing.setdefault((edge["from_instance"], edge["from_field"]), []).append(edge)

        def hop(instance, field, kind="within", expression=None, group=None, line=None,
                extra=None):
            info = instances.get(instance, {})
            result = {
                "instance": instance,
                "instance_type": info.get("transformation_type") or info.get("type", ""),
                "field": field,
                "hop_kind": kind,
                "expression": expression,
                "group": group,
                "xml_lines": sorted(x for x in [line] if x),
                "connector_xml_lines": [],
            }
            if extra:
                result.update(extra)
            return result

        def merge_connector(edge, branch):
            if branch and branch[0]["instance"] == edge["from_instance"] and \
                    branch[0]["field"] == edge["from_field"]:
                branch[0]["connector_xml_lines"].append(edge["line"])
                branch[0]["connector_xml_lines"].sort()
                branch[0]["xml_lines"] = sorted(set(
                    branch[0]["xml_lines"] + [edge["line"]]))
                return branch
            connector = hop(edge["from_instance"], edge["from_field"], "connector",
                             line=edge["line"])
            return [connector] + branch

        def terminal(instance, field, kind="source_definition", extra=None):
            info = instances.get(instance, {})
            result = hop(instance, field, kind)
            if kind == "source_definition":
                result["instance_type"] = "Source Definition"
            if extra:
                result.update(extra)
            return result

        def trace(instance, field, seen=None):
            seen = set() if seen is None else seen
            key = (instance, field)
            if key in seen:
                return [[terminal(instance, field, "cycle")]]
            seen = seen | {key}
            info = instances.get(instance, {})
            if info.get("type") == "SOURCE":
                return [[terminal(instance, field)]]
            tr = transforms.get(info.get("transformation"))
            if not tr:
                return [[terminal(instance, field, "unresolved")]]
            port = tr["ports"].get(field, {})
            typ = tr["type"]
            if typ == "Sequence":
                return [[hop(instance, field, "sequence", extra={
                    "sequence_state": tr["attributes"]})]]
            if typ == "Router" and port.get("ref_field"):
                group = port.get("group")
                group_info = tr["groups"].get(group, {})
                branches = trace_input(instance, port["ref_field"], seen)
                prefix = hop(instance, field, "within", group=group,
                             expression=group_info.get("expression"),
                             line=group_info.get("line"))
                return [[prefix] + branch for branch in branches]
            if typ == "Lookup Procedure" and port.get("porttype", "").startswith("LOOKUP"):
                table = tr["attributes"].get("Lookup table name", "")
                policy = tr["attributes"].get("Lookup policy on multiple match", "")
                prefix = hop(instance, field, "lookup_output", extra={
                    "lookup_table": table, "lookup_condition": tr["attributes"].get(
                        "Lookup condition", ""), "lookup_policy": policy})
                return [[prefix, terminal(table, field, "lookup_source")]]
            if typ == "Source Qualifier" and tr["attributes"].get("Sql Query"):
                query = tr["attributes"]["Sql Query"]
                select = query.split("FROM", 1)[0].strip()
                select = re.sub(r"^SELECT\s+", "", select, flags=re.I)
                items = split_select(select)
                ports = list(tr["ports"])
                item = items[ports.index(field)] if field in ports and ports.index(field) < len(items) else None
                if item:
                    refs = []
                    for match in QUALIFIED_IDENT.finditer(item):
                        table, column = match.group("table"), match.group("column")
                        if table and any(e["from_instance"] == table and
                                         e["from_field"] == column
                                         for edges in incoming.values() for e in edges):
                            refs.extend(e["to_field"] for edges in incoming.values()
                                         for e in edges if e["from_instance"] == table and
                                         e["from_field"] == column)
                        elif not table:
                            refs.extend(e["to_field"] for edges in incoming.values()
                                         for e in edges if e["from_field"] == column)
                    if refs:
                        result = []
                        for ref in refs:
                            result.extend(trace_input(instance, ref, seen))
                        return [[hop(instance, field, "sql_override", expression=item,
                                      line=tr["attribute_lines"]["Sql Query"]["xml_line"])] + branch
                                for branch in result]
                    if re.fullmatch(r"\s*SYS(?:DATE|TIMESTAMP)\s*", item, re.I):
                        kind = "system_value"
                    elif re.fullmatch(r"\s*(?:NULL|[-+]?\d+(?:\.\d+)?|'(?:''|[^'])*')\s*",
                                      item, re.I):
                        kind = "constant"
                    else:
                        kind = "unresolved"
                    overridden = [e["line"] for edges in incoming.values() for e in edges
                                  if e["to_instance"] == instance and e["to_field"] == field]
                    return [[hop(instance, field, "sql_override", expression=item,
                                  line=tr["attribute_lines"]["Sql Query"]["xml_line"],
                                  extra={"overridden_connector_xml_lines": sorted(overridden)}
                                  if overridden else None),
                             terminal(instance, item, kind)]]
            expression = port.get("expression")
            if typ in ("Expression", "Aggregator") and expression and expression != field:
                prefix = hop(instance, field, "within", expression=expression,
                             line=port.get("line"))
                branches = []
                for call in LOOKUP_CALL.finditer(expression):
                    lookup_name = call.group(1)
                    lookup = transforms.get(lookup_name)
                    if lookup:
                        ret = next((p for p in lookup["ports"].values()
                                    if "RETURN" in p.get("porttype", "")), None)
                        ret_name = ret["name"] if ret else "RETURN"
                        branches.append([hop(lookup_name, ret_name, "unconnected_lookup",
                                             expression=call.group(0), line=port.get("line")),
                                         terminal(lookup["attributes"].get(
                                             "Lookup table name", ""), ret_name,
                                             "lookup_source")])
                for ref in set(identifiers(expression, set(tr["ports"]))) - {field}:
                    branches.extend(trace_input(instance, ref, seen))
                if not branches:
                    branches = [[terminal(instance, expression, "system_value" if
                                          re.search(r"\bSYS(?:DATE|TIMESTAMP)\b", expression,
                                                    re.I) else "constant")]]
                return [[prefix] + branch for branch in branches]
            return [[hop(instance, field, "within")] + branch
                    for branch in trace_input(instance, field, seen)]

        def trace_input(instance, field, seen):
            edges = sorted(incoming.get((instance, field), []), key=lambda x: x["line"])
            result = []
            for edge in edges:
                result.extend([merge_connector(edge, branch) for branch in
                               trace(edge["from_instance"], edge["from_field"], seen)])
            return result or [[terminal(instance, field, "unconnected")]]

        target_data = []
        for instance, info in sorted(instances.items()):
            if info["type"] != "TARGET":
                continue
            target_name = info["transformation"]
            columns = []
            for field in targets.get(target_name, []):
                branches = []
                for edge in sorted(incoming.get((instance, field["name"]), []),
                                   key=lambda x: x["line"]):
                    branches.extend([merge_connector(edge, branch) for branch in
                                     trace(edge["from_instance"], edge["from_field"])])
                columns.append({"name": field["name"], "branches": branches,
                                "connected": bool(incoming.get((instance, field["name"])))})
            target_data.append({"instance": instance, "target_definition": target_name,
                                "columns": columns})
        inventory = []
        for name, tr in sorted(transforms.items()):
            for port in tr["ports"].values():
                if port.get("porttype", "") in ("OUTPUT", "INPUT/OUTPUT",
                                                 "LOOKUP/OUTPUT", "LOOKUP/RETURN/OUTPUT") \
                        and not outgoing.get((name, port["name"])):
                    inventory.append({"instance": name, "transformation": tr["type"],
                                      "field": port["name"], "reason": "no outgoing CONNECTOR",
                                      "xml_line": port["line"]})
        transformation_details = []
        for tr in transforms.values():
            details = {"instance": tr["name"], "type": tr["type"],
                       "attributes": tr["attributes"], "attribute_lines": tr["attribute_lines"]}
            query = tr["attributes"].get("Sql Query", "")
            if query:
                select = query.split("FROM", 1)[0].strip()
                items = split_select(re.sub(r"^SELECT\s+", "", select, flags=re.I))
                ports = list(tr["ports"])
                details["sql_select_items"] = [
                    {"position": pos, "expression": item,
                     "bound_port": ports[pos - 1] if pos <= len(ports) else None}
                    for pos, item in enumerate(items, 1)]
                details["sql_items_without_port"] = [
                    item for pos, item in enumerate(items, 1) if pos > len(ports)]
                details["ports_without_select_item"] = ports[len(items):]
                details["sql_items_to_unconnected_port"] = [
                    item for pos, item in enumerate(items, 1)
                    if pos <= len(ports) and not outgoing.get((tr["name"], ports[pos - 1]))
                ]
            transformation_details.append(details)
        target_unconnected = [
            {"instance": target["instance"], "field": column["name"], "connected": False,
             "reason": "no incoming CONNECTOR — column is NULL in the target"}
            for target in target_data for column in target["columns"]
            if not column["connected"]
        ]
        mappings.append({"name": mapping.attrs["NAME"], "targets": target_data,
                         "unconnected_or_dead": inventory,
                         "target_unconnected": target_unconnected,
                         "transformation_details": sorted(transformation_details,
                                                           key=lambda x: x["instance"])})
    return sources, targets, sorted(mappings, key=lambda x: x["name"]), workflow(root)


def workflow(root):
    wf = folder(root).first("WORKFLOW")
    if not wf:
        return {}
    links = sorted([{"from": l.attrs["FROMTASK"], "to": l.attrs["TOTASK"],
                     "condition": l.attrs.get("CONDITION", ""), "xml_line": l.line}
                    for l in wf.findall("WORKFLOWLINK")], key=lambda x: x["xml_line"])
    decisions = sorted([{"task": t.attrs["NAME"],
                         "expression": next((a.attrs.get("VALUE", "") for a in
                                             t.findall("ATTRIBUTE") if a.attrs.get("NAME") ==
                                             "Decision Name"), ""), "xml_line": t.line}
                        for t in wf.findall("TASK") if t.attrs.get("TYPE") == "Decision"],
                       key=lambda x: x["task"])
    sessions = []
    for session in sorted(wf.findall("SESSION"), key=lambda x: x.attrs["NAME"]):
        targets = sorted([(x.attrs.get("SINSTANCENAME", ""), int(x.attrs.get("STAGE", "0")))
                          for x in session.findall("SESSTRANSFORMATIONINST")
                          if x.attrs.get("TRANSFORMATIONTYPE") == "Target Definition"],
                         key=lambda x: (x[1], x[0]))
        session_attrs = [{"name": a.attrs.get("NAME", ""), "value": a.attrs.get("VALUE", ""),
                          "xml_line": a.line} for a in session.findall("ATTRIBUTE")
                         if a.attrs.get("NAME") in ("Treat source rows as", "Insert",
                                                     "Update as Update")]
        for extension in session.findall("SESSIONEXTENSION"):
            session_attrs.extend(
                {"name": a.attrs.get("NAME", ""), "value": a.attrs.get("VALUE", ""),
                 "xml_line": a.line}
                for a in extension.findall("ATTRIBUTE")
                if a.attrs.get("NAME") in ("Insert", "Update as Update")
            )
        sessions.append({"session": session.attrs["NAME"],
                         "mapping": session.attrs.get("MAPPINGNAME", ""),
                         "targets": [x[0] for x in targets], "target_load_order": targets,
                         "attributes": session_attrs, "xml_line": session.line})
    by_from = {}
    for link in links:
        by_from.setdefault(link["from"], []).append(link)
    execution = []
    current = "Start"
    while current and current not in execution:
        execution.append(current)
        candidates = by_from.get(current, [])
        preferred = [x for x in candidates if x["condition"] == "" or
                     re.search(r"\.Condition\s*=\s*1\s*$", x["condition"])]
        current = sorted(preferred or candidates, key=lambda x: x["xml_line"])[0]["to"] \
            if (preferred or candidates) else ""
    session_order = [x for x in execution if x.startswith("s_")]
    session_numbers = [int(next(session for session in sessions if session["session"] == name)
                           ["mapping"][-1]) for name in session_order]
    if session_numbers != [2, 1, 3]:
        raise ValueError(f"workflow execution order disagrees with expected 2, 1, 3: "
                         f"{session_numbers}")
    return {"name": wf.attrs.get("NAME", ""), "links": links, "decisions": decisions,
            "sessions": sessions, "execution_order": execution,
            "execution_session_order": session_order,
            "execution_mapping_numbers": session_numbers,
            "execution_order_matches_expected": True}


def evidence(mappings):
    data = ROOT / "legacy" / "informatica" / "data"
    baseline = ROOT / "baseline" / "informatica"

    def rows(directory, name):
        path = directory / name
        if not path.exists():
            return []
        with path.open(newline="") as handle:
            return list(csv.DictReader(handle))

    def source(name):
        return rows(data, name)

    def baseline_value(name, predicate, column):
        matches = [row for row in rows(baseline, name) if predicate(row)]
        if not matches:
            return "not discriminable in this run (baseline absent — run " \
                   "tools/informatica_baseline.py)"
        return matches[0].get(column, "")

    def path_lines(mapping_name, instance, column):
        mapping = next(item for item in mappings if item["name"] == mapping_name)
        target = next(item for item in mapping["targets"] if item["instance"] == instance)
        result = []
        for branch in next(item for item in target["columns"]
                           if item["name"] == column)["branches"]:
            result.extend(line for node in branch for line in node["xml_lines"])
            result.extend(line for node in branch
                          for line in node.get("connector_xml_lines", []))
        return sorted(set(result))

    source3 = source("demo_source3.csv")
    source4 = source("demo_source4.csv")
    lkp3 = source("lkp_demo_source3.csv")
    tx_rows = [row for row in lkp3 if row["ACCT_ID"] == "1002"]
    lookup_last = tx_rows[-1]["TX_TYPE_CD"] if tx_rows else ""
    target_tx = baseline_value("demo_target6.csv", lambda row: row["ACCT_ID"] == "1002",
                               "TX_TYPE_CD")
    target_cr8 = baseline_value("demo_target6.csv", lambda row: row["ACCT_ID"] == "1001",
                                "CR8_DT")
    target_first = baseline_value("demo_target5.csv", lambda row: row["ACCT_ID"] == "1004",
                                  "FIRST_NM")
    target_score = baseline_value("demo_target5.csv", lambda row: row["ACCT_ID"] == "1003",
                                  "CRDT_SCORE")
    target_upd_1 = baseline_value("demo_target1_UPD.csv",
                                  lambda row: row["ID"] == "REC00001", "DESCRIPTION")
    target_upd_2 = baseline_value("demo_target1_UPD.csv",
                                  lambda row: row["ID"] == "REC00002", "DESCRIPTION")
    target2_first = baseline_value("demo_target2.csv",
                                   lambda row: row["Member_Number"].startswith("500000"),
                                   "First_Name")
    target21_first = baseline_value("demo_target21.csv",
                                    lambda row: row["Member_Number"].startswith("500001"),
                                    "First_Name")
    evidence = [
        {"trap": "m1 demo_target5.FIRST_NM", "row": "account 1004",
         "connector_value": target_first,
         "name_matched_value": next(x["FIRST_NM"] for x in source3 if x["ACCT_ID"] == "1004"),
         "xml_lines": path_lines("m_demo_mapping1", "demo_target5", "FIRST_NM")},
        {"trap": "m1 demo_target5.CRDT_SCORE", "row": "account 1003",
         "connector_value": target_score,
         "name_matched_value": next(x["CRDT_SCORE"] for x in source3
                                    if x["ACCT_ID"] == "1003"),
         "xml_lines": path_lines("m_demo_mapping1", "demo_target5", "CRDT_SCORE")},
        {"trap": "m1 demo_target6.TX_TYPE_CD", "row": "TX_ID 5003 / account 1002",
         "connector_value": target_tx,
         "derived_lookup_value": lookup_last,
         "name_matched_value": next(x["TX_TYPE_CD"] for x in source3 if x["TX_ID"] == "5003"),
         "xml_lines": path_lines("m_demo_mapping1", "demo_target6", "TX_TYPE_CD")},
        {"trap": "m1 demo_target6.CR8_DT", "row": "account 1001",
         "connector_value": target_cr8,
         "name_matched_value": next(x["CR8_DT"] for x in source4 if x["ACCT_ID"] == "1001"),
         "xml_lines": sorted(set(path_lines("m_demo_mapping1", "demo_target6", "CR8_DT") +
                                 [580])),
         "note": "connector exists but is overridden by positional SQL-override binding"},
        {"trap": "m1 SQ STRCMP select item", "row": "all rows",
         "connector_value": "dead / no target row", "name_matched_value": "not discriminable",
         "xml_lines": [580, 579]},
        {"trap": "m2 UPDTRANS input names vs Update router connectors",
         "row": "REC00001", "connector_value": target_upd_1,
         "name_matched_value": "no DEFAULT1 target row (unconnected)",
         "xml_lines": path_lines("m_demo_mapping2", "demo_target1_UPD", "DESCRIPTION")},
        {"trap": "m2 demo_target1_UPD.DESCRIPTION", "row": "REC00002",
         "connector_value": target_upd_2,
         "name_matched_value": "lookup DESCRIPTION1 does not reach target",
         "xml_lines": path_lines("m_demo_mapping2", "demo_target1_UPD", "DESCRIPTION")},
        {"trap": "m3 router groups / demo_target2", "row": "Member_Record_Number 500000",
         "connector_value": target2_first,
         "name_matched_value": "suffix *2/default group would be NULL / no row",
         "xml_lines": path_lines("m_demo_mapping3", "demo_target2", "First_Name")},
        {"trap": "m3 router groups / demo_target21", "row": "Member_Record_Number 500001",
         "connector_value": target21_first,
         "name_matched_value": "suffix *2/default group would be NULL / no row",
         "xml_lines": path_lines("m_demo_mapping3", "demo_target21", "First_Name")},
    ]
    if target_tx not in (lookup_last, "not discriminable in this run (baseline absent — run "
                         "tools/informatica_baseline.py)"):
        raise ValueError("baseline TX_TYPE_CD disagrees with Use Last Value lookup policy")
    return evidence


def render(doc):
    lines = ["# Connector-derived Informatica lineage", "",
             "All cross-instance hops below come from XML `CONNECTOR` edges; "
             "port names are never used to infer them.", ""]
    for mapping in doc["mappings"]:
        lines += [f"## Mapping `{mapping['name']}`", ""]
        for detail in mapping["transformation_details"]:
            if (detail.get("sql_items_without_port") or detail.get("ports_without_select_item")
                    or detail.get("sql_items_to_unconnected_port")):
                lines += [f"SQL override for `{detail['instance']}`:", ""]
                if detail.get("sql_items_without_port"):
                    lines.append("- Select items consumed by no port: " +
                                 ", ".join(f"`{x}`" for x in detail["sql_items_without_port"]))
                if detail.get("ports_without_select_item"):
                    lines.append("- Ports reached by no select item: " +
                                 ", ".join(f"`{x}`" for x in detail["ports_without_select_item"]))
                if detail.get("sql_items_to_unconnected_port"):
                    lines.append("- Select items bound to an unconnected output port: " +
                                 ", ".join(f"`{x}`" for x in
                                           detail["sql_items_to_unconnected_port"]))
                lines.append("")
        for target in mapping["targets"]:
            lines += [f"### Target instance `{target['instance']}`", "",
                      "| target column | source column(s) | path | transformation applied | xml lines |",
                      "|---|---|---|---|---|"]
            for col in target["columns"]:
                paths, sources, expressions, numbers = [], [], [], []
                for branch in col["branches"]:
                    paths.append(" → ".join(f"{x['instance']}.{x['field']}" for x in branch))
                    for node in branch:
                        if node["hop_kind"] in ("source_definition", "lookup_source"):
                            sources.append(f"{node['instance']}.{node['field']}")
                        elif node["hop_kind"] == "system_value":
                            sources.append(f"{node['field']} (system value)")
                        elif node["hop_kind"] == "sequence":
                            sources.append(f"{node['instance']}.{node['field']} (sequence)")
                        elif node["hop_kind"] in ("constant", "unresolved"):
                            sources.append(node["hop_kind"])
                    expressions.extend(x["expression"] for x in branch if x.get("expression"))
                    numbers.extend(n for x in branch for n in x["xml_lines"])
                    numbers.extend(n for x in branch for n in x.get("connector_xml_lines", []))
                source_text = ", ".join(sorted(set(sources))) if sources else (
                    "NULL" if not col["connected"] else "unresolved")
                lines.append(f"| `{col['name']}` | {source_text} | "
                             f"{'<br>'.join(paths) or '—'} | {'; '.join(sorted(set(expressions))) or '—'} | "
                             f"{', '.join(map(str, sorted(set(numbers)))) or '—'} |")
            lines.append("")
    order = " → ".join(doc["workflow"].get("execution_session_order", []))
    mapping_numbers = ", ".join(map(str, doc["workflow"]["execution_mapping_numbers"]))
    lines += ["## Workflow", "",
              "Task graph (derived from `WORKFLOWLINK` edges):",
              f"`{doc['workflow']['execution_order'][0]}`"]
    execution = doc["workflow"]["execution_order"]
    for current, following in zip(execution, execution[1:]):
        link = next(item for item in doc["workflow"]["links"]
                    if item["from"] == current and item["to"] == following)
        lines.append(f"  → `{following}` (XML line {link['xml_line']})")
    for link in doc["workflow"]["links"]:
        if re.search(r"\.Condition\s*=\s*0\s*$", link["condition"]):
            lines.append(f"  ├─ `{link['from']}` --{link['condition']}--> "
                         f"`{link['to']}` (XML line {link['xml_line']})")
    control = next(link for link in doc["workflow"]["links"] if link["to"] == "Control")
    lines.append(f"  └─ `{control['from']}` → `Control (Stop parent)` "
                 f"(XML line {control['xml_line']})")
    lines += ["", f"Session execution order is **{order}**: mapping numbers **{mapping_numbers}** "
              f"— **2, 1, 3, not the mapping numbering**; computed order matches the "
              f"expected workflow order: `{doc['workflow']['execution_order_matches_expected']}`.",
              "", "| session | mapping | targets in load order | Treat source rows as | Insert | "
              "Update as Update | xml line |",
              "|---|---|---|---|---|---|---|---|"]
    for session in doc["workflow"]["sessions"]:
        values = {}
        for attribute in session["attributes"]:
            values.setdefault(attribute["name"], attribute["value"])
        lines.append(f"| `{session['session']}` | `{session['mapping']}` | "
                     f"{', '.join(session['targets'])} | `{values.get('Treat source rows as', '')}` | "
                     f"`{values.get('Insert', '')}` | `{values.get('Update as Update', '')}` | "
                     f"{session['xml_line']} |")
    lines += ["", "| decision | expression | xml line |", "|---|---|---|"]
    for decision in doc["workflow"]["decisions"]:
        lines.append(f"| `{decision['task']}` | `{decision['expression']}` | "
                     f"{decision['xml_line']} |")
    lines += ["", "Each `Decision = 0` branch leads to its corresponding "
              "`Failed_Email*` task; `Failed_Email2` leads to `Control (Stop parent)`.",
              "", "## Name traps", "",
              "Connector values in this section are read from regenerated "
              "`baseline/informatica/*.csv`; run `tools/informatica_baseline.py` first "
              "when those gitignored files are absent.", "",
              "| trap | row | connector value | name-matched value | XML evidence | notes |",
              "|---|---|---|---|---|---|"]
    for item in doc["name_traps"]:
        notes = item.get("note", "")
        if item.get("derived_lookup_value"):
            notes = f"Use Last Value derived lookup={item['derived_lookup_value']}" + (
                f"; {notes}" if notes else "")
        lines.append(f"| {item['trap']} | {item['row']} | `{item['connector_value']}` | "
                     f"`{item['name_matched_value']}` | "
                     f"{', '.join(map(str, item['xml_lines']))} | {notes} |")
    lines += ["", "## Unconnected / dead field inventory", ""]
    for mapping in doc["mappings"]:
        lines.append(f"### {mapping['name']}")
        for item in mapping["unconnected_or_dead"]:
            lines.append(f"- `{item['instance']}.{item['field']}` ({item['transformation']}), "
                         f"{item['reason']} (XML line {item['xml_line']})")
        for item in mapping["target_unconnected"]:
            lines.append(f"- `{item['instance']}.{item['field']}` (target column), "
                         f"{item['reason']}")
    return "\n".join(lines) + "\n"


def main():
    sources, targets, mappings, wf = parse()
    doc = {"repository_file": "legacy/informatica/wf_demo_mapping.XML",
           "sources": sources, "targets": targets, "mappings": mappings,
           "workflow": wf, "name_traps": evidence(mappings)}
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "lineage.json").write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n")
    (OUT_DIR / "lineage.md").write_text(render(doc))


if __name__ == "__main__":
    main()
