#!/usr/bin/env python3
"""Deterministic lineage extractor for the legacy SAS programs.

Parses every program under legacy/sas/programs/ (plus the PROC FORMAT
catalogs under legacy/sas/formats/) with a pragmatic structured/regex parser
and emits a machine-readable source-to-target mapping (STM) and a
human-readable STM document:

  docs/stm/sas_stm.json
  docs/stm/sas_stm.md

Per program the STM captures: input librefs/datasets, output datasets, macro
parameters with defaults, and step-level lineage — PROC SQL selects/joins/
where/group-by/having, DATA-step derived columns with their expressions and
guarding conditions, RETAIN/BY-group logic, hash-object lookups, PROC APPEND
targets, PROC MEANS aggregations, and PROC FORMAT recodes referenced by
FORMAT statements.

Usage:
    python3 tools/sas_lineage.py
"""

import json
import os
import re
from collections import OrderedDict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROGRAMS_DIR = os.path.join(REPO, "legacy", "sas", "programs")
FORMATS_DIR = os.path.join(REPO, "legacy", "sas", "formats")
OUT_JSON = os.path.join(REPO, "docs", "stm", "sas_stm.json")
OUT_MD = os.path.join(REPO, "docs", "stm", "sas_stm.md")

# Hand-written analyst annotations documenting semantics that a purely
# syntactic parse cannot decide (SAS missing-value comparison rules, global
# DROP-statement scope, non-deterministic timestamps, header/code mismatches).
AMBIGUITY_NOTES = {
    "load_customer_accounts": [
        "The `drop EXCEPTION_CODE EXCEPTION_DESC;` statement is a DATA-step "
        "statement (not a dataset option), so it applies to *both* output "
        "datasets — WORK.ACCT_EXCEPTIONS therefore does NOT contain the "
        "exception code/description columns; exception rows are copies of the "
        "account row at the time each rule fires.",
        "Exception rows are output *before* SNAPSHOT_DATE / LOAD_TIMESTAMP "
        "are assigned, so those columns are missing (null) on exception rows.",
        "LOAD_TIMESTAMP = datetime() is wall-clock and non-deterministic; it "
        "is excluded from the baseline and the migrated model.",
        "RAW_BANK.DAILY_RATES is declared as an input in the program header "
        "but never referenced in the code.",
        "An account row can fire multiple exception rules (e.g. HIGH_UTIL and "
        "NO_RISK), producing multiple identical rows in ACCT_EXCEPTIONS "
        "(identical because the code/description columns are dropped).",
    ],
    "daily_transaction_processing": [
        "PROC SQL uses SAS missing-value ordering: a missing RUNNING_BALANCE "
        "satisfies `RUNNING_BALANCE < 0`, so transactions on accounts absent "
        "from the snapshot (null balances) are classified OVERDRAFT — the "
        "ORPHAN_ACCOUNT branch is unreachable for them. The migrated SQL "
        "reproduces this with explicit IS NULL handling.",
        "Z-score statistics are computed from CURATED.DAILY_TRANSACTIONS "
        "*before* the day's feed is appended, i.e. from history only. STD() "
        "in PROC SQL is the sample standard deviation.",
        "PROC APPEND FORCE drops the enrichment columns not present in the "
        "existing CURATED.DAILY_TRANSACTIONS structure, so the final curated "
        "table keeps only the 10 original feed columns.",
        "Validation rules are sequential with RETURN: a row is rejected by "
        "the first failing rule only.",
    ],
    "credit_risk_scoring": [
        "Bureau join picks the latest SCORE_DATE per customer on or before "
        "the score date via a correlated subquery.",
        "WOE defaults for missing inputs: FICO→0.198, UTIL→0, DPD→0, AGE→0, "
        "LTV→0 (and LTV WOE applies only to MTG/AUTO/HELC).",
        "SCORE_TIMESTAMP = datetime() is non-deterministic and excluded from "
        "the baseline and migrated model.",
        "REPORTS.RISK_SUMMARY is PROC MEANS NWAY by ACCOUNT_TYPE × "
        "NEW_RISK_RATING; N_ACCOUNTS is the n of the first analysis variable "
        "(PD, never missing here).",
    ],
    "monthly_regulatory_reporting": [
        "SAS missing-value ordering: `LTV <= 0.80` is TRUE when LTV is "
        "missing, so MTG accounts without a LOAN_DETAILS match get risk "
        "weight 0.35.",
        "DAYS_PAST_DUE missing (no LOAN_DETAILS row) falls through every "
        "aging bucket to 'Unknown' (missing is not =0 and not >=1).",
        "The ORDER BY clauses affect display order only and are irrelevant "
        "to row-level parity.",
    ],
    "claims_processing": [
        "The hash object loads RAW_INS.POLICIES filtered to STATUS='ACTIVE'; "
        "a failed FIND (rc ne 0) covers both unknown and inactive policies. "
        "POLICY_ID is unique in the seed data so hash duplicate-key handling "
        "is not exercised.",
        "TERA_DW.FRAUD_INDICATORS is seeded as "
        "legacy/sas/data/csv/raw_ins/FRAUD_INDICATORS.csv (the insurance "
        "seed directory stands in for the Teradata libref).",
        "The `drop VALIDATION_ERROR rc;` statement applies to both step-1 "
        "outputs; WORK.CLAIMS_INVALID is WORK-only and not persisted.",
        "Adjudication rules are sequential with RETURN — first match wins. "
        "DENY (high fraud) rows go to the manual-review queue, not the "
        "auto-adjudicated set.",
        "$CLMSTAT. on CLAIM_STATUS is a display format; codes are stored. "
        "The migration adds an explicit CLAIM_STATUS_DESC column via a seed "
        "lookup implementing the format.",
    ],
    "policy_valuation": [
        "YTD_EARNED_PREMIUM uses intck('month', max(EFFECTIVE_DATE, "
        "01JAN2024), min(31JAN2024, EXPIRATION_DATE)) — month-boundary "
        "counting makes this 0 for every policy at the January valuation "
        "date, so YTD_EARNED_PREMIUM = 0, LOSS_RATIO and COMBINED_RATIO are "
        "missing, PREMIUM_ADEQUATE = 'N' for all rows and IBNR_ESTIMATE = 0. "
        "This is the faithful legacy semantics for run date 31JAN2024; the "
        "loss-ratio band logic only produces non-missing ratios for "
        "valuation dates later in the fiscal year.",
        "REPORTS.RESERVE_ADEQUACY is listed in the program header but never "
        "created anywhere in the code; it is not a real output.",
        "The MERGE is 1:1 by POLICY_ID (all inputs are aggregated or unique "
        "per policy); `if a` keeps in-force policies only.",
        "AGG_LOSS_RATIO / AGG_COMBINED_RATIO stay missing because "
        "TOTAL_EARNED sums to 0 (the `if TOTAL_EARNED > 0` guard fails).",
        "$POLTYPE./$RISKCAT. are display formats; migrated as explicit "
        "*_DESC columns via seed lookups.",
    ],
}

BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.S)


def strip_comments(text):
    return BLOCK_COMMENT.sub(" ", text)


def parse_header(text):
    m = BLOCK_COMMENT.search(text)
    header = m.group(0) if m else ""
    def grab(label):
        mm = re.search(label + r":\s*(.*?)(?=\n\s*\w[\w ]*:|\n=====|\Z)", header, re.S)
        if not mm:
            return []
        raw = mm.group(1)
        return [d for d in re.findall(r"[A-Z_]+\.[A-Z_0-9]+", raw)]
    purpose = re.search(r"Purpose:\s*(.*?)(?=\n\s*Inputs:)", header, re.S)
    return {
        "purpose": re.sub(r"\s+", " ", purpose.group(1)).strip() if purpose else "",
        "declared_inputs": grab("Inputs"),
        "declared_outputs": grab("Outputs"),
    }


def parse_macro(text):
    m = re.search(r"%macro\s+(\w+)\s*\(([^)]*)\)\s*;", text, re.I)
    if not m:
        return None
    params = []
    for part in m.group(2).split(","):
        part = part.strip()
        if not part:
            continue
        if "=" in part:
            name, default = part.split("=", 1)
            params.append({"name": name.strip(), "default": default.strip()})
        else:
            params.append({"name": part, "default": None})
    return {"name": m.group(1), "parameters": params}


