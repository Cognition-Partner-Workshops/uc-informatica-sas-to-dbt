#!/usr/bin/env python3
"""Generate tools/sas_golden/golden_plan.sas from tests/golden/*/scenarios.json.

The plan is plain SAS macro calls consumed by run_golden.sas, so the SAS host
needs no JSON parsing and every CSV is read with an explicit INPUT statement
(no PROC IMPORT type guessing). Column types are inferred once, here, from all
CSVs that share a table layout (seed, scenario inputs, expected outputs and
baseline/sas), so a column is typed the same way in every scenario.

Usage:
    python3 tools/sas_golden/build_plan.py            # rewrite golden_plan.sas
    python3 tools/sas_golden/build_plan.py --check    # exit 1 if it is stale
"""
import argparse
import csv
import glob
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PLAN = os.path.join(REPO, "tools", "sas_golden", "golden_plan.sas")
SEED = os.path.join(REPO, "legacy", "sas", "data", "csv")
BASELINE = os.path.join(REPO, "baseline", "sas")
PROGRAMS = os.path.join(REPO, "legacy", "sas", "programs")

# scenario input directory -> libref (librefs as assigned in legacy/sas/config/autoexec_local.sas)
DIR_LIBREF = {
    "oracle_dw": "ORA_DW",
    "teradata_dw": "TERA_DW",
    "raw_bank": "RAW_BANK",
    "raw_ins": "RAW_INS",
    "stg_bank": "STG_BANK",
    "stg_ins": "STG_INS",
    "curated": "CURATED",
    "reports": "REPORTS",
}
# Migration companion columns: not SAS variables, derived at export as put(<var>, <format>).
DESC_COLUMNS = {
    "ACCOUNT_TYPE_DESC": ("ACCOUNT_TYPE", "$ACCTTYPE."),
    "ACCOUNT_STATUS_DESC": ("ACCOUNT_STATUS", "$ACCTSTAT."),
    "RISK_RATING_DESC": ("RISK_RATING", "RISKRATE."),
    "CUSTOMER_SEGMENT_DESC": ("CUSTOMER_SEGMENT", "$CUSTSEG."),
    "REGION_CODE_DESC": ("REGION_CODE", "$REGION."),
    "CLAIM_STATUS_DESC": ("CLAIM_STATUS", "$CLMSTAT."),
    "POLICY_TYPE_DESC": ("POLICY_TYPE", "$POLTYPE."),
    "RISK_CATEGORY_DESC": ("RISK_CATEGORY", "$RISKCAT."),
}
DEFAULT_CURR_DT = "31JAN2024"
DEFAULT_PREV_YM = "202401"
DATE_PARAMS = ("proc_date", "score_date", "txn_date", "run_date", "val_date")

RE_DATE9 = re.compile(r"^\d{2}[A-Za-z]{3}\d{4}$")
RE_ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RE_DT = re.compile(r"^\d{2}[A-Za-z]{3}\d{4}:\d{2}:\d{2}:\d{2}$")
RE_NUM = re.compile(r"^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$")


def family(table):
    """Dated feeds (TXN_FEED_20240131, CLAIMS_FEED_20240115) share one layout."""
    return re.sub(r"_\d{8}$", "_YYYYMMDD", table.upper())


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.reader(fh))
    return (rows[0] if rows else []), rows[1:]


def value_kind(v):
    if RE_DT.match(v):
        return "datetime"
    if RE_DATE9.match(v):
        return "date9"
    if RE_ISO.match(v):
        return "iso"
    if RE_NUM.match(v) and not (len(v) > 1 and v[0] == "0" and v[1].isdigit()):
        return "num"
    return "char"


class Layouts:
    """Per (table family, column): set of value kinds and max byte length."""

    def __init__(self):
        self.kinds, self.maxlen = {}, {}

    def add(self, table, path):
        header, rows = read_csv(path)
        for i, col in enumerate(header):
            key = (family(table), col.strip().upper())
            kinds = self.kinds.setdefault(key, set())
            ml = self.maxlen.get(key, 1)
            for r in rows:
                v = r[i] if i < len(r) else ""
                if v.strip() == "":
                    continue
                kinds.add(value_kind(v.strip()))
                ml = max(ml, len(v.encode("utf-8")))
            self.maxlen[key] = ml

    def char_len(self, col):
        """One length per column name, so join/hash keys match across tables."""
        return max(n for (_, c), n in self.maxlen.items() if c == col.upper())

    def sas_type(self, table, col):
        kinds = self.kinds.get((family(table), col.upper()), set())
        if not kinds:  # all-empty column (e.g. prior-state LOAD_TIMESTAMP): use the same column elsewhere
            kinds = set().union(*(k for (_, c), k in self.kinds.items() if c == col.upper()))
        if not kinds or "char" in kinds:
            return "char"
        if kinds <= {"date9", "iso"}:
            return "date"
        if kinds == {"datetime"}:
            return "datetime"
        if kinds == {"num"}:
            return "num"
        return "char"


def file_informat(kind, values):
    if kind == "date":
        return "yymmdd10." if any(RE_ISO.match(v) for v in values) else "date9."
    return {"datetime": "datetime20.", "num": "best32."}.get(kind)


def sas_quote(s):
    return s.replace("%", "%%")


def program_librefs(program):
    with open(os.path.join(PROGRAMS, f"{program}.sas"), encoding="utf-8") as fh:
        src = fh.read().upper()
    return {m.group(2): m.group(1) for m in re.finditer(r"\b(TERA_DW|RAW_INS|RAW_BANK|ORA_DW|STG_BANK|STG_INS|CURATED|REPORTS)\.([A-Z_]+)\b", src)}, src


