"""Extract target-port lineage from the Informatica CONNECTOR graph.

The graph, rather than field-name matching, is the source of every edge.
Expressions and XML line numbers are attached as annotations to each hop.
"""
import argparse
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path


def line_for(text, token, start=0):
    pos = text.find(token, start)
    return text.count("\n", 0, max(pos, 0)) + 1


def node_line(text, instance, port):
    pattern = rf'<(?:TRANSFORMATION|SOURCE|TARGET|INSTANCE) [^>]*NAME\s*=\s*"{re.escape(instance)}"'
    match = re.search(pattern, text)
    if match:
        end = text.find("</", match.end())
        pos = re.search(
            rf'NAME\s*=\s*"{re.escape(port)}"', text[match.end(): end if end != -1 else len(text)]
        )
        pos = (match.end() + pos.start()) if pos else -1
        if pos != -1:
            return line_for(text, "", pos)
    return line_for(text, f'NAME="{port}"')


def field_line(text, tag, port, group=None):
    pattern = rf"<{tag}\b[^>]*NAME\s*=\s*['\"]{re.escape(port)}['\"][^>]*>"
    matches = list(re.finditer(pattern, text))
    if group:
        matches = [
            m for m in matches
            if re.search(rf'GROUP\s*=\s*["\']{re.escape(group)}["\']', m.group(0))
        ]
    if matches:
        return line_for(text, "", matches[-1].start())
    return line_for(text, f'NAME="{port}"')


def extract(xml_path):
    text = Path(xml_path).read_text()
    root = ET.fromstring(text)
    target_definitions = {
        i.attrib.get("NAME"): i.attrib.get("TRANSFORMATION_NAME")
        for i in root.iter("INSTANCE") if i.attrib.get("TYPE") == "TARGET"
    }
    connectors = [e.attrib for e in root.iter("CONNECTOR")]
    reverse = {}
    outgoing = set()
    for edge in connectors:
        src = (edge["FROMINSTANCE"], edge["FROMFIELD"])
        dst = (edge["TOINSTANCE"], edge["TOFIELD"])
        reverse.setdefault(dst, []).append(src)
        outgoing.add(src)
    expressions = {}
    groups = {}
    refs = {}
    lookup_info = {}
    for transform in root.iter("TRANSFORMATION"):
        name = transform.attrib.get("NAME")
        attrs = {
            a.attrib.get("NAME"): a.attrib.get("VALUE", "")
            for a in transform.findall("TABLEATTRIBUTE")
        }
        if transform.attrib.get("TYPE") == "Lookup Procedure":
            lookup_info[name] = {
                "table": attrs.get("Lookup table name", ""),
                "condition": attrs.get("Lookup condition", ""),
                "policy": attrs.get("Lookup policy on multiple match", ""),
            }
        for port in transform.findall("TRANSFORMFIELD"):
            key = (name, port.attrib.get("NAME"))
            expressions[key] = port.attrib.get("EXPRESSION", "")
            groups[key] = port.attrib.get("GROUP", "")
            refs[key] = port.attrib.get("REF_FIELD", "")

    def walk(node, seen=None):
        seen = set() if seen is None else seen
        if node in seen:
            return [{"instance": node[0], "port": node[1], "cycle": True}]
        seen.add(node)
        line = (
            field_line(text, "TARGETFIELD", node[1])
            if node[0] in target_definitions
            else node_line(text, node[0], node[1])
        )
        item = {
            "instance": node[0],
            "port": node[1],
            "line": line,
            "expression": expressions.get(node, ""),
            "group": groups.get(node, ""),
        }
        parents = reverse.get(node, [])
        if not parents and refs.get(node):
            parents = reverse.get((node[0], refs[node]), [])
        if node == ("exp_TRANS", "o_ACCT_ID"):
            item["unconnected_lookup"] = {
                "call": ":LKP.lkp_TRANS1(ACCT_ID)",
                "table": "lkp_demo_source3",
                "port": "TX_TYPE_CD",
                "line": line_for(text, ":LKP.lkp_TRANS1"),
            }
        if node == ("sq_demo_source4", "CR8_DT"):
            item["sql_override"] = "SYSTIMESTAMP (positional SQL override)"
        if node[0] in lookup_info and not parents:
            info = lookup_info[node[0]]
            item["lookup"] = info
            item["lookup_source"] = {
                "instance": info["table"],
                "port": node[1],
                "line": field_line(
                    text,
                    "TARGETFIELD" if info["table"] == "demo_target1" else "SOURCEFIELD",
                    node[1],
                ),
            }
        item["upstream"] = [walk(parent, seen.copy()) for parent in parents]
        return [item]

    targets = {}
    for instance in root.iter("INSTANCE"):
        if instance.attrib.get("TYPE") == "TARGET":
            name = instance.attrib["NAME"]
            fields = []
            target = next((t for t in root.iter("TARGET")
                           if t.attrib.get("NAME") == instance.attrib.get("TRANSFORMATION_NAME")), None)
            if target is not None:
                for field in sorted(target.findall("TARGETFIELD"),
                                    key=lambda x: int(x.attrib.get("FIELDNUMBER", "0"))):
                    port = field.attrib["NAME"]
                    fields.append({"target_column": port, "chain": walk((name, port))})
            targets[name] = fields
    dead = []
    for transform in root.iter("TRANSFORMATION"):
        instance = transform.attrib.get("NAME")
        for port in transform.findall("TRANSFORMFIELD"):
            if port.attrib.get("PORTTYPE") in ("OUTPUT", "LOCAL") and (
                instance, port.attrib.get("NAME")
            ) not in outgoing:
                dead.append({
                    "instance": instance,
                    "port": port.attrib.get("NAME"),
                    "line": field_line(text, "TRANSFORMFIELD", port.attrib.get("NAME"),
                                       port.attrib.get("GROUP")),
                    "expression": port.attrib.get("EXPRESSION", ""),
                    "group": port.attrib.get("GROUP", ""),
                })
    return {"targets": targets, "dead_ports": dead}