def split_top_level(s, sep=","):
    parts, depth, cur, quote = [], 0, [], None
    for ch in s:
        if quote:
            cur.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in "'\"":
            quote = ch
            cur.append(ch)
        elif ch == "(":
            depth += 1
            cur.append(ch)
        elif ch == ")":
            depth -= 1
            cur.append(ch)
        elif ch == sep and depth == 0:
            parts.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
    if cur:
        parts.append("".join(cur).strip())
    return [p for p in parts if p]


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def parse_select_items(select_clause):
    cols = []
    for item in split_top_level(select_clause):
        item = norm(item)
        # strip trailing format=/length= attributes
        item = re.sub(r"\s+(format|length|informat|label)\s*=\s*\S+", "", item, flags=re.I)
        m = re.search(r"^(.*)\s+as\s+(\w+)$", item, re.I | re.S)
        if m:
            cols.append({"column": m.group(2).upper(), "expression": norm(m.group(1))})
        elif item == "*" or item.endswith(".*"):
            cols.append({"column": item.upper(), "expression": "pass-through (all columns)"})
        else:
            m2 = re.match(r"^(?:(\w+)\.)?(\w+)$", item)
            if m2:
                cols.append({"column": m2.group(2).upper(), "expression": item})
            else:
                cols.append({"column": item.upper(), "expression": item})
    return cols


SQL_KEYWORDS = r"(?:inner\s+join|left\s+join|right\s+join|full\s+join|join|where|group\s+by|having|order\s+by)"


def parse_sql_create(stmt):
    m = re.search(r"create\s+table\s+([\w.]+)\s+as\s+select\s+(.*?)\s+from\s+(.*)$",
                  stmt, re.I | re.S)
    if not m:
        return None
    target, select_clause, rest = m.group(1).upper(), m.group(2), m.group(3)

    def cut(pattern):
        mm = re.search(pattern, rest_holder[0], re.I | re.S)
        if not mm:
            return None
        val = rest_holder[0][mm.end():]
        nxt = re.search(r"\b" + SQL_KEYWORDS + r"\b", val, re.I)
        clause = val[:nxt.start()] if nxt else val
        rest_holder[0] = rest_holder[0][:mm.start()] + (val[nxt.start():] if nxt else "")
        return norm(clause)

    rest_holder = [rest]
    joins = []
    for jm in re.finditer(r"\b(inner|left|right|full)?\s*join\s+([\w.()'\"=<> ]+?)\s+on\s+(.*?)(?=\b(?:inner|left|right|full)?\s*join\b|\bwhere\b|\bgroup\s+by\b|\bhaving\b|\border\s+by\b|$)",
                          rest, re.I | re.S):
        table_alias = norm(jm.group(2))
        joins.append({
            "type": (jm.group(1) or "inner").lower(),
            "table": table_alias,
            "on": norm(jm.group(3)),
        })
    base_m = re.match(r"\s*([\w.]+)(?:\s+(?:as\s+)?(\w+))?", rest)
    base = norm(base_m.group(0)) if base_m else norm(rest)

    where = cut(r"\bwhere\b")
    group_by = cut(r"\bgroup\s+by\b")
    having = cut(r"\bhaving\b")
    order_by = cut(r"\border\s+by\b")

    return {
        "type": "proc_sql_create",
        "output": target,
        "from": base,
        "joins": joins,
        "where": where,
        "group_by": group_by,
        "having": having,
        "order_by": order_by,
        "columns": parse_select_items(select_clause),
    }


def parse_proc_sql(block):
    steps = []
    for stmt in split_top_level(block, ";"):
        stmt = stmt.strip()
        if re.match(r"create\s+table", stmt, re.I):
            parsed = parse_sql_create(stmt)
            if parsed:
                steps.append(parsed)
        elif re.match(r"insert\s+into", stmt, re.I):
            m = re.search(r"insert\s+into\s+([\w.]+)\s+select\s+(.*?)\s+from\s+([\w.]+)",
                          stmt, re.I | re.S)
            if m:
                steps.append({
                    "type": "proc_sql_insert",
                    "output": m.group(1).upper(),
                    "from": m.group(3).upper(),
                    "columns": parse_select_items(m.group(2)),
                })
    return steps


