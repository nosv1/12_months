from __future__ import annotations

from datetime import datetime


class TelemetryException(Exception):
    def __init__(self, *args) -> None:
        super().__init__(*args)


class UnknownError(TelemetryException):
    def __init__(self, field: str, value_str: str) -> None:
        super().__init__(f"{field} had an UNKNOWN error caused by '{value_str}'")


##########           FLOAT           ##########


class ValueOutOfRangeError(TelemetryException):
    def __init__(self, field: str, value: float, range: tuple[float, float]):
        super().__init__(
            f"{field}'s value ({value}) was out its range: [{range[0]}, {range[1]}]"
        )


class ValueStrNotANumber(TelemetryException):
    def __init__(self, field: str, value_str: str):
        value_str = "[no value]" if len(value_str) == 0 else value_str
        super().__init__(f"{field}'s was not a number - {value_str}")


##########           HEADER           ##########


class InconsistentHeaderError(TelemetryException):
    def __init__(
        self,
        expected_parts: list[str],
        actual_parts: list[str],
        missing: list[str],
        extra: list[str],
    ) -> None:
        super().__init__(
            f"The header was inconsistent with the expected header in config.py "
            f"\n\tconfig: {expected_parts}"
            f"\n\tactual: {actual_parts}"
            f"\n\tmissing: {missing}"
            f"\n\textra: {extra}"
        )


##########           LINE           ##########


class RowColumnCountError(TelemetryException):
    def __init__(self, expected: int, actual: int) -> None:
        super().__init__(
            f"The number of columns in the data row did not match the number of header values - Expected: {expected}, Actual: {actual}"
        )


##########           TIMESTAMP           ##########


class TimestampFormatError(TelemetryException):
    def __init__(self, timestamp_str: str):
        super().__init__(
            f"Timestamp is not in the ISO 8601, UTC format - {timestamp_str}"
        )


class TimestampsOutOfOrderError(TelemetryException):
    def __init__(self, robot_id: str, timestamp: datetime, prev_timestamp: datetime):
        super().__init__(
            f"{robot_id}'s had a timestamp appear out of order - current: {timestamp}, previous: {prev_timestamp}"
        )


class TimestampIdenticalError(TelemetryException):
    def __init__(self, robot_id: str, timestamp: datetime, prev_timestamp: datetime):
        super().__init__(
            f"{robot_id} had matching timestamps - {timestamp} = {prev_timestamp}"
        )


##########           VELOCITY           ##########


class VelocityIsNotNumberError(ValueStrNotANumber):
    def __init__(self, field: str, value_str: str) -> None:
        super().__init__(field, value_str)


class VelocityOutOfRangeError(ValueOutOfRangeError):
    def __init__(self, field: str, value: float, range: tuple[float, float]):
        super().__init__(field, value, range)


##########           BATTERY           ##########


class BatteryIsNotNumberError(ValueStrNotANumber):
    def __init__(self, field: str, value_str: str) -> None:
        super().__init__(field, value_str)


class BatteryOutOfRangeError(ValueOutOfRangeError):
    def __init__(self, field: str, value: float, range: tuple[float, float]):
        super().__init__(field, value, range)


##########           TEMPERATURE           ##########


class TemperatureIsNotNumberError(ValueStrNotANumber):
    def __init__(self, field: str, value_str: str) -> None:
        super().__init__(field, value_str)


class TemperatureOutOfRangeError(ValueOutOfRangeError):
    def __init__(self, field: str, value: float, range: tuple[float, float]):
        super().__init__(field, value, range)
