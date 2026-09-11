from datetime import datetime
from typing import Optional


class Validator:
    def validate_timestamp(
        timestamp_iso_str: str, prev_timestamp: Optional[datetime]
    ) -> tuple[bool, Optional[str]]:
        timestamp = datetime.fromisoformat(timestamp_iso_str)
        if prev_timestamp and timestamp < prev_timestamp:
            return False, "timestamp is after previous reading's timestamp"
        return timestamp, None

    def validate_float(float_str: str):
        if float_str.lower() == "nan":
            return False, "nan present"

        try:
            n = float(float_str)
            return n, None
        except ValueError:
            return False, "ValueError - could not convert a value to float"

    def validate_velocity(velocity_str: str):
        valid_float, msg = Validator.validate_float(velocity_str)
        if not valid_float:
            return valid_float, msg
        return valid_float, None

    def validate_battery(battery_str):
        valid_float, msg = Validator.validate_float(battery_str)
        if not valid_float:
            return valid_float, msg

        if not (0 <= valid_float <= 100):
            return False, "battery is not within range [0-100]"

        return valid_float, None

    def validate_temperature(temperature_str):
        valid_float, msg = Validator.validate_float(temperature_str)
        if not valid_float:
            return valid_float, msg

        if not (0 <= valid_float):
            return False, "temperature is not reasonable"

        return valid_float, None
