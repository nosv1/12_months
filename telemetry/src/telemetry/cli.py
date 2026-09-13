from __future__ import annotations

import argparse
import json
import logging
from collections.abc import Iterable
from pathlib import Path

from telemetry.analysis import Analysis
from telemetry.parser import MissingDataError, ParsedLine
from telemetry.robot import Robot
from telemetry.telemetry_warning import BatteryWarning, TemperatureWarning
from telemetry.validator import validate_parsed_line

logger = logging.getLogger(__name__)


def parse_telemetry_lines(
    lines: Iterable[str], headers_count: int = 0
) -> dict[str, Robot]:
    # defining with unknown in case there is missing data in a telemetry line
    # it may be the case where robot id *is* inside the line, but it's also less
    # easy to assume robot id is in the correct index if there is missing information
    robots_dict: dict[str, Robot] = {"unknown": Robot("unknown")}

    for i, line in enumerate(lines):
        if i < headers_count:
            continue

        try:
            parsed_line = ParsedLine.parse_line(line)

        except MissingDataError:
            logger.warning("Line %d was missing data.", i + 1)
            robots_dict["unknown"].bad_readings.append((line, "line is missing data"))
            continue

        robot_id = parsed_line.robot_id
        if robot_id not in robots_dict:
            robots_dict[robot_id] = Robot(robot_id)
        robot = robots_dict[robot_id]

        try:
            reading = validate_parsed_line(
                parsed_line, robot.readings[-1] if robot.readings else None
            )

        except ValueError as ve:
            logger.warning("Line %d had a value error - %s", i + 1, str(ve))
            robot.bad_readings.append((line, str(ve)))
            continue

        robot.readings.append(reading)

    return robots_dict


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
