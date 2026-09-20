from __future__ import annotations


class TelemetryException(Exception):
    def __init__(self, *args) -> None:
        super().__init__(*args)


##########           FLOAT           ##########


class ValueOutOfRangeError(TelemetryException):
    def __init__(self, field: str, value: float, range: tuple[float, float]):
        super().__init__(
            f"{field}'s value ({value}) was out its range: [{range[0]}, {range[1]}]"
        )


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


##########           TEMPERATURE           ##########


class TemperatureIsNotNumberError(TelemetryException):
    def __init__(self, value_str: str) -> None:
        super().__init__(f"Temperature value is not a number - {value_str}")


class TemperatureOutOfRangeError(ValueOutOfRangeError):
    def __init__(self, field: str, value: float, range: tuple[float, float]):
        super().__init__(field, value, range)
