from __future__ import annotations

import logging
import math
from collections.abc import Iterable
from datetime import datetime

from telemetry.parser import ParsedLine
from telemetry.reading import BadReading, Reading
from telemetry.robot import Robot

logger = logging.getLogger(__name__)


def validate_timestamp_format(timestamp_iso_str: str) -> datetime:
    return datetime.fromisoformat(timestamp_iso_str)


def validate_timestamp_order(timestamp: datetime, prev_timestamp: datetime):
    if timestamp < prev_timestamp:
        raise ValueError("timestamp is before previous reading's timestamp")

    if timestamp == prev_timestamp:
        raise ValueError("timestamp equals previous reading's timestamp")
    return True


def validate_float(float_str: str) -> float:
    value = float(float_str)
    if math.isnan(value):
        raise ValueError("nan present")

    return value


def validate_velocity(velocity_str: str) -> float:
    value = validate_float(velocity_str)
    if abs(value) >= 2:
        raise ValueError("velocity is out of maximum range [-2, 2]")
    return value


def validate_battery(battery_str: str) -> float:
    value = validate_float(battery_str)
    if not (0 <= value <= 100):
        raise ValueError("battery is not within range [0-100]")
    return value


def validate_temperature(temperature_str: str) -> float:
    value = validate_float(temperature_str)
    if not (0 <= value):
        raise ValueError("temperature is not reasonable")
    return value


def validate_parsed_line(parsed_line: ParsedLine) -> Reading:
    return Reading(
        robot_id=parsed_line.robot_id,
        timestamp=validate_timestamp_format(parsed_line.timestamp_str),
        velocity=validate_velocity(parsed_line.velocity_str),
        battery=validate_battery(parsed_line.battery_str),
        temperature=validate_temperature(parsed_line.temperature_str),
    )


def handle_value_error(parsed_line: ParsedLine, ve: ValueError) -> BadReading:
    logger.warning("Line %d had a value error - %s", parsed_line.line_number, str(ve))
    return BadReading(parsed_line.line_number, parsed_line.original_line, str(ve))


def validate_parsed_line_values(
    parsed_lines: Iterable[ParsedLine],
) -> tuple[list[Reading], list[BadReading]]:
    readings: list[Reading] = []
    bad_readings: list[BadReading] = []
    for parsed_line in parsed_lines:
        try:
            readings.append(validate_parsed_line(parsed_line))

        except ValueError as ve:
            bad_readings.append(handle_value_error(parsed_line, ve))

    return readings, bad_readings


def validate_robot_timestamps(
    parsed_lines: list[ParsedLine],
) -> tuple[list[ParsedLine], list[BadReading]]:
    bad_readings: list[BadReading] = []
    i = len(parsed_lines) - 1
    while i > 0:
        parsed_line = parsed_lines[i]
        prev_parsed_line = parsed_lines[i - 1]
        try:
            valid_timestamp = False
            valid_prev_timestamp = False
            try:
                timestamp = validate_timestamp_format(parsed_line.timestamp_str)
                valid_timestamp = True
            except ValueError as ve:
                bad_readings.append(handle_value_error(parsed_line, ve))

            try:
                prev_timestamp = validate_timestamp_format(
                    prev_parsed_line.timestamp_str
                )
                valid_prev_timestamp = True
            except ValueError as ve:
                bad_readings.append(handle_value_error(prev_parsed_line, ve))

            if valid_timestamp and valid_prev_timestamp:
                validate_timestamp_order(timestamp, prev_timestamp)

        except ValueError as ve:
            logger.warning(
                "Line %s had a value error - %s",
                parsed_line.line_number,
                ve,
            )
            bad_readings.append(
                BadReading(parsed_line.line_number, parsed_line.original_line, str(ve))
            )
            del parsed_lines[i]
        i -= 1

    return parsed_lines, bad_readings


def validate_parsed_robots(
    parsed_robots: dict[str, list[ParsedLine]],
) -> dict[str, Robot]:
    robots_dict: dict[str, Robot] = {}
    for robot_id, parsed_lines in parsed_robots.items():
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
