#!/usr/bin/env python3
"""Deterministic lineage parser for the Informatica PowerCenter export.

Reads legacy/informatica/wf_demo_mapping.XML (stdlib xml.etree only) and emits:
  docs/stm/informatica_stm.json  - machine-readable source-to-target mapping
  docs/stm/informatica_stm.md    - per-mapping tables: Target | Target Column |
                                   Expression / Rule | Source(s)

For every mapping it captures sources, targets, transformations, port-level
lineage via CONNECTOR elements (target column -> expression chain -> source
column), Source Qualifier SQL overrides, lookup tables/conditions, router group
filter conditions, update-strategy logic and sequence-generator configuration.
"""
import json
import os
import re
import xml.etree.ElementTree as ET

XML_PATH = os.path.join("legacy", "informatica", "wf_demo_mapping.XML")
OUT_JSON = os.path.join("docs", "stm", "informatica_stm.json")
OUT_MD = os.path.join("docs", "stm", "informatica_stm.md")

IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


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

# Attributes worth surfacing per transformation type.
INTERESTING_ATTRS = {
    "Source Qualifier": ["Sql Query", "User Defined Join", "Source Filter"],
    "Lookup Procedure": [
        "Lookup table name",
        "Lookup condition",
        "Lookup policy on multiple match",
        "Lookup Sql Override",
        "Lookup Source Filter",
    ],
    "Sequence": ["Start Value", "Increment By", "End Value", "Current Value", "Cycle"],
    "Update Strategy": ["Update Strategy Expression", "Forward Rejected Rows"],
}

def parse(path):
    tree = ET.parse(path)
    root = tree.getroot()
    folder = root.find(".//FOLDER")

    global_sources = {}
    for s in folder.findall("SOURCE"):
        global_sources[s.get("NAME")] = {
            "database_type": s.get("DATABASETYPE"),
            "fields": [
                {"name": f.get("NAME"), "datatype": f.get("DATATYPE"),
                 "precision": f.get("PRECISION"), "scale": f.get("SCALE")}
                for f in s.findall("SOURCEFIELD")
            ],
        }
    global_targets = {}
    for t in folder.findall("TARGET"):
        global_targets[t.get("NAME")] = {
            "fields": [
                {"name": f.get("NAME"), "datatype": f.get("DATATYPE"),
                 "precision": f.get("PRECISION"), "scale": f.get("SCALE"),
                 "key": f.get("KEYTYPE")}
                for f in t.findall("TARGETFIELD")
            ],
        }

    mappings = []
    for m in folder.findall("MAPPING"):
        mappings.append(parse_mapping(m, global_sources, global_targets))
    mappings.sort(key=lambda x: x["name"])
    return {
        "repository_file": XML_PATH,
        "sources": global_sources,
        "targets": global_targets,
        "mappings": mappings,
    }


