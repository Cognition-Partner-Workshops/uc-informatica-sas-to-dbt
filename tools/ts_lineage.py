#!/usr/bin/env python3
"""Deterministic lineage parser for multi-mapping PowerCenter folder exports.

Reads every folder export under legacy/informatica_ts/ (stdlib xml.etree only)
and writes, per export file <NAME>:
  docs/stm/ts/<NAME>.json - machine-readable source-to-target mapping
  docs/stm/ts/<NAME>.md   - per-mapping tables in session-execution order
plus docs/stm/ts/INVENTORY.md (per-workflow inventory and count check).

Same per-mapping shape as tools/informatica_lineage.py (sources, targets,
transformations, port-level lineage, lookup conditions, router groups, SQL
overrides), extended with Normalizer, Joiner, Sorter, Sequence generator,
Update Strategy, Mapplets (expanded inline), Source Qualifier Pre/Post SQL,
target-instance Pre/Post SQL, VSAM copybook fields, PowerExchange
(PWX_SEQ_NRDB2) definitions, and the workflow's session order, links and
Command tasks.

Every emitted string passes through a redactor: e-mail addresses become
<email>, home-directory paths become <path>, and the folder owner user names
of all processed exports become <owner>. Connection names, DESCRIPTION attributes and e-mail task contents
are never emitted.

The per-file counts of mappings, sessions, sources, targets, mapplets,
workflows and transformations by type are compared with a line count of the
raw XML (what `grep -c` reports); the tool exits 1 on any mismatch.
"""
import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_INPUT = os.path.join(REPO_ROOT, "legacy", "informatica_ts")
DEFAULT_OUT = os.path.join(REPO_ROOT, "docs", "stm", "ts")

IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
LKP_CALL_RE = re.compile(r":LKP\.([A-Za-z_][A-Za-z0-9_]*)", re.I)
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")
HOME_RE = re.compile(r"(?:/export)?/home\d*/[^/\s;:'\"|]+", re.I)
GENERIC_OWNERS = {"", "administrator"}
MAX_CHAIN = 200

INTERESTING_ATTRS = {
    "Source Qualifier": ["Sql Query", "User Defined Join", "Source Filter",
                         "Pre SQL", "Post SQL", "Select Distinct",
                         "Number Of Sorted Ports"],
    "Lookup Procedure": ["Lookup table name", "Lookup condition",
                         "Lookup policy on multiple match", "Lookup Sql Override",
                         "Lookup Source Filter", "Source Type",
                         "Dynamic Lookup Cache"],
    "Sequence": ["Start Value", "Increment By", "End Value", "Current Value",
                 "Cycle", "Reset", "Number of Cached Values"],
    "Update Strategy": ["Update Strategy Expression", "Forward Rejected Rows"],
    "Joiner": ["Join Type", "Join Condition", "Sorted Input",
               "Null ordering in master", "Null ordering in detail"],
    "Sorter": ["Distinct", "Case Sensitive", "Null Treated Low"],
    "Normalizer": ["Reset", "Restart"],
    "Filter": ["Filter Condition"],
    "Aggregator": ["Sorted Input"],
}
GRP_COUNTED = ("MAPPING", "SESSION", "SOURCE", "TARGET", "MAPPLET", "WORKFLOW",
               "TRANSFORMATION")
SESSION_EXT_ATTRS = ("Source filename", "Source file directory", "Input Type",
                     "Command", "Output filename", "Output file directory",
                     "Output Type", "Pre SQL", "Post SQL", "Insert SQL override",
                     "File Name Override", "Map Name Override",
                     "Schema Name Override", "Target load type",
                     "Truncate target table option", "Insert", "Delete",
                     "Update as Update", "Update as Insert", "Update else Insert",
                     "Append if Exists")


