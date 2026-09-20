from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from math import isnan
from typing import Any

from telemetry_boss_fight.accepted_reading import AcceptedReading
from telemetry_boss_fight.config import EXPECTED_HEADERS
from telemetry_boss_fight.errors import (
    BatteryIsNotNumberError,
    BatteryOutOfRangeError,
    InconsistentHeaderError,
    RowColumnCountError,
    TelemetryException,
    TemperatureIsNotNumberError,
    TemperatureOutOfRangeError,
    TimestampFormatError,
    UnknownError,
    ValueOutOfRangeError,
    ValueStrNotANumber,
    VelocityIsNotNumberError,
    VelocityOutOfRangeError,
)
from telemetry_boss_fight.rejected_reading import RejectedReading

##########           LINE           ##########


def validate_header_parts(header_parts: list[str]) -> list[str]:
    missing_parts: list[str] = []
    extra_parts: list[str] = []

    for header_field in header_parts:
        if header_field not in EXPECTED_HEADERS.as_str_set():
            extra_parts.append(header_field)

    unique_header_parts = set(header_parts)
    for known_header_value in EXPECTED_HEADERS.as_str_set():
        if known_header_value not in unique_header_parts:
            missing_parts.append(known_header_value)

    if missing_parts != [] or extra_parts != []:
        raise InconsistentHeaderError(
            expected_parts=list(EXPECTED_HEADERS.as_str_set()),
            actual_parts=header_parts,
            missing=missing_parts,
            extra=extra_parts,
        )

    return header_parts


##########           FLOAT           ##########


def validate_float(value_str: str) -> float:
    value = float(value_str)
    if isnan(value):
        raise ValueStrNotANumber("unknown", value_str)
    return value


##########           VALUE IN RANGE           ##########


def validate_in_range(value: float, range: tuple[float, float]) -> float:
    if range[0] <= value <= range[1]:
        return value
    raise ValueOutOfRangeError("unknown", value, range)


##########           TIMESTAMP           ##########


def validate_timestamp(timestamp_str: str) -> datetime:
    header = EXPECTED_HEADERS.TIMESTAMP.value
    try:
        return datetime.fromisoformat(timestamp_str)

    except ValueError as err:
        raise TimestampFormatError(timestamp_str) from err

    except Exception as err:
        raise UnknownError(header.header, timestamp_str) from err


##########           VELOCITY           ##########


def validate_velocity(velocity_str: str) -> float:
    header = EXPECTED_HEADERS.VELOCITY.value
    try:
        velocity = validate_float(velocity_str)

    except (ValueStrNotANumber, ValueError) as err:
        raise VelocityIsNotNumberError(header.header, velocity_str) from err

    except Exception as err:
        raise UnknownError(header.header, velocity_str) from err

    try:
        if header.range is None:
            raise IndexError(f"{header.header} is missing a value range in config!")

        value_range = (header.range[0], header.range[1])
        velocity = validate_in_range(velocity, value_range)

    except ValueOutOfRangeError as err:
        raise VelocityOutOfRangeError(
            field=header.header,
            value=velocity,
            range=value_range,
        ) from err

    return velocity


##########           BATTERY           ##########


def validate_battery(battery_str: str) -> float:
    header = EXPECTED_HEADERS.BATTERY.value
    try:
        battery = validate_float(battery_str)

    except (ValueStrNotANumber, ValueError) as err:
        raise BatteryIsNotNumberError(header.header, battery_str) from err

    except Exception as err:
        raise UnknownError(header.header, battery_str) from err

    try:
        if header.range is None:
            raise IndexError(f"{header.header} is missing a value range in config!")

        value_range = (header.range[0], header.range[1])
        battery = validate_in_range(battery, value_range)

    except ValueOutOfRangeError as err:
        raise BatteryOutOfRangeError(
            field=header.header,
            value=battery,
            range=value_range,
        ) from err

    return battery


##########           TEMPERATURE           ##########


def validate_temperature(temperature_str: str) -> float:
    header = EXPECTED_HEADERS.TEMPERATURE.value
    try:
        temperature = validate_float(temperature_str)

    except (ValueStrNotANumber, ValueError) as err:
        raise TemperatureIsNotNumberError(header.header, temperature_str) from err

    except Exception as err:
        raise UnknownError(header.header, temperature_str) from err

    try:
        if header.range is None:
            raise IndexError(f"{header.header} is missing a value range in config!")

        value_range = (header.range[0], header.range[1])
        temperature = validate_in_range(temperature, value_range)

    except ValueOutOfRangeError as err:
        raise TemperatureOutOfRangeError(
            field=header.header,
            value=temperature,
            range=value_range,
        ) from err

    except Exception as err:
        raise UnknownError(header.header, temperature_str) from err

    return temperature


def validate_line_parts_count(
    line_parts: list[str], header_parts: list[str]
) -> list[str]:
    if len(line_parts) != len(header_parts):
        raise RowColumnCountError(len(header_parts), len(line_parts))
    return line_parts


def validate_parsed_line(
    fields: dict[str, str], poss_rejected_reading: RejectedReading
) -> AcceptedReading | RejectedReading:
    validated_values: dict[str, Any] = {}
    for header, part in fields.items():

        validator = HEADER_VALIDATORS[header]
        if validator is None:
            continue

        try:
            validated_values[header] = validator(part)

        except TelemetryException as te:
            poss_rejected_reading.errors.append(te)

    if poss_rejected_reading.errors != []:
        return poss_rejected_reading

    else:
        return AcceptedReading(fields=validated_values)


HEADER_VALIDATORS: dict[str, None | Callable] = {
    EXPECTED_HEADERS.TIMESTAMP.value.header: validate_timestamp,
    EXPECTED_HEADERS.ROBOT_ID.value.header: None,
    EXPECTED_HEADERS.VELOCITY.value.header: validate_velocity,
    EXPECTED_HEADERS.BATTERY.value.header: validate_battery,
    EXPECTED_HEADERS.TEMPERATURE.value.header: validate_temperature,
}
assert len(HEADER_VALIDATORS) == len(EXPECTED_HEADERS.as_str_set())
for header in HEADER_VALIDATORS:
    assert header in EXPECTED_HEADERS.as_str_set()
for header in EXPECTED_HEADERS.as_str_set():
    assert header in HEADER_VALIDATORS
