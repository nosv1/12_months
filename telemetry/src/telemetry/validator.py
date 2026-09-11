from __future__ import annotations

from datetime import datetime
from typing import Optional


class Validator:
    def __init__(self, is_valid: bool, msg: Optional[str] = None):
        self.is_valid = is_valid
        self.msg = msg

    @staticmethod
    def validate_timestamp(
        timestamp_iso_str: str, prev_timestamp: Optional[datetime]
    ) -> tuple[Validator, Optional[datetime]]:
        timestamp = datetime.fromisoformat(timestamp_iso_str)
        if prev_timestamp:
            if timestamp < prev_timestamp:
                return (
                    Validator(
                        False, "timestamp is before previous reading's timestamp"
                    ),
                    None,
                )
            if timestamp == prev_timestamp:
                return (
                    Validator(False, "timestamp equals previous reading's timestamp"),
                    None,
                )
        return Validator(True), timestamp

    @staticmethod
    def validate_float(float_str: str) -> tuple[Validator, Optional[float]]:
        if float_str.lower() == "nan":
            return Validator(False, "nan present"), None

        try:
            n = float(float_str)
            return Validator(True), n

        except ValueError:
            return (
                Validator(False, "ValueError - could not convert a value to float"),
                None,
            )

    @staticmethod
    def validate_velocity(velocity_str: str):
        validator, value = Validator.validate_float(velocity_str)
        return validator, value

    @staticmethod
    def validate_battery(battery_str: str):
        validator, value = Validator.validate_float(battery_str)
        if not validator.is_valid:
            return validator, value

        if not (0 <= value <= 100):
            return Validator(False, "battery is not within range [0-100]"), None

        return validator, value

    @staticmethod
    def validate_temperature(temperature_str: str):
        validator, value = Validator.validate_float(temperature_str)
        if not validator.is_valid:
            return validator, value

        if not (0 <= value):
            return Validator(False, "temperature is not reasonable"), None

        return validator, value