def parse_data_step(header_line, body):
    outputs = []
    for m in re.finditer(r"([\w.]+)\s*(?:\(([^)]*)\))?", header_line):
        name = m.group(1).upper()
        if name in ("DATA",):
            continue
        outputs.append({"dataset": name, "options": norm(m.group(2) or "")})

    step = {
        "type": "data_step",
        "outputs": [o["dataset"] for o in outputs],
        "output_options": {o["dataset"]: o["options"] for o in outputs if o["options"]},
        "sources": [],
        "by": None,
        "retain": [],
        "hash_lookups": [],
        "formats": {},
        "lengths": {},
        "drop": [],
        "keep": [],
        "derived_columns": [],
        "conditional_outputs": [],
    }

    stmts = split_top_level(body, ";")
    cond_stack = []
    last_cond = [None]
    for raw in stmts:
        stmt = norm(raw)
        if not stmt:
            continue
        low = stmt.lower()
        if low.startswith(("set ", "merge ")):
            step["sources"] += re.findall(r"[\w]+\.[\w&.]+|\bWORK\.\w+", stmt, re.I) or \
                               [t for t in re.findall(r"([\w.&]+)(?:\s*\(|\s|$)", stmt.split(None, 1)[1]) if t]
            step["sources"] = [s.upper() for s in dict.fromkeys(
                re.findall(r"[\w&]+\.[\w&]+", stmt))] or step["sources"]
            step["merge"] = low.startswith("merge ")
        elif low.startswith("by "):
            step["by"] = stmt[3:].strip().upper()
        elif low.startswith("retain "):
            step["retain"] += stmt.split()[1:]
        elif low.startswith("declare hash"):
            m = re.search(r"declare\s+hash\s+(\w+)\s*\((.*)\)", stmt, re.I | re.S)
            step["hash_lookups"].append({"object": m.group(1), "declare": norm(m.group(2)),
                                         "key": [], "data": []})
        elif re.match(r"\w+\.definekey", low):
            if step["hash_lookups"]:
                step["hash_lookups"][-1]["key"] += re.findall(r"'(\w+)'", stmt)
        elif re.match(r"\w+\.definedata", low):
            if step["hash_lookups"]:
                step["hash_lookups"][-1]["data"] += re.findall(r"'(\w+)'", stmt)
        elif low.startswith("format "):
            for fm in re.finditer(r"((?:\w+\s+)+)(\$?\w+\.[\d.]*)", stmt[7:]):
                for col in fm.group(1).split():
                    step["formats"][col.upper()] = fm.group(2)
        elif low.startswith("length "):
            for lm in re.finditer(r"(\w+)\s+(\$?\s*\d+)", stmt[7:]):
                step["lengths"][lm.group(1).upper()] = lm.group(2).replace(" ", "")
        elif low.startswith("drop "):
            step["drop"] += [c.upper() for c in stmt.split()[1:]]
        elif low.startswith("keep "):
            step["keep"] += [c.upper() for c in stmt.split()[1:]]
        elif low.startswith("if ") or low.startswith("else if ") or low == "else" or low.startswith("else "):
            _parse_conditional(stmt, step, cond_stack, last_cond)
        elif low == "end":
            if cond_stack:
                last_cond[0] = cond_stack.pop()
        elif low.startswith("output"):
            target = stmt.split()[1].upper() if len(stmt.split()) > 1 else "(all outputs)"
            step["conditional_outputs"].append({
                "target": target,
                "condition": " AND ".join(cond_stack) if cond_stack else None,
            })
        elif low.startswith("where "):
            step["where"] = stmt[6:].strip()
        elif re.match(r"^\w+\s*=", stmt) and not low.startswith("rc ="):
            var, expr = stmt.split("=", 1)
            step["derived_columns"].append({
                "column": var.strip().upper(),
                "expression": norm(expr),
                "condition": " AND ".join(cond_stack) if cond_stack else None,
            })
        elif re.match(r"^rc\s*=", low):
            step["derived_columns"].append({
                "column": "RC", "expression": norm(stmt.split("=", 1)[1]),
                "condition": None})
    return step


