import argparse
import os
import sys
from datetime import date

from .config import RunConfig
from .lineage import generate_lineage
from .workflow.runner import run_mapping, run_workflow, workflow_exit_code


def _snowflake_arg(args, name: str, env_name: str) -> str:
    value = getattr(args, name)
    return value if value is not None else os.environ.get(env_name, "")


def _config(args):
    return RunConfig(
        business_date=date(2024, 1, 31),
        io_mode=args.io,
        source_dir="legacy/informatica/data",
        target_dir=args.target_dir,
        source_variant=args.source_variant,
        account=_snowflake_arg(args, "account", "SNOWFLAKE_ACCOUNT"),
        user=_snowflake_arg(args, "user", "SNOWFLAKE_USER"),
        role=_snowflake_arg(args, "role", "SNOWFLAKE_ROLE"),
        warehouse=_snowflake_arg(args, "warehouse", "SNOWFLAKE_WAREHOUSE"),
        database=_snowflake_arg(args, "database", "SNOWFLAKE_DATABASE"),
        source_schema=_snowflake_arg(args, "source_schema", "SNOWFLAKE_SOURCE_SCHEMA"),
        target_schema=_snowflake_arg(args, "target_schema", "SNOWFLAKE_TARGET_SCHEMA"),
        baseline_schema=_snowflake_arg(args, "baseline_schema", "SNOWFLAKE_BASELINE_SCHEMA"),
        private_key_path=_snowflake_arg(
            args, "private_key_path", "SNOWFLAKE_PRIVATE_KEY_PATH"
        ),
    )


def _add_snowflake_args(parser):
    parser.add_argument("--account", default=None)
    parser.add_argument("--user", default=None)
    parser.add_argument("--role", default=None)
    parser.add_argument("--warehouse", default=None)
    parser.add_argument("--database", default=None)
    parser.add_argument("--source-schema", dest="source_schema", default=None)
    parser.add_argument("--target-schema", dest="target_schema", default=None)
    parser.add_argument("--baseline-schema", dest="baseline_schema", default=None)
    parser.add_argument("--private-key-path", dest="private_key_path", default=None)


def main(argv=None):
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    mapping = sub.add_parser("run-mapping")
    mapping.add_argument("mapping")
    mapping.add_argument("--io", choices=("local", "snowflake"), default="local")
    mapping.add_argument("--source-variant", choices=("normal", "abort"), default="normal")
    mapping.add_argument("--target-dir", default="out/pyspark/local")
    _add_snowflake_args(mapping)
    workflow = sub.add_parser("run-workflow")
    workflow.add_argument("--io", choices=("local", "snowflake"), default="local")
    workflow.add_argument("--source-variant", choices=("normal", "abort"), default="normal")
    workflow.add_argument("--target-dir", default="out/pyspark/local")
    _add_snowflake_args(workflow)
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
