#!/usr/bin/env python3
"""Deterministic reverse-engineering extractor for the PowerCenter export."""
import json
import os
import re
import xml.etree.ElementTree as ET

XML_PATH = os.path.join("legacy", "informatica", "wf_demo_mapping.XML")
OUT_JSON = os.path.join("docs", "stm", "informatica_stm.json")
OUT_MD = os.path.join("docs", "stm", "informatica_stm.md")
IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
QUALIFIED_RE = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\.([A-Za-z_][A-Za-z0-9_]*)\b")

INTERESTING_ATTRS = {
    "Source Qualifier": [
        "Sql Query", "User Defined Join", "Source Filter",
        "Number Of Sorted Ports", "Select Distinct", "Output is deterministic",
        "Output is repeatable",
    ],
    "Lookup Procedure": [
        "Lookup table name", "Lookup condition",
        "Lookup policy on multiple match", "Lookup Sql Override",
        "Lookup Source Filter", "Connection Information",
        "Lookup caching enabled", "Case Sensitive String Comparison",
        "Sorted Input", "Null ordering",
    ],
    "Sequence": ["Start Value", "Increment By", "End Value", "Current Value", "Cycle"],
    "Update Strategy": ["Update Strategy Expression", "Forward Rejected Rows"],
    "Aggregator": ["Sorted Input", "Transformation Scope"],
}


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


def clean_sql(text):
    return " ".join((text or "").split())


def sql_parts(sql):
    match = re.search(r"\bSELECT\s+(.*?)\s+\bFROM\b(.*)", sql or "", re.I | re.S)
    if not match:
        return [], None, None, None
    select = split_select_list(clean_sql(match.group(1)))
    remainder = clean_sql(match.group(2))
    order_by = None
    order_match = re.search(r"\bORDER\s+BY\s+(.+)$", remainder, re.I)
    if order_match:
        order_by = order_match.group(1).strip()
        remainder = remainder[:order_match.start()].strip()
    where = None
    where_match = re.search(r"\bWHERE\s+(.+)$", remainder, re.I)
    if where_match:
        where = where_match.group(1).strip()
        remainder = remainder[:where_match.start()].strip()
    join = None
    join_match = re.search(
        r"\b(?:INNER|LEFT|RIGHT|FULL(?:\s+OUTER)?)\s+JOIN\s+.+?\s+\bON\b\s+(.+)",
        remainder, re.I)
    if join_match:
        join = join_match.group(1).strip()
    return select, where, join, order_by


def attrs(element):
    return {child.get("NAME"): child.get("VALUE")
            for child in element.findall("ATTRIBUTE")}


def parse_sessions(root):
    result = {}
    source_formats = {
        source.get("NAME"): next(
            (attribute.get("VALUE")
             for attribute in source.findall("TABLEATTRIBUTE")
             if attribute.get("NAME") == "Datetime Format"), None)
        for source in root.find(".//FOLDER").findall("SOURCE")
    }
    for session in root.iter("SESSION"):
        info = {
            "name": session.get("NAME"),
            "mapping": session.get("MAPPINGNAME"),
            "attributes": attrs(session),
            "writers": [],
            "readers": [],
            "source_configs": {},
        }
        for ext in session.findall("SESSIONEXTENSION"):
            details = {
                "instance": ext.get("SINSTANCENAME"),
                "name": ext.get("NAME"),
                "type": ext.get("TYPE"),
                "attributes": attrs(ext),
                "connection": next(
                    (c.get("CONNECTIONNAME") or c.get("VARIABLE")
                     for c in ext.findall("CONNECTIONREFERENCE")), None),
            }
            if ext.get("TYPE") == "WRITER":
                info["writers"].append(details)
            elif ext.get("TYPE") in ("READER", "LOOKUPEXTENSION"):
                info["readers"].append(details)
            if ext.get("TRANSFORMATIONTYPE") == "Source Definition":
                flatfile = ext.find("FLATFILE")
                if flatfile is not None:
                    info["source_configs"][ext.get("SINSTANCENAME")] = dict(
                        flatfile.attrib)
        for instance in session.findall("SESSTRANSFORMATIONINST"):
            flatfile = instance.find("FLATFILE")
            if flatfile is not None:
                config = dict(flatfile.attrib)
                config["Datetime Format"] = source_formats.get(
                    instance.get("SINSTANCENAME"), "")
                info["source_configs"][instance.get("SINSTANCENAME")] = config
        result[session.get("MAPPINGNAME")] = info
    return result