def parse_mapping(m, global_sources, global_targets):
    name = m.get("NAME")
    transforms = {}
    for t in m.findall("TRANSFORMATION"):
        ttype = t.get("TYPE")
        info = {"name": t.get("NAME"), "type": ttype, "fields": {}, "groups": [],
                "attributes": {}}
        for f in t.findall("TRANSFORMFIELD"):
            info["fields"][f.get("NAME")] = {
                "expression": f.get("EXPRESSION"),
                "porttype": f.get("PORTTYPE"),
                "group": f.get("GROUP"),
                "ref_field": f.get("REF_FIELD"),
                "datatype": f.get("DATATYPE"),
                "expressiontype": f.get("EXPRESSIONTYPE"),
            }
        for g in t.findall("GROUP"):
            info["groups"].append({
                "name": g.get("NAME"), "type": g.get("TYPE"),
                "expression": g.get("EXPRESSION"),
            })
        for a in t.findall("TABLEATTRIBUTE"):
            if a.get("NAME") in INTERESTING_ATTRS.get(ttype, []):
                info["attributes"][a.get("NAME")] = a.get("VALUE")
        transforms[t.get("NAME")] = info

    instances = {}
    for i in m.findall("INSTANCE"):
        instances[i.get("NAME")] = {
            "name": i.get("NAME"),
            "type": i.get("TYPE"),
            "transformation_name": i.get("TRANSFORMATION_NAME"),
            "transformation_type": i.get("TRANSFORMATION_TYPE"),
            "associated_sources": [
                a.get("NAME") for a in i.findall("ASSOCIATED_SOURCE_INSTANCE")
            ],
        }

    connectors = [
        {"from_instance": c.get("FROMINSTANCE"), "from_field": c.get("FROMFIELD"),
         "from_type": c.get("FROMINSTANCETYPE"),
         "to_instance": c.get("TOINSTANCE"), "to_field": c.get("TOFIELD"),
         "to_type": c.get("TOINSTANCETYPE")}
        for c in m.findall("CONNECTOR")
    ]
    # incoming[(instance, field)] -> (from_instance, from_field)
    incoming = {(c["to_instance"], c["to_field"]):
                (c["from_instance"], c["from_field"]) for c in connectors}

    target_instances = sorted(
        i["name"] for i in instances.values() if i["type"] == "TARGET")
    source_instances = sorted(
        i["name"] for i in instances.values() if i["type"] == "SOURCE")

    def transform_of(instance_name):
        inst = instances.get(instance_name)
        if not inst:
            return None
        return transforms.get(inst["transformation_name"])

    def trace(instance_name, field, depth=0):
        """Walk one port upstream, returning (chain_steps, terminal_sources)."""
        if depth > 25:
            return ["... (depth limit)"], []
        inst = instances.get(instance_name)
        if inst is None:
            return [f"{instance_name}.{field}"], []
        if inst["type"] == "SOURCE":
            return [f"{instance_name}.{field}"], [f"{instance_name}.{field}"]
        tr = transform_of(instance_name)
        if tr is None:
            return [f"{instance_name}.{field}"], []
        ttype = tr["type"]
        fld = tr["fields"].get(field, {})
        steps, sources = [], []

        if ttype == "Sequence":
            attrs = tr["attributes"]
            steps.append(
                f"{instance_name}.{field} [sequence start={attrs.get('Start Value')} "
                f"increment={attrs.get('Increment By')} "
                f"current={attrs.get('Current Value')} cycle={attrs.get('Cycle')}]")
            return steps, [f"{instance_name} (generated)"]

        if ttype == "Router" and fld.get("ref_field"):
            grp = fld.get("group")
            gexpr = next((g["expression"] for g in tr["groups"]
                          if g["name"] == grp), None)
            cond = f" WHERE {gexpr}" if gexpr else " (DEFAULT group)"
            steps.append(f"{instance_name}.{field} [router group {grp}{cond}]")
            up = incoming.get((instance_name, fld["ref_field"]))
            if up:
                s2, src2 = trace(up[0], up[1], depth + 1)
                steps += s2
                sources += src2
            return steps, sources

        if ttype == "Lookup Procedure" and fld.get("porttype", "").startswith("LOOKUP"):
            attrs = tr["attributes"]
            steps.append(
                f"{instance_name}.{field} [lookup {attrs.get('Lookup table name')}."
                f"{field} ON {attrs.get('Lookup condition')}]")
            sources.append(f"{attrs.get('Lookup table name')}.{field} (lookup)")
            # trace the lookup input port(s)
            for pname, pinfo in tr["fields"].items():
                if "INPUT" in (pinfo.get("porttype") or ""):
                    up = incoming.get((instance_name, pname))
                    if up:
                        _, src2 = trace(up[0], up[1], depth + 1)
                        sources += [f"{s} (lookup key)" for s in src2]
            return steps, sources

        expr = fld.get("expression")
        if expr and expr != field:
            steps.append(f"{instance_name}.{field} = {expr}")
            refs = [tok for tok in dict.fromkeys(IDENT_RE.findall(expr))
                    if tok in tr["fields"] and tok != field]
            for ref in refs:
                up = incoming.get((instance_name, ref))
                if up:
                    s2, src2 = trace(up[0], up[1], depth + 1)
                    steps += s2
                    sources += src2
            if not refs:
                sources.append(f"literal/expression: {expr}")
            return steps, sources

        # pass-through port
        steps.append(f"{instance_name}.{field}")
        up = incoming.get((instance_name, field))
        if up:
            s2, src2 = trace(up[0], up[1], depth + 1)
            steps += s2
            sources += src2
        return steps, sources

    lineage = {}
    for tgt in target_instances:
        tgt_def = instances[tgt]["transformation_name"]
        cols = []
        for f in global_targets.get(tgt_def, {}).get("fields", []):
            col = f["name"]
            up = incoming.get((tgt, col))
            if up is None:
                cols.append({"column": col, "rule": "(not connected — NULL)",
                             "chain": [], "sources": []})
                continue
            steps, sources = trace(up[0], up[1])
            rule = steps[0] if steps else ""
            cols.append({"column": col, "rule": rule, "chain": steps,
                         "sources": sorted(dict.fromkeys(sources))})
        lineage[tgt] = {"target_table": tgt_def, "columns": cols}

    physical_targets = {}
    for instance in target_instances:
        table = instances[instance]["transformation_name"]
        physical_targets.setdefault(table, []).append(instance)
    for table in physical_targets:
        physical_targets[table].sort()
    lookup_details = []
    for tname, tinfo in sorted(transforms.items()):
        if tinfo["type"] != "Lookup Procedure":
            continue
        table = tinfo["attributes"].get("Lookup table name")
        lookup_details.append({
            "transformation": tname,
            "table": table,
            "exists_in_export": table in global_sources or table in global_targets,
            "condition": tinfo["attributes"].get("Lookup condition"),
            "multiple_match_policy":
                tinfo["attributes"].get("Lookup policy on multiple match"),
            "ports": sorted(tinfo["fields"]),
        })
    sql_overrides = []
    for tname, tinfo in sorted(transforms.items()):
        sql = tinfo["attributes"].get("Sql Query", "")
        if not sql:
            continue
        select_match = re.search(r"\bSELECT\s+(.*?)\s+\bFROM\b", sql,
                                 flags=re.I | re.S)
        if not select_match:
            continue
        expressions = split_select_list(select_match.group(1))
        ports = [n for n, f in tinfo["fields"].items()
                 if f.get("porttype") in ("INPUT/OUTPUT", "OUTPUT")]
        sql_overrides.append({
            "transformation": tname,
            "sql": sql,
            "positional_bindings": [
                {"position": i + 1, "expression": expr,
                 "port": ports[i] if i < len(ports) else None}
                for i, expr in enumerate(expressions)
            ],
        })
    unconnected_lkp_calls = []
    for tname, tinfo in sorted(transforms.items()):
        for port, expr in sorted(
                (n, f.get("expression")) for n, f in tinfo["fields"].items()):
            if expr and ":LKP." in expr:
                unconnected_lkp_calls.append({
                    "transformation": tname, "port": port, "expression": expr,
                })
    aggregator_groupby = {}
    for tname, tinfo in sorted(transforms.items()):
        if tinfo["type"] == "Aggregator":
            aggregator_groupby[tname] = [
                n for n, f in tinfo["fields"].items()
                if f.get("expression") and f.get("expressiontype") == "GROUPBY"
            ]
    return {
        "name": name,
        "sources": source_instances,
        "targets": target_instances,
        "transformations": {
            k: {"type": v["type"], "attributes": v["attributes"],
                "router_groups": v["groups"],
                "expression_evaluation_order": list(v["fields"]),
                "expressions": {fn: fi["expression"]
                                for fn, fi in sorted(v["fields"].items())
                                if fi["expression"] and fi["expression"] != fn}}
            for k, v in sorted(transforms.items())
        },
        "target_lineage": lineage,
        "physical_target_instances": physical_targets,
        "lookup_details": lookup_details,
        "unconnected_lkp_calls": unconnected_lkp_calls,
        "sql_overrides": sql_overrides,
        "aggregator_groupby_ports": aggregator_groupby,
        "unpopulated_target_columns": {
            tgt: [c["column"] for c in info["columns"] if not c["chain"]]
            for tgt, info in lineage.items()
        },
    }