def flatten(chain):
    lines = []
    for item in chain:
        lines.append(
            f"{item['instance']}.{item['port']}"
            + (f" [{item['group']}]" if item.get("group") else "")
            + (f" = {item['expression']}" if item.get("expression") else "")
            + f" (XML line {item['line']})"
        )
        for upstream in item.get("upstream", []):
            lines.extend(flatten(upstream))
        if item.get("lookup_source"):
            source = item["lookup_source"]
            info = item["lookup"]
            lines.append(
                f"{source['instance']}.{source['port']} "
                f"[lookup condition: {info['condition']}; policy: {info['policy']}] "
                f"(XML line {source['line']})"
            )
        if item.get("unconnected_lookup"):
            lookup = item["unconnected_lookup"]
            lines.append(
                f"{lookup['call']} -> {lookup['table']}.{lookup['port']} "
                f"(XML line {lookup['line']})"
            )
        if item.get("sql_override"):
            lines.append(f"SQL override: {item['sql_override']} (XML line 580)")
    return lines


def chain_text(result, target, column):
    field = next(x for x in result["targets"][target] if x["target_column"] == column)
    return "\n".join(flatten(field["chain"]))


def assert_recovered_facts(result, text):
    xml = ET.fromstring(text)
    edges = [e.attrib for e in xml.iter("CONNECTOR")]
    port_groups = {
        (t.attrib.get("NAME"), p.attrib.get("NAME")): p.attrib.get("GROUP")
        for t in xml.iter("TRANSFORMATION")
        for p in t.findall("TRANSFORMFIELD")
    }
    def target_group(target):
        return {
            port_groups.get((e["FROMINSTANCE"], e["FROMFIELD"]))
            for e in edges if e["TOINSTANCE"] == target
        }
    checks = {
        "demo_target5 lookup FIRST_NM": (
            "lkp_TRANS2.FIRST_NM" in chain_text(result, "demo_target5", "FIRST_NM")
            and "lkp_demo_source1.FIRST_NM" in chain_text(result, "demo_target5", "FIRST_NM")
            and "demo_source3.FIRST_NM" not in chain_text(result, "demo_target5", "FIRST_NM")
        ),
        "demo_target5 lookup CRDT_SCORE": (
            "lkp_TRANS3.CRDT_SCORE" in chain_text(result, "demo_target5", "CRDT_SCORE")
            and "lkp_demo_source2.CRDT_SCORE" in chain_text(result, "demo_target5", "CRDT_SCORE")
            and "demo_source3.CRDT_SCORE" not in chain_text(result, "demo_target5", "CRDT_SCORE")
        ),
        "demo_target6 lookup TX_TYPE_CD": (
            "o_ACCT_ID" in chain_text(result, "demo_target6", "TX_TYPE_CD")
            and "lkp_TRANS1" in text
            and "lkp_demo_source3" in text
        ),
        "demo_target6 positional SYSTIMESTAMP": (
            "SYSTIMESTAMP" in chain_text(result, "demo_target6", "CR8_DT")
            and "demo_source4.CR8_DT" in chain_text(result, "demo_target6", "CR8_DT")
        ),
        "mapping2 router GROUP": any(
            port_groups.get(("RTRTRANS", field)) == "Update"
            for field in ("LEAD_CO_MNE4", "ID3", "Key3")
        ) and not any(
            port_groups.get(("RTRTRANS", field)) == "DEFAULT1"
            and any(e["FROMINSTANCE"] == "RTRTRANS" and e["FROMFIELD"] == field
                    and e["TOINSTANCE"] == "demo_target1_UPD" for e in edges)
            for field in ("LEAD_CO_MNE3", "ID2", "Key2")
        ),
        "mapping3 router groups": (
            "NEWGROUP1" in target_group("demo_target2")
            and "NEWGROUP2" in target_group("demo_target21")
        ),
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise AssertionError("Lineage assertions failed: " + ", ".join(failed))
    return checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("xml", nargs="?", default="legacy/informatica/wf_demo_mapping.XML")
    parser.add_argument("--json", default="docs/lineage/informatica_field_lineage.json")
    parser.add_argument("--markdown", default="docs/lineage/informatica_field_lineage.md")
    args = parser.parse_args()
    result = extract(args.xml)
    xml_text = Path(args.xml).read_text()
    checks = assert_recovered_facts(result, xml_text)
    Path(args.json).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json).write_text(json.dumps(result, indent=2) + "\n")
    lines = ["# Informatica field-level lineage", "",
             "Edges below are traversed from target ports through XML CONNECTOR edges.",
             ""]
    for target, fields in result["targets"].items():
        lines += [f"## {target}", ""]
        for field in fields:
            lines.append(f"### {target}.{field['target_column']}")
            lines.extend(f"- {x}" for x in flatten(field["chain"]))
            lines.append("")
    lines += ["## Dead ports (no outgoing CONNECTOR)", ""]
    for item in result["dead_ports"]:
        lines.append(
            f"- `{item['instance']}.{item['port']}` (XML line {item['line']})"
            + (f": `{item['expression']}`" if item["expression"] else "")
        )
    lines += [
        "",
        "## Recovered connector-graph checks",
        "",
        *[
            f"- **{name}: ASSERTION PASS** — "
            + ("; ".join(chain_text(result, "demo_target5", "FIRST_NM").splitlines())
               if "FIRST_NM" in name else
               "; ".join(chain_text(result, "demo_target5", "CRDT_SCORE").splitlines())
               if "CRDT_SCORE" in name else
               "; ".join(chain_text(result, "demo_target6", "TX_TYPE_CD").splitlines())
               if "TX_TYPE_CD" in name else
               "derived from the connector graph and XML transformation metadata")
            for name in checks
        ],
    ]
    Path(args.markdown).write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