def _parse_conditional(stmt, step, cond_stack, last_cond):
    m = re.match(r"(?:else\s+)?if\s+(.*?)\s+then\s+(.*)$", stmt, re.I | re.S)
    if not m:
        if stmt.lower().startswith("else"):
            rest = stmt[4:].strip()
            cond = "NOT (" + (last_cond[0] or "prior condition") + ")"
            if rest.lower() == "do":
                cond_stack.append(cond)
            elif "=" in rest:
                var, expr = rest.split("=", 1)
                step["derived_columns"].append(
                    {"column": var.strip().upper(), "expression": norm(expr), "condition": cond})
        return
    cond, action = norm(m.group(1)), norm(m.group(2))
    prefix = "ELSE " if stmt.lower().startswith("else") else ""
    full_cond = prefix + cond
    last_cond[0] = full_cond
    if action.lower() == "do":
        cond_stack.append(full_cond)
    elif action.lower().startswith("output"):
        target = action.split()[1].upper() if len(action.split()) > 1 else "(all outputs)"
        step["conditional_outputs"].append({"target": target, "condition": full_cond})
    elif "=" in action:
        var, expr = action.split("=", 1)
        step["derived_columns"].append(
            {"column": var.strip().upper(), "expression": norm(expr), "condition": full_cond})


def parse_proc_append(block):
    m = re.search(r"base\s*=\s*([\w.]+)\s+data\s*=\s*([\w.]+)", block, re.I)
    if not m:
        return None
    return {"type": "proc_append", "output": m.group(1).upper(), "from": m.group(2).upper(),
            "force": "force" in block.lower()}


def parse_proc_means(block):
    data = re.search(r"data\s*=\s*([\w.]+)", block, re.I)
    cls = re.search(r"class\s+(.*?);", block, re.I | re.S)
    var = re.search(r"\bvar\s+(.*?);", block, re.I | re.S)
    out = re.search(r"output\s+out\s*=\s*([\w.]+)(?:\(([^)]*)\))?(.*?);", block, re.I | re.S)
    stats = []
    if out:
        for sm in re.finditer(r"(\w+)(?:\((\w+)\))?\s*=\s*(\w+)", out.group(3)):
            stats.append({"stat": sm.group(1).lower(), "var": (sm.group(2) or "").upper(),
                          "as": sm.group(3).upper()})
    return {
        "type": "proc_means",
        "from": data.group(1).upper() if data else None,
        "class": [c.upper() for c in cls.group(1).split()] if cls else [],
        "vars": [v.upper() for v in var.group(1).split()] if var else [],
        "output": out.group(1).upper() if out else None,
        "output_options": norm(out.group(2) or "") if out else "",
        "stats": stats,
        "nway": "nway" in block.lower(),
    }


