from __future__ import annotations

import argparse
import datetime as dt
import logging
import sys

from .config import RunConfig
from .io import LocalCsvIO, SnowflakeIO
from .mappings import MAPPINGS
from .session import build_spark
from .workflow import run_mapping, run_workflow


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="informatica_pyspark")
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("run-mapping", "run-workflow"):
        sub = subparsers.add_parser(command)
        if command == "run-mapping":
            sub.add_argument("name", choices=sorted(MAPPINGS))
        sub.add_argument("--business-date", required=True)
        sub.add_argument("--io", choices=("local", "snowflake"), default="local")
        sub.add_argument("--data-dir", default="legacy/informatica/data")
        sub.add_argument("--out-dir", default="out")
        sub.add_argument("--account")
        sub.add_argument("--user")
        sub.add_argument("--role")
        sub.add_argument("--warehouse")
        sub.add_argument("--database")
        sub.add_argument("--src-schema")
        sub.add_argument("--run-schema")
    return parser


def _config(args: argparse.Namespace) -> RunConfig:
    return RunConfig(
        business_date=dt.date.fromisoformat(args.business_date),
        io_mode=args.io,
        data_dir=args.data_dir,
        out_dir=args.out_dir,
        account=args.account,
        user=args.user,
        role=args.role,
        warehouse=args.warehouse,
        database=args.database,
        src_schema=args.src_schema,
        run_schema=args.run_schema,
    )


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = _parser().parse_args(argv)
    try:
        cfg = _config(args)
        spark = build_spark(cfg)
        io = LocalCsvIO(spark, cfg) if cfg.io_mode == "local" else SnowflakeIO(spark, cfg)
        if args.command == "run-mapping":
            try:
                run_mapping(args.name, cfg, io)
            finally:
                spark.stop()
        else:
            run_workflow(cfg, io)
        return 0
    except Exception:
        logging.getLogger(__name__).exception("Informatica run failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
