from __future__ import annotations

import argparse
import json
import logging
from collections.abc import Iterable
from pathlib import Path

from telemetry.analysis import Analysis
from telemetry.parser import parse_telemetry_lines
from telemetry.telemetry_warning import BatteryWarning, TemperatureWarning

logger = logging.getLogger(__name__)


def report(output_dir: Path, robot_analysis_dict: dict[str, Analysis]):
    output_dir.mkdir(parents=True, exist_ok=True)

    output_json = {}
    for r_id, analysis in robot_analysis_dict.items():
        output_json[r_id] = analysis.to_json()
        print(f"{r_id}: {json.dumps(output_json[r_id], indent=4)}")

    with (output_dir / "output.json").open("w") as output:
        json.dump(output_json, output, indent=4)


def main():
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

    telemetry_file_path: Path = args.telemetry_file_path
    output_dir: Path = args.output_dir

    defined_warnings = [
        BatteryWarning(min_battery=20),
        TemperatureWarning(max_temperature=60),
    ]
    with telemetry_file_path.open("r") as telemetry_file:
        telemetry_lines: Iterable[str] = telemetry_file.readlines()
        robots_dict = parse_telemetry_lines(telemetry_lines, headers_count=1)

    analysis_dict = {
        r_id: Analysis.analyze_robot(r, defined_warnings)
        for r_id, r in robots_dict.items()
    }
    # [r.plot(output_dir) for r in robots_dict.values()]
    report(output_dir, analysis_dict)


if __name__ == "__main__":
    main()
