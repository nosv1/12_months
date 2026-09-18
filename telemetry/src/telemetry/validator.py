from __future__ import annotations

import logging
import math
from collections.abc import Iterable
from datetime import datetime

from telemetry.exceptions import (
    BatteryNotANumberError,
    BatteryOutOfRangeError,
    BatteryWasNaNError,
    NaNError,
    NotANumberError,
    TelemetryException,
    TemperatureNotANumberError,
    TemperatureOutOfRangeError,
    TemperatureWasNaNError,
    TimestampFormatError,
    TimestampIdenticalError,
    TimestampOutOfOrderError,
    VelocityNotANumberError,
    VelocityOutOfRangeError,
    VelocityWasNaNError,
)
from telemetry.parser import ParsedLine
from telemetry.reading import BadReading, Reading
from telemetry.robot import Robot

logger = logging.getLogger(__name__)


def validate_timestamp_format(timestamp_str: str) -> datetime:
    try:
        return datetime.fromisoformat(timestamp_str)
    except ValueError as ve:
        raise TimestampFormatError(timestamp_str) from ve


def validate_timestamp_order(timestamp: datetime, prev_timestamp: datetime):
    if timestamp < prev_timestamp:
        raise TimestampOutOfOrderError(timestamp, prev_timestamp)

    if timestamp == prev_timestamp:
        raise TimestampIdenticalError(timestamp)
    return True


def validate_float(float_str: str) -> float:
    try:
        value = float(float_str)

    except ValueError as ve:
        raise NotANumberError("", float_str) from ve

    if math.isnan(value):
        raise NaNError("", float_str)

    return value


def validate_velocity(velocity_str: str) -> float:
    try:
        value = validate_float(velocity_str)
    except NotANumberError as nan:
        raise VelocityNotANumberError(velocity_str) from nan
    except NaNError as nan:
        raise VelocityWasNaNError(velocity_str) from nan

    if not abs(value) <= 2:
        raise VelocityOutOfRangeError(velocity_str)
    return value


def validate_battery(battery_str: str) -> float:
    try:
        value = validate_float(battery_str)
    except NotANumberError as nan:
        raise BatteryNotANumberError(battery_str) from nan
    except NaNError as nan:
        raise BatteryWasNaNError(battery_str) from nan

    if not (0 <= value <= 100):
        raise BatteryOutOfRangeError(battery_str)
    return value


def validate_temperature(temperature_str: str) -> float:
    try:
        value = validate_float(temperature_str)
    except NotANumberError as nan:
        raise TemperatureNotANumberError(temperature_str) from nan
    except NaNError as nan:
        raise TemperatureWasNaNError(temperature_str) from nan
    if not (-40 <= value <= 150):
        raise TemperatureOutOfRangeError(temperature_str)
    return value


def validate_parsed_line(parsed_line: ParsedLine) -> Reading:
    return Reading(
        line_number=parsed_line.line_number,
        robot_id=parsed_line.robot_id,
        timestamp=validate_timestamp_format(parsed_line.timestamp_str),
        velocity=validate_velocity(parsed_line.velocity_str),
        battery=validate_battery(parsed_line.battery_str),
        temperature=validate_temperature(parsed_line.temperature_str),
    )


def handle_telemetry_exception(
    parsed_line: ParsedLine, te: TelemetryException
) -> BadReading:
    logger.warning("Line %d had an exception - %s", parsed_line.line_number, str(te))
    return BadReading(parsed_line.line_number, parsed_line.original_line, te)


def validate_parsed_line_values(
    parsed_lines: Iterable[ParsedLine],
) -> tuple[list[Reading], list[BadReading]]:
    readings: list[Reading] = []
    bad_readings: list[BadReading] = []
    for parsed_line in parsed_lines:
        try:
            readings.append(validate_parsed_line(parsed_line))

        except TelemetryException as te:
            bad_readings.append(handle_telemetry_exception(parsed_line, te))
            continue

        try:
            if len(readings) > 1:
                validate_timestamp_order(readings[-1].timestamp, readings[-2].timestamp)

        except TelemetryException as te:
            readings.pop()
            bad_readings.append(handle_telemetry_exception(parsed_line, te))

    return readings, bad_readings


def validate_parsed_robots(
    parsed_robots: dict[str, list[ParsedLine]],
) -> dict[str, Robot]:
    robots_dict: dict[str, Robot] = {}
    for robot_id, parsed_lines in parsed_robots.items():
        robot = Robot(robot_id)
        robot.readings, new_bad_readings = validate_parsed_line_values(parsed_lines)
        robot.bad_readings += new_bad_readings
        robots_dict[robot_id] = robot

    return robots_dict
