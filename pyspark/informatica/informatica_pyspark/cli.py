import argparse
import sys
from datetime import date

from .config import RunConfig
from .lineage import generate_lineage
from .workflow.runner import run_mapping, run_workflow, workflow_exit_code


def _config(args):
    return RunConfig(
        business_date=date(2024, 1, 31),
        io_mode=args.io,
        source_dir="legacy/informatica/data",
        target_dir=args.target_dir,
        source_variant=args.source_variant,
    )


def main(argv=None):
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    mapping = sub.add_parser("run-mapping")
    mapping.add_argument("mapping")
    mapping.add_argument("--io", choices=("local", "snowflake"), default="local")
    mapping.add_argument("--source-variant", choices=("normal", "abort"), default="normal")
    mapping.add_argument("--target-dir", default="out/pyspark/local")
    workflow = sub.add_parser("run-workflow")
    workflow.add_argument("--io", choices=("local", "snowflake"), default="local")
    workflow.add_argument("--source-variant", choices=("normal", "abort"), default="normal")
    workflow.add_argument("--target-dir", default="out/pyspark/local")
    lineage = sub.add_parser("lineage")
    lineage.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    if args.command == "lineage":
        with open(args.out, "w") as handle:
            handle.write(generate_lineage())
        return 0
    if args.command == "run-mapping":
        return run_mapping(args.mapping, _config(args))
    result = run_workflow(_config(args))
    return workflow_exit_code(result)


if __name__ == "__main__":
    sys.exit(main())