def parse_program(path):
    text = open(path).read()
    header = parse_header(text)
    code = strip_comments(text)
    macro = parse_macro(code)

    steps = []
    # PROC SQL blocks
    for m in re.finditer(r"proc\s+sql\s*;(.*?)quit\s*;", code, re.I | re.S):
        steps += [dict(s, order=m.start()) for s in parse_proc_sql(m.group(1))]
    # DATA steps
    for m in re.finditer(r"\bdata\s+((?:[\w.]+\s*(?:\([^)]*\))?\s*)+);(.*?)\brun\s*;",
                         code, re.I | re.S):
        hdr = m.group(1)
        if hdr.strip().upper().startswith("_NULL_"):
            continue
        if re.match(r"\s*lib\s*=", hdr, re.I):
            continue
        step = parse_data_step(hdr, m.group(2))
        step["order"] = m.start()
        steps.append(step)
    # PROC APPEND
    for m in re.finditer(r"proc\s+append\s+(.*?);", code, re.I | re.S):
        s = parse_proc_append(m.group(0))
        if s:
            s["order"] = m.start()
            steps.append(s)
    # PROC MEANS
    for m in re.finditer(r"proc\s+means\s+(.*?)run\s*;", code, re.I | re.S):
        s = parse_proc_means(m.group(0))
        s["order"] = m.start()
        steps.append(s)

    steps.sort(key=lambda s: s["order"])
    for s in steps:
        s.pop("order", None)

    inputs = sorted({d for d in re.findall(
        r"\b(ORA_DW|RAW_BANK|RAW_INS|TERA_DW|CURATED|STG_BANK|STG_INS)\.([\w&]+)", code)
        if not d[1].startswith("&")} | set(
        tuple(x.split(".")) for x in re.findall(
            r"\b(?:RAW_BANK|RAW_INS)\.&\w+", code)))
    # datasets referenced via macro-substituted names (feed datasets)
    feeds = re.findall(r"%let\s+(?:txn_ds|feed_ds)\s*=\s*(\w+)_%sysfunc", code, re.I)

    outputs = sorted({f"{a}.{b}" for a, b in re.findall(
        r"(?:create\s+table|insert\s+into|base\s*=|out\s*=|data\s+)\s*"
        r"(STG_BANK|STG_INS|CURATED|REPORTS)\.(\w+)", code, re.I)})

    name = os.path.splitext(os.path.basename(path))[0]
    return {
        "program": name,
        "purpose": header["purpose"],
        "declared_inputs": header["declared_inputs"],
        "declared_outputs": header["declared_outputs"],
        "macro": macro,
        "inputs": sorted({".".join(t) if isinstance(t, tuple) else t for t in inputs}),
        "feed_dataset_patterns": [f + "_YYYYMMDD" for f in feeds],
        "persistent_outputs": outputs,
        "steps": steps,
        "notes": AMBIGUITY_NOTES.get(name, []),
    }


def parse_formats():
    catalogs = {}
    for fname in sorted(os.listdir(FORMATS_DIR)):
        if not fname.endswith(".sas"):
            continue
        text = strip_comments(open(os.path.join(FORMATS_DIR, fname)).read())
        for m in re.finditer(r"value\s+(\$?\w+)\s+(.*?);", text, re.I | re.S):
            name, body = m.group(1).upper(), m.group(2)
            mapping = OrderedDict()
            for em in re.finditer(r"([^=\n]+?)\s*=\s*'([^']*)'", body):
                key = norm(em.group(1)).strip("'\" ")
                mapping[key] = em.group(2)
            catalogs[name] = {"source_file": f"legacy/sas/formats/{fname}",
                              "mapping": mapping}
    return catalogs


def render_md(programs, formats):
    lines = ["# SAS Source-to-Target Mapping (STM)", "",
             "Generated by `tools/sas_lineage.py` from `legacy/sas/programs/*.sas` "
             "and `legacy/sas/formats/*.sas`. Run date pinned to **31JAN2024** "
             "(`&CURR_DT` in `legacy/sas/config/autoexec_local.sas`).", ""]
    for prog in programs:
        lines.append(f"## {prog['program']}")
        lines.append("")
        lines.append(f"**Purpose:** {prog['purpose']}")
        lines.append("")
        if prog["macro"]:
            params = ", ".join(
                f"`{p['name']}={p['default']}`" if p["default"] else f"`{p['name']}`"
                for p in prog["macro"]["parameters"])
            lines.append(f"**Macro:** `%{prog['macro']['name']}` — parameters: {params}")
            lines.append("")
        lines.append(f"**Inputs:** {', '.join('`%s`' % i for i in prog['inputs']) or '—'}"
                     + (f" (feed pattern: `{'`, `'.join(prog['feed_dataset_patterns'])}`)"
                        if prog["feed_dataset_patterns"] else ""))
        lines.append(f"**Persistent outputs:** "
                     f"{', '.join('`%s`' % o for o in prog['persistent_outputs'])}")
        lines.append("")
        lines.append("| Output Dataset | Column | Derivation | Source(s) |")
        lines.append("|---|---|---|---|")
        for step in prog["steps"]:
            for row in step_rows(step):
                lines.append("| " + " | ".join(cell.replace("|", "\\|") for cell in row) + " |")
        if prog["notes"]:
            lines.append("")
            lines.append("**Notes / ambiguities:**")
            for note in prog["notes"]:
                lines.append(f"- {note}")
        lines.append("")
    lines.append("## PROC FORMAT recodes")
    lines.append("")
    for name, cat in formats.items():
        lines.append(f"### {name} ({cat['source_file']})")
        lines.append("")
        lines.append("| Code | Label |")
        lines.append("|---|---|")
        for k, v in cat["mapping"].items():
            lines.append(f"| `{k}` | {v} |")
        lines.append("")
    return "\n".join(lines) + "\n"