def target_libref(program_src, target):
    hits = sorted(set(re.findall(r"\b(STG_BANK|STG_INS|CURATED|REPORTS)\." + re.escape(target) + r"\b", program_src)))
    if len(hits) != 1:
        raise SystemExit(f"cannot resolve libref of target {target}: {hits}")
    return hits[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    kits = sorted(glob.glob(os.path.join(REPO, "tests", "golden", "sas_*", "scenarios.json")))
    layouts = Layouts()
    for d in os.listdir(SEED):
        for f in glob.glob(os.path.join(SEED, d, "*.csv")):
            layouts.add(os.path.basename(f)[:-4], f)
    for f in glob.glob(os.path.join(BASELINE, "*.csv")):
        layouts.add(os.path.basename(f)[:-4], f)
    for f in glob.glob(os.path.join(REPO, "tests", "golden", "sas_*", "scenarios", "*", "*", "**", "*.csv"), recursive=True):
        layouts.add(os.path.basename(f)[:-4], f)

    out = [
        "/* GENERATED by tools/sas_golden/build_plan.py from tests/golden/*/scenarios.json. Do not edit. */",
        "/* One block per scenario (gs_begin to gs_end); the gs_* macros are defined in run_golden.sas. */",
        "",
    ]
    n_scen = 0
    for manifest in kits:
        kit_dir = os.path.dirname(manifest)
        kit = os.path.basename(kit_dir)
        program = kit[len("sas_"):]
        refs, src = program_librefs(program)
        with open(manifest, encoding="utf-8") as fh:
            scenarios = json.load(fh)
        all_targets = []
        for s in scenarios:
            for t in s["targets"]:
                t = t.split(".")[-1].upper()
                if t not in all_targets:
                    all_targets.append(t)
        for s in scenarios:
            n_scen += 1
            sid, params = s["id"], s.get("params", {})
            curr_dt = next((params[p] for p in DATE_PARAMS if p in params and params[p]), None) or s.get("run_date") or DEFAULT_CURR_DT
            prev_ym = params.get("report_month") or DEFAULT_PREV_YM
            rel_scen = os.path.relpath(os.path.join(kit_dir, "scenarios", sid), REPO)
            out.append(f"/* ---- {kit} / {sid} ---- */")
            out.append(f"%gs_begin(program={program}, kit={kit}, id={sid}, curr_dt={curr_dt}, prev_ym={prev_ym}, scendir={rel_scen})")
            out.append("%include gsauto;")
            out.append("%include gsfmt;")
            out.append("%gs_params()")
            for f in sorted(glob.glob(os.path.join(kit_dir, "scenarios", sid, "inputs", "*", "*.csv"))):
                d, table = os.path.basename(os.path.dirname(f)), os.path.basename(f)[:-4].upper()
                libs = [DIR_LIBREF[d]]
                if refs.get(table) == "TERA_DW" and libs[0] != "TERA_DW":
                    libs.append("TERA_DW")
                header, rows = read_csv(f)
                specs, fmts, drops = [], [], []
                for i, col in enumerate(header):
                    col = col.strip().upper()
                    kind = layouts.sas_type(table, col)
                    vals = [r[i].strip() for r in rows if i < len(r) and r[i].strip()]
                    if kind == "char":
                        specs.append(f"{col} :$char{layouts.char_len(col)}.")
                    else:
                        specs.append(f"{col} :{file_informat(kind, vals)}")
                        if kind == "date":
                            fmts.append(f"{col} date9.")
                        elif kind == "datetime":
                            fmts.append(f"{col} datetime20.")
                    if col in DESC_COLUMNS:
                        drops.append(col)
                for lib in libs:
                    out.append(
                        f"%gs_input(lib={lib}, ds={table}, csv={os.path.relpath(f, REPO)}, "
                        f"spec=%str({' '.join(specs)}), fmt=%str({' '.join(fmts)}), drop={' '.join(drops)})"
                    )
            call = f"%{program}(" + ", ".join(f"{k}={sas_quote(v)}" for k, v in params.items()) + ")"
            out.append(f"%gs_prepare(call=%nrstr({call}))")
            out.append("%include gsprg / source2;")
            out.append("%gs_invoke()")
            out.append("%gs_after()")
            listed = {t.split(".")[-1].upper() for t in s["targets"]}
            for t in all_targets:
                bpath = os.path.join(BASELINE, f"{t}.csv")
                cols = [c.strip().upper() for c in read_csv(bpath)[0]]
                dates = [c for c in cols if layouts.sas_type(t, c) == "date"]
                desc = [f"{c}:{DESC_COLUMNS[c][0]}:{DESC_COLUMNS[c][1]}" for c in cols if c in DESC_COLUMNS]
                out.append(
                    f"%gs_export(lib={target_libref(src, t)}, ds={t}, listed={int(t in listed)}, "
                    f"cols={' '.join(cols)}, datecols={' '.join(dates)}, desc={' '.join(desc)})"
                )
            out.append("%gs_end()")
            out.append("")
    text = "\n".join(out)
    if args.check:
        with open(PLAN, encoding="utf-8") as fh:
            stale = fh.read() != text
        print("golden_plan.sas is " + ("STALE" if stale else "up to date"))
        sys.exit(1 if stale else 0)
    with open(PLAN, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"wrote {os.path.relpath(PLAN, REPO)}: {len(kits)} programs, {n_scen} scenarios")


if __name__ == "__main__":
    main()