def parse_workflow(root):
    workflow = root.find(".//WORKFLOW")
    if workflow is None:
        return {"name": None, "tasks": [], "links": []}
    return {
        "name": workflow.get("NAME"),
        "tasks": [dict(task.attrib) for task in workflow.findall("TASK")],
        "links": [dict(link.attrib) for link in workflow.findall("WORKFLOWLINK")],
    }


def parse(path):
    root = ET.parse(path).getroot()
    folder = root.find(".//FOLDER")
    global_sources = {}
    for source in folder.findall("SOURCE"):
        global_sources[source.get("NAME")] = {
            "database_type": source.get("DATABASETYPE"),
            "fields": [
                {"name": f.get("NAME"), "datatype": f.get("DATATYPE"),
                 "precision": f.get("PRECISION"), "scale": f.get("SCALE")}
                for f in source.findall("SOURCEFIELD")
            ],
            "flatfile": (dict(source.find("FLATFILE").attrib)
                         if source.find("FLATFILE") is not None else {}),
            "datetime_format": next(
                (a.get("VALUE") for a in source.findall("TABLEATTRIBUTE")
                 if a.get("NAME") == "Datetime Format"), None),
        }
    global_targets = {}
    for target in folder.findall("TARGET"):
        global_targets[target.get("NAME")] = {
            "fields": [
                {"name": f.get("NAME"), "datatype": f.get("DATATYPE"),
                 "precision": f.get("PRECISION"), "scale": f.get("SCALE"),
                 "key": f.get("KEYTYPE")}
                for f in target.findall("TARGETFIELD")
            ],
        }
    sessions = parse_sessions(root)
    mappings = [
        parse_mapping(mapping, global_sources, global_targets,
                      sessions.get(mapping.get("NAME"), {}))
        for mapping in folder.findall("MAPPING")
    ]
    mappings.sort(key=lambda item: item["name"])
    return {
        "repository_file": XML_PATH,
        "sources": global_sources,
        "targets": global_targets,
        "sessions": list(sessions.values()),
        "workflow": parse_workflow(root),
        "mappings": mappings,
    }


