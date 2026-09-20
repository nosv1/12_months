# types one command, points it at the file, and gets the report

import argparse
import logging
from pathlib import Path

from telemetry_boss_fight.main import main

logger = logging.getLogger(__name__)


def handle_logging_level(log_info: None | str):
    if log_info is None:
        return

    logging.basicConfig(level=logging.INFO)
    logger.info("Logging now set to INFO")


def cli() -> None:
    parser = argparse.ArgumentParser(description="...")
    parser.add_argument(
        "telemetry_path",
        help="the path to the telemetry file",
        type=Path,
    )
    parser.add_argument(
        "-l", "--log_info", help="set logging level to 'info'", action="store_true"
    )

    args = parser.parse_args()
    handle_logging_level(args.log_info)
    main(args.telemetry_path)
