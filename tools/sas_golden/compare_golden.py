#!/usr/bin/env python3
"""Compare SAS golden-kit expectations with an actual run, scenario by scenario.

For every scenario in tests/golden/*/scenarios.json the expected directory is
  golden/                (real SAS output from run_golden.sas) when present, else
  expected_provisional/  (hand-derived, provisional)
or forced with --expected golden|provisional. Each pair of directories is
compared by tools/parity_diff.py, unchanged, with tools/keys/sas_keys.json.
Where a scenario's expected file repeats a key from sas_keys.json (fan-out
scenarios), parity_diff is also run with all columns as the key, and that
result decides the row (sorting on a non-unique key is not deterministic).

Actual outputs are either
  --actual-root DIR      DIR/<kit>/<scenario_id>/<TARGET>.csv  (e.g. dbt exports)
  --actual-subdir NAME   tests/golden/<kit>/scenarios/<id>/NAME/<TARGET>.csv

Examples:
  python3 tools/sas_golden/compare_golden.py --expected provisional --actual-subdir expected_provisional
  python3 tools/sas_golden/compare_golden.py --expected provisional --actual-subdir golden
  python3 tools/sas_golden/compare_golden.py --actual-root /tmp/dbt_exports

Exit code 0 only if every row is MATCH or ABSENT_OK.
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys
import tempfile

import pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PARITY = os.path.join(REPO, "tools", "parity_diff.py")
KEYS = os.path.join(REPO, "tools", "keys", "sas_keys.json")
PASS = {"MATCH", "ABSENT_OK"}


def run_parity(exp_dir, act_dir, keys_path, report_path):
    proc = subprocess.run(
        [sys.executable, PARITY, "--baseline", exp_dir, "--actual", act_dir, "--keys", keys_path, "--report", report_path],
        capture_output=True, text=True,
    )
    results, current = {}, None
    for line in proc.stdout.splitlines():
        m = re.match(r"^## (\S+)$", line)
        if m:
            current = m.group(1)
            results[current] = {"status": "MATCH", "detail": ""}
            continue
        if current is None:
            continue
        if "**MISSING in actual output**" in line:
            results[current] = {"status": "MISSING", "detail": "target not in actual"}
        elif "**MISMATCH**" in line:
            results[current]["status"] = "MISMATCH"
        elif line.startswith("  - ") and results[current]["status"] == "MISMATCH" and not results[current]["detail"]:
            results[current]["detail"] = line[4:]
    if proc.returncode not in (0, 1) or (not results and proc.returncode != 0):
        raise RuntimeError(f"parity_diff failed ({proc.returncode}): {proc.stderr.strip()[-500:]}")
    return results


def target_csvs(d):
    return sorted(f for f in glob.glob(os.path.join(d, "*.csv")))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--expected", choices=["auto", "golden", "provisional"], default="auto")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--actual-root")
    src.add_argument("--actual-subdir")
    ap.add_argument("--kit", action="append", help="limit to kit(s), e.g. sas_claims_processing")
    ap.add_argument("--keys", default=KEYS)
    ap.add_argument("--report-dir", help="keep parity_diff reports here (default: temp dir)")
    args = ap.parse_args()

    with open(args.keys) as fh:
        keys = {k.upper(): [c.upper() for c in v] for k, v in json.load(fh).items()}
    report_root = args.report_dir or tempfile.mkdtemp(prefix="compare_golden_")
    rows = []
    for manifest in sorted(glob.glob(os.path.join(REPO, "tests", "golden", "sas_*", "scenarios.json"))):
        kit_dir = os.path.dirname(manifest)
        kit = os.path.basename(kit_dir)
        if args.kit and kit not in args.kit:
            continue
        with open(manifest) as fh:
            scenarios = json.load(fh)
        for s in scenarios:
            sid = s["id"]
            sdir = os.path.join(kit_dir, "scenarios", sid)
            golden, prov = os.path.join(sdir, "golden"), os.path.join(sdir, "expected_provisional")
            if args.expected == "golden":
                exp_dir, exp_kind = golden, "golden"
            elif args.expected == "provisional":
                exp_dir, exp_kind = prov, "provisional"
            else:
                exp_dir, exp_kind = (golden, "golden") if os.path.isdir(golden) else (prov, "provisional")
            act_dir = os.path.join(args.actual_root, kit, sid) if args.actual_root else os.path.join(sdir, args.actual_subdir)

            if not os.path.isdir(exp_dir):
                # Scenarios whose expected outcome is "no target created" (no expected dir).
                produced = [os.path.basename(f)[:-4] for f in target_csvs(act_dir) if len(pd.read_csv(f)) > 0] if os.path.isdir(act_dir) else []
                rows.append((kit, sid, "(none)", exp_kind, "-", "ABSENT_FAIL" if produced else "ABSENT_OK", "-",
                             f"actual has rows in {produced}" if produced else s.get("expected_outcome", "no target expected")))
                continue
            if not os.path.isdir(act_dir):
                for f in target_csvs(exp_dir):
                    rows.append((kit, sid, os.path.basename(f)[:-4], exp_kind, "-", "NO_ACTUAL", "-", act_dir))
                continue

            rdir = os.path.join(report_root, kit, sid)
            os.makedirs(rdir, exist_ok=True)
            primary = run_parity(exp_dir, act_dir, args.keys, os.path.join(rdir, "parity.md"))
            allcol_keys, nrows = {}, {}
            for f in target_csvs(exp_dir):
                t = os.path.basename(f)[:-4].upper()
                df = pd.read_csv(f)
                df.columns = [c.strip().upper() for c in df.columns]
                nrows[t] = len(df)
                k = [c for c in keys.get(t, list(df.columns[:1])) if c in df.columns]
                if k and df.duplicated(subset=k).any():
                    allcol_keys[t] = list(df.columns)
            allcol = {}
            if allcol_keys:
                kp = os.path.join(rdir, "allcol_keys.json")
                with open(kp, "w") as fh:
                    json.dump(allcol_keys, fh)
                allcol = run_parity(exp_dir, act_dir, kp, os.path.join(rdir, "parity_allcol.md"))
            for t, res in sorted(primary.items()):
                status, detail, ac = res["status"], res["detail"], "-"
                if t in allcol_keys:
                    ac = allcol[t]["status"]
                    status = ac
                    detail = allcol[t]["detail"] or detail
                rows.append((kit, sid, t, exp_kind, str(nrows.get(t, "?")), status, ac, detail))

    head = ("KIT", "SCENARIO", "TARGET", "EXPECTED", "ROWS", "STATUS", "ALLCOL", "DETAIL")
    widths = [max(len(str(r[i])) for r in rows + [head]) for i in range(7)]
    print("  ".join(h.ljust(w) for h, w in zip(head, widths)) + "  " + head[7])
    for r in rows:
        print("  ".join(str(v).ljust(w) for v, w in zip(r, widths)) + "  " + str(r[7])[:200])
    bad = [r for r in rows if r[5] not in PASS]
    n_scen = len({(r[0], r[1]) for r in rows})
    print(f"\n{len(rows)} rows, {n_scen} scenarios, {len(rows) - len(bad)} pass, {len(bad)} fail. Reports: {report_root}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
