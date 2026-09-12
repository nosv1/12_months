import argparse
import json
import logging
from enum import Enum
from pathlib import Path
from typing import TextIO

from telemetry.analysis import Analysis
from telemetry.reading import Reading
from telemetry.robot import Robot
from telemetry.validator import (
    validate_battery,
    validate_temperature,
    validate_timestamp,
    validate_velocity,
)
from telemetry.warning import BatteryWarning, TemperatureWarning

logger = logging.getLogger(__name__)


def parser(telemetry_file: TextIO) -> dict[str, Robot]:
    class HEADERS(Enum):
        TIMESTAMP_IDX = 0
        ROBOT_ID_IDX = 1
        VELOCITY_IDX = 2
        BATTERY_IDX = 3
        TEMPERATURE_IDX = 4
        NUM_COLUMNS = 5

    robots_dict: dict[str, Robot] = {}

    for i, line in enumerate(telemetry_file.readlines()):
        if not i:
            continue

        parts = line.split(",")
        if not parts or len(parts) != HEADERS.NUM_COLUMNS.value:
            logger.warning("Line %d was missing data.", i + 1)
            robot.bad_readings.append((line, "line is missing data"))
            continue

        robot_id = parts[HEADERS.ROBOT_ID_IDX.value]
        if robot_id not in robots_dict:
            robots_dict[robot_id] = Robot(robot_id)
        robot = robots_dict[robot_id]

        try:
            timestamp = validate_timestamp(
                parts[HEADERS.TIMESTAMP_IDX.value],
                robot.readings[-1].timestamp if robot.readings else None,
            )
            velocity = validate_velocity(parts[HEADERS.VELOCITY_IDX.value])
            battery = validate_battery(parts[HEADERS.BATTERY_IDX.value])
            temperature = validate_temperature(parts[HEADERS.TEMPERATURE_IDX.value])

        except ValueError as ve:
            logger.warning("Line %d had a value error.", i + 1)
            robot.bad_readings.append((line, str(ve)))
            continue

        robot.readings.append(
            Reading(
                robot_id=robot_id,
                timestamp=timestamp,
                velocity=velocity,
                battery=battery,
                temperature=temperature,
            )
        )

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
        robots_dict = parser(telemetry_file)
        analysis_dict = {
            r_id: Analysis.analyze_robot(r, defined_warnings)
            for r_id, r in robots_dict.items()
        }
        # [r.plot(output_dir) for r in robots_dict.values()]
        report(output_dir, analysis_dict)


if __name__ == "__main__":
    main()
