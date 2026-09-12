from __future__ import annotations

import math
from datetime import datetime
from typing import Optional


def validate_timestamp(
    timestamp_iso_str: str, prev_timestamp: Optional[datetime]
) -> datetime:
    timestamp = datetime.fromisoformat(timestamp_iso_str)
    if prev_timestamp:
        if timestamp < prev_timestamp:
            raise ValueError("timestamp is before previous reading's timestamp")

        if timestamp == prev_timestamp:
            raise ValueError("timestamp equals previous reading's timestamp")
    return timestamp


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