def parse_mapping(mapping, global_sources, global_targets, session):
    transforms = {}
    for transform in mapping.findall("TRANSFORMATION"):
        fields = {}
        for field in transform.findall("TRANSFORMFIELD"):
            fields[field.get("NAME")] = {
                "expression": field.get("EXPRESSION"),
                "porttype": field.get("PORTTYPE"),
                "group": field.get("GROUP"),
                "ref_field": field.get("REF_FIELD"),
                "datatype": field.get("DATATYPE"),
                "precision": field.get("PRECISION"),
                "scale": field.get("SCALE"),
                "expressiontype": field.get("EXPRESSIONTYPE"),
                "defaultvalue": field.get("DEFAULTVALUE"),
            }
        transform_attrs = {}
        for attribute in transform.findall("TABLEATTRIBUTE"):
            if attribute.get("NAME") in INTERESTING_ATTRS.get(
                    transform.get("TYPE"), []):
                transform_attrs[attribute.get("NAME")] = attribute.get("VALUE")
        transforms[transform.get("NAME")] = {
            "name": transform.get("NAME"),
            "type": transform.get("TYPE"),
            "fields": fields,
            "groups": [dict(group.attrib) for group in transform.findall("GROUP")],
            "attributes": transform_attrs,
        }

    instances = {}
    for instance in mapping.findall("INSTANCE"):
        instances[instance.get("NAME")] = {
            "name": instance.get("NAME"),
            "type": instance.get("TYPE"),
            "transformation_name": instance.get("TRANSFORMATION_NAME"),
            "transformation_type": instance.get("TRANSFORMATION_TYPE"),
            "associated_sources": [
                child.get("NAME")
                for child in instance.findall("ASSOCIATED_SOURCE_INSTANCE")
            ],
        }
    connectors = [
        {"from_instance": c.get("FROMINSTANCE"), "from_field": c.get("FROMFIELD"),
         "from_type": c.get("FROMINSTANCETYPE"), "to_instance": c.get("TOINSTANCE"),
         "to_field": c.get("TOFIELD"), "to_type": c.get("TOINSTANCETYPE")}
        for c in mapping.findall("CONNECTOR")
    ]
    incoming = {(c["to_instance"], c["to_field"]):
                (c["from_instance"], c["from_field"]) for c in connectors}

    def transform_of(instance_name):
        instance = instances.get(instance_name)
        return transforms.get(instance["transformation_name"]) if instance else None

    def override_for(instance_name):
        transform = transform_of(instance_name)
        if not transform or transform["type"] != "Source Qualifier":
            return {}
        sql = transform["attributes"].get("Sql Query", "")
        expressions, row_filter, join, order_by = sql_parts(sql)
        ports = [
            name for name, field in transform["fields"].items()
            if field.get("porttype") in ("INPUT/OUTPUT", "OUTPUT")
        ]
        return {
            "sql": sql,
            "row_filter": row_filter,
            "join": join,
            "order_by": order_by,
            "bindings": {
                ports[index]: {"position": index + 1, "expression": expression}
                for index, expression in enumerate(expressions)
                if index < len(ports)
            },
        }

    overrides = {instance: override_for(instance)
                 for instance in instances if override_for(instance).get("sql")}

    def lkp_return(transform):
        return next(
            (name for name, field in transform["fields"].items()
             if "LOOKUP/RETURN/OUTPUT" in (field.get("porttype") or "")), None)

    def lookup_call(expression):
        match = re.search(r":LKP\.([A-Za-z_][A-Za-z0-9_]*)\((.*?)\)", expression or "")
        if not match:
            return None
        transform = transforms.get(match.group(1))
        if not transform:
            return None
        table = transform["attributes"].get("Lookup table name")
        return {
            "transformation": match.group(1),
            "arguments": [arg.strip() for arg in split_select_list(match.group(2))],
            "table": table,
            "condition": transform["attributes"].get("Lookup condition"),
            "multiple_match_policy":
                transform["attributes"].get("Lookup policy on multiple match"),
            "return_port": lkp_return(transform),
            "return_source": f"{table}.{lkp_return(transform)}",
        }

    def trace(instance_name, field, depth=0):
        if depth > 30:
            return ["... (depth limit)"], []
        instance = instances.get(instance_name)
        if instance is None:
            return [f"{instance_name}.{field}"], []
        if instance["type"] == "SOURCE":
            return [f"{instance_name}.{field}"], [f"{instance_name}.{field}"]
        transform = transform_of(instance_name)
        if transform is None:
            return [f"{instance_name}.{field}"], []
        ttype = transform["type"]
        info = transform["fields"].get(field, {})
        if (ttype == "Source Qualifier" and
                field in overrides.get(instance_name, {}).get("bindings", {})):
            binding = overrides[instance_name]["bindings"][field]
            expression = binding["expression"]
            step = (f"{instance_name}.{field} = {expression} "
                    f"[SQL override position {binding['position']}]")
            qualified = [f"{table}.{port}" for table, port in
                         QUALIFIED_RE.findall(expression)]
            return [step], qualified or [f"literal/expression: {expression}"]
        if ttype == "Sequence":
            a = transform["attributes"]
            return [f"{instance_name}.{field} [sequence start={a.get('Start Value')} "
                    f"increment={a.get('Increment By')} current={a.get('Current Value')} "
                    f"cycle={a.get('Cycle')}]"], [f"{instance_name} (generated)"]
        if ttype == "Router" and info.get("ref_field"):
            group = info.get("group")
            group_info = next((g for g in transform["groups"]
                               if g.get("NAME") == group), {})
            condition = group_info.get("EXPRESSION") or "(default group)"
            step = f"{instance_name}.{field} [router group {group} WHERE {condition}]"
            upstream = incoming.get((instance_name, info["ref_field"]))
            if upstream:
                steps, sources = trace(upstream[0], upstream[1], depth + 1)
                return [step] + steps, sources
            return [step], []
        if ttype == "Lookup Procedure" and "LOOKUP" in (info.get("porttype") or ""):
            a = transform["attributes"]
            table = a.get("Lookup table name")
            step = (f"{instance_name}.{field} [lookup {table}.{field} "
                    f"ON {a.get('Lookup condition')}]")
            sources = [f"{table}.{field} (lookup)"]
            for port, pinfo in transform["fields"].items():
                if "INPUT" in (pinfo.get("porttype") or ""):
                    upstream = incoming.get((instance_name, port))
                    if upstream:
                        _, source_list = trace(upstream[0], upstream[1], depth + 1)
                        sources.extend(f"{source} (lookup key)" for source in source_list)
            return [step], sources
        expression = info.get("expression")
        call = lookup_call(expression)
        if call:
            step = (f"{instance_name}.{field} = {expression} "
                    f"[yields {call['return_source']}; lookup "
                    f"{call['transformation']} ON {call['condition']}; "
                    f"multiple-match {call['multiple_match_policy']}]")
            sources = [f"{call['return_source']} (lookup return)"]
            for argument in call["arguments"]:
                upstream = incoming.get((instance_name, argument))
                if upstream:
                    _, source_list = trace(upstream[0], upstream[1], depth + 1)
                    sources.extend(f"{source} (lookup key)" for source in source_list)
            return [step], sources
        if expression and expression != field:
            step = f"{instance_name}.{field} = {expression}"
            refs = [token for token in dict.fromkeys(IDENT_RE.findall(expression))
                    if token in transform["fields"] and token != field]
            steps, sources = [step], []
            for reference in refs:
                upstream = incoming.get((instance_name, reference))
                if upstream:
                    more_steps, more_sources = trace(
                        upstream[0], upstream[1], depth + 1)
                    steps.extend(more_steps)
                    sources.extend(more_sources)
            if not refs:
                sources.append(f"literal/expression: {expression}")
            return steps, sources
        steps = [f"{instance_name}.{field}"]
        upstream = incoming.get((instance_name, field))
        if upstream:
            more_steps, sources = trace(upstream[0], upstream[1], depth + 1)
            steps.extend(more_steps)
            return steps, sources
        return steps, []

    target_instances = sorted(
        instance["name"] for instance in instances.values()
        if instance["type"] == "TARGET")
    source_instances = sorted(
        instance["name"] for instance in instances.values()
        if instance["type"] == "SOURCE")
    lineage = {}
    for target in target_instances:
        target_table = instances[target]["transformation_name"]
        columns = []
        for field in global_targets.get(target_table, {}).get("fields", []):
            column = field["name"]
            upstream = incoming.get((target, column))
            if not upstream:
                columns.append({"column": column, "rule": "(not connected — NULL)",
                                "chain": [], "sources": []})
                continue
            chain, sources = trace(upstream[0], upstream[1])
            columns.append({
                "column": column, "rule": chain[0] if chain else "",
                "chain": chain, "sources": sorted(set(sources)),
            })
        lineage[target] = {"target_table": target_table, "columns": columns}

    physical_targets = {}
    for target in target_instances:
        physical_targets.setdefault(
            instances[target]["transformation_name"], []).append(target)
    for targets in physical_targets.values():
        targets.sort()

    lookup_details = []
    for transform_name, transform in sorted(transforms.items()):
        if transform["type"] != "Lookup Procedure":
            continue
        a = transform["attributes"]
        return_port = lkp_return(transform)
        table = a.get("Lookup table name")
        lookup_details.append({
            "transformation": transform_name,
            "table": table,
            "exists_in_export": table in set(global_sources) | set(global_targets),
            "condition": a.get("Lookup condition"),
            "multiple_match_policy": a.get("Lookup policy on multiple match"),
            "connection_information": a.get("Connection Information"),
            "lookup_caching_enabled": a.get("Lookup caching enabled"),
            "case_sensitive_string_comparison":
                a.get("Case Sensitive String Comparison"),
            "sorted_input": a.get("Sorted Input"),
            "null_ordering": a.get("Null ordering"),
            "return_port": return_port,
            "ports": list(transform["fields"]),
        })

    sql_overrides = []
    misleading_bindings = []
    for instance_name, override in sorted(overrides.items()):
        bindings = [
            {"position": detail["position"], "expression": detail["expression"],
             "port": port}
            for port, detail in override["bindings"].items()
        ]
        bindings.sort(key=lambda item: item["position"])
        table_by_port = {}
        for binding in bindings:
            qualified = QUALIFIED_RE.findall(binding["expression"])
            if qualified:
                table_by_port[binding["port"]] = qualified[0][0]
            if (not qualified or qualified[0][1] != binding["port"]):
                misleading_bindings.append({
                    "transformation": instance_name, "port": binding["port"],
                    "position": binding["position"],
                    "expression": binding["expression"], "severity": "high",
                    "reason": "bound expression is not table.port with the same port name",
                })
        sibling_tables = list(dict.fromkeys(table_by_port.values()))
        if len(sibling_tables) > 1:
            first_table = sibling_tables[0]
            for port, table in table_by_port.items():
                if table == first_table:
                    continue
                misleading_bindings.append({
                    "transformation": instance_name, "port": port,
                    "position": next(b["position"] for b in bindings
                                     if b["port"] == port),
                    "expression": f"{table}.{port}", "severity": "note",
                    "reason": f"same-named port comes from sibling table {table}, "
                    f"rather than sibling table {first_table}",
                })
        sql_overrides.append({
            "transformation": instance_name, "sql": override["sql"],
            "row_filter": override["row_filter"], "join": override["join"],
            "order_by": override["order_by"], "positional_bindings": bindings,
        })

    def lookup_call_for(transform_name, port, expression):
        call = lookup_call(expression)
        if call:
            misleading_bindings.append({
                "transformation": transform_name, "port": port,
                "expression": expression, "severity": "high",
                "reason": f"named port yields {call['return_source']}",
                "lookup": call,
            })
        return call

    unconnected_lkp_calls = []
    for transform_name, transform in sorted(transforms.items()):
        for port, field in transform["fields"].items():
            call = lookup_call_for(transform_name, port, field.get("expression"))
            if call:
                unconnected_lkp_calls.append({
                    **call, "transformation": transform_name,
                    "lookup_transformation": call["transformation"],
                    "port": port, "expression": field["expression"],
                })

    aggregator_groupby = {}
    for transform_name, transform in sorted(transforms.items()):
        if transform["type"] == "Aggregator":
            aggregator_groupby[transform_name] = [
                name for name, field in transform["fields"].items()
                if field.get("expressiontype") == "GROUPBY"
            ]

    router_details = []
    for instance_name, instance in sorted(instances.items()):
        transform = transform_of(instance_name)
        if not transform or transform["type"] != "Router":
            continue
        groups = []
        for group in transform["groups"]:
            if group.get("TYPE") == "INPUT":
                continue
            outputs = [
                field for field, info in transform["fields"].items()
                if info.get("group") == group.get("NAME")
            ]
            downstream = sorted(set(
                connector["to_instance"] for connector in connectors
                if connector["from_instance"] == instance_name and
                connector["from_field"] in outputs
            ))
            expression = group.get("EXPRESSION")
            references = []
            for token in IDENT_RE.findall(expression or ""):
                if token not in transform["fields"]:
                    continue
                source = incoming.get((instance_name, token))
                if source:
                    source_steps, _ = trace(source[0], source[1])
                    definition = " → ".join(source_steps)
                else:
                    definition = transform["fields"][token].get("expression") or token
                references.append({"port": token, "definition": definition,
                                   "chain": source_steps if source else [definition]})
            groups.append({
                "name": group.get("NAME"), "condition": expression,
                "expanded_condition": expression or "(default group — no condition)",
                "condition_references": references, "output_ports": outputs,
                "downstream_instances": downstream,
                "has_outgoing_connectors": bool(downstream),
            })
        router_details.append({
            "instance": instance_name, "transformation": transform["name"],
            "groups": groups,
            "evaluation": "PowerCenter evaluates output groups independently; a row can satisfy multiple groups.",
        })

    transformations = {}
    for transform_name, transform in sorted(transforms.items()):
        transformations[transform_name] = {
            "type": transform["type"], "attributes": transform["attributes"],
            "router_groups": transform["groups"],
            "expression_evaluation_order": list(transform["fields"]),
            "ports": [
                {"name": port, **field}
                for port, field in transform["fields"].items()
                if transform["type"] in ("Expression", "Aggregator")
            ],
            "expressions": {
                port: field["expression"]
                for port, field in transform["fields"].items()
                if field.get("expression") and field.get("expression") != port
            },
        }
    return {
        "name": mapping.get("NAME"), "sources": source_instances,
        "targets": target_instances,
        "source_configs": {
            source: {
                **global_sources.get(source, {}).get("flatfile", {}),
                "Datetime Format": global_sources.get(source, {}).get(
                    "datetime_format"),
                **session.get("source_configs", {}).get(source, {}),
            }
            for source in source_instances
            if global_sources.get(source, {}).get("flatfile")
            or source in session.get("source_configs", {})
        },
        "transformations": transformations, "target_lineage": lineage,
        "physical_target_instances": physical_targets,
        "lookup_details": lookup_details,
        "unconnected_lkp_calls": unconnected_lkp_calls,
        "sql_overrides": sql_overrides,
        "misleading_bindings": misleading_bindings,
        "router_details": router_details,
        "aggregator_groupby_ports": aggregator_groupby,
        "unpopulated_target_columns": {
            target: [column["column"] for column in info["columns"]
                     if not column["chain"]]
            for target, info in lineage.items()
        },
        "session": session,
    }