def write_md(stm, path):
    lines = ["# Informatica Source-to-Target Mapping (STM)", "",
             f"Derived deterministically from `{stm['repository_file']}` by "
             "`tools/informatica_lineage.py`.", "",
             "Business/run date is pinned to **2024-01-31** for all SYSDATE / "
             "SYSTIMESTAMP references.", ""]
    for m in stm["mappings"]:
        lines += [f"## Mapping `{m['name']}`", "",
                  f"- Sources: {', '.join('`%s`' % s for s in m['sources'])}",
                  f"- Target instances: {', '.join('`%s`' % t for t in m['targets'])}",
                  ""]
        if m["physical_target_instances"]:
            lines.append("Physical target instance groups: " + "; ".join(
                f"`{table}` = {', '.join(instances)}"
                for table, instances in m["physical_target_instances"].items()))
            lines.append("")
        for tname, tinfo in sorted(m["transformations"].items()):
            attrs = tinfo["attributes"]
            groups = [g for g in tinfo["router_groups"] if g["type"] != "INPUT"]
            if (not attrs and not groups and
                    not (tinfo["type"] == "Aggregator")):
                continue
            lines.append(f"### Transformation `{tname}` ({tinfo['type']})")
            lines.append("")
            for k, v in attrs.items():
                if v:
                    v_clean = " ".join(str(v).split())
                    lines.append(f"- **{k}**: `{v_clean}`")
            for g in groups:
                cond = g["expression"] or "(default group)"
                lines.append(f"- Router group `{g['name']}`: `{cond}`")
            if tinfo["type"] == "Aggregator":
                lines.append("- GROUPBY ports: " +
                             (", ".join(m["aggregator_groupby_ports"].get(tname, []))
                              or "(none)"))
            lines.append("")
        for lookup in m["lookup_details"]:
            lines.append(
                f"- Lookup `{lookup['transformation']}`: table "
                f"`{lookup['table']}` (exists in export: "
                f"**{lookup['exists_in_export']}**), condition "
                f"`{lookup['condition']}`, multiple-match policy "
                f"`{lookup['multiple_match_policy']}`.")
        for override in m["sql_overrides"]:
            lines.append(f"- SQL override `{override['transformation']}` positional "
                         "bindings: " + "; ".join(
                             f"{b['position']} → `{b['port']}` = `{b['expression']}`"
                             for b in override["positional_bindings"]))
        for call in m["unconnected_lkp_calls"]:
            lines.append(f"- Unconnected lookup call `{call['transformation']}."
                         f"{call['port']}`: `{call['expression']}`.")
        if m["unpopulated_target_columns"]:
            lines.append("- Target columns with no connector: " + "; ".join(
                f"`{t}`: {', '.join(cols) or '(none)'}"
                for t, cols in m["unpopulated_target_columns"].items()))
            lines.append("")
        for tgt in m["targets"]:
            info = m["target_lineage"][tgt]
            lines += [f"### Target instance `{tgt}` (table `{info['target_table']}`)",
                      "",
                      "| Target | Target Column | Expression / Rule | Source(s) |",
                      "|---|---|---|---|"]
            for c in info["columns"]:
                chain = " → ".join(c["chain"]) if c["chain"] else c["rule"]
                chain = chain.replace("|", "\\|")
                srcs = "; ".join(c["sources"]).replace("|", "\\|") or "—"
                lines.append(f"| {tgt} | {c['column']} | {chain} | {srcs} |")
            lines.append("")
    with open(path, "w") as fh:
        fh.write("\n".join(lines) + "\n")


def main():
    stm = parse(XML_PATH)
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w") as fh:
        json.dump(stm, fh, indent=2, sort_keys=True)
        fh.write("\n")
    write_md(stm, OUT_MD)
    print(f"wrote {OUT_JSON} and {OUT_MD}")


if __name__ == "__main__":
    main()
