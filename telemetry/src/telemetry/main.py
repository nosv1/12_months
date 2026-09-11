import json
import os
import sys
from enum import Enum
from typing import TextIO

from telemetry.analysis import Analysis
from telemetry.reading import Reading
from telemetry.robot import Robot
from telemetry.validator import Validator
from telemetry.warning import BatteryWarning, TemperatureWarning


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
            print(f"WARNING: Line {i+1} was missing data.")
            continue

        robot_id = parts[HEADERS.ROBOT_ID_IDX.value]
        if robot_id not in robots_dict:
            robots_dict[robot_id] = Robot(robot_id)
        robot = robots_dict[robot_id]

        messages = []
        timestamp, msg = Validator.validate_timestamp(
            parts[HEADERS.TIMESTAMP_IDX.value],
            robot.readings[-1].timestamp if robot.readings else None,
        )
        if msg:
            messages.append(msg)

        velocity, msg = Validator.validate_velocity(parts[HEADERS.VELOCITY_IDX.value])
        if msg:
            messages.append(msg)

        battery, msg = Validator.validate_battery(parts[HEADERS.BATTERY_IDX.value])
        if msg:
            messages.append(msg)

        temperature, msg = Validator.validate_temperature(
            parts[HEADERS.TEMPERATURE_IDX.value]
        )
        if msg:
            messages.append(msg)

        if messages:
            robot.bad_readings.append([line, messages])
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


def report(output_dir: str, robot_analysis_dict: dict[str, Analysis]):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_json = {}
    for r_id, analysis in robot_analysis_dict.items():
        output_json[r_id] = analysis.to_json()
        print(f"{r_id}: {json.dumps(output_json[r_id], indent=4)}")

    with open(os.path.join(output_dir, "output.json"), "w") as output:
        json.dump(output_json, output, indent=4)


if __name__ == "__main__":
    telemetry_file_path = sys.argv[1]  ## python main.py <telemetry_path> <output_dir>
    output_dir = sys.argv[2]

    defined_warnings = [
        BatteryWarning(min_battery=20),
        TemperatureWarning(max_temperature=60),
    ]
    with open(telemetry_file_path, "r") as telemetry_file:
        robots_dict = parser(telemetry_file)
        analysis_dict = {
            r_id: Analysis.analyze_robot(r, defined_warnings)
            for r_id, r in robots_dict.items()
        }
        report(output_dir, analysis_dict)
        pass