class Redactor:
    def __init__(self, owners):
        names = sorted({o for o in owners if o and o.lower() not in GENERIC_OWNERS},
                       key=lambda s: (-len(s), s))
        self.owner_re = (re.compile(r"(?<![A-Za-z0-9_])(?:%s)(?![A-Za-z0-9_])" %
                                    "|".join(re.escape(n) for n in names), re.I)
                         if names else None)
        self.hits = {"email": 0, "path": 0, "owner": 0}

    def text(self, s):
        if not isinstance(s, str) or not s:
            return s
        s, n = EMAIL_RE.subn("<email>", s)
        self.hits["email"] += n
        s, n = HOME_RE.subn("<path>", s)
        self.hits["path"] += n
        if self.owner_re:
            s, n = self.owner_re.subn("<owner>", s)
            self.hits["owner"] += n
        return s

    def walk(self, obj):
        if isinstance(obj, dict):
            return {self.text(k): self.walk(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self.walk(v) for v in obj]
        return self.text(obj)


def attrs_of(e, drop=("DESCRIPTION",)):
    return {k: v for k, v in sorted(e.attrib.items()) if k not in drop}


def split_select_list(text):
    parts, start, depth, quote = [], 0, 0, None
    for i, char in enumerate(text):
        if quote:
            if char == quote:
                quote = None
        elif char in ("'", '"'):
            quote = char
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            parts.append(text[start:i].strip())
            start = i + 1
    parts.append(text[start:].strip())
    return parts


def grep_counts(path):
    """Line counts as `grep -c '<TAG '` reports them, plus per-type counts."""
    counts = {tag: 0 for tag in GRP_COUNTED}
    by_type = {}
    type_re = re.compile(r'\bTYPE ="([^"]*)"')
    with open(path, encoding="latin-1") as fh:
        for line in fh:
            for tag in GRP_COUNTED:
                if "<%s " % tag in line:
                    counts[tag] += 1
            if "<TRANSFORMATION " in line:
                m = type_re.search(line)
                key = m.group(1) if m else "(none)"
                by_type[key] = by_type.get(key, 0) + 1
    return counts, dict(sorted(by_type.items()))


def parse_fields(elems, parent=""):
    out = []
    for f in elems:
        path = f"{parent}.{f.get('NAME')}" if parent else f.get("NAME")
        info = {"name": f.get("NAME"), "path": path, "datatype": f.get("DATATYPE"),
                "precision": f.get("PRECISION"), "scale": f.get("SCALE")}
        for k, attr in (("key", "KEYTYPE"), ("level", "LEVEL"), ("occurs", "OCCURS"),
                        ("picture", "PICTURETEXT"), ("offset", "PHYSICALOFFSET"),
                        ("length", "PHYSICALLENGTH"), ("field_type", "FIELDTYPE"),
                        ("usage", "USAGE"), ("group", "GROUP"),
                        ("nullable", "NULLABLE")):
            if f.get(attr) not in (None, ""):
                info[k] = f.get(attr)
        out.append(info)
        out += parse_fields(f.findall(f.tag), path)
    return out


def parse_transformation(t, prefix=""):
    ttype = t.get("TYPE")
    info = {"name": prefix + t.get("NAME"), "type": ttype, "fields": {},
            "groups": [], "attributes": {}, "source_fields": [],
            "vsam": t.get("ISVSAM_NORMALIZER") == "YES",
            "ref_source": t.get("REF_SOURCE_NAME")}
    for f in t.findall("TRANSFORMFIELD"):
        info["fields"][f.get("NAME")] = {
            "expression": f.get("EXPRESSION"), "porttype": f.get("PORTTYPE") or "",
            "group": f.get("GROUP"), "ref_field": f.get("REF_FIELD"),
            "ref_source_field": f.get("REF_SOURCE_FIELD"),
            "datatype": f.get("DATATYPE"), "expressiontype": f.get("EXPRESSIONTYPE"),
            "sortkey": f.get("ISSORTKEY"), "sortdir": f.get("SORTDIRECTION"),
        }
    for g in t.findall("GROUP"):
        info["groups"].append({"name": g.get("NAME"), "type": g.get("TYPE"),
                               "expression": g.get("EXPRESSION")})
    for a in t.findall("TABLEATTRIBUTE"):
        if a.get("NAME") in INTERESTING_ATTRS.get(ttype, []) and a.get("VALUE"):
            info["attributes"][a.get("NAME")] = a.get("VALUE")
    info["source_fields"] = parse_fields(t.findall("SOURCEFIELD"))
    return info


def parse_container(c, prefix=""):
    """Transformations, instances and connectors of a MAPPING or MAPPLET."""
    transforms = {prefix + t.get("NAME"): parse_transformation(t, prefix)
                  for t in c.findall("TRANSFORMATION")}
    instances = {}
    for i in c.findall("INSTANCE"):
        name = prefix + i.get("NAME")
        tname = i.get("TRANSFORMATION_NAME")
        instances[name] = {
            "name": name, "type": i.get("TYPE"),
            "transformation_name": (prefix + tname
                                    if i.get("TYPE") == "TRANSFORMATION" else tname),
            "transformation_type": i.get("TRANSFORMATION_TYPE"),
            "associated_sources": [prefix + a.get("NAME") for a in
                                   i.findall("ASSOCIATED_SOURCE_INSTANCE")],
            "attributes": {a.get("NAME"): a.get("VALUE")
                           for a in i.findall("TABLEATTRIBUTE") if a.get("VALUE")},
        }
    connectors = [{"from_instance": prefix + c2.get("FROMINSTANCE"),
                   "from_field": c2.get("FROMFIELD"),
                   "to_instance": prefix + c2.get("TOINSTANCE"),
                   "to_field": c2.get("TOFIELD")} for c2 in c.findall("CONNECTOR")]
    return transforms, instances, connectors


def expand_mapplets(transforms, instances, connectors, mapplets):
    expansions = []
    for _ in range(10):
        todo = sorted(n for n, i in instances.items() if i["type"] == "MAPPLET")
        if not todo:
            break
        for name in todo:
            inst = instances.pop(name)
            mp = mapplets[inst["transformation_name"]]
            t2, i2, c2 = parse_container(mp, name + "/")
            transforms.update(t2)
            in_port, out_port = {}, {}
            for iname, iinfo in i2.items():
                tr = t2.get(iinfo["transformation_name"], {})
                if tr.get("type") == "Input Transformation":
                    for f in tr["fields"]:
                        in_port.setdefault(f, iname)
                elif tr.get("type") == "Output Transformation":
                    for f in tr["fields"]:
                        out_port.setdefault(f, iname)
            instances.update(i2)
            unresolved = 0
            for c in connectors:
                if c["to_instance"] == name:
                    c["to_instance"] = in_port.get(c["to_field"], name)
                    unresolved += c["to_instance"] == name
                if c["from_instance"] == name:
                    c["from_instance"] = out_port.get(c["from_field"], name)
                    unresolved += c["from_instance"] == name
            connectors.extend(c2)
            expansions.append({"instance": name, "mapplet": mp.get("NAME"),
                               "inner_instances": sorted(i2),
                               "unresolved_ports": unresolved})
    return sorted(expansions, key=lambda e: e["instance"])


def parse_mapping(m, folder_transforms, mapplets, sources, targets):
    name = m.get("NAME")
    transforms, instances, connectors = parse_container(m)
    for iname, inst in instances.items():
        if inst["type"] == "TRANSFORMATION" and inst["transformation_name"] not in transforms:
            ft = folder_transforms.get(inst["transformation_name"].split("/")[-1])
            if ft:
                transforms[inst["transformation_name"]] = ft
    expansions = expand_mapplets(transforms, instances, connectors, mapplets)
    incoming = {(c["to_instance"], c["to_field"]): (c["from_instance"], c["from_field"])
                for c in connectors}
    outgoing = {}
    for c in connectors:
        outgoing.setdefault(c["from_instance"], set()).add(c["to_instance"])

    target_instances = sorted(n for n, i in instances.items() if i["type"] == "TARGET")
    source_instances = sorted(n for n, i in instances.items() if i["type"] == "SOURCE")

    def transform_of(iname):
        inst = instances.get(iname)
        return transforms.get(inst["transformation_name"]) if inst else None

    lookup_tables = {t: tr["attributes"].get("Lookup table name")
                     for t, tr in transforms.items() if tr["type"] == "Lookup Procedure"}
    memo = {}

    def trace(iname, field, stack=frozenset()):
        key = (iname, field)
        if key in memo:
            return memo[key]
        if key in stack or len(stack) > 60:
            return [f"{iname}.{field} (cycle/depth limit)"], []
        stack = stack | {key}
        res = _trace(iname, field, stack)
        steps = list(dict.fromkeys(res[0]))
        if len(steps) > MAX_CHAIN:
            steps = steps[:MAX_CHAIN] + ["... (chain truncated)"]
        res = (steps, sorted(dict.fromkeys(res[1])))
        memo[key] = res
        return res

    def follow(iname, field, stack):
        up = incoming.get((iname, field))
        return trace(up[0], up[1], stack) if up else ([], [])

    def _trace(iname, field, stack):
        inst = instances.get(iname)
        if inst is None:
            return [f"{iname}.{field}"], []
        if inst["type"] == "SOURCE":
            return [f"{iname}.{field}"], [f"{iname}.{field}"]
        tr = transform_of(iname)
        if tr is None:
            return [f"{iname}.{field}"], []
        ttype, fld = tr["type"], tr["fields"].get(field, {})
        steps, srcs = [], []
        if ttype == "Sequence":
            a = tr["attributes"]
            return ([f"{iname}.{field} [sequence start={a.get('Start Value')} "
                     f"increment={a.get('Increment By')} current={a.get('Current Value')} "
                     f"cycle={a.get('Cycle')} reset={a.get('Reset')}]"],
                    [f"{iname} (generated)"])
        if ttype == "Normalizer" and not tr["vsam"]:
            pt = fld.get("porttype", "")
            if pt.startswith("GENERATED"):
                return [f"{iname}.{field} [normalizer {pt.split('/')[0].lower()}]"], \
                       [f"{iname} (generated)"]
            if pt == "OUTPUT":
                ref = fld.get("ref_source_field") or field
                ins = [p for p, pi in tr["fields"].items()
                       if pi["porttype"] == "INPUT" and pi.get("ref_source_field") == ref]
                steps.append(f"{iname}.{field} [normalizer: one row per occurrence of "
                             f"{', '.join(ins) or ref}]")
                for p in ins:
                    s2, src2 = follow(iname, p, stack)
                    steps += s2
                    srcs += src2
                return steps, srcs
        if ttype == "Router" and fld.get("ref_field"):
            grp = fld.get("group")
            gexpr = next((g["expression"] for g in tr["groups"] if g["name"] == grp), None)
            cond = f" WHERE {gexpr}" if gexpr else " (DEFAULT group)"
            steps.append(f"{iname}.{field} [router group {grp}{cond}]")
            s2, src2 = follow(iname, fld["ref_field"], stack)
            return steps + s2, srcs + src2
        if ttype == "Lookup Procedure" and fld.get("porttype", "").startswith("LOOKUP"):
            a = tr["attributes"]
            steps.append(f"{iname}.{field} [lookup {a.get('Lookup table name')}.{field} "
                         f"ON {a.get('Lookup condition')}]")
            srcs.append(f"{a.get('Lookup table name')}.{field} (lookup)")
            for pname, pinfo in tr["fields"].items():
                if "INPUT" in pinfo["porttype"]:
                    _, src2 = follow(iname, pname, stack)
                    srcs += [f"{s} (lookup key)" for s in src2]
            return steps, srcs
        expr = fld.get("expression")
        if expr and expr != field:
            steps.append(f"{iname}.{field} = {expr}")
            refs = [tok for tok in dict.fromkeys(IDENT_RE.findall(expr))
                    if tok in tr["fields"] and tok != field]
            for ref in refs:
                if (iname, ref) in incoming:
                    s2, src2 = follow(iname, ref, stack)
                else:
                    s2, src2 = trace(iname, ref, stack)
                steps += s2
                srcs += src2
            for lkp in LKP_CALL_RE.findall(expr):
                srcs.append(f"{lookup_tables.get(lkp, lkp)} (unconnected lookup {lkp})")
            if not refs and not LKP_CALL_RE.search(expr):
                srcs.append(f"literal/expression: {expr}")
            return steps, srcs
        steps.append(f"{iname}.{field}")
        s2, src2 = follow(iname, field, stack)
        return steps + s2, srcs + src2

    lineage = {}
    for tgt in target_instances:
        tdef = instances[tgt]["transformation_name"]
        cols = []
        for f in targets.get(tdef, {}).get("fields", []):
            col = f["name"]
            up = incoming.get((tgt, col))
            if up is None:
                cols.append({"column": col, "rule": "(not connected — NULL)",
                             "chain": [], "sources": []})
                continue
            steps, srcs = trace(up[0], up[1])
            cols.append({"column": col, "rule": steps[0] if steps else "",
                         "chain": steps, "sources": srcs})
        lineage[tgt] = {"target_table": tdef, "columns": cols}

    def downstream_targets(start):
        seen, todo, hits = set(), [start], set()
        while todo:
            cur = todo.pop()
            for nxt in outgoing.get(cur, ()):
                if nxt in seen:
                    continue
                seen.add(nxt)
                if instances.get(nxt, {}).get("type") == "TARGET":
                    hits.add(nxt)
                else:
                    todo.append(nxt)
        return sorted(hits)

    inst_by_tr = {}
    for iname, inst in instances.items():
        inst_by_tr.setdefault(inst["transformation_name"], []).append(iname)
    used = {t: tr for t, tr in sorted(transforms.items()) if t in inst_by_tr}

    physical = {}
    for t in target_instances:
        physical.setdefault(instances[t]["transformation_name"], []).append(t)
    lookup_details, sql_overrides, unconnected, agg_groupby = [], [], [], {}
    joiners, sorters, normalizers, sequences, upd, sqs = [], [], [], [], [], []
    for tname, tr in used.items():
        a, ttype = tr["attributes"], tr["type"]
        if ttype == "Lookup Procedure":
            table = a.get("Lookup table name")
            lookup_details.append({
                "transformation": tname, "table": table,
                "exists_in_export": table in sources or table in targets,
                "condition": a.get("Lookup condition"),
                "multiple_match_policy": a.get("Lookup policy on multiple match"),
                "sql_override": a.get("Lookup Sql Override"),
                "source_filter": a.get("Lookup Source Filter"),
                "ports": sorted(tr["fields"])})
        if ttype == "Source Qualifier":
            iname = inst_by_tr[tname][0]
            sqs.append({"transformation": tname,
                        "sources": sorted(instances[iname]["associated_sources"]),
                        "sql_query": a.get("Sql Query"), "pre_sql": a.get("Pre SQL"),
                        "post_sql": a.get("Post SQL"),
                        "source_filter": a.get("Source Filter"),
                        "user_defined_join": a.get("User Defined Join"),
                        "select_distinct": a.get("Select Distinct"),
                        "sorted_ports": a.get("Number Of Sorted Ports")})
            sql = a.get("Sql Query", "")
            mt = re.search(r"\bSELECT\s+(.*?)\s+\bFROM\b", sql, flags=re.I | re.S)
            if mt:
                ports = [n for n, f in tr["fields"].items()
                         if f["porttype"] in ("INPUT/OUTPUT", "OUTPUT")]
                sql_overrides.append({"transformation": tname, "sql": sql,
                                      "positional_bindings": [
                                          {"position": i + 1, "expression": e,
                                           "port": ports[i] if i < len(ports) else None}
                                          for i, e in enumerate(split_select_list(mt.group(1)))]})
        if ttype == "Aggregator":
            agg_groupby[tname] = [n for n, f in tr["fields"].items()
                                  if f.get("expressiontype") == "GROUPBY"]
        if ttype == "Joiner":
            joiners.append({"transformation": tname, "join_type": a.get("Join Type"),
                            "condition": a.get("Join Condition"),
                            "sorted_input": a.get("Sorted Input"),
                            "master_ports": [n for n, f in tr["fields"].items()
                                             if f["porttype"].endswith("MASTER")],
                            "detail_ports": [n for n, f in tr["fields"].items()
                                             if not f["porttype"].endswith("MASTER")]})
        if ttype == "Sorter":
            sorters.append({"transformation": tname, "distinct": a.get("Distinct"),
                            "case_sensitive": a.get("Case Sensitive"),
                            "keys": [{"port": n, "direction": f.get("sortdir")}
                                     for n, f in tr["fields"].items()
                                     if f.get("sortkey") == "YES"]})
        if ttype == "Normalizer":
            occurs = {}
            for f in tr["fields"].values():
                if f["porttype"] == "INPUT" and f.get("ref_source_field"):
                    occurs[f["ref_source_field"]] = occurs.get(f["ref_source_field"], 0) + 1
            normalizers.append({
                "transformation": tname, "vsam": tr["vsam"],
                "ref_source": tr["ref_source"],
                "occurs": {k: v for k, v in sorted(occurs.items()) if v > 1},
                "source_fields": [{"name": f["name"], "occurs": f.get("occurs"),
                                   "picture": f.get("picture")}
                                  for f in tr["source_fields"]],
                "generated_ports": [n for n, f in tr["fields"].items()
                                    if f["porttype"].startswith("GENERATED")]})
        if ttype == "Sequence":
            sequences.append({"transformation": tname,
                              "start_value": a.get("Start Value"),
                              "current_value": a.get("Current Value"),
                              "increment_by": a.get("Increment By"),
                              "end_value": a.get("End Value"), "cycle": a.get("Cycle"),
                              "reset": a.get("Reset"),
                              "cached_values": a.get("Number of Cached Values"),
                              "targets": sorted({t for i in inst_by_tr[tname]
                                                 for t in downstream_targets(i)})})
        if ttype == "Update Strategy":
            upd.append({"transformation": tname,
                        "expression": a.get("Update Strategy Expression"),
                        "forward_rejected_rows": a.get("Forward Rejected Rows"),
                        "targets": sorted({t for i in inst_by_tr[tname]
                                           for t in downstream_targets(i)})})
        for port, f in sorted(tr["fields"].items()):
            if f.get("expression") and ":LKP." in f["expression"].upper():
                unconnected.append({"transformation": tname, "port": port,
                                    "expression": f["expression"]})
    return {
        "name": name,
        "sources": source_instances,
        "source_tables": {s: instances[s]["transformation_name"] for s in source_instances},
        "targets": target_instances,
        "transformations": {
            k: {"type": v["type"], "attributes": v["attributes"],
                "router_groups": v["groups"],
                "expression_evaluation_order": list(v["fields"]),
                "expressions": {fn: fi["expression"] for fn, fi in sorted(v["fields"].items())
                                if fi["expression"] and fi["expression"] != fn}}
            for k, v in used.items()},
        "target_lineage": lineage,
        "physical_target_instances": {k: sorted(v) for k, v in sorted(physical.items())},
        "target_instance_attributes": {t: instances[t]["attributes"]
                                       for t in target_instances if instances[t]["attributes"]},
        "target_load_order": [attrs_of(e) for e in m.findall("TARGETLOADORDER")],
        "lookup_details": lookup_details,
        "unconnected_lkp_calls": unconnected,
        "sql_overrides": sql_overrides,
        "source_qualifiers": sqs,
        "aggregator_groupby_ports": agg_groupby,
        "joiners": joiners, "sorters": sorters, "normalizers": normalizers,
        "sequence_generators": sequences, "update_strategies": upd,
        "mapplet_expansions": expansions,
        "mapping_variables": [attrs_of(v) for v in m.findall("MAPPINGVARIABLE")],
        "unpopulated_target_columns": {
            t: [c["column"] for c in info["columns"] if not c["chain"]]
            for t, info in lineage.items()},
    }


def topo_order(nodes, links):
    indeg = {n: 0 for n in nodes}
    nxt = {n: [] for n in nodes}
    for lk in links:
        if lk["from"] in nxt and lk["to"] in indeg:
            nxt[lk["from"]].append(lk["to"])
            indeg[lk["to"]] += 1
    ready = sorted(n for n, d in indeg.items() if d == 0)
    order = []
    while ready:
        cur = ready.pop(0)
        order.append(cur)
        for n in sorted(nxt[cur]):
            indeg[n] -= 1
            if indeg[n] == 0:
                ready.append(n)
        ready.sort()
    return order + sorted(n for n in nodes if n not in order)


def command_task(task, scope, component=None):
    pairs = task.findall("VALUEPAIR")
    return {"name": task.get("NAME"), "scope": scope, "component": component,
            "attributes": {a.get("NAME"): a.get("VALUE") for a in task.findall("ATTRIBUTE")},
            "commands": [{"order": v.get("EXECORDER"), "name": v.get("NAME"),
                          "value": v.get("VALUE")} for v in pairs]}


def parse_workflow(wf):
    tis = [{"name": t.get("NAME"), "task_name": t.get("TASKNAME"),
            "task_type": t.get("TASKTYPE"), "enabled": t.get("ISENABLED"),
            "fail_parent_if_fails": t.get("FAIL_PARENT_IF_INSTANCE_FAILS"),
            "treat_input_links_as_and": t.get("TREAT_INPUTLINK_AS_AND")}
           for t in wf.findall("TASKINSTANCE")]
    links = [{"from": l.get("FROMTASK"), "to": l.get("TOTASK"),
              "condition": l.get("CONDITION") or ""} for l in wf.findall("WORKFLOWLINK")]
    order = topo_order([t["name"] for t in tis], links)
    ti_by = {t["name"]: t for t in tis}
    sessions, commands, emails = {}, [], []
    for t in wf.findall("TASK"):
        if t.get("TYPE") == "Command":
            commands.append(command_task(t, "workflow"))
        elif t.get("TYPE") == "Email":
            emails.append({"name": t.get("NAME"), "scope": "workflow"})
    for s in wf.findall("SESSION"):
        comps = []
        for c in s.findall("SESSIONCOMPONENT"):
            task = c.find("TASK")
            ctype = c.get("TYPE")
            if task is not None and task.get("TYPE") == "Email":
                emails.append({"name": task.get("NAME"), "scope": s.get("NAME"),
                               "component": ctype})
                continue
            vals = [{"order": v.get("EXECORDER"), "name": v.get("NAME"),
                     "value": v.get("VALUE")} for v in c.findall("VALUEPAIR")]
            comps.append({"type": ctype, "task": c.get("REFOBJECTNAME"), "values": vals})
            if task is not None and task.get("TYPE") == "Command":
                ct = command_task(task, s.get("NAME"), ctype)
                ct["commands"] = ct["commands"] or vals
                commands.append(ct)
        exts = []
        for e in s.findall("SESSIONEXTENSION"):
            cref = e.find("CONNECTIONREFERENCE")
            exts.append({"instance": e.get("SINSTANCENAME"), "kind": e.get("TYPE"),
                         "subtype": e.get("SUBTYPE"),
                         "connection_type": cref.get("CONNECTIONTYPE") if cref is not None else None,
                         "connection_subtype": cref.get("CONNECTIONSUBTYPE") if cref is not None else None,
                         "attributes": {a.get("NAME"): a.get("VALUE")
                                        for a in e.findall("ATTRIBUTE")
                                        if a.get("NAME") in SESSION_EXT_ATTRS and a.get("VALUE")}})
        overrides = {}
        for sti in s.findall("SESSTRANSFORMATIONINST"):
            at = {a.get("NAME"): a.get("VALUE") for a in sti.findall("ATTRIBUTE")
                  if a.get("VALUE") and a.get("NAME") != "Connection Information"}
            if at:
                overrides[sti.get("SINSTANCENAME")] = at
        sessions[s.get("NAME")] = {
            "name": s.get("NAME"), "mapping": s.get("MAPPINGNAME"),
            "attributes": {a.get("NAME"): a.get("VALUE") for a in s.findall("ATTRIBUTE")
                           if a.get("NAME") in ("Treat source rows as", "Commit Type",
                                                "Commit Interval", "Parameter Filename",
                                                "Pushdown Optimization")},
            "components": comps, "readers_writers": exts,
            "transformation_overrides": overrides}
    session_order = [ti_by[n]["task_name"] for n in order
                     if ti_by[n]["task_type"] == "Session" and ti_by[n]["task_name"] in sessions]
    session_order += sorted(n for n in sessions if n not in session_order)
    return {
        "name": wf.get("NAME"),
        "attributes": {a.get("NAME"): a.get("VALUE") for a in wf.findall("ATTRIBUTE")
                       if a.get("NAME") in ("Parameter Filename", "Workflow Log File Name")},
        "task_instances": tis, "links": links, "execution_order": order,
        "session_order": session_order,
        "sessions": [sessions[n] for n in session_order],
        "command_tasks": commands, "email_tasks": emails,
        "user_variables": [attrs_of(v) for v in wf.findall("WORKFLOWVARIABLE")
                           if v.get("USERDEFINED") == "YES"],
    }


def folder_owners(path):
    return [f.get("OWNER") for f in ET.parse(path).getroot().iter("FOLDER")]


def parse_file(path, owners=()):
    root = ET.parse(path).getroot()
    folder = root.find(".//FOLDER")
    red = Redactor(list(owners) + folder_owners(path))
    sources = {}
    for s in folder.findall("SOURCE"):
        sources[s.get("NAME")] = {
            "database_type": s.get("DATABASETYPE"), "dbd_name": s.get("DBDNAME"),
            "owner_name": s.get("OWNERNAME"),
            "flatfile": attrs_of(s.find("FLATFILE")) if s.find("FLATFILE") is not None else None,
            "fields": parse_fields(s.findall("SOURCEFIELD"))}
    targets = {}
    for t in folder.findall("TARGET"):
        targets[t.get("NAME")] = {
            "database_type": t.get("DATABASETYPE"),
            "groups": [attrs_of(g) for g in t.findall("GROUP")],
            "pwx_metadata": {m.get("NAME"): m.get("VALUE")
                             for m in t.findall("METADATAEXTENSION")},
            "fields": parse_fields(t.findall("TARGETFIELD"))}
    folder_transforms = {t.get("NAME"): parse_transformation(t)
                         for t in folder.findall("TRANSFORMATION")}
    mapplets = {m.get("NAME"): m for m in folder.findall("MAPPLET")}
    mappings = {m.get("NAME"): parse_mapping(m, folder_transforms, mapplets, sources, targets)
                for m in folder.findall("MAPPING")}
    workflows = [parse_workflow(w) for w in folder.findall("WORKFLOW")]
    order = [s["mapping"] for w in workflows for s in w["sessions"] if s["mapping"] in mappings]
    order = list(dict.fromkeys(order)) + sorted(m for m in mappings if m not in order)
    for w in workflows:
        for pos, s in enumerate(w["sessions"], 1):
            if s["mapping"] in mappings:
                mappings[s["mapping"]].setdefault("sessions", []).append(
                    {"workflow": w["name"], "session": s["name"], "position": pos})
    by_type = {}
    for t in root.iter("TRANSFORMATION"):
        by_type[t.get("TYPE")] = by_type.get(t.get("TYPE"), 0) + 1
    counts = {"MAPPING": len(folder.findall("MAPPING")),
              "SESSION": len(list(folder.iter("SESSION"))),
              "SOURCE": len(folder.findall("SOURCE")),
              "TARGET": len(folder.findall("TARGET")),
              "MAPPLET": len(mapplets), "WORKFLOW": len(workflows),
              "TRANSFORMATION": sum(by_type.values())}
    g_counts, g_types = grep_counts(path)
    stm = {
        "repository_file": os.path.relpath(path, REPO_ROOT).replace(os.sep, "/"),
        "folder": folder.get("NAME"),
        "counts": counts, "transformations_by_type": dict(sorted(by_type.items())),
        "grep_counts": g_counts, "grep_transformations_by_type": g_types,
        "counts_match": counts == g_counts and dict(sorted(by_type.items())) == g_types,
        "sources": sources, "targets": targets,
        "mapplets": sorted(mapplets),
        "workflows": workflows,
        "mapping_order": order,
        "mappings": [mappings[m] for m in order],
    }
    stm = red.walk(stm)
    return stm, red.hits


def md_cell(v):
    return " ".join(str(v).split()).replace("|", "\\|")


def write_md(stm, path):
    c = stm["counts"]
    lines = [f"# PowerCenter STM: `{stm['folder']}`", "",
             f"Derived deterministically from `{stm['repository_file']}` by "
             "`tools/ts_lineage.py`. Personal identifiers are redacted as "
             "`<owner>`, `<path>`, `<email>`.", "",
             "| Mappings | Sessions | Sources | Targets | Transformations | Mapplets |",
             "|---|---|---|---|---|---|",
             f"| {c['MAPPING']} | {c['SESSION']} | {c['SOURCE']} | {c['TARGET']} | "
             f"{c['TRANSFORMATION']} | {c['MAPPLET']} |", "",
             "Transformations by type: " + ", ".join(
                 f"{k} {v}" for k, v in stm["transformations_by_type"].items()), ""]
    for w in stm["workflows"]:
        lines += [f"## Workflow `{w['name']}`", "", "Session order:", ""]
        for i, s in enumerate(w["sessions"], 1):
            lines.append(f"{i}. `{s['name']}` → mapping `{s['mapping']}`")
        lines += ["", "| From | To | Condition |", "|---|---|---|"]
        for lk in w["links"]:
            lines.append(f"| {lk['from']} | {lk['to']} | {md_cell(lk['condition']) or '—'} |")
        lines.append("")
        cmds = [ct for ct in w["command_tasks"] if ct["commands"]]
        if cmds:
            lines += ["Command tasks:", ""]
            for ct in cmds:
                lines.append(f"- `{ct['scope']}` / {ct['component'] or 'task'} `{ct['name']}`: " +
                             "; ".join(f"`{md_cell(x['name'])}` = `{md_cell(x['value'])}`"
                                       for x in ct["commands"]))
            lines.append("")
        for s in w["sessions"]:
            rw = [x for x in s["readers_writers"] if x["attributes"]]
            if rw or s["transformation_overrides"]:
                lines.append(f"- Session `{s['name']}`: " + "; ".join(
                    f"{x['kind']} `{x['instance']}` " + ", ".join(
                        f"{k}=`{md_cell(v)}`" for k, v in sorted(x["attributes"].items()))
                    for x in rw))
        lines.append("")
    lines += ["## Source definitions", "", "| Source | Database type | Fields |", "|---|---|---|"]
    for n, s in sorted(stm["sources"].items()):
        lines.append(f"| {n} | {s['database_type']} | {len(s['fields'])} |")
    lines += ["", "## Target definitions", "", "| Target | Database type | Fields |", "|---|---|---|"]
    for n, t in sorted(stm["targets"].items()):
        lines.append(f"| {n} | {t['database_type']} | {len(t['fields'])} |")
    lines.append("")
    for m in stm["mappings"]:
        sess = ", ".join(f"`{s['session']}` (#{s['position']})" for s in m.get("sessions", []))
        lines += [f"## Mapping `{m['name']}`", "", f"- Sessions: {sess or '(none)'}",
                  f"- Sources: {', '.join('`%s`' % s for s in m['sources'])}",
                  f"- Target instances: {', '.join('`%s`' % t for t in m['targets'])}", ""]
        for e in m["mapplet_expansions"]:
            lines.append(f"- Mapplet `{e['mapplet']}` expanded inline as `{e['instance']}/…`")
        for tname, ti in m["transformations"].items():
            groups = [g for g in ti["router_groups"] if g["type"] != "INPUT"]
            if not ti["attributes"] and not groups:
                continue
            lines.append(f"### Transformation `{tname}` ({ti['type']})")
            lines.append("")
            for k, v in ti["attributes"].items():
                lines.append(f"- **{k}**: `{md_cell(v)}`")
            for g in groups:
                lines.append(f"- Router group `{g['name']}`: `{md_cell(g['expression'] or '(default group)')}`")
            lines.append("")
        for t, at in m["target_instance_attributes"].items():
            lines.append(f"- Target instance `{t}`: " + ", ".join(
                f"{k}=`{md_cell(v)}`" for k, v in sorted(at.items())))
        for j in m["joiners"]:
            lines.append(f"- Joiner `{j['transformation']}`: {j['join_type']} ON "
                         f"`{md_cell(j['condition'])}`")
        for s in m["sorters"]:
            lines.append(f"- Sorter `{s['transformation']}` keys: " + ", ".join(
                f"{k['port']} {k['direction']}" for k in s["keys"]) +
                f"; distinct={s['distinct']}")
        for n in m["normalizers"]:
            lines.append(f"- Normalizer `{n['transformation']}` (vsam={n['vsam']}"
                         f"{', source ' + n['ref_source'] if n['ref_source'] else ''}) occurs: " +
                         (", ".join(f"{k}×{v}" for k, v in n["occurs"].items()) or "—") +
                         f"; generated: {', '.join(n['generated_ports']) or '—'}")
        for s in m["sequence_generators"]:
            lines.append(f"- Sequence `{s['transformation']}`: start={s['start_value']} "
                         f"current={s['current_value']} increment={s['increment_by']} "
                         f"cycle={s['cycle']} reset={s['reset']} → {', '.join(s['targets'])}")
        for u in m["update_strategies"]:
            lines.append(f"- Update Strategy `{u['transformation']}`: "
                         f"`{md_cell(u['expression'])}` → {', '.join(u['targets'])}")
        for lk in m["lookup_details"]:
            lines.append(f"- Lookup `{lk['transformation']}`: table `{lk['table']}` "
                         f"(exists in export: **{lk['exists_in_export']}**), condition "
                         f"`{md_cell(lk['condition'])}`, multiple-match policy "
                         f"`{lk['multiple_match_policy']}`.")
        for o in m["sql_overrides"]:
            lines.append(f"- SQL override `{o['transformation']}` positional bindings: " +
                         "; ".join(f"{b['position']} → `{b['port']}` = `{md_cell(b['expression'])}`"
                                   for b in o["positional_bindings"]))
        for call in m["unconnected_lkp_calls"]:
            lines.append(f"- Unconnected lookup call `{call['transformation']}.{call['port']}`: "
                         f"`{md_cell(call['expression'])}`.")
        lines.append("")
        for tgt in m["targets"]:
            info = m["target_lineage"][tgt]
            lines += [f"### Target instance `{tgt}` (table `{info['target_table']}`)", "",
                      "| Target | Target Column | Expression / Rule | Source(s) |",
                      "|---|---|---|---|"]
            for col in info["columns"]:
                chain = " → ".join(col["chain"]) if col["chain"] else col["rule"]
                lines.append(f"| {tgt} | {col['column']} | {md_cell(chain)} | "
                             f"{md_cell('; '.join(col['sources'])) or '—'} |")
            lines.append("")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def write_inventory(stms, path):
    keys = ("MAPPING", "SESSION", "SOURCE", "TARGET", "TRANSFORMATION", "MAPPLET")
    lines = ["# PowerCenter inventory (legacy/informatica_ts)", "",
             "Generated by `tools/ts_lineage.py`. Counts are parsed from the XML and "
             "checked against a line count of the raw export (`grep -c '<TAG '`).", "",
             "| Export | Workflow | " + " | ".join(k.title() + "s" for k in keys) +
             " | grep check |", "|---|---|" + "---|" * len(keys) + "---|"]
    total = {k: 0 for k in keys}
    for name, s in stms:
        for k in keys:
            total[k] += s["counts"][k]
        lines.append(f"| {name} | {', '.join(w['name'] for w in s['workflows'])} | " +
                     " | ".join(str(s["counts"][k]) for k in keys) +
                     f" | {'match' if s['counts_match'] else 'MISMATCH'} |")
    lines.append("| **Total** | | " + " | ".join(f"**{total[k]}**" for k in keys) + " | |")
    types = sorted({t for _, s in stms for t in s["transformations_by_type"]})
    lines += ["", "## Transformations by type", "",
              "| Export | " + " | ".join(types) + " |", "|---|" + "---|" * len(types)]
    for name, s in stms:
        lines.append(f"| {name} | " + " | ".join(
            str(s["transformations_by_type"].get(t, 0)) for t in types) + " |")
    for name, s in stms:
        lines += ["", f"## {name}", ""]
        for m in s["mappings"]:
            srcs = ", ".join(
                f"{m['source_tables'][i]} "
                f"({s['sources'].get(m['source_tables'][i], {}).get('database_type', '?')})"
                for i in m["sources"])
            tgts = ", ".join(sorted({
                f"{m['target_lineage'][t]['target_table']} "
                f"({s['targets'].get(m['target_lineage'][t]['target_table'], {}).get('database_type', '?')})"
                for t in m["targets"]}))
            extras = []
            if m["lookup_details"]:
                extras.append("lookups: " + ", ".join(sorted({str(l["table"]) for l in m["lookup_details"]})))
            for q in m["sequence_generators"]:
                extras.append(f"sequence {q['transformation']} start={q['start_value']} current={q['current_value']}")
            for u in m["update_strategies"]:
                extras.append(f"update strategy → {', '.join(u['targets'])}")
            pos = ", ".join(f"#{x['position']}" for x in m.get("sessions", [])) or "—"
            lines.append(f"- {pos} `{m['name']}`: {srcs or '—'} → {tgts or '—'}" +
                         (f" ({'; '.join(extras)})" if extras else ""))
        cmds = [ct for w in s["workflows"] for ct in w["command_tasks"] if ct["commands"]]
        lines.append(f"- Command tasks with commands: {len(cmds)} "
                     f"({sum(len(ct['commands']) for ct in cmds)} commands)")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("inputs", nargs="*", help="export files or directories "
                    f"(default: {os.path.relpath(DEFAULT_INPUT, REPO_ROOT)})")
    ap.add_argument("--out-dir", default=DEFAULT_OUT)
    args = ap.parse_args(argv)
    files = []
    for p in args.inputs or [DEFAULT_INPUT]:
        if os.path.isdir(p):
            files += [os.path.join(p, f) for f in sorted(os.listdir(p))
                      if os.path.isfile(os.path.join(p, f)) and not f.startswith(".")]
        else:
            files.append(p)
    os.makedirs(args.out_dir, exist_ok=True)
    stms, ok = [], True
    owners = sorted({o for f in files for o in folder_owners(f) if o})
    for f in files:
        name = os.path.basename(f)
        stm, hits = parse_file(os.path.abspath(f), owners)
        with open(os.path.join(args.out_dir, name + ".json"), "w", encoding="utf-8") as fh:
            json.dump(stm, fh, indent=2, sort_keys=True, ensure_ascii=False)
            fh.write("\n")
        write_md(stm, os.path.join(args.out_dir, name + ".md"))
        stms.append((name, stm))
        ok &= stm["counts_match"]
        print(f"{name}: " + " ".join(f"{k.lower()}s={v}" for k, v in stm["counts"].items()) +
              f" grep={'match' if stm['counts_match'] else 'MISMATCH'} "
              f"redacted={sum(hits.values())}")
    write_inventory(stms, os.path.join(args.out_dir, "INVENTORY.md"))
    print(f"total mappings={sum(s['counts']['MAPPING'] for _, s in stms)}; "
          f"wrote {len(stms)} STMs + INVENTORY.md to "
          f"{os.path.relpath(args.out_dir, REPO_ROOT)}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
