from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from telemetry.analysis import Analysis
from telemetry.parser import ParsedLine, parse_lines
from telemetry.reader import read_file
from telemetry.reading import BadReading
from telemetry.robot import Robot
from telemetry.telemetry_warning import (
    BatteryWarning,
    TelemetryWarning,
    TemperatureWarning,
)
from telemetry.validator import validate_parsed_line_values, validate_robot_timestamps

logger = logging.getLogger(__name__)


def group_robots(
    parsed_lines: list[ParsedLine],
) -> dict[str, list[ParsedLine]]:
    parsed_robots_dict: dict[str, list[ParsedLine]] = {}
    for parsed_line in parsed_lines:
        if parsed_line.robot_id not in parsed_robots_dict:
            parsed_robots_dict[parsed_line.robot_id] = []
        parsed_robots_dict[parsed_line.robot_id].append(parsed_line)
    return parsed_robots_dict


def report(
    output_dir: Path,
    robot_analysis_dict: dict[str, Analysis],
    bad_readings: list[BadReading],
):
    output_dir.mkdir(parents=True, exist_ok=True)

    output_json = {}
    for r_id, analysis in robot_analysis_dict.items():
        output_json[r_id] = analysis.to_json()
        print(f"{r_id}: {json.dumps(output_json[r_id], indent=4)}")

    output_json["bad_readings"] = [br.to_json() for br in bad_readings]

    with (output_dir / "output.json").open("w") as output:
        json.dump(output_json, output, indent=4)


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


def get_robots_dict(
    parsed_robots_dict: dict[str, list[ParsedLine]],
) -> dict[str, Robot]:
    robots_dict: dict[str, Robot] = {}
    for robot_id, parsed_lines in parsed_robots_dict.items():
        robot = Robot(robot_id)
        validated_timestamp_lines, robot.bad_readings = validate_robot_timestamps(
            parsed_lines
        )

        robot.readings, new_bad_readings = validate_parsed_line_values(
            validated_timestamp_lines
        )
        robot.bad_readings += new_bad_readings
        robots_dict[robot_id] = robot

    return robots_dict


def get_analysis_dict(
    robots_dict: dict[str, Robot], defined_warnings: list[TelemetryWarning]
):
    return {
        r_id: Analysis.analyze_robot(r, defined_warnings)
        for r_id, r in robots_dict.items()
    }


def main(telemetry_file_path: Path, output_dir: Path) -> None:
    defined_warnings = [
        BatteryWarning(min_battery=20),
        TemperatureWarning(max_temperature=60),
    ]
    telemetry_lines = read_file(telemetry_file_path)
    parsed_lines, bad_readings = parse_lines(telemetry_lines, headers_count=1)
    parsed_robots_dict = group_robots(parsed_lines)
    robots_dict = get_robots_dict(parsed_robots_dict)
    analysis_dict = get_analysis_dict(robots_dict, defined_warnings)
    # [r.plot(output_dir) for r in robots_dict.values()]
    report(output_dir, analysis_dict, bad_readings)


if __name__ == "__main__":
    cli()
