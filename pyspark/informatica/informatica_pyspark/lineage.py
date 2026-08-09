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
        for edge in self.edges:
            self.incoming.setdefault((edge.mapping, edge.to_instance, edge.to_field), []).append(edge)
            self.outgoing.setdefault((edge.mapping, edge.from_instance, edge.from_field), []).append(edge)

    def mappings(self):
        return self.root.findall(".//MAPPING")

    def mapping_names(self):
        return [m.attrib["NAME"] for m in self.mappings()]

    def target_instances(self, mapping: str):
        mp = next(m for m in self.mappings() if m.attrib["NAME"] == mapping)
        return [i.attrib for i in mp.findall("./INSTANCE") if i.attrib.get("TYPE") == "TARGET"]

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

    def chain(self, mapping: str, instance: str, field: str) -> list[tuple[str, str, int | None]]:
        edges = self.incoming.get((mapping, instance, field), [])
        if not edges:
            # Router output ports are numbered copies of their input ports. The
            # XML has no intra-router CONNECTOR; collapse that implicit hop.
            match = re.match(r"^(.*?)(\d+)$", field)
            if instance.startswith("rtr_") and match:
                base_edges = self.incoming.get((mapping, instance, match.group(1)), [])
                if base_edges:
                    edge = base_edges[0]
                    return self.chain(mapping, edge.from_instance, edge.from_field)
            return [(instance, field, None)]
        result = [(instance, field, edges[0].line)]
        result.extend(self.chain(mapping, edges[0].from_instance, edges[0].from_field))
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
                    rendered = " <- ".join(
                        f"`{instance}.{port}`" + (f" [XML line {line}]" if line else "")
                        for instance, port, line in chain
                    )
                    rows.append(f"- `{field}`: {rendered}")
                rows.append("")
        return "\n".join(rows).rstrip() + "\n"


def generate_lineage() -> str:
    return Lineage().render()