def md_value(value):
    return "`" + clean_sql(str(value)) + "`"


def write_md(stm, path):
    lines = [
        "# Informatica Source-to-Target Mapping (STM)", "",
        f"Derived deterministically from `{stm['repository_file']}` by "
        "`tools/informatica_lineage.py`.", "",
        "Business/run date is pinned to **2024-01-31** for all SYSDATE / "
        "SYSTIMESTAMP references.", "",
        "## Workflow and session execution order", "",
    ]
    for link in stm["workflow"]["links"]:
        condition = f" (condition `{link['CONDITION']}`)" if link["CONDITION"] else ""
        lines.append(f"- `{link['FROMTASK']}` → `{link['TOTASK']}`{condition}")
    lines += [
        "",
        "PowerCenter evaluates Router output groups independently rather than as "
        "an if/else chain. Mapping-specific session details below therefore "
        "determine execution order and pre-run lookup state.", "",
    ]
    for session in stm["sessions"]:
        lines += [f"### Session `{session['name']}` (mapping `{session['mapping']}`)",
                  "",
                  f"- Treat source rows as: `{session['attributes'].get('Treat source rows as')}`"]
        for writer in session["writers"]:
            attrs_ = writer["attributes"]
            flags = "; ".join(
                f"{key}={md_value(attrs_.get(key, ''))}"
                for key in ("Target load type", "Insert", "Update as Update",
                            "Update as Insert", "Update else Insert", "Delete",
                            "Truncate target table option", "Reject filename"))
            lines.append(f"- Writer `{writer['instance']}`: {flags}")
        for source, config in sorted(session["source_configs"].items()):
            lines.append(f"- Flat-file reader `{source}`: " +
                         "; ".join(f"{key}={md_value(config.get(key, ''))}"
                                   for key in ("SKIPROWS", "CONSECDELIMITERSASONE",
                                               "NULL_CHARACTER",
                                               "Datetime Format")))
        lines.append("")

    for mapping in stm["mappings"]:
        lines += [
            f"## Mapping `{mapping['name']}`", "",
            f"- Sources: {', '.join(md_value(s) for s in mapping['sources'])}",
            f"- Target instances: {', '.join(md_value(t) for t in mapping['targets'])}",
            "",
        ]
        if mapping["physical_target_instances"]:
            lines.append("Physical target instance groups: " + "; ".join(
                f"{md_value(table)} = {', '.join(instances)}"
                for table, instances in mapping["physical_target_instances"].items()))
            lines.append("")
        if mapping["sql_overrides"]:
            lines += ["### SQL overrides", ""]
            for override in mapping["sql_overrides"]:
                lines.append(f"- `{override['transformation']}` SQL: "
                             f"{md_value(override['sql'])}")
                for key in ("row_filter", "join", "order_by"):
                    if override[key]:
                        lines.append(f"  - {key}: {md_value(override[key])}")
                lines.append("- Positional bindings: " + "; ".join(
                    f"{b['position']} → {md_value(b['port'])} = "
                    f"{md_value(b['expression'])}"
                    for b in override["positional_bindings"]))
            lines.append("")
        if mapping["misleading_bindings"]:
            lines += ["### Misleading or name-sensitive bindings", ""]
            for item in mapping["misleading_bindings"]:
                detail = item["reason"]
                if item.get("lookup"):
                    detail += (f"; return port `{item['lookup']['return_port']}`, "
                               f"table `{item['lookup']['table']}`")
                lines.append(f"- **{item['severity']}** `{item['transformation']}."
                             f"{item['port']}` = {md_value(item['expression'])}: "
                             f"{detail}.")
            lines.append("")
        if mapping["lookup_details"]:
            lines += ["### Lookup details", ""]
            for lookup in mapping["lookup_details"]:
                lines.append(
                    f"- `{lookup['transformation']}`: table "
                    f"{md_value(lookup['table'])}; condition "
                    f"{md_value(lookup['condition'])}; multiple-match "
                    f"{md_value(lookup['multiple_match_policy'])}; connection "
                    f"{md_value(lookup['connection_information'])}; cache "
                    f"{md_value(lookup['lookup_caching_enabled'])}; case-sensitive "
                    f"{md_value(lookup['case_sensitive_string_comparison'])}; "
                    f"sorted input {md_value(lookup['sorted_input'])}; null ordering "
                    f"{md_value(lookup['null_ordering'])}; RETURN port "
                    f"{md_value(lookup['return_port']) if lookup['return_port'] else '(none — connected lookup, outputs flow through connectors)'}; exists in export "
                    f"**{lookup['exists_in_export']}**.")
                if lookup["connection_information"] == "$Target":
                    lines.append("  - `$Target` means the mapping's own target "
                                 "table and therefore pre-run target state.")
            lines.append("")
        for router in mapping["router_details"]:
            lines += [f"### Router `{router['instance']}`", "",
                      f"- {router['evaluation']}"]
            for group in router["groups"]:
                destinations = ", ".join(md_value(d) for d in
                                          group["downstream_instances"]) or "(none)"
                fate = "has" if group["has_outgoing_connectors"] else "has zero"
                lines.append(f"- Group `{group['name']}`: condition "
                             f"{md_value(group['condition'] or '(default group)')}; "
                             f"expanded `{group['expanded_condition']}`; output ports "
                             f"{', '.join(group['output_ports']) or '(none)'}; "
                             f"{fate} outgoing connectors; downstream {destinations}.")
                for reference in group["condition_references"]:
                    lines.append(f"  - `{reference['port']}` definition: "
                                 f"{' → '.join(reference['chain'])}")
                if not group["has_outgoing_connectors"]:
                    lines.append("  - Rows reaching this group are discarded.")
            lines.append("")
        for name, transform in mapping["transformations"].items():
            if transform["type"] not in ("Expression", "Aggregator") or not transform["ports"]:
                continue
            lines += [f"### Transformation `{name}` ({transform['type']})", "",
                      "Ports are rendered in XML order, which is PowerCenter's "
                      "variable evaluation order."]
            for port in transform["ports"]:
                if port.get("expression"):
                    lines.append(f"- `{port['name']}` ({port.get('porttype')}): "
                                 f"{md_value(port['expression'])}")
            if transform["type"] == "Aggregator":
                for key, value in transform["attributes"].items():
                    lines.append(f"- **{key}**: {md_value(value)}")
                groupby = mapping["aggregator_groupby_ports"].get(name, [])
                lines.append(f"- GROUPBY ports: {', '.join(groupby) or '(none)'}")
                lines.append("- Non-group-by pass-through ports yield the last row "
                             "received per group; with no GROUPBY port, one row is "
                             "returned for the whole input.")
            lines.append("")
        notes = []
        for call in mapping["unconnected_lkp_calls"]:
            notes.append(f"- Unconnected lookup call `{call['transformation']}."
                         f"{call['port']}` calling "
                         f"`{call['lookup_transformation']}`: "
                         f"{md_value(call['expression'])}; yields "
                         f"{md_value(call['return_source'])}, RETURN port "
                         f"{md_value(call['return_port'])}.")
        if mapping["unpopulated_target_columns"]:
            notes.append("- Target columns with no connector: " + "; ".join(
                f"{md_value(target)}: {', '.join(columns) or '(none)'}"
                for target, columns in mapping["unpopulated_target_columns"].items()))
        if notes:
            lines += ["### Notes", ""] + notes + [""]
        for target in mapping["targets"]:
            info = mapping["target_lineage"][target]
            lines += [f"### Target instance `{target}` (table `{info['target_table']}`)",
                      "",
                      "| Target | Target Column | Expression / Rule | Source(s) |",
                      "|---|---|---|---|"]
            for column in info["columns"]:
                chain = " → ".join(column["chain"]) if column["chain"] else column["rule"]
                source = "; ".join(column["sources"]) or "—"
                lines.append(f"| {target} | {column['column']} | "
                             f"{chain.replace('|', chr(92) + '|')} | "
                             f"{source.replace('|', chr(92) + '|')} |")
            lines.append("")
    with open(path, "w") as output:
        output.write("\n".join(lines) + "\n")


def main():
    stm = parse(XML_PATH)
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w") as output:
        json.dump(stm, output, indent=2, sort_keys=True)
        output.write("\n")
    write_md(stm, OUT_MD)
    print(f"wrote {OUT_JSON} and {OUT_MD}")


if __name__ == "__main__":
    main()
