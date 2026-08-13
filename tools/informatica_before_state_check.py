#!/usr/bin/env python3
"""Smoke test the Informatica before-state tools for deterministic output."""
import difflib
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


EXPECTED = {
    Path("docs/stm/informatica_stm.json"),
    Path("docs/stm/informatica_stm.md"),
    Path("baseline/informatica/demo_target1_INS.csv"),
    Path("baseline/informatica/demo_target1_UPD.csv"),
    Path("baseline/informatica/demo_target2.csv"),
    Path("baseline/informatica/demo_target21.csv"),
    Path("baseline/informatica/demo_target3.csv"),
    Path("baseline/informatica/demo_target5.csv"),
    Path("baseline/informatica/demo_target6.csv"),
}
OUTPUT_ROOTS = (Path("docs/stm"), Path("baseline/informatica"))


def run_pass(repo_root, pass_root):
    shutil.copytree(repo_root, pass_root, ignore=shutil.ignore_patterns(".git"))
    for output_root in OUTPUT_ROOTS:
        shutil.rmtree(pass_root / output_root, ignore_errors=True)
    commands = [
        [sys.executable, "tools/informatica_lineage.py"],
        [sys.executable, "tools/informatica_baseline.py"],
    ]
    for command in commands:
        result = subprocess.run(
            command, cwd=pass_root, text=True, capture_output=True, check=False
        )
        if result.returncode:
            output = (result.stdout + result.stderr).strip()
            raise RuntimeError(f"{' '.join(command)} failed:\n{output}")


def generated_files(pass_root):
    files = set()
    for output_root in OUTPUT_ROOTS:
        root = pass_root / output_root
        if root.exists():
            files.update(path.relative_to(pass_root) for path in root.rglob("*")
                         if path.is_file())
    return files


def compare(pass_a, pass_b):
    files_a = generated_files(pass_a)
    files_b = generated_files(pass_b)
    problems = []
    if files_a != files_b:
        missing = sorted(files_a - files_b)
        extra = sorted(files_b - files_a)
        if missing:
            problems.append("pass 2 is missing: " + ", ".join(map(str, missing)))
        if extra:
            problems.append("pass 2 added: " + ", ".join(map(str, extra)))
    for path in sorted(files_a & files_b):
        first = (pass_a / path).read_bytes()
        second = (pass_b / path).read_bytes()
        if first == second:
            continue
        problems.append(f"{path} differs:")
        try:
            first_text = first.decode()
            second_text = second.decode()
        except UnicodeDecodeError:
            problems.append(f"  binary sizes: {len(first)} vs {len(second)} bytes")
        else:
            diff = difflib.unified_diff(
                first_text.splitlines(), second_text.splitlines(),
                fromfile="pass 1/" + str(path), tofile="pass 2/" + str(path),
                lineterm="",
            )
            problems.extend("  " + line for line in diff)
    return problems


def main():
    repo_root = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix="informatica-before-state-") as temp:
        temp_root = Path(temp)
        pass_a = temp_root / "pass-1"
        pass_b = temp_root / "pass-2"
        try:
            run_pass(repo_root, pass_a)
            run_pass(repo_root, pass_b)
        except RuntimeError as error:
            print(f"FAIL: {error}", file=sys.stderr)
            return 1

        files = generated_files(pass_a)
        missing = sorted(EXPECTED - files)
        empty = sorted(path for path in files
                       if not (pass_a / path).stat().st_size)
        problems = []
        if missing:
            problems.append("expected outputs missing: " + ", ".join(map(str, missing)))
        if empty:
            problems.append("expected outputs empty: " + ", ".join(map(str, empty)))
        problems.extend(compare(pass_a, pass_b))
        if problems:
            print("FAIL: Informatica before-state determinism check", file=sys.stderr)
            print("\n".join(problems), file=sys.stderr)
            return 1
        print("PASS: Informatica before-state tools are deterministic")
        print("  outputs: " + ", ".join(map(str, sorted(files))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
