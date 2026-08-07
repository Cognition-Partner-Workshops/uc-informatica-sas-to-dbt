import argparse
import logging
import sys
from dataclasses import replace

from .config import RunConfig, RunContext
from .io import CsvIO, SnowflakeIO
from .mappings import REGISTRY
from .session import build_spark
from .workflow import run_workflow


def _input_override(value):
    name, separator, path = value.partition("=")
    if not separator or not name or not path:
        raise argparse.ArgumentTypeError(
            "input override must be in the form name=path"
        )
    return name, path


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="pyspark/informatica/conf/local.yml")
    parser.add_argument(
        "--input-override",
        action="append",
        type=_input_override,
        default=[],
        metavar="NAME=PATH",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    mapping = sub.add_parser("mapping")
    mapping.add_argument("--name", required=True, choices=sorted(REGISTRY))
    sub.add_parser("workflow")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO)
    cfg = RunConfig.from_yaml(args.config)
    if args.input_override:
        cfg = replace(cfg, input_overrides=dict(args.input_override))
    spark = build_spark(cfg)
    io = CsvIO(spark, cfg) if cfg.io == "csv" else SnowflakeIO(spark, cfg)
    ctx = RunContext(cfg, spark, io)
    try:
        if args.command == "workflow":
            return run_workflow(ctx)
        outputs = REGISTRY[args.name].run(ctx)
        for instance, df in outputs.items():
            io.write(instance, df)
        return 0
    finally:
        spark.stop()


if __name__ == "__main__":
    sys.exit(main())
