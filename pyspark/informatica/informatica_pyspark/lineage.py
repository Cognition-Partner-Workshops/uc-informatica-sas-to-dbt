"""CONNECTOR-graph lineage parser and deterministic documentation generator."""

import html
import re
from dataclasses import dataclass
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[3]
XML_PATH = ROOT / "legacy/informatica/wf_demo_mapping.XML"


def _attrs(line: str) -> dict[str, str]:
    return {k: html.unescape(v) for k, v in
            re.findall(r'([A-Za-z_][\w$]*)\s*=\s*"([^"]*)"', line)}


@dataclass(frozen=True)
class Edge:
    mapping: str
    from_instance: str
    from_field: str
    to_instance: str
    to_field: str
    line: int


class Lineage:
    def __init__(self, xml_path: Path = XML_PATH):
        self.xml_path = Path(xml_path)
        self.lines = self.xml_path.read_text().splitlines()
        self.root = ET.fromstring("\n".join(self.lines))
        self.edges: list[Edge] = []
        mapping = ""
        for line_no, line in enumerate(self.lines, 1):
            if "<MAPPING " in line:
                mapping = _attrs(line).get("NAME", "")
            if "<CONNECTOR " in line:
                a = _attrs(line)
                self.edges.append(Edge(mapping, a["FROMINSTANCE"], a["FROMFIELD"],
                                       a["TOINSTANCE"], a["TOFIELD"], line_no))
        self.incoming = {}
        self.outgoing = {}
        self.field_lines = {}
        for edge in self.edges:
            self.incoming.setdefault((edge.mapping, edge.to_instance, edge.to_field), []).append(edge)
            self.outgoing.setdefault((edge.mapping, edge.from_instance, edge.from_field), []).append(edge)
        mapping = ""
        for line_no, line in enumerate(self.lines, 1):
            if "<MAPPING " in line:
                mapping = _attrs(line).get("NAME", "")
            if "<TRANSFORMFIELD " in line:
                attrs = _attrs(line)
                if attrs.get("NAME"):
                    self.field_lines[(mapping, attrs.get("NAME"), attrs["NAME"])] = line_no

    def mappings(self):
        return self.root.findall(".//MAPPING")

    def mapping_names(self):
        return [m.attrib["NAME"] for m in self.mappings()]

    def target_instances(self, mapping: str):
        mp = next(m for m in self.mappings() if m.attrib["NAME"] == mapping)
        return [i.attrib for i in mp.findall("./INSTANCE") if i.attrib.get("TYPE") == "TARGET"]

    def instance_line(self, mapping: str, instance: str) -> int:
        start = next(i for i, line in enumerate(self.lines, 1)
                     if f'<MAPPING ' in line and f'NAME ="{mapping}"' in line)
        return next(i for i in range(start, len(self.lines) + 1)
                    if "<INSTANCE " in self.lines[i - 1] and
                    _attrs(self.lines[i - 1]).get("NAME") == instance)

    def session_bindings(self):
        bindings = []
        for line_no, line in enumerate(self.lines, 1):
            if "<SESSION " in line:
                attrs = _attrs(line)
                bindings.append((attrs["NAME"], attrs["MAPPINGNAME"], line_no))
        return bindings

    def target_fields(self, physical: str):
        target = next(t for t in self.root.findall(".//TARGET") if t.attrib["NAME"] == physical)
        return [f.attrib["NAME"] for f in sorted(target.findall("./TARGETFIELD"),
                                                    key=lambda x: int(x.attrib["FIELDNUMBER"]))]

    def transformations(self, mapping: str):
        mp = next(m for m in self.mappings() if m.attrib["NAME"] == mapping)
        return {t.attrib["NAME"]: t for t in mp.findall("./TRANSFORMATION")}

    def expression(self, mapping: str, transformation: str, port: str) -> str:
        t = self.transformations(mapping)[transformation]
        return next(f.attrib.get("EXPRESSION", "") for f in t.findall("./TRANSFORMFIELD")
                    if f.attrib["NAME"] == port)

    def _field(self, mapping: str, instance: str, field: str):
        transformation = self.transformations(mapping).get(instance)
        if transformation is None:
            return None
        return next((f for f in transformation.findall("./TRANSFORMFIELD")
                     if f.attrib.get("NAME") == field), None)

    def lookup_details(self, mapping: str, instance: str) -> dict[str, str | int]:
        transformation = self.transformations(mapping)[instance]
        attrs = {a.attrib["NAME"]: a.attrib.get("VALUE", "")
                 for a in transformation.findall("./TABLEATTRIBUTE")}
        line_numbers = {}
        for line_no, line in enumerate(self.lines, 1):
            if f'<TRANSFORMATION ' in line and f'NAME ="{instance}"' in line:
                start = line_no
                break
        else:
            start = 1
        for name in ("Lookup table name", "Lookup condition", "Lookup policy on multiple match"):
            line_numbers[name] = next(
                (n for n in range(start, len(self.lines) + 1)
                 if f'NAME ="{name}"' in self.lines[n - 1]), start)
        return {
            "table": attrs.get("Lookup table name", ""),
            "condition": attrs.get("Lookup condition", ""),
            "policy": attrs.get("Lookup policy on multiple match", ""),
            "table_line": line_numbers["Lookup table name"],
            "condition_line": line_numbers["Lookup condition"],
            "policy_line": line_numbers["Lookup policy on multiple match"],
        }

    def router_details(self, mapping: str, instance: str, field: str) -> dict[str, str] | None:
        transformation = self.transformations(mapping).get(instance)
        if transformation is None or transformation.attrib.get("TYPE") != "Router":
            return None
        port = self._field(mapping, instance, field)
        if port is None or not port.attrib.get("REF_FIELD"):
            return None
        group_name = port.attrib.get("GROUP", "")
        group = next((g for g in transformation.findall("./GROUP")
                      if g.attrib.get("NAME") == group_name), None)
        return {
            "group": group_name,
            "expression": group.attrib.get("EXPRESSION", "") if group is not None else "",
        }

    def lookup_call(self, mapping: str, instance: str, field: str) -> str | None:
        port = self._field(mapping, instance, field)
        expression = port.attrib.get("EXPRESSION", "") if port is not None else ""
        match = re.search(r":LKP\.([A-Za-z0-9_]+)\(", expression)
        return match.group(1) if match else None

    def chain(self, mapping: str, instance: str, field: str,
              incoming_line: int | None = None) -> list[tuple[str, str, int | None]]:
        edges = self.incoming.get((mapping, instance, field), [])
        if not edges:
            port = self._field(mapping, instance, field)
            ref_field = port.attrib.get("REF_FIELD") if port is not None else None
            if ref_field:
                ref_edges = self.incoming.get((mapping, instance, ref_field), [])
                result = [(instance, field, incoming_line)]
                if ref_edges:
                    edge = ref_edges[0]
                    result.append((instance, ref_field, edge.line))
                    result.extend(self.chain(mapping, edge.from_instance, edge.from_field,
                                             edge.line))
                return result
            return [(instance, field, incoming_line)]
        result = [(instance, field, edges[0].line)]
        result.extend(self.chain(mapping, edges[0].from_instance, edges[0].from_field,
                                 edges[0].line))
        return result

    def dead_ports(self, mapping: str) -> set[str]:
        output = set()
        for name, transformation in self.transformations(mapping).items():
            for port in transformation.findall("./TRANSFORMFIELD"):
                key = (mapping, name, port.attrib["NAME"])
                if key not in self.outgoing:
                    output.add(f"{name}.{port.attrib['NAME']}")
        return output

    def sq_position_table(self):
        transformation = self.transformations("m_demo_mapping1")["sq_demo_source4"]
        sql = next(a.attrib["VALUE"] for a in transformation.findall("./TABLEATTRIBUTE")
                   if a.attrib["NAME"] == "Sql Query")
        select = sql.split("FROM", 1)[0].split("SELECT", 1)[1].replace("\r\n", " ").replace("\n", " ")
        values, start, depth = [], 0, 0
        for index, char in enumerate(select):
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
            elif char == "," and depth == 0:
                values.append(select[start:index].strip())
                start = index + 1
        values.append(select[start:].strip())
        ports = [x.attrib["NAME"] for x in transformation.findall("./TRANSFORMFIELD")]
        return list(zip(range(1, len(ports) + 1), ports, values))

    def render(self) -> str:
        rows = ["# Informatica connector lineage", ""]
        for mapping in self.mapping_names():
            rows += [f"## {mapping}", ""]
            for target in self.target_instances(mapping):
                physical = target["TRANSFORMATION_NAME"]
                rows.append(f"### {target['NAME']} (`{physical}`)")
                for field in self.target_fields(physical):
                    chain = self.chain(mapping, target["NAME"], field)
                    rendered_parts = []
                    for instance, port, line in chain:
                        suffix = f" [XML line {line}]" if line else ""
                        router = self.router_details(mapping, instance, port)
                        if router:
                            suffix += (f" [GROUP {router['group']}; "
                                       f"EXPRESSION {router['expression'] or '<default>'}]")
                        transformation = self.transformations(mapping).get(instance)
                        if transformation is not None and transformation.attrib.get("TYPE") == "Lookup Procedure":
                            details = self.lookup_details(mapping, instance)
                            suffix += (f" [LOOKUP {details['table']} line {details['table_line']}; "
                                       f"CONDITION {details['condition']} line {details['condition_line']}; "
                                       f"POLICY {details['policy']} line {details['policy_line']}]")
                        lookup_name = self.lookup_call(mapping, instance, port)
                        if lookup_name:
                            details = self.lookup_details(mapping, lookup_name)
                            return_port = next(
                                field.attrib["NAME"]
                                for field in self.transformations(mapping)[lookup_name]
                                .findall("./TRANSFORMFIELD")
                                if "LOOKUP/RETURN" in field.attrib.get("PORTTYPE", "")
                            )
                            suffix += (f" [LOOKUP CALL {lookup_name} RETURN {return_port}; "
                                       f"TABLE {details['table']} line {details['table_line']}; "
                                       f"CONDITION {details['condition']} line {details['condition_line']}; "
                                       f"POLICY {details['policy']} line {details['policy_line']}]")
                        rendered_parts.append(f"`{instance}.{port}`{suffix}")
                    rendered = " <- ".join(rendered_parts)
                    rows.append(f"- `{field}`: {rendered}")
                rows.append("")
        return "\n".join(rows).rstrip() + "\n"


def generate_lineage() -> str:
    return Lineage().render()
