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

# Documented anomalies found by inspection of the expressions (kept faithful,
# not fixed — the baseline and dbt models reproduce these behaviors exactly).
ANOMALY_NOTES = {
    "m_demo_mapping1": [
        "sq_demo_source4 SQL override selects SYSTIMESTAMP into the CR8_DT port, "
        "discarding demo_source4.CR8_DT. Pinned to 2024-01-31 in the migration.",
        "sq_demo_source4 selects STRCMP(ACCT_STAT_CD, TX_TYPE_CD) into the "
        "TX_TYPE_CD port but that port is never connected downstream — a no-op.",
        "exp_TRANS2.o_SELL_ST_DT = TO_DATE(TO_CHAR(SYSDATE),'DD/MM/YYYY') is "
        "self-inconsistent: TO_CHAR(SYSDATE) renders MM/DD/YYYY HH24:MI:SS, which "
        "cannot be parsed with format DD/MM/YYYY (month 31 is invalid on the run "
        "date 2024-01-31). The port yields NULL for every row.",
        "The aggregator agg_TRANS only aggregates SUM(TX_AMT); all other ports are "
        "pass-through, which in PowerCenter returns the LAST row per ACCT_ID group. "
        "Determinism is defined as last-by-TX_ID within each ACCT_ID.",
        "Router group DEFAULT1 is not connected to any target: rows with NULL "
        "ACCT_TYP satisfy neither condition and are dropped.",
        "demo_target3 declares PRODUCT_ID and PRODUCT_NO as number(15), but the "
        "source ports are strings and the synthesized product codes are "
        "alphanumeric; they are carried as strings in the migration. STD_COST, "
        "LIST_PRICE and demo_target6.CRDT_LN are numeric in the target "
        "definitions and are cast to numbers on load (PowerCenter's implicit "
        "string-to-number conversion).",
    ],
    "m_demo_mapping2": [
        "EXPTRANS.MD5_src = AES_DECRYPT(LEAD_CO_MNE1, SUBSTR(SHORT_NAME,1,3), 256) "
        "is self-inconsistent: LEAD_CO_MNE1 is the plaintext lookup value (never "
        "AES-encrypted) and the passphrase is only 3 characters, so AES_DECRYPT "
        "always fails and returns NULL.",
        "Because MD5_src is always NULL, MD5_tgt != MD5_src evaluates to NULL, so "
        "Changed_Flag = IIF(NOT ISNULL(Key) AND (MD5_tgt != MD5_src),'Update') is "
        "never 'Update'. The Update router group — and therefore the "
        "demo_target1_UPD instance — receives zero rows. Matched rows fall to the "
        "unconnected DEFAULT1 group and are dropped. This is preserved faithfully.",
        "SEQTRANS Current Value = 57: the first NEXTVAL generated is 57, "
        "incrementing by 1 per Insert row in source-file (ID) order.",
        "UPDTRANS applies DD_UPDATE to every row it receives (which is none).",
    ],
    "m_demo_mapping3": [
        "SQ_demo_source2 SQL override filters WHERE Member_Type_Code IS NOT NULL "
        "(rows with NULL Member_Type_Code never enter the pipeline).",
        "EXPTRANS.o_Relationship_to_Subscriber_Code_Label aborts the session "
        "(ABORT(...)) when the label is NULL; otherwise it is a pass-through. Seed "
        "data guarantees no NULL labels among filtered-in rows.",
        "Router: NEWGROUP1 (SSN IS NULL) loads instance demo_target2, so its "
        "Soc_Number column is NULL by construction; NEWGROUP2 (SSN IS NOT NULL) "
        "loads instance demo_target21. DEFAULT1 is unconnected.",
    ],
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
            for lkp_name in re.findall(r":LKP\.(\w+)", expr):
                lt = transforms.get(lkp_name)
                if lt is None:
                    continue
                attrs = lt["attributes"]
                ret = next((fn for fn, fi in lt["fields"].items()
                            if "RETURN" in (fi.get("porttype") or "")), None)
                steps.append(
                    f"{lkp_name} [unconnected lookup "
                    f"{attrs.get('Lookup table name')}.{ret} "
                    f"ON {attrs.get('Lookup condition')}]")
                sources.append(
                    f"{attrs.get('Lookup table name')}.{ret} (lookup)")
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

    return {
        "name": name,
        "sources": source_instances,
        "targets": target_instances,
        "transformations": {
            k: {"type": v["type"], "attributes": v["attributes"],
                "router_groups": v["groups"],
                "expressions": {fn: fi["expression"]
                                for fn, fi in sorted(v["fields"].items())
                                if fi["expression"] and fi["expression"] != fn}}
            for k, v in sorted(transforms.items())
        },
        "target_lineage": lineage,
        "notes": ANOMALY_NOTES.get(name, []),
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
        for tname, tinfo in sorted(m["transformations"].items()):
            attrs = tinfo["attributes"]
            groups = [g for g in tinfo["router_groups"] if g["type"] != "INPUT"]
            if not attrs and not groups:
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
        if m["notes"]:
            lines.append("### Notes (faithful anomalies, not fixed)")
            lines.append("")
            for n in m["notes"]:
                lines.append(f"- {n}")
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