def step_rows(step):
    rows = []
    t = step["type"]
    if t == "proc_sql_create" or t == "proc_sql_insert":
        srcs = [step.get("from") or ""]
        srcs += [j["table"] for j in step.get("joins", [])]
        src_txt = "; ".join(s for s in srcs if s)
        extra = []
        for j in step.get("joins", []):
            extra.append(f"{j['type']} join {j['table']} on {j['on']}")
        if step.get("where"):
            extra.append(f"where {step['where']}")
        if step.get("group_by"):
            extra.append(f"group by {step['group_by']}")
        if step.get("having"):
            extra.append(f"having {step['having']}")
        if extra:
            rows.append([step["output"], "*(step)*", "; ".join(extra), src_txt])
        for col in step["columns"]:
            rows.append([step["output"], col["column"], f"`{col['expression']}`", src_txt])
    elif t == "data_step":
        src_txt = ", ".join(step["sources"])
        outs = " / ".join(step["outputs"])
        meta = []
        if step.get("merge"):
            meta.append(f"MERGE by {step['by']}")
        elif step.get("by"):
            meta.append(f"BY {step['by']}")
        if step["retain"]:
            meta.append(f"RETAIN {' '.join(step['retain'])}")
        for h in step["hash_lookups"]:
            meta.append(f"hash {h['object']}({h['declare']}) key={','.join(h['key'])} "
                        f"data={','.join(h['data'])}")
        if step["drop"]:
            meta.append(f"DROP (all outputs): {' '.join(step['drop'])}")
        if step.get("where"):
            meta.append(f"WHERE {step['where']}")
        if meta:
            rows.append([outs, "*(step)*", "; ".join(meta), src_txt])
        for col in step["derived_columns"]:
            deriv = f"`{col['expression']}`"
            if col["condition"]:
                deriv = f"if `{col['condition']}` then " + deriv
            rows.append([outs, col["column"], deriv, src_txt])
        for out in step["conditional_outputs"]:
            rows.append([out["target"], "*(row output)*",
                         f"when `{out['condition']}`" if out["condition"] else "always",
                         src_txt])
        for colname, fmt in step["formats"].items():
            rows.append([outs, colname, f"display format `{fmt}`", src_txt])
    elif t == "proc_append":
        rows.append([step["output"], "*(all columns of base)*",
                     "PROC APPEND" + (" FORCE (extra columns dropped)" if step["force"] else ""),
                     step["from"]])
    elif t == "proc_means":
        stats_txt = ", ".join(f"{s['as']}={s['stat']}({s['var'] or 'first var'})"
                              for s in step["stats"])
        rows.append([step["output"] or "", "*(aggregate)*",
                     f"PROC MEANS {'NWAY ' if step['nway'] else ''}CLASS "
                     f"{' × '.join(step['class'])}; {stats_txt}",
                     step["from"] or ""])
    return rows


def main():
    programs = [parse_program(os.path.join(PROGRAMS_DIR, f))
                for f in sorted(os.listdir(PROGRAMS_DIR)) if f.endswith(".sas")]
    formats = parse_formats()

    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w") as fh:
        json.dump({"run_date": "31JAN2024", "programs": programs, "formats": formats},
                  fh, indent=2)
    with open(OUT_MD, "w") as fh:
        fh.write(render_md(programs, formats))
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
