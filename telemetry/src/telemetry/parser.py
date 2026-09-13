from __future__ import annotations

import logging
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Optional

from telemetry.reading import Reading
from telemetry.robot import Robot
from telemetry.validator import (
    validate_battery,
    validate_temperature,
    validate_timestamp,
    validate_velocity,
)

logger = logging.getLogger(__name__)


class MissingDataError(Exception):
    pass


@dataclass
class ParsedLine:
    TIMESTAMP_IDX = 0
    ROBOT_ID_IDX = 1
    VELOCITY_IDX = 2
    BATTERY_IDX = 3
    TEMPERATURE_IDX = 4
    NUM_COLUMNS = 5

    timestamp_str: str
    robot_id: str
    velocity_str: str
    battery_str: str
    temperature_str: str

    @staticmethod
    def parse_line(line: str) -> ParsedLine:
        parts = line.split(",")
        if len(parts) != ParsedLine.NUM_COLUMNS:
            raise MissingDataError("line is missing data")

        return ParsedLine(
            timestamp_str=parts[ParsedLine.TIMESTAMP_IDX],
            robot_id=parts[ParsedLine.ROBOT_ID_IDX],
            velocity_str=parts[ParsedLine.VELOCITY_IDX],
            battery_str=parts[ParsedLine.BATTERY_IDX],
            temperature_str=parts[ParsedLine.TEMPERATURE_IDX],
        )

    def validate(self, prev_reading: Optional[Reading]) -> Reading:
        return Reading(
            robot_id=self.robot_id,
            timestamp=validate_timestamp(
                self.timestamp_str,
                prev_reading.timestamp if prev_reading else None,
            ),
            velocity=validate_velocity(self.velocity_str),
            battery=validate_battery(self.battery_str),
            temperature=validate_temperature(self.temperature_str),
        )


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
            reading = parsed_line.validate(
                robot.readings[-1] if robot.readings else None
            )

        except ValueError as ve:
            logger.warning("Line %d had a value error - %s", i + 1, str(ve))
            robot.bad_readings.append((line, str(ve)))
            continue

        robot.readings.append(reading)

    return robots_dict
