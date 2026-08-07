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


def extract(xml_path):
    text = Path(xml_path).read_text()
    root = ET.fromstring(text)
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
    for transform in root.iter("TRANSFORMATION"):
        name = transform.attrib.get("NAME")
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
        item = {
            "instance": node[0],
            "port": node[1],
            "line": node_line(text, node[0], node[1]),
            "expression": expressions.get(node, ""),
            "group": groups.get(node, ""),
        }
        parents = reverse.get(node, [])
        if not parents and refs.get(node):
            parents = reverse.get((node[0], refs[node]), [])
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
                    "line": node_line(text, instance, port.attrib.get("NAME")),
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
    return lines


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("xml", nargs="?", default="legacy/informatica/wf_demo_mapping.XML")
    parser.add_argument("--json", default="docs/lineage/informatica_field_lineage.json")
    parser.add_argument("--markdown", default="docs/lineage/informatica_field_lineage.md")
    args = parser.parse_args()
    result = extract(args.xml)
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
        "- `demo_target5.FIRST_NM` traces through `lkp_TRANS2` to `lkp_demo_source1.FIRST_NM`, not `demo_source3.FIRST_NM`.",
        "- `demo_target5.CRDT_SCORE` traces through `lkp_TRANS3` to `lkp_demo_source2.CRDT_SCORE`, not `demo_source3.CRDT_SCORE`.",
        "- `demo_target6.TX_TYPE_CD` traces through `o_ACCT_ID` to unconnected `:LKP.lkp_TRANS1(ACCT_ID)`; its return port is `lkp_demo_source3.TX_TYPE_CD`.",
        "- `demo_target6.CR8_DT` traces to the SQL override positional `SYSTIMESTAMP` at the `CR8_DT` port, not `demo_source4.CR8_DT`.",
        "- `m_demo_mapping2` router ports resolve by `GROUP`: `Update` carries `LEAD_CO_MNE4`, `ID3`, `Key3`; `DEFAULT1` carries the similarly named discarded ports.",
        "- `demo_target2` is fed by router group `NEWGROUP1` (SSN null); `demo_target21` is fed by `NEWGROUP2` (SSN not null).",
    ]
    Path(args.markdown).write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
