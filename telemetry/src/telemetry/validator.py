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
    except ValueError:
        raise TimestampFormatError(timestamp_str)


def validate_timestamp_order(timestamp: datetime, prev_timestamp: datetime):
    if timestamp < prev_timestamp:
        raise TimestampOutOfOrderError(timestamp, prev_timestamp)

    if timestamp == prev_timestamp:
        raise TimestampIdenticalError(timestamp)
    return True


def validate_float(float_str: str) -> float:
    try:
        value = float(float_str)

    except ValueError:
        raise NotANumberError("", float_str)

    if math.isnan(value):
        raise NaNError("", float_str)

    return value


def validate_velocity(velocity_str: str) -> float:
    try:
        value = validate_float(velocity_str)
    except NotANumberError:
        raise VelocityNotANumberError(velocity_str)
    except NaNError:
        raise VelocityWasNaNError(velocity_str)

    if not abs(value) <= 2:
        raise VelocityOutOfRangeError(velocity_str)
    return value


def validate_battery(battery_str: str) -> float:
    try:
        value = validate_float(battery_str)
    except NotANumberError:
        raise BatteryNotANumberError(battery_str)
    except NaNError:
        raise BatteryWasNaNError(battery_str)

    if not (0 <= value <= 100):
        raise BatteryOutOfRangeError(battery_str)
    return value


def validate_temperature(temperature_str: str) -> float:
    try:
        value = validate_float(temperature_str)
    except NotANumberError:
        raise TemperatureNotANumberError(temperature_str)
    except NaNError:
        raise TemperatureWasNaNError(temperature_str)
    if not (-40 <= value <= 150):
        raise TemperatureOutOfRangeError(temperature_str)
    return value


def validate_parsed_line(parsed_line: ParsedLine) -> Reading:
    return Reading(
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
            except TimestampFormatError as te:
                bad_readings.append(handle_telemetry_exception(parsed_line, te))

            try:
                prev_timestamp = validate_timestamp_format(
                    prev_parsed_line.timestamp_str
                )
                valid_prev_timestamp = True
            except TimestampFormatError as te:
                bad_readings.append(handle_telemetry_exception(prev_parsed_line, te))

            if valid_timestamp and valid_prev_timestamp:
                validate_timestamp_order(timestamp, prev_timestamp)

        except (TimestampOutOfOrderError, TimestampIdenticalError) as te:
            bad_readings.append(handle_telemetry_exception(prev_parsed_line, te))

        except ValueError as ve:
            logger.warning(
                "Line %s had a value error - %s",
                parsed_line.line_number,
                ve,
            )
            bad_readings.append(
                BadReading(parsed_line.line_number, parsed_line.original_line, ve)
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
