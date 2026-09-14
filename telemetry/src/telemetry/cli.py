from __future__ import annotations

import argparse
import logging
from pathlib import Path

from telemetry.main import main

logger = logging.getLogger(__name__)


def cli() -> None:
    arg_parser = argparse.ArgumentParser(description="telemetry report")

    arg_parser.add_argument(
        "telemetry_file_path",
        type=Path,
        help="the csv path of the telemetry file",
    )
    arg_parser.add_argument(
        "output_dir",
        type=Path,
        help="the directory path where the report will be saved",
    )
    args = arg_parser.parse_args()

    main(args.telemetry_file_path, args.output_dir)


if __name__ == "__main__":
    cli()
